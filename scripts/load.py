import logging
import os
import psycopg2

# ----------------------------
# Logging Configuration
# ----------------------------
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DB_PASSWORD = "Sriram_23"

# ----------------------------
# Load Function
# ----------------------------
def load_data():
    conn = None
    cur = None

    try:
        logging.info("Starting bulk load process...")

        logging.info("Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            dbname="retail_db",
            user="postgres",
            password=DB_PASSWORD,
            host="localhost",
            port="5432"
        )

        cur = conn.cursor()

        # 🔥 Truncate existing data (prevents duplicates)
        logging.info("Truncating existing data...")
        cur.execute("TRUNCATE TABLE retail_transactions;")
        conn.commit()

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

        logging.info("Bulk load completed successfully.")

    except Exception as e:
        logging.error(f"Error during bulk load: {e}")
        if conn:
            conn.rollback()
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    load_data()