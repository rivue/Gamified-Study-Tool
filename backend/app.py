#app.py

import os
import openai
import resend
from dotenv import load_dotenv
from datetime import timedelta
from flask import Flask, jsonify, make_response, send_from_directory, request, redirect
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

# Load .env as early as possible so imports can read env vars
load_dotenv()
from database.supabase import supabase
from database.models import db, User
from database.upgrade_db import run_upgrades
app = Flask(__name__, static_folder='../frontend/dist')
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['FLASK_ENV'] = os.getenv('FLASK_ENV', 'development')

CANONICAL_HOST = "www.rivue.ai"

if app.config['FLASK_ENV'] != 'migration':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    resend.api_key = os.getenv("RESEND_API_KEY")

print(f"app level secret key: {app.secret_key}")

session_pooler = True
# supabase direct connection = ipv6 (I think?), supabase pooler connection = ipv4
host = os.getenv('DB_HOST_SESSION_POOLER') if session_pooler else os.getenv('DB_HOST') 
user = os.getenv('DB_USER_SESSION_POOLER') if session_pooler else os.getenv('DB_USER')

password = os.getenv('DB_PASSWORD')
port = os.getenv('SUPABASE_PORT')
database = os.getenv('DATABASE')

print(f"flask_env: {app.config['FLASK_ENV']}")
if app.config["FLASK_ENV"] == "production":
    if not all([host, port, database, user, password]):
        print("Production database environment variables not fully set.")
        raise Exception("Production database environment variables not fully set.")
    uri = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=0)
else:
    # Default to local Supabase Postgres instance for development
    uri = 'postgresql+psycopg2://postgres:postgres@127.0.0.1:54322/postgres' 

# os.makedirs("instance", exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
print(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
app.config['FLASK_SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

if session_pooler:
    from sqlalchemy.pool import NullPool
    # When using an external pooler like pgbouncer, 
    # it's recommended to disable the application's own pooling.
    # NullPool doesn't support pool_size, max_overflow, pool_timeout
    engine_options = {
        "poolclass": NullPool,
        "pool_recycle": 1800  # This is still valid for NullPool
    }
else:
    # Use normal pooling when not using session pooler
    engine_options = {
        "pool_size": 5,
        "max_overflow": 10,
        "pool_timeout": 30,
        "pool_recycle": 1800
    }


app.config["SQLALCHEMY_ENGINE_OPTIONS"] = engine_options

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
    origins = ["https://www.rivue.ai", "https://rivue-s3xo7.ondigitalocean.app/"]
else:
    origins = "*"
CORS(app, origins=origins, supports_credentials=True)



# Global error handler for all unhandled exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled exception: {str(e)}")
    app.logger.error(f"Route: {request.path}")
    app.logger.error(f"Method: {request.method}")
    app.logger.error(f"Data: {request.get_json() if request.is_json else request.form.to_dict()}")
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
    
@app.after_request
def add_cross_origin_headers(response):
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'
    if app.config['FLASK_ENV'] == 'production':
        response.headers.setdefault('Strict-Transport-Security', 'max-age=15552000; includeSubDomains')
    return response


@app.before_request
def enforce_scheme_and_host():
    if app.config['FLASK_ENV'] != 'production':
        return None

    scheme = request.headers.get('X-Forwarded-Proto', request.scheme)
    host = request.headers.get('X-Forwarded-Host', request.host.split(':')[0])

    path = request.path
    query_string = request.query_string.decode('utf-8')
    suffix = f"{path}?{query_string}" if query_string else path

    target_host = CANONICAL_HOST if host != CANONICAL_HOST else host

    if scheme != 'https' or host != target_host:
        return redirect(f"https://{target_host}{suffix}", code=308)

class UserAlreadyMemberError(Exception):
    pass

class InvalidJoinCodeError(Exception):
    """Raised when a private library's join-code is wrong."""
    pass

class MaxUnitsReachedError(Exception):
    """Raised when a user tries to join a library that has reached its max units."""
    pass

class NotFoundError(Exception):
    """Raised when a library is not found."""
    pass

class PermissionError(Exception):
    """Raised when a user does not have permission to access a resource."""
    pass

# Error handlers for custom exceptions
@app.errorhandler(UserAlreadyMemberError)
def handle_user_already_member(e):
    return jsonify({"error": "Conflict", "message": str(e) or "User is already a member"}), 409

@app.errorhandler(InvalidJoinCodeError)
def handle_invalid_join_code(e):
    return jsonify({"error": "Bad request", "message": str(e) or "Invalid join code"}), 400

@app.errorhandler(MaxUnitsReachedError)
def handle_max_units_reached(e):
    return jsonify({"error": "Forbidden", "message": str(e) or "Maximum units reached"}), 403

@app.errorhandler(NotFoundError)
def handle_not_found(e):
    return jsonify({"error": "Not found", "message": str(e) or "Resource not found"}), 404

@app.errorhandler(PermissionError)
def handle_permission_error(e):
    return jsonify({"error": "Invalid Permissions", "message": str(e) or "You do not have permission to do that"}), 403

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
from routes.graph_routes import init_graph_routes
from routes.feedback_routes import init_feedback_routes
from routes.admin_routes import init_admin_routes
from routes.library_routes import init_library_routes
from routes.material_routes import init_material_routes
from routes.task_routes import init_task_routes

init_auth_routes(app)
init_profile_routes(app)
init_utility_routes(app)
init_graph_routes(app)
init_feedback_routes(app)
init_admin_routes(app)
init_library_routes(app)
init_material_routes(app)
init_task_routes(app)

if app.config['FLASK_ENV'] not in ['migration', 'production']:
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
    debug_mode = app.config['FLASK_ENV'] == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
