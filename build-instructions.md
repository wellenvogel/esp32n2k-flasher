# macOS

`pyinstaller -F -w -n ESPHome-Flasher -i icon.icns esphomeflasher/__main__.py`

# Windows

1. Start up VM (ensure VC++ compiler installed)
   you can use choco install microsoft-visual-cpp-build-tools (if you have choco on Windows) 
2. Install Python (3) from App Store
3. Download esp32n2k-flasher from GitHub, use a visual studio prompt
4. `pip install -e.` and `pip install pyinstaller`
5. Check with `python -m flashtool.__main__`
6. `python -m PyInstaller.__main__ -F -w -n ESP32N2K-Flasher -i icon.ico esphomeflasher\__main__.py`
7. Go to `dist` folder, check ESP32N2K-Flasher.exe works.
