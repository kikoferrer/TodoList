import sqlite3
import os


class Database:
    def __init__(self, title: str):
        self.title = title.lower()

    def connect_db(self):
        if not os.path.exists("db"):
            os.makedirs("db")
        self.conn = sqlite3.connect("./db/todolist.db")
        self.cursor = self.conn.cursor()

    def close_db(self) -> None:
        self.conn.close()

    def create_table(self) -> None:
        self.connect_db()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS "{}" (
                id_num INTEGER,
                entry_content TEXT NOT NULL,
                date_updated TEXT
            )
        """.format(
                self.title
            )
        )
        self.conn.commit()
        self.close_db()

    def extract_table(self) -> dict:
        self.connect_db()
        self.cursor.execute("SELECT * FROM '{}'".format(self.title))
        rows = self.cursor.fetchall()
        data = {}
        for i, row in enumerate(rows, start=1):
            data[i] = {
                "id_num": i,
                "entry_content": row[1],
                "date_updated": row[2],
            }
        self.close_db()
        return data

    def save_entries_to_db(self, data: dict) -> None:
        self.connect_db()
        self.cursor.execute("DELETE FROM '{}'".format(self.title))
        self.cursor.executemany(
            "INSERT INTO '{}' (id_num, entry_content, date_updated) VALUES (:id_num, :entry_content, :date_updated)".format(
                self.title
            ),
            data.values(),
        )
        self.conn.commit()
        self.close_db()
