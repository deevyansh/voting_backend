import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
load_dotenv()

connection = psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=psycopg2.extras.RealDictCursor)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS teams (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    votes INTEGER NOT NULL DEFAULT 0
)
""")

cursor.execute("INSERT INTO teams (name, votes) VALUES (%s, %s)", ("Real Madrid", 0))
cursor.execute("INSERT INTO teams (name, votes) VALUES (%s, %s)", ("Barcelona", 0))
cursor.execute("INSERT INTO teams (name, votes) VALUES (%s, %s)", ("Manchester United", 0))

cursor.execute("""
    CREATE TABLE IF NOT EXISTS otps(
    email TEXT PRIMARY KEY,
    code TEXT NOT NULL,
    created_at TEXT NOT NULL
    )
""")


cursor.execute ("""
    CREATE TABLE IF NOT EXISTS voted_emails(
        email TEXT PRIMARY KEY,
        id INTEGER NOT NULL      
    )
""")

connection.commit()
connection.close()