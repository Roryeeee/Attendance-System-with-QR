import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True)
    name = Column(String)
    role = Column(String)
    team_name = Column(String, nullable=True)
    checked_in = Column(Boolean, default=False)
    checkin_time = Column(DateTime, nullable=True)

engine = create_engine('sqlite:///attendance.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def update_team_field(*args):
    if role_var.get().lower() == "participant":
        label_team.pack()
        entry_team.pack()
    else:
        label_team.pack_forget()
        entry_team.pack_forget()

def add_user():
    uid = entry_id.get().strip()
    name = entry_name.get().strip()
    role = role_var.get().lower()

    if not uid or not name or role not in ["participant", "organizer", "mentor", "evaluator"]:
        messagebox.showerror("Error", "Please fill all required fields correctly.")
        return

    if role == "participant":
        team = entry_team.get().strip()
        if not team:
            messagebox.showerror("Error", "Participants must have a team name.")
            return
    else:
        team = None

    if session.query(User).filter_by(user_id=uid).first():
        messagebox.showerror("Error", "User ID already exists.")
        return

    new_user = User(user_id=uid, name=name, role=role, team_name=team)
    session.add(new_user)
    session.commit()
    messagebox.showinfo("Success", "User added.")

def delete_user():
    uid = entry_id.get().strip()
    user = session.query(User).filter_by(user_id=uid).first()
    if user:
        session.delete(user)
        session.commit()
        messagebox.showinfo("Deleted", "User deleted.")
    else:
        messagebox.showerror("Error", "User not found.")

def reset_attendance():
    confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all check-ins?")
    if confirm:
        users = session.query(User).all()
        for user in users:
            user.checked_in = False
            user.checkin_time = None
        session.commit()
        messagebox.showinfo("Reset Complete", "All users' check-in status has been cleared.")


root = tk.Tk()
root.title("Register / Manage Users")
root.geometry("400x350")
root.config(bg="#f0f0f0")

tk.Label(root, text="User ID:").pack()
entry_id = tk.Entry(root, width=40)
entry_id.pack()

tk.Label(root, text="Full Name:").pack()
entry_name = tk.Entry(root, width=40)
entry_name.pack()

tk.Label(root, text="Role:").pack()
role_var = tk.StringVar(root)
role_var.set("participant")
role_menu = tk.OptionMenu(root, role_var, "participant", "organizer", "mentor", "evaluator")
role_menu.pack()
role_var.trace_add("write", update_team_field)

label_team = tk.Label(root, text="Team Name (if participant):")
entry_team = tk.Entry(root, width=40)

# Show team name by default since role starts as "participant"
label_team.pack()
entry_team.pack()

tk.Button(root, text="Add User", command=add_user).pack(pady=5)
tk.Button(root, text="Delete User", command=delete_user).pack(pady=5)
tk.Button(root, text="Reset Attendance", command=reset_attendance, bg="red", fg="white").pack(pady=5)

root.mainloop()
