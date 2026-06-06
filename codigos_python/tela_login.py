import customtkinter as ctk
from PIL import Image
from database import validar_login


class TelaLogin(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.configure(fg_color="#0F293D") # azul do fundo

        master.title("BotStock - Login")
        master.geometry("900x700")
         

        # TÍTULO
        self.lbl_titulo = ctk.CTkLabel(
            self, text="BotStock", font=ctk.CTkFont(size=100, weight="bold"), text_color= "white")
        self.lbl_titulo.pack(pady=(100, 40))


        # CARD LOGIN
        self.frm_login = ctk.CTkFrame(
            self, width=320, height=180, corner_radius=20, fg_color="#000000")
        self.frm_login.pack(pady=(20,50))
        self.frm_login.pack_propagate(False) 


        # CAMPO DE EMAIL
        self.txb_email = ctk.CTkEntry(
            self.frm_login, placeholder_text="Email", width=260, height=40,
            corner_radius=10, font=ctk.CTkFont(size=14))
        self.txb_email.pack(pady=(30, 15))
        self.txb_email.bind("<Return>", self.fazer_login)


        # FRAME SENHA E ÍCONE
        self.frm_senha = ctk.CTkFrame(self.frm_login, fg_color="transparent")
        self.frm_senha.pack(pady=10)


        # ÍCONES
        self.icon_eye_open = ctk.CTkImage(
            light_image=Image.open("eye_open.png"), size=(24, 24))
        self.icon_eye_close = ctk.CTkImage(
            light_image=Image.open("eye_close.png"), size=(24, 24))


        # CAMPO DE SENHA
        self.txb_senha = ctk.CTkEntry(
            self.frm_senha, placeholder_text="Senha", show="*", width=220,
            height=40, corner_radius=10, font=ctk.CTkFont(size=14))
        self.txb_senha.pack(side="left", padx=(0, 5))
        self.txb_senha.bind("<Return>", self.fazer_login)


        # BOTÃO COM ÍCONES
        self.btn_mostrar = ctk.CTkButton(
            self.frm_senha, image=self.icon_eye_close, text="", width=42,
            height=42, command=self.mostra_senha)
        self.btn_mostrar.pack(side="left")


        # BOTÃO LOGIN
        self.btn_login = ctk.CTkButton(
            self, text="Login", width=320, height=45, corner_radius=20,
            fg_color="#000000", font=ctk.CTkFont(size=20, weight="bold"), text_color="#7A797C",
            command=self.fazer_login)
        self.btn_login.pack(pady=(10, 0))


        # LABEL DE ERRO
        self.lbl_status = ctk.CTkLabel(
            self, text="", text_color="red", font=ctk.CTkFont(size=14))
        self.lbl_status.pack(pady=0)


        # LABEL ESQUECI SENHA
        self.lbl_senha = ctk.CTkLabel(
            self, text="Caso esqueça a SENHA, entre em contato com o TI", text_color="#7C8FE2")
        self.lbl_senha.pack(pady=0)


        # LIMPA OS ENTRYS
        self.txb_email.delete(0, "end")
        self.txb_senha.delete(0, "end")
        self.lbl_status.configure(text="")


    # FUNÇÕES
    def fazer_login(self, event=None):

        email = self.txb_email.get().lower()
        senha = self.txb_senha.get()
        if not email or not senha:
            self.lbl_status.configure(text="Preencha os campos corretamente!")
            return

        usuario = validar_login(email, senha)

        if usuario:
            self.master.mostrar_principal(email)
        else:
            self.lbl_status.configure(text="Email ou senha inválidos")


    def mostra_senha(self):
        if self.txb_senha.cget("show") == "":
            self.txb_senha.configure(show="*")
            self.btn_mostrar.configure(image=self.icon_eye_close)
        else:
            self.txb_senha.configure(show="")
            self.btn_mostrar.configure(image=self.icon_eye_open)