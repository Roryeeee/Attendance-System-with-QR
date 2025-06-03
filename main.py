import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# Helper to run another script
def run_script(script_name):
    try:
        subprocess.run([sys.executable, script_name])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run {script_name}:\n{e}")

# GUI Setup
root = tk.Tk()
root.title("Hackathon Attendance System")
root.geometry("400x300")
root.config(bg="#f0f0f0")

title = tk.Label(root, text="🛠️ Hackathon Operations", font=("Arial", 18, "bold"), bg="#f0f0f0")
title.pack(pady=20)

# Buttons
btn_generate_qr = tk.Button(root, text="📷 Generate QR Code", width=30, height=2,
                            command=lambda: run_script("QR_Generator.py"))
btn_register_user = tk.Button(root, text="📝 Register / Manage Users", width=30, height=2,
                              command=lambda: run_script("register_users.py"))
btn_attendance = tk.Button(root, text="📡 Run Attendance Scanner", width=30, height=2,
                           command=lambda: run_script("QR_code_scanning.py"))
btn_export = tk.Button(root, text="📤 Export Attendance to CSV", width=30, height=2,
                       command=lambda: run_script("export_attendence.py"))

btn_generate_qr.pack(pady=5)
btn_register_user.pack(pady=5)
btn_attendance.pack(pady=5)
btn_export.pack(pady=5)

root.mainloop()
