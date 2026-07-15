import sqlite3


DB_PATH = "API/examguard.db"


def create_database():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            image_name TEXT,

            image_path TEXT,

            status TEXT,

            risk_score INTEGER,

            detections TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()
    conn.close()
def check_tables():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )

    print(cursor.fetchall())

    conn.close()

def save_history(
    image_name,
    image_path,
    status,
    risk_score,
    detections
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO history(

            image_name,
            image_path,
            status,
            risk_score,
            detections

        )

        VALUES(?,?,?,?,?)

    """,(

        image_name,
        image_path,
        status,
        risk_score,
        detections

    ))

    conn.commit()

    conn.close()


def get_history():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM history

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
def clear_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()