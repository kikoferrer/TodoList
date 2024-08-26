from fastapi import FastAPI
from database import Database
import datetime
import os


app = FastAPI()

db = None
todo_cache = {}


def reenumerate_cache(todo_cache):
    todo = {}
    for i, entry in enumerate(todo_cache.values(), start=1):
        entry["id_num"] = i
        todo[i] = entry
    return todo


@app.post("/tables")
async def choose_database(title_payload: dict):
    global db
    global todo_cache
    title = title_payload["message"]
    db = Database(title.lower())
    db.create_table()
    todo_cache = db.extract_table()


@app.post("/entries")
async def create_entry(entry_payload: dict) -> dict:
    entry = entry_payload["message"]
    if todo_cache:
        next_index = max(todo_cache.keys()) + 1
    else:
        next_index = 1

    new_entry = {
        "id_num": next_index,
        "entry_content": entry,
        "date_updated": str(datetime.date.today()),
    }

    todo_cache[next_index] = new_entry
    response = f"New item entered at id {next_index}"
    return {"message": response}


@app.get("/entries")
async def show_list() -> dict:
    if not todo_cache:
        return todo_cache
    else:
        todo_list = reenumerate_cache(todo_cache)
        db.save_entries_to_db(todo_list)
        return todo_list


@app.get("/entries/{entry_id}")
async def show_entry(entry_id: int) -> dict:
    entry = todo_cache[entry_id]
    return entry


@app.put("/entries/{entry_id}")
async def update_entry(entry_id: int, entry_payload: dict) -> dict:
    entry = entry_payload["message"]
    entry_num = todo_cache[entry_id]
    entry_num["entry_content"] = entry
    entry_num["date_updated"] = str(datetime.date.today())
    response = f"entry {entry_id} updated to: {entry}"
    return {"message": response}


@app.delete("/entries/{entry_id}")
async def delete_entry(entry_id: int):
    todo_cache.pop(entry_id)


@app.post("/shutdown")
async def save_to_database() -> dict:
    db.close_db()
    os.system("pkill uvicorn")
    return {"message": "Server Shutdown"}
