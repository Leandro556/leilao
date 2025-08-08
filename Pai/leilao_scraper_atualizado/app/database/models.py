
from app.database.db import get_connection

def save_edital(edital):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO editais (estado, municipio, descricao, data, url)
        VALUES (?, ?, ?, ?, ?)
    """, (edital['estado'], edital['municipio'], edital['descricao'], edital['data'], edital['url']))
    conn.commit()
    conn.close()

def get_all_editais():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM editais ORDER BY data DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
