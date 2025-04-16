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
        if len(topic) > 200:
            return jsonify({"error": "Topic is too long. Maximum 200 characters allowed."}), 400
        if len(topic) < 1:
            return jsonify({"error": "No message."}), 400

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

        try :
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
        library_response, status_code = lbh.create_library(user_id, topic, library_difficulty, language, language_difficulty, guide)

        if status_code == 201:
            
            library_id = library_response.get_json().get("library_id")
            print("library_id after status_code")
            process_document(selected_file, library_id) # extract embeddings + and upload to pinecone
        else:
            raise Exception("Library creation failed")

        try:

            # def print_form_values():
            form = request.form.to_dict(flat=False)
                # Simple debug print of all form values
           
                
                # Specifically print group-related data
            for key, values in form.items():
                if 'groupNames' in key:
                    print(f"Group name {key}: {values[0]}")
                elif 'groupSections' in key:
                    print(f"Group sections {key}: {values}")

            return jsonify({"error": "breaking things rn"}), 400
            futures_dict = {}
            #  print("Form data:")
            # # for key, values in form.items():
            #     # print(f"  {key}: {values}")
            #     section_names = []
            # for key, values in request.form.items():
            #     if 'groupSections' in key:
            #         section_names.extend(values)

            # # For debugging
            # print(f"Processing sections: {section_names}")

            # # Set up concurrent tasks
            # futures_dict = {}
            # for section_name in section_names:
            #     if section_name:  # Skip empty section names
            #         rag_context = query_and_respond_pinecone(section_name, library_id)
            #         future = executor.submit(
            #             lgn.generate_room_content, 
            #             user_id, 
            #             section_name, 
            #             library_difficulty, 
            #             language, 
            #             language_difficulty, 
            #             extra_context, 
            #             guide, 
            #             rag_context
            #         )
            #         futures_dict[future] = section_name
            for room_name in room_names: # for 'groupSections' in key, values in form.items()?
                rag_context = query_and_respond_pinecone(room_name, library_id) # replace room_name with section names, pinecone doesn't need
                                                                                # units
                future = executor.submit(lgn.generate_room_content, user_id, room_name, library_difficulty, language, language_difficulty, extra_context, guide, rag_context)
                                                                                # can replace room_name --> section names here as well. Nothing db related here
                futures_dict[future] = room_name

            completed_rooms = {}
            for future in concurrent.futures.as_completed(futures_dict):
                print("future")
                
                room_name = futures_dict[future]
                
                try:
                    room_contents = future.result()
                    # print(f"room_contents: {room_contents}")
                    user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
                    # print("user_id in library_routes.py")
                    print(f"room_contents library_routes 176: {room_contents}")
                    lbh.save_library_room_contents(library_id, room_name, room_contents, user_id)
                    completed_rooms[room_name] = True
                    # print(f"Successfully generated and saved content for room: {room_name}")

                except Exception as e:
                    
                    print(f"Error generating content for room {room_name}: {str(e)}")
                    completed_rooms[room_name] = False

            # Check if all rooms were successfully completed
            if all(completed_rooms.values()):
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
        
        library_topic = request.args.get("library_topic", None)

        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        library = lbh.get_library(library_id, user_id)
        print("after get_library in lbh")
        if not library:
            return jsonify(status="error", message="Library not found"), 404

        # Check if the library has a default image and possibly trigger image generation
        response, status_code = lbh.has_default_image(library_id)
        if status_code != 200:
            return response

        # If there's a default image and the click count is divisible by 4, queue up image generation
        if response.json['has_default_image'] and library.get_json().get("clicks") % 4 == 0:
            executor.submit(generate_images_task, library_id)
        
        print("before library.get_json")
        # Retrieve library data
        library_data = library.get_json()
        print("after library.get_json")

        # Attempt to retrieve existing room contents
        room_data = None
        # print("library api")
        # print(library_topic)
        # library_topic = "science thing"
        if library_topic:
            room_data = lbh.retrieve_library_room_contents(library_id, library_topic, user_id)
            print("after retrieve")
            if not room_data:
                if library_topic in library_data.get('room_names', []):
                    try:
                        # If no content exists, generate the room content
                        room_contents = lgn.generate_libroom_content(
                            user_id,
                            library_topic,
                            library_id
                        )
                        print(f"room_contents library_routes 240: {room_contents}")
                        lbh.save_library_room_contents(library_id, library_topic, room_contents)
                        room_data = room_contents
                    except Exception as e:
                        return jsonify(status="error", message="Failed to generate room content"), 500
                else:
                    return jsonify(status="error", message="Room not found"), 404
        else:
            room_data = lbh.get_library_room_state(user_id, library_id)
            room_data = room_data

        return jsonify(status="success", data=library_data, room_data=room_data)
        
    @app.route('/api/library/room', methods=['POST'])
    def generate_room():
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        subtopics = request.form.getlist("roomNames")  # Get list of subtopics
        library_id = request.form.get("libraryId")

        # Validate inputs
        if not subtopics:
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

            # Process each subtopic
            results = []
            rag_context = None
            if selected_file:
                process_document(selected_file, library_id)

            futures_dict = {}
            for subtopic in subtopics:
                # Check for existing content
                existing_content = lbh.retrieve_library_room_contents(library_id, subtopic, user_id)
                if existing_content:
                    results.append({"subtopic": subtopic, "status": "success", "data": existing_content})
                    continue

                # Generate new content for this subtopic
                try:

                    print("before rag_context")
                    rag_context = query_and_respond_pinecone(subtopic, library_id)
                    print(f"rag context: {rag_context}")
                    future = executor.submit(lgn.generate_libroom_content, user_id, subtopic, library_id, rag_context)
                    futures_dict[future] = subtopic
                     
                except Exception as e:
                    results.append({"subtopic": subtopic, "status": "error", "message": f"Failed to generate content: {str(e)}"})

            completed_subtopics = {}
            for future in concurrent.futures.as_completed(futures_dict):
                print("before subtopic")
                subtopic = futures_dict[future]
                print("after subtopic")
                try: 
                    subtopic_contents = future.result()

                    # Save the generated content
                    print(f" library_id: {library_id} subtopic: {subtopic} subtopic_contents: {subtopic_contents} user_id: {user_id}")
                    lbh.save_library_room_contents(library_id, subtopic, subtopic_contents, user_id)
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
            print(rooms)
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
        room_name = data.get('roomName')

        # score = data.get('score')
        # time = data.get('time')
        # completed_rooms = data.get('completed', []) 
        
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        if not user_id:
            return jsonify({'status': 'error', 'message': "Not logged in..."}), 401
        
        if library_id is None: # or score is None:
            return jsonify({'status': 'error', 'message': 'Missing libraryId or score'}), 400

        try:
            response, status = lbh.update_game_end(user_id, library_id, room_name) # score, time, completed_rooms, True)
            return response, status
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
        
    @app.route("/api/libraries", methods=["GET"])
    def get_libraries():
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        return lbh.get_libraries_info(user_id)
    
    @app.route("/api/library/like", methods=["POST"])
    def like_library():
        data = request.get_json()
        return lbh.like_library(data.get('libraryId'))
    
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