from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import JSON, update
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo
import traceback
import logging
import secrets, string
import hashlib
import random
import time

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    timezone = db.Column(db.String(50), default='UTC', nullable=False, server_default='UTC')
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, server_default=db.func.now())

    mentor_name = db.Column(db.String(100), default='Azalea') # TODO: not using
    system_role = db.Column(db.String(100), default='') # TODO: not using
    profile = db.Column(db.Text, nullable=True) # TODO: not using
    ai_tutor_profile = db.Column(db.Text, nullable=True) # TODO: not using
    current_content = db.Column(db.String(500), nullable=True) # TODO: not using
    
    experience_points = db.Column(db.Integer, default=0)
    achievements = db.relationship('UserAchievement', backref='user', cascade="all, delete-orphan")

    actions = db.relationship('UserAction', backref='user', cascade="all, delete-orphan") # TODO: not using

    chats = db.relationship('ChatHistory', backref='user', cascade="all, delete-orphan") # TODO: not using
    lessons = db.relationship('Lesson', backref='user', cascade="all, delete-orphan") # TODO: not using

    tier = db.Column(db.String(50), default='free')  # 'free', 'paid', 'pro'
    daily_request_count = db.Column(db.Integer, default=0) # TODO: I am not using
    last_request_time = db.Column(db.DateTime, default=datetime.utcnow) # TODO: I am not using
    streak_count = db.Column(db.Integer, default=0, nullable=False)
    last_streak_date = db.Column(db.Date, nullable=True)
    highest_streak = db.Column(db.Integer, default=0, nullable=False)

    violation_count = db.Column(db.Integer, default=0) # TODO: I am not using (yet?)

    confirmed = db.Column(db.Boolean, default=False)
    confirmation_token = db.Column(db.String(100), nullable=True)
    confirm_sent_at = db.Column(db.DateTime, nullable=True)

    password_reset_token = db.Column(db.String(100), nullable=True)
    password_reset_sent_at = db.Column(db.DateTime, nullable=True)
    
    owned_libraries = db.relationship('Library', foreign_keys='Library.owner_id', # Specify the foreign key column in Library
        back_populates='owner', lazy='dynamic', cascade="all, delete-orphan") # If user deleted, delete their libraries too

    # 2. Library Memberships (Many-to-Many via Association Object)
    # 'library_memberships' will be a list of LibraryMembership objects
    library_memberships = db.relationship('LibraryMembership', back_populates='user', cascade="all, delete-orphan", # If user deleted, remove their memberships
        lazy='dynamic')

    def as_dict(self):

        user_data = {
            "profile": self.profile,
        }
        
        user_data["owned_libraries"] = [lib.library_topic for lib in self.owned_libraries]
        user_data["joined_libraries_topics"] = [lib.library_topic for lib in self.joined_libraries] # Use the convenience property
        
        return user_data
    
    @property
    def joined_libraries(self):
        """Returns a list of Library objects the user is a member of."""
        # This queries through the LibraryMembership association objects
        return [membership.library for membership in self.library_memberships]
    
    def update_daily_streak(self): 
        tz = ZoneInfo(self.timezone or 'UTC')
        today_local = datetime.now(tz).date()
        yesterday_local = today_local - timedelta(days=1)
            
        if self.last_streak_date is None:
            self.streak_count = 1

        else:
            last = self.last_streak_date
            # last request was today, no change
            if last == today_local:
                return self.streak_count
            # last request was yesterday, increment streak
            if last == yesterday_local:
                self.streak_count += 1
            # broke streak, reset
            else:
                self.streak_count = 1

        self.last_streak_date = today_local
        
        if self.streak_count > self.highest_streak:
            self.highest_streak = self.streak_count
        
        return self.streak_count
    
class IPTracking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hashed_ip = db.Column(db.String(64), unique=True, nullable=False)
    library_generated = db.Column(db.Boolean, default=False, nullable=False)
    library_generated_time = db.Column(db.DateTime, nullable=True)
    room_generated = db.Column(db.Boolean, default=False, nullable=False)
    room_generated_time = db.Column(db.DateTime, nullable=True)

    def __init__(self, ip):
        self.hashed_ip = hashlib.sha256(ip.encode()).hexdigest()

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    completion_date = db.Column(db.DateTime, default=datetime.utcnow)

class UserAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    system_role = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=True)
    message_type = db.Column(db.String(50), default='message')
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)  # 1-5 scale
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    status = db.Column(db.String(50), default='new')  # e.g., new, reviewed, resolved

    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=True)

    user = db.relationship('User', backref=db.backref('feedback', lazy=True))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_name = db.Column(db.String(100), nullable=False)
    completion_date = db.Column(db.DateTime, nullable=True)
    shared = db.Column(db.Boolean, default=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_name = db.Column(db.String(200), nullable=False)
    completion_date = db.Column(db.DateTime, nullable=True)
    system_role = db.Column(db.String(100), default='')
    shared = db.Column(db.Boolean, default=False)
    public = db.Column(db.Boolean, default=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

###lib###
class Library(db.Model):
    DEFAULT_IMAGE_URL = "https://csb10032002fc59a9f5.blob.core.windows.net/library-images/background.png"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', foreign_keys=[owner_id],
        back_populates='owned_libraries')
    
    memberships = db.relationship('LibraryMembership', back_populates='library', cascade="all, delete-orphan", # If library deleted, remove memberships
        lazy='dynamic')

    library_topic = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    guide = db.Column(db.String(50), nullable=False, default=lambda: random.choice(["Azalea", "Irona", "Bubbles", "Sterling"]))
    language = db.Column(db.String(50), nullable=False)
    language_difficulty = db.Column(db.String(50), nullable=False)
    context = db.Column(db.String(200), nullable=True)
    is_public = db.Column(db.Boolean, default=True, nullable=False)
    join_code = db.Column(db.String(8), unique=True, nullable=True, default=lambda: Library._generate_unique_code())

    clicks = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)

    room_names = db.Column(MutableList.as_mutable(JSON), nullable=False)
    image_url = db.Column(db.String(200), nullable=False, default=DEFAULT_IMAGE_URL)
    
    units = db.relationship('LibraryUnit', backref='library', cascade="all, delete-orphan", lazy=True,
                            order_by="LibraryUnit.position")

    factoids = db.relationship('LibraryFactoid', backref='library', cascade="all, delete-orphan")
    
    @classmethod
    def _generate_unique_code(cls):
        code_length = 8
        alphabet = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(secrets.choice(alphabet) for _ in range(code_length))
            # quick in‑memory test; the UNIQUE constraint is the final guard
            if not db.session.query(cls.id).filter_by(join_code=code).first():
                return code
            time.sleep(0.01)

    def set_privacy(self, new_status: bool):
        """Sets the library's privacy and manages the join code."""
        if new_status == self.is_public:
            return # No change needed

        self.is_public = new_status
        if not new_status:
            # Make private: Generate a code if it doesn't have one
            if not self.join_code:

                self.join_code = self._generate_unique_code()
        else:
            # Make public: Remove the code
            self.join_code = None
        return self.join_code

    def attach_unit(self, unit: 'LibraryUnit', position=None):
        """Attach a unit to this library at the specified position
        
        Args:
            unit: LibraryUnit to attach
            position: Position to insert (0-indexed). If None, append to the end.
        
        Returns:
            The attached unit
        """

        try:
        
            if not isinstance(unit, LibraryUnit):
                raise ValueError("unit must be an instance of LibraryUnit")
            

            with db.session.no_autoflush:
            
                # Get current maximum position if we need to append
                if position is None:
                    
                    max_position = db.session.query(db.func.max(LibraryUnit.position))\
                                    .filter(LibraryUnit.library_id == self.id).scalar() or -1
                    
                    unit.position = max_position + 1
                    
                    # Make sure the unit is added to the session if it's not already
                    db.session.add(unit)
                        
                else:

                    # Instead of a single update statement
                    positions = db.session.query(LibraryUnit.id, LibraryUnit.position)\
                        .filter(LibraryUnit.library_id == self.id, LibraryUnit.position >= position)\
                        .order_by(LibraryUnit.position.desc()).all()
                        
                    for id, current_position in positions:
                        db.session.query(LibraryUnit).filter(LibraryUnit.id == id)\
                            .update({LibraryUnit.position: current_position + 1})
                    
                    unit.position = position

                    # Make sure the unit is added to the session if it's not already
                    db.session.add(unit)
                        
            unit.library_id = self.id # attach after position is set

            return unit
        
        except SQLAlchemyError as e:
            print(f"error: {e}")
            db.session.rollback() # keep the DB clean
            raise

class LibraryUnit(db.Model):
    __tablename__ = "library_unit"
    id = db.Column(db.Integer, primary_key=True)
    library_id = db.Column(db.Integer, db.ForeignKey('library.id'), nullable=False)
    unit_name = db.Column(db.String(200), nullable=False)
        
    position = db.Column(db.Integer, nullable=False, index=True) 

    sections = db.relationship('LibrarySection', backref='unit', cascade="all, delete-orphan", lazy=True)

    __table_args__ = (
        db.UniqueConstraint('library_id', 'position',
                            name='uq_library_unit_position'),
    )

    def add_section(self, section_name):
        """Add a new section to this unit"""
        section = LibrarySection(unit_id=self.id, section_name=section_name)
        db.session.add(section)
        return section

class LibrarySection(db.Model):
    __tablename__ = "library_section"
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('library_unit.id'), nullable=False)
    section_name = db.Column(db.String(200), nullable=False)
    
    # Link factoids to a section
    factoids = db.relationship('LibraryFactoid', backref='section', cascade="all, delete-orphan", lazy=True)

class LibraryRoomState(db.Model): # maps users to states of rooms they are in
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    library_id = db.Column(db.Integer, db.ForeignKey('library.id'), nullable=False)

    room_name = db.Column(db.String(200), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('library_section.id'), nullable=True)

    num_lessons = db.Column(db.Integer, nullable=False)
    lesson_state = db.Column(db.Integer, nullable=False)  # 1-state 1, 2-state 2, 3-state 3, 4-state 4, etc...
    
    # __table_args__ = (
    #     db.UniqueConstraint('user_id', 'factoid_id', name='uq_user_factoid'),
    # )

    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "library_id": self.library_id,
            "room_name": self.room_name,
            "num_lessons": self.num_lessons,
            "lesson_state": self.lesson_state,
        }
    
class LibraryFavorites(db.Model): # map of users to libraries they have favorited
    __tablename__ = "library_favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    library_id = db.Column(db.Integer, db.ForeignKey('library.id'), nullable=False)
    is_favorited = db.Column(db.Boolean, default=False, nullable=False)

    __table_args__ = (
      db.UniqueConstraint("user_id", "library_id", name="uq_user_library_fav"),
    )

# Add this model definition with your other models
class LibraryMembership(db.Model):
    __tablename__ = 'library_membership' # Explicit table name is good practice

    # Composite primary key ensures a user can only be a member of a library once
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    library_id = db.Column(db.Integer, db.ForeignKey('library.id'), primary_key=True)

    # extra information (just joined_at for now)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())

    user = db.relationship('User', back_populates='library_memberships')
    library = db.relationship('Library', back_populates='memberships')

    def __repr__(self):
        return f'<LibraryMembership User {self.user_id} in Library {self.library_id}>'

class LibraryCompletion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    library_id = db.Column(db.Integer, db.ForeignKey('library.id'), nullable=False)
    completion_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    completed_rooms = db.Column(db.Text, nullable=True)

    is_complete = db.Column(db.Boolean, default=False)
    
    library = db.relationship('Library', backref=db.backref('completions', lazy=True))

class LibraryFactoid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    library_id = db.Column(db.Integer, db.ForeignKey('library.id'), nullable=True)
    room_name = db.Column(db.String(200), nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey('library_section.id'), nullable=True)
    lesson_name = db.Column(db.String(200), nullable=False)
    factoid_content = db.Column(db.Text, nullable=False)

    questions = db.relationship('LibraryQuestion', backref='factoid')

class LibraryQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    factoid_id = db.Column(db.Integer, db.ForeignKey('library_factoid.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    correct_choice = db.Column(db.JSON, nullable=False)
    question_type = db.Column(db.String(50), nullable=False, default="multiple_choice")

    choices = db.relationship('LibraryQuestionChoice', backref='question', lazy='dynamic')

class LibraryQuestionChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('library_question.id'), nullable=False)
    choice_text = db.Column(db.String(400), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)