# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['runserver.py'],
    pathex=['D:/ProjectPy/SMIP/src'],
    binaries=[],
    datas=[
        ('D:/ProjectPy/SMIP/db.sqlite3', '.'),
        ('D:/ProjectPy/SMIP/src/config/*', 'config'),
        ('D:/ProjectPy/SMIP/src/static/*', 'static'),
        ('D:/ProjectPy/SMIP/src/templates/*', 'templates'),  # Include templates if needed
    ],
    hiddenimports=[],
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
    name='MyDjangoApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MyDjangoApp',
    workpath='D:/ProjectPy/SMIP/src/build',
    distpath='D:/ProjectPy/SMIP/src/dist'
)
