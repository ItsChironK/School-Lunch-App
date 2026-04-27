import tkinter as tk
from tkinter import messagebox

# DATA
MENU = {
    "Cheeseburger": 5.00,
    "Pizza Slice": 4.00,
    "Chicken Sandwich": 4.50,
    "Fries": 2.50,
    "Milk": 1.00,
    "Juice": 1.50,
    "Water": 1.00,
    "Apple": 1.25,
    "Salad": 3.50,
    "Brownies": 2.00
}

balance = 15.00
student = {}
order = []

# WINDOW
root = tk.Tk()
root.title("School Lunch")
root.geometry("400x700")

# PAGES
frames = {}

def show_frame(name):
    frames[name].tkraise()

# ---------------- LOGIN PAGE ----------------
login_frame = tk.Frame(root)
frames["login"] = login_frame

entries = {}

def create_input(parent, label):
    tk.Label(parent, text=label).pack()
    e = tk.Entry(parent)
    e.pack(pady=5)
    entries[label] = e

create_input(login_frame, "County")
create_input(login_frame, "School")
create_input(login_frame, "Student Name")
create_input(login_frame, "Lunch ID")

def submit():
    for key, entry in entries.items():
        if entry.get() == "":
            messagebox.showerror("Error", f"Enter {key}")
            return

    student["county"] = entries["County"].get()
    student["school"] = entries["School"].get()
    student["name"] = entries["Student Name"].get()
    student["id"] = entries["Lunch ID"].get()

    update_confirm()
    show_frame("confirm")

tk.Button(login_frame, text="Continue", command=submit).pack(pady=20)

# ---------------- CONFIRM PAGE ----------------
confirm_frame = tk.Frame(root)
frames["confirm"] = confirm_frame

info_label = tk.Label(confirm_frame, text="", justify="left")
info_label.pack(pady=20)

def update_confirm():
    text = ""
    for k, v in student.items():
        text += f"{k}: {v}\n"
    info_label.config(text=text)

tk.Button(confirm_frame, text="Looks Good", command=lambda: show_frame("menu")).pack()
tk.Button(confirm_frame, text="Edit", command=lambda: show_frame("login")).pack()

# ---------------- MENU PAGE ----------------
menu_frame = tk.Frame(root)
frames["menu"] = menu_frame

vars = {}

balance_label = tk.Label(menu_frame, text="")
balance_label.pack()

def update_balance():
    balance_label.config(text=f"Balance: ${balance:.2f}")

for item, price in MENU.items():
    var = tk.IntVar()
    vars[item] = var
    tk.Checkbutton(menu_frame, text=f"{item} - ${price}", variable=var).pack(anchor="w")

def checkout():
    global balance, order
    order = []
    total = 0

    for item, var in vars.items():
        if var.get():
            order.append(item)
            total += MENU[item]

    if not order:
        messagebox.showwarning("No Items", "Select something")
        return

    if total > balance:
        messagebox.showerror("Error", "Not enough money")
        return

    balance -= total
    update_checkout()
    show_frame("checkout")

tk.Button(menu_frame, text="Checkout", command=checkout).pack(pady=20)

# ---------------- CHECKOUT PAGE ----------------
checkout_frame = tk.Frame(root)
frames["checkout"] = checkout_frame

summary_label = tk.Label(checkout_frame, text="", justify="left")
summary_label.pack(pady=20)

def update_checkout():
    text = f"Name: {student['name']}\n\nItems:\n"
    for item in order:
        text += f"- {item}\n"
    text += f"\nRemaining Balance: ${balance:.2f}"
    summary_label.config(text=text)

tk.Button(checkout_frame, text="New Order", command=lambda: show_frame("menu")).pack()

# ---------------- SETUP ----------------
for frame in frames.values():
    frame.grid(row=0, column=0, sticky="nsew")

show_frame("login")
root.mainloop()
