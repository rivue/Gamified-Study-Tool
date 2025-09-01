1) Create a backend endpoint `POST /api/materials` that accepts `{ name, size, type, course_id }`, creates a `materials` record, and returns the new record including its `id`. The frontend then uploads the file directly to Supabase Storage at `POST {supabase_storage_url}/storage/v1/object/course_materials/{course_id}/{id}_{original_filename}`.
# Prod URL: https://lubdvjbtcknmyycjqyve.supabase.co
# Local URL: http://localhost:54323
table (table defined in models.py) that acts as the central point of truth of the document

 Supabase URLs: To define the upload URLs in UPLOAD.md, I'll need your Supabase project ID. The production URL is typically
      https://<project_id>.supabase.co. For local development, is your Supabase instance running at http://localhost:54321?
    > local url is 54323, production url is lubdvjbtcknmyycjqyve

   2. Course ID: The component needs to know the course_id for the upload path. I assume this is available from the current URL route
      (e.g., the id in /courses/123/materials). Is this correct?
      > that is true, yes

   3. Upload Process: The specified file path {course_id}/{file_id}_{original_filename} requires a file_id from the database before the
      file is uploaded. This suggests a two-step process:
       1. First, the frontend will call a new backend endpoint (e.g., POST /api/materials) with the file metadata (name, size, type) and
          the course_id. The backend creates the database record and returns the new id (file_id).
       2. Second, the frontend uses this file_id to upload the file directly to the correct path in the Supabase Storage bucket.
    > that works for me

      Does this two-step approach work for you? It's a robust and common pattern for this scenario.


2) Create a background job that is triggered when a document is added to the supabase storage system. the background job will: 1) parse the document using already existing code that uses google's cloud vision library. 2) feed the text into chatgpt (there is code for this already) using a newly created SystemPrompt that generates a summary for the course. 3) saves the summary in the material document, and update the status of the material to "Ready"

3) add the following api routes that the frontend can access: 
GET /api/materials --> gets the list of materials for a course, including their current status. the frontend can poll this endpoint to see when a material becomes 'Ready'
- GET /api/materials/<material_id>/summary --> Fetches the generated summary for a specific material.

1) Storage bucket:  In your Supabase project dashboard, go to the "Storage" section.
       * Create a new bucket and name it exactly course-materials.

       - make sure you deploy storage when ur done

2) background trigger:
    - do it with supabase functions in supabase/functions directory
    - make sure you add the system prompt, maybe create MaterialSummary.txt
    - add add env's to local + prod
    - make sure you deploy edge functions when ur done