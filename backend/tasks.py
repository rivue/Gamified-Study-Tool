from __future__ import annotations
from app import supabase

from typing import Optional
from celery import states

from celery_app import celery
from database.models import db, Material
from vector_processing.file_handler import process_document_no_pinecone
from openai import OpenAI

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

        # - Download the file from Supabase by material.storage_path
        material_file = supabase.storage.from_("course-materials").download(material.storage_path)
        print("successfully downloaded the file")
        
        # - Extract text
        extracted_text = process_document_no_pinecone(material_file)
        print("successfully extracted text")

        # - Generate a detailed extracted summary with creative examples/metaphors/acronyms
        client = OpenAI()
        prompt = (
            "You are an expert study coach. Create an extracted summary of the following content.\n"
            "- Be detailed and well-structured with clear headings and bullet points.\n"
            "- Include creative examples, metaphors, and acronyms/mnemonics to aid memorization.\n"
            "- Keep the summary strictly grounded in the source; do not invent facts.\n"
            "- Where appropriate, include a few concise practice questions.\n\n"
            "SOURCE CONTENT START\n"
            f"{extracted_text}\n"
            "SOURCE CONTENT END"
        )
        # Prefer the Responses API if available; otherwise fall back to Chat Completions
        summary: str = ""
        try:
            # Fallback for older SDKs that don't support Responses API
            chat = getattr(client, "chat", None)
            if not chat or not hasattr(chat, "completions"):
                raise AttributeError("OpenAI client lacks both responses and chat.completions APIs")
            resp = chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1200,
            )
            # Extract first choice content
            choices = getattr(resp, "choices", []) or []
            if choices and getattr(choices[0], "message", None):
                content = getattr(choices[0].message, "content", "")
            else:
                # Some SDK versions return dict-like structures
                content = (choices[0]["message"]["content"] if choices else "")
            summary = (content or "").strip()
        except Exception:
            # Propagate to outer retry handler after ensuring summary is at least a string
            raise

        # - Update DB rows as needed
        material.summary = summary or "No summary generated."

        # Mark ready
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
