import tkinter as tk
from tkinter import messagebox
import qrcode
import uuid
import json
from pathlib import Path

def generate_qr(data, filename, folder):
    folder.mkdir(parents=True, exist_ok=True) 
    qr_data = json.dumps(data)
    img = qrcode.make(qr_data)
    img.save(folder / f"{filename}.png")       

def update_team_field(*args):
    if role_var.get().lower() == "participant":
        label_team.pack()
        entry_team.pack()
    else:
        label_team.pack_forget()
        entry_team.pack_forget()

def on_submit():
    name = entry_name.get().strip()
    role = role_var.get().capitalize()

    if not name or role not in ["Participant", "Organizer", "Volunteer"]:
        messagebox.showerror("Error", "Please provide a valid name and select a role.")
        return

    user_id = str(uuid.uuid4())[:8]
    data = {"user_id": user_id, "name": name, "role": role}

    if role == "Participant":
        team = entry_team.get().strip()
        if not team:
            messagebox.showerror("Error", "Participant must enter a team name.")
            return
        data["team"] = team

    save_path = Path.home() / "Documents" / "qrs"
    generate_qr(data, user_id, save_path)
    messagebox.showinfo("Success", f"QR code saved in {save_path}.")

root = tk.Tk()
root.title("Generate QR Code")
root.geometry("400x300")
root.config(bg="#f0f0f0")

tk.Label(root, text="Name:").pack()
entry_name = tk.Entry(root, width=40)
entry_name.pack()

tk.Label(root, text="Role:").pack()
role_var = tk.StringVar()
role_var.set("Participant")
role_menu = tk.OptionMenu(root, role_var, "Participant", "Organizer", "Volunteer")
role_menu.pack()
role_var.trace_add("write", update_team_field)

label_team = tk.Label(root, text="Team Name (if participant):")
entry_team = tk.Entry(root, width=40)

# Initially show team field because default is "Participant"
label_team.pack()
entry_team.pack()

tk.Button(root, text="Generate QR", command=on_submit).pack(pady=10)
root.mainloop()
