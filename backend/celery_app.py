import os
from celery import Celery

# Import the Flask app to bind Celery tasks to the Flask application context
from app import app as flask_app


def make_celery(app: "flask.Flask") -> Celery:
    """Create a Celery instance configured from environment vars.

    Ensures tasks run within the Flask app context so they can use
    Flask-SQLAlchemy sessions, configuration, and other app resources.
    """
    broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    result_backend = os.getenv("CELERY_RESULT_BACKEND", broker_url)

    celery = Celery(app.import_name, broker=broker_url, backend=result_backend)

    # Reasonable defaults; adjust as needed
    celery.conf.update(
        task_track_started=True,
        timezone="UTC",
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        task_acks_late=True,
        worker_prefetch_multiplier=1,
        task_time_limit=300,       # hard timeout
        task_soft_time_limit=270,  # soft timeout
        enable_utc=True,
        # For long jobs on Redis broker:
        broker_transport_options={"visibility_timeout": 3600}
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            # Run task inside Flask app context
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# Export a singleton Celery app for workers and producers
celery = make_celery(flask_app)

