# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['eyed3', 'demucs', 'tinytag', 'wavinfo', 'numpy']
hiddenimports += collect_submodules('demucs')
hiddenimports += collect_submodules('numpy')


a = Analysis(
    ['src\\gui.py'],
    pathex=[],
    binaries=[],
    datas=[('.\\src', 'src/'), ('.\\assets\\icon.ico', 'assets/icon.ico.'), ('.\\.venv\\Lib\\site-packages\\demucs\\remote', 'demucs/remote/')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Drum Track Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\icon.ico'],
)
