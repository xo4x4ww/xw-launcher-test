```

xw-launcher/
├── code/               # Исходный код лаунчера
│   ├── src/            # Python модули
│   ├── build.py        # Скрипт сборки .exe
│   ├── run.py          # Точка входа
│   └── launcher_config.json
├── assets/             # Ресурсы (иконки)
│   └── icon.ico        # Иконка для .exe
├── index.html          # Лендинг для GitHub Pages (корень)
├── style.css           # Стили для сайта
├── icon.png            # Иконка для сайта
├── build.py            # Скрипт сборки (в корне)
├── version_info.txt    # Информация о версии для Windows
├── .gitignore
├── README.md
└── LICENSE

```

---

```

## 🛠️ Сборка .exe файла

```

```

**Результат:** `dist/XWLauncher.exe`

**Советы по сборке:**

1. Положите иконку `icon.ico` в папку `assets/` (необязательно)
1. Скрипт сам создаст все необходимые папки
1. После сборки файл появится в папке `dist/`

## 🌐 GitHub Pages

Сайт доступен в корне репозитория:

- `index.html` — главная страница
- `style.css` — стили
- `icon.png` — иконка сайта

**Активация:** Settings → Pages → Source: `main` branch, root `/`

**Ссылка на скачивание .exe** ведёт на GitHub Releases. Чтобы она работала:

1. Создайте релиз `v0.9.1`
1. Прикрепите к нему `XWLauncher.exe`

## ⚠️ Дисклеймер (Соответствие EULA Mojang)

- **"Minecraft"** является торговой маркой **Mojang Studios**.
- Лаунчер **не связан** с Mojang Studios или Microsoft.
- Лаунчер **не содержит** пиратских копий Minecraft.
- Лаунчер **требует** наличия официального клиента Minecraft.
- Все загружаемые файлы берутся из официальных источников Mojang.
- Проект распространяется в образовательных и некоммерческих целях.

## 📄 Лицензия

MIT License — свободно для изучения, модификации и некоммерческого использования.

## 🙏 Благодарности

- [minecraft-launcher-lib](https://github.com/minecraft-laboratory/minecraft-launcher-lib)
- Mojang Studios

© 2026 XW Team

```