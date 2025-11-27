import mysql.connector
from dotenv import load_dotenv
import os
import time

load_dotenv()

TABLE_CREATION_QUERY = """
CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'open'
);
"""

def wait_for_mysql():
    for _ in range(20):
        try:
            conn = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER", "root"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DATABASE")
            )
            conn.close()
            print("MySQL ready.")
            return
        except:
            print("Waiting for MySQL...")
            time.sleep(2)


def create_tables():
    wait_for_mysql()
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    cursor = conn.cursor()
    cursor.execute(TABLE_CREATION_QUERY)
    conn.commit()
    cursor.close()
    conn.close()
    print("Tables created successfully.")


if __name__ == "__main__":
    create_tables()
