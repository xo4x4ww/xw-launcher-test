# main.py - Точка входа для GUI лаунчера

import tkinter as tk
import sys
import os

# Добавляем текущую папку в путь для импортов
sys.path.insert(0, os.path.dirname(__file__))

from app import LauncherApp

def main():
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()