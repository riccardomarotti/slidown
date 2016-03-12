# -*- mode: python -*-

import os

block_cipher = None

def reveal_js_path():
    paths = []
    for root, dirs, files in os.walk('slidown/reveal.js'):
        for name in dirs:
            full_path = os.path.join(root, name)
            paths.append((os.path.join(full_path, '*'),
                          full_path.split('slidown/')[1]))

    return paths

a = Analysis(['slidown/slidown.py'],
             pathex=['slidown'],
             binaries=[(os.popen('which pandoc').read().strip(), 'pandoc')],
             datas=reveal_js_path(),
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='slidown',
          debug=False,
          strip=True,
          upx=True,
          console=False )
