import datetime
import msvcrt
import locale
import time
import sys
import os

OP_POR_DIA = 10
encoding = locale.getpreferredencoding()

def criarUsuário() -> dict:
    nome = input("Digite seu nome: ")
    nascimento = datetime.datetime.strptime(input("Digite sua data de nascimento(dd/mm/AAAA)\n"), "%d/%m/%Y")
    cpf = input("Digite seu CPF apenas com números\n")
    endereço = input("Digite seu endereço da seguinte forma: logradouro, n° - bairro - cidade/sigla estado\n")
    senha = input("Digite sua senha\n")
    return {"nome": nome, "nascimento": nascimento, "cpf": cpf, "endereço": endereço, "senha": senha, "extrato": []}


def criarConta(tamanho, usuário) -> dict:
    if not usuário:
        print("Faça login ou crie um novo usuário para criar uma conta.\n")
        time.sleep(2)
        return
    
    print(f"Criando conta, Agência n° 0001, número {tamanho + 1}, usuário: {usuário["nome"]}")
    print("Conta criada com sucesso, faça login para usar. \nSaindo...")
    time.sleep(2)
    return {"agência": "0001", "número": tamanho + 1, "usuário": usuário, "saldo": 0, "dia": datetime.datetime.now().day, "limite": OP_POR_DIA}


def login(usuário, contas = None, opt = None) -> dict:
    print("O(a) Senhor(a) possui as seguintes contas disponíveis:")
    contasUsuário = [conta for conta in contas if conta["usuário"]["cpf"] == usuário["cpf"]]
    if not contasUsuário:
        print("Você não tem contas disponíveis. Crie uma primeiro.")
        print("Aperte uma tecla para retornar.")
        msvcrt.getch()
        return
    
    for conta in contasUsuário:
        print(f"agência: {conta["agência"]} | número {conta["número"]}")
        
    select = int(input("\nDigite o número da conta desejada: "))
    while not (conta := next((conta for conta in contasUsuário if conta["número"] == select), None)):
        select = input("Digite o número da conta desejada: ")
        if select.isdigit():
            select = int(select)
            
    return conta


def saque(*, valor, conta):
    if conta["saldo"] < valor:
        print("Saldo indisponível...")
        print("Pressione uma tecla para retornar")
        msvcrt.getch()
        return
    
    if conta["limite"] <= 0:
        print("Limite de operações diárias dessa conta atingido.")
        print("Pressione uma tecla para retornar")
        msvcrt.getch()
        return
    
    conta["saldo"] -= valor
    conta["usuário"]["extrato"].append(f"Conta: {conta["número"]} \t Saque: \t\t{valor}")
    print("Saque efetuado com sucesso")
    print("Pressione uma tecla para retornar")
    msvcrt.getch()
    return


def depósito(valor, conta, /):
    if conta["limite"] <= 0:
        print("Limite de operações diárias dessa conta atingido")
        return
    
    conta["saldo"] += valor
    conta["usuário"]["extrato"].append(f"Conta: {conta["número"]} \t Depósito: \t\t{valor}")
    return


def extrato(saldo, /, *, extrato):
    for movimento in extrato:
        print(movimento)
        
    print(f"Saldo: R${saldo}")
    print("Aperte uma tecla para retornar.")
    msvcrt.getch()
    return


def list_all(usuários) -> None:
    for user in usuários:
        for key in list(user):
            print(f"{key} ")
    print("Aperte uma tecla para retornar.")
    msvcrt.getch()
    return

def menu():
    os.system("cls")
    print("""
  
    [U] Novo usuário
    [C] Nova conta
    [L] Fazer Login
    [S] Saque
    [D] Depósito
    [E] Extrato
    [T] Lista usuários
          
    Aperte a tecla da opção desejada ou 'Esc' para sair.
          """)
    char = msvcrt.getch()
    if char == b'\x1b':
        print("Saindo...")
        sys.exit()
    
    char = bytes.decode(char, encoding, errors="ignore")
    return char


def main() -> None:
    usuários = []
    usuárioLogado = {}
    contas = []
    logged = {}
    while True:
        match menu():
            case 'u':
                usuárioLogado = criarUsuário()
                if any(u["cpf"] == usuárioLogado["cpf"] for u in usuários):
                    print("Usuário já existe. Falha na criação\n")
                    time.sleep(2)
                    continue
                usuários.append(usuárioLogado)
                continue
            
            case 'c':
                contas.append(criarConta(len(contas), usuárioLogado))
                continue    
            
            case 'l':
                print("Aperte 1 para login de usuário e 2 para login de conta.")
                opt = msvcrt.getch()
                opt = bytes.decode(opt, encoding, errors="ignore")
                while (opt != '1') and (opt != '2'):
                    print("Aperte 1 para login de usuário ou 2 para login de conta.")
                    opt = msvcrt.getch()
                    opt = bytes.decode(opt, errors="ignore")
                    print(opt)
                    
                if opt == '2':
                    cpf = input("Digite seu CPF: ")
                    senha = input("Digite sua senha: ")
                    if usuário := next((u for u in usuários if u["cpf"] == cpf), None):
                        if senha == usuário["senha"]:
                            logged = login(usuário, contas, "conta")
                            continue
                        print("Senha incorreta.")
                        print("Aperte uma tecla para continuar.")
                        continue
                    
                    else:
                        print("Usuário não encontrado.")
                        print("Aperte uma tecla para continuar.")
                        msvcrt.getch()
                        continue
                    
                if opt == '1':
                    cpf = input("Digite seu CPF: ")
                    senha = input("Digite sua senha: ")
                    if usuário := next((u for u in usuários if u["cpf"] == cpf), None):
                        if senha == usuário["senha"]:                        
                            usuárioLogado = usuário
                            print("Usuário logado com sucesso.")
                            print("Pressione uma tecla para retornar.")
                            msvcrt.getch()
                        else:
                            print("Senha incorreta.")
                            print("Aperte uma tecla para continuar.")
                            msvcrt.getch()
                    else:
                        print("Usuário não encontrado.")
                        print("Aperte uma tecla para continuar.")
                        msvcrt.getch()
                    continue
                
            case 's':
                if not logged:
                    print("Você ainda não fez login com a conta.")
                    time.sleep(2)
                    continue
                
                valor = input("Digite o valor desejado: ")
                while not valor.isdecimal():
                    valor = input("Digite o valor desejado: ")                  
                valor = float(valor)
                saque(valor=valor, conta=logged)
                continue
            
            case 'd':
                if not logged:
                    print("Você ainda não fez login com a conta.")
                    time.sleep(2)
                    continue
                
                valor = input("Digite o valor desejado: ")
                while not valor.isdigit():
                    valor = input("Digite o valor desejado: ")                  

                valor = float(valor)
                depósito(valor, logged)
                continue
        
            case 'e':
                if not logged:
                    print("Você ainda não fez login com a conta.")
                    time.sleep(2)
                    continue
                
                extrato(logged["saldo"], extrato=usuárioLogado["extrato"])
                continue
        
            case 't':
                list_all(usuários)
                continue
        
    return 0


if __name__ == "__main__":
    main()