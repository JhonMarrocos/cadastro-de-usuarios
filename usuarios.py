# Bibliotecas Necessarias

from time import sleep as sl
import platform
import os
import stdiomask
import hashlib
import json

# VariáVeis Principais

usuarios = [] # Armazena (Email, Usuario, Senha) na variavel usuarios

local_arquivo = os.path.dirname(os.path.abspath(__file__)) # Localiza o script do programa

arquivo_json = os.path.join(local_arquivo, "cadastros.json") # Banco de dados dos cadastrados

# Funções

def limpar(): # Limpa o Terminal

    if platform.system() == "Windows":
        os.system("cls")

    else:
        os.system("clear")

def pausar(): # Pausa o terminal
    return input('ENTER para continuar...')

def loading(): # Barra de Loading similar ao usando no tqdm

    for n in range(101):
        i = "■" * (n * 25 // 101)
        print(f"\r{n}% {i}", end="", flush=True)
        sl(0.01)
    print()

def titulo(text): # Retorta um Cabeçalho

    linhas = "=" * 30
    return f"{linhas}\n{text.center(len(linhas))}\n{linhas}"

def encontrar_email(email): # Verifica se existe o email na lista de usuarios
    for i, item in enumerate(usuarios):
        if item["Email"] == email:
            return i
    return -1

def encontrar_usuario(usuario): # Verifica se existe o usuario na lista de usuarios
    for i, item in enumerate(usuarios):
        if item["Usuario"] == usuario:
            return i
    return -1

def criptografar_senha(senha): # Criptografa a senhas usando hash

    return hashlib.sha256(senha.encode()).hexdigest()

def carregar(): # Carrega os Dados dos usuarios cadastrados

    global usuarios

    try:
        with open(arquivo_json, "r", encoding="utf-8") as arq:
            usuarios = json.load(arq)

    except FileNotFoundError:
        escrever()

def escrever(): # Escreve/Atualiza dados dos usuarios cadastrados

    with open(arquivo_json, "w", encoding="utf-8") as arq:
        json.dump(usuarios, arq, indent=4, ensure_ascii=False)

def main(): # Corpo Principal do Programa
    while True:
        print(titulo("XYZ CORP"))
        print("|1| - Cadastrar\n|2| - Remover\n|3| - Logar\n|4| - Usuarios\n|0| - Sair")

        try:
            opc = int(input("\nEscolha Uma Opcao: "))
            loading()
            limpar()

            match opc:

                case 1:
                    while True:
                        email = str(input("Digite Seu Email: ")).strip()
                        limpar()

                        if not '@' in email or not '.com' in email:
                            print("Email inválido!")
                            pausar()
                            limpar()
                            continue

                        indice = encontrar_email(email)

                        if indice != -1:
                            print(f"O Email {email} ja Existe!")
                            pausar()
                            limpar()
                            continue

                        while True:
                            usuario = str(input("Digite um Nome de Usuario: ")).strip()
                            limpar()

                            indice = encontrar_usuario(usuario)

                            if indice != -1:
                                print(f"O Usuario {usuario} ja esta Cadastrado!")
                                pausar()
                                limpar()

                            else:
                                break

                        senha = str(input("Escolha uma Senha de no minimo 8 Caracteres: ")).strip()
                        limpar()

                        if len(senha) < 8:
                            print(f"A senha {senha} e invalida!")
                            pausar()
                            limpar()
                            continue

                        else:
                            usuarios.append({
                                "Email": email,
                                "Usuario": usuario,
                                "Senha": criptografar_senha(senha)
                            })

                            print("Cadastrando...")
                            loading()
                            print("\nCadastro Realizado com Sucesso!")
                            escrever()
                            pausar()
                            limpar()

                        break

                case 2:
                    login = str(input("Usuario: ")).strip()
                    senha = stdiomask.getpass(prompt='Senha: ', mask='*')
                    limpar()

                    idx = encontrar_usuario(login)

                    if idx != -1 and usuarios[idx]["Senha"] == criptografar_senha(senha):

                        remover = input(
                            "Tem certeza que deseja excluir a conta? ([S] || [N]): "
                        ).strip().upper()
                        limpar()

                        if remover == "S":
                            usuarios.pop(idx)
                            escrever()
                            print("Usuário removido com sucesso!")
                            pausar()
                            limpar()

                        elif remover == "N":
                            print("Voltando ao menu...")
                            loading()

                    else:
                        print("Usuario ou Senha Invalida!")
                        pausar()
                        limpar()

                case 3:
                    login = str(input("Usuario: ")).strip()
                    senha = stdiomask.getpass(prompt='Senha: ', mask='*')
                    limpar()

                    idx = encontrar_usuario(login)

                    if idx != -1 and usuarios[idx]["Senha"] == criptografar_senha(senha):
                        print(f"Bem Vindo {login}!")
                        pausar()
                        limpar()
                    
                    else:
                        print("Usuario ou Senha Invalida!")
                        pausar()
                        limpar()

                    continue

                case 4:
                    for i, item in enumerate(usuarios):
                        print(f"|{i+1}| - Nick: {item['Usuario']} Email: {item['Email']}")

                    print()
                    pausar()
                    limpar()
                    continue

                case 0:
                    print("Saindo...")
                    print("Ate Mais!")
                    sl(2)
                    break

                case _:
                    print("Opcao Invalida!")
                    pausar()
                    limpar()

        except ValueError:
            print("Digite Somente Numeros!")
            pausar()
            limpar()

# main
print('Iniciando...')
loading()
pausar()
limpar()
carregar()
main()