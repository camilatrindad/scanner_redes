#!/usr/bin/env bash
set -euo pipefail

echo "Script para gerar .exe com PyInstaller"

if [[ "$(uname -s)" != *"NT"* && "$(expr substr $(uname -s) 1 5)" != "MINGW" && "$(uname -s)" != "CYGWIN_NT-10.0" ]]; then
  echo "Aviso: é recomendado rodar este script em Windows para gerar .exe nativo."
  echo "Você pode usar uma VM/WSL2/Windows host. Tentando construir aqui mesmo..."
fi

python -m pip install --user -r requirements.txt


python -m PyInstaller --onefile --name scanner_dark scanner_dark.py

echo "Build concluído. Arquivo gerado em dist/"
