
import sqlite3
import os

# Use the same URI as in your app
db_uri = "sqlite:///app.db"
db_path = "app.db"  # Relative path, since we're in /app/backend

try:
    print(f"Connecting to SQLite database at: {db_path}")

    # Connect to the database
    connection = sqlite3.connect(db_path)
    print("Connected successfully!")

    # Run a simple query to verify the database is accessible
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:", tables)

    connection.close()

except Exception as e:
    print(f"Failed to connect to the database: {e}")