from fastapi import FastAPI

app = FastAPI()


@app.post("/entries")
def create_entry(entry: str):
    pass


@app.get("/entries")
def show_list() -> dict[str,]:
    pass


@app.get("/entries/{entry_id}")
def show_entry(entry_id: int):
    pass


@app.put("/entries/{entry_id}")
def update_entry(entry_id: int):
    pass


@app.delete("/entries/{entry_id}")
def delete_entry(entry_id: int):
    pass
