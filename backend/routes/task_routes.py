from __future__ import annotations

from flask import jsonify, request


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
        if not isinstance(material_id, int):
            return jsonify({"error": "Bad request", "message": "material_id (int) is required"}), 400

        # Local import to avoid circular imports during app startup
        from tasks import process_material
        async_result = process_material.delay(material_id)
        return (
            jsonify({
                "status": "queued",
                "task_id": async_result.id,
                "material_id": material_id,
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
