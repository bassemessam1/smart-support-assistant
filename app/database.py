import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
    )


def create_ticket(title: str, description: str):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO tickets (title, description, status) VALUES (%s, %s, 'open')",
            (title, description)
        )
        conn.commit()
        ticket_id = cursor.lastrowid

        cursor.execute("SELECT * FROM tickets WHERE id=%s", (ticket_id,))
        return cursor.fetchone()

    finally:
        cursor.close()
        conn.close()


def update_ticket(ticket_id: int, description: str):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM tickets WHERE id=%s", (ticket_id,))
        row = cursor.fetchone()
        if not row:
            return {"error": "Ticket not found"}

        cursor.execute("UPDATE tickets SET description=%s WHERE id=%s", (description, ticket_id))
        conn.commit()

        cursor.execute("SELECT * FROM tickets WHERE id=%s", (ticket_id,))
        return cursor.fetchone()

    finally:
        cursor.close()
        conn.close()


def get_ticket_status(ticket_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, status FROM tickets WHERE id=%s", (ticket_id,))
        row = cursor.fetchone()
        return row or {"error": "Ticket not found"}

    finally:
        cursor.close()
        conn.close()


def get_all_tickets():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tickets ORDER BY id ASC")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
