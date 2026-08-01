# CounterLauncher

<p align="center">
  <img src="channels4_profile_256.png" alt="CounterLauncher Logo" width="128">
</p>

<p align="center">
  <b>A lightweight, modern Minecraft Java Edition launcher written in Python.</b>
</p>

<p align="center">
  <a href="https://github.com/CounterGD/CounterLauncherRemake/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/CounterGD/CounterLauncherRemake/build.yml?branch=main&label=Build&logo=github" alt="Build Status">
  </a>
  <a href="https://github.com/CounterGD/CounterLauncherRemake/releases">
    <img src="https://img.shields.io/github/v/release/CounterGD/CounterLauncherRemake?logo=github" alt="Latest Release">
  </a>
  <a href="https://github.com/CounterGD/CounterLauncherRemake/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/CounterGD/CounterLauncherRemake" alt="License">
  </a>
  <img src="https://img.shields.io/badge/Python-3.13+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Linux-Supported-FCC624?logo=linux&logoColor=black" alt="Linux">
  <img src="https://img.shields.io/badge/Status-Active%20Development-orange" alt="Development Status">
</p>

---

## ✨ Features

- 🎮 Launch Minecraft Java Edition
- 📥 Download official Minecraft versions
- 📚 Automatic library downloader
- 🖼️ Automatic asset downloader
- 🧩 Native library installer
- ☕ Automatic Java runtime installation
- 📦 Portable Linux AppImage builds
- 🐍 Written entirely in Python

---

## 📸 Screenshots

> Screenshots coming soon.

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/CounterGD/CounterLauncherRemake.git
cd CounterLauncherRemake
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run CounterLauncher:

```bash
python minecraft_dl.py
```

---

## 🔨 Building

Using PyInstaller:

```bash
pyinstaller --onefile --name CounterLauncher minecraft_dl.py
```

Or use the Makefile:

```bash
make
```

This builds the executable and packages it into an AppImage.

---

## 📁 Project Structure

```text
CounterLauncherRemake/
├── .github/
│   └── workflows/
│       └── build.yml
├── AppDir/
├── build/
├── dist/
├── java.py
├── libs.py
├── minecraft_dl.py
├── Makefile
├── LICENSE
├── EULA.md
├── PRIVACY.md
└── README.md
```

---

## 🛣️ Roadmap

- [x] Minecraft version downloader
- [x] Library downloader
- [x] Asset downloader
- [x] Native downloader
- [x] Java runtime installer
- [x] Linux AppImage packaging
- [ ] Launcher GUI
- [ ] Microsoft account authentication
- [ ] Offline mode
- [ ] Fabric support
- [ ] Forge support
- [ ] NeoForge support
- [ ] Automatic launcher updates
- [ ] Windows support
- [ ] macOS support

---

## 🤝 Contributing

Contributions are welcome!

If you find a bug or have an idea for a new feature:

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Open a Pull Request.

---

## 📜 Legal

CounterLauncher is an independent project.

It is **not affiliated with, endorsed by, sponsored by, or approved by Mojang Studios or Microsoft.**

Minecraft is a trademark of Microsoft Corporation.

Please read:

- [LICENSE](LICENSE)
- [EULA](EULA.md)
- [Privacy Policy](PRIVACY.md)

---

## 📄 License

Copyright © 2026 CounterGD.

See the LICENSE file for more information.

---

update: [![build result](https://build.opensuse.org/projects/home:Counter6/packages/CounterLauncher/badge.svg?type=default)](https://build.opensuse.org/package/show/home:Counter6/CounterLauncher)

<p align="center">
  Made with ❤️ by <b>CounterGD</b>
</p>
