# library_routes.py

import random
from flask import request, jsonify
from flask_login import current_user, AnonymousUserMixin
from bleach import clean
from flask_executor import Executor
import fitz
import re
import concurrent.futures

import base64
from io import BytesIO
import time

from openapi import moderate
from utils import mask_email, get_client_ip
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
            library_difficulty = "Easy"
        else:
            library_difficulty = clean(library_difficulty)
            if library_difficulty not in VALID_DIFFICULTIES:
                library_difficulty = "Easy"


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
                existing_content = lbh.retrieve_library_room_contents(existing_library, topic)
                if existing_content:
                    return jsonify(status="success", library_id=existing_library)
                else:
                    try:
                        # Generate room content asynchronously
                        room_future = executor.submit(lgn.generate_libroom_content, user_id, topic, existing_library)
                        room_contents = room_future.result()
                        lbh.save_library_room_contents(existing_library, topic, room_contents)
                        return jsonify(status="success", library_id=existing_library)
                    except Exception as e:
                        return jsonify(status="error", message=f"Failed to generate room content {e}"), 500

        
        room_names = request.form.getlist('roomNames')
        if room_names:
            print(room_names)
        else:
            return jsonify({"error": f"Must specify room names for now, also we are in the process of breaking things"}), 400
        
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
        # TODO vvv 
        content_for_moderation = topic
        if extra_context:
            content_for_moderation += extra_context
        moderation_future = executor.submit(moderate, content_for_moderation)

        # Start library generation task (flask Gemini 1.5)
        # TODO Maybe in the case where we are extracting it from a table of contents / syllabus?
        # room_names_future = executor.submit(lgn.suggest_library_wing, user_id, topic, library_difficulty, language, language_difficulty, extra_context)

        # Wait for moderation result
        # TODO vvv 
        violation, message = moderation_future.result()
        if violation:
            if user_id:
                increment_violations(user_id)
            return jsonify({"error": f"Message breaks our usage policy. Please check our guidelines.\n{message}"}), 400

        # Create the library
        # TODO Maybe in the case where we are extracting it from a table of contents / syllabus?
        # room_names = room_names_future.result()

        # TODO (room_names is already from frontend)
        # Creates library database object
        library_response, status_code = lbh.create_library(user_id, topic, room_names, library_difficulty, language, language_difficulty, guide)

        print("before library_response")

        if status_code == 201:
            
            library_id = library_response.get_json().get("library_id")
            print("library_id after status_code")
            process_document(selected_file, library_id) # extract embeddings + and upload to pinecone
        else:
            raise Exception("Library creation failed")

        try:

            futures_dict = {}
            for room_name in room_names:
                print(f"room names: {room_names}")
                print(f"room names: {room_name}")
                rag_context = query_and_respond_pinecone(room_name, library_id)
                future = executor.submit(lgn.generate_room_content, user_id, room_name, library_difficulty, language, language_difficulty, extra_context, guide, rag_context)
                futures_dict[future] = room_name

            completed_rooms = {}
            for future in concurrent.futures.as_completed(futures_dict):
                print("future")
                
                room_name = futures_dict[future]
                
                try:
                    room_contents = future.result()
            
                    lbh.save_library_room_contents(library_id, room_name, room_contents)
                    completed_rooms[room_name] = True
                    print(f"Successfully generated and saved content for room: {room_name}")
                    # return jsonify({"error": f"No error, we're in the process of breaking things for now😭😭😭"}), 400

                except Exception as e:
                    
                    print(f"Error generating content for room {room_name}: {str(e)}")
                    completed_rooms[room_name] = False

            # Check if all rooms were successfully completed
            if all(completed_rooms.values()):
                print("all")
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
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        library = lbh.get_library(library_id, user_id)
        print("get_library 1")
        if not library:
            return jsonify(status="error", message="Library not found"), 404

        # Check if the library has a default image and possibly trigger image generation
        response, status_code = lbh.has_default_image(library_id)
        if status_code != 200:
            return response

        # If there's a default image and the click count is divisible by 4, queue up image generation
        if response.json['has_default_image'] and library.get_json().get("clicks") % 4 == 0:
            executor.submit(generate_images_task, library_id)
        ("get_library 2")
        # Retrieve library data
        library_data = library.get_json()
        library_topic = library_data.get("library_topic")
        print("get_library 3")
        # Attempt to retrieve existing room contents
        room_data = lbh.retrieve_library_room_contents(library_id, library_topic)
        if not room_data:
            try:
                # If no content exists, generate the room content
                room_contents = lgn.generate_libroom_content(
                    user_id,
                    library_topic,
                    library_id
                )
                lbh.save_library_room_contents(library_id, library_topic, room_contents)
                room_data = room_contents
            except Exception as e:
                return jsonify(status="error", message="Failed to generate room content"), 500

        return jsonify(status="success", data=library_data, room_data=room_data)
        
    @app.route("/api/library/room", methods=["POST"])
    def generate_room():
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        data = request.get_json()
        subtopic = data.get("subtopic")
        library_id = data.get("libraryId")

        if not subtopic:
            return jsonify(status="error", message="No subtopic provided"), 400
        if not library_id:
            return jsonify(status="error", message="No library ID provided"), 400

        print("subtopic: " + subtopic)
        # Attempt to retrieve existing room contents
        existing_content = lbh.retrieve_library_room_contents(library_id, subtopic.replace("-", " "))
        if existing_content:
            return jsonify(status="success", data=existing_content)
        
        # If no content exists, generate new content
        if not user_id:
            ip = request.remote_addr # TODO ip stuff?
            # if not check_generation_allowed(ip, 'room'):
            #     return jsonify(status="error", message="Room generation limit reached."), 403
            
        print(f"userid: ${user_id}")
        if user_id:
            within_limit, message = is_within_limit(current_user)
            if not within_limit:
                return jsonify({"error": message}), 429
        elif not lbh.is_center_room(library_id, subtopic):
            return jsonify(status="error", message="Please login to continue."), 400

        try:
            library_response = get_library(library_id)
            if not library_response or library_response.status_code == "error":
                return jsonify(status="error", message="Can only generate library rooms for valid libraries"), 400

            library_data = library_response.get_json()
            room_list = library_data.get('data', {}).get('room_names', [])

            print(f"room_names: {room_list}")
            if not subtopic in room_list:
                return jsonify(status="error", message="Can only generate library rooms for valid libraries"), 400

            generated_content = lgn.generate_libroom_content(user_id, subtopic, library_id)
            lbh.save_library_room_contents(library_id, subtopic, generated_content)
            existing_content = lbh.retrieve_library_room_contents(library_id, subtopic)
            if not user_id:
                mark_generation_done(ip, 'room')
            return jsonify(status="success", data=existing_content)
        except Exception as e:
            return jsonify(status="error", message=f"Failed to generate content {e}"), 500
    
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
        score = data.get('score')
        time = data.get('time')
        completed_rooms = data.get('completed', []) 
        
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        if not user_id:
            return jsonify({'status': 'error', 'message': "Not logged in..."}), 401
        
        if library_id is None or score is None:
            return jsonify({'status': 'error', 'message': 'Missing libraryId or score'}), 400

        try:
            response, status = lbh.update_game_end(user_id, library_id, score, time, completed_rooms, True)
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