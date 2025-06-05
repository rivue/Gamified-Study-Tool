# routes/auth_routes.py
import re
from datetime import datetime
from flask import request, jsonify, url_for, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, current_user, login_user
import pymysql.err as pymysql_err
import os
import re
# from oauth2client import client, crypt

from database.models import db, User
from database.user_handler import confirm, generate_confirmation_token, get_user_tier, get_daily_request_count
from message_handler import initialize_messages
from email_provider.resend_api import send_email
from email_provider.email_templates import Registration, PasswordReset

# GOOGLE_CLIENT_ID = "529262341360-9sq10od3qkro19jaavhgachkpviugfv3.apps.googleusercontent.com"

def generate_token_and_send_verification_email(user):
        user.confirmation_token = generate_confirmation_token(user.id)
        user.confirm_sent_at = datetime.utcnow()
        db.session.commit()
        
        if os.getenv('FLASK_ENV') == 'production':
            frontend_url = "https://rivue.ai"
        else:
            frontend_url = "http://localhost:8080"

        confirmation_link = f"{frontend_url}/verify/{user.confirmation_token}"
        send_email(user.email, Registration, confirmation_link)

def generate_token_and_send_password_reset_email(user):
        user.password_reset_token = generate_confirmation_token(user.id)
        user.password_reset_sent_at = datetime.utcnow()
        db.session.commit()

        if os.getenv('FLASK_ENV') == 'production':
            frontend_url = "https://rivue.ai"
        else:
            frontend_url = "http://localhost:8080"

        reset_link = f"{frontend_url}/reset-password/{user.password_reset_token}"
        send_email(user.email, PasswordReset, reset_link)

def init_auth_routes(app):

    @app.route('/api/login', methods=['POST'])
    def login():
        try:
            email = request.form['email']
            password = request.form['password']
            timezone = request.form['timezone']
            user = User.query.filter_by(email=email).first()
            if not user:
                return jsonify({'status': 'fail', 'message': 'Account not found, signup to use our site!'}), 400
            
            if user and check_password_hash(user.password, password):
                # print(login_user(user, remember=True))
                # print(current_user.is_authenticated)
                if not user.confirmed:
                    return jsonify({'status': 'fail', 'message': 'Email not authenticated. Check your email inbox for a verification email. (it might also be in the spam folder!)'}), 400
                
                if timezone and timezone != user.timezone:
                    user.timezone = timezone
                    db.session.commit()

                login_result = login_user(user, remember=True)
                user.update_daily_streak()
                db.session.commit()
                
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'current_streak': user.streak_count,
                    'highest_streak': user.highest_streak
                }
                
                print(f"login resulf: {user_data}")
                return jsonify({'status': 'success', 'user': user_data})
            else:
                return jsonify({'status': 'fail', 'message': 'Incorrect Password'}), 400
        except Exception as e:
            print(f"{e}")
            return jsonify({'status': 'fail', 'message': 'An unexpected error occurred. Please try again later.'}), 500
        

    @app.route("/api/logout", methods=["GET"])
    @login_required
    def logout_route():
        logout_user()
        return jsonify({"status": "success"})


    # creates new user in database (signup) and sends email to verify account
    @app.route('/api/signup', methods=['POST'])
    def signup():
        try:
            email = request.form['new-email']
            username = request.form['username']
            first_name = request.form.get('first_name', '').strip() # Use .get and strip
            last_name = request.form.get('last_name', '').strip()   # Use .get and strip

            # Validation for first_name
            if first_name: # Only validate if provided
                if len(first_name) > 25:
                    return jsonify({'message': 'Field first_name cannot exceed 25 characters.'}), 400
                if not re.match(r"^[a-zA-Z-]+$", first_name):
                    return jsonify({'message': 'Field first_name can only contain letters and hyphens.'}), 400
            
            # Validation for last_name
            if last_name: # Only validate if provided
                if len(last_name) > 25:
                    return jsonify({'message': 'Field last_name cannot exceed 25 characters.'}), 400
                if not re.match(r"^[a-zA-Z-]+$", last_name):
                    return jsonify({'message': 'Field last_name can only contain letters and hyphens.'}), 400

            existing_user_by_email = User.query.filter_by(email=email).first()
            if existing_user_by_email:
                return jsonify({'message': 'An account with this email already exists.'}), 400

            existing_user_by_username = User.query.filter_by(username=username).first()
            if existing_user_by_username:
                return jsonify({'message': 'This username is already taken. Please choose another.'}), 400

            password = request.form['new-password']
            hashed_password = generate_password_hash(password)
            joined_at = datetime.utcnow()
            new_user = User(
                email=email,
                username=username,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                joined_at=joined_at
            )
            db.session.add(new_user)
            db.session.commit()

            generate_token_and_send_verification_email(new_user)

            return jsonify({})
        except Exception as e:
            return jsonify({'message': 'An unexpected error occurred. Please try again later.'}), 500

    # sends user an email to verify and confirm their email
    @app.route('/api/send-verify-link', methods=['POST'])
    def send_verify_link():
        try:
            data = request.get_json(silent=True) or {}
            email = data.get('email')
            
            if not email:
                return jsonify({'status': 'error', 'message': 'Email is required'}), 400
            
            user = User.query.filter_by(email=email).first()
            
            if not user:
                return jsonify({'status': 'error', 'message': 'User not found'}), 404

            if user.confirmed:
                return jsonify({'status': 'error', 'message': 'No need to send an email, you\'re already verified!'})

            generate_token_and_send_verification_email(user)
                
            return jsonify({'status': 'success', 'message': 'Password reset link sent successfully!'})
        
        except KeyError as e:
            app.logger.error(f"KeyError: {e}")
            return jsonify({'status': 'error', 'message': 'Invalid request data'}), 400
        except Exception as e:
            app.logger.error(f"Unexpected error: {e}")
            return jsonify({'status': 'error', 'message': 'An unexpected error occurred'}), 500
        
    # takes user's token from email and confirms their account
    @app.route('/api/confirm', methods=['POST'])
    def confirm_email():
        try:
            data = request.get_json(silent=True) or {}
            # Use the URL token or fall back to body token
            token = data.get('token')

            if not token:
                return jsonify({'status': 'error', 'message': 'No token provided'}), 400
            app.logger.info(f"token_to_use: {token}")

            user = User.query.filter_by(confirmation_token=token).first()
            if not user:
                return jsonify({'status': 'error', 'message': 'invalid_registration_token'}), 400

            app.logger.info(f"user: {user}, confirmed: {user.confirmed}")

            if user.confirmed:
                return jsonify({'status': 'success', 'message': 'Email already confirmed!'}), 200

            if confirm(user.id, token):
                app.logger.info("confirm successful")
                login_user(user)
                initialize_messages(user.id)
                user.confirmation_token = None
                user.confirm_sent_at = None
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Email confirmed successfully!'})

            return jsonify({'status': 'error', 'message': 'invalid_registration_token'}), 400
        except KeyError as e:
            app.logger.error(f"KeyError: {e}")
            return jsonify({'status': 'error', 'message': 'Invalid request data'}), 400
        except Exception as e:
            app.logger.error(f"KeyError: {e}")
            return jsonify({'status': 'error', 'message': 'something failed'}), 500

    # sends user an email to reset their password
    @app.route('/api/send-reset-link', methods=['POST'])
    def send_reset_link():
        try:
            data = request.get_json(silent=True) or {}
            email = data.get('email')
            
            if not email:
                return jsonify({'status': 'error', 'message': 'Email is required'}), 400
            
            user = User.query.filter_by(email=email).first()
            
            if not user:
                return jsonify({'status': 'error', 'message': 'User not found'}), 404
            
            if not user.confirmed:
                return jsonify({'status': 'error', 'message': 'User account is not confirmed'}), 400

            generate_token_and_send_password_reset_email(user)
                
            return jsonify({'status': 'success', 'message': 'Password reset link sent successfully!'}), 200
        
        except KeyError as e:
            app.logger.error(f"KeyError: {e}")
            return jsonify({'status': 'error', 'message': 'error occurred'}), 400
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'error occurred'}), 400


    # takes token from user to reset their password
    @app.route('/api/reset-password', methods=['POST'])
    def reset_password():
        try:
            data = request.get_json(silent=True) or {}
            token = data.get('token')
            new_password = data.get('new_password')

            if not token or not new_password:
                return jsonify({'status': 'error', 'message': 'Token and new password are required'}), 400

            user = User.query.filter_by(password_reset_token=token).first()

            if not user:
                return jsonify({'status': 'error', 'message': 'Invalid or expired token'}), 400

            user.password = generate_password_hash(new_password)
            user.password_reset_token = None
            user.password_reset_sent_at = None
            db.session.commit()

            return jsonify({'status': 'success', 'message': 'Password reset successfully!'}), 200

        except KeyError as e:
            app.logger.error(f"KeyError: {e}")
            return jsonify({'status': 'error', 'message': 'Something unexpected happened'}), 400
        except Exception as e:
            app.logger.error(f"Unexpected error: {e}")
            return jsonify({'status': 'error', 'message': 'An unexpected error occurred'}), 500
        
    @app.route('/api/check-auth', methods=['GET'])
    def check_auth():
        if current_user and current_user.is_authenticated and current_user.confirmed:
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

