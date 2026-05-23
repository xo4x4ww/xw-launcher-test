#!/usr/bin/env python3
# build.py - Скрипт сборки XW Launcher в .exe с помощью PyInstaller

import subprocess
import sys
import os
import shutil

VERSION = "0.9.1-alpha"
NAME = "XWLauncher"

# Полные пути к файлам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON = os.path.join(BASE_DIR, "assets", "icon.ico")
VERSION_FILE = os.path.join(BASE_DIR, "version_info.txt")
MAIN_SCRIPT = os.path.join(BASE_DIR, "code", "src", "main.py")
SRC_DIR = os.path.join(BASE_DIR, "code", "src")

def clean_build():
    """Очистка временных папок"""
    folders = ["build_temp", "dist"]
    for folder in folders:
        path = os.path.join(BASE_DIR, folder)
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"  🧹 Очищена папка {folder}/")
    print()

def build():
    print(f"🚀 Сборка {NAME} v{VERSION} в .exe...")
    
    # Проверяем существование необходимых файлов
    if not os.path.exists(MAIN_SCRIPT):
        print(f"❌ Ошибка: не найден {MAIN_SCRIPT}")
        sys.exit(1)
    
    # Проверяем наличие всех модулей
    required_files = ["app.py", "config.py", "minecraft.py", "ui_pages.py", "ui_widgets.py"]
    for file in required_files:
        file_path = os.path.join(SRC_DIR, file)
        if not os.path.exists(file_path):
            print(f"❌ Ошибка: не найден {file_path}")
            sys.exit(1)
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", NAME,
        "--distpath", os.path.join(BASE_DIR, "dist"),
        "--workpath", os.path.join(BASE_DIR, "build_temp"),
        "--specpath", os.path.join(BASE_DIR, "build_temp"),
        "--paths", SRC_DIR,
        "--add-data", f"{SRC_DIR}{os.pathsep}.",
        "--hidden-import", "tkinter",
        "--hidden-import", "minecraft_launcher_lib",
        "--hidden-import", "requests",
        "--hidden-import", "urllib3",
        "--collect-all", "minecraft_launcher_lib",
        "--collect-all", "requests",
    ]
    
    if os.path.exists(ICON):
        cmd.extend(["--icon", ICON])
        print(f"  ✅ Иконка: {ICON}")
    else:
        print("  ⚠️ Иконка не найдена (assets/icon.ico)")
    
    if os.path.exists(VERSION_FILE):
        cmd.extend(["--version-file", VERSION_FILE])
        print(f"  ✅ Версия из файла: {VERSION_FILE}")
    
    cmd.append(MAIN_SCRIPT)
    
    print("  🔨 Сборка начата, пожалуйста, подождите...")
    print("  (Это может занять 2-5 минут)\n")
    
    # Запускаем PyInstaller
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        exe_path = os.path.join(BASE_DIR, "dist", f"{NAME}.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / 1024 / 1024
            print(f"\n{'='*50}")
            print(f"✅ ГОТОВО! Файл создан: {exe_path}")
            print(f"   Размер: {size_mb:.1f} MB")
            print(f"{'='*50}")
        else:
            print(f"\n⚠️ Сборка завершена, но файл не найден по пути: {exe_path}")
            print("   Проверьте папку dist/")
    else:
        print(f"\n❌ ОШИБКА при сборке! Код: {result.returncode}")
        print("   Проверьте warn-файл в build_temp/XWLauncher/")

def setup_folders():
    """Создаёт необходимые папки"""
    folders = ["dist", "build_temp", "assets"]
    for folder in folders:
        os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

if __name__ == "__main__":
    print("=" * 50)
    print("XW Launcher Builder v" + VERSION)
    print("=" * 50)
    clean_build()
    setup_folders()
    build()
    print("\n💡 Совет: Положите icon.ico в папку assets/ для иконки")
    print("📦 Готовый лаунчер: dist/XWLauncher.exe")