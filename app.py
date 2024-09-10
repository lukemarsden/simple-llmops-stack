from flask import Flask, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import base64

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # List all tables in the database
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchall()
    print("Tables in the database:", [table['table_name'] for table in tables])
    
    try:
        cur.execute('''
            SELECT id, text, metadata_, 
            (metadata_->>'timestamp')::timestamp as timestamp 
            FROM data_document_embeddings 
            ORDER BY (metadata_->>'timestamp')::timestamp DESC 
            LIMIT 100;
        ''')
        rows = cur.fetchall()
        for row in rows:
            row['text_b64'] = base64.b64encode(row['text'].encode()).decode()
    except psycopg2.Error as e:
        print("Error:", e)
        rows = []
    
    cur.close()
    conn.close()
    return render_template('index.html', rows=rows, tables=tables)

if __name__ == '__main__':
    app.run(debug=True)