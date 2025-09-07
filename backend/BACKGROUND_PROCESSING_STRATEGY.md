# Background Processing Strategy for Long-Running Tasks

This document outlines a robust architectural approach for handling long-running, asynchronous tasks like AI summarization, PDF processing, and vector embedding generation.

## 1. The Challenge

Our application needs to perform heavy processing tasks that are initiated by user actions (e.g., uploading a file). A naive approach using a single serverless function (like a Supabase Edge Function) to handle the entire process poses a significant risk:

- **Timeouts:** Serverless functions have short execution time limits (e.g., 1-2 minutes). A large file, slow external API call (to Gemini), or complex processing can easily exceed this limit, causing the task to fail.
- **Code Duplication:** Our core processing logic is in Python (`vector_processing`, `knowledge_net`). Re-implementing this in TypeScript for an Edge Function would create a split-brain architecture that is difficult to maintain.

## 2. Proposed Architecture: The Hybrid Approach

To solve this, we will use a hybrid model that combines the strengths of serverless triggers with the power of a dedicated backend task queue.

The workflow is as follows:

1.  **Trigger:** A user uploads a file to **Supabase Storage**.
2.  **Notification:** A **Supabase Hook** (Storage Trigger) fires, invoking a lightweight **Edge Function**.
3.  **Delegation:** The Edge Function's *only* responsibility is to immediately send a webhook call to a dedicated endpoint on our Flask backend (e.g., `/api/tasks/process-material`). It passes a reference to the file, like its path or ID.
4.  **Acknowledgement:** The Flask endpoint receives the request, validates it, and immediately adds a job to a **Celery Task Queue** (backed by Redis).
5.  **Immediate Response:** The endpoint instantly returns a `202 Accepted` status, signaling that the task has been queued. The Edge Function and Supabase Hook have now completed their work.
6.  **Execution:** A separate **Celery Worker** process, running on our backend server, picks up the job from the queue.
7.  **Completion:** The worker executes the entire long-running task with no time limits:
    - Downloads the file from Supabase Storage.
    - Performs any necessary pre-processing (e.g., text extraction from PDF).
    - Calls the Gemini API for summarization or analysis.
    - Writes the result back to our Supabase database.

### Visual Flow

```
[User] -> [Supabase Storage]
   |
   v
[Supabase Hook] -> [Edge Function] --(Fast Webhook Call)--> [Flask API Endpoint]
                                                                 |
                                                                 v
                                                             [Celery Queue (Redis)] -> [Celery Worker]
                                                                                            |
                                                                                            +--> (Heavy Lifting)
                                                                                            |    - Download File
                                                                                            |    - Call Gemini API
                                                                                            |    - Update Supabase DB
```

## 3. Benefits of this Approach

- **Reliability:** Eliminates the risk of timeouts for background jobs.
- **Resilience:** Celery provides robust, configurable retry mechanisms for failed tasks (e.g., if the Gemini API is temporarily unavailable).
- **Centralized Logic:** All complex processing logic remains in our Python backend, leveraging our existing code and libraries.
- **Responsiveness:** The triggering system (Supabase) is not blocked and remains highly responsive.
- **Message Durability:** Redis provides persistent message queuing with advanced routing and delivery guarantees.

