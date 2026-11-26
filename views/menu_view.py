
import customtkinter as ctk

from tkinter import ttk, messagebox


class MenuView:

    MODULOS = {

        "Categorias": {
            "pk": "id_categoria",

            "campos": [
                ("Nome", "nome")
            ],

            "colunas": [
                "id_categoria",
                "nome"
            ]
        },

        "Produtos": {
            "pk": "id_produto",

            "campos": [
                ("Nome", "nome"),
                ("Código", "codigo"),
                ("Preço", "preco"),
                ("Estoque", "estoque"),
                ("ID da categoria", "id_categoria")
            ],

            "colunas": [
                "id_produto",
                "nome",
                "codigo",
                "preco",
                "estoque",
                "categoria",
                "id_categoria"
            ]
        },

        "Clientes": {
            "pk": "id_cliente",

            "campos": [
                ("Nome", "nome"),
                ("CPF", "cpf"),
                ("Endereço", "endereco")
            ],

            "colunas": [
                "id_cliente",
                "nome",
                "cpf",
                "endereco"
            ]
        },

        "Vendedores": {
            "pk": "id_vendedor",

            "campos": [
                ("Nome", "nome"),
                ("CPF", "cpf"),
                ("Endereço", "endereco")
            ],

            "colunas": [
                "id_vendedor",
                "nome",
                "cpf",
                "endereco"
            ]
        }
    }

    def __init__(self, controller):

        self.controller = controller

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.janela = ctk.CTk()

        self.janela.title("Sistema de Mercado")
        self.janela.geometry("1200x720")
        self.janela.minsize(1000, 600)

        # MENU LATERAL

        self.menu = ctk.CTkFrame(
            self.janela,
            width=215,
            corner_radius=0
        )

        self.menu.pack(
            side="left",
            fill="y"
        )

        self.menu.pack_propagate(False)

        ctk.CTkLabel(
            self.menu,
            text="MERCADO",
            font=("Arial", 25, "bold")
        ).pack(pady=(32, 35))

        botoes = [
            "Dashboard",
            "Categorias",
            "Produtos",
            "Clientes",
            "Vendedores",
            "Vendas"
        ]

        for nome in botoes:

            ctk.CTkButton(
                self.menu,
                text=nome,
                height=42,
                command=lambda n=nome: self.mostrar_pagina(n)
            ).pack(
                fill="x",
                padx=14,
                pady=6
            )

        ctk.CTkButton(
            self.menu,
            text="Sair",
            fg_color="#8B2525",
            hover_color="#641B1B",
            command=self.janela.destroy
        ).pack(
            side="bottom",
            fill="x",
            padx=14,
            pady=22
        )

        # ÁREA PRINCIPAL

        self.conteudo = ctk.CTkFrame(
            self.janela,
            fg_color="transparent",
            corner_radius=0
        )

        self.conteudo.pack(
            side="right",
            fill="both",
            expand=True,
            padx=24,
            pady=22
        )

        self.modulo_atual = None

        self.mostrar_pagina("Dashboard")

    def limpar(self):

        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def titulo(self, texto, descricao=None):

        ctk.CTkLabel(
            self.conteudo,
            text=texto,
            font=("Arial", 28, "bold")
        ).pack(
            anchor="w",
            pady=(4, 4)
        )

        if descricao:

            ctk.CTkLabel(
                self.conteudo,
                text=descricao,
                text_color="gray"
            ).pack(
                anchor="w",
                pady=(0, 15)
            )

    def mostrar_pagina(self, nome):

        self.limpar()

        self.modulo_atual = nome

        if nome == "Dashboard":

            self.pagina_dashboard()

        elif nome == "Vendas":

            self.pagina_vendas()

        else:

            self.pagina_cadastro(nome)

    # DASHBOARD

    def pagina_dashboard(self):

        self.titulo(
            "Dashboard",
            "Resumo geral do seu mercado"
        )

        dados = self.controller.dashboard()

        cards = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )

        cards.pack(
            fill="x",
            pady=15
        )

        indicadores = [
            ("Produtos cadastrados", dados["produtos"]),
            ("Clientes", dados["clientes"]),
            ("Vendedores", dados["vendedores"]),
            ("Vendas realizadas", dados["vendas"]),
            (
                "Faturamento total",
                f'R$ {float(dados["faturamento"]):.2f}'
            )
        ]

        for indice, (rotulo, valor) in enumerate(indicadores):

            card = ctk.CTkFrame(
                cards,
                corner_radius=12
            )

            card.grid(
                row=indice // 2,
                column=indice % 2,
                padx=8,
                pady=8,
                sticky="nsew"
            )

            ctk.CTkLabel(
                card,
                text=rotulo,
                text_color="gray",
                font=("Arial", 14)
            ).pack(
                anchor="w",
                padx=18,
                pady=(16, 5)
            )

            ctk.CTkLabel(
                card,
                text=str(valor),
                font=("Arial", 25, "bold")
            ).pack(
                anchor="w",
                padx=18,
                pady=(0, 16)
            )

        cards.grid_columnconfigure(0, weight=1)
        cards.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            self.conteudo,
            text="Atualizar indicadores",
            command=lambda: self.mostrar_pagina("Dashboard")
        ).pack(
            anchor="w",
            pady=12
        )

    # CATEGORIAS, PRODUTOS, CLIENTES E VENDEDORES

    def pagina_cadastro(self, modulo):

        config = self.MODULOS[modulo]

        self.titulo(
            modulo,
            f"Gerencie os registros de {modulo.lower()}"
        )

        # BOTÕES

        acoes = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )

        acoes.pack(
            fill="x",
            pady=(0, 12)
        )

        ctk.CTkButton(
            acoes,
            text="Cadastrar novo",
            command=lambda: self.formulario(modulo)
        ).pack(
            side="left",
            padx=(0, 8)
        )

        ctk.CTkButton(
            acoes,
            text="Atualizar lista",
            fg_color="#444444",
            command=lambda: self.carregar_tabela(modulo)
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            acoes,
            text="Editar selecionado",
            fg_color="#8A641D",
            command=lambda: self.editar_selecionado(modulo)
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            acoes,
            text="Excluir selecionado",
            fg_color="#8B2525",
            hover_color="#641B1B",
            command=lambda: self.excluir_selecionado(modulo)
        ).pack(
            side="left",
            padx=5
        )

        # ÁREA DO FORMULÁRIO
        # O formulário aparece dentro da janela principal.

        self.form_area = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )

        self.form_area.pack(
            fill="x"
        )

        # TABELA

        area = ctk.CTkFrame(
            self.conteudo
        )

        area.pack(
            fill="both",
            expand=True
        )

        colunas = config["colunas"]

        self.tabela = ttk.Treeview(
            area,
            columns=colunas,
            show="headings"
        )

        for coluna in colunas:

            self.tabela.heading(
                coluna,
                text=coluna.replace("_", " ").title()
            )

            self.tabela.column(
                coluna,
                width=125,
                anchor="center"
            )

        barra_y = ttk.Scrollbar(
            area,
            orient="vertical",
            command=self.tabela.yview
        )

        barra_x = ttk.Scrollbar(
            area,
            orient="horizontal",
            command=self.tabela.xview
        )

        self.tabela.configure(
            yscrollcommand=barra_y.set,
            xscrollcommand=barra_x.set
        )

        self.tabela.pack(
            side="top",
            fill="both",
            expand=True
        )

        barra_y.pack(
            side="right",
            fill="y"
        )

        barra_x.pack(
            side="bottom",
            fill="x"
        )

        self.carregar_tabela(modulo)

    def carregar_tabela(self, modulo):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        registros = self.controller.listar(modulo)

        colunas = self.MODULOS[modulo]["colunas"]

        for registro in registros:

            valores = [
                registro.get(coluna, "")
                for coluna in colunas
            ]

            self.tabela.insert(
                "",
                "end",
                values=valores
            )

    # FORMULÁRIO DE CADASTRO E EDIÇÃO

    def formulario(self, modulo, registro=None):

        config = self.MODULOS[modulo]

        identificador = None

        if registro:
            identificador = registro.get(config["pk"])

        # Limpa o formulário anterior
        for widget in self.form_area.winfo_children():
            widget.destroy()

        painel = ctk.CTkFrame(
            self.form_area
        )

        painel.pack(
            fill="x",
            pady=10
        )

        ctk.CTkLabel(
            painel,
            text="Editar registro" if registro else "Novo cadastro",
            font=("Arial", 18, "bold")
        ).pack(
            anchor="w",
            padx=12,
            pady=(10, 4)
        )

        grade = ctk.CTkFrame(
            painel,
            fg_color="transparent"
        )

        grade.pack(
            fill="x",
            padx=8
        )

        entradas = {}

        for indice, (rotulo, campo) in enumerate(config["campos"]):

            grupo = ctk.CTkFrame(
                grade,
                fg_color="transparent"
            )

            grupo.grid(
                row=indice // 2,
                column=indice % 2,
                padx=5,
                pady=5,
                sticky="ew"
            )

            ctk.CTkLabel(
                grupo,
                text=rotulo
            ).pack(
                anchor="w"
            )

            entrada = ctk.CTkEntry(
                grupo,
                width=260
            )

            entrada.pack(
                fill="x"
            )

            if registro:

                valor = registro.get(campo, "")

                entrada.insert(
                    0,
                    str(valor) if valor is not None else ""
                )

            entradas[campo] = entrada

        grade.grid_columnconfigure(0, weight=1)
        grade.grid_columnconfigure(1, weight=1)

        botoes = ctk.CTkFrame(
            painel,
            fg_color="transparent"
        )

        botoes.pack(
            anchor="e",
            padx=12,
            pady=10
        )

        def salvar():

            valores = [
                entradas[campo].get().strip()
                for _, campo in config["campos"]
            ]

            sucesso, mensagem = self.controller.salvar(
                modulo,
                valores,
                identificador
            )

            if sucesso:

                messagebox.showinfo(
                    "Sistema de Mercado",
                    mensagem
                )

                painel.destroy()

                self.carregar_tabela(modulo)

            else:

                messagebox.showerror(
                    "Atenção",
                    mensagem
                )

        ctk.CTkButton(
            botoes,
            text="Salvar",
            command=salvar
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            fg_color="#555555",
            command=painel.destroy
        ).pack(
            side="left",
            padx=5
        )

    # SELEÇÃO, EDIÇÃO E EXCLUSÃO

    def obter_selecionado(self):

        selecionados = self.tabela.selection()

        if not selecionados:

            messagebox.showwarning(
                "Atenção",
                "Selecione um registro na tabela."
            )

            return None

        return self.tabela.item(
            selecionados[0],
            "values"
        )

    def editar_selecionado(self, modulo):

        valores = self.obter_selecionado()

        if valores is None:
            return

        colunas = self.MODULOS[modulo]["colunas"]

        registro = dict(
            zip(colunas, valores)
        )

        self.formulario(
            modulo,
            registro
        )

    def excluir_selecionado(self, modulo):

        valores = self.obter_selecionado()

        if valores is None:
            return

        identificador = valores[0]

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir este registro?"
        )

        if not confirmar:
            return

        sucesso, mensagem = self.controller.excluir(
            modulo,
            identificador
        )

        if sucesso:

            messagebox.showinfo(
                "Sistema de Mercado",
                mensagem
            )

            self.carregar_tabela(modulo)

        else:

            messagebox.showerror(
                "Erro",
                mensagem
            )

    # VENDAS

    def pagina_vendas(self):

        self.titulo(
            "Vendas",
            "Registre uma venda e consulte o histórico"
        )

        formulario = ctk.CTkFrame(
            self.conteudo
        )

        formulario.pack(
            fill="x",
            pady=(0, 15)
        )

        ctk.CTkLabel(
            formulario,
            text="Registrar venda",
            font=("Arial", 18, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            padx=12,
            pady=10,
            sticky="w"
        )

        campos = [
            "ID do cliente",
            "ID do vendedor (opcional)",
            "ID do produto",
            "Quantidade"
        ]

        entradas = {}

        for coluna, rotulo in enumerate(campos):

            grupo = ctk.CTkFrame(
                formulario,
                fg_color="transparent"
            )

            grupo.grid(
                row=1,
                column=coluna,
                padx=8,
                pady=8,
                sticky="ew"
            )

            ctk.CTkLabel(
                grupo,
                text=rotulo
            ).pack(
                anchor="w"
            )

            entrada = ctk.CTkEntry(
                grupo,
                width=150
            )

            entrada.pack(
                fill="x"
            )

            entradas[rotulo] = entrada

            formulario.grid_columnconfigure(
                coluna,
                weight=1
            )

        def registrar():

            sucesso, mensagem = self.controller.registrar_venda(
                entradas["ID do cliente"].get(),
                entradas["ID do vendedor (opcional)"].get(),
                entradas["ID do produto"].get(),
                entradas["Quantidade"].get()
            )

            if sucesso:

                messagebox.showinfo(
                    "Venda",
                    mensagem
                )

                for entrada in entradas.values():
                    entrada.delete(0, "end")

                self.carregar_vendas()

            else:

                messagebox.showerror(
                    "Erro na venda",
                    mensagem
                )

        ctk.CTkButton(
            formulario,
            text="Registrar venda",
            command=registrar
        ).grid(
            row=2,
            column=0,
            columnspan=4,
            padx=10,
            pady=(5, 12)
        )

        ctk.CTkLabel(
            self.conteudo,
            text="Histórico de vendas",
            font=("Arial", 18, "bold")
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        colunas = [
            "id_venda",
            "data_venda",
            "cliente",
            "vendedor",
            "total"
        ]

        area = ctk.CTkFrame(
            self.conteudo
        )

        area.pack(
            fill="both",
            expand=True
        )

        self.tabela_vendas = ttk.Treeview(
            area,
            columns=colunas,
            show="headings"
        )

        for coluna in colunas:

            self.tabela_vendas.heading(
                coluna,
                text=coluna.replace("_", " ").title()
            )

            self.tabela_vendas.column(
                coluna,
                width=150,
                anchor="center"
            )

        self.tabela_vendas.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        ctk.CTkButton(
            self.conteudo,
            text="Atualizar histórico",
            command=self.carregar_vendas
        ).pack(
            anchor="e",
            pady=8
        )

        self.carregar_vendas()

    def carregar_vendas(self):

        for item in self.tabela_vendas.get_children():
            self.tabela_vendas.delete(item)

        vendas = self.controller.listar("Vendas")

        for venda in vendas:

            valores = [
                venda["id_venda"],
                venda["data_venda"],
                venda["cliente"],
                venda["vendedor"],
                f'R$ {float(venda["total"]):.2f}'
            ]

            self.tabela_vendas.insert(
                "",
                "end",
                values=valores
            )

    def iniciar(self):

        self.janela.mainloop()
