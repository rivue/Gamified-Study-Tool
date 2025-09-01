import os
from supabase import create_client, Client
from .models import db, Material
from werkzeug.datastructures import FileStorage

# This is a placeholder for your actual Supabase client.
# Ideally, you should initialize this once in your main app factory
# and import it here to avoid creating multiple clients.
try:
    # Attempt to import from a central location
    from ..app import supabase
except (ImportError, ModuleNotFoundError):
    print("Warning: Could not import Supabase client from backend.app. Using a fallback initialization.")
    SUPABASE_URL = os.environ.get("SUPABASE_URL", "http://localhost:54323")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY") # Your anon key
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

    # 1. Create an initial Material record to get an ID
    # We set a temporary storage_path because the column is not nullable.
    new_material = Material(
        library_id=course_id, # Assuming course_id maps to library_id
        name=file.filename,
        type=file.filename.split('.')[-1].lower(),
        size=file.content_length or 0,
        status='processing',
        storage_path='_temp' 
    )
    db.session.add(new_material)
    db.session.flush() # Use flush to get the auto-generated ID from the DB sequence

    material_id = new_material.id
    storage_path = f"{course_id}/{material_id}_{file.filename}"
    
    try:
        # 2. Upload the file to Supabase Storage
        file.stream.seek(0)
        file_bytes = file.read()
        
        supabase.storage.from_("course_materials").upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": file.mimetype or 'application/octet-stream'}
        )

        # 3. Update the material record with the final storage_path
        new_material.storage_path = storage_path
        db.session.commit()

        return new_material

    except Exception as e:
        # If anything fails, roll back the entire transaction
        db.session.rollback()
        print(f"Error during material upload: {e}")
        # You might want to add logic here to delete the file from storage if it was already uploaded
        raise