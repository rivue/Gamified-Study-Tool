import pytest
from backend.database.models import User, db

def test_successful_signup(client, init_db, mock_send_email):
    """Test successful user signup."""
    response = client.post('/api/signup', data={
        'new-email': 'newuser@example.com',
        'username': 'newusername',
        'first_name': 'New',
        'last_name': 'User',
        'new-password': 'newpassword'
    })
    assert response.status_code == 200
    # Assuming signup returns an empty JSON on success or a specific message
    # assert response.json == {} or response.json.get("message") == "Expected success message"

    user = User.query.filter_by(email='newuser@example.com').first()
    assert user is not None
    assert user.username == 'newusername'
    assert user.first_name == 'New'
    assert user.last_name == 'User'
    assert user.confirmed is False # Assuming confirmation is still required
    assert user.confirmation_token is not None # Check that a token was generated
    mock_send_email.assert_called_once() # Verify email was "sent"

def test_signup_duplicate_email(client, init_db, test_user, mock_send_email):
    """Test signup with a duplicate email."""
    response = client.post('/api/signup', data={
        'new-email': test_user.email, # Using existing user's email
        'username': 'anotherusername',
        'first_name': 'Another',
        'last_name': 'User',
        'new-password': 'password123'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'An account with this email already exists.'
    mock_send_email.assert_not_called()

def test_signup_duplicate_username(client, init_db, test_user, mock_send_email):
    """Test signup with a duplicate username."""
    response = client.post('/api/signup', data={
        'new-email': 'unique_email@example.com',
        'username': test_user.username, # Using existing user's username
        'first_name': 'Unique',
        'last_name': 'Emailer',
        'new-password': 'password123'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'This username is already taken. Please choose another.'
    mock_send_email.assert_not_called()

def test_signup_missing_email(client, init_db, mock_send_email):
    """Test signup with missing email."""
    response = client.post('/api/signup', data={
        # 'new-email': 'missing@example.com', # Email is missing
        'username': 'someusername',
        'first_name': 'Some',
        'last_name': 'Name',
        'new-password': 'password123'
    })
    # This will likely result in a 400 Bad Request due to Werkzeug/Flask form handling
    # or a KeyError if the route code directly accesses request.form['new-email']
    # without checking. The exact error might depend on Flask's behavior with missing form fields.
    assert response.status_code == 400 # Or another appropriate error code for missing field
    # Add assertion for specific error message if available and consistent
    # e.g. assert "Email is required" in response.json['message']
    # For now, we check that it's not a success and no email is sent.
    mock_send_email.assert_not_called()

def test_signup_missing_username(client, init_db, mock_send_email):
    """Test signup with missing username."""
    response = client.post('/api/signup', data={
        'new-email': 'validemail@example.com',
        # 'username': 'missinguser', # Username is missing
        'first_name': 'Valid',
        'last_name': 'Email',
        'new-password': 'password123'
    })
    assert response.status_code == 400
    mock_send_email.assert_not_called()

def test_signup_missing_password(client, init_db, mock_send_email):
    """Test signup with missing password."""
    response = client.post('/api/signup', data={
        'new-email': 'validemail2@example.com',
        'username': 'validusername2',
        'first_name': 'Valid',
        'last_name': 'User2',
        # 'new-password': 'missingpassword' # Password is missing
    })
    assert response.status_code == 400
    mock_send_email.assert_not_called()

# Optional: Test with empty first_name and last_name as they are nullable
def test_signup_optional_names(client, init_db, mock_send_email):
    """Test successful signup with optional first_name and last_name empty."""
    response = client.post('/api/signup', data={
        'new-email': 'optionalnames@example.com',
        'username': 'optionalnamesuser',
        'first_name': '', # Empty first name
        'last_name': '',  # Empty last name
        'new-password': 'securepassword'
    })
    assert response.status_code == 200
    user = User.query.filter_by(email='optionalnames@example.com').first()
    assert user is not None
    assert user.username == 'optionalnamesuser'
    assert user.first_name == '' 
    assert user.last_name == ''
    mock_send_email.assert_called_once()

# --- New Validation Tests for /api/signup ---

def test_signup_name_too_long(client, init_db, mock_send_email):
    """Test signup with first_name or last_name longer than 25 characters."""
    long_name = "a" * 26
    
    # Test first_name too long
    response_first = client.post('/api/signup', data={
        'new-email': 'longfirstname@example.com',
        'username': 'longfirstnameuser',
        'first_name': long_name,
        'last_name': 'ValidLast',
        'new-password': 'password123'
    })
    assert response_first.status_code == 400
    assert response_first.json['message'] == 'Field first_name cannot exceed 25 characters.'
    mock_send_email.assert_not_called()
    
    # Test last_name too long
    mock_send_email.reset_mock() # Reset mock for the next call
    response_last = client.post('/api/signup', data={
        'new-email': 'longlastname@example.com',
        'username': 'longlastnameuser',
        'first_name': 'ValidFirst',
        'last_name': long_name,
        'new-password': 'password123'
    })
    assert response_last.status_code == 400
    assert response_last.json['message'] == 'Field last_name cannot exceed 25 characters.'
    mock_send_email.assert_not_called()

def test_signup_name_max_length(client, init_db, mock_send_email):
    """Test signup with first_name and last_name at max length (25 chars)."""
    name_at_max = "a" * 25
    response = client.post('/api/signup', data={
        'new-email': 'maxlengthname@example.com',
        'username': 'maxlengthnameuser',
        'first_name': name_at_max,
        'last_name': name_at_max,
        'new-password': 'password123'
    })
    assert response.status_code == 200
    user = User.query.filter_by(email='maxlengthname@example.com').first()
    assert user is not None
    assert user.first_name == name_at_max
    assert user.last_name == name_at_max
    mock_send_email.assert_called_once()

def test_signup_name_invalid_chars(client, init_db, mock_send_email):
    """Test signup with first_name or last_name containing invalid characters."""
    invalid_name_digit = "Invalid1"
    invalid_name_symbol = "Invalid!"

    # Test first_name with digits
    response_first_digit = client.post('/api/signup', data={
        'new-email': 'invalidfirstdigit@example.com',
        'username': 'invalidfirstdigituser',
        'first_name': invalid_name_digit,
        'last_name': 'ValidLast',
        'new-password': 'password123'
    })
    assert response_first_digit.status_code == 400
    assert response_first_digit.json['message'] == 'Field first_name can only contain letters and hyphens.'
    mock_send_email.assert_not_called()
    
    mock_send_email.reset_mock()
    # Test last_name with symbols
    response_last_symbol = client.post('/api/signup', data={
        'new-email': 'invalidlastsymbol@example.com',
        'username': 'invalidlastsymboluser',
        'first_name': 'ValidFirst',
        'last_name': invalid_name_symbol,
        'new-password': 'password123'
    })
    assert response_last_symbol.status_code == 400
    assert response_last_symbol.json['message'] == 'Field last_name can only contain letters and hyphens.'
    mock_send_email.assert_not_called()

def test_signup_name_with_hyphen(client, init_db, mock_send_email):
    """Test signup with first_name and last_name containing hyphens."""
    hyphenated_name = "Mary-Anne"
    response = client.post('/api/signup', data={
        'new-email': 'hyphenname@example.com',
        'username': 'hyphennameuser',
        'first_name': hyphenated_name,
        'last_name': 'Smith-Jones',
        'new-password': 'password123'
    })
    assert response.status_code == 200
    user = User.query.filter_by(email='hyphenname@example.com').first()
    assert user is not None
    assert user.first_name == hyphenated_name
    assert user.last_name == 'Smith-Jones'
    mock_send_email.assert_called_once()
