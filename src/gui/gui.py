import tkinter as tk
from tkinter import Menu

root = tk.Tk()
root.title("Menu + Left/Right Frames")
root.geometry("1200x800")

# ---------------- Menu Bar ----------------
menubar = Menu(root)
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Open")
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)
root.config(menu=menubar)

# ---------------- Main Frames ----------------
# Use a container frame for the left + right area
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew")

# Left window (resizable)
left_frame = tk.Frame(main_frame, bg="lightblue", bd=2, relief="sunken")
left_frame.grid(row=0, column=0, sticky="nsew")

# Right frame (fixed width or resizable)
right_frame = tk.Frame(
    main_frame,
    bg="lightgreen",
    bd=2,
    relief="sunken",
    width=200,
)
right_frame.grid(row=0, column=1, sticky="ns")

# ---------------- Grid Configuration ----------------
root.grid_rowconfigure(0, weight=1)  # main_frame grows vertically
root.grid_columnconfigure(0, weight=1)  # main_frame grows horizontally

main_frame.grid_rowconfigure(0, weight=1)  # left_frame grows vertically
main_frame.grid_columnconfigure(0, weight=1)  # left_frame grows horizontally
main_frame.grid_columnconfigure(1, weight=0)  # right_frame keeps fixed width

# ---------------- Example Content ----------------
tk.Label(left_frame, text="Left Window").pack(expand=True)
tk.Label(right_frame, text="Right Frame").pack(expand=True)

root.mainloop()
