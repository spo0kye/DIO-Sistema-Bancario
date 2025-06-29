import datetime
from abc import ABC, abstractmethod


class Cliente():
    def __init__(self, endereço, senha):
        self._endereço = endereço
        self._contas = []
        self._senha = senha


    @property
    def endereço(self):
        return self._endereço
    
    
    @property
    def contas(self):
        return self._contas


    @property
    def senha(self):
        return self._senha
    

    def realizar_transação(self, conta, transação):
        transação.registrar(conta)


    def adicionar_conta(self, conta):
        self.contas.append(conta)


    def deletar_conta(self, nro_conta):
        conta = [conta for conta in self.contas if conta.número == nro_conta]
        self.contas.remove(conta) if conta else print("Conta não encontrada")
       
        
    def __str__(self):
        all = []
        for key, value in self.__dict__.items():
            all.append(f"{key}: {value}".replace("_", ""))
        return ', '.join(all)


class Transação(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass
    

class Depósito(Transação):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
            return self._valor
        

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta._histórico.adicionar_transação(self)
    

class Saque(Transação):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor


    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta._histórico.adicionar_transação(self)


class Histórico():
    def __init__(self):
        self._transações = []
    
    
    @property
    def transações(self):
        return self._transações
    
    
    def adicionar_transação(self, transação) -> None:
        self._transações.append({
            "tipo": transação.__class__.__name__,
            "valor": transação.valor,
            "data": datetime.datetime.now().date()
        })
        
    
    def __str__(self):
        lista = []
        for transação in self.transações:
            lista.append(', '.join(f"{k}: {v}" for k, v in transação.items()))
            lista.append('\n')
            
        if lista:
            return ''.join(lista)
        
        else:
            return "\nNenhuma transação encontrada."
        

class Conta():
    n_contas = 0
    def __init__(self, cliente: Cliente):
        self._saldo = 0
        self._número = Conta.n_contas + 1
        self._agência = "001"
        self._cliente = cliente
        self._histórico = Histórico()
        Conta.n_contas += 1

    
    @property
    def saldo(self) -> float:
        return self._saldo
    
    
    @property
    def número(self):
        return self._número
    
    
    @property
    def agência(self):
        return self._agência
    
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def histórico(self):
        return self._histórico


    def nova_conta(cls, cliente: Cliente, número: int): 
        return cls(cliente, número)
    
    
    def sacar(self, valor: float) -> bool:
        if valor > self.saldo:
            print("\nErro! Saldo insuficiente.")
    
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque efetuado com sucesso.")
            return True
    
        else:
            print("\nErro! Valor inválido.")
                
        return False
    
    
    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            print("\nDepósito efetuado com sucesso.")
            return True
        
        else:
            print("\nValor inválido")


class pessoaFísica(Cliente):
    def __init__(self, cpf: str, nome: str, endereço: str, nascimento: datetime.date, senha):
        super().__init__(endereço, senha)
        self._cpf = cpf
        self._nome = nome
        self._nascimento = nascimento

        
    @property
    def cpf(self):
        return self._cpf
    
    
    @property
    def nome(self):
        return self._nome
    
    
    @property
    def nascimento(self):
        return self._nascimento


class ContaCorrente(Conta):
    def __init__(self, cliente, limite=500, limite_saques=3):
        super().__init__(cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        
    
    @property
    def limite(self):
        return self._limite
    
    
    @property
    def limite_saques(self):
        return self._limite_saques
    
    
    def sacar(self, valor):
        if valor > self.limite:
            print("\nErro! Valor maior do que o limite.")
            return False
        
        elif len(
            [transação for transação in self.histórico.transações if transação.get("data").day == datetime.datetime.now().day]
        ) > self.limite_saques:
            print("\nErro! Limite de saques diários atingidos.")
            return False
        
        else:
            return super().sacar(valor)