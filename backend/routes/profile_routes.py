# routes/profile_routes.py

import re
from flask import request, jsonify
from flask_login import login_required, current_user

from database.models import db, User # db is already imported here
import database.db_handlers as dbh
from stats import get_total_user_exp, get_streak
from message_handler import update_system_role, initialize_messages

def init_profile_routes(app):

    @app.route('/api/user/streak', methods=['GET'])
    @login_required
    def get_user_streak():
        try:
            current_user.update_daily_streak(True)
            db.session.commit()
            print("Current user streak count:", current_user.streak_count)
            print("Highest user streak count:", current_user.highest_streak)
            return jsonify({'current_streak': current_user.streak_count, 'highest_streak': current_user.highest_streak})
        except Exception as e:
            # It's good practice to log the exception e
            app.logger.error(f"Error in /api/user/streak: {e}")
            return jsonify({'error': 'Failed to retrieve streak data'}), 500

    @app.route("/api/profile", methods=["GET"])
    @login_required
    def get_profile_route():
        profile_data = dbh.get_complete_user_data(current_user.id)
        return jsonify(status="success", profile=profile_data)

    @app.route("/api/profile/user", methods=["POST"])
    @login_required
    def update_user_profile():
        data = request.json.get("data", {})
        
        # Validate and update first_name
        if 'first_name' in data:
            first_name = data.get('first_name', '').strip()
            if first_name: # Only validate if provided and not just whitespace
                if len(first_name) > 25:
                    return jsonify({'message': 'Field first_name cannot exceed 25 characters.'}), 400
                if not re.match(r"^[a-zA-Z-]+$", first_name):
                    return jsonify({'message': 'Field first_name can only contain letters and hyphens.'}), 400
            current_user.first_name = first_name if first_name else None # Store as None if empty after strip
        
        # Validate and update last_name
        if 'last_name' in data:
            last_name = data.get('last_name', '').strip()
            if last_name: # Only validate if provided and not just whitespace
                if len(last_name) > 25:
                    return jsonify({'message': 'Field last_name cannot exceed 25 characters.'}), 400
                if not re.match(r"^[a-zA-Z-]+$", last_name):
                    return jsonify({'message': 'Field last_name can only contain letters and hyphens.'}), 400
            current_user.last_name = last_name if last_name else None # Store as None if empty after strip
        
        # Update timezone if provided
        if 'timezone' in data:
            current_user.timezone = data.get('timezone')

        # For other profile data, use the existing dbh.set_profile
        # We'll pass all data to it, it will update the 'profile' text column
        # If first_name/last_name are also in the 'profile' json, they'd be there too.
        # Or, we can choose to exclude them from what's passed to set_profile if desired.
        # For now, let's assume 'profile' is for other, more free-form profile text.
        # To avoid overwriting specific fields if they are also in the generic 'profile' blob
        # from the client, it's better to handle them separately.
        
        # Let's assume 'profile_text' is the key for the generic profile blob in 'data'
        if 'profile_text' in data:
             dbh.set_profile(current_user.id, data.get('profile_text'))

        db.session.commit()
        return jsonify(status="success", message="Profile updated successfully.")

    @app.route("/api/profile/username", methods=["POST"])
    @login_required
    def update_username():
        data = request.json
        new_username = data.get('new_username')

        if not new_username:
            return jsonify({'status': 'error', 'message': 'New username is required.'}), 400

        # Check if the new username is already taken by another user
        existing_user = User.query.filter(User.username == new_username, User.id != current_user.id).first()
        if existing_user:
            return jsonify({'status': 'error', 'message': 'This username is already taken. Please choose another.'}), 400

        current_user.username = new_username
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Username updated successfully.'})

    @app.route("/api/profile/tutor", methods=["POST"])
    @login_required
    def update_tutor_profile():
        new_data = request.json.get("data")
        dbh.set_tutor(current_user.id, new_data)
        return jsonify(status="success")

    @app.route("/api/plan", methods=["GET"])
    @login_required
    def get_user_plan():
        tier = get_user_tier(current_user.id)
        return jsonify(status="success", tier=tier)

    @app.route("/api/plan", methods=["POST"])
    @login_required
    def set_user_plan():
        data = request.json
        tierName = data.get('tier')
        if not tierName:
            return jsonify(status="error", message=""), 400

        set_user_tier(current_user.id, tierName)
        return jsonify(status="success")
    
    # @app.route("/api/mentor", methods=["GET"])
    # @login_required
    # def get_user_mentor():
    #     print("test")
    #     print(current_user.is_authenticated)
    #     name = dbh.get_mentor_name(current_user.id)
    #     return jsonify(status="success", selectedMentorId=name)

    # @app.route("/api/mentor", methods=["POST"])
    # @login_required
    # def set_user_mentor():
    #     data = request.json
    #     name = data.get('mentorId')
    #     print(name)
    #     if not name:
    #         return jsonify(status="error", message=""), 400

    #     dbh.set_mentor_name(current_user.id, name)
    #     update_system_role(current_user.id, dbh.get_system_role(current_user.id))
    #     isInitial = len(dbh.get_api_messages(current_user.id))
    #     if isInitial == 2:
    #         initialize_messages(current_user.id)
    #     return jsonify(status="success")