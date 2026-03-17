from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel
from Connection_db.Connect_db import connect_library_db
import psycopg2.extras
from auth.jwt_auth import get_current_user

class Issued_pydantic(BaseModel):
    user_id: int
    user_name: str
    book_title: str


route = APIRouter(prefix="/issued-books")

conn = connect_library_db()
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


# ✅ GET → See books by genre
@route.get("/gener ")
def which_genre_book_you_want(genre: str):
    query = "SELECT * FROM books WHERE LOWER(genre) = LOWER(%s)"
    cur.execute(query, (genre,))
    details = cur.fetchall()

    if details:
        return details
    else:
        raise HTTPException(status_code=400, detail="Enter valid genre ! we do not have this genre book")

# ✅ POST → Issue Book
@route.post("/")
def issue_book(data: Issued_pydantic):

    # 🔹 1. Check User
    query = "SELECT * FROM users WHERE id=%s AND LOWER(name)=LOWER(%s)"
    cur.execute(query, (data.user_id, data.user_name))
    user = cur.fetchone()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid user ID or name")

    # 🔹 2. Check Book + Copies
    query = "SELECT * FROM books WHERE LOWER(title)=LOWER(%s)"
    cur.execute(query, (data.book_title,))
    book = cur.fetchone()

    if not book:
        raise HTTPException(status_code=400, detail="Book not found")

    if book["copies_available"] <= 0:
        raise HTTPException(status_code=400, detail="Book not available")

    # 🔹 3. Insert into issued_books
    insert_query = """
    INSERT INTO issued_books (user_id, book_title,user_name)
    VALUES (%s, %s , %s)
    """
    cur.execute(insert_query, (data.user_id, data.book_title, data.user_name,))

    # 🔹 4. Decrease copies
    update_query = """
    UPDATE books
    SET copies_available = copies_available - 1
    WHERE LOWER(title)=LOWER(%s)
    """
    cur.execute(update_query, (data.book_title,))

    conn.commit()

    return "Book issued successfully"
@route.get("/see-table")
def see_entire_issued_books_table(current_user: dict = Depends(get_current_user)):
    # 🔥 Check role here
    if current_user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admin can see users")

    cur.execute("SELECT * FROM issued_books")
    details = cur.fetchall()
    cur.close()
    conn.close()
    return details
@route.get("/")
def see_your_credentials(email:str):
    query="select id,name,email from users where email=%s"
    cur.execute(query,(email,))
    details=cur.fetchall()
    return(details)
@route.get("/see-books-issued-on-you")
def books_issued_on_you(user_id:int):
    query="select * from issued_books where user_id=%s"
    cur.execute(query,(user_id,))
    details=cur.fetchall()
    if details:
        return details
    else:
        raise HTTPException(status_code=400, detail="Invalid user ID or no book issued on your id")

@route.delete("/")
def return_book(issued_id:int,book_title:str):
    query="select * from issued_books where issued_id=%s"
    cur.execute(query, (issued_id,))
    details=cur.fetchall()
    if details:
        qu = """
        DELETE FROM issued_books
        WHERE issued_id=%s 
        """
        cur.execute(qu,(issued_id,))
        result=conn.commit()
        update_query = """
        UPDATE books
        SET copies_available = copies_available + 1
        WHERE LOWER(title) = LOWER(%s)
        """
        cur.execute(update_query, (book_title,))
        conn.commit()
        return"book returned"
    else:
        raise HTTPException(status_code=400, detail="Invalid user ID or no book issued on your id")