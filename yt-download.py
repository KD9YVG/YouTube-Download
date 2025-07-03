import tkinter as tk
import os
from tkinter import messagebox


root = tk.Tk()
root.title("Youtube Downloader")
root.geometry("600x400")

# Try to detect dark mode (macOS)
import platform
def is_dark_mode():
    if platform.system() == "Darwin":
        try:
            import subprocess
            result = subprocess.run([
                'defaults', 'read', '-g', 'AppleInterfaceStyle'
            ], capture_output=True, text=True)
            return 'Dark' in result.stdout
        except Exception:
            return False
    return False

dark_mode = is_dark_mode()






# URL label
url_label = tk.Label(root, text="URL:")
url_label.pack(pady=(20, 5))

# URL entry field
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

# Output text field (large, un-editable)
output_text = tk.Text(root, height=12, width=70, state='disabled', wrap='word', bg='black', fg='white', insertbackground='white')
output_text.pack(pady=10)

import subprocess

def download_action():
    url = url_entry.get()
    if not url.strip():
        messagebox.showerror("Error", "URL field cannot be empty.")
        return
    # Clear previous output
    output_text.config(state='normal')
    output_text.delete(1.0, tk.END)
    output_text.config(state='disabled')
    # Run yt-dlp and capture output
    try:
        process = subprocess.Popen(
            ['yt-dlp', '-f', 'mp4', url],
            cwd='/Users/southbrookkids/Desktop/New Assets',
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        for line in process.stdout:
            output_text.config(state='normal')
            output_text.insert(tk.END, line)
            output_text.see(tk.END)
            output_text.config(state='disabled')
        process.wait()
    except Exception as e:
        output_text.config(state='normal')
        output_text.insert(tk.END, f"Error: {e}\n")
        output_text.config(state='disabled')

# Download button
download_button = tk.Button(
    root,
    text="Download",
    command=download_action
)
download_button.pack(pady=20)

root.mainloop()

