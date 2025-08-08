
import sqlite3

def init_db():
    conn = sqlite3.connect("leiloes.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS editais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estado TEXT,
            municipio TEXT,
            descricao TEXT,
            data TEXT,
            url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect("leiloes.db")
