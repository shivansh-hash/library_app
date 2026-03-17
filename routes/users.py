from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from Connection_db.Connect_db import connect_library_db
import psycopg2.extras
from auth.jwt_auth import get_current_user

route = APIRouter(prefix="/User")
conn = connect_library_db()
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# -------------------------
# Pydantic Model
# -------------------------
class User_pydantic(BaseModel):
    name: str
    email: EmailStr
    password: str


# -------------------------
# REGISTER (Public)
# -------------------------
@route.post("/register")
def register_user(user: User_pydantic):
    cur.execute("SELECT * FROM users WHERE email=%s", (user.email,))
    details = cur.fetchone()

    if details:
        cur.close()
        conn.close()
        return {"message": "User already exists"}

    cur.execute(
        "INSERT INTO users (name,email,password) VALUES(%s,%s,%s)",
        (user.name, user.email, user.password)
    )
    created_user = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return {
        "message": "User registered successfully",
        "name": user.name,
        "email": user.email
    }


# -------------------------
# ADMIN ONLY - View users
# -------------------------
@route.get("/")
def See_user_table(current_user: dict = Depends(get_current_user)):

    # 🔥 Check role here
    if current_user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admin can see users")

    cur.execute("SELECT * FROM users")
    details = cur.fetchall()

    cur.close()
    conn.close()

    return details
@route.delete("/")
def delete_user(email:str,current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admin can see users")
    query="select * from users where email=%s"
    cur.execute(query,(email,))
    details=cur.fetchall()
    if details:
        query="delete from users where email=%s"
        cur.execute(query,(email,))
        conn.commit()
        return "user deleted"
    else:
        return"user not found"


