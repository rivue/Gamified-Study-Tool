Short answer: keep one Celery task, but split the work into small, pure helper functions and add selective retries. Move to a task chain only if you need independent retry policies, progress UI, or horizontal scaling per stage.

Why
- Your pipeline is strictly sequential (download → extract → summarize → persist). A single orchestrator task is simpler and avoids passing large intermediates between tasks.
- However, autoretry_for=(Exception,) will re-run everything (including the OpenAI call) on any error. That’s costly and noisy. Different steps have different retry semantics.

Recommended refactor (single task, pure helpers + selective retry)
- Extract helpers for each step. Keep the Celery decorator only on the orchestrator.
- Add progress updates (self.update_state) so the UI can reflect stage.
- Retry only transient errors per step; do not retry 4xx/NotFound; add an idempotency key for the OpenAI call to avoid duplicate charges on retries.
- Avoid passing big blobs via Celery; keep intermediates in memory or store and pass references.

```python
# ...existing code...
import hashlib
import io
import logging
from requests import HTTPError, Timeout  # adjust to the libs you actually use

log = logging.getLogger(__name__)

def _download_bytes(storage_path: str) -> bytes:
    return supabase.storage.from_("course-materials").download(storage_path)

def _extract_text_from_bytes(blob: bytes) -> str:
    # Ensure process_document_no_pinecone can handle file-like; wrap if needed
    file_like = io.BytesIO(blob)
    return process_document_no_pinecone(file_like)

def _generate_summary(client: OpenAI, text: str, material_id: int) -> str:
    # Idempotency to avoid duplicate charges on retry for same input
    key = hashlib.sha256(text.encode("utf-8")).hexdigest()
    resp = client.responses.create(
        model="gpt-4o-mini",
        input=(
            "You are an expert study coach. Create an extracted summary of the following content.\n"
            "- Be detailed and well-structured with clear headings and bullet points.\n"
            "- Include creative examples, metaphors, and acronyms/mnemonics to aid memorization.\n"
            "- Keep the summary strictly grounded in the source; do not invent facts.\n"
            "- Where appropriate, include a few concise practice questions.\n\n"
            "SOURCE CONTENT START\n"
            f"{text}\n"
            "SOURCE CONTENT END"
        ),
        temperature=0.3,
        max_output_tokens=1200,
        extra_headers={"Idempotency-Key": f"material:{material_id}:{key}"},
    )
    return (getattr(resp, "output_text", None) or "").strip() or "No summary generated."

@celery.task(
    bind=True,
    name="tasks.process_material",
    autoretry_for=(Timeout,),  # only auto-retry transient network timeouts
    retry_backoff=True,
    retry_jitter=True,
    max_retries=5,
)
def process_material(self, material_id: int) -> dict:
    material: Optional[Material] = db.session.get(Material, material_id)
    if not material:
        self.update_state(state=states.FAILURE, meta={"error": "material_not_found", "material_id": material_id})
        return {"status": "error", "error": "material_not_found", "material_id": material_id}

    try:
        material.status = "processing"
        db.session.add(material)
        db.session.commit()

        self.update_state(state="PROGRESS", meta={"stage": "download"})
        blob = _download_bytes(material.storage_path)

        self.update_state(state="PROGRESS", meta={"stage": "extract"})
        extracted_text = _extract_text_from_bytes(blob)

        self.update_state(state="PROGRESS", meta={"stage": "summarize"})
        client = OpenAI()
        try:
            summary = _generate_summary(client, extracted_text, material_id)
        except HTTPError as e:
            # Do not retry on 4xx from the model; surface error
            if 400 <= getattr(e, "response", {}).status_code < 500:
                raise
            # Retry other HTTP errors
            raise self.retry(exc=e)

        material.summary = summary
        material.status = "ready"
        db.session.add(material)
        db.session.commit()
        return {"status": "ok", "material_id": material_id}

    except Timeout as exc:
        db.session.rollback()
        raise self.retry(exc=exc)

    except Exception as exc:
        db.session.rollback()
        try:
            material.status = "error"
            db.session.add(material)
            db.session.commit()
        except Exception:
            db.session.rollback()
        raise
# ...existing code...
```

When to split into multiple Celery tasks (chain)
- You need per-stage retry/backoff limits and timeouts (e.g., long OCR vs short API call).
- You want visible progress and resumability between stages.
- You plan to scale stages independently or parallelize across many materials.

Sketch (avoid passing large strings in results; pass references instead):
```python
# python
from celery import chain

@celery.task
def t_download(material_id): ...
@celery.task
def t_extract(file_ref): ...
@celery.task
def t_summarize(text_ref): ...
@celery.task
def t_persist(material_id, summary_ref): ...

def kickoff(material_id: int):
    return chain(
        t_download.s(material_id),
        t_extract.s(),
        t_summarize.s(),
        t_persist.s(material_id),
    ).apply_async()
```

Gotchas
- OpenAI calls: protect with idempotency and avoid blanket retries.
- Don’t pass big blobs through Celery result backend; store in Supabase or DB and pass keys.
- Prefer logging over print in workers.
- Consider soft/hard time limits per stage if documents can be large.

If you share expected document sizes and SLAs, I can suggest concrete timeouts and retry classes per step.