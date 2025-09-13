from flask import request, jsonify
from flask_login import login_required
from database.models import MockTest, db
from tasks import process_mock_test


def init_mock_test_routes(app):

    @app.route("/api/mock-tests/course/<int:course_id>", methods=["GET"])
    @login_required
    def get_mock_tests(course_id):
        tests = MockTest.query.filter_by(library_id=course_id).order_by(MockTest.id.desc()).all()
        return jsonify([t.as_dict() for t in tests]), 200

    @app.route("/api/mock-tests/generate", methods=["POST"])
    @login_required
    def generate_mock_test():
        data = request.get_json(silent=True) or {}
        course_id = data.get("course_id")
        material_ids = data.get("material_ids", [])
        name = data.get("name", "Mock Test")

        if not course_id or not material_ids:
            return jsonify({"error": "course_id and material_ids required"}), 400

        mock_test = MockTest(
            library_id=course_id,
            name=name,
            material_ids=material_ids,
            status="pending",
        )
        db.session.add(mock_test)
        db.session.commit()

        async_result = process_mock_test.delay(mock_test.id)
        return jsonify({**mock_test.as_dict(), "task_id": async_result.id}), 202
