import sqlite3
import os


class Database:
    def __init__(self, title: str):
        if not os.path.exists("db"):
            os.makedirs("db")
        self.conn = sqlite3.connect("./db/todolist.db")
        self.cursor = self.conn.cursor()
        self.title = title

    def create_table(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS "{}" (
                id_num INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_content TEXT NOT NULL,
                date_updated TEXT
            )
        """.format(
                self.title
            )
        )
        self.conn.commit()

    def extract_table(self) -> dict:
        self.cursor.execute(f"SELECT * FROM {self.title}")
        rows = self.cursor.fetchall()
        data = {}
        for i, row in enumerate(rows, start=1):
            data[i] = {
                "id_num": i,
                "entry_content": row[0],
                "date_updated": row[1],
            }
        return data

    def save_entries_to_db(self, data: dict) -> None:
        self.cursor.execute("DELETE FROM '{}'".format(self.title))
        self.cursor.executemany(
            "INSERT INTO '{}' (id_num, entry_content, date_updated) VALUES (:id_num, :entry_content, :date_updated)".format(
                self.title
            ),
            data.values(),
        )
        self.conn.commit()

    def close_db(self) -> None:
        self.conn.close()
