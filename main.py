import subprocess
import time
import tkinter as tk
from frontend.gui import TodoListApp


if __name__ == "__main__":
    subprocess.Popen(["uvicorn", "api:app", "--reload"], cwd="backend/")
    time.sleep(1)
    root = tk.Tk()
    TodoListApp(root)
    root.mainloop()
