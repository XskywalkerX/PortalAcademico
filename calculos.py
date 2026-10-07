def calcular_media(disciplina):
    """
    Calcula a média ponderada da disciplina.

    Pesos:
        AV1  -> 25%
        AV2  -> 25%
        AV3  -> 30%
        EDAG -> 20%

    Retorna:
        Média ponderada da disciplina.
    """

    media = (
        0.25 * disciplina.av1
        + 0.25 * disciplina.av2
        + 0.30 * disciplina.av3
        + 0.20 * disciplina.edag
    )

    return media


def soma_medias(historico):
    """
    Soma as médias das disciplinas do histórico.

    Retorna:
        Soma das médias.
    """

    if not historico.disciplinas:
        return 0

    return sum(
        disciplina.media
        for disciplina in historico.disciplinas
    )


def media_geral(historico):
    """
    Calcula a média geral das disciplinas.

    Retorna:
        Média geral.
    """

    if not historico.disciplinas:
        return 0

    return (
        soma_medias(historico)
        / len(historico.disciplinas)
    )


def verificar_situacao(disciplina, solicitar_final=True):
    """
    Determina a situação acadêmica da disciplina.

    Regras:

        Média >= 7:
            Aprovado

        Média >= 4 e < 7:
            Final

        Média < 4:
            Reprovado

    Caso exista uma nota da Final, ela será utilizada
    para calcular a média final.

    A nota da Final NÃO é solicitada aqui.
    A interface é responsável por solicitar essa nota.

    Retorna:
        Uma tupla:

        (situação, média_final)
    """

    media = calcular_media(disciplina)

    # ----------------------------------------------
    # APROVADO DIRETO
    # ----------------------------------------------

    if media >= 7:
        return "Aprovado", media

    # ----------------------------------------------
    # REPROVADO DIRETO
    # ----------------------------------------------

    if media < 4:
        return "Reprovado", media

    # ----------------------------------------------
    # FINAL
    # ----------------------------------------------

    # Se não existe nota da final,
    # o aluno está aguardando a Final.

    if disciplina.nota_final is None:
        return "Final", media

    # ----------------------------------------------
    # CÁLCULO DA MÉDIA COM A FINAL
    # ----------------------------------------------

    media_final = (
        media * 0.60
        + disciplina.nota_final * 0.40
    )

    # ----------------------------------------------
    # RESULTADO DA FINAL
    # ----------------------------------------------

    if media_final >= 5:
        situacao = "Aprovado na Final"
    else:
        situacao = "Reprovado na Final"

    return situacao, media_final