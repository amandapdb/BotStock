import customtkinter as ctk
from database import buscar_nome_por_email
from datetime import datetime
from tkinter import messagebox
from database import cadastrar_produto, cadastrar_fornecedor, listar_fornecedores



class TelaCadastroProduto(ctk.CTkFrame):
    def __init__(self, master, email_usuario):
        super().__init__(master)
        self.email_usuario = email_usuario

        self.pack(fill="both", expand=True)
        self.configure(fg_color="#0F293D")
        master.title("BotStock - Cadastro de Produtos")


        # TÍTULO
        self.titulo = ctk.CTkLabel(
            self, text="Cadastro de Novos Produtos", font=ctk.CTkFont(size=35, weight="bold"),
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


       # CARACTERÍSTICAS
        self.lbl_carac = ctk.CTkLabel(
            self.container,
            text="Características da lente:", font=ctk.CTkFont(size=25, weight="bold"),
            text_color="white")
        self.lbl_carac.pack(anchor="w", padx=10, pady=(15, 5))

        self.frame_linha = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_linha.pack(fill="x", pady=10)

        self.frame_carac = ctk.CTkFrame(self.frame_linha, fg_color="transparent")
        self.frame_carac.pack(side="left", padx=(20, 0))


        # POWER
        self.entry_pwr = ctk.CTkEntry(self.frame_carac, width=120, height=40, placeholder_text="PWR")
        self.entry_pwr.pack(side="left", padx=20)
        self.entry_pwr.bind("<KeyRelease>", self.validar_input)

        # BASE CURVATURE
        self.entry_bc = ctk.CTkEntry(self.frame_carac, width=120, height=40, placeholder_text="BC")
        self.entry_bc.pack(side="left", padx=20)
        self.entry_bc.bind("<KeyRelease>", self.validar_input)

        # DIAMÊTRO
        self.entry_diam = ctk.CTkEntry(self.frame_carac, width=120, height=40, placeholder_text="∅")
        self.entry_diam.pack(side="left", padx=20)
        self.entry_diam.bind("<KeyRelease>", self.validar_input)



        # FRAME FORNECEDOR
        self.frame_fornecedor = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_fornecedor.pack(fill="x", padx=20, pady=20)

        # LABEL FORNECEDOR
        self.frame_esquerda = ctk.CTkFrame(self.frame_fornecedor, fg_color="transparent")
        self.frame_esquerda.pack(side="left", pady=(15, 15))

        self.lbl_fornecedor = ctk.CTkLabel(
            self.frame_esquerda,
            text="Fornecedor:", font=ctk.CTkFont(size=25, weight="bold"),
            text_color="white")
        self.lbl_fornecedor.pack()

        # COMBOBOX FORNECEDOR
        self.frame_direita = ctk.CTkFrame(self.frame_fornecedor, fg_color="transparent")
        self.frame_direita.pack(side="left", padx=(10, 0), pady=(15, 15))

        valores = sorted(listar_fornecedores())

        self.combo_fornecedor = ctk.CTkComboBox(
            self.frame_direita, values=valores,
            width=200, height=40)
        self.combo_fornecedor.pack(side="left")
        self.combo_fornecedor.set("Selecione")


        #BOTÃO ADICIONAR FORNECEDOR
        self.btn_add_fornecedor = ctk.CTkButton(
            self.frame_direita, text="+", width=40, height=40, command=self.abrir_popup_fornecedor)
        self.btn_add_fornecedor.pack(side="left", padx=(10, 0))


        # FRAME NICHO
        self.frame_nicho = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_nicho.pack(fill="x", padx=20, pady=10)


        # LABEL NICHO
        self.lbl_nicho = ctk.CTkLabel(
            self.frame_nicho, text="Nicho:", font=ctk.CTkFont(size=25, weight="bold"),
            text_color="white")
        self.lbl_nicho.pack(side="left")


        # COMBOBOX NICHO
        self.combo_nicho = ctk.CTkComboBox(
            self.frame_nicho, height=40, values=["1", "2", "3", "4", "5"],)
        self.combo_nicho.pack(side="left", padx=(10, 0))
        self.combo_nicho.set("Selecione")

        
        # LINHA SEPARADORA
        linha = ctk.CTkFrame(self.container, height=2, fg_color="#2A4A5E")
        linha.pack(fill="x", padx=60, pady=60)


        # LABEL CONFIRMAÇÃO
        self.lbl_confirm = ctk.CTkLabel(
            self.container, text="Cadastrar Lente?", font=ctk.CTkFont(size=25),
            text_color="white")
        self.lbl_confirm.pack(pady=(40, 20))


        # BOTÃO CANCELAR
        self.frame_botoes = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_botoes.pack()

        self.btn_cancelar = ctk.CTkButton(
            self.frame_botoes, text="Cancelar", width=140, height=45, 
            font=ctk.CTkFont(size=15), fg_color="black", cursor="hand2", command=self.cancelar_cadastro)
        self.btn_cancelar.pack(side="left", padx=10)


        # BOTÃO CADASTRAR
        self.btn_cadastrar = ctk.CTkButton(
            self.frame_botoes, text="Cadastrar", width=140, height=45,
            font=ctk.CTkFont(size=15), cursor="hand2", command=self.cadastrar_produto)
        self.btn_cadastrar.pack(side="left", padx=10)



    # FUNÇÕES   
    def voltar_principal(self):
        self.master.mostrar_principal(self.email_usuario)

    
    def validar_input(self, event):
        entry = event.widget
        valor = entry.get()

        permitido = "0123456789+-."

        novo_valor = "".join([c for c in valor if c in permitido])

        if valor != novo_valor:
            entry.delete(0, "end")
            entry.insert(0, novo_valor)


    def atualizar_data(self):
        self.lbl_data_valor.configure(
            text=datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.after(1000, self.atualizar_data)


    def cancelar_cadastro(self):
        resposta = messagebox.askyesno(
            "Atenção",
            "Tem certeza que deseja cancelar esse cadastro?")

        if resposta:
            self.entry_pwr.delete(0, "end")
            self.entry_bc.delete(0, "end")
            self.entry_diam.delete(0, "end")
            self.combo_fornecedor.set("Selecione")


    def cadastrar_produto(self):

        responsavel = buscar_nome_por_email(self.email_usuario)
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        pwr = self.entry_pwr.get()
        bc = self.entry_bc.get()
        diam = self.entry_diam.get()
        fornecedor = self.combo_fornecedor.get()
        nicho = self.combo_nicho.get()

        if nicho == "Selecione":
            messagebox.showerror("Erro", "Selecione um nicho!")
            return

        if not pwr or not bc or not diam:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        if fornecedor == "Selecione":
            messagebox.showerror("Erro", "Selecione um fornecedor!")
            return
        
        dados = {
            "pwr": pwr, 
            "bc": bc, 
            "diam": diam, 
            "nicho": nicho, 
            "fornecedor": fornecedor,
            "responsavel": responsavel, 
            "data": data_hora}
        cadastrar_produto(dados)

        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

        self.entry_pwr.delete(0, "end")
        self.entry_bc.delete(0, "end")
        self.entry_diam.delete(0, "end")
        self.combo_fornecedor.set("Selecione")
        self.combo_nicho.set("Selecione")
    


    def abrir_popup_fornecedor(self):
        self.popup = ctk.CTkToplevel(self)
        self.popup.title("Novo Fornecedor")
        self.popup.geometry("300x150")

        self.popup.lift()
        self.popup.attributes("-topmost", True)
        self.popup.after(100, lambda: self.popup.attributes("-topmost", False))

        self.entry_novo_fornecedor = ctk.CTkEntry(
            self.popup, placeholder_text="Nome do fornecedor")
        self.entry_novo_fornecedor.pack(pady=20, padx=20)

        btn_salvar = ctk.CTkButton(
            self.popup, text="Salvar", command=self.salvar_fornecedor)
        btn_salvar.pack(pady=10)

       
    def salvar_fornecedor(self):
        novo = self.entry_novo_fornecedor.get()
        if not novo:
            return

        ok = cadastrar_fornecedor(novo)
        if not ok:
            messagebox.showerror("Erro", "Fornecedor já existe")
            return

        valores = list(self.combo_fornecedor.cget("values"))
        valores.append(novo)
        valores = sorted(valores)

        self.combo_fornecedor.configure(values=valores)
        self.combo_fornecedor.set(novo)

        self.popup.destroy()
