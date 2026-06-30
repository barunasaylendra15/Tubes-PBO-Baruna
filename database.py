import sqlite3
import pandas as pd
from konfigurasi import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    # Membuat tabel transaksi dengan tambahan kolom bukti_nota
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jenis TEXT NOT NULL,
            deskripsi TEXT NOT NULL,
            jumlah REAL NOT NULL CHECK(jumlah > 0),
            kategori TEXT NOT NULL,
            tanggal DATE NOT NULL,
            bukti_nota TEXT
        )
    ''')
    conn.commit()
    conn.close()

def execute_query(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return True

def get_dataframe(query, params=()):
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df