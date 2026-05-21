#!/usr/bin/env python3
# build.py - Скрипт сборки XW Launcher в .exe с помощью PyInstaller

import subprocess
import sys
import os

VERSION = "0.9.1-alpha"
NAME = "XWLauncher"

# Полные пути к файлам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON = os.path.join(BASE_DIR, "assets", "icon.ico")
VERSION_FILE = os.path.join(BASE_DIR, "version_info.txt")
MAIN_SCRIPT = os.path.join(BASE_DIR, "code", "src", "main.py")

def build():
    print(f"🚀 Сборка {NAME} v{VERSION} в .exe...")
    
    # Проверяем существование необходимых файлов
    if not os.path.exists(MAIN_SCRIPT):
        print(f"❌ Ошибка: не найден {MAIN_SCRIPT}")
        print(f"   Запустите скрипт из корневой папки проекта")
        sys.exit(1)
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", NAME,
        "--distpath", os.path.join(BASE_DIR, "dist"),
        "--workpath", os.path.join(BASE_DIR, "build_temp"),
        "--specpath", os.path.join(BASE_DIR, "build_temp"),
        "--paths", os.path.join(BASE_DIR, "code", "src"),
    ]
    
    if os.path.exists(ICON):
        cmd.extend(["--icon", ICON])
        print(f"  ✅ Иконка: {ICON}")
    else:
        print("  ⚠️ Иконка не найдена (assets/icon.ico), используется стандартная")
    
    if os.path.exists(VERSION_FILE):
        cmd.extend(["--version-file", VERSION_FILE])
        print(f"  ✅ Версия из файла: {VERSION_FILE}")
    else:
        print(f"  ⚠️ Файл версии не найден: {VERSION_FILE}")
        # Добавляем флаг для версии через командную строку
        cmd.extend(["--version", VERSION])
    
    cmd.append(MAIN_SCRIPT)
    
    print("  🔨 Сборка начата, пожалуйста, подождите...")
    print("  (Это может занять 1-3 минуты)")
    
    # Запускаем PyInstaller
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        exe_path = os.path.join(BASE_DIR, "dist", f"{NAME}.exe")
        print(f"\n✅ Готово! Файл создан: {exe_path}")
        print(f"   Размер: {os.path.getsize(exe_path) / 1024 / 1024:.1f} MB")
    else:
        print(f"\n❌ Ошибка при сборке! Код ошибки: {result.returncode}")
        print("   Проверьте, что установлены все зависимости:")
        print("   pip install pyinstaller minecraft-launcher-lib")

def setup_folders():
    """Создаёт необходимые папки, если их нет"""
    folders = ["dist", "build_temp", "assets"]
    for folder in folders:
        os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)
        print(f"  📁 Папка {folder}/ создана (если не существовала)")

if __name__ == "__main__":
    print("=" * 50)
    print("XW Launcher Builder")
    print("=" * 50)
    setup_folders()
    build()
    print("\n💡 Совет: Скопируйте assets/icon.ico в папку assets/ для добавления иконки")