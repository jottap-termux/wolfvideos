#!/usr/bin/env python3
import os
import sys
import subprocess
import requests
import shutil
from time import sleep

# Configurações (ajustadas para Termux com SDCard)
HOME = os.path.expanduser("~")
PASTA_DOWNLOADS = "/sdcard/WolfVideos"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
ARQUIVO_COOKIES = "/sdcard/cookies.txt"
URL_ATUALIZACAO_COOKIES = "https://jottap-termux.github.io/cookies.txt"
ATUALIZAR_COOKIES_AUTO = True
TERMUX_PATH = "/data/data/com.termux/files/home/.local/bin"

def verificar_e_configurar_ambiente():
    """Verifica e configura todo o ambiente necessário"""
    print("\033[1;34m[•] Configurando ambiente...\033[0m")
    
    # Verifica se está no Termux
    is_termux = 'com.termux' in HOME
    
    # Configura PATH para Termux
    if is_termux:
        configurar_path_termux()
    
    # Cria pasta de downloads
    os.makedirs(PASTA_DOWNLOADS, exist_ok=True)
    print(f"\033[1;32m[✓] Pasta de downloads: {PASTA_DOWNLOADS}\033[0m")
    
    # Instala dependências
    if not instalar_dependencias_auto():
        sys.exit(1)
    
    # Configura cookies
    criar_cookies()
    
    # Atualiza cookies se necessário
    if ATUALIZAR_COOKIES_AUTO:
        atualizar_cookies()

def configurar_path_termux():
    """Configura o PATH para incluir binários do pip no Termux"""
    if TERMUX_PATH not in os.environ["PATH"]:
        with open(os.path.join(HOME, ".bashrc"), "a") as f:
            f.write(f'\nexport PATH="$PATH:{TERMUX_PATH}"\n')
        os.environ["PATH"] += f":{TERMUX_PATH}"
        print("\033[1;33m[•] PATH configurado para Termux\033[0m")

def instalar_dependencias_auto():
    """Instala automaticamente todas as dependências necessárias"""
    print("\033[1;34m[•] Instalando/Atualizando dependências...\033[0m")

    try:
        # Verifica se está no Termux
        is_termux = 'com.termux' in HOME

        if is_termux:
            # Comandos para Termux
            subprocess.run(["pkg", "update", "-y"], check=True)
            subprocess.run(["pkg", "upgrade", "-y"], check=True)
            subprocess.run(["pkg", "install", "-y", "python", "ffmpeg", "libxml2", "libxslt", "binutils"], check=True)
            
            # Instala pip se não existir
            if not shutil.which("pip"):
                subprocess.run(["pkg", "install", "-y", "python-pip"], check=True)
            
            # Instala yt-dlp e requests
            subprocess.run([sys.executable, "-m", "pip", "install", "--user", "--upgrade", "yt-dlp", "requests"], check=True)
            
            # Garante que o yt-dlp está acessível
            if not shutil.which("yt-dlp"):
                print("\033[1;33m[•] Configurando yt-dlp...\033[0m")
                subprocess.run(["ln", "-s", f"{TERMUX_PATH}/yt-dlp", f"{TERMUX_PATH}/yt-dlp"], check=True)
        else:
            # Comandos para Linux tradicional
            subprocess.run(["sudo", "apt", "update", "-y"], check=True)
            subprocess.run(["sudo", "apt", "upgrade", "-y"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "python3", "python3-pip", "ffmpeg"], check=True)
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp", "requests"], check=True)

        print("\033[1;32m[✓] Dependências instaladas/atualizadas!\033[0m")
        
        # Verifica instalação do yt-dlp
        if not verificar_yt_dlp():
            print("\033[1;31m[!] Falha crítica: yt-dlp não instalado corretamente\033[0m")
            return False
            
        return True
    except subprocess.CalledProcessError as e:
        print(f"\033[1;31m[!] Erro durante instalação: {e}\033[0m")
        if 'com.termux' in HOME:
            print("\033[1;33m[•] Solução manual no Termux:")
            print("  1. pkg update && pkg upgrade")
            print("  2. pkg install -y python ffmpeg libxml2 libxslt binutils")
            print("  3. pip install --user yt-dlp requests")
            print("  4. ln -s ~/.local/bin/yt-dlp ~/.local/bin/yt-dlp\033[0m")
        return False

def verificar_yt_dlp():
    """Verifica se o yt-dlp está instalado e acessível"""
    try:
        # Verifica se o comando existe
        if not shutil.which("yt-dlp"):
            # Tenta encontrar o caminho manualmente no Termux
            termux_ytdlp = f"{TERMUX_PATH}/yt-dlp"
            if os.path.exists(termux_ytdlp):
                os.environ["PATH"] += f":{TERMUX_PATH}"
                return True
            return False
        
        # Verifica a versão
        result = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"\033[1;32m[✓] yt-dlp versão {result.stdout.strip()} instalado\033[0m")
            return True
        return False
    except Exception:
        return False

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def mostrar_banner():
    print("""\033[1;36m
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣶⠶⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠁⠀⠸⠛⢳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠃⠀⠀⠀⠀⣿⠹⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠀⣿⠀⢿⠀⣴⠟⠷⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠃⠀⠀⠀⠀⢀⣤⡟⠀⢸⣿⠃⠀⠀⠘⣷⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠁⠀⠀⠀⠀⠀⣸⡿⠿⠟⢿⡏⠀⠀⠀⢀⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣾⠟⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⣼⡇⠀⠀⠀⣸⡏⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠛⡋⠉⣩⡇⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⣰⠟⠋⠁⠀⠀⢠⡟⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠏⢠⡞⣱⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠟⠀⠀⠀⠀⠀⣾⠃⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠃⢀⣿⢁⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⣠⢰⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠁⠀⢸⣿⣿⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⢀⣶⣾⡇⢸⣧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠀⠀⠀⢸⣿⣿⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣏⣠⢰⢻⡟⢃⡿⡟⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⡇⠀⠀⠀⠀⠁⢿⠹⣿⣄⠀⠀⠀⢀⠀⠀⠀⠀⢺⠏⣿⣿⠼⠁⠈⠰⠃⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡟⠃⠀⠈⢻⣷⣄⠈⠁⣿⣿⡇⠀⠀⠈⣧⠀⠀⠀⠘⣠⠟⠁⠀⠀⠀⠀⠀⢻⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣾⠟⠀⠀⣴⠀⠀⣿⡿⠀⠸⠋⢸⣿⣧⡐⣦⣸⡆⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠘⣿⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⡿⠃⠀⣀⣴⣿⡆⢀⣿⠃⠀⠀⠀⣸⠟⢹⣷⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣧⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣀⣤⣾⡏⠛⠻⠿⣿⣿⣿⠁⣼⠇⠀⠀⠀⠀⠁⠀⢸⣿⠙⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣇⠀⠀⠀⠀⠀
⠲⢾⣿⣿⣿⣿⣇⢀⣠⣴⣿⡿⢁⣼⣿⣀⠀⠀⠀⠀⠀⠀⠈⢿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣆⠀⠀⠀⠀
⠀⠀⠉⠙⠛⠻⣿⣷⣶⣿⣷⠾⣿⣵⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠙⠀⠀⠀⠀⠀⠀⠀⢤⡀⠀⠀⠀⠀⠀⠀⠀⡀⢿⡆⠀⠀⠀
⠀⠀⠀⠀⠀⣰⣿⡟⣴⠀⠀⠉⠉⠁⢿⡇⣴⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡆⠀⠀⠀⠀⣴⠀⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⢠⣿⠿⣿⣿⢠⠇⠀⠀⠀⢸⣿⢿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣀⠀⠀⢸⣿⡄⠀⠀⣼⣿⣇⢹⡟⢿⡇⠀⠀
⠀⠀⠀⠀⣿⠃⣠⣿⣿⣿⠀⠀⠀⠀⠀⢻⡈⢿⣆⠀⢳⡀⠀⢠⠀⠀⠀⠀⠀⢸⣿⣦⠀⣸⠿⣷⡀⠀⣿⣿⢿⣾⣿⠸⠇⠀⠀
⠀⠀⠀⠀⠋⣰⣿⣿⣿⣿⡀⢰⡀⠀⠀⠀⠀⠈⢻⣆⣼⣷⣄⠈⢷⡀⠀⠀⠀⢸⣿⢿⣶⠟⠀⠙⣷⣼⣿⣿⡄⠻⣿⣧⡀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣧⡿⠀⠀⠀⠀⠀⠀⠀⠙⢿⡄⠻⣷⣼⣿⣦⡀⠀⣼⠇⠸⠋⠀⠀⠀⠈⠻⣿⣿⣷⡀⠈⠻⣷⡀⠀
⠀⠀⠀⠀⠀⣿⣼⡿⢻⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠈⠻⣷⡙⣿⣶⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣷⢠⣀⠘⣷⡀
⠀⠀⠀⠀⠀⠀⣿⠇⣾⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠈⠛⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠀⢻⣷⣾⡇
⠀⠀⠀⠀⠀⠀⣿⢠⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠀⢈⣿⡹⣷
⠀⠀⠀⠀⠀⠀⠈⠀⠻⠿⠿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⡇⠉

██╗    ██╗ ██████╗ ██╗     ████████
██║    ██║██╔═══██╗██║     ██║
██║ █╗ ██║██║   ██║██║     ████████
██║███╗██║██║   ██║██║     ██
╚███╔███╔╝╚██████╔╝███████╗██╗
 ╚══╝╚══╝  ╚═════╝ ╚══════╝╚══════╝
 ██╗   ██╗██╗██████╗ ███████╗ ██████╗ ███████╗
 ██║   ██║██║██╔══██╗██╔════╝██╔═══██╗██╔════╝
 ██║   ██║██║██║  ██║█████╗  ██║   ██║███████╗
 ╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║╚════██║
  ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝███████║
   ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝
 \033[1;32m_______________________________________________
  • insta:jottap_62 • by jottap_62 • v4.3 • Wolf Edition• |
 ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
\033[1;33m• Recursos Premium:
  ✔ Download de vídeos 4K/1080p
  ✔ Conversão para MP3 com qualidade de estúdio
  ✔ Bypass de paywalls e restrições
  ✔ Sistema de cookies automático
  ✔ Player integrado com pré-visualização
  ✔ Suporte a múltiplas plataformas\033[0m""")

def criar_cookies():
    """Cria arquivo de cookies padrão se não existir"""
    try:
        if not os.path.exists(ARQUIVO_COOKIES):
            cookies_padrao = """# Netscape HTTP Cookie File
.xvideos.com    TRUE    /       FALSE   1735689600      ts      1
.xvideos.com    TRUE    /       FALSE   1735689600      platform      pc
.xvideos.com    TRUE    /       FALSE   1735689600      hash    5a8d9f8e7c6b5a4d3e2f1
"""
            with open(ARQUIVO_COOKIES, 'w') as f:
                f.write(cookies_padrao)
            print("\033[1;33m[•] Arquivo de cookies criado em:", ARQUIVO_COOKIES, "\033[0m")
    except PermissionError:
        print("\033[1;31m[!] Erro de permissão. Tentando criar cookies em local alternativo...\033[0m")
        # Usa um caminho alternativo dentro do Termux
        alt_cookies = os.path.join(HOME, ".cookies.txt")
        with open(alt_cookies, 'w') as f:
            f.write(cookies_padrao)
        print("\033[1;33m[•] Arquivo de cookies criado em:", alt_cookies, "\033[0m")
        return alt_cookies
    return ARQUIVO_COOKIES

def verificar_dependencias():
    """Verifica e instala dependências necessárias"""
    print("\033[1;34m[•] Verificando dependências...\033[0m")

    # Verifica yt-dlp
    try:
        subprocess.run(["yt-dlp", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("\033[1;32m[✓] yt-dlp já está instalado\033[0m")
    except:
        print("\033[1;33m[•] Instalando yt-dlp...\033[0m")
        subprocess.run([sys.executable, "-m", "pip", "install", "--user", "yt-dlp"], check=True)

    # Verifica ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("\033[1;32m[✓] ffmpeg já está instalado\033[0m")
    except:
        print("\033[1;31m[!] ffmpeg não encontrado. É necessário para conversão MP3.\033[0m")
        if 'com.termux' in HOME:
            print("\033[1;33m[•] Execute: pkg install ffmpeg -y\033[0m")
        else:
            print("\033[1;33m[•] Execute: sudo apt install ffmpeg -y\033[0m")

    # Verifica cookies
    if not os.path.exists(ARQUIVO_COOKIES):
        criar_cookies()
    else:
        print("\033[1;32m[✓] Arquivo de cookies encontrado\033[0m")

def atualizar_ferramentas():
    """Atualiza o yt-dlp corretamente via pip"""
    print("\033[1;33m[•] Atualizando ferramentas...\033[0m")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--user", "--upgrade", "yt-dlp", "requests"], check=True)
        print("\033[1;32m[✓] Ferramentas atualizadas com sucesso!\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Erro ao atualizar: {e}\033[0m")

def atualizar_cookies():
    """Atualiza cookies a partir da URL"""
    try:
        print("\033[1;34m[•] Baixando novos cookies...\033[0m")
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(URL_ATUALIZACAO_COOKIES, headers=headers, timeout=10)

        if response.status_code == 200:
            with open(ARQUIVO_COOKIES, 'w') as f:
                f.write(response.text)
            print("\033[1;32m[✓] Cookies atualizados com sucesso!\033[0m")
        else:
            print("\033[1;31m[!] Falha ao baixar cookies. Status code:", response.status_code, "\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Erro ao atualizar cookies: {str(e)}\033[0m")

def listar_formatos(link):
    """Lista os formatos disponíveis para download"""
    print("\033[1;36m[•] Listando formatos disponíveis...\033[0m")
    try:
        subprocess.run(f'yt-dlp --cookies "{ARQUIVO_COOKIES}" -F "{link}"', shell=True)
    except Exception as e:
        print(f"\033[1;31m[!] Erro ao listar formatos: {str(e)}\033[0m")

def baixar_video(link, formato='mp4', qualidade=None):
    """Executa o download com múltiplas estratégias"""
    tentativas = [
        f'yt-dlp --user-agent "{USER_AGENT}" --cookies "{ARQUIVO_COOKIES}" --no-check-certificate',
        f'yt-dlp --user-agent "{USER_AGENT}" --cookies "{ARQUIVO_COOKIES}" --force-generic-extractor',
        'yt-dlp --ignore-errors'
    ]

    for tentativa, cmd in enumerate(tentativas, 1):
        print(f"\n\033[1;35m[•] Tentativa {tentativa}/3\033[0m")

        output_template = f'"{PASTA_DOWNLOADS}/%(title)s.%(ext)s"'

        if formato == 'mp3':
            comando = f'{cmd} -x --audio-format mp3 --audio-quality 0 -o {output_template} "{link}"'
        elif qualidade:
            comando = f'{cmd} -f {qualidade} --merge-output-format {formato} -o {output_template} "{link}"'
        else:
            comando = f'{cmd} -f bestvideo+bestaudio/best --merge-output-format {formato} -o {output_template} "{link}"'

        try:
            resultado = subprocess.run(comando, shell=True)
            if resultado.returncode == 0:
                print(f"\033[1;32m[✓] Download concluído com sucesso!\033[0m")
                return True
        except Exception as e:
            print(f"\033[1;31m[!] Erro na tentativa {tentativa}: {str(e)}\033[0m")

    print("\033[1;31m[!] Todas as tentativas falharam. Verifique sua conexão e a URL.\033[0m")
    return False

def mostrar_menu_config():
    global ATUALIZAR_COOKIES_AUTO
    while True:
        clear_screen()
        print("""\033[1;36m
╔════════════════════════════════════════╗
║           ⚙️  CONFIGURAÇÕES             ║
╠════════════════════════════════════════╣
║ 1. {} Atualização automática de cookies║
║ 2. ⚡ Instalar todas as dependências    ║
║ 0. 🔙 Voltar ao menu principal         ║
╚════════════════════════════════════════╝
\033[0m""".format("✅" if ATUALIZAR_COOKIES_AUTO else "❌"))

        opcao = input("\n\033[1;36m⚙️ Escolha uma opção: \033[0m").strip()

        if opcao == "0":
            break
        elif opcao == "1":
            ATUALIZAR_COOKIES_AUTO = not ATUALIZAR_COOKIES_AUTO
            status = "ativada" if ATUALIZAR_COOKIES_AUTO else "desativada"
            print(f"\033[1;32m[✓] Atualização automática de cookies {status}\033[0m")
            sleep(1)
        elif opcao == "2":
            instalar_dependencias_auto()
            input("\n\033[1;36mPressione Enter para continuar...\033[0m")
        else:
            print("\033[1;31m[!] Opção inválida. Tente novamente.\033[0m")
            sleep(1)

def mostrar_menu_principal():
    print("""\033[1;36m
╔════════════════════════════════════════╗
║    🎬 WOLF VIDEO DOWNLOADER PREMIUM    ║
╠════════════════════════════════════════╣
║ 1. 🎥 Baixar vídeo (melhor qualidade)  ║
║ 2. 📊 Escolher qualidade específica    ║
║ 3. 🎧 Converter para MP3               ║
║ 4. 📋 Listar formatos disponíveis      ║
║ 5. 🔄 Atualizar ferramentas            ║
║ 6. 🍪 Atualizar cookies manualmente    ║
║ 7. ⚙️ Configurações                     ║
║ 0. 🚪 Sair                             ║
╚════════════════════════════════════════╝
\033[0m""")

def main():
    clear_screen()
    mostrar_banner()
    
    # Configuração completa do ambiente
    verificar_e_configurar_ambiente()
    
    # Verifica se é Termux e ajusta permissões
    if 'com.termux' in HOME:
        print("\033[1;33m[•] Modo Termux detectado\033[0m")
        if not os.path.exists(PASTA_DOWNLOADS):
            os.makedirs(PASTA_DOWNLOADS, mode=0o755, exist_ok=True)

    while True:
        mostrar_menu_principal()
        opcao = input("\n\033[1;36m✨ Escolha uma opção [0-7]: \033[0m").strip()

        if opcao == "0":
            print("\n\033[1;32m[✓] Programa encerrado.\033[0m")
            break
        elif opcao == "7":
            mostrar_menu_config()
        elif opcao == "6":
            atualizar_cookies()
        elif opcao == "5":
            atualizar_ferramentas()
        elif opcao in ["1", "2", "3", "4"]:
            link = input("\n\033[1;36m🔗 Digite a URL do vídeo: \033[0m").strip()

            if not link.startswith(('http://', 'https://')):
                print("\033[1;31m[!] URL inválida. Deve começar com http:// ou https://\033[0m")
                continue

            if opcao == "4":
                listar_formatos(link)
            elif opcao == "3":
                if baixar_video(link, 'mp3'):
                    print(f"\033[1;32m[✓] Arquivo salvo em: {PASTA_DOWNLOADS}\033[0m")
            elif opcao == "1":
                if baixar_video(link, 'mp4'):
                    print(f"\033[1;32m[✓] Arquivo salvo em: {PASTA_DOWNLOADS}\033[0m")
            elif opcao == "2":
                listar_formatos(link)
                qualidade = input("\n\033[1;36m🔢 Digite o código do formato desejado (ex: 137+140 ou 22): \033[0m").strip()
                if baixar_video(link, 'mp4', qualidade):
                    print(f"\033[1;32m[✓] Arquivo salvo em: {PASTA_DOWNLOADS}\033[0m")
        else:
            print("\033[1;31m[!] Opção inválida. Tente novamente.\033[0m")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[1;31m[!] Programa interrompido pelo usuário.\033[0m")
        sys.exit(0)
