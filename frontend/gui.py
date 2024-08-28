import tkinter as tk
import os
import json
from api_requests import FrontendRequests

bg = "#181818"
fg = "#EFEFEF"
selected_bg = "#4A4A4A"
selected_fg = "#ffffff"
btn_bg = "#383838"

list_file = "list_items.json"

window = tk.Tk()
window.title("Todo List")
window.geometry("1280x720")

req = FrontendRequests()

main_frame = tk.Frame(master=window, width=1280, height=720, bg=bg)
main_frame.pack(fill=tk.BOTH, expand=True)

window_frame = tk.Frame(master=main_frame, width=50, height=50, bg=btn_bg)
window_frame.pack(padx=5, pady=5, fill=tk.BOTH, side=tk.TOP, expand=True)


def clear_list():
    for widget in window_frame.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()


def add_entry(text):
    req.add_entry(text)
    display_list()


def update_item(id_num, text):
    req.update_entry(id_num, text)
    display_list()


def delete_item(id_num):
    req.delete(id_num)
    display_list()


def display_list():
    clear_list()
    get_list = req.get()
    for key, value in get_list.items():
        id_num = value["id_num"]
        entry = value["entry_content"]
        date = value["date_updated"]

        entry_frame = tk.Frame(
            window_frame,
            bg=bg,
        )
        entry_frame.pack(padx=5, pady=5, fill=tk.X, side=tk.TOP)

        text_var = tk.StringVar()
        text_var.set(f"{id_num}. {entry} - {date} (last date updated)")
        label = tk.Label(
            entry_frame,
            textvariable=text_var,
            bg=bg,
            fg=fg,
        )
        label.pack(side=tk.LEFT)

        update_btn = tk.Button(
            entry_frame,
            text="Update",
            command=lambda id_num=id_num: open_entry_window(id_num),
            bg=btn_bg,
            fg=fg,
            border=0,
            activebackground=selected_bg,
            activeforeground=selected_fg,
        )
        delete_btn = tk.Button(
            entry_frame,
            text="Delete",
            command=lambda id_num=id_num: delete_item(id_num),
            bg=btn_bg,
            fg=fg,
            border=0,
            activebackground=selected_bg,
            activeforeground=selected_fg,
        )
        update_btn.pack(side=tk.RIGHT, padx=5)
        delete_btn.pack(side=tk.RIGHT, padx=5)

    entry_frame = tk.Frame(
        window_frame,
        bg=bg,
    )
    entry_frame.pack(padx=5, pady=5, fill=tk.X, side=tk.TOP)

    create_btn = tk.Button(
        entry_frame,
        text="+",
        command=open_entry_window,
        bg=btn_bg,
        fg=fg,
        border=0,
        activebackground=selected_bg,
        activeforeground=selected_fg,
    )
    create_btn.pack(pady=5, padx=5, side=tk.LEFT)


button_frame = tk.Frame(master=main_frame, width=50, height=50, bg=bg)
button_frame.pack(padx=5, fill=tk.X, side=tk.BOTTOM)


def open_entry_window(id_num=None):
    entry_window = tk.Toplevel(window, bg=bg)
    entry_window.title("Enter your Entry")

    entry_label = tk.Label(entry_window, text="Enter your entry here: ", bg=bg, fg=fg)
    entry_label.pack(side=tk.LEFT, padx=10, pady=5)

    entry_field = tk.Entry(entry_window, bg=selected_bg, fg=fg)
    entry_field.pack(side=tk.LEFT, pady=5)

    def submit_entry():
        entered_text = entry_field.get()
        if id_num is None:
            add_entry(entered_text)
        else:
            update_item(id_num, entered_text)
        entry_window.destroy()

    submit_button = tk.Button(
        entry_window,
        text="Submit",
        command=submit_entry,
        bg=btn_bg,
        fg=fg,
        border=0,
        activebackground=selected_bg,
        activeforeground=selected_fg,
    )
    submit_button.pack(side=tk.LEFT, padx=10, pady=5)


def list_names():
    list_window = tk.Toplevel(window, bg=bg)
    list_window.title("List Names")

    listbox = tk.Listbox(list_window, bg=selected_bg, fg=fg)
    listbox.pack(padx=10, pady=10)

    if os.path.exists(list_file):
        with open(list_file, "r") as f:
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
            with open(list_file, "w") as f:
                json.dump(list_items, f)

    def update_label():
        selected_index = listbox.curselection()
        if selected_index:
            selected_item = listbox.get(selected_index)
            list_label_var.set(selected_item)
        list_window.destroy()

    list_entry = tk.Entry(list_window, bg=selected_bg, fg=fg)
    list_entry.pack(padx=10, pady=10)

    list_btn = tk.Button(
        list_window,
        text="+",
        command=add_to_list,
        bg=btn_bg,
        fg=fg,
        border=0,
        activebackground=selected_bg,
        activeforeground=selected_fg,
    )
    list_btn.pack(padx=10, pady=10)

    update_btn = tk.Button(
        list_window,
        text="Select",
        command=update_label,
        bg=btn_bg,
        fg=fg,
        border=0,
        activebackground=selected_bg,
        activeforeground=selected_fg,
    )
    update_btn.pack(padx=10, pady=10)


list_button = tk.Button(
    button_frame,
    text="Select List Name",
    command=list_names,
    bg=btn_bg,
    fg=fg,
    border=0,
    activebackground=selected_bg,
    activeforeground=selected_fg,
)
list_button.pack(side=tk.RIGHT, padx=5, pady=5)

list_label_var = tk.StringVar()
list_label = tk.Label(button_frame, textvariable=list_label_var, bg=bg, fg=fg)
list_label.pack(side=tk.RIGHT, padx=5, pady=5)


def monitor_label(*args):
    req.get_table(list_label_var.get())
    display_list()


list_label_var.trace("w", monitor_label)


def settings():
    settings_window = tk.Toplevel(window)
    settings_window.title("Settings")
    settings_window.geometry("300x200")

    tk.Label(settings_window, text="Settings window").pack()


def exit_window():
    window.destroy()


menu = tk.Menu(
    window,
    tearoff=False,
    bg=btn_bg,
    fg=fg,
    relief=tk.FLAT,
    border=0,
    activebackground=selected_bg,
    activeforeground=selected_fg,
    activeborderwidth=0,
)
menu_item = tk.Menu(
    menu,
    tearoff=False,
    bg=btn_bg,
    fg=fg,
    relief=tk.FLAT,
    border=0,
    activebackground=selected_bg,
    activeforeground=selected_fg,
    activeborderwidth=0,
)

menu_item.add_command(label="Settings", command=settings)
menu_item.add_command(label="Exit", command=exit_window)


menu.add_cascade(label="Options", menu=menu_item)
window.config(menu=menu)

window.mainloop()
