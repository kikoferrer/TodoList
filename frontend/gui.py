import tkinter as tk


window = tk.Tk()
window.title("Todo List")

input_frame = tk.Frame(master=window, width=50, height=50, bg="red")
input_frame.pack(fill=tk.X, side=tk.BOTTOM)

button_frame = tk.Frame(master=window, width=50, height=50, bg="green")
button_frame.pack(fill=tk.X, side=tk.BOTTOM)

main_frame = tk.Frame(master=window, width=800, height=500, bg="blue")
main_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)


window.mainloop()
