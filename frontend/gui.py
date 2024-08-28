import tkinter as tk
import os
import json
import signal
import atexit
from frontend.api_requests import FrontendRequests


class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List")
        self.root.geometry("1280x720")

        self.bg = "#181818"
        self.fg = "#EFEFEF"
        self.selected_bg = "#4A4A4A"
        self.selected_fg = "#ffffff"
        self.btn_bg = "#383838"

        self.list_file = "frontend/list_items.json"

        self.req = FrontendRequests()

        self.main_frame = tk.Frame(master=self.root, width=1280, height=720, bg=self.bg)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.window_frame = tk.Frame(
            master=self.main_frame, width=50, height=50, bg=self.btn_bg
        )
        self.window_frame.pack(padx=5, pady=5, fill=tk.BOTH, side=tk.TOP, expand=True)

        self.button_frame = tk.Frame(
            master=self.main_frame, width=50, height=50, bg=self.bg
        )
        self.button_frame.pack(padx=5, fill=tk.X, side=tk.BOTTOM)

        self.list_button = tk.Button(
            self.button_frame,
            text="Select List Name",
            command=self.list_names,
            bg=self.btn_bg,
            fg=self.fg,
            border=0,
            activebackground=self.selected_bg,
            activeforeground=self.selected_fg,
        )
        self.list_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.list_label_var = tk.StringVar()
        self.list_label = tk.Label(
            self.button_frame, textvariable=self.list_label_var, bg=self.bg, fg=self.fg
        )
        self.list_label.pack(side=tk.RIGHT, padx=5, pady=5)

        self.list_label_var.trace("w", self.monitor_label)

        self.menu = tk.Menu(
            self.root,
            tearoff=False,
            bg=self.btn_bg,
            fg=self.fg,
            relief=tk.FLAT,
            border=0,
            activebackground=self.selected_bg,
            activeforeground=self.selected_fg,
            activeborderwidth=0,
        )
        self.menu_item = tk.Menu(
            self.menu,
            tearoff=False,
            bg=self.btn_bg,
            fg=self.fg,
            relief=tk.FLAT,
            border=0,
            activebackground=self.selected_bg,
            activeforeground=self.selected_fg,
            activeborderwidth=0,
        )

        self.menu_item.add_command(label="Settings", command=self.settings)
        self.menu_item.add_command(label="Exit", command=self.exit_window)

        self.menu.add_cascade(label="Options", menu=self.menu_item)
        self.root.config(menu=self.menu)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_window)
        atexit.register(self.exit_window)
        signal.signal(signal.SIGINT, self.exit_on_signal)
        signal.signal(signal.SIGTERM, self.exit_on_signal)
        signal.signal(signal.SIGABRT, self.exit_on_signal)
        signal.signal(signal.SIGSEGV, self.exit_on_signal)
        signal.signal(signal.SIGBUS, self.exit_on_signal)
        signal.signal(signal.SIGFPE, self.exit_on_signal)
        signal.signal(signal.SIGILL, self.exit_on_signal)

    def clear_list(self):
        for widget in self.window_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

    def add_entry(self, text):
        self.req.add_entry(text)
        self.display_list()

    def update_item(self, id_num, text):
        self.req.update_entry(id_num, text)
        self.display_list()

    def delete_item(self, id_num):
        self.req.delete(id_num)
        self.display_list()

    def display_list(self):
        self.clear_list()
        get_list = self.req.get()
        for key, value in get_list.items():
            id_num = value["id_num"]
            entry = value["entry_content"]
            date = value["date_updated"]

            entry_frame = tk.Frame(
                self.window_frame,
                bg=self.bg,
            )
            entry_frame.pack(padx=5, pady=5, fill=tk.X, side=tk.TOP)

            text_var = tk.StringVar()
            text_var.set(f"{id_num}. {entry} - {date} (last date updated)")
            label = tk.Label(
                entry_frame,
                textvariable=text_var,
                bg=self.bg,
                fg=self.fg,
            )
            label.pack(side=tk.LEFT)

            update_btn = tk.Button(
                entry_frame,
                text="Update",
                command=lambda id_num=id_num: self.open_entry_window(id_num),
                bg=self.btn_bg,
                fg=self.fg,
                border=0,
                activebackground=self.selected_bg,
                activeforeground=self.selected_fg,
            )
            delete_btn = tk.Button(
                entry_frame,
                text="Delete",
                command=lambda id_num=id_num: self.delete_item(id_num),
                bg=self.btn_bg,
                fg=self.fg,
                border=0,
                activebackground=self.selected_bg,
                activeforeground=self.selected_fg,
            )
            update_btn.pack(side=tk.RIGHT, padx=5)
            delete_btn.pack(side=tk.RIGHT, padx=5)

        entry_frame = tk.Frame(
            self.window_frame,
            bg=self.bg,
        )
        entry_frame.pack(padx=5, pady=5, fill=tk.X, side=tk.TOP)

        create_btn = tk.Button(
            entry_frame,
            text="+",
            command=self.open_entry_window,
            bg=self.btn_bg,
            fg=self.fg,
            border=0,
            activebackground=self.selected_bg,
            activeforeground=self.selected_fg,
        )
        create_btn.pack(pady=5, padx=5, side=tk.LEFT)

    def open_entry_window(self, id_num=None):
        entry_window = tk.Toplevel(self.root, bg=self.bg)
        entry_window.title("Enter your Entry")

        entry_label = tk.Label(
            entry_window, text="Enter your entry here: ", bg=self.bg, fg=self.fg
        )
        entry_label.pack(side=tk.LEFT, padx=10, pady=5)

        entry_field = tk.Entry(entry_window, bg=self.selected_bg, fg=self.fg)
        entry_field.pack(side=tk.LEFT, pady=5)

        def submit_entry():
            entered_text = entry_field.get()
            if id_num is None:
                self.add_entry(entered_text)
            else:
                self.update_item(id_num, entered_text)
            entry_window.destroy()

        submit_button = tk.Button(
            entry_window,
            text="Submit",
            command=submit_entry,
            bg=self.btn_bg,
            fg=self.fg,
            border=0,
            activebackground=self.selected_bg,
            activeforeground=self.selected_fg,
        )
        submit_button.pack(side=tk.LEFT, padx=10, pady=5)

    def list_names(self):
        list_window = tk.Toplevel(self.root, bg=self.bg)
        list_window.title("List Names")

        listbox = tk.Listbox(list_window, bg=self.selected_bg, fg=self.fg)
        listbox.pack(padx=10, pady=10)

        if os.path.exists(self.list_file):
            with open(self.list_file, "r") as f:
                list_items = json.load(f)
                listbox.delete(0, tk.END)
                for item in list_items:
                    listbox.insert(tk.END, item)
        else:
            list_items = []

        def add_to_list():
            item = list_entry.get().strip()
            if item:
                listbox.insert(tk.END, item)
                list_entry.delete(0, tk.END)
                list_items.append(item)
                with open(self.list_file, "w") as f:
                    json.dump(list_items, f)

        def update_label():
            selected_index = listbox.curselection()
            if selected_index:
                selected_item = listbox.get(selected_index)
                self.list_label_var.set(selected_item)
            list_window.destroy()

        list_entry = tk.Entry(list_window, bg=self.selected_bg, fg=self.fg)
        list_entry.pack(padx=10, pady=10)

        list_btn = tk.Button(
            list_window,
            text="+",
            command=add_to_list,
            bg=self.btn_bg,
            fg=self.fg,
            border=0,
            activebackground=self.selected_bg,
            activeforeground=self.selected_fg,
        )
        list_btn.pack(padx=10, pady=10)

        update_btn = tk.Button(
            list_window,
            text="Select",
            command=update_label,
            bg=self.btn_bg,
            fg=self.fg,
            border=0,
            activebackground=self.selected_bg,
            activeforeground=self.selected_fg,
        )
        update_btn.pack(padx=10, pady=10)

    def monitor_label(self, *args):
        self.req.get_table(self.list_label_var.get())
        self.display_list()

    def settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x200")

        tk.Label(settings_window, text="Settings window").pack()

    def exit_window(self):
        self.req.shutdown()
        self.root.destroy()

    def exit_on_signal(self, sig, frame):
        self.req.shutdown()
        self.root.destroy()
