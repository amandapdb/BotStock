import customtkinter as ctk
import tkinter.messagebox as msg
from database import buscar_tipo_usuario


class TelaPrincipal(ctk.CTkFrame):
    def __init__(self, master, email):
        super().__init__(master)
        self.email = email
        self.tipo_usuario = buscar_tipo_usuario(self.email)

        self.pack(fill="both", expand=True)
        self.configure(fg_color="#0F293D")
        master.title("BotStock - Home")


        # TÍTULO
        self.titulo = ctk.CTkLabel(
            self, text="BotStock", font=ctk.CTkFont(size=100, weight="bold"), text_color= "white")
        self.titulo.pack(pady=(30, 20))


        # BOTÃO LOGOUT
        btn_voltar = ctk.CTkButton(
            self, text="Logout", font=ctk.CTkFont(size=20), width=50, height=50, command=self.voltar_login,
            fg_color="transparent", hover_color="#cc0000", text_color="white", cursor="hand2")
        btn_voltar.place(relx=1.0, x=-10, y=10, anchor="ne")


        # GRID DOS BOTÕES
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.grid_frame.columnconfigure((0,1), weight=1)
        self.grid_frame.rowconfigure((0,1), weight=1)


        # BOTÕES
        btn1 = ctk.CTkButton(
        self.grid_frame, text="Cadastro de \nNovos Produtos", font=ctk.CTkFont(size=40, weight="bold"),
        text_color="black", cursor="hand2",
        command=lambda: self.master.mostrar_cadastro(self.email))

        btn2 = ctk.CTkButton(
        self.grid_frame, text="Abastecimento\n de Mercadoria", font=ctk.CTkFont(size=40, weight="bold"),
        text_color="black", cursor="hand2",
        command=lambda: self.master.mostrar_entrada(self.email))

        btn3 = ctk.CTkButton(
        self.grid_frame, text="Separação \nde Pedidos", font=ctk.CTkFont(size=40, weight="bold"),
        text_color="black", cursor="hand2",
        command=lambda:self.master.mostrar_pedidos(self.email))

        btn4 = ctk.CTkButton(
        self.grid_frame, text="Relatórios", font=ctk.CTkFont(size=40, weight="bold"),
        text_color="black", cursor="hand2",
        command=self.verificar_acesso_relatorios)

        btn1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        btn2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        btn3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        btn4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")


    # FUNÇÕES
    def voltar_login(self):
        self.master.mostrar_login()


    # ACESSO PARA GERENTES AO BOTÃO 
    def verificar_acesso_relatorios(self):

        tipo = buscar_tipo_usuario(self.email)

        if tipo != "gerente":
            msg.showwarning("Acesso negado", "Acesso restrito a gerentes")
            return

        self.master.mostrar_relatorios(self.email)