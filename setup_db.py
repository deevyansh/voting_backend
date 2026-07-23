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

# cursor.execute("INSERT INTO teams (name, votes) VALUES (%s, %s)", ("Real Madrid", 0))
# cursor.execute("INSERT INTO teams (name, votes) VALUES (%s, %s)", ("Barcelona", 0))
# cursor.execute("INSERT INTO teams (name, votes) VALUES (%s, %s)", ("Manchester United", 0))

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



# cursor.execute("ALTER TABLE teams ADD COLUMN IF NOT EXISTS logo_url TEXT")

# cursor.execute("UPDATE teams SET logo_url = %s WHERE name = %s", 
#     ("https://r2.thesportsdb.com/images/media/team/badge/vwpvry1467462651.png", "Real Madrid"))
# cursor.execute("UPDATE teams SET logo_url = %s WHERE name = %s", 
#     ("https://r2.thesportsdb.com/images/media/team/badge/uyhbfe1612467038.png", "Barcelona"))
# cursor.execute("UPDATE teams SET logo_url = %s WHERE name = %s", 
#     ("https://r2.thesportsdb.com/images/media/team/badge/xzqdr11517660252.png", "Manchester United"))

# cursor.execute("INSERT INTO teams (name, votes, logo_url) VALUES (%s, %s, %s)",
#     ("Liverpool", 0, "https://r2.thesportsdb.com/images/media/team/badge/uvxuqp1448813233.png"))
# cursor.execute("INSERT INTO teams (name, votes, logo_url) VALUES (%s, %s, %s)",
#     ("Bayern Munich", 0, "https://r2.thesportsdb.com/images/media/team/badge/xzrwuq1420227405.png"))
# cursor.execute("INSERT INTO teams (name, votes, logo_url) VALUES (%s, %s, %s)",
#     ("Paris Saint-Germain", 0, "https://r2.thesportsdb.com/images/media/team/badge/twuxyx1420229907.png"))



cursor.execute("UPDATE teams SET logo_url = %s WHERE name = %s", 
    ("https://r2.thesportsdb.com/images/media/team/badge/kfaher1737969724.png", "Liverpool"))
cursor.execute("UPDATE teams SET logo_url = %s WHERE name = %s", 
    ("https://r2.thesportsdb.com/images/media/team/badge/01ogkh1716960412.png", "Bayern Munich"))
cursor.execute("UPDATE teams SET logo_url = %s WHERE name = %s", 
    ("https://r2.thesportsdb.com/images/media/team/badge/rwqrrq1473504808.png", "Paris Saint-Germain"))

connection.commit()
connection.close()