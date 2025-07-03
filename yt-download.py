
import tkinter as tk
import os
from tkinter import messagebox

# Set the output path here
OUTPUT_PATH = '/Users/brayden/Desktop'


root = tk.Tk()
root.title("Youtube Downloader")
root.geometry("600x400")
## Output path on line 77 "cwd"

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


# File name label and entry
filename_label = tk.Label(root, text="File Name:")
filename_label.pack(pady=(10, 2))
filename_entry = tk.Entry(root, width=60)
filename_entry.pack(pady=2)

# Output text field (large, un-editable)
output_text = tk.Text(root, height=12, width=70, state='disabled', wrap='word', bg='black', fg='white', insertbackground='white')
output_text.pack(pady=10)

import subprocess

def download_action():
    url = url_entry.get()
    filename = filename_entry.get().strip()
    if not url.strip():
        messagebox.showerror("Error", "URL field cannot be empty.")
        return
    if not filename:
        messagebox.showerror("Error", "File name field cannot be empty.")
        return
    # Clear previous output
    output_text.config(state='normal')
    output_text.delete(1.0, tk.END)
    output_text.config(state='disabled')
    # Run yt-dlp and capture output
    try:
        # Use yt-dlp to get the output file name
        get_name_cmd = [
            'yt-dlp', '--get-filename', '-f', 'mp4', '-o', '%(title)s.%(ext)s', url
        ]
        result = subprocess.run(get_name_cmd, cwd=OUTPUT_PATH, capture_output=True, text=True)
        original_name = result.stdout.strip().split('\n')[-1]
        # Download the video
        process = subprocess.Popen(
            ['yt-dlp', '-f', 'mp4', '-o', '%(title)s.%(ext)s', url],
            cwd=OUTPUT_PATH,
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
        # Rename the file
        import pathlib
        src = pathlib.Path(OUTPUT_PATH) / original_name
        ext = src.suffix
        dst = pathlib.Path(OUTPUT_PATH) / (filename + ext)
        if src.exists():
            src.rename(dst)
            output_text.config(state='normal')
            output_text.insert(tk.END, f"\nFile renamed to: {dst.name}\n")
            output_text.config(state='disabled')
        else:
            output_text.config(state='normal')
            output_text.insert(tk.END, f"\nError: Downloaded file not found for renaming.\n")
            output_text.config(state='disabled')
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

