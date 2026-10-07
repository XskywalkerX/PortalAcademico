def ler_float(mensagem):
    """Lê um valor float do usuário, garantindo que seja válido.

    Args:
        mensagem (str): A mensagem a ser exibida para o usuário."""

    while True:
        try:
            valor = float(input(mensagem))
            if(valor >= 0 and valor <= 10):
                return valor
            else:
                print("Valor inválido. Por favor, digite um número entre 0 e 10.")
        except ValueError:
            print("Valor inválido. Por favor, digite um número válido.")

def ler_string(mensagem):
    """Lê uma string do usuário, garantindo que não esteja vazia.

    Args:
        mensagem (str): A mensagem a ser exibida para o usuário."""
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        else:
            print("Valor inválido. Por favor, digite uma string não vazia.")


def saudacao():
    """Exibe a mensagem inicial do sistema de notas."""
    print("Olá! Bem-vindo ao sistema de notas SENAI CIMATEC\n")


def menu():

    opcao = ""

    while opcao != "6":
        print("================ MENU ================\n")
        print("1. Adicionar disciplina")
        print("2. Listar disciplina pelo nome")
        print("3. Alterar notas de uma disciplina")
        print("4. Excluir disciplina")
        print("5. Alterar nota da final")
        print("6. Listar resumo acadêmico")
        print("7. Sair\n")

        opcao = input("Digite a opção desejada: ")

        if opcao not in ["1", "2", "3", "4", "5", "6", "7"]:
            print("Opção inválida. Por favor, digite uma opção válida.\n")

        return opcao

