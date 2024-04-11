import tkinter as tk
import pyperclip
import hashlib

def generate_license_key():
    # Get the virtual ID from the entry field
    virtual_id = virtual_id_entry.get()
    
    # Calculate the license key using SHA-256 hash
    hash_object = hashlib.sha256(virtual_id.encode())
    license_key = hash_object.hexdigest()[:16]
    
    # Update the license key label with the generated key
    license_key_label.config(text=f"Generated License Key: {license_key}")

def copy_license_key():
    # Extract the license key from the label text
    license_key = license_key_label.cget("text").split(": ")[1]
    
    # Copy the license key to the clipboard
    pyperclip.copy(license_key)

# Create the main window
root = tk.Tk()
root.title("License Key Generator")

# Set window size and position it in the center
window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Set background color and font
root.config(bg="#f0f0f0")
root.option_add("*Font", "Arial 12")

# Create and pack widgets
virtual_id_label = tk.Label(root, text="Enter Virtual ID:")
virtual_id_label.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="w")

virtual_id_entry = tk.Entry(root)
virtual_id_entry.grid(row=0, column=1, padx=10, pady=(20, 5))

generate_button = tk.Button(root, text="Generate License Key", command=generate_license_key)
generate_button.grid(row=1, column=0, columnspan=2, pady=10)

license_key_label = tk.Label(root, text="", wraplength=300, justify="left")
license_key_label.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 5))

copy_button = tk.Button(root, text="Copy License Key to Clipboard", command=copy_license_key)
copy_button.grid(row=3, column=0, columnspan=2, pady=10)

# Run the GUI
root.mainloop()

