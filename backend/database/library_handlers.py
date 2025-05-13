from datetime import datetime
from flask import jsonify
from sqlalchemy import func, distinct
from contextlib import contextmanager
import random
import math
import string
import time
import secrets
from database.models import (
    db,
    User,
    Library,
    LibraryUnit,
    LibrarySection,
    LibraryFactoid,
    LibraryQuestion,
    LibraryQuestionChoice,
    LibraryRoomState,
    LibraryMembership,
    LibraryFavorites,
    LibraryCompletion
)

@contextmanager
def db_transaction():
    try:
        yield
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def create_library(
    user_id, library_topic, difficulty, language, language_difficulty, guide, is_public
):
    
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        code_length = 8
        alphabet = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(secrets.choice(alphabet) for _ in range(code_length))
            # quick in‑memory test; the UNIQUE constraint is the final guard
            if not db.session.query(Library.id).filter_by(join_code=code).first():
                break
            time.sleep(0.01)

        library = Library(
            owner_id=user_id,
            owner=user,
            library_topic=library_topic,
            room_names=[],
            difficulty=difficulty,
            language=language,
            language_difficulty=language_difficulty,
            guide=guide,
            join_code=code,
            is_public=is_public,
        )
        db.session.add(library)
        db.session.commit()
        membership, status = create_library_membership(user_id, library.id)
        if status != 200:
            return jsonify({"message": f"Library error creating: + {membership}"}), status
        return (
            jsonify(
                {"message": "Library created successfully", "library_id": library.id}
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

def create_library_favorite(
    user_id, library_id
):
    try:
        library_favorites = LibraryFavorites(
            user_id=user_id,
            library_id=library_id,
            is_favorited=False,
        )
        db.session.add(library_favorites)
        db.session.commit()
        return (
            jsonify(
                {"message": "Library Favorites object created successfully", "library_favorites_id": library_favorites.id}
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400
    
def create_unit_and_add(library_id, unit_name, position=None):
    try:
        unit = LibraryUnit(
            library_id=library_id,
            unit_name=unit_name
        )

        library = Library.query.get(library_id)

        db.session.add(unit)

        if len(library.units) >= 20:
            return jsonify({"error": "Library has reached maximum number of units"}), 400

        if not unit or not library:
            return jsonify({"error": "Library or Unit not found"}), 404

        if position is not None:
            library.attach_unit(unit, position)
        else:
            library.attach_unit(unit)

        db.session.flush()  # Flush to get the unit ID before commit
        db.session.commit()

        return (
            jsonify(
                {"message": "Unit created and added successfully", "unit": unit.id}
            ),
            201,
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
def create_section_and_add(unit_id, section_name):
    try:
        unit = LibraryUnit.query.get(unit_id)

        if not unit or not section_name:
            return jsonify({"error": "Library or Section not found"}), 404

        section = unit.add_section(section_name)

        if not section:
            return jsonify({"error": "Section failed to generate"}), 404
        
        db.session.flush()

        return (
            jsonify(
                {"message": "Section created and added successfully", "section": section.id}
            ),
            201,
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 400

def get_library_id(library_topic, difficulty, language, language_difficulty, guide):
    try:
        library = Library.query.filter_by(
            library_topic=library_topic,
            difficulty=difficulty,
            language=language,
            language_difficulty=language_difficulty,
            guide=guide
        ).first()

        if not library:
            return None

        return library.id

    except Exception as e:
        print(f"Error fetching library: {str(e)}")
        return None

def get_library(library_id, user_id=None, click=True):

    library = Library.query.get(library_id)

    if not library:
        return jsonify({"message": "Library not found"}), 404
    
    if click:
        library.clicks += 1
        db.session.commit()
        
    library_data = library.as_dict()
    library_data["tutorial"] = True # default
    library_data["is_public"] = library.is_public

    section_to_unit_map = {}
    unit_to_section_map = {}
    unit_to_position_map = {}
    if user_id:
        room_names = []
        for unit in library.units:
            unit_to_position_map[unit.unit_name] = unit.position
            unit_to_section_map[unit.unit_name] = []
            for section in unit.sections:
                room_names.append((section.section_name, section.id))
                section_to_unit_map[section.section_name] = (unit.id, section.id)
                unit_to_section_map[unit.unit_name].append((section.id, section.section_name))
                    
        library_data["room_names"] = room_names

        existing_completion = LibraryCompletion.query.filter_by(library_id=library_id, user_id=user_id).first()
        if existing_completion:
            library_data["score"] = existing_completion.score
            library_data["best_time"] = existing_completion.time
            library_data["completion"] = len(existing_completion.completed_rooms.split(","))*4
        any_completion = LibraryCompletion.query.filter_by(user_id=user_id, is_complete=True).first()

        if any_completion:
            library_data["tutorial"] = False

    library_data["clicks"] = library.clicks
    library_data["section_to_unit_map"] = section_to_unit_map
    library_data["unit_to_section_map"] = unit_to_section_map
    library_data["unit_to_position_map"] = unit_to_position_map

    favorited_status = LibraryFavorites.query.filter_by(
        user_id=user_id,
        library_id=library_id
    ).first()

    library_data["favorited_status"] = favorited_status.is_favorited
    
    return jsonify(library_data)

def get_library_scores(library_id):
    
    # TODO: update once I implement a points system

    try:

        memberships = LibraryMembership.query.filter_by(library_id=library_id).all()
        
        if not memberships:
            return jsonify({'error': 'No memberships found for the given library'}), 404
        
        member_list = []
        for membership in memberships:
                member_list.append({
                    'user_id': membership.user_id,
                })

        return jsonify(member_list)
    
    except Exception as e:
        print("no")
        return jsonify({'error': str(e)}), 500
    
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

def get_library_room_state(user_id, library_id, section_id=None):

    if not section_id: # for all rooms (ex: map page)
        room_states = LibraryRoomState.query.filter_by(
            user_id=user_id,
            library_id=library_id
        ).all()

        return [s.as_dict() for s in room_states]
    
    else: # for a specific room
        state = LibraryRoomState.query.filter_by(
            user_id=user_id,
            library_id=library_id,
            # room_name="placeholderlrs1234",
            section_id=section_id,
        ).first()
        return state.as_dict() if state else None

def save_library_room_contents(library_id, section_unit_map, section_contents_map, user_id):

    try:
        responses = []
        num_lessons = 3

        with db_transaction():
            curr = 1
            for unit_name, sections in section_unit_map.items():

                # 1.1 + 1.2) create unit and add to library
                response_obj, status_code = create_unit_and_add(library_id, unit_name)
                                
                if status_code != 201:
                    message = response_obj.get_json()['message']
                    return jsonify(status="error", message=message.to_str()), 200
                                
                unit_id = response_obj.get_json()["unit"]

                curr += 1
                for section in sections:

                    # 2.1 + 2.2) create sections and add to unit
                    response_obj, status_code = create_section_and_add(unit_id, section)

                    if status_code != 201:
                        print(response_obj.get_json()['message'])
                        message = response_obj.get_json()['message']
                        return jsonify(status="error", message=message.to_str()), 200
                    
                    section_id = response_obj.get_json()["section"]

                    
                    # 3) add room states
                    add_section_user_state(user_id, library_id, section_id, num_lessons)

                    if "factoids" not in section_contents_map[section]:
                        print(f"Warning: No factoids for section '{section}'")
                        continue

                    print(f"Processing section: {section}")
                    print(f"Section content structure: {type(section_contents_map[section])}")
                    print(f"Keys in section content: {section_contents_map[section].keys()}")
                    
                    # 4.1 + 4.2) create factoids and add to sections
                    factoids = section_contents_map[section]["factoids"]
                    
                    # 4) add factoids to sections
                    for index, item in enumerate(factoids):
                        lesson_name = "factoid_set_" + str(math.floor(index/9) + 1)
                        
                        factoid_content = item["factoid_text"]
                        question_data = item["question"]
                        
                        section = LibrarySection.query.get(section_id)
                        
                        # Add factoid to library
                        factoid_response, status_code = add_factoid_to_section(
                            section_id, factoid_content, lesson_name
                        )

                        if status_code != 201:
                            return factoid_response
                        factoid_id = factoid_response.get_json()["factoid_id"]

                        # Add question to factoid
                        question_type = question_data["type"]
                        question_text = question_data["text"]
                        correct_choice = question_data["correct_choice"]
                        
                        # wrong_choices = question_data["wrong_choices"]
                        wrong_choices = question_data.get("wrong_choices", [])

                        question_response, status_code = add_question_to_factoid(
                            factoid_id, question_text, correct_choice, wrong_choices, question_type
                        )
                        if status_code != 201:
                            return question_response
                        responses.append(
                            {
                                "factoid_response": factoid_response.json,
                                "question_response": question_response.json,
                            }
                        )

                     
        return jsonify(status="success", data=responses)
    
    except Exception as e:
        print("Exception save_library_room_contents")
        print("message: ", str(e))
        return jsonify({"message": str(e)}), 400


def retrieve_library_room_contents(library_id, section_id, user_id):

    # user HAS to be logged
    if not user_id:
        return None

    # query lesson room state map
    # map user id, library id, and room name in map to retrieve state
    # send state and factoids for that state back
    curr_state = get_library_room_state(user_id, library_id, section_id)

    if not curr_state:
        return None
    
    print("after curr_state check")
    
    if curr_state["lesson_state"] > curr_state["num_lessons"]:
        # User has completed all lessons, randomly get 7-9 factoids

        all_factoids = LibraryFactoid.query.filter_by(
            section_id=section_id
        ).all()
    
        # Randomly select between 7-9 factoids or all if less than 7
        num_factoids = min(random.randint(7, 9), len(all_factoids))
        factoids = random.sample(all_factoids, num_factoids) if len(all_factoids) >= num_factoids else all_factoids

    else:
        # Get factoids for the current lesson state
        factoids = LibraryFactoid.query.filter_by(
            section_id=section_id, lesson_name=f"factoid_set_{curr_state['lesson_state']}"
        ).all()
    
    print(f"length of factoids: {len(factoids)}")

    if len(factoids) < 3:
        return None
    
    print(f"factoids: {factoids}")

    room_contents = []
    for factoid in factoids:
        questions = []
        for question in factoid.questions:
            question_choices = question.choices.all() if question.choices else []
            wrong_choices = [
                choice.choice_text
                for choice in question_choices
                if not choice.is_correct
            ]
            correct_choice = next(
                (
                    choice.choice_text
                    for choice in question_choices
                    if choice.is_correct
                ),
                None,
            )
            questions.append(
                {
                    "question_text": question.question_text,
                    "correct_choice": correct_choice,
                    "wrong_choices": wrong_choices,
                    "question_type": question.question_type,
                }
            )
        room_contents.append(
            {"factoid_text": factoid.factoid_content, "questions": questions, "room_state": curr_state}
        )

    return {"factoids": room_contents}

def add_section_user_state(user_id, library_id, section_id, num_lessons, initial_lesson_state=1):

    # Check if a record already exists for this user, library, and room
    existing_state = LibraryRoomState.query.filter_by(
        user_id=user_id,
        section_id=section_id,
    ).first()
    
    if existing_state:
        return existing_state
    
    # Create new library room state
    new_state = LibraryRoomState(
        user_id=user_id,
        library_id=library_id,
        room_name="placeholder",
        section_id=section_id,
        num_lessons=num_lessons,
        lesson_state=initial_lesson_state
    )
    
    # Add to database and commit
    db.session.add(new_state)
    db.session.commit()
    
    return new_state

def increase_lesson_state(user_id, library_id, section_id):

    # Get the state for this user, library, and room
    state = LibraryRoomState.query.filter_by(
        user_id=user_id,
        library_id=library_id,
        section_id=section_id
    ).first()
    
    if not state:
        return None, False  # State not found
    
    # Check if lesson_state can be increased
    if state.lesson_state <= state.num_lessons:
        state.lesson_state += 1
        db.session.commit()
        return state, True
    
    return state, False  # Lesson state already at maximum

def get_library_favorited_status(user_id, library_id):
    try:
        library_favorites = LibraryFavorites.query.filter_by(
            library_id=library_id,
            user_id=user_id
        ).first()


        if not library_favorites:
            return jsonify({"message": "Library favorites not found"}), 404

        library = Library.query.get(library_id)

        if not library:
            return jsonify({'error': 'Library not found'}), 404
        
        response_data = {}
        
        response_data["library_favorites"] = library_favorites
        response_data["num_favorites"] = library.likes
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

def update_library_favorited_status(user_id, library_id, status: bool):
    try:
        if status not in [True, False]:
            return jsonify({"message": "Invalid status"}), 400

        library_favorites = LibraryFavorites.query.filter_by(
            library_id=library_id,
            user_id=user_id
        ).first()
        if not library_favorites:
            return jsonify({"error": "Library favorites not found"}), 404
        
        library = Library.query.get(library_id)
        if library is None:
            return jsonify({'error': 'Library not found'}), 404
        
        if library_favorites.is_favorited != status:

            update_library_likes(library_id, status)        
            library_favorites.is_favorited = status
            db.session.commit()
        return jsonify({"message": "Library favorites status updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
def get_library_visibility_status(library_id):
    try:
        library = Library.query.get(library_id)
        if library is None:
            return jsonify({'error': 'Library not found'}), 404
        visibility_status = library.is_public
        return jsonify({"is_public": visibility_status}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def update_library_visibility_status(user_id, library_id, status: bool):
    try:
        
        user = User.query.get(user_id)
        library = Library.query.get(library_id)        
        
        if not user.owned_libraries.filter_by(id=library.id).first():
            return jsonify({'error': 'You are not the owner!'}), 400
        if library is None:
            return jsonify({'error': 'Library not found'}), 404
        if status not in [True, False]:
            return jsonify({"error": "Invalid status"}), 400
        
        join_code = library.set_privacy(status)
        
        db.session.commit()
        return jsonify({"join_code": join_code, "message": "Library visibility status updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
def create_library_membership(user_id, library_id):
    try:
        library = Library.query.get(library_id)
        if library is None:
            return jsonify({'error': 'Library not found'}), 404
        
        user = User.query.get(user_id)
        if user is None:
            return jsonify({'error': 'User not found'}), 404

        membership = LibraryMembership(
            user_id=user_id,
            library_id=library_id,
            joined_at=datetime.utcnow()
        )
        db.session.add(membership)
        db.session.commit()
        return jsonify({"message": "Library membership added successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400
    
def update_library_likes(library_id, status: bool):
    try:
        library = Library.query.get(library_id)
        if library is None:
            return jsonify({'error': 'Library not found'}), 404
        
        if status not in [True, False]:
            return jsonify({"message": "Invalid status"}), 400
        if status:
            library.likes += 1
        else:
            library.likes = max(0, library.likes - 1)
        db.session.commit()
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

def add_factoid_to_section(section_id, factoid_content, lesson_name):
    try:
        factoid = LibraryFactoid(
            section_id=section_id, lesson_name=lesson_name, factoid_content=factoid_content
        )
        db.session.add(factoid)
        db.session.commit()
        return (
            jsonify(
                {"message": "Factoid added successfully", "factoid_id": factoid.id}
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

def add_question_to_factoid(factoid_id, question_text, correct_choice, wrong_choices, question_type):
    try:
        question = LibraryQuestion(
            factoid_id=factoid_id,
            question_text=question_text,
            correct_choice=correct_choice,
            question_type=question_type,
        )
        db.session.add(question)
        db.session.flush()  # Flush to get the question_id before commit

        # Add choices to the question
        add_choices_to_question(question.id, correct_choice, wrong_choices)

        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Question and choices added successfully",
                    "question_id": question.id,
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

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
            # print("choice", choice)
            correct = LibraryQuestionChoice(
                question_id=question_id, choice_text=choice, is_correct=True
            )
            db.session.add(correct)
            
        for choice in wrong_choices:
            # print("choice", choice)
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

def update_game_end(user_id, library_id, section_id):
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
         
        increase_lesson_state(user_id, library_id, section_id)

        user.update_daily_streak()

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
        
        my_libraries = Library.query.filter_by(owner_id=user_id).order_by(Library.id.desc()).all()

        favorited_map = {fav.library_id: fav.is_favorited for fav in LibraryFavorites.query.filter_by(user_id=user_id).all()}
        my_libraries = [lib for lib in my_libraries if len(lib.room_names) == 0]  # Filter for empty room_names
        my_libraries = my_libraries[:40]
        my_dicts = [model_to_dict(library, exclude=['room_names', 'factoids']) for library in my_libraries]
        response_data['mine'] = my_dicts
        response_data["favorites_map"] = favorited_map

    return jsonify(response_data)
    
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
LibraryUnit.as_dict = lambda self: model_to_dict(self)
LibrarySection.as_dict = lambda self: model_to_dict(self)
LibraryFactoid.as_dict = lambda self: model_to_dict(self)
LibraryQuestion.as_dict = lambda self: model_to_dict(self)
LibraryRoomState.as_dict = lambda self: model_to_dict(self)
LibraryQuestionChoice.as_dict = lambda self: model_to_dict(self)
LibraryCompletion.as_dict = lambda self: model_to_dict(self)
LibraryMembership.as_dict = lambda self: model_to_dict(self)