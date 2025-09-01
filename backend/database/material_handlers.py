import os
import json
from supabase import create_client, Client
from .models import db, Material
from werkzeug.datastructures import FileStorage
from io import BytesIO

# This is a placeholder for your actual Supabase client.
# Ideally, you should initialize this once in your main app factory
# and import it here to avoid creating multiple clients.
try:
    # Attempt to import from a central location
    from ..app import supabase
except (ImportError, ModuleNotFoundError):
    print("Warning: Could not import Supabase client from backend.app. Using a fallback initialization.")
    SUPABASE_URL = os.environ.get("SUPABASE_URL", "http://127.0.0.1:54321")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    if not SUPABASE_KEY:
        raise ValueError("Supabase key is not set in environment variables.")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def create_and_upload_material(course_id: int, file: FileStorage):
    """
    Creates a material record, uploads the file to Supabase Storage,
    and updates the record with the final storage path.
    """
    if not file or not file.filename:
        raise ValueError("Invalid file provided.")

    # --- Safer File Reading with Chunking ---
    # Enforce a maximum file size to protect the server (e.g., 25MB)
    MAX_FILE_SIZE = 25 * 1024 * 1024
    CHUNK_SIZE = 4 * 1024 * 1024  # Read in 4MB chunks

    parts = []
    total_bytes_read = 0
    while True:
        chunk = file.stream.read(CHUNK_SIZE)
        if not chunk:
            break  # End of file
        
        total_bytes_read += len(chunk)
        if total_bytes_read > MAX_FILE_SIZE:
            raise ValueError(f"File exceeds the maximum allowed size of {int(MAX_FILE_SIZE / 1024 / 1024)}MB.")
            
        parts.append(chunk)

    file_bytes = b''.join(parts)
    # --- End of Safer File Reading ---

    new_material = Material(
        library_id=course_id,
        name=file.filename,
        type=file.filename.split('.')[-1].lower(),
        size=total_bytes_read, # Use the actual bytes read for size
        status='processing',
        storage_path='_temp'
    )
    db.session.add(new_material)
    db.session.flush()

    material_id = new_material.id
    storage_path = f"{course_id}/{material_id}_{file.filename}"
    
    try:
        try:
            supabase.storage.from_("course-materials").upload(
                path=storage_path,
                file=file_bytes,
                file_options={"content-type": file.mimetype or "application/octet-stream"}
            )
        except json.JSONDecodeError:
            raise Exception("Failed to parse Supabase response. Check your SUPABASE_URL and ensure you are using the SERVICE_ROLE_KEY.")

        new_material.storage_path = storage_path
        db.session.commit()

        return new_material

    except Exception as e:
        db.session.rollback()
        print(f"Error during material upload: {e}")
        raise