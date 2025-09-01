Note to self: 
    - make sure you add the system prompt, maybe create MaterialSummary.txt
    - add add env's to local + prod
    - make sure you deploy edge functions + also maybe storage as well when ur done

2) Create a background job that is triggered when a document is added to the supabase storage system. the background job will: 1) parse the document using already existing code that uses google's cloud vision library. 2) feed the text into chatgpt (there is code for this already) using a newly created SystemPrompt that generates a summary for the course. 3) saves the summary in the material document, and update the status of the material to "Ready"

3) add the following api routes that the frontend can access: 
GET /api/materials --> gets the list of materials for a course, including their current status. the frontend can poll this endpoint to see when a material becomes 'Ready'
- GET /api/materials/<material_id>/summary --> Fetches the generated summary for a specific material.


2) background trigger:
    - do it with supabase functions in supabase/functions directory
    - make sure you add the system prompt, maybe create MaterialSummary.txt
    - add add env's to local + prod
    - make sure you deploy edge functions when ur done