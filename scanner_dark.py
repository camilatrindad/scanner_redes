import os
import socket
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
except ImportError:
    A4 = None
    canvas = None
from datetime import datetime
dispositivos = {}
portas_abertas = []  

def escanear_rede():
    dispositivos.clear()
    resultado.delete("1.0", tk.END)

    ip_base_raw = entrada_ip.get().strip()
    if not ip_base_raw:
        messagebox.showerror("Erro", "Digite o IP base")
        return

    ip_base_raw = ip_base_raw.rstrip('.')
    partes = ip_base_raw.split('.')
    if len(partes) >= 4:
        ip_base = '.'.join(partes[:3])
    elif len(partes) == 3:
        ip_base = ip_base_raw
    else:
        messagebox.showerror("Erro", "Informe pelo menos os 3 primeiros octetos (ex: 192.168.0)")
        return

    botao_rede.config(state="disabled")
    resultado.insert(tk.END, f"Iniciando scan na rede {ip_base}.0/24...\n")

    def scan():
        # verifica se o comando ping está disponível
        ping_ok = True
        try:
            subprocess.run(["ping", "-c", "1", "-W", "1", "127.0.0.1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            ping_ok = False

        for i in range(1, 255):
            ip = f"{ip_base}.{i}"
            alive = False

            if ping_ok:
                try:
                    res = subprocess.run(["ping", "-c", "1", "-W", "1", ip],
                                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    if res.returncode == 0:
                        alive = True
                except Exception:
                    ping_ok = False

            if not alive:
                
                for p in (80, 443):
                    try:
                        s = socket.socket()
                        s.settimeout(0.4)
                        if s.connect_ex((ip, p)) == 0:
                            alive = True
                            s.close()
                            break
                        s.close()
                    except Exception:
                        pass

            if alive:
                dispositivos[ip] = []
                janela.after(0, lambda ip=ip: resultado.insert(tk.END, f"🟢 Ativo: {ip}\n"))

        def finish():
            resultado.insert(tk.END, "\n✔ Scan de rede finalizado\n")
            botao_rede.config(state="normal")

        janela.after(0, finish)

    threading.Thread(target=scan, daemon=True).start()

def escanear_portas():
    portas_abertas.clear()
    resultado.delete("1.0", tk.END)
    ip_raw = entrada_ip_porta.get().strip()
    if not ip_raw:
        messagebox.showerror("Erro", "Digite o IP para escanear portas")
        return

    try:
        ip = socket.gethostbyname(ip_raw)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível resolver o host: {e}")
        return

    resultado.insert(tk.END, f"Iniciando scan de portas em {ip} ({ip_raw})...\n")
    botao_portas.config(state="disabled")

    portas = [22, 80, 443, 3389]

    def scan_ports():
        for p in portas:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.0)
                ret = s.connect_ex((ip, p))
                s.close()
                if ret == 0:
                    portas_abertas.append(p)
                    janela.after(0, lambda p=p: resultado.insert(tk.END, f"🟢 Porta {p} aberta\n"))
                else:
                    janela.after(0, lambda p=p: resultado.insert(tk.END, f"🔒 Porta {p} fechada/filtrada\n"))
            except Exception as e:
                janela.after(0, lambda p=p, e=e: resultado.insert(tk.END, f"Erro checando porta {p}: {e}\n"))

        janela.after(0, lambda: botao_portas.config(state="normal"))
        janela.after(0, lambda: resultado.insert(tk.END, "\n✔ Scan de portas finalizado\n"))

    threading.Thread(target=scan_ports, daemon=True).start()

def gerar_pdf():
    if canvas is None:
        messagebox.showerror("Erro", "Pacote 'reportlab' não encontrado. Instale reportlab para gerar PDF (ex.: .venv/bin/python -m pip install reportlab)")
        return

    if not dispositivos:
        messagebox.showwarning("Aviso", "Nenhum dado para gerar relatório")
        return

    nome_arquivo = f"relatorio_scanner_{datetime.now().strftime('%d%m%Y_%H%M')}.pdf"
    pdf = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    y = altura - 50
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Relatório de Scanner de Rede")
    y -= 30

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    y -= 30

    pdf.drawString(50, y, "Dispositivos Ativos:")
    y -= 20

    for ip in dispositivos:
        pdf.drawString(60, y, f"- {ip}")
        y -= 15
        if y < 50:
            pdf.showPage()
            y = altura - 50

    if portas_abertas:
        y -= 20
        pdf.drawString(50, y, "Portas Abertas Encontradas:")
        y -= 20
        for porta in portas_abertas:
            pdf.drawString(60, y, f"- Porta {porta}")
            y -= 15

    pdf.save()
    messagebox.showinfo("PDF Gerado", f"Relatório salvo como:\n{nome_arquivo}")



janela = tk.Tk()
janela.title("Scanner de Rede e Portas")
janela.geometry("600x500")
janela.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

style.configure(".", background="#1e1e1e", foreground="white")
style.configure("TLabel", background="#1e1e1e", foreground="white")
style.configure("TButton", background="#333", foreground="white")
style.configure("TEntry", fieldbackground="#333", foreground="white")

ttk.Label(janela, text="Scanner de Rede e Portas", font=("Arial", 16, "bold")).pack(pady=10)

frame1 = ttk.Frame(janela)
frame1.pack(pady=5)

ttk.Label(frame1, text="IP base:").grid(row=0, column=0, padx=5)
entrada_ip = ttk.Entry(frame1, width=20)
entrada_ip.grid(row=0, column=1)
entrada_ip.insert(0, "192.168.0")

botao_rede = ttk.Button(frame1, text="Escanear Rede", command=escanear_rede)
botao_rede.grid(row=0, column=2, padx=10)

frame2 = ttk.Frame(janela)
frame2.pack(pady=5)

ttk.Label(frame2, text="IP para portas:").grid(row=0, column=0, padx=5)
entrada_ip_porta = ttk.Entry(frame2, width=20)
entrada_ip_porta.grid(row=0, column=1)

botao_portas = ttk.Button(frame2, text="Escanear Portas", command=escanear_portas)
botao_portas.grid(row=0, column=2, padx=10)

resultado = ScrolledText(
    janela, width=70, height=15,
    bg="#111", fg="white", insertbackground="white"
)
resultado.pack(padx=10, pady=10)

ttk.Button(janela, text="Gerar Relatório em PDF", command=gerar_pdf).pack(pady=10)

janela.mainloop()
