# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['KonTinkerer.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.datas += [('conNCW06.exe','C:\\Users\\dongd\\OneDrive\\Documents\\GitHub\\ShrinkRay\\Resources\\conNCW06.exe', 'Data')]
a.datas += [('ffmpegReduced.exe','C:\\Users\\dongd\\OneDrive\\Documents\\GitHub\\ShrinkRay\\Resources\\ffmpegReduced.exe', 'Data')]
a.datas += [('micReplace.ncw','C:\\Users\\dongd\\OneDrive\\Documents\\GitHub\\ShrinkRay\\Resources\\micReplace.ncw', 'Data')]
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='KonTinkerer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )