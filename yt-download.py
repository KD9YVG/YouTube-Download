
import tkinter as tk
import os
from tkinter import messagebox
from tkinter import ttk



import shutil

# Ensure /opt/homebrew/bin is in PATH for Homebrew detection (macOS ARM)
import sys
if sys.platform == "darwin":
    brew_path = "/opt/homebrew/bin"
    if brew_path not in os.environ.get("PATH", ""):
        os.environ["PATH"] = brew_path + ":" + os.environ.get("PATH", "")

def check_brew():
    return shutil.which('brew') is not None

def check_yt_dlp():
    yt_dlp_path = shutil.which('yt-dlp')
    return yt_dlp_path is not None

def show_loading_window(title, message, install_func):
    loading_win = tk.Toplevel(root)
    loading_win.title(title)
    loading_win.geometry("400x120")
    loading_win.resizable(False, False)
    tk.Label(loading_win, text=message, pady=10).pack()
    pb = ttk.Progressbar(loading_win, orient='horizontal', mode='indeterminate', length=350)
    pb.pack(pady=10)
    pb.start(10)

    def on_success(msg_title=None, msg_text=None):
        loading_win.destroy()
        if msg_title and msg_text:
            messagebox.showinfo(msg_title, msg_text)

    def on_error(e):
        loading_win.destroy()
        messagebox.showerror("Install Failed", f"An error occurred:\n{e}")

    def run_install():
        try:
            result = install_func()
            # If install_func returns a tuple (title, text), show info
            if isinstance(result, tuple):
                root.after(0, on_success, result[0], result[1])
            else:
                root.after(0, on_success)
        except Exception as e:
            root.after(0, on_error, e)

    import threading
    threading.Thread(target=run_install, daemon=True).start()
    loading_win.transient(root)
    loading_win.grab_set()
    root.wait_window(loading_win)


def prompt_install_brew():
    def show_brew_popup():
        popup = tk.Toplevel(root)
        popup.title("Install Homebrew")
        popup.geometry("520x340")
        popup.resizable(False, False)
        instructions = (
            "To install Homebrew, please follow these steps:\n\n"
            "1. Open the Terminal app (in Applications > Utilities).\n"
            "2. Paste the following command and press Return:\n\n"
            "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"\n\n"
            "3. Follow the on-screen instructions.\n\n"
            "IMPORTANT: At the end, read the final lines in Terminal. If it tells you to add Homebrew to your PATH, copy and paste those commands as well.\n\n"
            "4. When finished, quit and reopen this app."
        )
        label = tk.Label(popup, text=instructions, justify="left", wraplength=500, anchor="w")
        label.pack(padx=15, pady=(15, 5), fill="x")
        def copy_command():
            root.clipboard_clear()
            root.clipboard_append('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
            messagebox.showinfo("Copied!", "The install command has been copied.\nPaste it into Terminal and follow the instructions.")
        copy_btn = tk.Button(popup, text="Copy Install Command", command=copy_command)
        copy_btn.pack(pady=(5, 0))
        close_btn = tk.Button(popup, text="Close", command=popup.destroy)
        close_btn.pack(pady=(10, 15))
        popup.transient(root)
        popup.grab_set()
        root.wait_window(popup)

    install = messagebox.askyesno(
        "Homebrew Not Found",
        "Homebrew (brew) is not installed.\n\nThis app can only install Homebrew if you have access to the Terminal.\n\nWould you like instructions to install Homebrew manually?"
    )
    if install:
        show_brew_popup()
    else:
        messagebox.showwarning("Homebrew Required", "Homebrew is required to install yt-dlp. Please install it and restart the app.")

def prompt_install_yt_dlp():
    install = messagebox.askyesno(
        "yt-dlp Not Found",
        "yt-dlp is not installed.\nWould you like to install it with Homebrew now?"
    )
    if install:
        def do_install():
            import subprocess
            subprocess.run(['brew', 'install', 'yt-dlp'], check=True)
            return ("yt-dlp Installed", "yt-dlp was installed successfully.")
        show_loading_window("Installing yt-dlp", "Installing yt-dlp, please wait...", do_install)
    else:
        messagebox.showwarning("yt-dlp Required", "yt-dlp is required to download videos. Please install it and restart the app.")


root = tk.Tk()
root.title("Youtube Downloader")
root.geometry("600x550")

# Ensure the app quits when the main window is closed
def on_close():
    root.quit()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_close)


# Dependency check function to run after mainloop starts
def check_dependencies():
    if not check_yt_dlp():
        if not check_brew():
            prompt_install_brew()
        elif not check_yt_dlp():
            prompt_install_yt_dlp()



# Path to store the last used output directory
LAST_PATH_FILE = os.path.expanduser('~/.yt_downloader_last_path')

# Load last used path if it exists
def load_last_path():
    try:
        with open(LAST_PATH_FILE, 'r') as f:
            path = f.read().strip()
            if os.path.isdir(path):
                return path
    except Exception:
        pass
    return ''

OUTPUT_PATH = tk.StringVar(value=load_last_path())

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

# Output path label and entry
output_path_label = tk.Label(root, text="Output Folder:")
output_path_label.pack(pady=(15, 2))
output_path_entry = tk.Entry(root, width=60, textvariable=OUTPUT_PATH)
output_path_entry.pack(pady=2)

# Browse button for output path
from tkinter import filedialog
def browse_output_path():
    folder_selected = filedialog.askdirectory(initialdir=OUTPUT_PATH.get() or os.path.expanduser('~'), title="Select Output Folder")
    if folder_selected:
        OUTPUT_PATH.set(folder_selected)
        try:
            with open(LAST_PATH_FILE, 'w') as f:
                f.write(folder_selected)
        except Exception:
            pass
browse_button = tk.Button(root, text="Browse", command=browse_output_path)
browse_button.pack(pady=(0, 10))

# URL label
url_label = tk.Label(root, text="URL:")
url_label.pack(pady=(5, 5))

# URL entry field
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

# File name label and entry
filename_label = tk.Label(root, text="File Name:")
filename_label.pack(pady=(10, 2))
filename_entry = tk.Entry(root, width=60)
filename_entry.pack(pady=2)


# Progress bar
progress = ttk.Progressbar(root, orient='horizontal', mode='indeterminate', length=500)
progress.pack(pady=(10, 0))

# Output text field (large, un-editable)
output_text = tk.Text(root, height=12, width=70, state='disabled', wrap='word', bg='black', fg='white', insertbackground='white')
output_text.pack(pady=10)

import subprocess

import threading

def download_action():
    # Start progress bar immediately
    progress.pack(pady=(10, 0))
    progress.start(10)

    def run_download():
        # Save the output path for next time
        try:
            with open(LAST_PATH_FILE, 'w') as f:
                f.write(OUTPUT_PATH.get())
        except Exception:
            pass
        url = url_entry.get()
        filename = filename_entry.get().strip()
        if not url.strip():
            messagebox.showerror("Error", "URL field cannot be empty.")
            progress.stop()
            progress.grid_remove() if hasattr(progress, 'grid_remove') else progress.pack_forget()
            return
        if not filename:
            messagebox.showerror("Error", "File name field cannot be empty.")
            progress.stop()
            progress.grid_remove() if hasattr(progress, 'grid_remove') else progress.pack_forget()
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
            output_dir = OUTPUT_PATH.get()
            result = subprocess.run(get_name_cmd, cwd=output_dir, capture_output=True, text=True)
            if result.returncode != 0 or not result.stdout.strip():
                output_text.config(state='normal')
                output_text.insert(tk.END, "\nError: yt-dlp is not installed or not found in PATH.\nPlease ensure Homebrew and yt-dlp are installed, then quit and reopen this app.\n")
                output_text.config(state='disabled')
                progress.stop()
                progress.grid_remove() if hasattr(progress, 'grid_remove') else progress.pack_forget()
                return
            original_name = result.stdout.strip().split('\n')[-1]
            # Download the video
            process = subprocess.Popen(
                ['yt-dlp', '-f', 'mp4', '-o', '%(title)s.%(ext)s', url],
                cwd=output_dir,
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
            src = pathlib.Path(output_dir) / original_name
            ext = src.suffix
            dst = pathlib.Path(output_dir) / (filename + ext)
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
        progress.stop()
        progress.grid_remove() if hasattr(progress, 'grid_remove') else progress.pack_forget()

    threading.Thread(target=run_download, daemon=True).start()

# Download button

# Download button
download_button = tk.Button(
    root,
    text="Download",
    command=download_action
)
download_button.pack(pady=(20, 5))

# Quit button
quit_button = tk.Button(
    root,
    text="Quit",
    command=root.quit
)
quit_button.pack(pady=(0, 20))

root.after(0, check_dependencies)
root.mainloop()
