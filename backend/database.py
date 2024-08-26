import sqlite3


class Database:
    def __init__(self, title: str):
        self.conn = sqlite3.connect("./db/todolist.db")
        self.cursor = self.conn.cursor()
        self.title = title

    def create_table(self) -> None:
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.title} (
            id_num INTEGER,
            entry_content TEXT NOT NULL,
            date_updated DATE,
            )
        """
        )

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
        self.cursor.execute(f"DELETE FROM {self.title}")
        self.cursor.executemany(
            f"INSERT INTO {self.title} (id_num, entry_content, date_updated) VALUES (?, ?, ?)",
            data.values(),
        )
        self.conn.commit()

    def close_db(self) -> None:
        self.conn.close()
