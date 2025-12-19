#!/usr/bin/env bash
set -euo pipefail

VERSION=${1:-1.0.0}
ARCH=$(dpkg --print-architecture || echo "amd64")

echo "Gerando binário com PyInstaller (Linux)..."
python3 -m pip install --user -r requirements.txt
python3 -m PyInstaller --onefile --name scanner_dark scanner_dark.py

PKGDIR=package_dir
rm -rf "$PKGDIR"
mkdir -p "$PKGDIR"/usr/bin

echo "Copiando binário para pacote..."
cp dist/scanner_dark "$PKGDIR"/usr/bin/scanner_dark

mkdir -p "$PKGDIR"/DEBIAN
cat > "$PKGDIR"/DEBIAN/control <<EOF
Package: scanner-dark
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Maintainer: Seu Nome <you@example.com>
Description: Scanner dark - empacotado a partir de scanner_dark.py
EOF

echo "Construindo .deb..."
dpkg-deb --build "$PKGDIR" "scanner-dark_${VERSION}_${ARCH}.deb"

echo "Pacote criado: scanner-dark_${VERSION}_${ARCH}.deb"
