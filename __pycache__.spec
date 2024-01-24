# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['__pycache__', 'build', 'delete.png', 'delete.spec', 'deleteD.png', 'dist', 'edit.png', 'edit.py', 'editD.png', 'icon.png', 'limits.db', 'main.py', 'main.pyw', 'profiles.db'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='__pycache__',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='__pycache__',
)
app = BUNDLE(
    coll,
    name='__pycache__.app',
    icon='icon.png',
    bundle_identifier=None,
)
