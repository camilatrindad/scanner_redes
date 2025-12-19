Scanner Dark — Empacotamento
=================================

Instruções rápidas para gerar executáveis e pacote .deb do projeto.

Requisitos
- Python 3.8+
- Em Linux: `dpkg-deb` para criar o .deb
- Em Windows: recomenda-se rodar o `build_exe.sh` diretamente no Windows (ou numa VM)

Instalar dependências (opcional, recomendado em venv):

```bash
python -m pip install -r requirements.txt
```

Gerar EXE (Windows)

Recomendado: abra um prompt/Powershell no Windows, ative seu ambiente e rode:

```powershell
python -m pip install -r requirements.txt
python -m PyInstaller --onefile --name scanner_dark scanner_dark.py
# exe ficará em dist\scanner_dark.exe
```

Ou (no Linux) executar o script de conveniência (pode não gerar um exe nativo válido):

```bash
./build_exe.sh
```

Gerar DEB (Linux)

```bash
chmod +x build_deb.sh
./build_deb.sh 1.0.0
# gera scanner-dark_1.0.0_<arch>.deb
```

Observações
- O `.exe` é normalmente gerado em Windows. Cross-compilar de Linux para Windows requer ferramentas/ambientes adicionais.
- O script `build_deb.sh` usa PyInstaller para gerar um binário Linux e `dpkg-deb` para empacotar.
- Personalize o `control` em `build_deb.sh` com seu nome e email.
