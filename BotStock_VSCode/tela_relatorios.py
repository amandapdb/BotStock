import customtkinter as ctk
import tkinter.messagebox as msg
from database import relatorio_estoque_por_nicho, listar_fornecedores, deletar_fornecedor
from database import listar_usuarios, deletar_usuario, cadastrar_usuario, buscar_ultima_movimentacao
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class TelaRelatorios(ctk.CTkFrame):
    def __init__(self, master, email_usuario):
        super().__init__(master)
        self.email_usuario = email_usuario

        self.pack(fill="both", expand=True)
        self.configure(fg_color="#0F293D")
        master.title("BotStock - Relatórios")


        # TÍTULO
        self.titulo = ctk.CTkLabel(
            self, text="Relatórios", font=ctk.CTkFont(size=35, weight="bold"),
            text_color="white")
        self.titulo.pack(anchor="w", padx=65, pady=(15, 10))


        # BOTÃO VOLTAR
        btn_voltar = ctk.CTkButton(
            self, text="↩", font=ctk.CTkFont(size=25), width=50, height=50,
            command=self.voltar_principal, fg_color="transparent", hover_color="#0300cc",
            text_color="white", cursor="hand2")
        btn_voltar.place(x=10, y=10)


       # ÁREA PRINCIPAL
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=10)


        # LINHA DE CIMA
        self.linha_superior = ctk.CTkFrame(self.container, fg_color="transparent")
        self.linha_superior.pack(fill="both", expand=True, pady=(0, 10))


        # FRAME A
        self.frame_a = ctk.CTkFrame(self.linha_superior, fg_color="#12324A", corner_radius=15)
        self.frame_a.pack(side="left", fill="both", expand=True, padx=(0, 10))


        # SUBTÍTULO
        self.subtitulo = ctk.CTkLabel(
            self.frame_a, text="Opções:", font=ctk.CTkFont(size=35, weight="bold"),
            text_color="white")
        self.subtitulo.pack(anchor="w", padx=45, pady=(15, 10))


        #CONFIGURAÇÕES PADRÃO PARA OS BOTÕES
        botao_config = {
            "width": 260, "height": 50, "corner_radius": 10,
            "font": ctk.CTkFont( size=20, weight="bold"),
            "fg_color": "#1f6aa5", "hover_color": "#155a8a"}


        #CAIXA PARA BOTÕES
        self.area_botoes = ctk.CTkFrame(self.frame_a, width=300, fg_color="transparent")
        self.area_botoes.pack(pady=20)
        self.area_botoes.pack_propagate(False)


        #BOTÃO EXCLUIR FORNECEDORES
        self.btn_editar_fornecedor = ctk.CTkButton(
            self.area_botoes, text="Editar Fornecedores", command=self.abrir_popup_fornecedor,
            **botao_config)
        self.btn_editar_fornecedor.pack(pady=10)


        #BOTÃO EDITAR CADASTROS
        self.btn_cadastrar_cadastro = ctk.CTkButton(
            self.area_botoes, text="Cadastrar Usuários", command=self.abrir_popup_cadastro_funcionario,
            **botao_config)
        self.btn_cadastrar_cadastro.pack(pady=10)


        #BOTÃO EXCLUIR USUÁRIOS
        self.btn_editar_usuario = ctk.CTkButton(
            self.area_botoes, text="Editar Usuários", command=self.abrir_popup_funcionarios,
            **botao_config)
        self.btn_editar_usuario.pack(pady=10)


        # FRAME B
        self.frame_b = ctk.CTkFrame(self.linha_superior, fg_color="#12324A", corner_radius=15)
        self.frame_b.pack(side="left", fill="both", expand=True, padx=(10, 0))

        self.montar_frame_b()

        # LINHA DE BAIXO
        self.linha_inferior = ctk.CTkFrame(self.container, fg_color="transparent")
        self.linha_inferior.pack(fill="both", expand=True, pady=(10, 0))

        # FRAME GRANDE DE BAIXO (C + D juntos)
        self.frame_cd = ctk.CTkFrame(self.linha_inferior, fg_color="#12324A", corner_radius=15)
        self.frame_cd.pack(fill="both", expand=True)

        self.criar_grafico_frame_cd()

    # FUNÇÕES
    def voltar_principal(self):
        self.master.mostrar_principal(self.email_usuario)


    def abrir_popup_fornecedor(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Fornecedores")
        popup.geometry("300x400")

        titulo = ctk.CTkLabel(
            popup, text="Fornecedores Cadastrados", 
            font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        titulo.pack(pady=(20, 10))

        popup.grab_set()

        fornecedores = listar_fornecedores()

        for nome in fornecedores:
            linha = ctk.CTkFrame(popup, fg_color="#12324A")
            linha.pack(fill="x", pady=5, padx=10)

            label = ctk.CTkLabel(linha, text=nome, text_color="white")
            label.pack(side="left", padx=10)

            btn_excluir = ctk.CTkButton(
                linha,
                text="Excluir", width=70, fg_color="red",
                command=lambda n=nome: self.excluir_fornecedor(n, popup))
            btn_excluir.pack(side="right", padx=10)

    def excluir_fornecedor(self, nome, popup):

        confirmar = msg.askyesno(
            "Confirmação",
            f"Deseja realmente excluir o fornecedor '{nome}'?")

        if not confirmar:
            return

        deletar_fornecedor(nome)

        popup.destroy()
        self.abrir_popup_fornecedor()


    def excluir_usuario(self, email, popup):

        confirmar = msg.askyesno(
            "Confirmação",
            f"Deseja excluir o usuário '{email}'?")

        if not confirmar:
            return

        deletar_usuario(email)

        popup.destroy()
        self.abrir_popup_funcionarios()


    def abrir_popup_funcionarios(self):

        popup = ctk.CTkToplevel(self)
        popup.title("Funcionários")
        popup.geometry("300x400")

        titulo = ctk.CTkLabel(
            popup, text="Usuários Cadastrados", 
            font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        titulo.pack(pady=(20, 10))

        popup.grab_set()

        usuarios = listar_usuarios()

        for email in usuarios:
            linha = ctk.CTkFrame(popup, fg_color="#12324A")
            linha.pack(fill="x", pady=5, padx=10)

            label = ctk.CTkLabel(
                linha, text=email, text_color="white")
            label.pack(side="left", padx=10)

            btn_excluir = ctk.CTkButton(
                linha,
                text="Excluir", width=70, fg_color="red",
                command=lambda e=email: self.excluir_usuario(e, popup))
            btn_excluir.pack(side="right", padx=10)


    def abrir_popup_cadastro_funcionario(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Cadastrar Funcionário")
        popup.geometry("350x400")
        popup.configure(fg_color="#0F293D")

        titulo = ctk.CTkLabel(
            popup, text="Preencha os campos:", 
            font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        titulo.pack(pady=(20, 10))

        popup.grab_set()

        # ENTRIES
        entry_nome = ctk.CTkEntry(popup, placeholder_text="Nome completo")
        entry_nome.pack(pady=10, padx=20)

        entry_email = ctk.CTkEntry(popup, placeholder_text="Email")
        entry_email.pack(pady=10, padx=20)

        entry_senha = ctk.CTkEntry(popup, placeholder_text="Senha", show="*")
        entry_senha.pack(pady=10, padx=20)

        entry_tipo = ctk.CTkEntry(popup, placeholder_text="(funcionario/gerente)")
        entry_tipo.pack(pady=10, padx=20)

        # BOTÃO SALVAR
        btn_salvar = ctk.CTkButton(
            popup,
            text="Cadastrar",
            command=lambda: self.salvar_funcionario(
                entry_nome.get(),
                entry_email.get(),
                entry_senha.get(),
                entry_tipo.get(),
                popup))
        btn_salvar.pack(pady=20)

    def salvar_funcionario(self, nome, email, senha, tipo, popup):

        if not nome or not email or not senha or not tipo:
            msg.showwarning("Erro", "Preencha todos os campos")
            return

        sucesso = cadastrar_usuario(email, senha, tipo, nome)

        if not sucesso:
            msg.showwarning("Erro", "Email já cadastrado")
            return

        msg.showinfo("Sucesso", "Funcionário cadastrado com sucesso")
        popup.destroy()


    def criar_grafico_frame_cd(self):

        # limpa widgets antigos
        for w in self.frame_cd.winfo_children():
            w.destroy()

        dados = relatorio_estoque_por_nicho()
        nichos = list(dados.keys())
        valores = list(dados.values())

        # guarda a figura no self
        self.fig, self.ax = plt.subplots(figsize=(6, 5))

        bars = self.ax.bar(nichos, valores)
        self.ax.set_ylim(0, 7)
        self.ax.set_title("Acompanhamento por Nicho", color="white", fontsize=25, pad=12)

        self.ax.set_xlabel(
            "Nichos", color="white", fontsize=18, labelpad=10)

        self.ax.set_ylabel(
            "Quantidade de Lentes", color="white", fontsize=15, labelpad=20)
        
        self.fig.subplots_adjust(bottom=0.25)

        self.fig.patch.set_facecolor("#12324A")
        self.ax.set_facecolor("#12324A")
        self.ax.tick_params(colors="white")

        for bar in bars:
            h = bar.get_height()
            if h >= 6:
                bar.set_color("#2ecc71")
            elif h >= 3:
                bar.set_color("#f1c40f")
            else:
                bar.set_color("#e74c3c")

        # guarda o canvas no self
        self.canvas_grafico = FigureCanvasTkAgg(self.fig, master=self.frame_cd)
        self.canvas_grafico.draw()
        self.canvas_grafico.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        

    
    def on_close(self):
    # destrói o canvas do Tk
        try:
            if hasattr(self, "canvas_grafico"):
                self.canvas_grafico.get_tk_widget().destroy()
        except:
            pass

        # fecha a figura do matplotlib (ESSENCIAL)
        try:
            import matplotlib.pyplot as plt
            if hasattr(self, "fig"):
                plt.close(self.fig)
        except:
            pass

    def montar_frame_b(self):

        # limpar antes (evita duplicar)
        for widget in self.frame_b.winfo_children():
            widget.destroy()

        estoque = relatorio_estoque_por_nicho()

        titulo_status = ctk.CTkLabel(
            self.frame_b,
            text="Status dos Nichos", font=ctk.CTkFont(size=35, weight="bold"),
            text_color="white")
        titulo_status.pack(anchor="w", padx=45, pady=(15, 10))

        frame_nichos = ctk.CTkFrame(self.frame_b, fg_color="transparent")
        frame_nichos.pack(pady=10)

        for nicho, valor in estoque.items():

            if valor >= 6:
                cor = "#1F8A4D"
            elif valor >= 3:
                cor = "#B58B00"
            else:
                cor = "#B03A3A"

            texto = f"NICHO {nicho}\n\n{valor}/7"

            box = ctk.CTkLabel(
                frame_nichos, text=texto, width=110, height=90, corner_radius=10, fg_color=cor,
                text_color="white", font=ctk.CTkFont(size=16, weight="bold"))
            box.pack(side="left", padx=12, pady=5)


        titulo_hist = ctk.CTkLabel(
        self.frame_b,
        text="Última Retirada", font=ctk.CTkFont(size=18, weight="bold"),
        text_color="white")
        titulo_hist.pack(pady=(20, 10))


        tipo, dado = buscar_ultima_movimentacao()

        if not dado:
            texto = "Nenhuma movimentação registrada"
        else:
            itens = dado.get("itens", [])

            if itens:
                lente = itens[0].get("lente", "")
                qtd = itens[0].get("quantidade", "")
            else:
                lente = ""
                qtd = ""

            responsavel = dado.get("responsavel", "")
            data = dado.get("data_hora", "")
            icone = "📤"
            texto = f"{icone} Retirada - {lente} ({qtd})\n👤 {responsavel}\n🕒 {data}"
            
        frame_hist = ctk.CTkFrame(
            self.frame_b, fg_color="#1E4764", corner_radius=12)
        frame_hist.pack(pady=(5, 10), padx=20)
           
        label_hist = ctk.CTkLabel(
        frame_hist, text=texto, text_color="white", justify="left",
        font=ctk.CTkFont(size=16))
        label_hist.pack(padx=25, pady=20)

        frame_hist.configure(width=420, height=120)
        frame_hist.pack_propagate(False)