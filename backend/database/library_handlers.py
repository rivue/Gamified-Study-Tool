from datetime import datetime
from flask import jsonify
from sqlalchemy import func, IntegrityError, OperationalError
import random
import math
import json
from database.models import (
    db,
    User,
    Library,
    LibraryFactoid,
    LibraryQuestion,
    LibraryQuestionChoice,
    LibraryRoomState,
    LibraryCompletion
)
MAX_ROOM_NAME_LENGTH = 200

def create_library(
   user_id, library_topic, room_names, difficulty, language, language_difficulty, guide
):
   # Validate input parameters
   if not library_topic or not isinstance(library_topic, str):
       return jsonify({"message": "Invalid or missing library_topic. It must be a string."}), 400
   if not room_names or not isinstance(room_names, list):
       return jsonify({"message": "Invalid or missing room_names. It must be a list."}), 400
   if not difficulty or not isinstance(difficulty, str):
       return jsonify({"message": "Invalid or missing difficulty. It must be a string."}), 400
   if not language or not isinstance(language, str):
       return jsonify({"message": "Invalid or missing language. It must be a string."}), 400
   if not language_difficulty or not isinstance(language_difficulty, str):
       return jsonify({"message": "Invalid or missing language_difficulty. It must be a string."}), 400
   if guide and not isinstance(guide, str):  # Guide is optional, so we only check if provided
       return jsonify({"message": "Guide must be a string if provided."}), 400

   try:
       # Check if library topic already exists (unique constraint violation)
       existing_library = Library.query.filter_by(library_topic=library_topic).first()
       if existing_library:
           return jsonify({"message": "Library topic already exists"}), 400

       # Create new library entry
       library = Library(
           user_id=user_id,
           library_topic=library_topic,
           room_names=room_names,
           difficulty=difficulty,
           language=language,
           language_difficulty=language_difficulty,
           guide=guide,
       )

       db.session.add(library)
       db.session.commit()

       return (
           jsonify(
               {"message": "Library created successfully", "library_id": library.id}
           ),
           201,
       )

   except IntegrityError as e:
       # Handle specific integrity errors like unique constraint violations
       db.session.rollback()
       return jsonify({"message": "Failed to create library due to duplicate topic"}), 400

   except OperationalError as e:
       # Handle database connection issues
       db.session.rollback()
       return jsonify({"message": "Database connection error. Please try again later."}), 500

   except Exception as e:
       # Handle any other exceptions
       db.session.rollback()
       return jsonify({"message": "An unexpected error occurred: " + str(e)}), 500


def get_library(library_id, user_id=None, click=True):
    library = Library.query.get(library_id)
    if not library:
        
        return jsonify({"message": "Library not found"}), 404
    
    if click:
        library.clicks += 1
        db.session.commit()
        
    library_data = library.as_dict()
    library_data["tutorial"] = True #default
    if user_id:
        existing_completion = LibraryCompletion.query.filter_by(library_id=library_id, user_id=user_id).first()
        if existing_completion:
            library_data["score"] = existing_completion.score
            library_data["best_time"] = existing_completion.time
            library_data["completion"] = len(existing_completion.completed_rooms.split(","))*4
        any_completion = LibraryCompletion.query.filter_by(user_id=user_id, is_complete=True).first()
        print(any_completion)
        if any_completion:
            library_data["tutorial"] = False

    library_data["clicks"] = library.clicks
    return jsonify(library_data)

def get_library_details(library_id):
    try:
        library = Library.query.get(library_id)
        if library is None:
            return jsonify({'error': 'Library not found'}), 404

        # Fetch required details
        details = {
            'topic': library.library_topic,
            'guide': library.guide,
            'difficulty': library.difficulty
        }
        return jsonify(details), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_library_room_state(user_id, library_id, room_name=None):
    # Validate input parameters
    if not isinstance(user_id, int) or user_id <= 0:
        return jsonify({"error": "Invalid user_id. It must be a positive integer."}), 400
    if not isinstance(library_id, int) or library_id <= 0:
        return jsonify({"error": "Invalid library_id. It must be a positive integer."}), 400
    
    try:
        if not room_name:  # for all rooms (ex: map page)
            room_states = LibraryRoomState.query.filter_by(
                user_id=user_id,
                library_id=library_id
            ).all()

            if not room_states:
                return jsonify({"message": "No room states found for the given user and library."}), 404

            return jsonify([s.as_dict() for s in room_states])

        else:  # for a specific room
            state = LibraryRoomState.query.filter_by(
                user_id=user_id,
                library_id=library_id,
                room_name=room_name
            ).first()

            if not state:
                return jsonify({"message": "Room state not found for the specified room."}), 404

            return jsonify(state.as_dict())

    except OperationalError as e:
        return jsonify({"error": f"Database operational error: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

def save_library_room_contents(library_id, room_name, lessons, user_id):
    # Validate input parameters
    if not isinstance(library_id, int) or library_id <= 0:
        return jsonify({"error": "Invalid library_id. It must be a positive integer."}), 400
    if not room_name or not isinstance(room_name, str):
        return jsonify({"error": "Invalid or missing room_name. It must be a non-empty string."}), 400
    if not isinstance(user_id, int) or user_id <= 0:
        return jsonify({"error": "Invalid user_id. It must be a positive integer."}), 400
    if not isinstance(lessons, dict) or "factoids" not in lessons:
        return jsonify({"error": "Invalid lessons format. It must be a dictionary with a 'factoids' key."}), 400
    if not isinstance(lessons["factoids"], list):
        return jsonify({"error": "Invalid lessons factoids. 'factoids' must be a list."}), 400

    try:
        responses = []
        num_lessons = 3  # This value may be dynamic in other contexts.
        
        # Add room name to library
        room_response, status = add_room_name_to_library(library_id, room_name)
        if status != 200:
            return jsonify({"status": "error", "message": "Failed to add room name to library"}), 200
        
        # Add library room state and check for errors if a response is returned
        state_result = add_library_room_state(user_id, library_id, room_name, num_lessons)
        if isinstance(state_result, tuple) and len(state_result) == 2:
            state_response, state_status = state_result
            if state_status not in [200, 201]:
                return state_response
        
        # Process each factoid in lessons
        for index, item in enumerate(lessons["factoids"]):
            # Validate that each factoid item is a dict and contains required keys
            if not isinstance(item, dict):
                return jsonify({"error": "Each factoid item must be a dictionary."}), 400
            if "factoid_text" not in item or "question" not in item:
                return jsonify({"error": "Each factoid must include 'factoid_text' and 'question'."}), 400

            # Compute lesson name based on index (e.g., 9 factoids per lesson set)
            lesson_name = "factoid_set_" + str(math.floor(index / 9) + 1)
            factoid_content = item["factoid_text"]
            question_data = item["question"]

            # Add factoid to library; expect a tuple (factoid_response, status_code)
            factoid_response, status_code = add_factoid_to_library(
                library_id, room_name, factoid_content, lesson_name
            )
            if status_code != 201:
                return factoid_response

            # Extract factoid_id from response JSON
            factoid_json = factoid_response.json
            factoid_id = factoid_json.get("factoid_id")
            if not factoid_id:
                return jsonify({"error": "Failed to retrieve factoid_id from response."}), 500

            # Validate question data
            if not isinstance(question_data, dict):
                return jsonify({"error": "Question data must be a dictionary."}), 400
            if "type" not in question_data or "text" not in question_data or "correct_choice" not in question_data:
                return jsonify({"error": "Question data must include 'type', 'text', and 'correct_choice'."}), 400

            question_type = question_data["type"]
            question_text = question_data["text"]
            correct_choice = question_data["correct_choice"]
            wrong_choices = question_data.get("wrong_choices", [])

            # Add question to factoid; expect a tuple (question_response, status_code)
            question_response, status_code = add_question_to_factoid(
                factoid_id, question_text, correct_choice, wrong_choices, question_type
            )
            if status_code != 201:
                return question_response

            responses.append({
                "factoid_response": factoid_response.json,
                "question_response": question_response.json,
            })

        return jsonify({"status": "success", "data": responses}), 200

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": f"Database integrity error: {str(e)}"}), 400

    except OperationalError as e:
        db.session.rollback()
        return jsonify({"error": f"Database operational error: {str(e)}"}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 400

def retrieve_library_room_contents(library_id, room_name, user_id):
    # Validate user_id and library_id
    if not isinstance(user_id, int) or user_id <= 0:
        return jsonify({"error": "Invalid user_id. It must be a positive integer."}), 400
    if not isinstance(library_id, int) or library_id <= 0:
        return jsonify({"error": "Invalid library_id. It must be a positive integer."}), 400

    # Validate room_name: must be a non-empty string and not too long
    if not room_name or not isinstance(room_name, str):
        return jsonify({"error": "Missing or invalid room_name. It must be a non-empty string."}), 400
    if len(room_name) > MAX_ROOM_NAME_LENGTH:
        return jsonify({"error": f"room_name is too long. Maximum allowed length is {MAX_ROOM_NAME_LENGTH} characters."}), 400

    try:
        # Retrieve the current room state for the given user, library, and room name
        curr_state = get_library_room_state(user_id, library_id, room_name)
        # If no state is found, return an error response
        if not curr_state:
            return jsonify({"error": "Room state not found for the given parameters."}), 404

        # Depending on the lesson_state relative to num_lessons, get appropriate factoids.
        if curr_state["lesson_state"] > curr_state["num_lessons"]:
            # User has completed all lessons: retrieve all factoids for the room.
            all_factoids = LibraryFactoid.query.filter_by(
                library_id=library_id, room_name=room_name
            ).all()
            if not all_factoids:
                return jsonify({"error": "No factoids found for the specified room."}), 404
            # Randomly select between 7 and 9 factoids (or all if fewer available)
            num_factoids = min(random.randint(7, 9), len(all_factoids))
            factoids = random.sample(all_factoids, num_factoids) if len(all_factoids) >= num_factoids else all_factoids
        else:
            # Get factoids for the current lesson state.
            lesson_name = f"factoid_set_{curr_state['lesson_state']}"
            factoids = LibraryFactoid.query.filter_by(
                library_id=library_id, room_name=room_name, lesson_name=lesson_name
            ).all()
            if not factoids:
                return jsonify({"error": "No factoids found for the current lesson state."}), 404

        # If not enough factoids are found, we consider it an error.
        if len(factoids) < 3:
            return jsonify({"error": "Not enough factoids available to build room contents."}), 404

        # Build the room contents with factoids and their corresponding questions.
        room_contents = []
        for factoid in factoids:
            questions = []
            for question in factoid.questions:
                # Retrieve all choices if available.
                question_choices = question.choices.all() if question.choices else []
                wrong_choices = [choice.choice_text for choice in question_choices if not choice.is_correct]
                correct_choice = next((choice.choice_text for choice in question_choices if choice.is_correct), None)
                questions.append({
                    "question_text": question.question_text,
                    "correct_choice": correct_choice,
                    "wrong_choices": wrong_choices,
                    "question_type": question.question_type,
                })
            room_contents.append({
                "factoid_text": factoid.factoid_content,
                "questions": questions,
                "room_state": curr_state
            })

        return jsonify({"room_name": room_name, "factoids": room_contents}), 200

    except Exception as e:
        # Catch any unexpected errors, log if needed, and return a generic error message.
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


def add_library_room_state(user_id, library_id, room_name, num_lessons, initial_lesson_state=1):
    # Validate input parameters
    if not isinstance(user_id, int) or user_id <= 0:
        return jsonify({"error": "Invalid user_id. It must be a positive integer."}), 400
    if not isinstance(library_id, int) or library_id <= 0:
        return jsonify({"error": "Invalid library_id. It must be a positive integer."}), 400
    if not room_name or not isinstance(room_name, str):
        return jsonify({"error": "Invalid or missing room_name. It must be a non-empty string."}), 400
    if not isinstance(num_lessons, int) or num_lessons <= 0:
        return jsonify({"error": "Invalid num_lessons. It must be a positive integer."}), 400
    if not isinstance(initial_lesson_state, int) or initial_lesson_state not in [1, 2, 3]:
        return jsonify({"error": "Invalid initial_lesson_state. It must be 1, 2, or 3."}), 400

    try:
        # Check if a record already exists for this user, library, and room
        existing_state = LibraryRoomState.query.filter_by(
            user_id=user_id,
            library_id=library_id,
            room_name=room_name
        ).first()

        if existing_state:
            # Return existing state without creating a duplicate
            return jsonify({"message": "Library room state already exists", "state": existing_state}), 200

        # Create new library room state
        new_state = LibraryRoomState(
            user_id=user_id,
            library_id=library_id,
            room_name=room_name,
            num_lessons=num_lessons,
            lesson_state=initial_lesson_state
        )

        # Add to database and commit
        db.session.add(new_state)
        db.session.commit()

        return jsonify({"message": "Library room state added successfully", "state": new_state}), 201

    except IntegrityError as e:
        # Handle database integrity issues (e.g., unique constraint violations)
        db.session.rollback()
        return jsonify({"error": f"Database integrity error: {str(e)}"}), 400

    except OperationalError as e:
        # Handle database connection issues
        db.session.rollback()
        return jsonify({"error": f"Database connection error: {str(e)}"}), 500

    except Exception as e:
        # Handle unexpected errors
        db.session.rollback()
        return jsonify({"error": f"Failed to add library room state: {str(e)}"}), 500


def increase_lesson_state(user_id, library_id, room_name):

    # Get the state for this user, library, and room
    state = LibraryRoomState.query.filter_by(
        user_id=user_id,
        library_id=library_id,
        room_name=room_name
    ).first()
    
    if not state:
        return None, False  # State not found
    
    # Check if lesson_state can be increased
    if state.lesson_state <= state.num_lessons:
        state.lesson_state += 1
        db.session.commit()
        return state, True
    
    return state, False  # Lesson state already at maximum

def add_factoid_to_library(library_id, room_name, factoid_content, lesson_name):
    # Validate input parameters
    if not isinstance(library_id, int) or library_id <= 0:
        return jsonify({"message": "Invalid or missing library_id. It must be a positive integer."}), 400
    if not room_name or not isinstance(room_name, str):
        return jsonify({"message": "Invalid or missing room_name. It must be a string."}), 400
    if not factoid_content or not isinstance(factoid_content, str):
        return jsonify({"message": "Invalid or missing factoid_content. It must be a string."}), 400
    if not lesson_name or not isinstance(lesson_name, str):
        return jsonify({"message": "Invalid or missing lesson_name. It must be a string."}), 400

    try:
        # Check if the library exists
        library = Library.query.filter_by(id=library_id).first()
        if not library:
            return jsonify({"message": "Library not found with the provided library_id."}), 404
        
        # Create new factoid entry
        factoid = LibraryFactoid(
            library_id=library_id,
            room_name=room_name,
            factoid_content=factoid_content,
            lesson_name=lesson_name
        )

        db.session.add(factoid)
        db.session.commit()

        return (
            jsonify(
                {"message": "Factoid added successfully", "factoid_id": factoid.id}
            ),
            201,
        )

    except IntegrityError as e:
        # Handle specific integrity errors like unique constraint violations
        db.session.rollback()
        return jsonify({"message": "Failed to add factoid due to a database constraint violation."}), 400

    except OperationalError as e:
        # Handle database connection issues
        db.session.rollback()
        return jsonify({"message": "Database connection error. Please try again later."}), 500

    except Exception as e:
        # Handle any other exceptions
        db.session.rollback()
        return jsonify({"message": "An unexpected error occurred: " + str(e)}), 500

def add_question_to_factoid(factoid_id, question_text, correct_choice, wrong_choices, question_type="multiple_choice"):
    # Validate input parameters
    if not isinstance(factoid_id, int) or factoid_id <= 0:
        return jsonify({"error": "Invalid factoid_id. It must be a positive integer."}), 400
    if not question_text or not isinstance(question_text, str):
        return jsonify({"error": "Invalid question_text. It must be a non-empty string."}), 400
    if not isinstance(correct_choice, str) or not correct_choice:
        return jsonify({"error": "Invalid correct_choice. It must be a non-empty string."}), 400
    if not isinstance(wrong_choices, list) or not all(isinstance(choice, str) for choice in wrong_choices):
        return jsonify({"error": "Invalid wrong_choices. It must be a list of non-empty strings."}), 400
    if question_type not in ["multiple_choice", "true_false"]:
        return jsonify({"error": "Invalid question_type. It must be 'multiple_choice' or 'true_false'."}), 400

    try:
        # Check if the factoid exists
        factoid = LibraryFactoid.query.get(factoid_id)
        if not factoid:
            return jsonify({"error": "Factoid not found"}), 404

        # Create the question
        question = LibraryQuestion(
            factoid_id=factoid_id,
            question_text=question_text,
            correct_choice=correct_choice,
            question_type=question_type,
        )
        db.session.add(question)
        db.session.flush()  # Flush to get the question.id before commit

        # Add choices to the question
        add_choices_to_question(question.id, correct_choice, wrong_choices)

        db.session.commit()

        return jsonify({
            "message": "Question and choices added successfully",
            "question_id": question.id
        }), 201

    except IntegrityError as e:
        # Handle database integrity issues (e.g., unique constraint violations)
        db.session.rollback()
        return jsonify({"error": f"Database integrity error: {str(e)}"}), 400

    except OperationalError as e:
        # Handle database connection issues
        db.session.rollback()
        return jsonify({"error": f"Database connection error: {str(e)}"}), 500

    except Exception as e:
        # Handle unexpected errors
        db.session.rollback()
        return jsonify({"error": f"Failed to add question: {str(e)}"}), 500



def add_room_name_to_library(library_id, new_room_name):
    # Validate input
    if not new_room_name or not isinstance(new_room_name, str):
        return jsonify({"error": "Invalid or missing new_room_name. It must be a non-empty string."}), 400

    try:
        # Get the library
        library = Library.query.get(library_id)
        if not library:
            return jsonify({"error": "Library not found"}), 404

        # Initialize room_names if null or invalid
        if library.room_names is None:
            library.room_names = []
        elif not isinstance(library.room_names, list):
            return jsonify({"error": "Invalid room_names format in the database. Expected a list."}), 500

        # Check for duplicates
        if new_room_name in library.room_names:
            return jsonify({"warning": f"Room '{new_room_name}' already exists in this library"}), 200

        # Add new room name
        library.room_names.append(new_room_name)

        # Commit changes
        db.session.commit()

        return jsonify({"message": "Room added successfully", "library_id": library_id, "new_room_name": new_room_name}), 200

    except IntegrityError as e:
        # Handle database integrity issues
        db.session.rollback()
        return jsonify({
            "error": f"Database integrity error: {str(e)}",
            "library_id": library_id
        }), 400

    except OperationalError as e:
        # Handle database connection issues
        db.session.rollback()
        return jsonify({
            "error": f"Database connection error: {str(e)}",
            "library_id": library_id
        }), 500

    except Exception as e:
        # Handle unexpected errors
        db.session.rollback()
        return jsonify({
            "error": f"Failed to add room: {str(e)}",
            "library_id": library_id
        }), 500

def get_factoid(factoid_id):
    factoid = LibraryFactoid.query.get(factoid_id)
    if factoid:
        return jsonify(factoid.as_dict())
    else:
        return jsonify({"message": "Factoid not found"}), 404


def get_question(question_id):
    question = LibraryQuestion.query.get(question_id)
    if question:
        return jsonify(question.as_dict())
    else:
        return jsonify({"message": "Question not found"}), 404


def add_choices_to_question(question_id, correct_choice, wrong_choices):
    try:


        print(question_id, correct_choice, wrong_choices)

        # Add correct choice
        for choice in correct_choice:
            print("choice", choice)
            correct = LibraryQuestionChoice(
                question_id=question_id, choice_text=choice, is_correct=True
            )
            db.session.add(correct)
            
        for choice in wrong_choices:
            print("choice", choice)
            wrong = LibraryQuestionChoice(
                question_id=question_id, choice_text=choice, is_correct=False
            )
            db.session.add(wrong)

        db.session.commit()
        return jsonify({"message": "Choices added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

def get_library_room_names(library_id):
    library = Library.query.get(library_id)
    if not library:
        return jsonify({"message": "Library not found"}), 404
    return jsonify({"room_names": library.room_names}).json["room_names"], 200


def get_library_content(library_id):
    library = Library.query.get(library_id)
    if not library:
        return jsonify({"message": "Library not found"}), 404
    
    factoids = LibraryFactoid.query.filter_by(library_id=library_id).all()
    content_list = []
    
    # Randomly select up to 10 factoids # if we select all of them they get super 
    # long for the prompt, although this might result in duplicate questions
    if len(factoids) > 10:
        factoids = random.sample(factoids, 10)
    
    for factoid in factoids:
        factoid_content = factoid.factoid_content
        questions = LibraryQuestion.query.filter_by(factoid_id=factoid.id).all()
        
        for question in questions:
            question_content = f"Question: {question.question_text}\n"
            factoid_content += question_content
        
        content_list.append(factoid_content)
    full_content = "\n".join(content_list)
    
    return jsonify({"library_content": full_content}), 200

def get_library_settings(library_id):
    library = Library.query.get(library_id)
    if not library:
        return jsonify({"message": "Library not found"}), 404
    return library.difficulty, library.language, library.language_difficulty, library.context

def get_library_topic(library_id):
    library = Library.query.get(library_id)
    return library.library_topic

def get_library_guide(library_id):
    library = Library.query.get(library_id)
    return library.guide

def is_center_room(library_id, room_name):
    library = Library.query.get(library_id)
    if not library:
        return jsonify({"message": "Library not found"}), 404
    return room_name == library.library_topic

def update_game_end(user_id, library_id, room_name):#, score,time, completed_rooms, is_complete):
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        increase_lesson_state(user_id, library_id, room_name)

        # existing_completion = LibraryCompletion.query.filter_by(library_id=library_id, user_id=user_id).first()
        # if existing_completion:
        #     if is_complete and not existing_completion.is_complete:
        #         existing_completion.is_complete = is_complete
        #         existing_completion.completion_date = datetime.utcnow()
        #     if score > existing_completion.score:
        #         existing_completion.score = score
        #         user.experience_points += (score - existing_completion.score)
        #     if time < existing_completion.time:
        #         existing_completion.time = time
                
        #     # Update completed_rooms
        #     current_completed = set(existing_completion.completed_rooms.split(",")) if existing_completion.completed_rooms else set()
        #     current_completed.update(completed_rooms)
        #     existing_completion.completed_rooms = ",".join(sorted(current_completed))
        # else:
        #     new_completion = LibraryCompletion(
        #         library_id=library_id,
        #         user_id=user_id,
        #         score=score,
        #         time=time,
        #         completed_rooms=",".join(sorted(completed_rooms)) if completed_rooms else None,
        #         is_complete=is_complete,
        #         completion_date=datetime.utcnow() if is_complete else None
        #     )
        #     db.session.add(new_completion)
        #     user.experience_points += score

        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Game ended and recorded successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

def get_libraries_info(user_id=None):
    top_liked_libraries = Library.query.order_by(Library.likes.desc()).limit(40).all()
    latest_libraries = Library.query.order_by(Library.id.desc()).limit(40).all()

    top_liked_dicts = [model_to_dict(library, exclude=['room_names', 'factoids']) for library in top_liked_libraries]
    latest_dicts = [model_to_dict(library, exclude=['room_names', 'factoids']) for library in latest_libraries]

    response_data = {
        'most_liked': top_liked_dicts,
        'latest': latest_dicts
    }

    if user_id is not None:
        my_libraries = Library.query.filter_by(user_id=user_id).order_by(Library.id.desc()).limit(40).all()
        my_dicts = [model_to_dict(library, exclude=['room_names', 'factoids']) for library in my_libraries]
        response_data['mine'] = my_dicts

    return jsonify(response_data)

def like_library(library_id):
    try:
        library = Library.query.get(library_id)
        if library is None:
            return jsonify({'error': 'Library not found'}), 404
        
        library.likes += 1
        db.session.commit()
        return jsonify({'message': 'Like added successfully', 'likes': library.likes}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def has_default_image(library_id):
    try:
        library = Library.query.get(library_id)
        if library is None:
            return jsonify({'error': 'Library not found'}), 404
        
        has_default = library.image_url == Library.DEFAULT_IMAGE_URL
        return jsonify({'has_default_image': has_default}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_library_image(library_id, image_url):
    try:
        library = Library.query.get(library_id)
        if library is None:
            return jsonify({'error': 'Library not found'}), 404
        
        if not image_url:
            image_url=Library.DEFAULT_IMAGE_URL
        library.image_url = image_url
        db.session.commit()
        return jsonify({'message': 'Image updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def get_available_generated_rooms(library_id):
    library = Library.query.get(library_id)
    if not library:
        return jsonify({"message": "Library not found"}), 404

    room_names = library.room_names if library.room_names else []
    available_rooms = []

    for room_name in room_names:
        factoids_count = LibraryFactoid.query.filter_by(library_id=library_id, room_name=room_name).count()
        if factoids_count >= 4 and library.library_topic != room_name:
            available_rooms.append(room_name)

    return available_rooms

def get_top_scores_by_unique_users(limit=5):
    """
    Returns the top 'limit' scores across all libraries, ensuring unique users,
    returning the user's email instead of user_id.
    """
    subquery = (
        db.session.query(
            LibraryCompletion.user_id,
            func.min(LibraryCompletion.time).label('min_time')
        )
        .group_by(LibraryCompletion.user_id)
        .subquery()
    )

    query = (
        db.session.query(
            User.email,
            LibraryCompletion.library_id,
            LibraryCompletion.time
        )
        .select_from(LibraryCompletion)
        .join(User, LibraryCompletion.user_id == User.id)
        .join(
            subquery,
            (LibraryCompletion.user_id == subquery.c.user_id) & 
            (LibraryCompletion.time == subquery.c.min_time)
        )
        .order_by(subquery.c.min_time.asc())
        .limit(limit)
    )

    return query.all()



def get_library_top_scores_by_unique_users(library_id, limit=5):
    """
    Returns the top 'limit' scores for a specific library, ensuring unique users,
    returning the user's email instead of user_id.
    """
    subquery = (
        db.session.query(
            LibraryCompletion.user_id,
            func.min(LibraryCompletion.time).label('min_time')
        )
        .filter(LibraryCompletion.library_id == library_id)
        .group_by(LibraryCompletion.user_id)
        .subquery()
    )

    query = (
        db.session.query(
            User.email,
            LibraryCompletion.library_id,
            LibraryCompletion.time
        )
        .select_from(LibraryCompletion)
        .join(User, LibraryCompletion.user_id == User.id)
        .join(
            subquery,
            (LibraryCompletion.user_id == subquery.c.user_id) &
            (LibraryCompletion.time == subquery.c.min_time)
        )
        .filter(LibraryCompletion.library_id == library_id)
        .order_by(subquery.c.min_time.asc())
        .limit(limit)
    )

    return query.all()





# UTILSSSS 
        
# Utility function to convert a model instance to a dictionary
def model_to_dict(model_instance, exclude=None):
    exclude = exclude or []
    return {
        c.name: getattr(model_instance, c.name)
        for c in model_instance.__table__.columns
        if c.name not in exclude
    }

# Adding as_dict methods to models
Library.as_dict = lambda self: model_to_dict(self)
LibraryFactoid.as_dict = lambda self: model_to_dict(self)
LibraryQuestion.as_dict = lambda self: model_to_dict(self)
LibraryQuestionChoice.as_dict = lambda self: model_to_dict(self)
LibraryCompletion.as_dict = lambda self: model_to_dict(self)
