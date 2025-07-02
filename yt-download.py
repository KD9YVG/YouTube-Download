import tkinter as tk
import os
from tkinter import messagebox

root = tk.Tk()
root.title("Youtube Downloader")
root.geometry("400x300")

# URL label
url_label = tk.Label(root, text="URL:")
url_label.pack(pady=(40, 5))

# URL entry field
url_entry = tk.Entry(root, width=40)
url_entry.pack(pady=5)

def download_action():
    url = url_entry.get()
    if not url.strip():
        messagebox.showerror("Error", "URL field cannot be empty.")
        return
    os.system('cd / && cd Users/southbrookkids/Desktop/New Assets')
    os.system(f'yt-dlp -f mp4 "{url}"')

# Download button
download_button = tk.Button(root, text="Download", command=download_action)
download_button.pack(pady=20)

root.mainloop()

