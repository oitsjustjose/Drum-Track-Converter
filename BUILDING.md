# Building using Nuitka

## Installing Nuitka

Nuitka can be installed using pip -- I prefer not to do so globally, so I just run the module later on rather than the global `nuitka` command. Install Nuitka via:

```powershell
pip install nuitka
```

## Building to a single executable

Again, if you install `nuitka` globally using the `-u` switch, then replace `python -m nuitka` with just `nuitka` 😉

```powershell
python -m nuitka `
    --onefile `
    --enable-plugin=pyqt6 `
    --output-filename=Drum\ Track\ Converter.exe `
    --windows-icon-from-ico=icon.png `
    .\src\gui.py
```
