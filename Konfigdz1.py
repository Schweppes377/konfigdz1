import os
import tarfile
import time
import csv
import tkinter as tk
from datetime import datetime

current_path = ""
start_time = time.time()


def log_command(command, log_file):
    with open(log_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), command])


def execute_command(command, tar_path, log_file):
    global current_path, start_time
    result = ""

    with tarfile.open(tar_path, 'r') as tar:
        if command == "ls":
            members = [member for member in tar.getmembers() if
                       member.name.startswith(current_path.lstrip('/')) and member.name != current_path]
            unique_entries = set()
            for member in members:
                relative_path = member.name[len(current_path):].lstrip('/')
                first_part = relative_path.split('/')[0]
                unique_entries.add(first_part)
            result = "\n".join(sorted(unique_entries)) if unique_entries else "Directory is empty"
        elif command.startswith("cd "):
            new_path = command.split(" ", 1)[1].strip()
            if new_path == "/":
                current_path = ""
            elif new_path == "..":
                current_path = "/".join(current_path.strip("/").split("/")[:-1]) or ""
            else:
                full_new_path = os.path.join(current_path, new_path).replace("\\", "/")
                valid_directories = set(member.name for member in tar.getmembers() if member.isdir())
                if full_new_path in valid_directories:
                    current_path = full_new_path
                else:
                    result = "No such directory"
        elif command == "pwd":
            result = current_path or "/"
        elif command == "du":
            total_size = sum(member.size for member in tar.getmembers() if member.name.startswith(current_path))
            result = f"Disk usage: {total_size} bytes"
        elif command == "uptime":
            elapsed_time = time.time() - start_time
            result = f"Uptime: {elapsed_time:.2f} seconds"
        elif command == "exit":
            result = "Exiting emulator..."
            return result
        else:
            result = f"Unknown command: {command}"

    log_command(command, log_file)
    return result


def on_submit(command_entry, output_text, tar_path, log_file):
    command = command_entry.get()
    output = execute_command(command, tar_path, log_file)
    if output == "Exiting emulator...":
        output_text.insert(tk.END, f"$ {command}\n{output}\n\n")
        output_text.update()
        output_text.after(1000, root.destroy)
    else:
        output_text.insert(tk.END, f"$ {command}\n{output}\n\n")
    command_entry.delete(0, tk.END)


def create_gui(tar_file_path, log_file_path):
    global root
    root = tk.Tk()
    root.title("Shell Emulator")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    output_text = tk.Text(frame, width=80, height=20, wrap=tk.WORD)
    output_text.pack(padx=5, pady=5)

    command_entry = tk.Entry(frame, width=80)
    command_entry.pack(padx=5, pady=5)
    command_entry.bind("<Return>", lambda event: on_submit(command_entry, output_text, tar_file_path, log_file_path))

    submit_button = tk.Button(frame, text="Submit",
                              command=lambda: on_submit(command_entry, output_text, tar_file_path, log_file_path))
    submit_button.pack(pady=5)

    root.mainloop()


def run_emulator(tar_file_path, log_file_path):
    create_gui(tar_file_path, log_file_path)


# Функция для тестов
def execute_command_for_test(command, tar_path):
    global current_path, start_time
    log_file = "test_log.csv"
    return execute_command(command, tar_path, log_file)


if __name__ == "__main__":
    import sys

    TAR_FILE = 'filesystem.tar'
    LOG_FILE = 'logfile.csv'

    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <path_to_tar_file> <path_to_log_file>")
        print("Using default files: filesystem.tar and logfile.csv")
        run_emulator(TAR_FILE, LOG_FILE)
    else:
        tar_file = sys.argv[1]
        log_file = sys.argv[2]
        run_emulator(tar_file, log_file)
