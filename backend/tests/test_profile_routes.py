import pytest
from backend.database.models import User, db
from flask_login import login_user, logout_user

def test_update_user_profile_names_success(client, init_db, test_user):
    """Test successful update of first_name and last_name for a logged-in user."""
    # Log in the test user
    with client.application.test_request_context():
        login_user(test_user)

    response = client.post('/api/profile/user', json={
        'data': {
            'first_name': 'UpdatedFirst',
            'last_name': 'UpdatedLast'
        }
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['message'] == 'Profile updated successfully.'

    updated_user = User.query.get(test_user.id)
    assert updated_user.first_name == 'UpdatedFirst'
    assert updated_user.last_name == 'UpdatedLast'

    # Clean up login state
    with client.application.test_request_context():
        logout_user()

    # Ensure the original test_user's name is valid for other tests if they re-use it
    test_user.first_name = "Test" 
    test_user.last_name = "User"
    db.session.commit()

def test_update_user_profile_timezone_success(client, init_db, test_user):
    """Test successful update of timezone for a logged-in user."""
    with client.application.test_request_context():
        login_user(test_user)

    response = client.post('/api/profile/user', json={
        'data': {
            'timezone': 'America/New_York'
        }
    })
    assert response.status_code == 200
    updated_user = User.query.get(test_user.id)
    assert updated_user.timezone == 'America/New_York'
    
    with client.application.test_request_context():
        logout_user()

def test_update_user_profile_generic_profile_text_success(client, init_db, test_user):
    """Test successful update of the generic profile text blob."""
    with client.application.test_request_context():
        login_user(test_user)

    new_profile_text = 'This is my new general profile description.'
    response = client.post('/api/profile/user', json={
        'data': {
            'profile_text': new_profile_text 
        }
    })
    assert response.status_code == 200
    updated_user = User.query.get(test_user.id)
    assert updated_user.profile == new_profile_text # 'profile' is the db column for this
    
    with client.application.test_request_context():
        logout_user()


def test_update_user_profile_unauthenticated(client, init_db):
    """Test attempting to update profile when not logged in."""
    response = client.post('/api/profile/user', json={
        'data': {'first_name': 'Attempt'}
    })
    # Flask-Login's @login_required typically redirects to login_view or returns 401
    assert response.status_code == 401 
    assert response.json['error'] == 'User not authenticated'

def test_update_username_success(client, init_db, test_user):
    """Test successful username change for a logged-in user."""
    with client.application.test_request_context():
        login_user(test_user)

    new_username = 'new_unique_username'
    response = client.post('/api/profile/username', json={'new_username': new_username})
    
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['message'] == 'Username updated successfully.'

    updated_user = User.query.get(test_user.id)
    assert updated_user.username == new_username

    with client.application.test_request_context():
        logout_user()

def test_update_username_taken(client, init_db, test_user):
    """Test changing username to one that is already taken."""
    # Create another user whose username we will try to take
    other_user = User(username='otheruser', email='other@example.com', password='password')
    db.session.add(other_user)
    db.session.commit()

    with client.application.test_request_context():
        login_user(test_user)

    response = client.post('/api/profile/username', json={'new_username': 'otheruser'})
    
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'This username is already taken. Please choose another.'
    
    original_user = User.query.get(test_user.id)
    assert original_user.username == 'testuser' # Username should not have changed

    with client.application.test_request_context():
        logout_user()

def test_update_username_missing_username(client, init_db, test_user):
    """Test changing username with missing new_username in payload."""
    with client.application.test_request_context():
        login_user(test_user)

    response = client.post('/api/profile/username', json={}) # Empty JSON
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'New username is required.'
    
    with client.application.test_request_context():
        logout_user()

def test_update_username_unauthenticated(client, init_db):
    """Test attempting to change username when not logged in."""
    response = client.post('/api/profile/username', json={'new_username': 'unauth_attempt'})
    assert response.status_code == 401
    assert response.json['error'] == 'User not authenticated'

# --- New Validation Tests for /api/profile/user ---

def test_update_profile_name_too_long(client, init_db, test_user):
    """Test updating first_name or last_name to be longer than 25 characters."""
    with client.application.test_request_context():
        login_user(test_user)
    
    long_name = "a" * 26
    
    # Test first_name too long
    response_first = client.post('/api/profile/user', json={
        'data': {'first_name': long_name}
    })
    assert response_first.status_code == 400
    assert response_first.json['message'] == 'Field first_name cannot exceed 25 characters.'
    
    # Test last_name too long
    response_last = client.post('/api/profile/user', json={
        'data': {'last_name': long_name}
    })
    assert response_last.status_code == 400
    assert response_last.json['message'] == 'Field last_name cannot exceed 25 characters.'

    updated_user = User.query.get(test_user.id)
    assert updated_user.first_name == "Test" # Should not have changed
    assert updated_user.last_name == "User"   # Should not have changed

    with client.application.test_request_context():
        logout_user()

def test_update_profile_name_max_length(client, init_db, test_user):
    """Test updating first_name and last_name to max length (25 chars)."""
    with client.application.test_request_context():
        login_user(test_user)
        
    name_at_max = "b" * 25
    response = client.post('/api/profile/user', json={
        'data': {
            'first_name': name_at_max,
            'last_name': name_at_max
        }
    })
    assert response.status_code == 200
    updated_user = User.query.get(test_user.id)
    assert updated_user.first_name == name_at_max
    assert updated_user.last_name == name_at_max

    with client.application.test_request_context():
        logout_user()
    # Reset for other tests
    test_user.first_name = "Test"
    test_user.last_name = "User"
    db.session.commit()


def test_update_profile_name_invalid_chars(client, init_db, test_user):
    """Test updating first_name or last_name with invalid characters."""
    with client.application.test_request_context():
        login_user(test_user)

    invalid_name_digit = "Invalid1"
    invalid_name_symbol = "Invalid!"

    # Test first_name with digits
    response_first_digit = client.post('/api/profile/user', json={
        'data': {'first_name': invalid_name_digit}
    })
    assert response_first_digit.status_code == 400
    assert response_first_digit.json['message'] == 'Field first_name can only contain letters and hyphens.'
    
    # Test last_name with symbols
    response_last_symbol = client.post('/api/profile/user', json={
        'data': {'last_name': invalid_name_symbol}
    })
    assert response_last_symbol.status_code == 400
    assert response_last_symbol.json['message'] == 'Field last_name can only contain letters and hyphens.'
    
    updated_user = User.query.get(test_user.id)
    assert updated_user.first_name == "Test" # Should not have changed
    assert updated_user.last_name == "User"   # Should not have changed
    
    with client.application.test_request_context():
        logout_user()

def test_update_profile_name_with_hyphen(client, init_db, test_user):
    """Test updating first_name and last_name with hyphens."""
    with client.application.test_request_context():
        login_user(test_user)
        
    hyphenated_first = "Mary-Anne"
    hyphenated_last = "Smith-Jones"
    response = client.post('/api/profile/user', json={
        'data': {
            'first_name': hyphenated_first,
            'last_name': hyphenated_last
        }
    })
    assert response.status_code == 200
    updated_user = User.query.get(test_user.id)
    assert updated_user.first_name == hyphenated_first
    assert updated_user.last_name == hyphenated_last
    
    with client.application.test_request_context():
        logout_user()
    # Reset for other tests
    test_user.first_name = "Test"
    test_user.last_name = "User"
    db.session.commit()

def test_update_profile_name_to_empty(client, init_db, test_user):
    """Test updating first_name and last_name to empty strings."""
    with client.application.test_request_context():
        login_user(test_user)
        
    # Pre-set some names to ensure they are changed
    test_user.first_name = "InitialFirst"
    test_user.last_name = "InitialLast"
    db.session.commit()
        
    response = client.post('/api/profile/user', json={
        'data': {
            'first_name': "",
            'last_name': ""
        }
    })
    assert response.status_code == 200
    updated_user = User.query.get(test_user.id)
    # Empty strings are stored as None due to `field if field else None` in route
    assert updated_user.first_name is None 
    assert updated_user.last_name is None
    
    with client.application.test_request_context():
        logout_user()
    # Reset for other tests
    test_user.first_name = "Test"
    test_user.last_name = "User"
    db.session.commit()

