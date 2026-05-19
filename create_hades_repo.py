import os

files = {
'README.md': '# HADES vΩ — DEPREDADOR90\n\nSovereign AI Infrastructure · ARM64 · Termux\n\n

![Version](https://img.shields.io/badge/version-vΩ--DEPREDADOR90-crimson?style=for-the-badge)

\n

![Status](https://img.shields.io/badge/status-OPERATIVO-brightgreen?style=for-the-badge)

\n',
'.gitignore': 'node_modules/\n*.env\nvault/*.enc\nvault/*.key\nlogs/\n*.log\n__pycache__/\n.pm2/\n',
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
    open(path, 'w').write(content)
    print(f'OK: {path}')
