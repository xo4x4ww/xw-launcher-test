#!/usr/bin/env python3
# run.py - Запуск лаунчера из корня проекта

import sys
import os

# Добавляем папку code/src в путь
src_path = os.path.join(os.path.dirname(__file__), "code", "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

print("Пути поиска модулей:")
for p in sys.path[:3]:
    print(f"  - {p}")

# Проверяем наличие всех файлов
required_files = ["app.py", "config.py", "minecraft.py", "ui_pages.py", "ui_widgets.py", "ui_pages_extras.py"]
missing = []
for file in required_files:
    if not os.path.exists(os.path.join(src_path, file)):
        missing.append(file)

if missing:
    print(f"❌ Отсутствуют файлы: {', '.join(missing)}")
    input("Нажмите Enter для выхода...")
    sys.exit(1)

try:
    from app import LauncherApp
    print("✅ Все модули загружены!")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    import traceback
    traceback.print_exc()
    input("\nНажмите Enter для выхода...")
    sys.exit(1)

def main():
    import tkinter as tk
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()