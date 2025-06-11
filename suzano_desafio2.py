import textwrap
from datetime import datetime

# Variáveis globais
usuarios = []
contas = []
AGENCIA = "0001"

def menu():
    menu_texto = """
    ================ MENU ================

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo Usuário
    [nc] Nova Conta
    [lc] Listar Contas
    [q] Sair

    => """
    return input(textwrap.dedent(menu_texto))


def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f} em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        print("✅ Depósito realizado com sucesso.")
    else:
        print("⚠️ Valor inválido. O valor deve ser positivo.")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor <= 0:
        print("⚠️ Valor inválido. Deve ser positivo.")
    elif valor > saldo:
        print("❌ Saldo insuficiente.")
    elif valor > limite:
        print(f"❌ Valor acima do limite de R$ {limite:.2f}.")
    elif numero_saques >= limite_saques:
        print("🚫 Limite de saques diários atingido.")
    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f} em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        numero_saques += 1
        print("✅ Saque realizado com sucesso.")
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, extrato):
    print("\n========== EXTRATO ==========")
    print("Nenhuma movimentação." if not extrato else extrato)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("=============================")


def criar_usuario():
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf)

    if usuario:
        print("⚠️ CPF já cadastrado!")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nº - bairro - cidade/sigla estado): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("✅ Usuário criado com sucesso.")


def filtrar_usuario(cpf):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta():
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf)

    if not usuario:
        print("⚠️ Usuário não encontrado. Cadastre-o primeiro.")
        return

    numero_conta = len(contas) + 1
    conta = {
        "agencia": AGENCIA,
        "numero_conta": numero_conta,
        "usuario": usuario
    }
    contas.append(conta)
    print(f"✅ Conta criada com sucesso! Agência: {AGENCIA}, Número da Conta: {numero_conta}")


def listar_contas():
    if not contas:
        print("⚠️ Nenhuma conta cadastrada.")
        return

    for conta in contas:
        linha = f"""\
            Agência: {conta['agencia']}
            C/C: {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
        """
        print("=" * 30)
        print(textwrap.dedent(linha))


def main():
    saldo = 0
    limite = 1000
    extrato = ""
    numero_saques = 0
    limite_saques = 4

    while True:
        opcao = menu()

        if opcao == "d":
            try:
                valor = float(input("Informe o valor do depósito: R$ "))
                saldo, extrato = depositar(saldo, valor, extrato)
            except ValueError:
                print("⚠️ Entrada inválida. Digite um número.")

        elif opcao == "s":
            try:
                valor = float(input("Informe o valor do saque: R$ "))
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=limite_saques
                )
            except ValueError:
                print("⚠️ Entrada inválida. Digite um número.")

        elif opcao == "e":
            exibir_extrato(saldo, extrato)

        elif opcao == "nu":
            criar_usuario()

        elif opcao == "nc":
            criar_conta()

        elif opcao == "lc":
            listar_contas()

        elif opcao == "q":
            print("🛑 Sistema encerrado. Obrigado por utilizar!")
            break

        else:
            print("❓ Operação inválida. Escolha uma das opções do menu.")

# Executa o programa
if __name__ == "__main__":
    main()
