import csv

def carregar_disciplinas(nome_arquivo):
    """Carrega as disciplinas de um arquivo CSV."""
    from model import Disciplina

    disciplinas = []
    try:
        with open(nome_arquivo, mode='r', newline='', encoding='utf-8') as arquivo:
            leitor_csv = csv.DictReader(arquivo)
            for linha in leitor_csv:
                nota_final = linha.get('Final')
                disciplina = Disciplina(
                    nome=linha['Nome'],
                    av1=float(linha['AV1']),
                    av2=float(linha['AV2']),
                    av3=float(linha['AV3']),
                    edag=float(linha['EDAG']),
                    nota_final=float(nota_final) if nota_final else None,
                    solicitar_final=False
                )
                disciplinas.append(disciplina)
    except FileNotFoundError:
        pass
    return disciplinas

def salvar_disciplinas(disciplinas, nome_arquivo):
    """Salva as disciplinas em um arquivo CSV."""
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
        escritor_csv = csv.writer(arquivo)
        escritor_csv.writerow(['Nome', 'AV1', 'AV2', 'AV3', 'EDAG', 'Final'])
        for disciplina in disciplinas:
            escritor_csv.writerow([
                disciplina.nome,
                disciplina.av1,
                disciplina.av2,
                disciplina.av3,
                disciplina.edag,
                disciplina.nota_final if disciplina.nota_final is not None else ''
            ])