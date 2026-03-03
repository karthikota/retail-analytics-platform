import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

DB_PASSWORD = "Sriram_23"

def generate_report():
    print("Connecting to PostgreSQL...")

    conn = psycopg2.connect(
        dbname="retail_db",
        user="postgres",
        password=DB_PASSWORD,
        host="localhost",
        port="5432"
    )

    query = """
        SELECT year, month, SUM(total_price) AS monthly_revenue
        FROM retail_transactions
        GROUP BY year, month
        ORDER BY year, month;
    """

    df = pd.read_sql(query, conn)
    conn.close()

    print("Generating revenue trend chart...")

    df["year_month"] = df["year"].astype(str) + "-" + df["month"].astype(str)

    plt.figure(figsize=(10,5))
    plt.plot(df["year_month"], df["monthly_revenue"], marker="o")
    plt.xticks(rotation=45)
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Year-Month")
    plt.ylabel("Revenue")
    plt.tight_layout()

    plt.savefig("screenshots/monthly_revenue.png")
    print("Report saved as monthly_revenue.png")

if __name__ == "__main__":
    generate_report()