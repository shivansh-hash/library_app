from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from auth.jwt_auth import create_access_token
import psycopg2.extras
from Connection_db.Connect_db import connect_library_db

route = APIRouter(prefix="/auth")

conn = connect_library_db()
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


class LoginModel(BaseModel):
    email: EmailStr
    password: str


@route.post("/login")
def login(data: LoginModel):

    query = "SELECT * FROM users WHERE email=%s AND password=%s"
    cur.execute(query, (data.email, data.password))
    user = cur.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "email": user["email"],
        "role": user["role"]
    })

    return {"access_token": token, "token_type": "bearer"}
@route.post("/logout")
def logout():
    return {"message": "Logged out successfully"}