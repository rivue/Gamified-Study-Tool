from __future__ import annotations
from app import supabase

from typing import Optional
import json
import re
from celery import states

from celery_app import celery
from database.models import db, Material, Test
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

        # - Generate a JSON quiz based strictly on the extracted text
        quiz_prompt = (
            "Create a concise quiz strictly based on the source content.\n"
            "Return ONLY valid minified JSON with this schema: \n"
            "{\n  \"questions\": [\n    {\n      \"type\": \"Multiple Choice\"|\"True/False\"|\"Short Answer\",\n      \"question\": string,\n      \"options\": array<string> (omit for True/False and Short Answer),\n      \"correct\": string,\n      \"explanation\": string\n    }\n  ]\n}\n"
            "Guidelines:\n"
            "- 6-8 questions total with a mix of types.\n"
            "- Options should be clear and non-ambiguous.\n"
            "- Keep answers grounded in the source; do not invent facts.\n\n"
            "SOURCE CONTENT START\n"
            f"{extracted_text}\n"
            "SOURCE CONTENT END"
        )
        quiz_json = {"questions": []}
        print("after quiz_json")
        try:
            chat = getattr(client, "chat", None)
            if not chat or not hasattr(chat, "completions"):
                raise AttributeError("OpenAI client lacks chat.completions API")
            print("after chat")
            resp = chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": quiz_prompt}],
                temperature=0.2,
                max_tokens=1200,
            )
            print("before choices")
            choices = getattr(resp, "choices", []) or []
            if choices and getattr(choices[0], "message", None):
                content = getattr(choices[0].message, "content", "")
            else:
                content = (choices[0]["message"]["content"] if choices else "")
            print("before text")
            text = (content or "").strip()
            # Extract JSON if wrapped in code fences
            fence_match = re.search(r"```(?:json)?\n(.*?)\n```", text, re.DOTALL | re.IGNORECASE)
            json_str = fence_match.group(1).strip() if fence_match else text
            print("after jsonstr")
            parsed = json.loads(json_str)
            # normalize to {"questions": [...]} shape
            if isinstance(parsed, list):
                quiz_json = {"questions": parsed}
            elif isinstance(parsed, dict) and "questions" in parsed:
                quiz_json = {"questions": parsed.get("questions", [])}
            else:
                # fallback if unexpected structure
                quiz_json = {"questions": []}
            print("after else chain")
        except Exception:
            # If quiz generation fails, continue without blocking summary
            quiz_json = {"questions": []}

        material.quiz = quiz_json

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


@celery.task(
    bind=True,
    name="tasks.process_test",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=5,
)
def process_test(self, test_id: int) -> dict:
    """Generate a test from multiple materials."""
    test: Optional[Test] = db.session.get(Test, test_id)
    if not test:
        self.update_state(state=states.FAILURE, meta={"error": "test_not_found", "test_id": test_id})
        return {"status": "error", "error": "test_not_found", "test_id": test_id}
    try:
        test.status = "processing"
        db.session.add(test)
        db.session.commit()

        combined_text = ""
        for mid in test.material_ids:
            material = db.session.get(Material, mid)
            if not material:
                continue
            material_file = supabase.storage.from_("course-materials").download(material.storage_path)
            combined_text += process_document_no_pinecone(material_file) + "\n"

        client = OpenAI()
        prompt = (
            "Create a comprehensive test based strictly on the source content.\n"
            "Return ONLY valid minified JSON with this schema: \n"
            "{\n  \"questions\": [\n    {\n      \"type\": \"Multiple Choice\"|\"True/False\"|\"Short Answer\",\n      \"question\": string,\n      \"options\": array<string> (omit for True/False and Short Answer),\n      \"correct\": string,\n      \"explanation\": string\n    }\n  ]\n}\n"
            "Guidelines:\n"
            "- 20-30 questions total with a mix of types.\n"
            "- Options should be clear and non-ambiguous.\n"
            "- Keep answers grounded in the source; do not invent facts.\n\n"
            "SOURCE CONTENT START\n"
            f"{combined_text}\n"
            "SOURCE CONTENT END"
        )

        quiz_json = {"questions": []}
        try:
            chat = getattr(client, "chat", None)
            if not chat or not hasattr(chat, "completions"):
                raise AttributeError("OpenAI client lacks chat.completions API")
            resp = chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=2000,
            )
            choices = getattr(resp, "choices", []) or []
            if choices and getattr(choices[0], "message", None):
                content = getattr(choices[0].message, "content", "")
            else:
                content = (choices[0]["message"]["content"] if choices else "")
            text = (content or "").strip()
            fence_match = re.search(r"```(?:json)?\n(.*?)\n```", text, re.DOTALL | re.IGNORECASE)
            json_str = fence_match.group(1).strip() if fence_match else text
            parsed = json.loads(json_str)
            if isinstance(parsed, list):
                quiz_json = {"questions": parsed}
            elif isinstance(parsed, dict) and "questions" in parsed:
                quiz_json = {"questions": parsed.get("questions", [])}
        except Exception:
            quiz_json = {"questions": []}

        test.questions = quiz_json.get("questions", [])
        test.status = "ready"
        db.session.add(test)
        db.session.commit()

        return {"status": "ok", "test_id": test_id}
    except Exception as exc:
        db.session.rollback()
        if test:
            try:
                test.status = "error"
                db.session.add(test)
                db.session.commit()
            except Exception:
                db.session.rollback()
        raise self.retry(exc=exc)
