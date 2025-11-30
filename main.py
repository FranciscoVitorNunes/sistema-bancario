
from datetime import datetime
from abc import ABC, abstractmethod


class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Historico:
    def __init__(self):
        self.transacoes = []
    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%y %H:%M:%S"),
            }
        )

class Conta:
    def __init__(self, saldo: float, numero: int, agencia: str, cliente):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int, agencia: str = "0001"):
        return cls(0.0, numero, agencia, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @saldo.setter
    def saldo(self, valor):
        self._saldo = valor
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico
    

    def sacar(self, valor: float) -> bool:
        saldo = self._saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operração falhou voce não possui saldo suficiente. @@@")
        
        elif  valor >0:
            self._saldo -= valor
            print("\n ==== Saque realizado com sucesso ====")
            return True

        else:
            print("\n@@@ Operação falhou. O valor informado é inválido")
        
        return False


    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            print("\n ==== Depósito realizado com sucesso ====")
        else:
            print("\n@@@ Operação falhou, valor informado é inválido. @@@")
        
        return False

class ContaCorrente(Conta):
    def __init__(self, saldo, numero, agencia, cliente, limite=500, limite_saques=3):
        super().__init__(saldo, numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    def sacar(self,valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo" == Saque.__name__]]
        )

        exedeu_limite = valor > self.limite
        exedeu_saques = numero_saques >= self.limite_saques

        if exedeu_limite:
            print(f"\n@@@ Operação falhou. O valor do saque excede o limite. @@@")
        
        elif exedeu_saques:
            print(f"\n@@@ Operação falhou. Número máximo de saques excedidos. @@@")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return  f"""
            Agencia:\t{self.agencia}
            C\C:\t{self.numero}
            Titular:\{self.cliente.nome}
        """


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)



import textwrap

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def sacar(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(clientes,cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado. @@@")
        return
    
    valor = float(input("Informe o valor que deseja sacar: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta,transacao)       

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui contas. @@@")
        return
    
    # FIXME: não permite ciente escolher a conta
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(clientes,cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado. @@@")
        return
    
    valor = float(input("Informe o valor que deseja depositar: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta,transacao)        

def exibir_extrato(clientes):

    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(clientes,cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado. @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes =conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram registradas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n {transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes):
    cpf_raw = input("Escreva seu cpf(somente números): ")
    # Normalizar: remover espaços e garantir apenas dígitos
    cpf = "".join(ch for ch in cpf_raw if ch.isdigit())

    if not cpf:
        print("CPF inválido.")
        return

    if filtrar_cliente(clientes, cpf):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Escreva seu nome: ")
    data_nacimento = input("Escreva sua data de nascimento: ")
    endereco = input("Escreva seu endereço: ")
    
    cliente = PessoaFisica(cpf, nome, data_nacimento, endereco)
    
    clientes.append(cliente)
    print("=== Usuário criado com sucesso! ===")
    return clientes
    
def filtrar_cliente(clientes, cpf):
    clientes_filtrados=[cliente for  cliente in clientes if cliente.cpf==cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def criar_conta(numero_conta, clientes: list,contas: list):

    cpf = input("Escreva seu cpf(somente números): ")
    cliente = filtrar_cliente(clientes, cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado. @@@")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n === Conta criada com sucesso! ===")
    return contas

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        if opcao == "d":
            depositar(clientes)

        if opcao == "s":
            sacar(clientes)
        
        if opcao == "e":
            exibir_extrato(clientes)

        if opcao == "nu":
            criar_cliente(clientes)

        if opcao == "nc":
            numero_conta= len(contas) + 1
            contas = criar_conta(numero_conta, clientes, contas)

        if opcao == "lc":
            listar_contas(contas)

        if opcao == "q":
            break

main()