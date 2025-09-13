from __future__ import annotations

from flask import jsonify, request
from flask_login import login_required
from database.models import Test, Library, db


def init_task_routes(app):
    @app.post("/api/tasks/process-material")
    def enqueue_process_material():
        """Webhook-compatible endpoint to queue material processing.

        Body JSON:
        {
          "material_id": 123
        }
        """
        data = request.get_json(silent=True) or {}
        material_id = data.get("material_id")
        storage_path = data.get("storage_path")
        print("storage path: ", storage_path)

        # Accept either an integer material_id or a storage_path that maps to a Material row
        resolved_material_id = None

        # Try to coerce material_id if provided as string
        if material_id is not None and not isinstance(material_id, int):
            try:
                material_id = int(material_id)
            except Exception:
                material_id = None

        if isinstance(material_id, int):
            resolved_material_id = material_id
        elif isinstance(storage_path, str) and storage_path:
            # Resolve by storage_path
            from database.models import db, Material  # local import avoids circulars
            row = db.session.query(Material.id).filter_by(storage_path=storage_path).first()
            if row:
                resolved_material_id = row[0]
            else:
                return jsonify({
                    "error": "Not found",
                    "message": "No material with provided storage_path",
                    "storage_path": storage_path,
                }), 404
        else:
            return jsonify({
                "error": "Bad request",
                "message": "Provide material_id (int) or storage_path (string)",
                "received": data,
            }), 400

        # Local import to avoid circular imports during app startup
        from tasks import process_material
        async_result = process_material.delay(resolved_material_id)
        return (
            jsonify({
                "status": "queued",
                "task_id": async_result.id,
                "material_id": resolved_material_id,
                "via": "material_id" if material_id is not None else "storage_path",
            }),
            202,
        )

    @app.get("/api/tasks/status/<task_id>")
    def get_task_status(task_id: str):
        """Return Celery task status and optional result/metadata."""
        # Local import to avoid circular import at module level
        from celery_app import celery
        res = celery.AsyncResult(task_id)
        payload = {
            "task_id": task_id,
            "state": res.state,
        }
        # Only include result/meta if available and JSON-serializable
        if res.state in ("SUCCESS", "FAILURE", "REVOKED") and res.result is not None:
            try:
                # Celery stores exceptions for FAILURE; convert to string
                payload["result"] = (
                    str(res.result) if isinstance(res.result, BaseException) else res.result
                )
            except Exception:
                payload["result"] = None
        return jsonify(payload), 200
    
    @app.route("/api/tests/course/<int:course_id>", methods=["GET"])
    @login_required
    def get_tests(course_id):
        tests = Test.query.filter_by(library_id=course_id).order_by(Test.id.desc()).all()
        return jsonify([t.as_dict() for t in tests]), 200

    @app.route("/api/tests/generate", methods=["POST"])
    @login_required
    def generate_test():
        data = request.get_json(silent=True) or {}
        course_id = data.get("course_id")
        material_ids = data.get("material_ids", [])
        name = data.get("name", "Test")

        if not course_id or not material_ids:
            return jsonify({"error": "course_id and material_ids required"}), 400

        if course_id != Library.query.get(course_id).owner_id:
            return jsonify({"error": "You are not the course owner!"}), 400

        test = Test(
            library_id=course_id,
            name=name,
            material_ids=material_ids,
            status="pending",
        )
        db.session.add(test)
        db.session.commit()
        from tasks import process_test
        async_result = process_test.delay(test.id)
        return jsonify({**test.as_dict(), "task_id": async_result.id}), 202