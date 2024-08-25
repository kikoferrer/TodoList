from fastapi import FastAPI
from models import Entry

app = FastAPI()


entries = {
    0: Entry(name="List 1", content="first todo list", id_num=0),
    1: Entry(name="List 2", content="second todo list", id_num=1),
    2: Entry(name="List 3", content="third todo list", id_num=2),
}


@app.post("/entries")
def create_entry(entry: str):
    pass


@app.get("/entries")
def show_list() -> dict[str, dict[int, Entry]]:
    return {"entries": entries}


@app.get("/entries/{entry_id}")
def show_entry(entry_id: int):
    pass


@app.put("/entries/{entry_id}")
def update_entry(entry_id: int):
    pass


@app.delete("/entries/{entry_id}")
def delete_entry(entry_id: int):
    pass
