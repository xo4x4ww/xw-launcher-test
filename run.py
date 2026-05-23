#!/usr/bin/env python3
# run.py - Запуск лаунчера из корня проекта

import sys
import os

# Добавляем папку code/src в путь ПЕРВОЙ
src_path = os.path.join(os.path.dirname(__file__), "code", "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Также добавляем папку code (на случай относительных импортов)
code_path = os.path.join(os.path.dirname(__file__), "code")
if code_path not in sys.path:
    sys.path.insert(0, code_path)

print("Пути поиска модулей:")
for p in sys.path[:3]:
    print(f"  - {p}")

try:
    from app import LauncherApp
    print("✅ Модуль app найден!")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print(f"\nПроверьте, что файлы существуют:")
    print(f"  - {os.path.join(src_path, 'app.py')}: {os.path.exists(os.path.join(src_path, 'app.py'))}")
    print(f"  - {os.path.join(src_path, 'config.py')}: {os.path.exists(os.path.join(src_path, 'config.py'))}")
    print(f"  - {os.path.join(src_path, 'minecraft.py')}: {os.path.exists(os.path.join(src_path, 'minecraft.py'))}")
    input("\nНажмите Enter для выхода...")
    sys.exit(1)

def main():
    import tkinter as tk
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()