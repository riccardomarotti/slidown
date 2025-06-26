# -*- mode: python -*-

import os
import shutil

block_cipher = None

def reveal_js_path():
    """Include reveal.js files from root directory"""
    paths = []
    reveal_root = 'reveal.js'
    if os.path.exists(reveal_root):
        for root, dirs, files in os.walk(reveal_root):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, '.')
                paths.append((full_path, os.path.dirname(rel_path)))
    return paths

def get_system_binaries():
    """Get system binaries for pandoc, wkhtmltopdf, and xdg-open"""
    binaries = []
    
    # Add pandoc
    pandoc_path = shutil.which('pandoc')
    if pandoc_path:
        binaries.append((pandoc_path, 'pandoc'))
    
    # Add wkhtmltopdf
    wkhtmltopdf_path = shutil.which('wkhtmltopdf')
    if wkhtmltopdf_path:
        binaries.append((wkhtmltopdf_path, 'wkhtmltopdf'))
    
    # Add xdg-open for browser opening
    xdg_open_path = shutil.which('xdg-open')
    if xdg_open_path:
        binaries.append((xdg_open_path, 'xdg-open'))
    
    return binaries

a = Analysis(['slidown/main.py'],
             pathex=['slidown'],
             binaries=get_system_binaries(),
             datas=reveal_js_path() + [('icon/slidown.png', 'icon')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='slidown',
          debug=False,
          strip=True,
          upx=True,
          console=False,
          icon='icon/slidown.png' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=True,
               upx=True,
               name='slidown')
