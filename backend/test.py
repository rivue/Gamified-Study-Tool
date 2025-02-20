# import secrets
# print(secrets.token_hex(32))
# db.session.commit()

# put below code in between these two lines (or their equivalent) in app.py
# migrate = Migrate(app, db)
# CORS(app, origins="*", supports_credentials=True)
app = Flask(__name__, static_folder='../frontend/dist')

# before running this code, install libraries, set up SECRET_KEY and FLASK_SECRET_KEY,
# and run flask db upgrade or flask db migrate idk
# also try running this code in app.py
with app.app_context():
    db.create_all()