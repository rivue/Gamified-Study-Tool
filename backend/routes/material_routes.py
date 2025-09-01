from flask import request, jsonify
from flask_login import login_required
from database.material_handlers import create_and_upload_material

def init_material_routes(app):

    @app.route("/api/upload", methods=["POST"])
    @login_required # Protect this endpoint
    def upload_material():
        """
        Handles the file upload from the frontend.
        Expects a multipart/form-data request with 'file' and 'course_id'.
        """
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']
        course_id = request.form.get('course_id')

        if not file or file.filename == '':
            return jsonify({"error": "No selected file"}), 400
            
        if not course_id:
            return jsonify({"error": "Course ID is required"}), 400

        try:
            new_material = create_and_upload_material(course_id=int(course_id), file=file)
            return jsonify(new_material.as_dict()), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            print(f"[ERROR] in upload_material: {e}") # It's good practice to log the error
            return jsonify({"error": "An unexpected error occurred on the server."}), 500