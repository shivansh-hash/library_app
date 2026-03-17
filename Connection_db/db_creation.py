import psycopg2.extras
conn=psycopg2.connect(
    host="localhost",
    database="postgres",   # connect to default DB first
    user="postgres",
    password="postgres123"
)
conn.autocommit = True
cur=conn.cursor()
db_create_querry=("CREATE DATABASE library_db;")
cur.execute(db_create_querry)
conn.commit()
print("creation done")