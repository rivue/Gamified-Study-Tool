from database.models import db, User, Challenge, Lesson, UserAction, Achievement, UserAchievement, Feedback,LibraryRoomState,LibraryCompletion
from utils import extract_single_emoji
from sqlalchemy.exc import SQLAlchemyError
import pytz

history_limit = 16
MAX_LESSON_NAME_LENGTH = 200
MAX_CHALLENGE_NAME_LENGTH = 200

def award_lesson_experience(user_id):
    user = User.query.get(user_id)
    if user:
        user.experience_points += 100
        db.session.commit()    

def set_system_role(user_id, role):
    user = User.query.get(user_id)
    if user:
        user.system_role = role
        db.session.commit()

def get_system_role(user_id, lesson_id=None):
    if lesson_id:
        lesson = Lesson.query.filter_by(user_id=user_id, id=lesson_id).first()
        return lesson.system_role if lesson else None
    user = User.query.get(user_id)
    return user.system_role if user else None

def set_mentor_name(user_id, name):
    user = User.query.get(user_id)
    if user:
        user.mentor_name = name
        db.session.commit()

def get_mentor_name(user_id):
    user = User.query.get(user_id)
    return user.mentor_name if user and user.mentor_name else "Azalea"

def add_achievement(achievement_name, description=None):
    achievement = Achievement(name=achievement_name, description=description)
    db.session.add(achievement)
    db.session.commit()

def grant_achievement_to_user(user_id, achievement_name):
    achievement = Achievement.query.filter_by(name=achievement_name).first()
    if achievement:
        user_achievement = UserAchievement(user_id=user_id, achievement_id=achievement.id)
        db.session.add(user_achievement)
        db.session.commit()

def get_user_achievements(user_id):
    achievements = db.session.query(Achievement.name).join(UserAchievement).filter(UserAchievement.user_id == user_id).all()
    return [achievement.name for achievement in achievements]

# Profile
def get_complete_user_data(user_id):
    user = User.query.get(user_id)
    if not user:
        return None

    # Format joined_at with user timezone if available
    formatted_date = None
    if user.joined_at:
        try:
            
            # Default to UTC if timezone not set
            tz = pytz.timezone(user.timezone) if user.timezone else pytz.UTC
            # Convert the datetime to the user's timezone
            localized_date = user.joined_at.replace(tzinfo=pytz.UTC).astimezone(tz)
            # Format the date nicely
            formatted_date = localized_date.strftime("%B %d, %Y")
        except Exception:
            # Fallback if timezone processing fails
            formatted_date = user.joined_at.strftime("%Y-%m-%d %H:%M:%S UTC")

    user_data = {
        "email": user.email,
        "tier": user.tier,
        "user": user.profile,
        "tutor": user.ai_tutor_profile,
        "timezone": user.timezone,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "joined_at": formatted_date,
    }
    return user_data

def set_profile(user_id, profile_data):
    user = User.query.get(user_id)
    if user:
        user.profile = profile_data
        db.session.commit()

def get_profile(user_id):
    user = User.query.get(user_id)
    return user.profile if user else None

def get_user_info(user_id):
    user = User.query.get(user_id)
    return user.as_dict() if user else None

def set_tutor(user_id, tutor_data):
    user = User.query.get(user_id)
    if user:
        user.ai_tutor_profile = tutor_data
        db.session.commit()

def get_tutor(user_id):
    user = User.query.get(user_id)
    return user.ai_tutor_profile if user else None

def get_user_content(user_id):
    user = User.query.get(user_id)
    return user.current_content if user else None

def add_challenge(user_id, challenge_name, user_started=True):
    # Validate challenge_name: must be a non-empty string and within length limits.
    if not isinstance(challenge_name, str) or not challenge_name.strip():
        return False, "Challenge name must be a non-empty string."
    if len(challenge_name) > MAX_CHALLENGE_NAME_LENGTH:
        return False, f"Challenge name too long. Maximum allowed length is {MAX_CHALLENGE_NAME_LENGTH} characters."

    try:
        # Prepend default emoji if none is found
        if not extract_single_emoji(challenge_name):
            challenge_name = f"⛰️{challenge_name}"
        
        # Create the new challenge
        challenge = Challenge(user_id=user_id, challenge_name=challenge_name, completion_date=None)
        db.session.add(challenge)
        db.session.commit()

        # Add associated content message and AI message
        add_content_message(user_id, challenge_name, challenge_id=challenge.id)

        return True, challenge.id

    except SQLAlchemyError as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        db.session.rollback()
        return False, f"An unexpected error occurred: {str(e)}"

def is_challenge_complete(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    return challenge.completion_date is not None if challenge else False


def add_lesson(user_id, lesson_name, user_started=True):
    # Validate lesson_name: must be a non-empty string and within length limits.
    if not isinstance(lesson_name, str) or not lesson_name.strip():
        return False, "Lesson name must be a non-empty string."
    if len(lesson_name) > MAX_LESSON_NAME_LENGTH:
        return False, f"Lesson name too long. Maximum allowed length is {MAX_LESSON_NAME_LENGTH} characters."

    try:
        # Check for an existing lesson
        existing_lesson = Lesson.query.filter_by(user_id=user_id, lesson_name=lesson_name).first()
        if existing_lesson:
            return False, existing_lesson.id

        # Prepend a default emoji if none is found in the lesson name.
        if not extract_single_emoji(lesson_name):
            lesson_name = f"🤔{lesson_name}"

        # Create the new lesson
        lesson = Lesson(user_id=user_id, lesson_name=lesson_name, completion_date=None, system_role=None)
        db.session.add(lesson)
        db.session.commit()

        # Add associated content message.
        add_content_message(user_id, lesson_name, lesson_id=lesson.id)

        return True, lesson.id

    except SQLAlchemyError as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        db.session.rollback()
        return False, f"An unexpected error occurred: {str(e)}"

def is_lesson_complete(lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id).first()
    return lesson.completion_date is not None if lesson else False

def is_lesson_shared(lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id).first()
    return bool(lesson and lesson.shared)

def is_challenge_shared(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    return bool(challenge and challenge.shared)

def publicise_challenge(challenge_id, user_id, make_public):
    challenge = Challenge.query.get(challenge_id)
    if challenge and challenge.user_id == user_id:
        challenge.public = make_public
        db.session.commit()
        return True
    return False

def publicise_lesson(lesson_id, user_id, make_public):
    lesson = Lesson.query.get(lesson_id)
    if lesson and lesson.user_id == user_id:
        lesson.public = make_public
        db.session.commit()
        return True
    return False

def get_public_lessons():
    public_lessons = Lesson.query.filter_by(public=True, shared=True).limit(16).all()
    return [lesson.as_dict() for lesson in public_lessons]

def get_public_challenges():
    public_challenges = Challenge.query.filter_by(public=True, shared=True).limit(16).all()
    return [challenge.as_dict() for challenge in public_challenges]

def get_user_challenges(user_id):
    return Challenge.query.filter_by(user_id=user_id).all()

def get_challenge_name(challenge_id):
    return Challenge.query.filter_by(id=challenge_id).first().challenge_name
    
def get_user_lessons(user_id):
    return Lesson.query.filter_by(user_id=user_id).all()

def get_lesson_name(lesson_id):
    return Lesson.query.filter_by(id=lesson_id).first().lesson_name

def get_completed_challenges(user_id):
    completed_challenges = Challenge.query.filter_by(user_id=user_id).filter(Challenge.completion_date.isnot(None)).all()
    return [challenge.as_dict() for challenge in completed_challenges]

def get_active_challenges(user_id):
    active_challenges = Challenge.query.filter_by(user_id=user_id).filter(Challenge.completion_date.is_(None)).all()
    return [challenge.as_dict() for challenge in active_challenges]

def get_completed_lessons(user_id):
    completed_lessons = Lesson.query.filter_by(user_id=user_id).filter(Lesson.completion_date.isnot(None)).all()
    return [lesson.as_dict() for lesson in completed_lessons]

def get_active_lessons(user_id):
    active_lessons = Lesson.query.filter_by(user_id=user_id).filter(Lesson.completion_date.is_(None)).all()
    return [lesson.as_dict() for lesson in active_lessons]

def get_user_lesson_names(user_id):
    lessons = Lesson.query.filter_by(user_id=user_id).all()
    return [lesson.lesson_name for lesson in lessons]

def share_challenge(challenge_id, user_id):
        challenge = Challenge.query.get(challenge_id)
        if challenge and challenge.user_id == user_id:
            challenge.shared = True
            db.session.commit()
            return True
        return False

def share_lesson(lesson_id, user_id):
    lesson = Lesson.query.get(lesson_id)
    if lesson and lesson.user_id == user_id:
        lesson.shared = True
        db.session.commit()
        return True
    return False

def add_feedback(user_id, content, lesson_id=None, challenge_id=None, rating=None):
    new_feedback = Feedback(
        user_id=user_id,
        content=content,
        lesson_id=lesson_id,
        challenge_id=challenge_id,
        rating=rating
    )
    db.session.add(new_feedback)
    db.session.commit()

def get_all_feedback():
    feedback_list = Feedback.query.all()
    return [feedback.as_dict() for feedback in feedback_list]

def get_user_details():
    users = User.query.all()

    user_details_list = []
    for user in users:
        user_details = {
            "email": user.email,
            "tier": user.tier,
            "experience_points": user.experience_points,
            "num_chats": len(user.chats),
            "num_lessons": len(user.lessons),
            "num_libraries": len(user.libraries)
        }
        user_details_list.append(user_details)

    return user_details_list


### GRAPHS ###

def get_offered_lessons(user_id):
    actions = UserAction.query.filter_by(user_id=user_id).filter(UserAction.action.like('Start lesson:%')).all()
    offered_lessons = [action.action.split('Start lesson:')[1].strip() for action in actions]
    return offered_lessons

def get_offered_challenges(user_id):
    actions = UserAction.query.filter_by(user_id=user_id).filter(UserAction.action.like('Accept challenge:%')).all()
    offered_challenges = [action.action.split('Accept challenge:')[1].strip() for action in actions]
    return offered_challenges

def user_knowledge_net_info(user_id):
    user = User.query.get(user_id)
    if not user:
        return None

    user_data = {
        "profile": user.profile,
        "active_libraries": [{
            'id': library.library_id,
            'topic': library.library.library_topic
        } for library in sorted(
            [l for l in user.libraries if not l.is_complete], 
            key=lambda x: x.id, reverse=True)[:10]
        ],
        "completed_libraries": [{
            'id': library.library_id,
            'topic': library.library.library_topic
        } for library in sorted(
            [l for l in user.libraries if l.is_complete], 
            key=lambda x: x.id, reverse=True)[:20]
        ],
        "active_lessons": [{
            'id': lesson.id,
            'name': lesson.lesson_name
        } for lesson in sorted(
            [l for l in user.lessons if not l.completion_date], 
            key=lambda x: x.id, reverse=True)[:30]
        ],
        "completed_lessons": [{
            'id': lesson.id,
            'name': lesson.lesson_name
        } for lesson in sorted(
            [l for l in user.lessons if l.completion_date], 
            key=lambda x: x.id, reverse=True)[:100]
        ],
        "latest_action": user.current_content
    }

    # Add offered lessons and challenges
    user_data['offered_lessons'] = get_offered_lessons(user_id)

    return user_data

### CLEAR ###

def clear_user_challenges(user_id):
    Challenge.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def clear_user_lessons(user_id):
    # MUST CLEAR all actions first.
    Lesson.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def clear_user_actions(user_id, lesson_id=None):
    UserAction.query.filter_by(user_id=user_id, lesson_id=lesson_id).delete()
    db.session.commit()

def clear_all_user_actions(user_id):
    UserAction.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def clear_user_achievements(user_id):
    UserAchievement.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def clear_user_profile(user_id):
    user = User.query.get(user_id)
    if user:
        user.profile = None
        user.ai_tutor_profile = None
        user.current_lesson = None
        user.system_role = ''
        db.session.commit()

def clear_user_library_completions(user_id):
    LibraryRoomState.query.filter_by(user_id=user_id).delete()
    LibraryCompletion.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def reset_user_profile(user_id):
    clear_all_user_actions(user_id)
    clear_user_achievements(user_id)
    clear_user_challenges(user_id)
    clear_user_lessons(user_id)
    clear_user_profile(user_id)
    clear_user_library_completions(user_id)
