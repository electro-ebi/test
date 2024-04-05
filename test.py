import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import sqlite3
import hashlib
import os
import uuid
import requests
import pyperclip  # Importing the pyperclip library

github_token ='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'
headers = {'Authorization': f'token {github_token}'}

license_key_filename = "license_key.txt"
app_version = "1.0.0"
github_repo_url = "https://api.github.com/repos/electro-ebi/Circle-radius-calculator/releases/latest"

entry = None
radius_var = None

def generate_license_key(uuid):
    hash_object = hashlib.sha256(uuid.encode())
    license_key = hash_object.hexdigest()[:16]
    #print("Generated License Key:", license_key)  # Checking
    return license_key

def evaluate_license_key(provided_key, uuid):
    generated_key = generate_license_key(uuid)
    #print("Generated License Key:", generated_key)
    #print("Provided License Key:", provided_key)
    return provided_key == generated_key

def get_virtual_id():
    virtual_id = str(uuid.getnode())
    #print("Virtual ID:", virtual_id)
    return virtual_id

def copy_to_clipboard(text):
    pyperclip.copy(text)

def calculate_radius(event=None):  
    global entry
    global radius_var
    if entry:
        diameter_str = entry.get()
        try:
            diameter = int(float(diameter_str))
            radius = diameter / 2
            radius_var.set(radius)
        except ValueError:
            radius_var.set("Invalid input")

def save_data():
    global entry
    global radius_var
    diameter_str = entry.get()
    radius_str = radius_var.get()

    try:
        diameter = int(float(diameter_str))
        radius = int(float(radius_str))

        folder_name = "user_data"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        file_path = os.path.join(folder_name, f"{diameter_str[0] + radius_str[0]}.txt")

        file_content = f"The diameter: {diameter}\nThe radius : {radius}"

        with open(file_path, "w") as file:
            file.write(file_content)

        folder_name = "user_db"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        conn = sqlite3.connect('user_db/circle_data.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS CircleData (Diameter TEXT, Radius TEXT)')
        c.execute('INSERT INTO CircleData (Diameter, Radius) VALUES (?, ?)', (diameter, radius))
        conn.commit()
        conn.close()

    except ValueError:
        radius_var.set("Invalid input")

def check_for_updates():
    try:
        response = requests.get(github_repo_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        latest_version = data["tag_name"]
        download_url = data["html_url"]  # URL to GitHub release page
        if latest_version != app_version:
            if messagebox.askyesno("Update Available", f"An update is available!\nDo you want to visit the GitHub release page to download it?"):
                os.system(f"start {download_url}")  # Open release page in default web browser
    except Exception as e:
        print(f"Error checking for updates: {e}")
        messagebox.showerror("Error", f"Error checking for updates: {e}")

def create_gui():
    global entry
    global radius_var

    root = tk.Tk()
    root.title("Circle Calculator")

    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    canvas.pack(fill="both", expand=True)

    gradient_colors = ["#832EB4", "#FD1D1D", "#FCB045"]
    for i in range(2):
        canvas.create_rectangle(0, i * root.winfo_screenheight(), root.winfo_screenwidth(), (i + 1) * root.winfo_screenheight(), fill=gradient_colors[i], width=0)

    frame = tk.Frame(canvas, bg="white", bd=5)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    diameter_label = tk.Label(frame, text="Enter the diameter:", font=("Arial", 16), bg="white")
    diameter_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    entry = tk.Entry(frame, font=("Arial", 16))
    entry.grid(row=0, column=1, padx=10, pady=10)

    radius_label = tk.Label(frame, text="Radius:", font=("Arial", 16), bg="white")
    radius_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    radius_var = tk.StringVar()
    radius_output = tk.Label(frame, textvariable=radius_var, font=("Arial", 16), bg="white")
    radius_output.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    save_button = ttk.Button(frame, text="Save", command=save_data, style='TButton', width=20)
    save_button.grid(row=2, column=0, columnspan=2, pady=20)

    check_for_updates()

    entry.bind("<KeyRelease>", lambda event: calculate_radius())

    root.mainloop()

def start():
    global entry
    global radius_var

    virtual_id = get_virtual_id()
    
    # Check for updates
    check_for_updates()
    # Copy the virtual ID to clipboard
    copy_to_clipboard(virtual_id)
    if os.path.exists(license_key_filename):
        with open(license_key_filename, "r") as file:
            license_key_file = file.read().strip()
            
        if  license_key_file == generate_license_key(virtual_id) :
            create_gui()
        elif license_key_file:
            provided_key = simpledialog.askstring("License Key", "Enter the license key virtual id will be in clipboard:")
            if provided_key is not None:
                with open(license_key_filename, "w") as file:
                        file.write(provided_key)
                if evaluate_license_key(provided_key, virtual_id):
                    create_gui()
                else:
                    messagebox.showerror("License Key", "Invalid license key. Please enter a valid license key.")
            else:
                messagebox.showerror("License Key", "No license key provided. Please enter a valid license key.")
        else:
            provided_key = simpledialog.askstring("License Key", "Enter the license key virtual id will be in clipboard:")
            if provided_key is not None:
                with open(license_key_filename, "w") as file:
                    file.write(provided_key)
                if evaluate_license_key(provided_key, virtual_id):
                    create_gui()
                else:
                    messagebox.showerror("License Key", "Invalid license key. Please enter a valid license key.")
            else:
                messagebox.showerror("License Key", "No license key provided. Please enter a valid license key.")
    else:
        provided_key = simpledialog.askstring("License Key", "Enter the license key virtual id will be in clipboard:")
        if provided_key is not None:
            with open(license_key_filename, "w") as file:
                file.write(provided_key)
            if evaluate_license_key(provided_key, virtual_id):
                create_gui()
            else:
                messagebox.showerror("License Key", "Invalid license key. Please enter a valid license key.")
        
        else:
            messagebox.showerror("License Key", "No license key provided. Please enter a valid license key.")
    
    

start()
