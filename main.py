import pyperclip
from tkinter import *
from tkinter import ttk
from file_handling import handle_file, write_to_file, test_path


def center(window: Tk, width, height):
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

root = Tk()
root.title("Cipher")
center(root, 600, 600)

frm = ttk.Frame(root, height=600, width=600)
frm.pack()

title_font = ("DroidSansMono NF Regular", 40)

info = {
    "mode": None,
    "path": None
}

def get_mode():
    # Clear frame
    for widget in frm.winfo_children():
        widget.destroy()

    ttk.Label(frm, text="Select mode", font=title_font).place(relx=0.5, y=100, anchor="center")
    ttk.Button(frm, text="Cipher",   command=lambda: get_path("cipher"  )).place(relx=0.4, y=200, anchor="center", height=50)
    ttk.Button(frm, text="Decipher", command=lambda: get_path("decipher")).place(relx=0.6, y=200, anchor="center", height=50)


def get_path(mode: str):
    info["mode"] = mode

    # Clear frame
    for widget in frm.winfo_children():
        widget.destroy()

    # Label and Entry
    ttk.Label(frm, text="Enter path to file", font=title_font).place(relx=0.5, y=100, anchor="center")

    file_entry = ttk.Entry(frm, width=25, font=("DroidSansMono NF Regular", 20))
    file_entry.place(relx=0.5, y=200, anchor="center")
    file_entry.focus()  # set cursor onto Entry

    feedback = ttk.Label(frm, text="", font=("DroidSansMono NF Regular", 14))
    feedback.place(relx=0.5, y=260, anchor="center")

    def on_enter(event=None):
        path = file_entry.get().strip().strip('"')
        if test_path(path):
            get_key(path)
        else:
            feedback.config(text="File not found. Try again.", foreground="red")
            file_entry.delete(0, END)

    # Bind Enter key
    file_entry.bind("<Return>", on_enter)

    # Submit button
    ttk.Button(frm, text="Submit", command=on_enter).place(relx=0.5, y=320, anchor="center", height=40)

    # Return button
    ttk.Button(frm, text="Return", command=lambda: get_mode()).place(relx=0.5, y = 360, anchor="center")


def get_key(path: str):
    info["path"] = path
    
    # Clear frame
    for widget in frm.winfo_children():
        widget.destroy()

    ttk.Label(frm, text="Enter key", font=title_font).place(relx=0.5, y=90, anchor="center")
    ttk.Label(frm, text="used for random sequence", font=("DroidSansMono NF Regular", 20)).place(relx=0.5, y=140, anchor="center")

    key_entry = ttk.Entry(frm, width=25, font=("DroidSansMono NF Regular", 20))
    key_entry.place(relx=0.5, y=200, anchor="center")
    key_entry.focus()  # set cursor to Entry

    feedback = ttk.Label(frm, text="", font=("DroidSansMono NF Regular", 14))
    feedback.place(relx=0.5, y=260, anchor="center")

    def on_enter(event=None):
        key = key_entry.get().strip()
        display_result(key)

    # Bind Enter key
    key_entry.bind("<Return>", on_enter)

    # Submit button
    ttk.Button(frm, text="Submit", command=on_enter).place(relx=0.5, y=320, anchor="center", height=40)

    # Return button
    ttk.Button(frm, text="Return", command=lambda: get_path(info["mode"])).place(relx=0.5, y=360, anchor="center")
    

def display_result(tkey: str, tmode=None, tpath=None):
    for widget in frm.winfo_children():
        widget.destroy()

    mode = info["mode"] if not tmode else tmode
    path = info["path"] if not tpath else tpath
    key = tkey
    
    finished_content = handle_file(path, key, mode)

    # Option menu (Overwrite, return to start, exit)
    # Menu button
    option_button = Menubutton(frm, text="Options  ", font=("DroidSansMono NF Regular", 20))
    option_button.place(relx=0.85, y=50, anchor="center")

    option_menu = Menu(option_button, tearoff=0)
    option_menu.add_command(label="Overwrite", command=lambda: write_to_file(info["path"], finished_content))
    option_menu.add_command(label="Copy", command=lambda: pyperclip.copy(finished_content))
    option_menu.add_command(label="Return to start", command=get_mode)
    option_menu.add_command(label="Exit", command=root.destroy)

    option_button.config(menu=option_menu)

    # Title label
    ttk.Label(frm, text="Result", font=title_font).pack(padx=0, pady=(20, 10))

    # Scrollbar
    scrollbar = ttk.Scrollbar(frm)
    scrollbar.place(x=10, y=140)
    
    text_widget = Text(
        frm,
        wrap="word",
        yscrollcommand=scrollbar.set,
        font=("DroidSansMono NF Regular", 12)
    )

    text_widget.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=text_widget.yview)

    # Insert content
    text_widget.insert("1.0", finished_content)

    text_widget.config(state="disabled") # stop writing to scrollbar

get_mode()
root.mainloop()