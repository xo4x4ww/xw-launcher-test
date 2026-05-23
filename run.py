#!/usr/bin/env python3
# run.py - Точка входа для запуска лаунчера из корня проекта

import sys
import os

# Добавляем путь к папке code/src
src_path = os.path.join(os.path.dirname(__file__), "code", "src")
sys.path.insert(0, src_path)

from main import main

if __name__ == "__main__":
    print("=" * 50)
    print("XW Launcher v0.9.1-alpha")
    print("=" * 50)
    main()