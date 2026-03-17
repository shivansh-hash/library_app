# " shri ganeshay namah "
import psycopg2.extras
from fastapi import FastAPI
from pydantic import BaseModel , EmailStr
class Connect_DB:
    def connect_to_admin_user(self):
            self.admin_conn=psycopg2.connect(
                dbname="library_db",
                user="admin_user",
                password="admin123",
                host="localhost",
                port="5432"
            )
            self.admin_cur=self.admin_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    def connect_to_normal_user(self):
            self.normal_conn = psycopg2.connect(
                database="library_db",
                user="normal_user",
                password="user123",
                host="localhost",
                port="5432"
            )
            self.normal_cur = self.normal_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def close_db(conn, cur):
        if cur:
            cur.close()
        if conn:
            conn.close()
db=Connect_DB()
db.connect_to_admin_user()
db.connect_to_normal_user()
db.admin_cur.execute("""
    CREATE TABLE IF NOT EXISTS book_details (
        Book_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        Book_Name TEXT,
        Gener TEXT,
        Quantity_available int
         
    )
""")
db.admin_cur.execute("""
    CREATE TABLE IF NOT EXISTS issued_books (
        issue_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        Book_id INT ,
        Book_Name TEXT,
        issue_date DATE DEFAULT CURRENT_DATE
    );
""")
db.admin_conn.commit()
class Book_Pydantic(BaseModel):
    book_name:str
    gener:str
    qt_available:int
app=FastAPI()

class Admin:
    @app.post("/Book_Details_Insert")
    def Details(book:Book_Pydantic):
        db.admin_cur.execute("insert into book_details (book_name,gener,quantity_available)  "
                       "values (%s,%s,%s)",(book.book_name,book.gener,book.qt_available))
        db.admin_conn.commit()
        return("insertion done ")

    @app.get("/To_See_Entire_Book_Details")
    def View_Book_Detail(self):
        db.admin_cur.execute("select * from book_details")
        row=db.admin_cur.fetchall()
        return(row)
    @app.get("/To_See_Particular_Gener/{gen}")

    def See_Through_Gener(gen:str):
        db.admin_cur.execute("select * from book_details where gener=%s", (gen,))
        check = db.admin_cur.fetchall()
        if check:
            db.admin_cur.execute("select * from book_details where gener=%s",(gen,))
            row=db.admin_cur.fetchall()
            return(row)
        else:
            return"This gener book is not available "

class User_Pydantic(BaseModel):
    name:str
    department:str
    email:EmailStr
class User:
    @app.post("/User_Login")
    def Insert_Into_User(users:User_Pydantic):
        db.admin_cur.execute("select 1 from user_admin where email=%s",(users.email,))
        check=db.admin_cur.fetchone()
        if check:
            return"User already exist you are logged in"
        else:
            db.admin_cur.execute("insert into user_admin(name,department,email) values(%s,%s,%s)",
                           (users.name,users.department,users.email,))
            db.admin_conn.commit()
            return"user registered"


class Issue_Book:
    @app.get('/Which_Gener_Book_You_Want_To_Check/{Book_Gener}')
    def Check_If_Book_Present(book_gener:str):
        db.normal_cur.execute("select * from book_details where gener=%s",(book_gener,))
        check=db.normal_cur.fetchall()
        if check:
            db.normal_cur.execute("select * from book_details where gener=%s", (book_gener,))
            row = db.normal_cur.fetchall()
            return(' This gener book is present here are all the book of this gener',row)

        else:
            return "This gener book is not available"
    @app.post('/Which_book_you_want_to_take/{book_id}/{book_name}')
    def Issue_Books(book_id:str,book_name:str):
        db.admin_cur.execute("select * from book_details where book_name=%s", (book_name,))
        check = db.admin_cur.fetchall()
        if check:
            db.admin_cur.execute("INSERT INTO issued_books (book_id, book_name) values(%s,%s)", (book_id,book_name))
            db.admin_conn.commit()
            db.admin_cur.execute("update book_details set quantity_available = quantity_available-1 where book_id=%s",
                           (book_id,))
            db.admin_conn.commit()
            return ('book issued')
        else:
            return"book is not available"
    @app.get('/See_Issued_Books_Table')
    def See_Issued_Books_Details(self):
        db.normal_cur.execute("select * from issued_books")
        row=db.normal_cur.fetchall()
        return(row)
    @app.delete('/Enter_Book_Id_You_Want_To_Return/{book_id}')
    def Return_Book(book_id:int):
        db.admin_cur.execute("select * from issued_books where book_id=%s", (book_id,))
        check = db.admin_cur.fetchone()
        if check:
            db.admin_cur.execute("delete from issued_books where book_id=%s",(book_id,))
            db.admin_conn.commit()
            db.admin_cur.execute("update book_details set quantity_available = quantity_available+1 where book_id=%s",(book_id,))
            db.admin_conn.commit()
            return("Book returned")
        else:
            return('you have no issued books')
"""
close_db(db.admin_conn,db.admin_cur)
close_db(db.normal_conn,db.normal_cur)
"""





































































