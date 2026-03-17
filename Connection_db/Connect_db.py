import psycopg2.extras
def connect_library_db():
    conn=psycopg2.connect(
        host="localhost",
        database="library_db",   # connect to Library_db (database)
        user="library_user",
        password="library@123"

    )
    return conn

#admin_cur=admin_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#normal_cur=normal_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
