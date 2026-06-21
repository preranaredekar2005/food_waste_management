import psycopg2
import pandas as pd
import os

# ── DB CONNECTION ──────────────────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "database": "food_wastage",
    "user": "postgres",
    "password": "prerana123",
    "port": 5432
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def create_tables(cur):
    cur.execute("""
        DROP TABLE IF EXISTS claims CASCADE;
        DROP TABLE IF EXISTS food_listings CASCADE;
        DROP TABLE IF EXISTS receivers CASCADE;
        DROP TABLE IF EXISTS providers CASCADE;
    """)

    cur.execute("""
        CREATE TABLE providers (
            Provider_ID   SERIAL PRIMARY KEY,
            Name          VARCHAR(100),
            Type          VARCHAR(50),
            Address       VARCHAR(200),
            City          VARCHAR(50),
            Contact       VARCHAR(20)
        );
    """)

    cur.execute("""
        CREATE TABLE receivers (
            Receiver_ID   SERIAL PRIMARY KEY,
            Name          VARCHAR(100),
            Type          VARCHAR(50),
            City          VARCHAR(50),
            Contact       VARCHAR(20)
        );
    """)

    cur.execute("""
        CREATE TABLE food_listings (
            Food_ID       SERIAL PRIMARY KEY,
            Food_Name     VARCHAR(100),
            Quantity      INTEGER,
            Expiry_Date   DATE,
            Provider_ID   INTEGER REFERENCES providers(Provider_ID),
            Provider_Type VARCHAR(50),
            Location      VARCHAR(50),
            Food_Type     VARCHAR(30),
            Meal_Type     VARCHAR(30)
        );
    """)

    cur.execute("""
        CREATE TABLE claims (
            Claim_ID      SERIAL PRIMARY KEY,
            Food_ID       INTEGER REFERENCES food_listings(Food_ID),
            Receiver_ID   INTEGER REFERENCES receivers(Receiver_ID),
            Status        VARCHAR(20),
            Timestamp     TIMESTAMP
        );
    """)
    print("✅ Tables created.")

def load_csv(cur, table, filepath, columns):
    df = pd.read_csv(filepath)
    for _, row in df.iterrows():
        placeholders = ", ".join(["%s"] * len(columns))
        col_names = ", ".join(columns)
        values = tuple(row[c] for c in columns)
        cur.execute(f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})", values)
    print(f"✅ Loaded {len(df)} rows into '{table}'.")

def main():
    conn = get_connection()
    conn.autocommit = False
    cur = conn.cursor()

    try:
        create_tables(cur)

        load_csv(cur, "providers",
                 os.path.join(DATA_DIR, "providers_data.csv"),
                 ["Provider_ID","Name","Type","Address","City","Contact"])

        load_csv(cur, "receivers",
                 os.path.join(DATA_DIR, "receivers_data.csv"),
                 ["Receiver_ID","Name","Type","City","Contact"])

        load_csv(cur, "food_listings",
                 os.path.join(DATA_DIR, "food_listings_data.csv"),
                 ["Food_ID","Food_Name","Quantity","Expiry_Date",
                  "Provider_ID","Provider_Type","Location","Food_Type","Meal_Type"])

        load_csv(cur, "claims",
                 os.path.join(DATA_DIR, "claims_data.csv"),
                 ["Claim_ID","Food_ID","Receiver_ID","Status","Timestamp"])

        conn.commit()
        print("\n🎉 Database setup complete! All data loaded into 'food_wastage' DB.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
