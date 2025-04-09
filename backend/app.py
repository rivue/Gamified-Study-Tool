#app.py

import os
import openai
import resend
from dotenv import load_dotenv
from datetime import timedelta
from flask import Flask, jsonify, make_response, send_from_directory, request
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
import logging
import sys

from database.models import db, User
from database.upgrade_db import run_upgrades
load_dotenv()
app = Flask(__name__, static_folder='../frontend/dist')
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['FLASK_ENV'] = os.getenv('FLASK_ENV', 'development')
openai.api_key = os.getenv("OPENAI_API_KEY")
resend.api_key = os.getenv("RESEND_API_KEY")

print(f"app level secret key: {app.secret_key}")

host = os.getenv('DB_HOST')
port = os.getenv('SUPABASE_PORT')
database = os.getenv('DATABASE')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

host_local = os.getenv('HOST_LOCAL')
port_local = os.getenv('PORT_LOCAL')
database_local = os.getenv('DATABASE_LOCAL')
user_local = os.getenv('USER_LOCAL')
password_local = os.getenv('PASSWORD_LOCAL')

print(f"flask_env: {app.config['FLASK_ENV']}")
if host and port and database and user and password and app.config["FLASK_ENV"] == "production":
    uri = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    
elif app.config["FLASK_ENV"] == "production":
    # throw an error because uri is not defined
    print("Database URI not defined")
    raise Exception("Database URI not defined")

else:
    uri = 'sqlite:///app.db'

# os.makedirs("instance", exist_ok=True)
# app.config['SQLALCHEMY_DATABASE_URI'] = uri
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') # TODO comment back in
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
app.config['FLASK_SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_size": 5,          # how many persistent connections
    "max_overflow": 10,      # extra connections on demand
    "pool_timeout": 30,      # how long to wait for a connection
    "pool_recycle": 1800     # recycle connections every 30 mins
}

app.config.update(
    # SESSION_COOKIE_SECURE=True,  # for HTTPS only
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    # REMEMBER_COOKIE_SECURE=True,
    REMEMBER_COOKIE_SECURE=False,
    REMEMBER_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_SAMESITE='Lax'
)

db.init_app(app)
migrate = Migrate(app, db)
if os.getenv('FLASK_ENV') == 'production':
    origins = "https://www.rivue.ai"
else:
    origins = "*"
CORS(app, origins=origins, supports_credentials=True)

# Global error handler for all unhandled exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled exception: {str(e)}")
    return jsonify({
        "error": "An internal server error occurred",
        "message": str(e)
    }), 500

# 404 error handler for resource not found
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({
        "error": "Resource not found",
    }), 404

# You can add more specific error handlers
@app.errorhandler(403)
def forbidden(e):
    return jsonify({"error": "Forbidden", "message": "You don't have permission to access this resource"}), 403

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request", "message": str(e)}), 400

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    session = db.session
    return session.get(User, int(user_id))
    # return User.query.get(int(user_id))
    # return session.get(User, int(user_id.id))

print("vvv database uri vvv:")
print(app.config['SQLALCHEMY_DATABASE_URI'])
print("^^^ database uri ^^^")
# Routes
from routes.auth_routes import init_auth_routes
from routes.profile_routes import init_profile_routes
from routes.utility_routes import init_utility_routes
from routes.chat_routes import init_chat_routes
from routes.graph_routes import init_graph_routes
from routes.feedback_routes import init_feedback_routes
from routes.admin_routes import init_admin_routes
from routes.library_routes import init_library_routes

init_auth_routes(app)
init_profile_routes(app)
init_utility_routes(app)
init_chat_routes(app)
init_graph_routes(app)
init_feedback_routes(app)
init_admin_routes(app)
init_library_routes(app)

with app.app_context():
    run_upgrades()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
    
@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
    
@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify({"error": "User not authenticated"}), 401)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)