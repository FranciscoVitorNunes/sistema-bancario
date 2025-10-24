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

def sacar(*,valor, saldo, limite, numero_saques, limite_saques, extrato):
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    elif valor > limite:
        print("Valor acima do limite permitido.")
    elif numero_saques >= limite_saques:
        print("Voce atingiu o limite diário de saques.")
    elif valor > saldo:
        print("Saldo insuficiente.")
    else:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    return saldo, extrato, numero_saques

def depositar(saldo, valor, extrato, /):
    saldo += valor
    extrato += f"Deposito:\t\tR$ {valor:.2f}\n"
    print("Deposito realizado com sucesso.")
    return saldo, extrato

def exibir_extrato(saldo,/,*, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf_raw = input("Escreva seu cpf(somente números): ")
    # Normalizar: remover espaços e garantir apenas dígitos
    cpf = "".join(ch for ch in cpf_raw if ch.isdigit())

    if not cpf:
        print("CPF inválido.")
        return

    if filtrar_usuario(usuarios, cpf):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Escreva seu nome: ")
    data_nacimento = input("Escreva sua data de nascimento: ")
    endereco = input("Escreva seu endereço: ")

    usuarios.append({"nome": nome, "data_nacimento": data_nacimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")
    return usuarios
    
def filtrar_usuario(usuarios, cpf):
    """Retorna o usuário cujo campo 'cpf' é igual a cpf, ou None se não existir."""
    for usuario in usuarios:
        if usuario.get("cpf") == cpf:
            return usuario
    return None

def criar_conta(agencia, usuarios: list,contas: list):

    cpf = input("Escreva seu cpf(somente números): ")
    usuario_existente = filtrar_usuario(usuarios, cpf)

    if usuario_existente:
        numero_da_conta = len(contas)+1
        contas.append({"agencia":agencia, "numero_conta":numero_da_conta, "usuario": usuario_existente})
        print("Conta criada com sucesso.")
    else:
        print("Usuario não encontrado.")

    return contas

def listar_contas(contas):
    if contas == None:
        print("Nenhuma conta registrada.")
        return
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()
        if opcao == "d":
            valor_do_deposito = float(input("Insira o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor_do_deposito, extrato)
        if opcao == "s":
            valor_do_saque = float(input("Insira o valor do saque: "))
            saldo, extrato, numero_saques = sacar(valor= valor_do_saque, saldo= saldo, limite= limite, numero_saques= numero_saques, limite_saques=LIMITE_SAQUES, extrato= extrato)
        
        if opcao == "e":
            exibir_extrato(saldo, extrato= extrato)

        if opcao == "nu":
            usuarios = criar_usuario(usuarios)

        if opcao == "nc":
            contas = criar_conta(AGENCIA, usuarios, contas)

        if opcao == "lc":
            listar_contas(contas)

        if opcao == "q":
            break

main()