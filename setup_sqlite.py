import sqlite3
import pandas as pd
import os

DB_PATH = "food_wastage.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_tables(conn):
    cur = conn.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS claims;
        DROP TABLE IF EXISTS food_listings;
        DROP TABLE IF EXISTS receivers;
        DROP TABLE IF EXISTS providers;

        CREATE TABLE providers (
            Provider_ID   INTEGER PRIMARY KEY,
            Name          TEXT,
            Type          TEXT,
            Address       TEXT,
            City          TEXT,
            Contact       TEXT
        );

        CREATE TABLE receivers (
            Receiver_ID   INTEGER PRIMARY KEY,
            Name          TEXT,
            Type          TEXT,
            City          TEXT,
            Contact       TEXT
        );

        CREATE TABLE food_listings (
            Food_ID       INTEGER PRIMARY KEY,
            Food_Name     TEXT,
            Quantity      INTEGER,
            Expiry_Date   TEXT,
            Provider_ID   INTEGER,
            Provider_Type TEXT,
            Location      TEXT,
            Food_Type     TEXT,
            Meal_Type     TEXT
        );

        CREATE TABLE claims (
            Claim_ID      INTEGER PRIMARY KEY,
            Food_ID       INTEGER,
            Receiver_ID   INTEGER,
            Status        TEXT,
            Timestamp     TEXT
        );
    """)
    conn.commit()
    print("✅ Tables created.")

def load_data(conn):
    base = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base, "data")

    tables = {
        "providers":    ("providers_data.csv",    ["Provider_ID","Name","Type","Address","City","Contact"]),
        "receivers":    ("receivers_data.csv",     ["Receiver_ID","Name","Type","City","Contact"]),
        "food_listings":("food_listings_data.csv", ["Food_ID","Food_Name","Quantity","Expiry_Date",
                                                    "Provider_ID","Provider_Type","Location","Food_Type","Meal_Type"]),
        "claims":       ("claims_data.csv",        ["Claim_ID","Food_ID","Receiver_ID","Status","Timestamp"]),
    }

    for table, (filename, cols) in tables.items():
        df = pd.read_csv(os.path.join(data_dir, filename))
        df[cols].to_sql(table, conn, if_exists="replace", index=False)
        print(f"✅ Loaded {len(df)} rows into '{table}'.")

    conn.commit()

if __name__ == "__main__":
    conn = get_connection()
    create_tables(conn)
    load_data(conn)
    conn.close()
    print("\n🎉 SQLite database ready: food_wastage.db")
