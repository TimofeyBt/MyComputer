import os
import subprocess
import sys
import win32com.client
import winreg as reg
import ctypes
import shutil
import tkinter as tk
from plyer import notification


def paste_text(event):
    event.widget.insert(tk.INSERT, event.widget.clipboard_get())

    return "break"

def create_path_settings():
    hint_text = "Введите путь к папке"

    path = os.getenv("MY_PC_DATA_PATH")


    def please_restart():
        root.destroy()

        restart_root = tk.Tk()
        restart_root.title("MyComputer Настройки")
        label = tk.Label(restart_root, text="Нужно перезагрузить ПК для обновления настроек пути", font=("Arial", 14))
        label.pack(padx=20, pady=20)

    def on_path_entry_click(event):
        if path_entry.get() == hint_text:
            path_entry.delete(0, tk.END)

    def of_focusout_path_entry(event):
        if path_entry.get() == "":
            path_entry.insert(0, hint_text)

    def set_path():
        path_to_add = path_entry.get()
        last_path = os.getenv("MY_PC_DATA_PATH")

        if path_to_add == last_path:
            root.destroy()
            create_standart_settings()
            return

        if not os.path.isdir(path_to_add):
            notification.notify(
                title="Укажите корректный путь к папке",
                message="Должен быть указан корректный путь к именно папке, где будут храниться данные",
                app_name="MyComputer",
            )
            return

        if path_to_add[-1] not in r"\/":
            path_to_add += "/"

        key = reg.HKEY_CURRENT_USER
        key_path = r"Environment"
        value_name = "MY_PC_DATA_PATH"

        with reg.OpenKey(key, key_path, 0, reg.KEY_WRITE) as registry_key:
            reg.SetValueEx(registry_key, value_name, 0, reg.REG_EXPAND_SZ, path_to_add)
        ctypes.windll.user32.PostMessageW(0xFFFF, 0x1A, 0, 0)

        _ = open(path_to_add + "bot_token.txt", "a").close()
        _ = open(path_to_add + "users.txt", "a").close()

        shutil.move("autostart.exe", path_to_add)



        please_restart()

    root = tk.Tk()
    root.title("MyComputer Настройки -- Путь к папке")

    root.geometry("750x200")

    root.config(bg="black")

    path_entry = tk.Entry(root, width=1, font=("Arial", 15), bd=0)
    path_entry.insert(0, hint_text if path is None else path)

    path_entry.pack(fill=tk.X, padx=20, pady=(20, 10))
    path_entry.config(bg="purple", fg="lightgray")

    path_entry.bind("<FocusIn>", on_path_entry_click)
    path_entry.bind("<FocusOut>", of_focusout_path_entry)

    path_entry.bind("<Control-v>", paste_text)

    save_path_button = tk.Button(root, text="Сохранить", width=10, height=1, bg="purple", fg="lightgrey",
                                 font=("Arial", 25), command=set_path, bd=0)
    save_path_button.pack(padx=20, pady=(40,10))
    root.mainloop()


def create_standart_settings():
    token_hint = "Введите токен бота"
    ids_hint = "Введите id через запятую"

    data_path = os.getenv("MY_PC_DATA_PATH")

    def save_data():

        bot_token = token_entry.get()
        telegram_ids = ids_entry.get()

        if not bot_token or not telegram_ids or bot_token == token_hint or ids_hint == telegram_ids:
            notification.notify(
                title="Введите данные",
                message="Сначало введите данные в поля для ввода",
                app_name="MyComputer",
            )
            return

        with open(data_path + "bot_token.txt", "w") as file:
            file.write(bot_token)
        with open(data_path + "users.txt", "w") as file:
            file.write(telegram_ids.replace(" ", ""))

        notification.notify(
            title="Данные успешно сохранены!",
            message="Данные успешно сохранены, теперь они будут использоваться для MyComputer",
            app_name="MyComputer",
        )

    def get_data():

        if data_path is None:
            notification.notify(
                title="Хм... Ссылка не была найдена",
                message="Попробуйте изменить ссылку к папке с данными",
                app_name="MyComputer",
            )

        try:
            bot_token_file = open(data_path + "bot_token.txt", "r")
            BOT_TOKEN = bot_token_file.read()
            bot_token_file.close()

        except:
            BOT_TOKEN = ""

            _ = open(data_path + "bot_token.txt", "w").close()

        try:
            telegram_ids_file = open(data_path + "users.txt", "r")
            TELEGRAM_IDS = telegram_ids_file.read()
            telegram_ids_file.close()
        except:
            TELEGRAM_IDS = ""

            _ = open(data_path + "users.txt", "w").close()

        return BOT_TOKEN, TELEGRAM_IDS

    def on_token_entry_click(event):
        if token_entry.get() == token_hint:
            token_entry.delete(0, tk.END)

    def of_focusout_token_entry(event):
        if token_entry.get() == "":
            token_entry.insert(0, token_hint)

    def on_ids_entry_click(event):
        if ids_entry.get() == ids_hint:
            ids_entry.delete(0, tk.END)

    def of_focusout_ids_entry(event):
        if ids_entry.get() == "":
            ids_entry.insert(0, ids_hint)

    root = tk.Tk()
    root.title("MyComputer Настройки")

    root.geometry("750x300")

    root.config(bg="black")

    token, ids = get_data()

    token_entry = tk.Entry(root, width=1, font=("Arial", 15), bd=0)
    token_entry.insert(0, token_hint if token == "" else token)

    token_entry.pack(fill=tk.X, padx=20, pady=(30, 10))
    token_entry.config(bg="purple", fg="lightgray")

    token_entry.bind("<FocusIn>", on_token_entry_click)
    token_entry.bind("<FocusOut>", of_focusout_token_entry)

    token_entry.bind("<Control-v>", paste_text)

    ids_entry = tk.Entry(root, width=1, font=("Arial", 15), bd=0)
    ids_entry.insert(0, ids_hint if ids == "" else ids)

    ids_entry.pack(fill=tk.X, padx=20, pady=(20, 10))
    ids_entry.config(bg="purple", fg="lightgray")

    ids_entry.bind("<FocusIn>", on_ids_entry_click)
    ids_entry.bind("<FocusOut>", of_focusout_ids_entry)

    ids_entry.bind("<Control-v>", paste_text)

    save_data_button = tk.Button(root, text="Сохранить", width=10, height=1, bg="purple", fg="lightgrey",
                                 font=("Arial", 25), command=save_data, bd=0)
    save_data_button.pack(padx=20, pady=(40,10))

    root.mainloop()


if os.getenv("MY_PC_DATA_PATH") is None:

    create_path_settings()

else:
    create_standart_settings()
