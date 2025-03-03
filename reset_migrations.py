
import sqlite3

# Connect to your database
conn = sqlite3.connect("instance/db.sqlite3")
cursor = conn.cursor()

# Delete migration records for problematic apps
cursor.execute("DELETE FROM django_migrations WHERE app IN (\"accounts\", \"employers\", \"jobs\", \"applications\")")

# Commit changes and close connection
conn.commit()
conn.close()
print("Migration records deleted successfully!")

