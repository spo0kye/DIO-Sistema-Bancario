from Classes import *
import datetime
import msvcrt
import locale
import time
import sys
import os

encoding = locale.getpreferredencoding()
usuários = []


class ContasIterador():
    def __init__(self):
        self.atual = 0
    
    
    def __iter__(self):
        return self


    def __next__(self):
        if self.atual < len(usuários):
            retorno = []
            self.atual += 1
            contas = [conta for usuário in usuários for conta in usuário.contas]
            for conta in contas:
                retorno.append({"nome": conta.cliente.nome, "número": conta.número, "saldo": conta.saldo})
            return retorno
        else:
            self.atual = 0
            raise StopIteration
        

def log(f):
    def wrapper(*args, **kwargs):
        print(f"Data: {datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}\nTipo: {f.__name__}")
        f(*args, **kwargs)
    return wrapper


def filtro(conta:Conta, filtro:str = None):
    if filtro:
        transações = [transação for transação in conta.histórico.transações if transação["tipo"] == filtro]
    else:
        transações = conta.histórico.transações
    
    if not transações:
        print("Nenhuma transação encontrada.")
        return
    
    for transação in transações:
        yield transação


def criarUsuário():
    global usuários
    nome = input("Digite seu nome: ")
    nascimento = datetime.datetime.strptime(input("Digite sua data de nascimento(dd/mm/AAAA)\n"), "%d/%m/%Y")
    cpf = input("Digite seu CPF\n")
    if any(u.cpf == cpf for u in usuários):
        print("Já existe um usuário cadastrado com esse CPF.\nAperte um botão para continuar")
        msvcrt.getch()
        return
    
    endereço = input("Digite seu endereço da seguinte forma: logradouro, n° - bairro - cidade/sigla estado\n")
    senha = input("Digite sua senha\n")
    return usuários.append(pessoaFísica(cpf, nome, endereço, nascimento, senha))


def criarConta(usuário):
    if not usuário:
        print("Faça login ou crie um novo usuário para criar uma conta.\n")
        time.sleep(2)
        return
    
    print(f"Criando conta, Agência n° 0001, número {Conta.n_contas + 1}, usuário: {usuário.nome}")
    print("Conta criada com sucesso, faça login para usar. \nSaindo...")
    time.sleep(2)
    nova_conta = ContaCorrente(usuário)
    usuário.adicionar_conta(nova_conta)


def login(usuário):
    print("O(a) Senhor(a) possui as seguintes contas disponíveis:")
    contasUsuário = usuário.contas
    if not contasUsuário:
        print("Você não tem contas disponíveis. Crie uma primeiro.")
        print("Aperte uma tecla para retornar.")
        msvcrt.getch()
        return
    
    for conta in contasUsuário:
        print(f"agência: nº 0001 | número {conta.número}")
        
    select = int(input("\nDigite o número da conta desejada: "))
    while not (conta := next((acc for acc in usuário.contas if select == acc.número), None)):
        select = input("Digite o número da conta desejada: ")
        if select.isdigit():
            select = int(select)
     
    return conta


@log
def saque(*, valor, conta):
    if conta.saldo < valor:
        print("Saldo indisponível...")
        print("Pressione uma tecla para retornar")
        msvcrt.getch()
        return
    
    if conta.limite <= 0:
        print("Limite de operações diárias dessa conta atingido.")
        print("Pressione uma tecla para retornar")
        msvcrt.getch()
        return
    
    Saque(valor).registrar(conta)
    print("Pressione uma tecla para retornar")
    msvcrt.getch()
    return


@log
def depósito(valor, conta, /):
    Depósito(valor).registrar(conta)
    print("Pressione uma tecla para retornar")
    msvcrt.getch()
    return


def extrato(conta, opt=None):
    if not opt:
        print(conta.histórico)
        print("Aperte uma tecla para retornar.")
        msvcrt.getch()
        return
    
    if opt == 1:
        entrada = input("Digite o tipo de transação que deseja filtar. Saque | Depósito\n")
        while not entrada in ["Saque", "Depósito"]:
            entrada = input("Digite o tipo de transação que deseja filtar. Saque | Depósito\n")
        os.system("cls")
        for transação in filtro(conta, entrada):
            print(f"tipo: {transação["tipo"]}, valor: {transação["valor"]}, data: {transação["data"]}")
        print("Aperte uma tecla para retornar.")
        msvcrt.getch()


def menu():
    os.system("cls")
    print("""
  
    [U] Novo usuário
    [C] Nova conta
    [L] Fazer Login
    [S] Saque
    [D] Depósito
    [E] Extrato
    [T] Listar todos os usuários
          
    Aperte a tecla da opção desejada ou 'Esc' para sair.
          """)
    char = msvcrt.getch()
    if char == b'\x1b':
        print("Saindo...")
        sys.exit()
    
    char = bytes.decode(char, encoding, errors="ignore")
    return char


def main() -> None:
    global usuários
    Contas = ContasIterador()
    while True:
        match menu():
            case 'u':
                criarUsuário()
                continue
                
            case 'c':
                if "usuárioLogado" in locals():
                    criarConta(usuárioLogado)
                    continue
                else:
                    print("\nFaça login com seu usuário primeiro.")
                    print("Aperte uma tecla para continuar.")
                    msvcrt.getch()
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
                    if usuário := next((u for u in usuários if u.cpf == cpf), None):
                        if senha == usuário.senha:
                            logged = login(usuário)
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
                    if usuário := next((u for u in usuários if u.cpf == cpf), None):
                        if senha == usuário.senha:                        
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
                if not "logged" in locals():
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
                if not "logged" in locals():
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
                if not "logged" in locals():
                    print("Você ainda não fez login com a conta.")
                    time.sleep(2)
                    continue
                
                print("Aperte 1 para filtrar os resultados ou 2 para ver o extrato completo")
                opt = msvcrt.getch()
                opt = bytes.decode(opt, errors="ignore")
                while (opt != '1') and (opt != '2'):
                    print("Aperte 1 para filtrar os resultados ou 2 para ver o extrato completo")
                    opt = msvcrt.getch()
                    opt = bytes.decode(opt, errors="ignore")
                match opt:
                    case '1':
                        extrato(logged, opt=1)
                        continue
                    
                    case '2':
                        extrato(logged)
                        continue
                continue
            
            case 't':
                for conta in Contas:
                    print(conta)
                    print("Aperte uma tecla para retornar.")
                    msvcrt.getch()
                del Contas
                continue
    return 0


if __name__ == "__main__":
    main()