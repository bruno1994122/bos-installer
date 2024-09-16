import os
import subprocess
import datetime
import shutil
import sys
import signal
from colorama import Fore, init

# Diretório de plugins
PLUGIN_DIR = 'plugins'

# Dicionário para armazenar variáveis e comandos personalizados
variables = {}
custom_commands = {}

# Inicialização do Colorama
init(autoreset=True)

def load_plugins():
    """Carrega todos os plugins do diretório PLUGIN_DIR."""
    if os.path.isdir(PLUGIN_DIR):
        for file_name in os.listdir(PLUGIN_DIR):
            if file_name.endswith('.bos'):
                plugin_path = os.path.join(PLUGIN_DIR, file_name)
                print(f"Carregando plugin: {plugin_path}")
                try:
                    with open(plugin_path) as f:
                        exec(f.read(), variables)
                except Exception as e:
                    print(f"Erro ao carregar o plugin {plugin_path}: {e}")

def execute_script(script_path):
    """Executa um script BOS a partir do caminho especificado."""
    with open(script_path, 'r') as file:
        for line in file:
            execute_action(line.strip())

def execute_action(action):
    action = replace_variables(action)  # Substitui variáveis no comando
    parts = action.split()
    command = parts[0]
    args = parts[1:]
    
    if command == "print":
        print_text(' '.join(args))
    elif command == "if":
        condition = args[0]
        action = ' '.join(args[2:])
        if_then(condition, action)
    elif command in ['cd', 'ls', 'touch', 'rm', 'mkdir', 'rmdir', 'cat', 'mv', 'cp']:
        file_commands(command, *args)
    elif command == "echo":
        if len(args) > 1:
            echo(' '.join(args[:-1]), args[-1])
        else:
            echo(' '.join(args))
    elif command == "date":
        date()
    elif command == "clear":
        clear()
    elif command == "exit":
        exit_program()
    elif command == "whoami":
        whoami()
    elif command == "uname":
        uname()
    elif command == "chmod":
        chmod(args[0], args[1])
    elif command == "ps":
        ps()
    elif command == "kill":
        kill(args[0])
    elif command == "shell":
        shell(' '.join(args))
    elif command == "set":
        if len(args) < 2:
            print("Erro: Comando 'set' precisa de dois argumentos: nome e valor.")
        else:
            set_variable(args[0], ' '.join(args[1:]))
    elif command == "input":
        input_command(args[0])
    elif command == "help":
        help()
    elif command == "exe":
        if args:
            exe(args[0])
        else:
            print("Erro: Comando 'exe' precisa de um argumento: nome do arquivo.")
    elif command == "plugin":
        if args:
            if args[0] == '-la':
                load_plugins()
            elif args[0] == '-ls':
                list_plugins()
            elif args[0] == '-a' and len(args) > 1:
                add_plugin(args[1])
            else:
                print("Erro: Comando 'plugin' requer '-la', '-ls', ou '-a <caminho>' como argumento.")
        else:
            print("Erro: Comando 'plugin' requer um argumento.")
    else:
        print(f"Comando desconhecido: {command}")

def replace_variables(action):
    """Substitui variáveis no comando."""
    for var_name, var_value in variables.items():
        action = action.replace(f"@({var_name})", var_value)
    return action

def print_text(text):
    print(text)

def if_then(condition, action):
    """Executa uma ação se a condição for verdadeira."""
    if eval(condition, {}, variables):
        execute_action(action)

def file_commands(command, *args):
    """Executa comandos de manipulação de arquivos e diretórios."""
    try:
        if command == 'cd':
            os.chdir(args[0])
        elif command == 'ls':
            print('\n'.join(os.listdir('.')))
        elif command == 'touch':
            with open(args[0], 'a'):
                os.utime(args[0], None)
        elif command == 'rm':
            os.remove(args[0])
        elif command == 'mkdir':
            os.mkdir(args[0])
        elif command == 'rmdir':
            os.rmdir(args[0])
        elif command == 'cat':
            with open(args[0], 'r') as f:
                print(f.read())
        elif command == 'mv':
            shutil.move(args[0], args[1])
        elif command == 'cp':
            shutil.copy(args[0], args[1])
    except Exception as e:
        print(f"Erro ao executar comando '{command}': {e}")

def echo(text, file=None):
    """Imprime um texto na tela ou o grava em um arquivo."""
    if file:
        with open(file, 'a') as f:
            f.write(text + '\n')
    else:
        print(text)

def date():
    """Exibe a data e hora atual."""
    print(datetime.datetime.now())

def clear():
    """Limpa o terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def exit_program():
    """Encerra o programa."""
    print("Saindo...")
    exit()

def whoami():
    """Exibe o nome do usuário atual."""
    print(os.getlogin())

def uname():
    """Exibe o nome do sistema operacional."""
    print(os.name)

def chmod(permission, file):
    """Altera permissões de um arquivo."""
    os.chmod(file, int(permission, 8))

def ps():
    """Exibe os processos em execução."""
    subprocess.run(['ps', 'aux'])

def kill(pid):
    """Encerra um processo pelo PID."""
    os.kill(int(pid), signal.SIGTERM)

def shell(command):
    """Executa um comando no shell."""
    subprocess.run(command, shell=True)

def set_variable(name, value):
    """Define uma variável."""
    variables[name] = value

def input_command(var_name):
    """Solicita uma entrada do usuário e armazena em uma variável."""
    variables[var_name] = input("Digite o valor: ")

def help():
    """Exibe a ajuda com os comandos disponíveis."""
    help_text = """
Comandos disponíveis:

Arquivos e Diretórios:
- cd <caminho>         : Muda o diretório atual.
- ls                  : Lista arquivos e diretórios no diretório atual.
- touch <arquivo>     : Cria um arquivo vazio ou atualiza a data de modificação.
- rm <arquivo>        : Remove um arquivo.
- mkdir <diretório>   : Cria um diretório.
- rmdir <diretório>   : Remove um diretório.
- cat <arquivo>       : Exibe o conteúdo de um arquivo.
- mv <origem> <destino> : Move ou renomeia um arquivo ou diretório.
- cp <origem> <destino> : Copia um arquivo ou diretório.

Execução e Variáveis:
- exe <arquivo>       : Executa um script Python (.py).
- nc <nome_comando> then <ação> : Define um novo comando personalizado.
- call <nome_comando> : Chama um comando personalizado.
- print <texto>       : Imprime um texto na tela.
- echo <texto> [<arquivo>] : Imprime um texto na tela ou o grava em um arquivo.
- date                : Exibe a data e hora atual.
- clear               : Limpa o terminal.
- exit                : Encerra o programa.
- whoami              : Exibe o nome do usuário atual.
- uname               : Exibe o nome do sistema operacional.
- chmod <permissão> <arquivo> : Altera permissões de um arquivo.
- ps                  : Exibe os processos em execução.
- kill <PID>           : Encerra um processo pelo PID.
- shell <comando>     : Executa um comando no shell.
- set <variável> <valor> : Define uma variável.
- input <variável>    : Solicita uma entrada do usuário e armazena em uma variável.
- help                : Exibe esta ajuda.
- plugin -la          : Carrega todos os plugins.
- plugin -ls          : Lista todos os plugins carregados.
- plugin -a <caminho> : Adiciona um novo plugin.

Para mais detalhes, consulte a documentação.
"""
    print(help_text)

def exe(file):
    """Executa um script Python (.py)."""
    if os.path.isfile(file):
        subprocess.run(['python', file])
    else:
        print(f"Erro: Arquivo '{file}' não encontrado.")

def add_plugin(plugin_path):
    """Adiciona um plugin ao diretório PLUGIN_DIR."""
    if not os.path.exists(PLUGIN_DIR):
        os.makedirs(PLUGIN_DIR)
    shutil.copy(plugin_path, PLUGIN_DIR)
    print(f"Plugin adicionado: {plugin_path}")

def list_plugins():
    """Lista todos os plugins no diretório PLUGIN_DIR."""
    if os.path.exists(PLUGIN_DIR):
        plugins = os.listdir(PLUGIN_DIR)
        print("Plugins disponíveis:")
        for plugin in plugins:
            print(f"- {plugin}")
    else:
        print("Nenhum plugin encontrado.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        script_file = sys.argv[1]
        if os.path.isfile(script_file):
            load_plugins()
            execute_script(script_file)
        else:
            print(f"Erro: Arquivo '{script_file}' não encontrado.")
    else:
        print("Uso: python bos.py <script.bos>")
