# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['token_counter_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('themes/*.json', 'themes'),  # Include theme files
        ('services', 'services'),      # Include services folder
        ('styles', 'styles'),          # Include styles folder
        ('config.json', '.'),          # Include config if exists
    ],
    hiddenimports=[
        'customtkinter',
        'tkinterdnd2',
        'tiktoken',
        'tiktoken_ext.openai_public',
        'tiktoken_ext',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TokenCounter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want to see console output
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # Add your icon file if you have one
)