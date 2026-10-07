from util import ler_string
import csv

nome_arquivo = 'usuarios.csv'
cabecalho = ['Nome', 'Senha']

class Usuario:
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

    def cadastrar_usuario(nome, senha):

        usuarios = carregar_usuarios(nome_arquivo)

        for usuario in usuarios:
            if verificar(nome, usuario.nome):
                return False

        novo_usuario = Usuario(nome, senha)
        usuarios.append(novo_usuario)

        salvar_usuarios(usuarios, nome_arquivo)

        return True

    def validar_login(nome, senha):

        usuarios = carregar_usuarios(nome_arquivo)

        for usuario in usuarios:
            if verificar(nome, usuario.nome):

                if senha == usuario.senha:
                    return True

                return False

        return False
        
        

def carregar_usuarios(nome_arquivo):
    """Carrega os usuários de um arquivo CSV."""

    usuarios = []
    try:
        with open(nome_arquivo, mode='r', newline='', encoding='utf-8') as arquivo:
            leitor_csv = csv.DictReader(arquivo)
            for linha in leitor_csv:
                usuario = Usuario(
                    nome=linha['Nome'],
                    senha=linha['Senha']
                )
                usuarios.append(usuario)
    except FileNotFoundError:
        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(cabecalho)
        return usuarios
    return usuarios

def salvar_usuarios(usuarios, nome_arquivo):
    """Salva os usuarios em um arquivo CSV."""
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
        escritor_csv = csv.writer(arquivo)
        escritor_csv.writerow(['Nome', 'Senha'])
        for usuario in usuarios:
            escritor_csv.writerow([
                usuario.nome,
                usuario.senha
            ])
            
def verificar(nome, validacao):
        return nome.lower() == validacao.lower()