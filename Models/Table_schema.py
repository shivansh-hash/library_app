from Connection_db.Connect_db import connect_library_db
import psycopg2.extras
def create_table_user():
    conn=connect_library_db()
    cur=conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL,
        role VARCHAR(20) DEFAULT 'USER' CHECK (role IN ('ADMIN','USER'))
    )
    """
    try :
        cur.execute(query)
        conn.commit()
        print("table creation done ")
    except:
        print("table creation not done ")
def create_table_books():
    conn = connect_library_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """create table if not exists books (book_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
        title VARCHAR (100) NOT NULL, genre VARCHAR(100)  NOT NULL ,writer VARCHAR (100) NOT NULL,  copies_available INT )"""
    try:
        cur.execute(query)
        conn.commit()
        print("table creation done ")
    except:
        print("table creation not done ")
def create_table_issued_books():
    conn = connect_library_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """create table if not exists issued_books (issued_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY ,
     user_id int NOT NULL,book_title VARCHAR(100),
    user_name VARCHAR(100)  NOT NULL, issue_date DATE DEFAULT CURRENT_DATE   NOT NULL,
            return_date DATE DEFAULT (CURRENT_DATE + INTERVAL '5 days'))"""
    try:
        cur.execute(query)
        conn.commit()
        print("table creation done ")
    except:
        print("table creation not done,")



create_table_user()
create_table_books()
create_table_issued_books()
