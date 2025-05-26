from backend.database.models import User, db

def test_user_model_attributes(init_db):
    """Test that a User object can be created with first_name and last_name."""
    user = User(
        username='modeltestuser',
        email='modeltest@example.com',
        password='securepassword',
        first_name='FirstName',
        last_name='LastName'
    )
    db.session.add(user)
    db.session.commit()

    retrieved_user = User.query.filter_by(username='modeltestuser').first()
    assert retrieved_user is not None
    assert retrieved_user.first_name == 'FirstName'
    assert retrieved_user.last_name == 'LastName'
    assert retrieved_user.email == 'modeltest@example.com'
    assert retrieved_user.username == 'modeltestuser'

def test_user_model_nullable_names(init_db):
    """Test that first_name and last_name can be null."""
    user = User(
        username='modeltestuser_nonames',
        email='modeltest_nonames@example.com',
        password='securepassword',
        first_name=None,
        last_name=None
    )
    db.session.add(user)
    db.session.commit()

    retrieved_user = User.query.filter_by(username='modeltestuser_nonames').first()
    assert retrieved_user is not None
    assert retrieved_user.first_name is None
    assert retrieved_user.last_name is None

def test_user_model_default_fields(init_db, app):
    """Test default fields of the User model like timezone and joined_at."""
    # Note: `timezone` and `joined_at` have server_default values set in the model
    # which are handled by the database. SQLAlchemy ORM objects won't have these
    # populated by Python until they are flushed or refreshed from the DB.
    # The migration `7f5e10f1f1d0` also added these.
    
    user = User(
        username='modeltestuser_defaults',
        email='modeltest_defaults@example.com',
        password='securepassword'
        # first_name, last_name, timezone, joined_at are not set here
    )
    db.session.add(user)
    db.session.commit() # This will flush and allow server defaults to be set

    retrieved_user = User.query.filter_by(username='modeltestuser_defaults').first()
    assert retrieved_user is not None
    assert retrieved_user.timezone is not None # Check it has a value (e.g., 'UTC')
    assert retrieved_user.joined_at is not None # Check it has a value
    
    # Check specific default values if they are consistent and known
    # For server_default='UTC' for timezone:
    assert retrieved_user.timezone == 'UTC'
    
    # For streak_count, highest_streak (also added in 7f5e10f1f1d0)
    assert retrieved_user.streak_count == 0
    assert retrieved_user.highest_streak == 0
    assert retrieved_user.confirmed == False # Default from User model
    
    # Check that the new fields are present after migration
    assert hasattr(retrieved_user, 'first_name')
    assert hasattr(retrieved_user, 'last_name')
    assert retrieved_user.first_name is None # Should be nullable
    assert retrieved_user.last_name is None # Should be nullable
