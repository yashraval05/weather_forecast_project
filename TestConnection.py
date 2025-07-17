import psycopg2
conn = psycopg2.connect(
    host="db.tskjdwgwanvthycebdiw.supabase.co",
    port="5432",
    database="postgres",
    user="postgres",
    password=""
)
print("Connected successfully!")
conn.close()
