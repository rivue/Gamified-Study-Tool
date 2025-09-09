backend:
- flask run

frontend:
- npm run serve

redis:
- docker run -p 6379:6379 redis:7

celery (in backend/):
- celery -A tasks worker --loglevel INFO 
Note: for MacOS, add -P solo --concurrency=1