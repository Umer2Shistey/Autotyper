"""
Author: Umer Zamir
Created on: 2024-11-13
"""

# Auto Typer
# Licensed under the MIT License
# See LICENSE file for details.

import tkinter as tk
import threading
import time
import random
import pyautogui
from keyboard import is_pressed

def type_text(text, wpm, error_rate=0.1):
    words = text.split()
    chars_per_minute = wpm * 5
    delay = 60 / chars_per_minute

    for word in words:
        if stop_typing.is_set():
            break

        for char in word + " ":
            if stop_typing.is_set():
                break

            # Simulate typing errors
            if random.random() < error_rate:
                wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
                pyautogui.write(wrong_char, interval=delay)
                time.sleep(delay)
                pyautogui.press('backspace')
                time.sleep(delay)

            pyautogui.write(char, interval=delay)
            time.sleep(delay)

def start_typing():
    stop_typing.clear()
    text = input_text.get("1.0", tk.END).strip()
    try:
        wpm = int(wpm_entry.get())
        error_rate = float(error_rate_entry.get())
    except ValueError:
        return  # Exit if inputs are invalid

    # 2-second delay to allow switching to the target window
    time.sleep(2)

    # Start typing in a separate thread
    typing_thread = threading.Thread(target=type_text, args=(text, wpm, error_rate))
    typing_thread.start()

def stop_typing_fn():
    stop_typing.set()

def monitor_keybinds():
    while True:
        if is_pressed("fn+6"):  # Start keybind
            start_typing()
        elif is_pressed("fn+7"):  # Stop keybind
            stop_typing_fn()
        time.sleep(0.1)

# Initialize Tkinter GUI
root = tk.Tk()
root.title("Typing Simulator")

# Text input area
tk.Label(root, text="Enter text to type:").pack()
input_text = tk.Text(root, height=15, width=60, wrap=tk.WORD)
input_text.pack(fill=tk.BOTH, expand=True)

# WPM entry
tk.Label(root, text="Words per minute (WPM):").pack()
wpm_entry = tk.Entry(root)
wpm_entry.insert(0, "60")
wpm_entry.pack()

# Error rate entry
tk.Label(root, text="Error rate (0 to 1):").pack()
error_rate_entry = tk.Entry(root)
error_rate_entry.insert(0, "0.1")
error_rate_entry.pack()

start_button = tk.Button(root, text="Start Typing", command=start_typing)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Typing", command=stop_typing_fn)
stop_button.pack(pady=5)

stop_typing = threading.Event()

keybind_thread = threading.Thread(target=monitor_keybinds, daemon=True)
keybind_thread.start()

# Run the Tkinter GUI loop
root.mainloop()
