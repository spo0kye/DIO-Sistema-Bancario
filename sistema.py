import datetime
import msvcrt
import locale
import sys
import os


LIMIT_PER_DAY = 10
OpQuantidade = {}
saques = 3
usuarios = {}


def main() -> None:
    if len(sys.argv) != 2:
        print("Modo de uso: python {app} {saldo}")
        return
    
    global saldo
    saldo = float(sys.argv[1])
    if saldo <= 0:
        print("Erro, saldo inválido")
        return
    
    while True:
        os.system("cls") if os.name == "nt" else os.system("clear")
        menu = f"""
    
        R${saldo:.2f}

        [U]: Criar usuário
        [C]: Criar Conta
        [L]: Fazer Login
        [S]: Saque ({saques} saques restantes)
        [D]: Depósito
        [E]: Extrato
        [T]: Teste

        [esc]: Sair
        """
        print(menu)
        
        # Pega a letra digitada pelo usuário sem a necessidade de apertar ENTER e decodifica-a
        char = msvcrt.getch()
        if char == b'\x1b':
            print("saindo...")
            return
        
        encoding = locale.getpreferredencoding()
        char = bytes.decode(char, encoding, errors="ignore")

        match char:
            case 'u':
                cpf = input("Digite seu CPF")
                nome = input("Seu nome")
                senha = input("Sua senha")
                criarUsuario(cpf, nome, senha)
                continue
            
            case 'c':
                cpf = input("Digite seu CPF")
                senha = input("Digite sua senha")
                criarConta(cpf, senha)
                continue
            
            case 'l':
                cpf = input("Digite o CPF de login: ")
                senha = input("Digite a senha de login: ")
                
                # Walrus operator, atribui e retorna o valor ao mesmo tempo
                if (logado := login(cpf, senha)):
                    if len(logado["contas"]) > 0:
                        print("Você tem as contas: ")
                        for conta in logado["contas"]:
                            print(f"{conta["id"] | conta["saldo"]}")
                continue
            
            case 's':
                if not saques > 0:
                    print("Limite de saques atingido.\nPressione uma tecla para voltar ao menu")
                    msvcrt.getch()
                    continue
                
                
                OpQuantidade.setdefault(str(datetime.datetime.now().date()), 0)
                if OpQuantidade[str(datetime.datetime.now().date())] > LIMIT_PER_DAY:
                    print("Limite de operações diárias atingido.")
                    continue
                saque()
                continue
            
            case 'd':
                OpQuantidade.setdefault(str(datetime.datetime.now().date()), 0)
                if OpQuantidade[str(datetime.datetime.now().date())] > LIMIT_PER_DAY:
                    print("Limite de operações diárias atingido.\nPressione uma tecla para voltar ao menu")
                    msvcrt.getch()
                    continue
                deposito()    
                
            case 't':
                print(usuarios)
                msvcrt.getch()
                continue
                
            
        
            case 'e':
                extratoFun()
                continue


def criarUsuario(cpf: str, nome: str, senha: str) -> None:
    if usuarios.get(cpf):
        print("Usuário já cadastrado. Pessione uma tecla para retornar")
        msvcrt.getch()
        return
    
    usuarios[cpf]= {"nome": nome, "senha": senha, "contas": []}
    print("Usuário cadastrado com sucesso! Pessione uma tecla para retornar")
    msvcrt.getch()
    return


def criarConta(cpf, senha) -> None:
    if not usuarios.get(cpf):
        print("Usuário não encontrado. Pessione uma tecla para retornar")
        msvcrt.getch()
        return

    if senha != usuarios[senha]:
        print("Senha incorreta. Pessione uma tecla para retornar")
        msvcrt.getch()
        return
    
    usuarios[cpf]["contas"].append({"id": len(usuarios[cpf]["contas"]), "saldo": saldo})
    print("Conta criada com sucesso!")
    msvcrt.getch()
    return
    

def login():
    msvcrt.getch()
    return

def saque() -> None:
    valor = 0
    print('Digite "sair" para cancelar a operação e voltar ao menu')
    while valor <= 0:
        global saldo
        global saques
        enter = input("Digite o valor desejado para saque: ")
        if enter == "sair":
            return

        try:
            valor = float(enter.format(".2f"))
        except:
            continue
        
        if valor <= saldo:
                saldo -= valor
                saques -= 1
                extrato.append({"operacao": "saque", "valor":f"{valor}", "data": f"{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}"})
                OpQuantidade[str(datetime.datetime.now().date())] += 1
                return
        
        elif valor >= saldo:
            print("Saldo indisponível. Pressione uma tecla para retornar")
            valor = 0
            msvcrt.getch()
    

def deposito() -> None:
    global saldo
    global extrato
    valor = 0    
    while valor == 0:
        enter = input("Digite o valor a ser depositado: ")
        
        try:
            valor = float(enter.format(".2f"))
        except:
            continue
        
        if valor <= 0:
            print("Valor inválido")
            continue
        
        OpQuantidade[str(datetime.datetime.now().date())] += 1
        saldo += valor
        extrato.append({"operacao": "deposito", "valor":f"{valor}", "data": f"{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}"})
    return


def extratoFun() -> None:
    global extrato
    for op in extrato:
        print(f"{op["operacao"]}: R${op["valor"]}, {op["data"]}") if extrato else print("Nenhum registro encontrado")
    
    print("Pressione uma tecla para sair...")
    msvcrt.getch()
    return
    

if __name__ == "__main__":
    main()