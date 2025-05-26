import pytest
import os
from backend.app import app as flask_app # Assuming your Flask app instance is named 'app' in backend/app.py
from backend.database.models import db, User
from flask_migrate import upgrade as flask_db_upgrade
from werkzeug.security import generate_password_hash

TEST_DATABASE_URI = 'sqlite:///:memory:'

@pytest.fixture(scope='session')
def app():
    """Session-wide test Flask application."""
    # --- App configuration for testing ---
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI,
        "WTF_CSRF_ENABLED": False,  # Disable CSRF for forms if you have them
        "LOGIN_DISABLED": False, # Ensure login is enabled for auth tests
        "SERVER_NAME": "localhost.localdomain", # Required for url_for to work without a request context
        "FLASK_ENV": "testing" # Set a distinct env for testing
    })

    # --- Environment variables needed by the app, if any, set them here ---
    os.environ['FLASK_SECRET_KEY'] = 'test_secret_key'
    # Critical: Ensure external service calls are mocked or disabled in testing environment
    # These were handled in app.py and retrieval.py using FLASK_ENV=migration
    # For testing, we might need a similar approach or ensure FLASK_ENV=testing handles it.
    # For now, the previous changes for 'migration' env should prevent issues if FLASK_ENV is not 'production'.
    # If app.py specifically checks for 'testing' to disable external calls, that's even better.
    os.environ['OPENAI_API_KEY'] = 'dummy_test_key'
    os.environ['PINECONE_API_KEY'] = 'dummy_test_key'
    os.environ['RESEND_API_KEY'] = 'dummy_test_key'


    with flask_app.app_context():
        db.create_all() # Create all tables first
        # Apply all migrations to ensure schema is up-to-date
        # The 'migrations' folder must be configured for Alembic to find it.
        # This assumes Flask-Migrate is initialized with the app.
        try:
            # Temporarily set FLASK_ENV to migration to use the migration-safe app init
            original_flask_env = os.environ.get('FLASK_ENV')
            os.environ['FLASK_ENV'] = 'migration'
            flask_app.config['FLASK_ENV'] = 'migration' # Also update app.config

            flask_db_upgrade(directory="backend/migrations")

            # Revert FLASK_ENV after migrations
            if original_flask_env:
                os.environ['FLASK_ENV'] = original_flask_env
                flask_app.config['FLASK_ENV'] = original_flask_env
            else:
                del os.environ['FLASK_ENV']
                flask_app.config['FLASK_ENV'] = 'development' # Or your default
            
            # Set back to testing after migration
            flask_app.config['FLASK_ENV'] = 'testing'


        except Exception as e:
            print(f"Error during migration upgrade: {e}")
            # Depending on the error, you might want to fail the tests here
            # For "no such table: alembic_version", it means init was needed.
            # This setup assumes migrations directory is already init'd with `flask db init`
            # and `flask db migrate` has been run at least once to create initial scripts.
            # The error "Target database is not up to date" should be resolved by stamp head or upgrade.
            # The error "no such table: user_lesson_progress" from previous steps indicates
            # an issue with the migration history itself or an empty DB.
            # `db.create_all()` followed by `flask_db_upgrade()` should handle most cases for a fresh test DB.


    yield flask_app

    # --- Teardown ---
    with flask_app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture()
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture()
def init_db(app):
    """Fixture to ensure the database is clean and initialized for each test function."""
    with app.app_context():
        db.drop_all() # Ensure tables are dropped first
        db.create_all() # Create tables based on models
        # Then apply migrations to get the schema to the latest version, including new columns
        try:
            original_flask_env = os.environ.get('FLASK_ENV')
            os.environ['FLASK_ENV'] = 'migration'
            flask_app.config['FLASK_ENV'] = 'migration'

            flask_db_upgrade(directory="backend/migrations")
            
            if original_flask_env:
                os.environ['FLASK_ENV'] = original_flask_env
                flask_app.config['FLASK_ENV'] = original_flask_env
            else:
                del os.environ['FLASK_ENV']
                flask_app.config['FLASK_ENV'] = 'development'
            
            flask_app.config['FLASK_ENV'] = 'testing'

        except Exception as e:
            print(f"Error during init_db migration upgrade: {e}")
            # This is problematic if it fails, tests might run on incorrect schema
    return db


@pytest.fixture()
def test_user(init_db):
    """Creates a test user in the database."""
    user = User(
        username='testuser',
        email='test@example.com',
        password=generate_password_hash('password'),
        first_name='Test',
        last_name='User',
        confirmed=True # Assume user is confirmed for most tests unless specific to confirmation
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def mock_send_email(mocker):
    """Mocks the send_email function."""
    return mocker.patch('backend.routes.auth_routes.send_email', return_value=None)
