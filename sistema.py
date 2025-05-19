import datetime
import msvcrt
import locale
import time
import sys
import os


OP_PER_DAY = 10
SAQUES = 3
usuarios = {}
logado = {}


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
        {f"R${logado.get("saldo")}\n        Operações diárias restantes: {OP_PER_DAY - logado.get(str(datetime.datetime.now().date()))}" if "logado" in locals() else ''}

        [U]: Criar usuário
        [C]: Criar Conta
        [L]: Fazer Login
        [S]: Saque
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
                cpf = input("Digite seu CPF: ")
                nome = input("Seu nome: ")
                senha = input("Sua senha: ")
                criarUsuario(cpf, nome, senha)
                continue
            
            case 'c':
                cpf = input("Digite seu CPF: ")
                senha = input("Digite sua senha: ")
                criarConta(cpf, senha)
                continue
            
            case 'l':
                cpf = input("Digite o CPF de login: ")
                senha = input("Digite a senha de login: ")
                
                logado = login(cpf, senha)
                logado.setdefault(str(datetime.datetime.now().date()), 0)
                continue
            
            case 's':
                if not logado:
                    print("Você não fez login com uma conta.\nPressione uma tecla para voltar ao menu")
                    msvcrt.getch()
                    continue
                
                
                logado.setdefault(str(datetime.datetime.now().date()), 0)
                if logado[str(datetime.datetime.now().date())] > OP_PER_DAY:
                    print("Limite de operações diárias atingido. Retornando")
                    time.sleep(2)
                    continue
                
                elif logado["saques"] == 0:
                    print("Limite de saques atingido. Retornando...")
                    time.sleep(2)
                    continue
                
                saque(logado)
                continue
            
            case 'd':
                if not logado:
                    print("Você não fez login com uma conta.\nPressione uma tecla para voltar ao menu")
                    msvcrt.getch()
                    continue
                
                logado.setdefault(str(datetime.datetime.now().date()), 0)
                if logado[str(datetime.datetime.now().date())] >= OP_PER_DAY:
                    print("Limite de operações diárias atingido.\nPressione uma tecla para voltar ao menu")
                    msvcrt.getch()
                    continue
                deposito(logado)

            case 't':
                print(usuarios)
                msvcrt.getch()
                continue
            
            case 'e':
                if not logado:
                    print("Você não fez o login ainda. Pressione uma tecla para retornar")
                    msvcrt.getch()
                    continue
                
                extratoFun(logado)
                continue


def criarUsuario(cpf: str, nome: str, senha: str) -> None:
    if usuarios.get(cpf):
        print("Usuário já cadastrado \nPessione uma tecla para retornar")
        msvcrt.getch()
        return
    
    usuarios[cpf]= {"nome": nome, "senha": senha, "contas": []}
    print("Usuário cadastrado com sucesso \nPessione uma tecla para retornar")
    msvcrt.getch()
    return


def criarConta(cpf, senha) -> None:
    if not usuarios.get(cpf):
        print("Usuário não encontrado \nPessione uma tecla para retornar")
        msvcrt.getch()
        return

    if senha != usuarios[cpf]["senha"]:
        print("Senha incorreta \nPessione uma tecla para retornar")
        msvcrt.getch()
        return
    
    usuarios[cpf]["contas"].append({"id": len(usuarios[cpf]["contas"]), "saldo": saldo, "saques": SAQUES, "extrato": []})
    print("Conta criada com sucesso! Pressione uma tecla para retornar")
    msvcrt.getch()
    return
    

def login(cpf, senha):
    if not usuarios.get(cpf):
        print("Erro, Usuário não cadastrado \nPressione uma tecla para retornar")
        msvcrt.getch()
        return

    if senha != usuarios[cpf]["senha"]:
        print("Erro, Senha incorreta \nPressione uma tecla para retornar")
        msvcrt.getch()
        return


    if len(usuarios[cpf]["contas"]) > 0:
        print("Você tem as contas: ")
        for conta in usuarios[cpf]["contas"]:
            print(f"{conta["id"]} | {conta["saldo"]}")
            
        while not (logado := next((u for u in usuarios[cpf]["contas"] if u["id"] == conta), None)):
            conta = int(input("Selecione o número da conta desejada: "))
            
        return logado
    else:
        print("Você não tem nenhuma conta para utilização \nPressione uma tecla para retornar")
        msvcrt.getch()
        return
    

def saque(logado) -> None:
    valor = 0
    print(f'Saques restantes: {logado.get("saques")} \nSaldo restante: {logado.get("saldo")}\
        \nDigite "sair" para cancelar a operação e voltar ao menu')
    while valor <= 0:
        enter = input("Digite o valor desejado para saque: ")
        if enter == "sair":
            return

        try:
            valor = float(enter.format(".2f"))
        except:
            continue
        
        if valor <= logado.get("saldo"):
                logado["saldo"] -= valor
                logado["saques"] -= 1
                logado["extrato"].append({"operacao": "saque", "valor":f"{valor}", "data": f"{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}"})
                logado[str(datetime.datetime.now().date())] += 1
                return
        
        elif valor >= saldo:
            print("Saldo indisponível. Pressione uma tecla para retornar")
            valor = 0
            msvcrt.getch()
    

def deposito(logado) -> None:
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
        
        logado[str(datetime.datetime.now().date())] += 1
        logado["saldo"] += valor
        logado["extrato"].append({"operacao": "deposito", "valor":f"{valor}", "data": f"{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}"})
    return


def extratoFun(logado) -> None:
    for op in logado["extrato"]:
        print(f"{op["operacao"]}: R${op["valor"]}, {op["data"]}") if logado["extrato"] else print("Nenhum registro encontrado")
    
    print("Pressione uma tecla para sair...")
    msvcrt.getch()
    return
    

if __name__ == "__main__":
    main()