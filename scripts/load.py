import logging
import os
import psycopg2
from dotenv import load_dotenv

# ----------------------------
# LOAD ENV (IMPORTANT FIX)
# ----------------------------
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

print("🔥 SCRIPT STARTED")

# ----------------------------
# LOGGING
# ----------------------------
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------------------
# LOAD FUNCTION
# ----------------------------
def load_data():
    print("🔥 INSIDE load_data()")

    conn = None
    cur = None

    try:
        print("HOST:", os.getenv("DB_HOST"))
        print("PORT:", os.getenv("DB_PORT"))
        print("USER:", os.getenv("DB_USER"))

        logging.info("Connecting to PostgreSQL...")

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            sslmode="require"   # 🔥 CRITICAL
        )

        print("✅ CONNECTED TO DATABASE")

        cur = conn.cursor()

        # ----------------------------
        # CREATE TABLE IF NOT EXISTS
        # ----------------------------
        cur.execute("""
        CREATE TABLE IF NOT EXISTS retail_transactions (
            invoice_no TEXT,
            stock_code TEXT,
            description TEXT,
            quantity INTEGER,
            invoice_date TIMESTAMP,
            unit_price NUMERIC,
            customer_id TEXT,
            country TEXT,
            is_cancelled BOOLEAN,
            is_return BOOLEAN,
            total_price NUMERIC,
            year INTEGER,
            month INTEGER,
            day INTEGER
        );
        """)
        conn.commit()

        # ----------------------------
        # TRUNCATE OLD DATA
        # ----------------------------
        logging.info("Truncating existing data...")
        cur.execute("TRUNCATE TABLE retail_transactions;")
        conn.commit()

        # ----------------------------
        # LOAD DATA
        # ----------------------------
        logging.info("Loading data using COPY command...")

        with open("data/cleaned/transformed_data.csv", "r", encoding="utf-8") as f:
            cur.copy_expert(
                sql="""
                    COPY retail_transactions
                    FROM STDIN
                    WITH CSV HEADER
                    DELIMITER ','
                """,
                file=f
            )

        conn.commit()

        print("✅ DATA LOADED INTO SUPABASE")
        logging.info("Bulk load completed successfully.")

    except Exception as e:
        print("❌ ERROR:", e)
        logging.error(f"Error during bulk load: {e}")
        if conn:
            conn.rollback()
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    load_data()