# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['delete.png', 'deleteD.png', 'edit.png', 'edit.py', 'editD.png', 'icon.png', 'limits.db', 'main.py', 'main.pyw', 'profiles.db'],
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
    name='delete',
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
    name='delete',
)
app = BUNDLE(
    coll,
    name='delete.app',
    icon='icon.png',
    bundle_identifier=None,
)
