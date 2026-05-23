# main.py - Точка входа для GUI лаунчера

import tkinter as tk
import sys
import os

# Добавляем текущую папку в путь для импортов
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import LauncherApp
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print(f"Текущая директория: {os.getcwd()}")
    print(f"Путь к файлам: {os.path.dirname(__file__)}")
    input("Нажмите Enter для выхода...")
    sys.exit(1)

def main():
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()