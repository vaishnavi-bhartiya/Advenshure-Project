import os
import logging
import pandas as pd
import sqlite3   # for local demo
import psycopg2  # for production Postgres
from psycopg2.extras import execute_values
from mock_api import fetch_data   # local mock instead of real API

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def get_data():
    df = fetch_data()
    logging.info(f"Fetched {len(df)} records")
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset=["email"])
    df = df.dropna(subset=["id", "email"])
    return df

#two loaders: one for Postgres (production), one for SQLite (local demo).


def load_to_postgres(df: pd.DataFrame):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT", 5432)
    )
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO users (id, name, email, address, created_at)
        VALUES %s
        ON CONFLICT (id) DO UPDATE
        SET name = EXCLUDED.name,
            email = EXCLUDED.email,
            address = EXCLUDED.address,
            created_at = EXCLUDED.created_at;
    """
    records = df[["id", "name", "email", "address", "createdAt"]].values.tolist()
    execute_values(cursor, insert_query, records, page_size=1000)
    conn.commit()
    cursor.close()
    conn.close()
    logging.info(f"Inserted {len(records)} records into Postgres")

def load_to_sqlite(df: pd.DataFrame):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT UNIQUE,
            address TEXT,
            created_at TEXT
        )
    """)
    records = df[["id", "name", "email", "address", "createdAt"]].values.tolist()
    cursor.executemany("INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?)", records)
    conn.commit()
    conn.close()
    logging.info(f"Inserted {len(records)} records into SQLite")

def main():
    df = get_data()
    df = clean_data(df)
    try:
        load_to_postgres(df)
    except Exception as e:
        logging.warning(f"Postgres not available, falling back to SQLite: {e}")
        load_to_sqlite(df)

if __name__ == "__main__":
    main()
