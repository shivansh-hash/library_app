from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel,EmailStr
from Connection_db.Connect_db import connect_library_db
from auth.jwt_auth import get_current_user
from Models.Table_schema import create_table_user , create_table_books,create_table_issued_books
import psycopg2.extras
class books_pydantic(BaseModel):
    """create table if not exists books (book_id int PRIMARY KEY ,
        title VARCHAR (100) NOT NULL, gener VARCHAR(100)  NOT NULL , copies_available INT )"""

    title:str
    genre:str
    writer:str
    copies_available:int
route= APIRouter(prefix="/Books")
conn = connect_library_db()
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
@route.get("/")
def see_book_details():
    query = "SELECT * FROM  books "
    cur.execute(query)
    details = cur.fetchall()
    return details



# -------------------------
# ADMIN ONLY - View books details
# -------------------------
@route.post("/")
def insert_into_book_details(books:books_pydantic,current_user: dict = Depends(get_current_user)):
    # 🔥 Check role here
    if current_user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admin can see users")
    query = "SELECT * FROM  books where title=%s AND genre=%s"
    cur.execute(query,(books.title,books.genre))
    details = cur.fetchall()
    if details:
        return "books is already present "
    else:
        query="insert into books (title,genre,writer,copies_available) values(%s,%s,%s,%s)"
        cur.execute(query, (books.title,books.genre,books.writer,books.copies_available))
        conn.commit()
        return"insertion successfully done"


# -------------------------
# Any user  - Search books via genre
# -------------------------
@route.get("/search")
def search_book_via_genre(genre:str):
    query="select * from books where Lower(genre)=Lower(%s)"
    cur.execute(query,(genre,))
    details=cur.fetchall()
    if details:
        return details
    else:
        return "enter valid genre"