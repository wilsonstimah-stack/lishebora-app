import tkinter as tk
from tkinter import ttk
import os
import subprocess
import sys
from backend_manager import ServerBackend
from common_utils import ROLE_DEVELOPER

def setup_demo():
    # Ensure DBs exist
    server = ServerBackend()
    
    # Check if we need to create a default admin
    conn = server.db.get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE role=?", (ROLE_DEVELOPER,))
    if not c.fetchone():
        print("Creating default Developer account...")
        server.register_user("admin@lishebora.ke", "0700000000", "admin123", ROLE_DEVELOPER, "adult")
    conn.close()

class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LisheBora System Launcher")
        self.geometry("300x250")
        
        ttk.Label(self, text="Select App to Launch", font=("Arial", 14, "bold")).pack(pady=20)
        
        ttk.Button(self, text="Client App (Patient)", command=self.launch_client).pack(fill="x", padx=20, pady=10)
        ttk.Button(self, text="Developer App (Nutritionist)", command=self.launch_dev).pack(fill="x", padx=20, pady=10)
        
        ttk.Label(self, text="Default Dev Login:\nadmin@lishebora.ke | admin123", font=("Arial", 8), foreground="gray").pack(side="bottom", pady=10)

    def launch_client(self):
        subprocess.Popen([sys.executable, "client_app.py"])

    def launch_dev(self):
        subprocess.Popen([sys.executable, "developer_app.py"])

if __name__ == "__main__":
    setup_demo()
    app = Launcher()
    app.mainloop()
