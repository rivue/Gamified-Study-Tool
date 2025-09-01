from datetime import datetime
from flask import jsonify, current_app as app
from sqlalchemy import func, distinct
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from contextlib import contextmanager
from sqlalchemy.orm import joinedload
import random
import math
import string
import time
import secrets
from app import InvalidJoinCodeError, UserAlreadyMemberError, MaxUnitsReachedError, NotFoundError
from sqlalchemy import or_
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
        db.session.flush()
        db.session.commit()

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
    except IntegrityError:
        db.session.rollback()
        return (
            jsonify(
                {"message": "Library Favorites object already exists"}
            ),
            400)
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400
    
def create_unit_and_add(library_id, unit_name, position=-1):
    try:
        with db_transaction():
            unit = LibraryUnit(
                library_id=library_id,
                unit_name=unit_name,
                position=position  # use -1 for placeholder since it doesn't allow None
            )

            library = Library.query.get(library_id)

            if not library:
                print("Warning: not library in create_unit_and_add.")
                raise NotFoundError

            if len(library.units) >= 20:
                print("Warning: Library has reached maximum number of units.")
                raise MaxUnitsReachedError

            db.session.add(unit)

            if not unit:
                print("Warning: not unit in create_unit_and_add.")
                raise NotFoundError

            if position != -1:
                library.attach_unit(unit, position)
            else:
                library.attach_unit(unit)

            db.session.flush()  # Flush to get the unit ID before commit

            return (
                jsonify(
                    {"message": "Unit created and added successfully", "unit": unit.id}
                ),
                201,
            )
    except MaxUnitsReachedError as e:
        print(f"Library has reached max amounts of units in create_unit_and_add: {str(e)}")
        raise
    except NotFoundError as e:
        print(f"Library or Unit not found error in create_unit_and_add: {str(e)}")
        raise
    except Exception as e:
        print("something else")
        print(f"Exception in create_unit_and_add: {str(e)}")
        return jsonify({"message": str(e)}), 400
    
def create_section_and_add(unit_id, section_name, position=-1):
    try:

        if not section_name or not section_name.strip():
            raise ValueError("Section name cannot be empty.")

        # Note to future: if this query starts taking forever, move duplicate name logic to add section / add unit frontend (or equivalent future component)
        unit = LibraryUnit.query.get(unit_id)
        if not unit:
            print("Warning: not unit in create_section_and_add.")
            raise NotFoundError

        if len(unit.sections) >= 20:
            return jsonify({"error": "Unit has reached maximum number of sections (20)"}), 400
        
        if not unit:
            raise ValueError(f"Unit with ID {unit_id} not found.")
        
        library = unit.library
        if not library:
            raise ValueError(f"Library not found for unit {unit_id}.")
        
        # Note to future: if this query starts taking forever, move duplicate name logic to add section / add unit frontend (or equivalent future component)
        existing_section_in_unit = LibrarySection.query.filter_by(unit_id=unit_id, section_name=section_name).first()
        if existing_section_in_unit:
            raise ValueError(f"Error: Section name '{section_name}' already exists in this unit.")

        # Note to future: if this join method starts taking forever, move duplicate name logic to add section / add unit frontend (or equivalent future component)
        existing_section_in_library = LibrarySection.query.join(LibraryUnit).filter(
            LibraryUnit.library_id == library.id,
            LibrarySection.section_name == section_name
        ).first()
        if existing_section_in_library:
            # This error message helps distinguish it from the unit-specific duplicate.
            raise ValueError(f"Error: Section name '{section_name}' already exists in this library in a different unit.")

        section = LibrarySection(
            unit_id=unit_id,
            section_name=section_name,
            position=position
        )
       
        if not section:
            print("Warning: not section in create_section_and_add.")
            raise NotFoundError(f"Section creation failed for section name '{section_name}' in unit {unit_id} via unit.add_section. The method may have returned None.")
        
        if position != -1:
            unit.attach_section(section, position)
        else:
            unit.attach_section(section)
            
        db.session.add(section)
        db.session.flush()  # Flush to get the section ID before commit

        return (
            jsonify(
                {"message": "Section created and added successfully", "section": section.id}
            ),
            201,
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    except NotFoundError as e:
        print(f"Library or Section not found error in create_unit_and_add: {str(e)}")
        raise
    except ValueError as e:
        raise

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
            unit_to_position_map[unit.unit_name] = (unit.position, unit.id)
            unit_to_section_map[unit.unit_name] = []
            for section in unit.sections:
                room_names.append((section.section_name, section.id))
                section_to_unit_map[section.section_name] = (unit.id, section.id)
                unit_to_section_map[unit.unit_name].append((section.id, section.section_name))
                    
        library_data["room_names"] = room_names

    library_data["clicks"] = library.clicks
    library_data["section_to_unit_map"] = section_to_unit_map
    library_data["unit_to_section_map"] = unit_to_section_map
    library_data["unit_to_position_map"] = unit_to_position_map

    favorited_status = LibraryFavorites.query.filter_by(
        user_id=user_id,
        library_id=library_id
    ).first()

    library_data["favorited_status"] = favorited_status.is_favorited

    membership_status = LibraryMembership.query.filter_by(
        user_id=user_id,
        library_id=library_id
    ).first()
    
    if membership_status:
        library_data["membership_status"] = True
    else:
        library_data["membership_status"] = False

    return jsonify(library_data)

def get_library_scores(library_id):
    try:
        memberships = (
            LibraryMembership.query.filter_by(library_id=library_id)
            .join(User)
            .order_by(LibraryMembership.points.desc())
            .options(joinedload(LibraryMembership.user))
            .all()
        )

        if not memberships:
            return jsonify({'error': 'No memberships found for the given library'}), 404

        member_list = [
            {
                'username': membership.user.username,
                'name': membership.user.first_name,
                'points': membership.points or 0,
            }
            for membership in memberships
            if membership.user
        ]

        return jsonify(member_list)

    except Exception as e:
        print(f"Error in get_library_scores: {e}")
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
        print(f"{state}")

        return state.as_dict() if state else None

def add_points_to_member(user_id, library_id, questions_right, total_questions):
    if total_questions == 0:
        return # Avoid division by zero

    membership = LibraryMembership.query.filter_by(
        user_id=user_id, library_id=library_id
    ).first()

    if not membership:
        print(f"Warning: Could not find membership for user {user_id} in library {library_id} to add points.")
        return

    points_to_add = math.floor(100 * (questions_right / total_questions))
    
    if points_to_add > 0:
        membership.points = (membership.points or 0) + points_to_add
        db.session.commit()


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
                    print("create unit and add error")
                    message = response_obj.get_json()['message']
                    return jsonify(status="error", message=message.to_str()), 200
                unit_id = response_obj.get_json()["unit"]

                curr += 1
                section_position = 0
                for section in sections:

                    # 2.1 + 2.2) create sections and add to unit
                    response_obj, status_code = create_section_and_add(unit_id, section, section_position)

                    print("response from create section and add") 
                    if status_code != 201:
                        print("create section and add error")
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
                    section_position += 1
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
    

def save_section_contents(library_id, section, section_contents_map, unit_id, position):

    try:
        responses = []
        num_lessons = 3

        with db_transaction():

            # 1.1 + 1.2) create sections and add to parent unit
            response_obj, status_code = create_section_and_add(unit_id, section, position)
            print("after add_section")
            if status_code != 201:
                print("create section and add error")
                print(response_obj.get_json()['message'])
                message = response_obj.get_json()['message']
                return jsonify(status="error", message=message.to_str()), 200
            
            section_id = response_obj.get_json()["section"]
            print("after section_id")
            
            # 2) add room states for every user in the library
            library = Library.query.get(library_id)
            for membership in library.memberships:
                add_section_user_state(membership.user_id, library_id, section_id, num_lessons)
                print(f"{membership}")
            
            if "factoids" not in section_contents_map:
                print(f"Warning: No factoids for section '{section}'")
            
            print(f"Processing section: {section}")
            print(f"Section content structure: {type(section_contents_map)}")
            print(f"Keys in section content: {section_contents_map.keys()}")
            
            # 4.1 + 4.2) create factoids and add to sections
            factoids = section_contents_map["factoids"]
            
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
        print("Exception save_section_content")
        print("message: ", str(e))
        return jsonify({"message": str(e)}), 400
    


def retrieve_library_room_contents(library_id, section_id, user_id):

    try:
        # user HAS to be logged
        if not user_id:
            return None

        # query lesson room state map
        # map user id, library id, and room name in map to retrieve state
        # send state and factoids for that state back
        curr_state = get_library_room_state(user_id, library_id, section_id)

        if not curr_state:
            return None
        
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
        
        if len(factoids) < 3:
            return None
        
        room_contents = []
        for factoid in factoids:
            questions = []
            for question in factoid.questions:
                question_choices = question.choices if question.choices else []
                # question_choices = question.choices.all() if question.choices else []
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
    
    except Exception as e:
        print(f"Exception retrieve_library_room_contents: {str(e)}")   
        raise

def join_library(user_id: int, library_id: int, join_code: str = None):
    """
    Atomically:
      • add membership (or raise IntegrityError if already member)
      • pre-populate room states
      • create favorite row
    """
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")

    library = Library.query.filter(Library.id == library_id).first()
    if not library:
        raise ValueError(f"Library {library_id} not found")
    
    # Check join conditions
    if library.is_public:
        # Public library - no join code needed
        pass
    else:
        # Private library - requires matching join code
        if not join_code or library.join_code != join_code:
            raise InvalidJoinCodeError("Invalid join code for private library")

    already_exists = db.session.query(LibraryMembership) \
        .filter_by(user_id=user_id, library_id=library_id) \
        .first()
    if already_exists:
        raise UserAlreadyMemberError("user already in this library")

    try:
        membership = LibraryMembership(user_id=user.id, library_id=library.id, joined_at=datetime.now())
        db.session.add(membership)
        # bulk-insert room states

        # Note: redundant when generating library for first time - maybe move to after save_library_room_contents
        states = [
            LibraryRoomState(user_id=user.id,
                             library_id=library.id,
                             room_name="placeholder",
                             section_id=section.id,
                             num_lessons=3,
                             lesson_state=1)
            for unit in library.units for section in unit.sections
        ]
        db.session.bulk_save_objects(states)

        db.session.add(LibraryFavorites(user_id=user.id,
                                            library_id=library.id,
                                            is_favorited=False))
        db.session.commit()
        return jsonify({"message": "User added to library successfully"}), 201
    
    except IntegrityError as e:
        db.session.rollback()
        print(f"{e}")
        raise UserAlreadyMemberError  # your custom error
    except Exception as e:
        db.session.rollback()
        print(f"Error in join_library: {e}")
    
def leave_library(user_id: int, library_id: int):
        
        try:
            with db_transaction():
                membership = LibraryMembership.query.filter_by(user_id=user_id, library_id=library_id).first()
                if not membership:
                    return jsonify(status="error", message="You are not a member of this course."), 403
                print("after membership")
                # Delete LibraryMembership (LibraryRoomState should cascade delete)
                db.session.delete(membership)
                print("after delete membership")
                # Delete LibraryFavorites if exists
                favorite = LibraryFavorites.query.filter_by(user_id=user_id, library_id=library_id).first()
                if favorite:
                    db.session.delete(favorite)
                print("after library favorices")
                # NOTE: add cascade effect to library room state
                # Explicitly delete LibraryRoomState as a fallback, though cascade should handle it.
                # This is more of a verification step or a safeguard.
                # If cascade is confirmed to work reliably, this explicit delete can be removed.
                # LibraryRoomState.query.filter_by(user_id=user_id, library_id=library_id).delete()
                print("after delete library room state")
        except NotFoundError as e:
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            raise

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
    
    return new_state

def increase_lesson_state(user_id, library_id, section_id):

    # Get the state for this user, library, and room
    state = LibraryRoomState.query.filter_by(
        user_id=user_id,
        library_id=library_id,
        section_id=section_id
    ).first()
    print(state)
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
        db.session.flush()  # Flush to get the factoid ID before commit
        
        return (
            jsonify(
                {"message": "Factoid added successfully", "factoid_id": factoid.id}
            ),
            201,
        )
    except Exception as e:
        print(f"Error in add_factoid_to_section: {str(e)}")
        raise

def add_question_to_factoid(factoid_id, question_text, correct_choice, wrong_choices, question_type):
    try:
        question = LibraryQuestion(
            factoid_id=factoid_id,
            question_text=question_text,
            correct_choice=correct_choice,
            question_type=question_type,
        )
        db.session.add(question)
        db.session.flush()

        # Add choices to the question
        add_choices_to_question(question.id, correct_choice, wrong_choices)

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
        print(f"Error in add_question_to_factoid: {str(e)}")
        raise

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

        return jsonify({"message": "Choices added successfully"}), 201
    except Exception as e:
        print(f"Error in add_choices_to_question: {str(e)}")
        raise

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
        return jsonify({'status': 'success', 'message': 'Game ended and recorded successfully.', 'current_streak': user.streak_count, 'highest_streak': user.highest_streak}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

def get_libraries_info(user_id=None, browse=False):

    # top_liked_libraries = Library.query.order_by(Library.likes.desc()).limit(40).all()

    # latest_libraries = Library.query.order_by(Library.id.desc()).limit(40).all()

    # top_liked_dicts = [model_to_dict(library, exclude=['room_names', 'factoids']) for library in top_liked_libraries]
    # latest_dicts = [model_to_dict(library, exclude=['room_names', 'factoids']) for library in latest_libraries]

    # response_data = {
    #     'most_liked': top_liked_dicts,
    #     'latest': latest_dicts
    # }
    
    if browse:
        
        response = {}

        # explore_libraries  = db.session.query(Library).filter_by(user_id not in Library.memberships).all()
        explore_libraries = (Library.query
            .filter(
                ~Library.id.in_(
                db.session.query(LibraryMembership.library_id)
                .filter_by(user_id=user_id)
                )#
                # Library.is_public.is_(True)
                )
            .all())

        # come back here --> get username from library to send to explore courses
        explore_libraries_data = []
        for library in explore_libraries:
            library_dict = model_to_dict(library, exclude=['room_names', 'factoids'])

            user = User.query.get(library_dict['owner_id'])
            name = None
            if user:
                name = user.username
                
            explore_libraries_data.append([library_dict, name])
        
        response["explore_libraries"] = explore_libraries_data
        return jsonify(response)
    
    else:
        response = {}

        if user_id:
            
            my_libraries = (Library.query.filter_by(owner_id=user_id).order_by(Library.id.desc()).all())
            response["mine"] = [model_to_dict(library, exclude=['room_names', 'factoids']) for library in my_libraries]

            joined_q = (
                db.session.query(Library)
                .join(LibraryMembership, 
                    Library.id == LibraryMembership.library_id)
                    .filter(LibraryMembership.user_id == user_id,
                            Library.owner_id != user_id)
            )
            joined_public  = joined_q.filter(Library.is_public.is_(True)).all()

            joined_private = joined_q.filter(Library.is_public.is_(False)).all()

            response["joined_public"]  = [model_to_dict(l, exclude=["room_names", "factoids"])
                                        for l in joined_public]
            response["joined_private"] = [model_to_dict(l, exclude=["room_names", "factoids"])
                                        for l in joined_private]
            
            favorited_map = {fav.library_id: fav.is_favorited for fav in LibraryFavorites.query.filter_by(user_id=user_id).all()}
            response["favorites_map"] = favorited_map

        return jsonify(response)
    
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