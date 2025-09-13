from flask import request, jsonify
from flask_login import login_required, current_user
from database.material_handlers import create_and_upload_material
from database.models import Material, Library

def init_material_routes(app):

    @app.route("/api/materials/course/<int:course_id>", methods=["GET"])
    @login_required
    def get_materials_for_course(course_id):
        """
        Fetches all materials for a given course ID.
        Optional query parameter 'state' can filter by specific states (comma-separated).
        """
        query = Material.query.filter_by(library_id=course_id)
        
        # Check for optional state filter COMMA SEPERATED VALUES - NOT A LIST OBJECT!!
        states_param = request.args.get('states')

        if states_param:
            print("alkjsdf;lkajsdf;lkajs")
            # Split comma-separated states and filter 
            states = [state.strip() for state in states_param.split(',')]
            query = query.filter(Material.status.in_(states))
        
        materials = query.order_by(Material.id.desc()).all()
        return jsonify([material.as_dict() for material in materials]), 200

    @app.route("/api/materials/upload", methods=["POST"])
    @login_required # Protect this endpoint
    def upload_material():
        """
        Handles the file upload from the frontend.
        Expects a multipart/form-data request with 'file' and 'course_id'.
        """
        
        # Check if the current user is the owner of the library (course)
      
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']
        course_id = request.form.get('course_id')

        if not file or file.filename == '':
            return jsonify({"error": "No selected file"}), 400
            
        if not course_id:
            return jsonify({"error": "Course ID is required"}), 400

        lib = Library.query.get(course_id)
        if lib.owner_id != current_user.id:
            return jsonify({"error": "You need to be the owner to do that!"}), 403
        
        try:
            new_material = create_and_upload_material(course_id=int(course_id), file=file)
            return jsonify(new_material.as_dict()), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            print(f"[ERROR] in upload_material: {e}") # It's good practice to log the error
            return jsonify({"error": "An unexpected error occurred on the server."}), 500
        
    @app.route("/api/materials/<int:material_id>/summary", methods=["GET"])
    @login_required
    def get_summary_for_material(material_id):
        """
        Fetches the summary for a given material ID.
        """
        material = Material.query.get(material_id)
        if not material:
            return jsonify({"error": "Material not found"}), 404
        
        return jsonify({
            "material_id": material.id,
            "summary": material.summary
        }), 200