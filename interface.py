import tkinter as tk
from tkinter import messagebox, ttk

from usuarios import Usuario
from model import HistoricoAcademico


class Interface:
    BG = "#0B1220"
    SIDEBAR = "#0F172A"
    SURFACE = "#111C30"
    CARD = "#16243A"
    CARD_HOVER = "#1D304C"
    INPUT = "#0E192B"
    BORDER = "#263752"
    PRIMARY = "#3B82F6"
    PRIMARY_HOVER = "#60A5FA"
    SUCCESS = "#22C55E"
    DANGER = "#EF4444"
    WARNING = "#F59E0B"
    TEXT = "#F8FAFC"
    MUTED = "#94A3B8"
    WHITE = "#FFFFFF"

    FONT = "Segoe UI"

    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Sistema Acadêmico")
        self.janela.geometry("1100x700")
        self.janela.minsize(980, 620)
        self.janela.configure(bg=self.BG)

        try:
            self.janela.iconname("Sistema Acadêmico")
        except tk.TclError:
            pass

        self._configurar_estilos()

        self.historicos = []
        self.historico = None
        
        self.usuario_logado = None

        self.janela.protocol("WM_DELETE_WINDOW", self.sair)
        self.tela_login()

    def _configurar_estilos(self):
        style = ttk.Style(self.janela)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Modern.TEntry",
            fieldbackground=self.INPUT,
            background=self.INPUT,
            foreground=self.TEXT,
            bordercolor=self.BORDER,
            lightcolor=self.BORDER,
            darkcolor=self.BORDER,
            padding=(12, 10),
            font=(self.FONT, 11),
        )

        style.map(
            "Modern.TEntry",
            bordercolor=[
                ("focus", self.PRIMARY),
                ("active", self.PRIMARY),
            ],
            lightcolor=[
                ("focus", self.PRIMARY),
                ("active", self.PRIMARY),
            ],
        )

        style.configure(
            "Modern.Treeview",
            background=self.CARD,
            fieldbackground=self.CARD,
            foreground=self.TEXT,
            borderwidth=0,
            rowheight=38,
            font=(self.FONT, 10),
        )

        style.configure(
            "Modern.Treeview.Heading",
            background=self.SURFACE,
            foreground=self.MUTED,
            relief="flat",
            borderwidth=0,
            font=(self.FONT, 9, "bold"),
        )

        style.map(
            "Modern.Treeview",
            background=[("selected", "#244D87")],
            foreground=[("selected", self.WHITE)],
        )

    def iniciar(self):
        self.janela.mainloop()

    def limpar_janela(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

    def _centralizar(self, janela, largura, altura):
        janela.update_idletasks()
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        x = max((largura_tela - largura) // 2, 0)
        y = max((altura_tela - altura) // 2, 0)
        janela.geometry(f"{largura}x{altura}+{x}+{y}")

    def _titulo(self, parent, texto, tamanho=24):
        return tk.Label(
            parent,
            text=texto,
            bg=parent.cget("bg"),
            fg=self.TEXT,
            font=(self.FONT, tamanho, "bold"),
        )

    def _subtitulo(self, parent, texto):
        return tk.Label(
            parent,
            text=texto,
            bg=parent.cget("bg"),
            fg=self.MUTED,
            font=(self.FONT, 10),
        )

    def _botao(
        self,
        parent,
        texto,
        comando,
        largura=20,
        primaria=True,
        altura=1,
        fonte=10,
        cor=None,
        cor_hover=None,
    ):
        fundo = cor or (self.PRIMARY if primaria else self.CARD)
        hover = cor_hover or (self.PRIMARY_HOVER if primaria else self.CARD_HOVER)
        cor_borda = fundo if primaria or cor else self.BORDER

        botao = tk.Button(
            parent,
            text=texto,
            command=comando,
            width=largura,
            height=altura,
            bg=fundo,
            fg=self.WHITE,
            activebackground=hover,
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=cor_borda,
            highlightcolor=cor_borda,
            cursor="hand2",
            font=(self.FONT, fonte, "bold"),
        )

        botao.bind("<Enter>", lambda _e: botao.configure(bg=hover))
        botao.bind("<Leave>", lambda _e: botao.configure(bg=fundo))
        return botao

    def _botao_menu(self, parent, texto, comando, ativo=False):
        fundo = "#183155" if ativo else self.SIDEBAR
        hover = "#1D3C69"

        botao = tk.Button(
            parent,
            text=texto,
            command=comando,
            anchor="w",
            bg=fundo,
            fg=self.TEXT if ativo else self.MUTED,
            activebackground=hover,
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            padx=18,
            cursor="hand2",
            font=(self.FONT, 10, "bold"),
        )

        botao.pack(fill="x", pady=4)
        botao.bind("<Enter>", lambda _e: botao.configure(bg=hover, fg=self.WHITE))
        botao.bind(
            "<Leave>",
            lambda _e: botao.configure(
                bg=fundo, fg=self.TEXT if ativo else self.MUTED
            ),
        )
        return botao

    def _criar_cabecalho_janela(self, janela, titulo, subtitulo=""):
        topo = tk.Frame(janela, bg=self.SURFACE)
        topo.pack(fill="x")

        conteudo = tk.Frame(topo, bg=self.SURFACE)
        conteudo.pack(fill="x", padx=28, pady=24)

        tk.Label(
            conteudo,
            text=titulo,
            bg=self.SURFACE,
            fg=self.TEXT,
            font=(self.FONT, 20, "bold"),
        ).pack(anchor="w")

        if subtitulo:
            tk.Label(
                conteudo,
                text=subtitulo,
                bg=self.SURFACE,
                fg=self.MUTED,
                font=(self.FONT, 9),
            ).pack(anchor="w", pady=(5, 0))

        return topo

    def _campo(self, parent, texto, largura=None, senha=False):
        bloco = tk.Frame(parent, bg=parent.cget("bg"))

        tk.Label(
            bloco,
            text=texto,
            bg=parent.cget("bg"),
            fg=self.MUTED,
            font=(self.FONT, 9, "bold"),
        ).pack(anchor="w", pady=(0, 7))

        entrada = ttk.Entry(
            bloco,
            style="Modern.TEntry",
            show="•" if senha else "",
        )

        if largura:
            entrada.configure(width=largura)

        entrada.pack(fill="x")
        bloco.pack(fill="x")
        return bloco, entrada

    def tela_login(self):
        self.limpar_janela()

        self.janela.title("Login | Sistema Acadêmico")
        self._centralizar(self.janela, 950, 600)
        self.janela.resizable(False, False)

        base = tk.Frame(self.janela, bg=self.BG)
        base.pack(fill="both", expand=True)

        esquerda = tk.Frame(base, bg=self.PRIMARY, width=365)
        esquerda.pack(side="left", fill="y")
        esquerda.pack_propagate(False)

        marca = tk.Frame(esquerda, bg=self.PRIMARY)
        marca.place(relx=0.5, rely=0.5, anchor="center")

        logo = tk.Label(
            marca,
            text="SA",
            bg="#2563EB",
            fg=self.WHITE,
            width=4,
            height=2,
            font=(self.FONT, 28, "bold"),
        )
        logo.pack(pady=(0, 22))

        tk.Label(
            marca,
            text="Sistema\nAcadêmico",
            bg=self.PRIMARY,
            fg=self.WHITE,
            justify="center",
            font=(self.FONT, 27, "bold"),
        ).pack()

        tk.Label(
            marca,
            text="Organize suas disciplinas,\nacompanhe suas notas e seu desempenho.",
            bg=self.PRIMARY,
            fg="#DBEAFE",
            justify="center",
            font=(self.FONT, 10),
        ).pack(pady=(18, 0))

        direita = tk.Frame(base, bg=self.SURFACE, width=585)
        direita.pack(side="right", fill="both", expand=True)
        direita.pack_propagate(False)

        formulario = tk.Frame(direita, bg=self.SURFACE)
        formulario.place(relx=0.5, rely=0.5, anchor="center", width=390)

        tk.Label(
            formulario,
            text="Bem-vindo de volta",
            bg=self.SURFACE,
            fg=self.TEXT,
            font=(self.FONT, 24, "bold"),
        ).pack(anchor="w")

        tk.Label(
            formulario,
            text="Entre com sua conta para acessar seu histórico acadêmico.",
            bg=self.SURFACE,
            fg=self.MUTED,
            wraplength=370,
            justify="left",
            font=(self.FONT, 10),
        ).pack(anchor="w", pady=(7, 30))

        _, self.entrada_usuario = self._campo(
            formulario, "USUÁRIO"
        )
        self.entrada_usuario.pack(fill="x", pady=(0, 18))

        _, self.entrada_senha = self._campo(
            formulario, "SENHA", senha=True
        )
        self.entrada_senha.pack(fill="x", pady=(0, 25))

        botao_login = self._botao(
            formulario,
            "ENTRAR",
            self.fazer_login,
            largura=30,
            primaria=True,
            altura=2,
        )
        botao_login.pack(fill="x", pady=(0, 14))

        linha = tk.Frame(formulario, bg=self.SURFACE)
        linha.pack(fill="x")

        tk.Label(
            linha,
            text="Ainda não possui uma conta?",
            bg=self.SURFACE,
            fg=self.MUTED,
            font=(self.FONT, 9),
        ).pack(side="left")

        cadastro = tk.Button(
            linha,
            text="Cadastrar usuário",
            command=self.tela_cadastro,
            bg=self.SURFACE,
            fg=self.PRIMARY_HOVER,
            activebackground=self.SURFACE,
            activeforeground=self.WHITE,
            bd=0,
            relief="flat",
            cursor="hand2",
            font=(self.FONT, 9, "bold", "underline"),
        )
        cadastro.pack(side="left", padx=(7, 0))

        self.entrada_usuario.bind("<Return>", lambda _e: self.fazer_login())
        self.entrada_senha.bind("<Return>", lambda _e: self.fazer_login())
        self.entrada_usuario.focus_set()

    def fazer_login(self):
        nome = self.entrada_usuario.get().strip()
        senha = self.entrada_senha.get()

        if not nome or not senha:
            messagebox.showwarning(
                "Campos obrigatórios",
                "Preencha usuário e senha.",
                parent=self.janela,
            )
            return

        if Usuario.validar_login(nome, senha):

            self.usuario_logado = nome

            self.historico = HistoricoAcademico(
            self.usuario_logado
        )

            self.tela_principal()
        else:
            messagebox.showerror(
                "Acesso negado",
                "Usuário ou senha incorretos.",
                parent=self.janela,
            )

    def tela_cadastro(self):
        janela = tk.Toplevel(self.janela)
        janela.title("Novo usuário")
        janela.configure(bg=self.BG)
        janela.resizable(False, False)
        self._centralizar(janela, 460, 480)
        janela.transient(self.janela)
        janela.grab_set()

        self._criar_cabecalho_janela(
            janela,
            "Criar conta",
            "Cadastre um novo acesso ao sistema acadêmico.",
        )

        corpo = tk.Frame(janela, bg=self.BG)
        corpo.pack(fill="both", expand=True, padx=30, pady=25)

        _, entrada_nome = self._campo(corpo, "USUÁRIO")
        entrada_nome.pack(fill="x", pady=(0, 18))

        _, entrada_senha = self._campo(corpo, "SENHA", senha=True)
        entrada_senha.pack(fill="x", pady=(0, 25))

        def cadastrar():
            nome = entrada_nome.get().strip()
            senha = entrada_senha.get()

            if not nome or not senha:
                messagebox.showwarning(
                    "Campos obrigatórios",
                    "Preencha todos os campos.",
                    parent=janela,
                )
                return

            if Usuario.cadastrar_usuario(nome, senha):
                messagebox.showinfo(
                    "Cadastro concluído",
                    "Usuário cadastrado com sucesso!",
                    parent=janela,
                )
                janela.destroy()
                self.entrada_usuario.focus_set()
            else:
                messagebox.showerror(
                    "Cadastro não realizado",
                    "Esse usuário já existe.",
                    parent=janela,
                )

        self._botao(
            corpo,
            "CRIAR USUÁRIO",
            cadastrar,
            largura=28,
            primaria=True,
            altura=2,
        ).pack(fill="x")

        entrada_nome.focus_set()

    def tela_principal(self):
        self.limpar_janela()

        self.janela.title("Sistema Acadêmico")
        self._centralizar(self.janela, 1100, 700)
        self.janela.resizable(True, True)

        base = tk.Frame(self.janela, bg=self.BG)
        base.pack(fill="both", expand=True)

        sidebar = tk.Frame(base, bg=self.SIDEBAR, width=235)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        marca = tk.Frame(sidebar, bg=self.SIDEBAR)
        marca.pack(fill="x", padx=20, pady=(27, 32))

        tk.Label(
            marca,
            text="SA",
            bg=self.PRIMARY,
            fg=self.WHITE,
            width=3,
            height=1,
            font=(self.FONT, 18, "bold"),
        ).pack(side="left")

        texto_marca = tk.Frame(marca, bg=self.SIDEBAR)
        texto_marca.pack(side="left", padx=(10, 0))

        tk.Label(
            texto_marca,
            text="SISTEMA",
            bg=self.SIDEBAR,
            fg=self.TEXT,
            font=(self.FONT, 10, "bold"),
        ).pack(anchor="w")

        tk.Label(
            texto_marca,
            text="Acadêmico",
            bg=self.SIDEBAR,
            fg=self.MUTED,
            font=(self.FONT, 9),
        ).pack(anchor="w")

        tk.Label(
            sidebar,
            text="MENU",
            bg=self.SIDEBAR,
            fg="#64748B",
            font=(self.FONT, 8, "bold"),
        ).pack(anchor="w", padx=20, pady=(0, 8))

        self._botao_menu(
            sidebar, "＋   Adicionar disciplina",
            self.tela_adicionar_disciplina, ativo=True
        )
        self._botao_menu(
            sidebar, "⌕   Consultar disciplina",
            self.tela_consultar_disciplina
        )
        self._botao_menu(
            sidebar, "✎   Alterar notas",
            self.tela_alterar_notas
        )
        self._botao_menu(
            sidebar, "−   Excluir disciplina",
            self.tela_excluir_disciplina
        )
        self._botao_menu(
            sidebar, "F   Alterar nota da final",
            self.tela_alterar_final
        )
        self._botao_menu(
            sidebar, "▦   Resumo acadêmico",
            self.tela_resumo
        )
        self._botao_menu(
            sidebar, "Ranking",
            self.tela_ranking
        )

        rodape = tk.Frame(sidebar, bg=self.SIDEBAR)
        rodape.pack(side="bottom", fill="x", padx=18, pady=20)

        usuario_card = tk.Frame(
            rodape,
            bg=self.SURFACE,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        usuario_card.pack(fill="x", pady=(0, 12))

        tk.Label(
            usuario_card,
            text=self.usuario_logado[:1].upper(),
            bg=self.PRIMARY,
            fg=self.WHITE,
            width=3,
            height=1,
            font=(self.FONT, 12, "bold"),
        ).pack(side="left", padx=10, pady=10)

        dados = tk.Frame(usuario_card, bg=self.SURFACE)
        dados.pack(side="left", pady=9)

        tk.Label(
            dados,
            text=self.usuario_logado,
            bg=self.SURFACE,
            fg=self.TEXT,
            font=(self.FONT, 9, "bold"),
        ).pack(anchor="w")

        tk.Label(
            dados,
            text="Usuário logado",
            bg=self.SURFACE,
            fg=self.MUTED,
            font=(self.FONT, 8),
        ).pack(anchor="w")

        sair = tk.Button(
            rodape,
            text="Encerrar sessão",
            command=self.sair,
            bg=self.SIDEBAR,
            fg="#FCA5A5",
            activebackground=self.SURFACE,
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=(self.FONT, 9, "bold"),
        )
        sair.pack(anchor="w", padx=8)

        conteudo = tk.Frame(base, bg=self.BG)
        conteudo.pack(side="right", fill="both", expand=True)

        header = tk.Frame(conteudo, bg=self.BG)
        header.pack(fill="x", padx=34, pady=(30, 20))

        esquerda = tk.Frame(header, bg=self.BG)
        esquerda.pack(side="left")

        tk.Label(
            esquerda,
            text=f"Olá, {self.usuario_logado}.",
            bg=self.BG,
            fg=self.TEXT,
            font=(self.FONT, 25, "bold"),
        ).pack(anchor="w")

        tk.Label(
            esquerda,
            text="Gerencie seu histórico acadêmico em um só lugar.",
            bg=self.BG,
            fg=self.MUTED,
            font=(self.FONT, 10),
        ).pack(anchor="w", pady=(5, 0))

        try:
            media = self.historico.media_geral()
            media_texto = f"{media:.2f}"
        except Exception:
            media_texto = "--"

        metricas = tk.Frame(header, bg=self.BG)
        metricas.pack(side="right")

        card_media = tk.Frame(
            metricas,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            padx=18,
            pady=12,
        )
        card_media.pack(side="left")

        tk.Label(
            card_media,
            text="MÉDIA GERAL",
            bg=self.CARD,
            fg=self.MUTED,
            font=(self.FONT, 8, "bold"),
        ).pack(anchor="w")

        tk.Label(
            card_media,
            text=media_texto,
            bg=self.CARD,
            fg=self.SUCCESS,
            font=(self.FONT, 21, "bold"),
        ).pack(anchor="w")

        area = tk.Frame(conteudo, bg=self.BG)
        area.pack(fill="both", expand=True, padx=34, pady=(0, 30))

        tk.Label(
            area,
            text="Ações rápidas",
            bg=self.BG,
            fg=self.TEXT,
            font=(self.FONT, 13, "bold"),
        ).pack(anchor="w", pady=(0, 12))

        grade = tk.Frame(area, bg=self.BG)
        grade.pack(fill="both", expand=True)

        acoes = [
            ("＋", "Adicionar disciplina", "Cadastre uma nova disciplina e suas notas.", self.tela_adicionar_disciplina, self.PRIMARY),
            ("⌕", "Consultar disciplina", "Veja notas, média e situação de uma disciplina.", self.tela_consultar_disciplina, "#7C3AED"),
            ("✎", "Alterar notas", "Atualize as avaliações já cadastradas.", self.tela_alterar_notas, "#0891B2"),
            ("−", "Excluir disciplina", "Remova uma disciplina do seu histórico.", self.tela_excluir_disciplina, self.DANGER),
            ("F", "Nota da final", "Atualize a nota da avaliação final.", self.tela_alterar_final, self.WARNING),
            ("▦", "Resumo acadêmico", "Visualize seu histórico completo e a média geral.", self.tela_resumo, self.SUCCESS),
            ("R", "Ranking", "Visualize as disciplinas rankeadas pela nota", self.tela_ranking, "#9EB208")
        ]

        for coluna in range(2):
            grade.grid_columnconfigure(coluna, weight=1, uniform="acoes")
        for linha in range(3):
            grade.grid_rowconfigure(linha, weight=1)

        for i, (icone, titulo, descricao, comando, cor) in enumerate(acoes):
            linha, coluna = divmod(i, 2)

            card = tk.Frame(
                grade,
                bg=self.CARD,
                highlightbackground=self.BORDER,
                highlightthickness=1,
                cursor="hand2",
            )
            card.grid(
                row=linha,
                column=coluna,
                sticky="nsew",
                padx=(0 if coluna == 0 else 8, 0 if coluna == 1 else 8),
                pady=(0 if linha == 0 else 8, 8 if linha < 2 else 0),
            )

            inner = tk.Frame(card, bg=self.CARD)
            inner.pack(fill="both", expand=True, padx=18, pady=17)

            icone_box = tk.Label(
                inner,
                text=icone,
                bg=cor,
                fg=self.WHITE,
                width=3,
                height=1,
                font=(self.FONT, 15, "bold"),
            )
            icone_box.pack(anchor="w")

            tk.Label(
                inner,
                text=titulo,
                bg=self.CARD,
                fg=self.TEXT,
                font=(self.FONT, 11, "bold"),
            ).pack(anchor="w", pady=(13, 5))

            tk.Label(
                inner,
                text=descricao,
                bg=self.CARD,
                fg=self.MUTED,
                justify="left",
                wraplength=340,
                font=(self.FONT, 9),
            ).pack(anchor="w")

            widgets = [card, inner, icone_box]
            for widget in widgets:
                widget.bind("<Button-1>", lambda _e, cmd=comando: cmd())
                widget.bind(
                    "<Enter>",
                    lambda _e, c=card: c.configure(
                        bg=self.CARD_HOVER, highlightbackground="#36557B"
                    ),
                )
                widget.bind(
                    "<Leave>",
                    lambda _e, c=card: c.configure(
                        bg=self.CARD, highlightbackground=self.BORDER
                    ),
                )

    def _formulario_disciplina(self, titulo, subtitulo, comando, texto_botao):
        janela = tk.Toplevel(self.janela)
        janela.title(titulo)
        janela.configure(bg=self.BG)
        janela.resizable(False, False)
        self._centralizar(janela, 510, 610)
        janela.transient(self.janela)
        janela.grab_set()

        self._criar_cabecalho_janela(janela, titulo, subtitulo)

        corpo = tk.Frame(janela, bg=self.BG)
        corpo.pack(fill="both", expand=True, padx=30, pady=24)

        _, entrada_nome = self._campo(corpo, "NOME DA DISCIPLINA")
        entrada_nome.pack(fill="x", pady=(0, 22))

        bloco_notas = tk.Frame(
            corpo,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        bloco_notas.pack(fill="x", pady=(0, 24))

        tk.Label(
            bloco_notas,
            text="NOTAS",
            bg=self.CARD,
            fg=self.MUTED,
            font=(self.FONT, 8, "bold"),
        ).pack(anchor="w", padx=16, pady=(15, 10))

        campos = {}
        grade = tk.Frame(bloco_notas, bg=self.CARD)
        grade.pack(fill="x", padx=16, pady=(0, 16))

        nomes = ["AV1", "AV2", "AV3", "EDAG"]

        for i, nome_campo in enumerate(nomes):
            bloco = tk.Frame(grade, bg=self.CARD)
            bloco.grid(row=i // 2, column=i % 2, sticky="ew", padx=5, pady=7)

            tk.Label(
                bloco,
                text=nome_campo,
                bg=self.CARD,
                fg=self.MUTED,
                font=(self.FONT, 8, "bold"),
            ).pack(anchor="w", pady=(0, 5))

            entrada = ttk.Entry(bloco, style="Modern.TEntry")
            entrada.pack(fill="x")
            campos[nome_campo] = entrada

        grade.grid_columnconfigure(0, weight=1)
        grade.grid_columnconfigure(1, weight=1)

        def salvar():
            try:
                nome = entrada_nome.get().strip()
                av1 = float(campos["AV1"].get())
                av2 = float(campos["AV2"].get())
                av3 = float(campos["AV3"].get())
                edag = float(campos["EDAG"].get())

                if not nome:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Dados inválidos",
                    "Digite um nome de disciplina e notas válidas.",
                    parent=janela,
                )
                return

            sucesso = comando(nome, av1, av2, av3, edag)

            if sucesso:
                messagebox.showinfo(
                    "Operação concluída",
                    "Disciplina salva com sucesso!",
                    parent=janela,
                )
                janela.destroy()
            else:
                messagebox.showerror(
                    "Não foi possível salvar",
                    "Essa disciplina já está cadastrada.",
                    parent=janela,
                )

        self._botao(
            corpo,
            texto_botao,
            salvar,
            largura=30,
            primaria=True,
            altura=2,
        ).pack(fill="x")

        entrada_nome.focus_set()
        return janela

    def tela_adicionar_disciplina(self):
        self._formulario_disciplina(
            "Adicionar disciplina",
            "Cadastre a disciplina e informe as notas das avaliações.",
            self.historico.adicionar_disciplina,
            "ADICIONAR DISCIPLINA",
        )

    def tela_consultar_disciplina(self):
        janela = tk.Toplevel(self.janela)
        janela.title("Consultar disciplina")
        janela.configure(bg=self.BG)
        janela.resizable(False, False)
        self._centralizar(janela, 610, 620)
        janela.transient(self.janela)
        janela.grab_set()

        self._criar_cabecalho_janela(
            janela,
            "Consultar disciplina",
            "Pesquise pelo nome para visualizar o desempenho acadêmico.",
        )

        corpo = tk.Frame(janela, bg=self.BG)
        corpo.pack(fill="both", expand=True, padx=30, pady=22)

        _, entrada_nome = self._campo(corpo, "NOME DA DISCIPLINA")
        entrada_nome.pack(fill="x", pady=(0, 12))

        def consultar():
            nome = entrada_nome.get().strip()
            disciplina = self.historico.listar_disciplina_por_nome(nome)

            if disciplina is None:
                messagebox.showerror(
                    "Disciplina não encontrada",
                    "Não foi encontrada nenhuma disciplina com esse nome.",
                    parent=janela,
                )
                return

            self._mostrar_detalhes(janela, disciplina)

        self._botao(
            corpo,
            "CONSULTAR",
            consultar,
            largura=25,
            primaria=True,
            altura=2,
        ).pack(anchor="w", pady=(0, 20))

        resultado = tk.Frame(
            corpo,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        resultado.pack(fill="both", expand=True)

        tk.Label(
            resultado,
            text="RESULTADO",
            bg=self.CARD,
            fg=self.MUTED,
            font=(self.FONT, 8, "bold"),
        ).pack(anchor="w", padx=18, pady=(16, 8))

        self.consulta_resultado = resultado
        self.consulta_resultado_nome = tk.Label(
            resultado,
            text="Nenhuma disciplina consultada.",
            bg=self.CARD,
            fg=self.MUTED,
            justify="left",
            font=(self.FONT, 10),
        )
        self.consulta_resultado_nome.pack(anchor="w", padx=18, pady=12)

        entrada_nome.bind("<Return>", lambda _e: consultar())
        entrada_nome.focus_set()

    def _mostrar_detalhes(self, parent, disciplina):
        for widget in self.consulta_resultado.winfo_children()[1:]:
            widget.destroy()

        tk.Label(
            self.consulta_resultado,
            text=disciplina.nome,
            bg=self.CARD,
            fg=self.TEXT,
            font=(self.FONT, 16, "bold"),
        ).pack(anchor="w", padx=18, pady=(2, 12))

        linhas = [
            ("AV1", f"{disciplina.av1:.2f}"),
            ("AV2", f"{disciplina.av2:.2f}"),
            ("AV3", f"{disciplina.av3:.2f}"),
            ("EDAG", f"{disciplina.edag:.2f}"),
            ("Média", f"{disciplina.media:.2f}"),
            ("Média Final", f"{disciplina.media_final:.2f}"),
            ("Situação", disciplina.situacao),
        ]

        tabela = tk.Frame(self.consulta_resultado, bg=self.CARD)
        tabela.pack(fill="x", padx=18, pady=(0, 18))

        for i, (campo, valor) in enumerate(linhas):
            tk.Label(
                tabela,
                text=campo,
                bg=self.CARD,
                fg=self.MUTED,
                font=(self.FONT, 9, "bold"),
            ).grid(row=i, column=0, sticky="w", pady=5)

            cor = self.SUCCESS if campo == "Situação" and "Aprov" in valor else self.TEXT

            tk.Label(
                tabela,
                text=valor,
                bg=self.CARD,
                fg=cor,
                font=(self.FONT, 10, "bold"),
            ).grid(row=i, column=1, sticky="e", padx=(30, 0), pady=5)

        tabela.grid_columnconfigure(1, weight=1)
        parent.update_idletasks()

    def tela_alterar_notas(self):
        janela = tk.Toplevel(self.janela)
        janela.title("Alterar notas")
        janela.configure(bg=self.BG)
        janela.resizable(False, False)
        self._centralizar(janela, 510, 610)
        janela.transient(self.janela)
        janela.grab_set()

        self._criar_cabecalho_janela(
            janela,
            "Alterar notas",
            "Atualize todas as avaliações da disciplina selecionada.",
        )

        corpo = tk.Frame(janela, bg=self.BG)
        corpo.pack(fill="both", expand=True, padx=30, pady=24)

        _, entrada_nome = self._campo(corpo, "NOME DA DISCIPLINA")
        entrada_nome.pack(fill="x", pady=(0, 22))

        bloco_notas = tk.Frame(
            corpo,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        bloco_notas.pack(fill="x", pady=(0, 24))

        tk.Label(
            bloco_notas,
            text="NOVAS NOTAS",
            bg=self.CARD,
            fg=self.MUTED,
            font=(self.FONT, 8, "bold"),
        ).pack(anchor="w", padx=16, pady=(15, 10))

        campos = {}
        grade = tk.Frame(bloco_notas, bg=self.CARD)
        grade.pack(fill="x", padx=16, pady=(0, 16))

        for i, nome_campo in enumerate(["AV1", "AV2", "AV3", "EDAG"]):
            bloco = tk.Frame(grade, bg=self.CARD)
            bloco.grid(row=i // 2, column=i % 2, sticky="ew", padx=5, pady=7)

            tk.Label(
                bloco,
                text=nome_campo,
                bg=self.CARD,
                fg=self.MUTED,
                font=(self.FONT, 8, "bold"),
            ).pack(anchor="w", pady=(0, 5))

            entrada = ttk.Entry(bloco, style="Modern.TEntry")
            entrada.pack(fill="x")
            campos[nome_campo] = entrada

        grade.grid_columnconfigure(0, weight=1)
        grade.grid_columnconfigure(1, weight=1)

        def alterar():
            try:
                nome = entrada_nome.get().strip()
                av1 = float(campos["AV1"].get())
                av2 = float(campos["AV2"].get())
                av3 = float(campos["AV3"].get())
                edag = float(campos["EDAG"].get())

                if not nome:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Dados inválidos",
                    "Digite um nome de disciplina e notas válidas.",
                    parent=janela,
                )
                return

            sucesso = self.historico.alterar_notas_disciplina(
                nome,
                av1,
                av2,
                av3,
                edag,
            )

            if sucesso:
                messagebox.showinfo(
                    "Operação concluída",
                    "Notas alteradas com sucesso!",
                    parent=janela,
                )
                janela.destroy()
            else:
                messagebox.showerror(
                    "Disciplina não encontrada",
                    "Não foi encontrada nenhuma disciplina com esse nome.",
                    parent=janela,
                )

        self._botao(
            corpo,
            "SALVAR ALTERAÇÕES",
            alterar,
            largura=30,
            primaria=True,
            altura=2,
        ).pack(fill="x")

        entrada_nome.focus_set()

    def tela_excluir_disciplina(self):
        janela = tk.Toplevel(self.janela)
        janela.title("Excluir disciplina")
        janela.configure(bg=self.BG)
        janela.resizable(False, False)
        self._centralizar(janela, 500, 410)
        janela.transient(self.janela)
        janela.grab_set()

        self._criar_cabecalho_janela(
            janela,
            "Excluir disciplina",
            "Essa ação removerá permanentemente a disciplina do histórico.",
        )

        corpo = tk.Frame(janela, bg=self.BG)
        corpo.pack(fill="both", expand=True, padx=30, pady=22)

        _, entrada_nome = self._campo(corpo, "NOME DA DISCIPLINA")
        entrada_nome.pack(fill="x", pady=(0, 25))

        aviso = tk.Frame(
            corpo,
            bg="#2A1720",
            highlightbackground="#5A2532",
            highlightthickness=1,
        )
        aviso.pack(fill="x", pady=(0, 24))

        tk.Label(
            aviso,
            text="Atenção",
            bg="#2A1720",
            fg="#FDA4AF",
            font=(self.FONT, 9, "bold"),
        ).pack(anchor="w", padx=14, pady=(12, 4))

        tk.Label(
            aviso,
            text="A disciplina será removida do histórico acadêmico.",
            bg="#2A1720",
            fg="#FBCFE8",
            font=(self.FONT, 9),
        ).pack(anchor="w", padx=14, pady=(0, 12))

        def excluir():
            nome = entrada_nome.get().strip()

            if not nome:
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Digite o nome da disciplina.",
                    parent=janela,
                )
                return

            disciplina = self.historico.buscar_disciplina(nome)

            if disciplina is None:
                messagebox.showerror(
                    "Disciplina não encontrada",
                    "Não foi encontrada nenhuma disciplina com esse nome.",
                    parent=janela,
                )
                return

            confirmar = messagebox.askyesno(
                "Confirmar exclusão",
                f"Deseja realmente excluir '{disciplina.nome}'?",
                parent=janela,
            )

            if not confirmar:
                return

            self.historico.excluir_disciplina(nome)

            messagebox.showinfo(
                "Exclusão concluída",
                "Disciplina excluída com sucesso!",
                parent=janela,
            )
            janela.destroy()

        self._botao(
            corpo,
            "EXCLUIR DISCIPLINA",
            excluir,
            largura=30,
            primaria=True,
            altura=2,
            cor=self.DANGER,
            cor_hover="#F87171",
        )

        entrada_nome.focus_set()

    def tela_alterar_final(self):
        janela = tk.Toplevel(self.janela)
        janela.title("Nota da final")
        janela.configure(bg=self.BG)
        janela.resizable(False, False)
        self._centralizar(janela, 500, 455)
        janela.transient(self.janela)
        janela.grab_set()

        self._criar_cabecalho_janela(
            janela,
            "Alterar nota da final",
            "Atualize a nota final de uma disciplina em situação de Final.",
        )

        corpo = tk.Frame(janela, bg=self.BG)
        corpo.pack(fill="both", expand=True, padx=30, pady=24)

        _, entrada_nome = self._campo(corpo, "NOME DA DISCIPLINA")
        entrada_nome.pack(fill="x", pady=(0, 18))

        _, entrada_nota = self._campo(corpo, "NOVA NOTA DA FINAL")
        entrada_nota.pack(fill="x", pady=(0, 26))

        def alterar():
            nome = entrada_nome.get().strip()

            try:
                nota = float(entrada_nota.get())
            except ValueError:
                messagebox.showerror(
                    "Nota inválida",
                    "Digite uma nota numérica válida.",
                    parent=janela,
                )
                return

            resultado = self.historico.alterar_nota_final(nome, nota)

            if resultado is True:
                messagebox.showinfo(
                    "Operação concluída",
                    "Nota da final alterada com sucesso!",
                    parent=janela,
                )
                janela.destroy()
            elif resultado is False:
                messagebox.showerror(
                    "Disciplina não encontrada",
                    "Não foi encontrada nenhuma disciplina com esse nome.",
                    parent=janela,
                )
            else:
                messagebox.showwarning(
                    "Operação indisponível",
                    "Essa disciplina não está em situação de Final.",
                    parent=janela,
                )

        self._botao(
            corpo,
            "ALTERAR NOTA",
            alterar,
            largura=30,
            primaria=True,
            altura=2,
        ).pack(fill="x")

        entrada_nome.focus_set()

    def tela_ranking(self):

        janela = tk.Toplevel(self.janela)

        janela.title("Ranking das disciplinas")
        janela.geometry("600x450")

        tk.Label(
            janela,
            text="Ranking das Disciplinas",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        ranking = self.historico.ranking_disciplinas()

        if not ranking:

            tk.Label(
                janela,
                text="Nenhuma disciplina cadastrada."
            ).pack(pady=30)

            return

        for i, disciplina in enumerate(ranking, start=1):

            texto = (
                f"{i}º  {disciplina.nome} "
                f"- Média: {disciplina.media_final:.2f}"
            )

            tk.Label(
                janela,
                text=texto,
                font=("Arial", 13)
            ).pack(anchor="w", padx=40, pady=5)

    def tela_resumo(self):
        janela = tk.Toplevel(self.janela)
        janela.title("Resumo acadêmico")
        janela.configure(bg=self.BG)
        janela.resizable(True, True)
        self._centralizar(janela, 900, 610)
        janela.minsize(800, 520)
        janela.transient(self.janela)
        janela.grab_set()

        self._criar_cabecalho_janela(
            janela,
            "Resumo acadêmico",
            "Visão geral de todas as disciplinas cadastradas.",
        )

        corpo = tk.Frame(janela, bg=self.BG)
        corpo.pack(fill="both", expand=True, padx=28, pady=(10, 28))

        topo = tk.Frame(corpo, bg=self.BG)
        topo.pack(fill="x", pady=(0, 14))

        try:
            media = self.historico.media_geral()
            media_texto = f"{media:.2f}"
        except Exception:
            media_texto = "--"

        tk.Label(
            topo,
            text="MÉDIA GERAL",
            bg=self.BG,
            fg=self.MUTED,
            font=(self.FONT, 8, "bold"),
        ).pack(side="left")

        tk.Label(
            topo,
            text=media_texto,
            bg=self.BG,
            fg=self.SUCCESS,
            font=(self.FONT, 18, "bold"),
        ).pack(side="left", padx=(8, 0))

        tabela_frame = tk.Frame(
            corpo,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        tabela_frame.pack(fill="both", expand=True)

        colunas = (
            "disciplina",
            "av1",
            "av2",
            "av3",
            "edag",
            "media",
            "final",
            "situacao",
        )

        tree = ttk.Treeview(
            tabela_frame,
            columns=colunas,
            show="headings",
            style="Modern.Treeview",
            selectmode="browse",
        )
        tree.pack(side="left", fill="both", expand=True, padx=1, pady=1)

        scroll = ttk.Scrollbar(
            tabela_frame,
            orient="vertical",
            command=tree.yview,
        )
        scroll.pack(side="right", fill="y", padx=(0, 1), pady=1)
        tree.configure(yscrollcommand=scroll.set)

        cabecalhos = {
            "disciplina": "DISCIPLINA",
            "av1": "AV1",
            "av2": "AV2",
            "av3": "AV3",
            "edag": "EDAG",
            "media": "MÉDIA",
            "final": "FINAL",
            "situacao": "SITUAÇÃO",
        }

        larguras = {
            "disciplina": 210,
            "av1": 70,
            "av2": 70,
            "av3": 70,
            "edag": 70,
            "media": 75,
            "final": 75,
            "situacao": 115,
        }

        for coluna in colunas:
            tree.heading(coluna, text=cabecalhos[coluna])
            tree.column(
                coluna,
                width=larguras[coluna],
                anchor="w" if coluna in ("disciplina", "situacao") else "center",
                stretch=coluna == "disciplina",
            )

        disciplinas = self.historico.resumo_academico()

        if not disciplinas:
            tree.insert(
                "",
                "end",
                values=("Nenhuma disciplina cadastrada.", "", "", "", "", "", "", ""),
            )
        else:
            for disciplina in disciplinas:
                tree.insert(
                    "",
                    "end",
                    values=(
                        disciplina.nome,
                        f"{disciplina.av1:.2f}",
                        f"{disciplina.av2:.2f}",
                        f"{disciplina.av3:.2f}",
                        f"{disciplina.edag:.2f}",
                        f"{disciplina.media:.2f}",
                        f"{disciplina.media_final:.2f}",
                        disciplina.situacao,
                    ),
                )

    def sair(self):
        resposta = messagebox.askyesno(
            "Encerrar sistema",
            "Deseja realmente sair do sistema?",
            parent=self.janela,
        )

        if resposta:
            self.janela.destroy()


if __name__ == "__main__":
    app = Interface()
    app.iniciar()