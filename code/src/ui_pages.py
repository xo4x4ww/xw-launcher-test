# ui_pages.py - Все страницы интерфейса

import os
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from ui_widgets import RoundedFrame, HoverButton

class Header(tk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, bg="#0d0d0d", height=36, **kwargs)
        self.pack_propagate(False)
        self.app = app

        tk.Label(self, text="XW Launcher", font=("Segoe UI", 16, "bold"),
                 bg="#0d0d0d", fg="#ffffff").pack(side="left")

        right = tk.Frame(self, bg="#0d0d0d")
        right.pack(side="right")

        profile_frame = RoundedFrame(right, bg="#1a1a1a", radius=8)
        profile_frame.pack(side="left")
        profile_inner = tk.Frame(profile_frame.inner_frame, bg="#1a1a1a")
        profile_inner.pack(fill="both", padx=2, pady=2)

        self.username = app.current_username
        self.profile_btn = tk.Menubutton(
            profile_inner, text=f" {self.username} ▼ ", font=("Segoe UI", 10),
            bg="#1a1a1a", fg="#cccccc", bd=0, cursor="hand2",
            activebackground="#1a1a1a", activeforeground="#ffffff",
            padx=8, pady=4
        )
        self.profile_btn.pack()
        self._update_menu()

    def _update_menu(self):
        app = self.app
        menu = tk.Menu(self.profile_btn, tearoff=0, bg="#1a1a1a", fg="#cccccc",
                       activebackground="#2a2a2a", activeforeground="#ffffff", bd=0, font=("Segoe UI", 10))
        for i, acc in enumerate(app._accounts):
            check = "✓ " if i == app._current_account_index else "  "
            menu.add_command(label=f"{check}{acc['username']}",
                             command=lambda idx=i: app.switch_account(idx))
        menu.add_separator()
        menu.add_command(label="➕ Добавить аккаунт", command=lambda: AccountsManager(app).add_account())
        menu.add_command(label="✏️ Управление аккаунтами", command=lambda: AccountsManager(app).manage())
        menu.add_separator()
        menu.add_command(label="⚙️ Настройки", command=lambda: SettingsDialog(app))
        menu.add_command(label="📁 Папка игры", command=lambda: os.startfile(app.minecraft_dir))
        menu.add_separator()
        menu.add_command(label="🚪 Выход", command=self.app.root.quit)
        self.profile_btn.config(menu=menu)

    def update_username(self, name):
        self.username = name
        self.profile_btn.config(text=f" {name} ▼ ")
        self._update_menu()

class Sidebar(tk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, bg="#0d0d0d", width=220, **kwargs)
        self.pack_propagate(False)
        self.app = app
        self.nav_buttons = {}

        nav_frame = tk.Frame(self, bg="#0d0d0d")
        nav_frame.pack(fill="x", pady=(30, 0))

        items = [
            ("🏠 Главная", "home"),
            ("📰 Новости версий", "news"),
            ("📦 Сборки", "modpacks"),
            ("🔧 Моды", "mods"),
        ]
        for text, key in items:
            item_frame = tk.Frame(nav_frame, bg="#0d0d0d", height=44)
            item_frame.pack(fill="x", pady=3)
            item_frame.pack_propagate(False)
            btn = HoverButton(item_frame, text=text, fg="#555555", bg="#0d0d0d",
                              font=("Segoe UI", 12), anchor="w",
                              command=lambda k=key: app._show_page(k))
            btn.pack(fill="both", padx=10)
            self.nav_buttons[key] = (item_frame, btn)

        bottom_frame = tk.Frame(self, bg="#0d0d0d")
        bottom_frame.pack(side="bottom", fill="x", pady=15)
        for text, cmd in [
            ("👤 Аккаунты", lambda: AccountsManager(app).manage()),
            ("⚙️ Настройки", lambda: SettingsDialog(app)),
            ("📁 Папка игры", lambda: os.startfile(app.minecraft_dir))
        ]:
            HoverButton(bottom_frame, text=text, fg="#555555", bg="#0d0d0d",
                        font=("Segoe UI", 11), anchor="w", command=cmd).pack(fill="x", padx=10, pady=4)

        self.set_active("home")

    def set_active(self, key):
        for k, (frame, btn) in self.nav_buttons.items():
            for w in frame.winfo_children():
                if isinstance(w, tk.Frame):
                    w.destroy()
            if k == key:
                btn.config(fg="#ffffff", bg="#0d0d0d", font=("Segoe UI", 12, "bold"))
                tk.Frame(frame, bg="#4a9eff", width=3).place(x=0, rely=0.15, height=30)
            else:
                btn.config(fg="#555555", bg="#0d0d0d", font=("Segoe UI", 12))

class HomePage(tk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, bg="#0d0d0d", **kwargs)
        self.app = app
        self._build()

    def _build(self):
        app = self.app
        username = app.current_username
        hour = datetime.now().hour
        greet = "Доброе утро" if hour < 12 else "Добрый день" if hour < 18 else "Добрый вечер"

        welcome = RoundedFrame(self, bg="#1a1a1a", radius=18)
        welcome.pack(fill="x", pady=(0, 25))

        w_content = tk.Frame(welcome.inner_frame, bg="#1a1a1a")
        w_content.pack(fill="both", padx=24, pady=20)
        tk.Label(w_content, text=f"{greet}, {username}!", font=("Segoe UI", 20, "bold"),
                 bg="#1a1a1a", fg="#ffffff").pack(anchor="w")
        tk.Label(w_content, text="Готовы к новым приключениям в Minecraft?",
                 font=("Segoe UI", 11), bg="#1a1a1a", fg="#999999").pack(anchor="w", pady=(4, 0))

        row = tk.Frame(self, bg="#0d0d0d")
        row.pack(fill="x", pady=(0, 25))

        vf = tk.Frame(row, bg="#0d0d0d")
        vf.pack(side="left", padx=(0, 30))
        tk.Label(vf, text="Версия", font=("Segoe UI", 10, "bold"), bg="#0d0d0d", fg="#999999").pack(anchor="w", pady=(0, 6))
        self.version_combo = ttk.Combobox(vf, values=[], state="readonly",
                                          font=("Segoe UI", 11), width=22, style="Dark.TCombobox")
        self.version_combo.pack()
        if hasattr(app, 'versions') and app.versions:
            self.update_versions(app.versions)

        af = tk.Frame(row, bg="#0d0d0d")
        af.pack(side="left")
        tk.Label(af, text="Аккаунт", font=("Segoe UI", 10, "bold"), bg="#0d0d0d", fg="#999999").pack(anchor="w", pady=(0, 6))
        self.account_combo = ttk.Combobox(af, values=[], state="readonly",
                                          font=("Segoe UI", 11), width=22, style="Dark.TCombobox")
        self.account_combo.pack()
        self.update_accounts([a["username"] for a in app._accounts], app._current_account_index)

        play_btn = tk.Button(self, text="▶ ИГРАТЬ", bg="#4a9eff", fg="#ffffff",
                             font=("Segoe UI", 13, "bold"), bd=0, padx=40, pady=12,
                             cursor="hand2", command=self._launch,
                             activebackground="#3a8eef", activeforeground="#ffffff")
        play_btn.pack(pady=(0, 30))

        cards_frame = tk.Frame(self, bg="#0d0d0d")
        cards_frame.pack(fill="x")

        left_card = RoundedFrame(cards_frame, bg="#1a1a1a", radius=18)
        left_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        left_card.config(height=140)
        left_card.pack_propagate(False)

        lc = tk.Frame(left_card.inner_frame, bg="#1a1a1a")
        lc.pack(fill="both", padx=20, pady=20)
        tk.Label(lc, text="📦", font=("Segoe UI", 32), bg="#1a1a1a", fg="#4a9eff").pack(anchor="w")
        tk.Label(lc, text="Сборки модов", font=("Segoe UI", 15, "bold"),
                 bg="#1a1a1a", fg="#ffffff").pack(anchor="w", pady=(8, 4))
        tk.Label(lc, text="Готовые сборки для любого стиля игры",
                 font=("Segoe UI", 9), bg="#1a1a1a", fg="#999999").pack(anchor="w")

        right_card = RoundedFrame(cards_frame, bg="#1a1a1a", radius=18)
        right_card.pack(side="right", fill="both", expand=True, padx=(10, 0))
        right_card.config(height=140)
        right_card.pack_propagate(False)

        rc = tk.Frame(right_card.inner_frame, bg="#1a1a1a")
        rc.pack(fill="both", padx=20, pady=20)
        mod_count = len(self.app._installed_mods)
        tk.Label(rc, text="🔧", font=("Segoe UI", 32), bg="#1a1a1a", fg="#50c878").pack(anchor="w")
        tk.Label(rc, text=f"Установлено модов: {mod_count}", font=("Segoe UI", 15, "bold"),
                 bg="#1a1a1a", fg="#ffffff").pack(anchor="w", pady=(8, 4))
        tk.Label(rc, text="Управляйте модами во вкладке Моды",
                 font=("Segoe UI", 9), bg="#1a1a1a", fg="#999999").pack(anchor="w")

    def update_versions(self, versions):
        self.version_combo["values"] = versions
        last = self.app.config.last_version
        if last in versions:
            self.version_combo.set(last)
        elif versions:
            self.version_combo.set(versions[0])

    def update_accounts(self, names, current_idx):
        self.account_combo["values"] = names
        if 0 <= current_idx < len(names):
            self.account_combo.set(names[current_idx])

    def refresh_greeting(self):
        self.destroy()
        self.__init__(self.master, self.app)
        self.pack(fill="both", expand=True)

    def _launch(self):
        version = self.version_combo.get()
        acc_name = self.account_combo.get()
        if not version:
            messagebox.showwarning("Внимание", "Выберите версию Minecraft")
            return
        if not acc_name:
            messagebox.showwarning("Внимание", "Выберите аккаунт")
            return
        self.app.game_launcher.launch(version, acc_name, self.app._accounts, self.app)

class NewsPage(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#0d0d0d", **kwargs)
        self._build()

    def _build(self):
        tk.Label(self, text="Новости версий", font=("Segoe UI", 22, "bold"),
                 bg="#0d0d0d", fg="#ffffff").pack(anchor="w", pady=(0, 20))
        news = [
            ("1.21.4", "Winter Drop — новые блоки и функции.", "3 декабря 2024"),
            ("1.21.3", "Исправлены критические ошибки.", "23 октября 2024"),
            ("1.21", "Tricky Trials — новые испытания.", "13 июня 2024"),
            ("1.20.5", "Armored Paws — броненосцы и волчья броня.", "23 апреля 2024"),
        ]
        for ver, desc, date in news:
            card = RoundedFrame(self, bg="#1a1a1a", radius=14)
            card.pack(fill="x", pady=6)
            inner = tk.Frame(card.inner_frame, bg="#1a1a1a")
            inner.pack(fill="both", padx=20, pady=18)
            tk.Label(inner, text=f"🆕 Minecraft {ver}", font=("Segoe UI", 13, "bold"),
                     bg="#1a1a1a", fg="#ffffff").pack(anchor="w")
            tk.Label(inner, text=date, font=("Segoe UI", 9), bg="#1a1a1a", fg="#4a9eff").pack(anchor="w", pady=(2, 8))
            tk.Label(inner, text=desc, font=("Segoe UI", 10), bg="#1a1a1a", fg="#aaaaaa").pack(anchor="w")

class ModpacksPage(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#0d0d0d", **kwargs)
        self._build()

    def _build(self):
        tk.Label(self, text="Сборки модов", font=("Segoe UI", 22, "bold"),
                 bg="#0d0d0d", fg="#ffffff").pack(anchor="w", pady=(0, 20))
        packs = [
            ("Better MC", "1.20.1", "Forge", "Улучшенный ванильный опыт", 150),
            ("All The Mods 9", "1.20.1", "Forge", "400+ модов", 420),
            ("Fabulously Optimized", "1.20.4", "Fabric", "Оптимизация и шейдеры", 45),
            ("RLCraft", "1.12.2", "Forge", "Хардкорное выживание", 120),
        ]
        for name, ver, loader, desc, cnt in packs:
            card = RoundedFrame(self, bg="#1a1a1a", radius=14)
            card.pack(fill="x", pady=6)
            inner = tk.Frame(card.inner_frame, bg="#1a1a1a")
            inner.pack(fill="both", padx=20, pady=18)
            tk.Label(inner, text=name, font=("Segoe UI", 14, "bold"), bg="#1a1a1a", fg="#ffffff").pack(anchor="w")
            tk.Label(inner, text=f"{ver} • {loader} • {cnt} модов", font=("Segoe UI", 9),
                     bg="#1a1a1a", fg="#4a9eff").pack(anchor="w", pady=(2, 8))
            tk.Label(inner, text=desc, font=("Segoe UI", 9), bg="#1a1a1a", fg="#999999").pack(anchor="w")
            btn = tk.Button(inner, text="Установить", bg="#333333", fg="#ffffff", bd=0, padx=15, pady=5,
                            cursor="hand2", activebackground="#444444", activeforeground="#ffffff",
                            command=lambda n=name: messagebox.showinfo("Инфо", f"Установка {n} будет доступна в следующей версии"))
            btn.pack(anchor="w", pady=(12, 0))

class ModsPage(tk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, bg="#0d0d0d", **kwargs)
        self.app = app
        self.mod_icons = {}
        self._build()

    def _build(self):
        header = tk.Frame(self, bg="#0d0d0d")
        header.pack(fill="x", pady=(0, 20))
        tk.Label(header, text="Моды", font=("Segoe UI", 22, "bold"),
                 bg="#0d0d0d", fg="#ffffff").pack(side="left")
        open_btn = tk.Button(header, text="📂 Открыть папку", bg="#333333", fg="#ffffff", bd=0, padx=15, pady=5,
                             cursor="hand2", command=self._open_mods_folder,
                             activebackground="#444444", activeforeground="#ffffff")
        open_btn.pack(side="right")

        if not self.app._installed_mods:
            empty = RoundedFrame(self, bg="#1a1a1a", radius=18)
            empty.pack(fill="both", expand=True)
            einner = tk.Frame(empty.inner_frame, bg="#1a1a1a")
            einner.pack(expand=True, padx=40, pady=40)
            tk.Label(einner, text="📦", font=("Segoe UI", 48), bg="#1a1a1a", fg="#888888").pack()
            tk.Label(einner, text="Нет установленных модов", font=("Segoe UI", 14, "bold"),
                     bg="#1a1a1a", fg="#ffffff").pack(pady=(10, 5))
            tk.Label(einner, text="Поместите файлы .jar в папку mods",
                     font=("Segoe UI", 10), bg="#1a1a1a", fg="#999999").pack()
            btn = tk.Button(einner, text="Открыть папку модов", bg="#4a9eff", fg="#ffffff", bd=0, padx=20, pady=8,
                            cursor="hand2", command=self._open_mods_folder,
                            activebackground="#3a8eef", activeforeground="#ffffff")
            btn.pack(pady=(20, 0))
        else:
            canvas = tk.Canvas(self, bg="#0d0d0d", highlightthickness=0)
            scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview, width=8)
            scrollbar.configure(bg="#2a2a2a", troughcolor="#151515", activebackground="#4a4a4a", bd=0)
            scrollable_frame = tk.Frame(canvas, bg="#0d0d0d")

            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            def on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
            canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            cols = tk.Frame(scrollable_frame, bg="#0d0d0d")
            cols.pack(fill="x", pady=(0, 8))
            tk.Label(cols, text="", font=("Segoe UI", 10), bg="#0d0d0d", width=3).pack(side="left")
            tk.Label(cols, text="Название", font=("Segoe UI", 10, "bold"), bg="#0d0d0d", fg="#666666",
                     width=28, anchor="w").pack(side="left")
            tk