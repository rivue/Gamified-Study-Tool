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
        timezone="UTC",
        task_track_started=True,
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
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

