# routes/auth_routes.py
from datetime import datetime
from flask import request, jsonify, url_for, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, current_user, login_user
from sqlalchemy.exc import IntegrityError
import pymysql.err as pymysql_err
import os
# from oauth2client import client, crypt

from database.models import db, User
from database.user_handler import confirm, generate_confirmation_token, get_user_tier, get_daily_request_count
from message_handler import initialize_messages
from email_provider.resend_api import send_registration_email
from email_provider.email_templates import Registration

# GOOGLE_CLIENT_ID = "529262341360-9sq10od3qkro19jaavhgachkpviugfv3.apps.googleusercontent.com"

def init_auth_routes(app):

    @app.route('/api/login', methods=['POST'])
    def login():
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        print(user)
        print(os.getenv('SECRET_KEY'))
        print(os.getenv('FLASK_SECRET_KEY'))
        if user and check_password_hash(user.password, password):
            # print(login_user(user, remember=True))
            # print(current_user.is_authenticated)
            login_result = login_user(user, remember=True)
            print("Login result:", login_result)
            print("User authenticated:", current_user.is_authenticated)
            print("User ID in session:", session.get('_user_id'))
            print("Session:", dict(session))
            print(f"SECRET_KEY at login      : {app.config['SECRET_KEY']}")
            # print(f"FLAKS_SECRET_KEY at login: {app.config['FLASK_SECRET_KEY']}")

            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'fail'})

    @app.route("/api/logout", methods=["GET"])
    @login_required
    def logout_route():
        logout_user()
        return jsonify({"status": "success"})

    @app.route('/api/check-auth', methods=['GET'])
    def check_auth():
        if current_user.is_authenticated and current_user.is_confirmed:
            return jsonify({'loggedIn': True, 'userTier': get_user_tier(current_user.id), 'requestCount': get_daily_request_count(current_user.id), 'userId': current_user.id})
        else:
            return jsonify({'loggedIn': False, 'userTier': None})

    @app.route('/api/test-cookie', methods=['GET'])
    def test_cookie():
        # Try to set a cookie
        resp = make_response(jsonify({'message': 'Testing cookies'}))
        resp.set_cookie('test_cookie', 'test_value')
        print("Response cookies:", resp.headers.get('Set-Cookie'))
        return resp

    @app.route('/api/check-cookie', methods=['GET'])
    def check_cookie():
        # Check if cookie exists
        cookie_value = request.cookies.get('test_cookie')
        print("Request cookies:", request.cookies) # returns ImmutableMultiDict([])
        return jsonify({'cookie_value': cookie_value})

    @app.route('/api/test-session', methods=['GET'])
    def test_session():
        # Try to set session data
        session['test_key'] = 'test_value'
        print("Current session:", dict(session))
        return jsonify({'message': 'Session set'})

    @app.route('/api/check-session', methods=['GET'])
    def check_session():
        # Check if session data persists
        session_value = session.get('test_key')
        print("Current session:", dict(session)) # Current session: {}
        return jsonify({'session_value': session_value})

    @app.route('/api/debug-headers', methods=['GET'])
    def debug_headers():
        print("Request headers:", dict(request.headers))
        print("Cookies:", request.cookies)
        return jsonify({
            'headers': dict(request.headers),
            'cookies': dict(request.cookies),
            'session': dict(session)
        })

    @app.route('/api/signup', methods=['POST'])
    def signup():
        try:
            email = request.form['new-email']
            password = request.form['new-password']
            hashed_password = generate_password_hash(password)
            new_user = User(email=email, password=hashed_password, username=email)
            db.session.add(new_user)
            db.session.commit()
            new_user.confirmation_token = generate_confirmation_token(new_user.id)
            
            new_user.confirm_sent_at = datetime.utcnow()
            db.session.commit()
            
            if os.getenv('FLASK_ENV') == 'production':
                frontend_url = "https://rivue.ai"
            else:
                frontend_url = "http://localhost:8080"
            confirmation_link = f"{frontend_url}/verify/{new_user.confirmation_token}"
            send_registration_email(email, Registration, confirmation_link)
            return jsonify({'status': 'success'})
        except IntegrityError as e:
            if isinstance(e.orig, pymysql_err.IntegrityError) and 'Duplicate entry' in str(e.orig):
                return jsonify({'status': 'error', 'message': 'An account with this email already exists.'}), 400
            else:
                return jsonify({'status': 'error', 'message': 'An unexpected error occurred. Please try again later.'}), 500

    @app.route('/api/confirm', methods=['POST'])
    def confirm_email():
        print("hello")
        try:
            data = request.get_json(silent=True) or {}
            # Use the URL token or fall back to body token
            token = data.get('token')

            if not token:
                return jsonify({'status': 'error', 'message': 'No token provided'}), 400
            print(f"token_to_use: {token}")

            user = User.query.filter_by(confirmation_token=token).first()
            print(f"user: {user}, confirmed: {user.confirmed}")

            if user and confirm(user.id, token):
                print("confirm successfull")
                login_user(user)
                initialize_messages(user.id)
                
                return jsonify({'status': 'success', 'message': 'Email confirmed successfully!'})
            else:
                print("/api/confirm here")
                if user is not None and not user.confirmed:
                    print(f"user: {user}, confirmed: {user.confirmed}")
                    user.confirmation_token = generate_confirmation_token(user.id)
                    user.confirm_sent_at = datetime.utcnow()
                    db.session.commit()
                    
                    if os.getenv('FLASK_ENV') == 'production':
                        frontend_url = "https://rivue.ai"
                    else:
                        frontend_url = "http://localhost:8080"
                    confirmation_link = f"{frontend_url}/verify/{token}"
                    send_registration_email(user.email, Registration, confirmation_link)
                    return jsonify({'status': 'error', 'message': 'expired_registration_token'}), 500
                return jsonify({'status': 'error', 'message': 'invalid_registration_token'}), 500
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'something failed'}), 500
        
    @app.route('/api/resend-verification', methods=['POST'])
    def resend_verification():
        data = request.get_json()
        token = data.get('token')
        
        # Find user by the expired token
        user = User.query.filter_by(confirmation_token=token).first()
        
        if user:
            # Generate new token
            user.confirmation_token = generate_confirmation_token(user.id)
            user.confirm_sent_at = datetime.utcnow()
            db.session.commit()
            
            # Send a new email
            if os.getenv('FLASK_ENV') == 'production':
                frontend_url = "https://rivue.ai"
            else:
                frontend_url = "http://localhost:8080"
                confirmation_link = f"{frontend_url}/verify/{token}"
            send_registration_email(user.email, Registration, confirmation_link)
            return jsonify({'status': 'success', 'message': 'Verification email sent!'})
        else:
            return jsonify({'status': 'error', 'message': 'User not found'})
    
    # @app.route('/api/auth/google/callback', methods=['POST'])
    # def google_auth_callback():
    #     token = request.json.get('id_token')

    #     try:
    #         idinfo = client.verify_id_token(token, GOOGLE_CLIENT_ID)

    #         if idinfo['aud'] not in [GOOGLE_CLIENT_ID]:
    #             raise crypt.AppIdentityError("Unrecognized client.")

    #         if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
    #             raise crypt.AppIdentityError("Wrong issuer.")
            
    #         userid = idinfo['sub']
    #         email = idinfo.get('email')
    #         name = idinfo.get('name')
    #         # picture = idinfo.get('picture')
            
    #         if not idinfo.get('email_verified'):
    #             raise ValueError('Email not verified by Google.')

    #     except crypt.AppIdentityError:
    #         return jsonify({'message': 'Invalid token'}), 401

        # user = User.query.filter_by(email=email).first()
        # if not user:
        #     user = User(
        #         email=email,
        #         username=name,
        #         confirmed=True,
        #     )
        #     db.session.add(user)
        #     db.session.commit()
        #     login_user(user)
        #     initialize_messages(user.id)
        #     return jsonify({'status': "success", "message":"new_user"}), 200
        # else:
        #     user.username = name
        #     user.confirmed = True
        #     db.session.commit()
        #     login_user(user)
        #     return jsonify({'status': "success", "message":"existing_user"}), 200

