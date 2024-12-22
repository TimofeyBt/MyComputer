import os
import subprocess

import pyautogui
import tkinter as tk
import keyboard
import random
import ctypes
from io import BytesIO

from plyer import notification

safer_status = False


def get_safer_status():
    return safer_status


def start_system_safer():
    global safer_status
    safer_status = True
    system_safer()


def stop_system_safer():
    global safer_status
    safer_status = False


def system_safer():
    keys = {
        '\n',
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '+',
        "delete", "enter", 'shift', 'ctrl', 'alt', 'alt_gr', 'cmd', 'win',
        'backspace', 'tab', 'space', 'esc', 'insert', 'home', 'end',
        'page_up', 'page_down',
        'up', 'down', 'left', 'right',
        'volume_up', 'volume_down', 'play/pause',
        'print_screen', 'pause', 'caps_lock', 'num_lock', 'scroll_lock', 'menu',
        'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
    }

    for key in keys:
        keyboard.block_key(key)

    root = tk.Tk()
    root.title("Система 'Защитник'")
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    label = tk.Label(root, text="Включена ситема 'Защитник', доступ ограничен", font=("Arial", 25))
    label.pack(padx=20, pady=20)
    root.update_idletasks()

    root.lift()

    pyautogui.FAILSAFE = False
    screen_w, screen_h = pyautogui.size()

    while safer_status:
        pyautogui.moveTo(random.randint(0, screen_w), random.randint(0, screen_h))
        keyboard.write("Ввод заблокирован ")
        root.update()

    root.destroy()
    keyboard.unhook_all()


def get_screenshot():
    screenshot = pyautogui.screenshot()

    img_byte_arr = BytesIO()
    screenshot.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    return img_byte_arr.read()


def lock():
    ctypes.windll.user32.LockWorkStation()


def off():
    subprocess.run(["shutdown", "/s", "/f", "/t", "0"])


def restart():
    subprocess.run(["shutdown", "/r", "/f", "/t", "0"])


def send_notification(text: str):
    root = tk.Tk()
    root.title("Уведомление")
    label = tk.Label(root, text=text, font=("Arial", 15))
    label.pack(padx=20, pady=20)
    root.lift()
    root.mainloop()
