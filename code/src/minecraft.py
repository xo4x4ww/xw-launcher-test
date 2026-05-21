# minecraft.py - Загрузка версий и запуск игры

import subprocess
import threading
from tkinter import messagebox
import minecraft_launcher_lib

class VersionLoader:
    def __init__(self, root, config):
        self.root = root
        self.config = config

    def load_versions_async(self, callback):
        def worker():
            try:
                manifest = minecraft_launcher_lib.utils.get_version_list()
                # Показываем последние 30 версий (release + snapshot по желанию)
                vers = [v["id"] for v in manifest if v.get("type") in ["release", "snapshot"]][:30]
                if not vers:
                    vers = ["1.21.4", "1.21.3", "1.21.1", "1.20.4", "1.20.1", "1.19.4"]
            except Exception as e:
                print(f"Ошибка загрузки версий: {e}")
                vers = ["1.21.4", "1.21.3", "1.21.1", "1.20.4", "1.20.1", "1.19.4"]
            self.root.after(0, lambda: callback(vers))
        threading.Thread(target=worker, daemon=True).start()

class GameLauncher:
    def __init__(self, root, config, minecraft_dir):
        self.root = root
        self.config = config
        self.minecraft_dir = minecraft_dir

    def launch(self, version, acc_name, accounts, app):
        # Обновляем текущего пользователя в конфиге
        for i, acc in enumerate(accounts):
            if acc["username"] == acc_name:
                app._current_account_index = i
                self.config.last_username = acc_name
                break
        self.config.last_version = version
        self.config.save()

        close_launcher = self.config.get("close_launcher", True)
        if close_launcher:
            self.root.iconify()

        def worker():
            try:
                # Убедимся, что версия установлена
                if not minecraft_launcher_lib.utils.is_version_installed(version, self.minecraft_dir):
                    def callback(progress: dict):
                        # Выводим прогресс загрузки в консоль (можно расширить для GUI)
                        print(f"Загрузка: {progress.get('status', '')} {progress.get('current', 0)}%")
                    minecraft_launcher_lib.install.install_minecraft_version(version, self.minecraft_dir, callback=callback)

                opts = {"username": acc_name}
                ram = self.config.get("ram_allocation")
                if ram and isinstance(ram, int) and ram >= 512:
                    opts["ram"] = str(ram)

                cmd = minecraft_launcher_lib.command.get_minecraft_command(version, self.minecraft_dir, opts)
                subprocess.Popen(cmd, cwd=self.minecraft_dir)

                if close_launcher:
                    self.root.after(1000, self.root.quit)
                else:
                    self.root.after(0, self.root.deiconify)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Ошибка запуска", str(e)))
                self.root.after(0, self.root.deiconify)

        threading.Thread(target=worker, daemon=True).start()