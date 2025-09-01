1) create a backend endpoing called POST /api/materials/upload in a file like backend/routes/materials_routes.py which accepts file uploads from the frontend and uploads them to a Supabase Storage Bucket named course_materials with the unique path: {course_id}/{file_id}_{original_filename}. Then, in the same endpoint, create a record in the "materials"
table (table defined below) that acts as the central point of truth of the document

2) Create a background job that is triggerred when a document is added to the supabase storage system. the background job will: 1) parse the document using already existing code that uses google's cloud vision library. 2) feed the text into chatgpt (there is code for this already) using a newly created SystemPrompt that generates a summary for the course. 3) saves the summary in the material document, and update the status of the material to "Ready"

3) add the following api routes that the frontend can access: 
GET /api/materials --> gets the list of materials for a course, including their current status. the frontend can poll this endpoint to see when a material becomes 'Ready'
- GET /api/materials/<material_id>/summary --> Fetches the generated summary for a specific material.

1) Storage bucket:  In your Supabase project dashboard, go to the "Storage" section.
       * Create a new bucket and name it exactly course_materials.
       * Security Policies: You will need to establish security rules (policies) for this bucket. For example,
         you'll likely want a policy that only allows authenticated users to upload files into a path that

2) background trigger:
    - do it with supabase functions in supabase/functions directory
    - make sure you add the system prompt, maybe create MaterialSummary.txt
    - add add env's to local + prod