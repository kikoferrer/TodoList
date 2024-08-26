from fastapi import FastAPI
from backend.database import Database
import datetime


app = FastAPI()

title = input("Enter todo list title: ")
db = Database(title)

todo_cache = db.extract_table()


@app.post("/entries")
def create_entry(entry: str) -> dict[str, dict]:
    if todo_cache:
        next_index = max(todo_cache.keys()) + 1
    else:
        next_index = 1

    new_entry = {
        "id_num": next_index,
        "entry_content": entry,
        "date_updated": datetime.date.today(),
    }

    todo_cache[next_index] = new_entry
    return {"message": new_entry}


@app.get("/entries")
def show_list() -> dict[int, dict]:
    return todo_cache


@app.get("/entries/{entry_id}")
def show_entry(entry_id: int) -> dict[int, dict]:
    pass


@app.put("/entries/{entry_id}")
def update_entry(entry_id: int):
    pass


@app.delete("/entries/{entry_id}")
def delete_entry(entry_id: int):
    pass
