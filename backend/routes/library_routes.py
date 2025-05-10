# library_routes.py

import random
from flask import request, jsonify
from flask_login import current_user, AnonymousUserMixin
from bleach import clean
from flask_executor import Executor
import concurrent.futures

from io import BytesIO

from openapi import moderate
from utils import mask_email, parse_group_structure
import database.library_handlers as lbh
import knowledge_net.library_generator as lgn
from images.library_imager import generate_images_task, save_image
from database.user_handler import increment_violations, is_within_limit, check_generation_allowed, mark_generation_done
from database.models import Library, LibraryFactoid, LibraryQuestion, db
from vector_processing.file_handler import process_document
from vector_processing.retrieval import query_and_respond_pinecone

def init_library_routes(app):

    executor = Executor(app)

    @app.route("/api/library/generate", methods=["POST"])
    def generate_library():
        
        # User checks
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        if not user_id:
            return jsonify(status="error", message="Must be logged in to generate libraries."), 403
        
        # Topic checks
        topic = request.form.get("topic")
        if not topic:
            return jsonify(status="error", message="No topic provided"), 400
        
        topic = clean(topic)

        if len(topic) > 70:
            return jsonify({"error": "Topic is too long. Maximum 200 characters allowed."}), 400
        if len(topic) < 4:
            return jsonify({"error": "Topic must be at least 4 characters."}), 400

        # Difficulty checks
        library_difficulty = request.form.get("libraryDifficulty")
        VALID_DIFFICULTIES = ["Easy", "Normal", "Hard"]
        if not library_difficulty:
            library_difficulty = "Normal"
        else:
            library_difficulty = clean(library_difficulty)
            if library_difficulty not in VALID_DIFFICULTIES:
                library_difficulty = "Normal"


        # Guide checks
        guide = request.form.get("guide")
        VALID_GUIDES = ["Azalea", "Irona", "Bubbles", "Sterling"]
        if guide:
            guide = clean(guide)
        if not guide or guide not in VALID_GUIDES:
            guide = random.choice(VALID_GUIDES)

        # Language & language difficulty checks
        language = request.form.get("language")
        if not language:
            language = "English"
        else:
            language = clean(language)

        language_difficulty = request.form.get("languageDifficulty")
        VALID_LANGUAGE_DIFFICULTIES = ["Easy", "Normal", "Hard"]
        if not language_difficulty:
            language_difficulty = "Normal"
        else:
            language_difficulty = clean(language_difficulty)
            if language_difficulty not in VALID_LANGUAGE_DIFFICULTIES:
                language_difficulty = "Normal"

        print(request.form.get("visibility"))
        is_public = request.form.get("visibility", "false").lower() == "true"

        # Extra context checks
        extra_context = request.form.get("extraContent")
        if extra_context:
            extra_context = clean(extra_context)
            if len(extra_context) > 200:
                return jsonify({"error": "Extra context is too long. Maximum 200 characters allowed."}), 400

        # Check for existing library
        if not extra_context:
            existing_library = lbh.get_library_id(topic, library_difficulty, language, language_difficulty, guide)
            if existing_library:
                # Now check if first room exists
                user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
                existing_content = lbh.retrieve_library_room_contents(existing_library, topic, user_id)
                if existing_content:
                    return jsonify(status="success", library_id=existing_library)
                else:
                    try:
                        # Generate room content asynchronously
                        room_future = executor.submit(lgn.generate_libroom_content, user_id, topic, existing_library)
                        room_contents = room_future.result()
                        lbh.save_library_room_contents(existing_library, topic, room_contents, user_id=user_id)
                        return jsonify(status="success", library_id=existing_library)
                    except Exception as e:
                        return jsonify(status="error", message=f"Failed to generate room content {e}"), 500
        
        groups = parse_group_structure()
        if groups:
            print("Parsed Groups:", groups)
        else:
            print("No groups provided.")

        try:
            selected_file = request.files.get("selectedFile").read()
            if not selected_file:
                return jsonify({"error": "No file provided (request.json)"}), 400

            if "selectedFile" not in request.files:
                print(request.files)
                return jsonify({"error": "No file provided (not in request.files)"}), 400
        except Exception as e:
            return jsonify({"error": f"Error reading file: {str(e)}"}), 400

        # Start moderation task
        content_for_moderation = topic
        if extra_context:
            content_for_moderation += extra_context
        moderation_future = executor.submit(moderate, content_for_moderation)

        # Wait for moderation result
        violation, message = moderation_future.result()
        if violation:
            if user_id:
                increment_violations(user_id)
            return jsonify({"error": f"Message breaks our usage policy. Please check our guidelines.\n{message}"}), 400

        # Creates library database object
        library_response, library_response_status_code = lbh.create_library(user_id, topic, library_difficulty, language, language_difficulty, guide, is_public)
        if library_response_status_code == 201:
            
            library_id = library_response.get_json().get("library_id")
            
            library_favorites_response, library_favorites_status_code = lbh.create_library_favorite(user_id, library_id)
            
            if library_favorites_status_code == 201:
                process_document(selected_file, library_id) # extract embeddings + and upload to pinecone
            else:
                return jsonify(status="error", message="Failed to create library favorites"), 500

        else:
            return jsonify(status="error", message="Failed to create library"), 500
        try:

            form = request.form.to_dict(flat=False)

            # Create a mapping of units to sections and collect all section names
            section_unit_map = {}
            section_names = []
            unit_names = []  # New list to store unique unit names

            # Parse the group structure from the form data
            for key, values in form.items():
                if key.startswith('groupSections[') and key.endswith('][]'):
                    # Extract group index from the key (format: "groupSections[index][]")
                    group_index = key[len('groupSections['):-3]  # Remove 'groupSections[' and '[]'
                    print(f"group_index: {group_index}")
                    # Get the corresponding group name if available
                    group_name = form.get(f'groupNames[{group_index}]', ['Group ' + group_index])[0]
                    print(f"group_name: {group_name}")
                    # Add group name to unit_names if not already there
                    if group_name and group_name not in unit_names:
                        unit_names.append(group_name)
                        section_unit_map[group_name] = []  # Initialize the list of sections for this unit
                        
                    for section in values:
                        if section:  # Skip empty section names
                            print(f" appending section named {section}")
                            section_names.append(section)
                            section_unit_map[group_name].append(section)  # Add section to the unit's list

            futures_dict = {}
            for section_name in section_names:
                if section_name: # Skip empty section names
                    rag_context = query_and_respond_pinecone(section_name, library_id)
                    print(f" section_name: {section_name} rag_context: {rag_context}")
                    future = executor.submit(lgn.generate_room_content, user_id, section_name, library_difficulty, language, language_difficulty, extra_context, guide, rag_context)
                    futures_dict[future] = section_name

            completed_rooms = {}
            section_contents_map = {}
            for future in concurrent.futures.as_completed(futures_dict):
                section_name = futures_dict[future]
                try:
                    content = future.result()
                    section_contents_map[section_name] = content
                    completed_rooms[section_name] = True

                except Exception as e:
                    print(f"Error generating content for room {section_name}: {str(e)}")
                    completed_rooms[section_name] = False

            # Check if all rooms were successfully completed
            if all(completed_rooms.values()):
                
                try:
                    print(section_contents_map)
                    lbh.save_library_room_contents(library_id, section_unit_map, section_contents_map, user_id)

                except Exception as e:
                    print(f"Error saving generated content: {str(e)}")

                library = lbh.get_library(library_id, user_id, False)
                return jsonify(status="success", library_data=library.get_json())
            
            else:
                failed_rooms = [room for room, success in completed_rooms.items() if not success]
                return jsonify(
                    status="partial_success",
                    message=f"Failed to generate content for rooms: {', '.join(failed_rooms)}",
                    library_data=library_response.get_json()
                )

        except Exception as e:
            return jsonify(status="error", message=f"Failed to generate room content: {str(e)}"), 500

    @app.route("/api/library/<int:library_id>", methods=["GET"])
    def get_library(library_id):
        
        try:

            library_topic = request.args.get("library_topic", None)

            user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
            library = lbh.get_library(library_id, user_id)

            if not library:
                return jsonify(status="error", message="Library not found"), 404

            # Check if the library has a default image and possibly trigger image generation
            response, status_code = lbh.has_default_image(library_id)

            if status_code != 200:
                return response
            
            # If there's a default image and the click count is divisible by 4, queue up image generation
            if response.json['has_default_image'] and library.get_json().get("clicks") % 4 == 0:
                executor.submit(generate_images_task, library_id)
            
            # Retrieve library data
            library_data = library.get_json()

            # Attempt to retrieve existing room contents
            room_data = None
            if library_topic:

                unit_id, section_id = library_data.get('section_to_unit_map').get(library_topic)
                room_data = lbh.retrieve_library_room_contents(library_id, section_id, user_id)

                if not room_data:
                    return jsonify(status="error", message="Room not found"), 404
            else:
                room_data = lbh.get_library_room_state(user_id, library_id)
                # return a map of room names --> unit 
                # room_data = room_data

            test = library_data.get("room_names")

            library_data["show_settings"] = user_id == library_data.get("owner_id")

            return jsonify(status="success", data=library_data, room_data=room_data)
        except: 
            return jsonify(status="error", message="Failed to retrieve library data"), 500
        
    @app.route('/api/library/unit', methods=['POST'])
    def generate_unit():
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        
        data = request.get_json()
        unit_name = data.get("unitName")
        library_id = data.get("libraryId")
        position = data.get("position")


        # Validate inputs
        if not user_id:
            return jsonify(status="error", message="Must be signed in."), 403
        if not unit_name:
            return jsonify(status="error", message="No unit name provided"), 400
        if not library_id:
            return jsonify(status="error", message="No library ID provided"), 400
        
        library = db.session.query(Library).filter_by(id=library_id).first()

        if not library:
            return jsonify(status="error", message="No library ID provided"), 400

        if user_id != library.owner_id:
            return jsonify(status="error", message="You do not own this library."), 403
        
        if len(library.units) >= 20:
            return jsonify(status="error", message="Library has reached maximum number of units (20 for now)"), 400

        try:
            
            new_unit_response, new_unit_status_code = lbh.create_unit_and_add(library_id, unit_name, position=position)
            
            new_unit = new_unit_response.get_json()

            if new_unit_status_code != 201:
                return jsonify(status="error", message="Failed to create unit"), 500

            return jsonify(status="success", unit_id=new_unit["unit"], message="Unit created successfully"), 200

        except Exception as e:
            print(f"Failed to process request: {str(e)}")
            return jsonify(status="error"), 500

    @app.route('/api/library/room', methods=['POST'])
    def generate_room():
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        section_names = request.form.getlist("roomNames")  # Get list of section names
        library_id = request.form.get("libraryId")

        # Validate inputs
        if not section_names:
            return jsonify(status="error", message="No subtopics provided"), 400
        if not library_id:
            return jsonify(status="error", message="No library ID provided"), 400

        try:

            # Check if "file" is in request.files
            selected_file = None
            if "file" in request.files:
                file = request.files["file"]
                if file.filename == "":
                    return jsonify(status="error", message="No file selected"), 400
                selected_file = file.read()

            # If no user is logged in, return an error
            if not user_id:
                return jsonify(status="error", message="Must be signed in."), 403
            
        except Exception as e:
            return jsonify(status="error", message=f"Failed to process request: {str(e)}"), 500
    
        try:
            library_response = get_library(library_id)
            if not library_response or library_response.status_code == "error":
                return jsonify(status="error", message="Can only generate library rooms for valid libraries"), 400

            library = library_response.get_json()

            # Process each subtopic
            results = []
            rag_context = None
            if selected_file:
                process_document(selected_file, library_id)

            futures_dict = {}
            for subtopic in section_names:
                # Check for existing content
                unit_id, section_id = library.get('section_to_unit_map').get(subtopic)
                existing_content = lbh.retrieve_library_room_contents(library_id, section_id, user_id)
                if existing_content:
                    results.append({"subtopic": subtopic, "status": "success", "data": existing_content})
                    continue

                # Generate new content for this subtopic
                try:

                    rag_context = query_and_respond_pinecone(subtopic, library_id)
                    print(f"rag context: {rag_context}")
                    future = executor.submit(lgn.generate_libroom_content, user_id, subtopic, library_id, rag_context)
                    futures_dict[future] = subtopic
                     
                except Exception as e:
                    results.append({"subtopic": subtopic, "status": "error", "message": f"Failed to generate content: {str(e)}"})

            completed_subtopics = {}
            for future in concurrent.futures.as_completed(futures_dict):
                subtopic = futures_dict[future]
                try: 
                    subtopic_contents = future.result()

                    # Save the generated content
                    lbh.save_library_room_contents(library_id, library.get('section_to_unit_map'), subtopic_contents, user_id)
                    results.append({"subtopic": subtopic, "status": "success", "data": subtopic_contents})
                    completed_subtopics[subtopic] = True

                except Exception as e:
                    print(f"Error generating content for subtopic {subtopic}: {str(e)}")
                    completed_subtopics[subtopic] = False

                        
            # Check if all subtopics failed
            if all(result["status"] == "error" for result in results):
                return jsonify(status="error", message="Failed to process any subtopics", errors=results), 500

            # Return results for all subtopics
            return jsonify(status="success", results=results)

        except Exception as e:
            return jsonify(status="error", message=f"Failed to process request: {str(e)}"), 500
        
    @app.route('/api/library/available-generated-rooms', methods=['POST'])
    def get_available_generated_rooms():
        try:
            data = request.get_json()
            library_id = data.get('libraryId')
                
            if not library_id:
                return jsonify(status="error", message="No library ID provided"), 400

            # Call the separate DB logic function
            rooms = lbh.get_available_generated_rooms(library_id)
            # Success response
            return jsonify({
                "status": "success",
                "data": {
                    "rooms": rooms  # could be an empty list if none
                }
            }), 200

        except Exception as e:
            return jsonify(status="error", message=f"Failed to generate content {e}"), 500


    @app.route("/api/library/end", methods=["POST"])
    def end_game():
        data = request.get_json()
        library_id = data.get('libraryId')
        section_id = data.get('sectionId')

        # score = data.get('score')
        # time = data.get('time')
        # completed_rooms = data.get('completed', []) 
        
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None

        if not user_id:
            return jsonify({'status': 'error', 'message': "Not logged in..."}), 401
        
        if library_id is None: # or score is None:
            return jsonify({'status': 'error', 'message': 'Missing libraryId or score'}), 400

        try:
            response, status = lbh.update_game_end(user_id, library_id, section_id) # score, time, completed_rooms, True)
            return response, status
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @app.route("/api/library/favorited_status/<int:library_id>", methods=["POST", "GET"])
    def library_favorited_status(library_id):
        try:
            if request.method == "POST":    
                data = request.get_json()
                new_status = data.get('newStatus')
                user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
                if not user_id:
                    return jsonify(status="error", message="Must be logged in to favorite libraries."), 403
                
                update_value, response_status = lbh.update_library_favorited_status(user_id, library_id, new_status)
                
                if response_status != 200:
                    return jsonify(status="error", message="Failed to update library favorited status."), 500
                
                return jsonify({'status': 'success', 'message': 'Library favorited status updated successfully.'}), 200
            
            elif request.method == "GET":
                user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
                if not user_id:
                    return jsonify(status="error", message="Must be logged in to check library favorited status."), 403
                
                favorited_status = lbh.get_library_favorited_status(user_id, library_id)
            
                if favorited_status is None:
                    return jsonify(status="error", message="Library not found."), 404
                
                return jsonify({'status': 'success', 'is_favorited': favorited_status}), 200

        except Exception as e:
            return jsonify(status="error", message=f"Failed to update library favorited status: {str(e)}"), 500
        
    @app.route("/api/library/visibility_status/<int:library_id>", methods=["GET", "POST"])
    def library_visibility_status(library_id):
        try:
            if request.method == "GET":
                
                user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
                if not user_id:
                    return jsonify(status="error", message="Must be logged in to check library visibility status."), 403
                
                library = lbh.get_library(library_id, user_id)
                if not library:
                    return jsonify(status="error", message="Library not found."), 404
                
                if library.owner_id != user_id:
                    return jsonify(status="error", message="You do not own this library."), 403

                visibility_status = lbh.get_library_visibility_status(user_id, library_id)
            
                if visibility_status is None:
                    return jsonify(status="error", message="Library not found."), 404
                
                return jsonify({'is_public': visibility_status}), 200
            
            elif request.method == "POST":
                
                data = request.get_json()
                new_status = data.get('newStatus')
                user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
                
                if not user_id:
                    return jsonify(status="error", message="Must be logged in to update library visibility status."), 403
                
                visibility_response, visibility_response_status = lbh.update_library_visibility_status(user_id, library_id, new_status)

                visibility_response_value = visibility_response.get_json()
                
                if visibility_response_status != 200:
                    return jsonify(status="error", message="Failed to update library visibility status."), 500
                return jsonify(join_code=visibility_response_value["join_code"], message='Library visibility status updated successfully.'), 200
            else:
                return jsonify(status="error", message="Method not allowed"), 405
        except Exception as e:
            return jsonify(status="error", message=f"Failed to update library visibility status: {str(e)}"), 500
    
    @app.route("/api/libraries", methods=["GET"])
    def get_libraries():
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        return lbh.get_libraries_info(user_id)
    
    @app.route('/api/scores', methods=['GET'])
    def fetch_scores():
        completions = lbh.get_top_scores_by_unique_users(limit=5)
        data = []
        for email, library_id, time in completions:
            data.append({
                "email": mask_email(email),
                "library_id": library_id,
                "time": time
            })
        return jsonify(data), 200

    @app.route('/api/scores/library/<int:library_id>', methods=['GET'])
    def fetch_scores_for_library(library_id):
        completions = lbh.get_library_top_scores_by_unique_users(library_id=library_id, limit=5)
        data = []
        for email, library_id, time in completions:
            data.append({
                "email": mask_email(email),
                "library_id": library_id,
                "time": time
            })
        return jsonify(data), 200