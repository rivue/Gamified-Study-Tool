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

#### current edge function vvv
# begin
#   if TG_OP = 'INSERT' and new.bucket_id = 'course-materials' then
#       perform net.http_post(
#           url:='http://host.docker.internal:5000/api/tasks/process-material',
#           headers:='{"Content-Type": "application/json"}'::jsonb,
#           body:=jsonb_build_object(
#               'material_id', (new.metadata->>'material_id')::int
#           )
#       );
#     end if;
#     return new;
# end;
