import unittest
from datetime import datetime, timedelta, date
from unittest.mock import patch

from app import create_app
from database.models import db, User, Library, LibrarySection, LibraryUnit, LibraryMembership, LibraryRoomState
from werkzeug.security import generate_password_hash

class TestStreakRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user
        self.test_user = User(
            username='testuser',
            email='testuser@example.com',
            password=generate_password_hash('password'),
            confirmed=True,
            timezone='UTC'
        )
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login_test_user(self):
        return self.client.post('/api/login', data={
            'email': 'testuser@example.com',
            'password': 'password',
            'timezone': 'UTC'
        }, follow_redirects=True)

    # --- Tests for /api/login ---
    @patch('backend.database.models.datetime')
    def test_login_new_streak(self, mock_datetime):
        # Scenario: User logs in, streak was 0, last_streak_date was null -> streak becomes 1.
        mock_datetime.now.return_value = datetime(2023, 1, 1, 10, 0, 0) # Set current time

        self.assertIsNone(self.test_user.last_streak_date)
        self.assertEqual(self.test_user.streak_count, 0)

        response = self.login_test_user()
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['status'], 'success')
        self.assertEqual(json_data['user']['current_streak'], 1)
        self.assertEqual(json_data['user']['highest_streak'], 1)

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 1)
        self.assertEqual(user.highest_streak, 1)
        self.assertEqual(user.last_streak_date, date(2023, 1, 1))

    @patch('backend.database.models.datetime')
    def test_login_continued_streak(self, mock_datetime):
        # Scenario: User logs in, streak was X, last_streak_date was yesterday -> streak becomes X+1.
        self.test_user.streak_count = 3
        self.test_user.highest_streak = 3
        self.test_user.last_streak_date = date(2023, 1, 1) # Yesterday
        db.session.commit()

        mock_datetime.now.return_value = datetime(2023, 1, 2, 10, 0, 0) # Today

        response = self.login_test_user()
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['status'], 'success')
        self.assertEqual(json_data['user']['current_streak'], 4)
        self.assertEqual(json_data['user']['highest_streak'], 4)

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 4)
        self.assertEqual(user.highest_streak, 4)
        self.assertEqual(user.last_streak_date, date(2023, 1, 2))

    @patch('backend.database.models.datetime')
    def test_login_reset_streak(self, mock_datetime):
        # Scenario: User logs in, streak was X, last_streak_date was 2 days ago -> streak becomes 1.
        self.test_user.streak_count = 5
        self.test_user.highest_streak = 5
        self.test_user.last_streak_date = date(2023, 1, 1) # 2 days ago
        db.session.commit()

        mock_datetime.now.return_value = datetime(2023, 1, 3, 10, 0, 0) # Today

        response = self.login_test_user()
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['status'], 'success')
        self.assertEqual(json_data['user']['current_streak'], 1)
        self.assertEqual(json_data['user']['highest_streak'], 5) # Highest streak remains

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 1)
        self.assertEqual(user.highest_streak, 5)
        self.assertEqual(user.last_streak_date, date(2023, 1, 3))

    @patch('backend.database.models.datetime')
    def test_login_same_day_streak(self, mock_datetime):
        # Scenario: User logs in multiple times on the same day, streak should not increase.
        self.test_user.streak_count = 1
        self.test_user.highest_streak = 1
        self.test_user.last_streak_date = date(2023, 1, 1)
        db.session.commit()

        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0) # Same day, later time

        response = self.login_test_user() # First login on this day (already set by last_streak_date)
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['user']['current_streak'], 1)
        self.assertEqual(json_data['user']['highest_streak'], 1)

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 1) # Streak remains 1

        # Simulate another login on the same day
        mock_datetime.now.return_value = datetime(2023, 1, 1, 14, 0, 0)
        response = self.login_test_user()
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['user']['current_streak'], 1) # Still 1
        self.assertEqual(json_data['user']['highest_streak'], 1)

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 1) # Still 1
        self.assertEqual(user.last_streak_date, date(2023, 1, 1))


    # --- Tests for /api/user/streak ---
    @patch('backend.database.models.datetime')
    def test_get_user_streak_new(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 1, 1, 10, 0, 0)
        self.login_test_user() # Login to establish session

        response = self.client.get('/api/user/streak')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['current_streak'], 1) # Initial streak after login
        self.assertEqual(json_data['highest_streak'], 1)

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 1)
        self.assertEqual(user.last_streak_date, date(2023, 1, 1))

    @patch('backend.database.models.datetime')
    def test_get_user_streak_continued(self, mock_datetime):
        self.test_user.streak_count = 2
        self.test_user.highest_streak = 2
        self.test_user.last_streak_date = date(2023, 1, 1) # Yesterday
        db.session.commit()

        mock_datetime.now.return_value = datetime(2023, 1, 2, 10, 0, 0) # Today
        self.login_test_user() # Login to establish session

        response = self.client.get('/api/user/streak')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        # The login itself would have updated the streak.
        # The GET /api/user/streak call then calls update_daily_streak again,
        # but since it's the same day, it shouldn't increment further.
        self.assertEqual(json_data['current_streak'], 3) # 2 (initial) + 1 (from login)
        self.assertEqual(json_data['highest_streak'], 3)

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 3)
        self.assertEqual(user.last_streak_date, date(2023, 1, 2))

    @patch('backend.database.models.datetime')
    def test_get_user_streak_reset(self, mock_datetime):
        self.test_user.streak_count = 4
        self.test_user.highest_streak = 4
        self.test_user.last_streak_date = date(2023, 1, 1) # 2 days ago
        db.session.commit()

        mock_datetime.now.return_value = datetime(2023, 1, 3, 10, 0, 0) # Today
        self.login_test_user() # Login to establish session

        response = self.client.get('/api/user/streak')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['current_streak'], 1) # Reset by login, then GET confirms
        self.assertEqual(json_data['highest_streak'], 4) # Highest remains

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 1)
        self.assertEqual(user.last_streak_date, date(2023, 1, 3))

    # --- Tests for /api/library/end ---
    def _setup_library_data(self):
        # Create a library
        library = Library(owner_id=self.test_user.id, library_topic="Test Library", difficulty="Easy", language="English", language_difficulty="Easy", guide="Azalea", is_public=True)
        db.session.add(library)
        db.session.flush() # To get library.id

        # Create a unit
        unit = LibraryUnit(library_id=library.id, unit_name="Test Unit", position=0)
        db.session.add(unit)
        db.session.flush() # To get unit.id

        # Create a section
        section = LibrarySection(unit_id=unit.id, section_name="Test Section", position=0)
        db.session.add(section)
        db.session.flush() # To get section.id

        # Add user as member (implicitly done by creating room state by some handlers, but good to be explicit)
        membership = LibraryMembership(user_id=self.test_user.id, library_id=library.id)
        db.session.add(membership)

        # Create room state
        room_state = LibraryRoomState(user_id=self.test_user.id, library_id=library.id, section_id=section.id, num_lessons=3, lesson_state=1, room_name="Test Section")
        db.session.add(room_state)

        db.session.commit()
        return library.id, section.id

    @patch('backend.database.models.datetime')
    def test_library_end_new_streak(self, mock_datetime):
        library_id, section_id = self._setup_library_data()
        mock_datetime.now.return_value = datetime(2023, 1, 1, 10, 0, 0)
        self.login_test_user() # Login to establish session

        # Initial login sets streak to 1
        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 1)
        self.assertEqual(user.last_streak_date, date(2023, 1, 1))

        # Now, advance time to next day for the library/end call
        mock_datetime.now.return_value = datetime(2023, 1, 2, 10, 0, 0)

        response = self.client.post('/api/library/end', json={
            'libraryId': library_id,
            'sectionId': section_id
        })
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['status'], 'success')
        self.assertEqual(json_data['current_streak'], 2) # 1 (from login) + 1 (from library/end on new day)
        self.assertEqual(json_data['highest_streak'], 2)

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 2)
        self.assertEqual(user.last_streak_date, date(2023, 1, 2))

    @patch('backend.database.models.datetime')
    def test_library_end_continued_streak(self, mock_datetime):
        library_id, section_id = self._setup_library_data()
        self.test_user.streak_count = 2
        self.test_user.highest_streak = 2
        self.test_user.last_streak_date = date(2023, 1, 1) # Yesterday
        db.session.commit()

        mock_datetime.now.return_value = datetime(2023, 1, 2, 10, 0, 0) # Today
        self.login_test_user() # Login establishes session, updates streak to 3

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 3) # After login
        self.assertEqual(user.last_streak_date, date(2023, 1, 2))

        # If library/end is called on the SAME day as login, streak should not increase again
        response = self.client.post('/api/library/end', json={
            'libraryId': library_id,
            'sectionId': section_id
        })
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['current_streak'], 3) # Remains 3
        self.assertEqual(json_data['highest_streak'], 3)

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 3)
        self.assertEqual(user.last_streak_date, date(2023, 1, 2))

        # Now, advance time to next day for the library/end call
        mock_datetime.now.return_value = datetime(2023, 1, 3, 10, 0, 0)
        response = self.client.post('/api/library/end', json={
            'libraryId': library_id,
            'sectionId': section_id
        })
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['current_streak'], 4) # Increments
        self.assertEqual(json_data['highest_streak'], 4)

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 4)
        self.assertEqual(user.last_streak_date, date(2023, 1, 3))


    @patch('backend.database.models.datetime')
    def test_library_end_reset_streak(self, mock_datetime):
        library_id, section_id = self._setup_library_data()
        self.test_user.streak_count = 5
        self.test_user.highest_streak = 5
        self.test_user.last_streak_date = date(2023, 1, 1) # Date far in past
        db.session.commit()

        mock_datetime.now.return_value = datetime(2023, 1, 3, 10, 0, 0) # Today (2 days after last_streak_date)
        self.login_test_user() # Login resets streak to 1

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 1) # Reset by login
        self.assertEqual(user.highest_streak, 5)
        self.assertEqual(user.last_streak_date, date(2023, 1, 3))

        # If library/end is called on the SAME day as login, streak should not increase again
        response = self.client.post('/api/library/end', json={
            'libraryId': library_id,
            'sectionId': section_id
        })
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['current_streak'], 1) # Remains 1
        self.assertEqual(json_data['highest_streak'], 5)

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 1)
        self.assertEqual(user.last_streak_date, date(2023, 1, 3))

        # Now, advance time to next day for the library/end call
        mock_datetime.now.return_value = datetime(2023, 1, 4, 10, 0, 0)
        response = self.client.post('/api/library/end', json={
            'libraryId': library_id,
            'sectionId': section_id
        })
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['current_streak'], 2) # Increments from 1 to 2
        self.assertEqual(json_data['highest_streak'], 5)

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.streak_count, 2)
        self.assertEqual(user.last_streak_date, date(2023, 1, 4))

if __name__ == '__main__':
    unittest.main()
