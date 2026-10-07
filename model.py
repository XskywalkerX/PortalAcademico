from calculos import calcular_media, verificar_situacao
from persistencia import carregar_disciplinas, salvar_disciplinas
from pathlib import Path
import hashlib

class HistoricoAcademico:

    def __init__(self, usuario):
        self.usuario = usuario

        pasta = Path("historicos")
        pasta.mkdir(exist_ok=True)

        identificador = hashlib.sha256(
            usuario.casefold().strip().encode("utf-8")
        ).hexdigest()[:16]

        self.arquivo_csv = str(
            pasta / f"disciplinas_{identificador}.csv"
        )

        self.disciplinas = carregar_disciplinas(
            self.arquivo_csv
        )

    def _salvar_disciplinas(self):
        salvar_disciplinas(
            self.disciplinas,
            self.arquivo_csv
        )

    # --------------------------------------------------
    # ADICIONAR DISCIPLINA
    # --------------------------------------------------

    def adicionar_disciplina(
        self,
        nome,
        av1,
        av2,
        av3,
        edag
    ):
        """
        Adiciona uma nova disciplina.

        Retorna:
            True  -> disciplina adicionada
            False -> disciplina já existe
        """

        # Verifica se já existe
        if any(
            disciplina.nome.casefold() == nome.casefold()
            for disciplina in self.disciplinas
        ):
            return False

        disciplina = Disciplina(
            nome,
            av1,
            av2,
            av3,
            edag
        )

        self.disciplinas.append(disciplina)

        self._salvar_disciplinas()

        return True

    # --------------------------------------------------
    # BUSCAR DISCIPLINA
    # --------------------------------------------------

    def buscar_disciplina(self, nome):
        """
        Procura uma disciplina pelo nome.

        Retorna:
            Disciplina encontrada
            None se não encontrar
        """

        for disciplina in self.disciplinas:

            if disciplina.nome.casefold() == nome.casefold():
                return disciplina

        return None

    # --------------------------------------------------
    # LISTAR DISCIPLINA
    # --------------------------------------------------

    def listar_disciplina_por_nome(self, nome):
        return self.buscar_disciplina(nome)


    def ranking_disciplinas(self):
        return sorted(
            self.disciplinas,
            key=lambda disciplina: disciplina.media_final,
            reverse=True
        )

    # --------------------------------------------------
    # ALTERAR NOTAS
    # --------------------------------------------------

    def alterar_notas_disciplina(
        self,
        nome,
        av1,
        av2,
        av3,
        edag
    ):
        """
        Altera todas as notas de uma disciplina.

        Retorna:
            True  -> alteração realizada
            False -> disciplina não encontrada
        """

        disciplina = self.buscar_disciplina(nome)

        if disciplina is None:
            return False

        disciplina.av1 = av1
        disciplina.av2 = av2
        disciplina.av3 = av3
        disciplina.edag = edag

        # Ao alterar as notas, a nota final anterior
        # deixa de ser válida.
        disciplina.nota_final = None

        disciplina.media = calcular_media(disciplina)

        disciplina.situacao, disciplina.media_final = (
            verificar_situacao(disciplina)
        )

        self._salvar_disciplinas()

        return True

    # --------------------------------------------------
    # EXCLUIR DISCIPLINA
    # --------------------------------------------------

    def excluir_disciplina(self, nome):
        """
        Exclui uma disciplina.

        Retorna:
            True  -> disciplina excluída
            False -> disciplina não encontrada
        """

        disciplina = self.buscar_disciplina(nome)

        if disciplina is None:
            return False

        self.disciplinas.remove(disciplina)

        self._salvar_disciplinas()

        return True

    # --------------------------------------------------
    # ALTERAR NOTA DA FINAL
    # --------------------------------------------------

    def alterar_nota_final(self, nome, nota_final):
        """
        Altera a nota da final de uma disciplina.

        Retorna:
            True  -> alteração realizada
            False -> disciplina não encontrada
            None  -> disciplina não está em situação de final
        """

        disciplina = self.buscar_disciplina(nome)

        if disciplina is None:
            return False

        situacoes_validas = [
            "Final",
            "Reprovado na Final",
            "Aprovado na Final"
        ]

        if disciplina.situacao not in situacoes_validas:
            return None

        disciplina.nota_final = nota_final

        disciplina.situacao, disciplina.media_final = (
            verificar_situacao(disciplina)
        )

        self._salvar_disciplinas()

        return True

    # --------------------------------------------------
    # RESUMO ACADÊMICO
    # --------------------------------------------------

    def resumo_academico(self):
        """
        Retorna a lista de disciplinas cadastradas.
        """

        return self.disciplinas

    # --------------------------------------------------
    # MÉDIA GERAL
    # --------------------------------------------------

    def media_geral(self):
        """
        Calcula a média geral das disciplinas.
        """

        if not self.disciplinas:
            return 0

        return (
            sum(
                disciplina.media_final
                for disciplina in self.disciplinas
            )
            / len(self.disciplinas)
        )


class Disciplina:

    def __init__(
        self,
        nome,
        av1,
        av2,
        av3,
        edag,
        nota_final=None,
        solicitar_final=True
    ):

        self.nome = nome

        self.av1 = av1
        self.av2 = av2
        self.av3 = av3
        self.edag = edag

        self.nota_final = nota_final

        self.media = calcular_media(self)

        self.situacao, self.media_final = (
            verificar_situacao(
                self,
                solicitar_final
            )
        )
