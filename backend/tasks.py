from __future__ import annotations

from typing import Optional
from celery import states

from celery_app import celery
from database.models import db, Material


@celery.task(
    bind=True,
    name="tasks.process_material",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=5,
)
def process_material(self, material_id: int) -> dict:
    """Example background task that processes a Material.

    This demonstrates the pattern described in BACKGROUND_PROCESSING_STRATEGY.md:
    queue the job quickly and execute the heavy work in a Celery worker.
    """
    print("processing material")
    material: Optional[Material] = db.session.get(Material, material_id)
    if not material:
        # Mark task as failure explicitly with a clear message
        self.update_state(state=states.FAILURE, meta={"error": "material_not_found", "material_id": material_id})
        return {"status": "error", "error": "material_not_found", "material_id": material_id}

    try:
        # Mark as processing
        material.status = "processing"
        db.session.add(material)
        db.session.commit()

        # TODO: Place heavy logic here
        # - Download the file from Supabase by material.storage_path
        # - Extract text, generate embeddings/summary
        # - Update DB rows as needed

        # For now, record a stub summary and mark ready
        material.summary = "Processed asynchrounously" #material.summary or "Processed asynchronously by worker."
        material.status = "ready"
        db.session.add(material)
        db.session.commit()

        return {"status": "ok", "material_id": material_id}
    except Exception as exc:  # noqa: BLE001 (simple top-level safety)
        db.session.rollback()
        # Persist failure state on the record for observability
        if material:
            try:
                material.status = "error"
                db.session.add(material)
                db.session.commit()
            except Exception:
                db.session.rollback()
        # Let Celery handle retry/backoff; include context in meta
        raise self.retry(exc=exc)

