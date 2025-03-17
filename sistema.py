import msvcrt
import locale
import math
import sys


extrato = []
saques = 3


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
        menu = f"""
    
        R${saldo:.2f}

        [S]: Saque ({saques} saques restantes)
        [D]: Depósito
        [E]: Extrato

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
            case 's':
                if not saques > 0:
                    print("Limite de saques atingido.\nPressione uma tecla para voltar ao menu")
                    msvcrt.getch()
                    continue
                saque()
            
            case 'd':
                deposito()
                
            case 'e':
                extratoFun()

   
def saque() -> None:
    valor = 0
    print("Digite sair para cancelar a operação e voltar ao menu")
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
            extrato.append({"operacao": "saque", "valor":f"{valor}"})
            return
        
        elif valor >= saldo:
            print("Saldo indisponível")
            valor = 0
    

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
            
        saldo += valor
        extrato.append({"operacao": "deposito", "valor":f"{valor}"})
    return


def extratoFun() -> None:
    global extrato
    for op in extrato:
        print(f"{op["operacao"]}: R${op["valor"]}")
    
    print("Pressione uma tecla para sair...")
    msvcrt.getch()
    return
    

if __name__ == "__main__":
    main()