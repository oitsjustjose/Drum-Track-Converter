# Building using PyInstaller

### First, install PyInstaller:

```powershell
pip install pyinstaller
```

### Then build the application:

```powershell
pyinstaller `
    --noconfirm `
    --onefile `
    --windowed `
    --icon ".\assets\icon.ico" `
    --name "Drum Track Converter" `
    --add-data ".\src;src/" `
    --add-data=".\assets\icon.ico;assets/icon.ico." `
    --add-data ".\.venv\Lib\site-packages\demucs\remote;demucs/remote/" `
    --hidden-import "eyed3" `
    --hidden-import "demucs" `
    --hidden-import "tinytag" `
    --hidden-import "wavinfo" `
    --hidden-import "numpy" `
    --collect-submodules "demucs" `
    --collect-submodules "numpy" `
    ".\src\gui.py"
```

# Outdated Nuitka Building Guide

### I wanted to use Nuitka, but ran into problems with Numpy

As a result, PyInstaller has been used instead. Outdated instructions are stilli included just in case :)

### Installing Nuitka

Nuitka can be installed using pip -- I prefer not to do so globally, so I just run the module later on rather than the global `nuitka` command. Install Nuitka via:

```powershell
pip install nuitka
```

### Building to a single executable

Again, if you install `nuitka` globally using the `-u` switch, then replace `python -m nuitka` with just `nuitka` 😉

```powershell
python -m nuitka `
    --onefile `
    --enable-plugin=pyside6 `
    --enable-plugin=numpy `
    --follow-import-to=numpy `
    --include-package-data=demucs `
    --output-filename="Drum Track Converter.exe" `
    --windows-icon-from-ico=assets\icon.ico `
    .\src\gui.py
```
