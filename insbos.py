import os
import requests
import shutil
import ctypes
import sys

def download_file(url, local_filename):
    """Baixa um arquivo da URL para o caminho local especificado."""
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

def set_env_var(path):
    """Configura a variável de ambiente do sistema."""
    current_path = os.environ.get('PATH', '')
    if path not in current_path:
        new_path = current_path + ";" + path
        os.environ['PATH'] = new_path
        # Atualiza a variável de ambiente do sistema
        reg_key = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        ctypes.windll.advapi32.RegSetValueExW(
            ctypes.windll.advapi32.RegOpenKeyExW(
                0x80000000, reg_key, 0, 0x20006
            ), 
            'Path', 0, 1, new_path.encode('utf-16le'), len(new_path.encode('utf-16le'))
        )
        print(f'Variável de ambiente PATH atualizada com: {path}')

def install_bos():
    """Instala o BOS e configura a variável de ambiente."""
    bos_url = 'https://github.com/SEU_USUARIO/bos-installer/raw/main/bos.py'
    download_file(bos_url, 'bos.py')

    print("Escolha onde instalar o BOS:")
    print("1. Instalar para o usuário atual")
    print("2. Instalar para todos os usuários")
    choice = input("Digite o número da opção desejada: ")

    if choice == '1':
        install_path = os.path.expanduser("~\\bos")
    elif choice == '2':
        install_path = r"C:\Program Files\BOS"
    else:
        print("Opção inválida.")
        sys.exit(1)

    # Cria o diretório de instalação se não existir
    if not os.path.exists(install_path):
        os.makedirs(install_path)

    # Move o arquivo BOS para o diretório de instalação
    shutil.move('bos.py', os.path.join(install_path, 'bos.py'))

    # Configura a variável de ambiente
    set_env_var(install_path)

    print("Instalação concluída com sucesso.")
    print(f"BOS instalado em {install_path}")

if __name__ == '__main__':
    install_bos()
