import psycopg2
import psycopg2.extras
import os
from datetime import datetime, timedelta
from email_utils import send_otp_email
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=psycopg2.extras.RealDictCursor)
    return conn

import random

def generate_otp():
    return str(random.randint(100000, 999999))

from fastapi import FastAPI
from fastapi import WebSocket, WebSocketDisconnect


connected_clients=[]

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from the backend!"}




@app.websocket("/wb")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept() 
    connected_clients.append(websocket)
    try: 
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)


async def broadcast_teams():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM teams")
    p=cursor.fetchall()
    conn.close()
    for i in connected_clients:
        await i.send_json(p)

@app.get("/teams")
def get_teams():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM teams")
    p=cursor.fetchall()
    conn.close()
    return p


@app.get("/persons")
def get_persons():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM persons")
    p=cursor.fetchall()
    conn.close()
    return p

@app.post("/persons/{name}/{age}")
def insert_person(name,age):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("INSERT INTO persons (name,age) VALUES (%s,%s)", (name,age))
    conn.commit()
    conn.close()
    return 0

@app.post("/vote/{email}/{team_id}")
async def vote(email: str, team_id: int):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM voted_emails WHERE email = %s", (email,))
    existing=cursor.fetchone()
    if existing is not None:
        conn.close()
        return {"success": False, "reason": "Already voted"}


    cursor.execute("UPDATE teams SET votes = votes + 1 WHERE id = %s", (team_id,))
    cursor.execute("INSERT INTO voted_emails (email,id) VALUES (%s,%s)", (email,team_id))
    conn.commit()
    conn.close()
    await broadcast_teams()
    return {"success":True}




@app.post("/send-otp/{email}")
def send_otp(email: str):
    otp=generate_otp()
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("INSERT INTO otps (email, code, created_at) VALUES (%s, %s, %s) ON CONFLICT (email) DO UPDATE SET code = EXCLUDED.code, created_at = EXCLUDED.created_at", (email,otp,datetime.now().isoformat()))
    conn.commit()
    conn.close()
    send_otp_email(email,otp)
    return {"Message": "Sent"}


@app.post("/verify-otp/{email}/{code}")
def verify_otp(email: str, code: str):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM otps WHERE email = %s", (email,))
    row=cursor.fetchone()
    if row is None:
        conn.close()
        return {"Verified": False, "reason": "NO OTP requested"}
    elif row["code"]!=code:
        conn.close()
        return {"Verified": False, "reason": "Wrong OTP entered"}
    elif datetime.now()-datetime.fromisoformat(row["created_at"])> timedelta(minutes=5):
        conn.close()
        return {"Verified": False, "reason": "Wrong time frame"}
    else:
        conn.close()
        return {"Verified":True}
    