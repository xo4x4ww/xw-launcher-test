#!/usr/bin/env python3
# run.py - Точка входа для запуска лаунчера

import sys
import os

# Добавляем корневую папку проекта в путь
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Добавляем папку src в путь
src_path = os.path.join(os.path.dirname(__file__), "src")
sys.path.insert(0, src_path)

from main import main

if __name__ == "__main__":
    print("=" * 50)
    print("XW Launcher v0.9.1-alpha")
    print("=" * 50)
    print("Запуск в режиме разработки...")
    main()