import customtkinter as ctk
from database import cadastrar_abastecimento, buscar_nome_por_email, relatorio_estoque_por_nicho
from datetime import datetime
from tkinter import messagebox
import tkinter as tk
from database import listar_lentes, db, buscar_nicho_por_lente
from tkcalendar import Calendar
import movimentacao


def piscar_nicho(numero):
    print("ENTROU NA FUNÇÃO")

    try:
        if movimentacao.garra is not None:
            movimentacao.garra.write(f"B{numero}\n".encode())
            print(f"Piscando Nicho {numero}")

    except Exception as e:
        print("Erro ao acionar LED:", e)


class TelaAbastecimentoMercadorias(ctk.CTkFrame):
    def __init__(self, master, email_usuario):
        super().__init__(master)
        self.email_usuario = email_usuario

        self.pack(fill="both", expand=True)
        self.configure(fg_color="#0F293D")
        master.title("BotStock - Abastecimento de Mercadoria")


        # TÍTULO
        self.titulo = ctk.CTkLabel(
            self, text="Abastecimento de Mercadoria", font=ctk.CTkFont(size=35, weight="bold"),
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
        self.container.pack(fill="x", expand=True, padx=20, pady=10)


        # FRAME DA ESQUERDA (LENTE E QUANTIDADE)
        self.frame_esquerda = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_esquerda.pack(side="left", fill="both", expand=True, padx=10, pady=10)


       # LABEL PERGUNTA
        self.lbl_pergunta = ctk.CTkLabel(
            self.frame_esquerda,
            text="Lente a ser abastecida:", font=ctk.CTkFont(size=25, weight="bold"),
            text_color="white")
        self.lbl_pergunta.pack(anchor="w", padx=10, pady=(15, 5))

        lentes = listar_lentes()


        # COMBOBOX LENTE
        self.combo_lente = ctk.CTkComboBox(
            self.frame_esquerda, width=250, height=40, values=lentes)
        if lentes:
            self.combo_lente.set("Selecione a Lente")
        else:
            self.combo_lente.configure(values=["Nenhuma lente cadastrada"])
            self.combo_lente.set("Nenhuma lente cadastrada")  
        self.combo_lente.pack(padx=10, pady=(5, 15))


        # LABEL QUANTIDADE
        self.lbl_quantidade = ctk.CTkLabel(
            self.frame_esquerda, text="Quantidade:", font=ctk.CTkFont(size=25, weight="bold"),
            text_color="white")
        self.lbl_quantidade.pack(anchor="w", padx=10, pady=(10,5))


        #COMBOBOX QUANTIDADE
        self.combo_quantidade = ctk.CTkComboBox(
            self.frame_esquerda, width=250, height=40, values=["1", "2", "3", "4", "5", "6", "7"])
        self.combo_quantidade.set("Selecione a Quantidade") 
        self.combo_quantidade.pack(padx=10, pady=(5, 30))


        # LABEL VALIDADE
        self.lbl_validade = ctk.CTkLabel(
            self.frame_esquerda, text="Data de Validade:", font=ctk.CTkFont(size=25, weight="bold"),
            text_color="white")
        self.lbl_validade.pack(anchor="w", padx=10, pady=(10,5))


        # BOTÃO DATA
        self.btn_data = ctk.CTkButton(
            self.frame_esquerda, text="Selecionar Data", width=250, height=50,
            corner_radius=10, font=ctk.CTkFont(size=18), text_color="white",command=self.abrir_calendario)
        self.btn_data.pack(padx=10, pady=(5, 15))


        # LABEL DATA ESCOLHIDA
        self.lbl_data_escolhida = ctk.CTkLabel(
            self.frame_esquerda, text="Nenhuma data selecionada",  font=ctk.CTkFont(size=20),
            text_color="white")
        self.lbl_data_escolhida.pack()


        # FRAME BOTÕES
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.pack(pady=30)


       # BOTÃO CANCELAR
        self.btn_cancelar = ctk.CTkButton(
            self.frame_botoes, text="Cancelar", width=250, height=50,
            corner_radius=10, fg_color="black", font=ctk.CTkFont(size=18), text_color="white",
            command=self.cancelar_abastecimento)
        self.btn_cancelar.pack(side="left", padx=20)


        # BOTÃO INICIAR
        self.btn_iniciar_abastecimento = ctk.CTkButton(
            self.frame_botoes, text="Iniciar Abastecimento", width=250, height=50,
            corner_radius=10, fg_color="green", font=ctk.CTkFont(size=18), text_color="white",
            command=self.iniciar_abastecimento)
        self.btn_iniciar_abastecimento.pack(side="left", padx=20)


    #FUNÇÕES
    def voltar_principal(self):
        self.master.mostrar_principal(self.email_usuario)


    def abrir_calendario(self):
        # se já tiver um aberto, não abre outro
        if hasattr(self, "top") and self.top.winfo_exists():
            return

        self.top = tk.Toplevel(self)
        self.top.title("Selecionar Data")
        self.top.geometry("300x300")

        # faz o popup ficar ligado à tela principal
        self.top.transient(self)
        self.top.grab_set()

        # se fechar no X, destruir corretamente
        self.top.protocol("WM_DELETE_WINDOW", self.fechar_calendario)

        self.cal = Calendar(self.top, selectmode="day", date_pattern="dd/mm/yyyy")
        self.cal.pack(pady=20)

        btn_confirmar = ctk.CTkButton(
            self.top, text="Confirmar", command=self.pegar_data)
        btn_confirmar.pack(pady=10)


    def fechar_calendario(self):
        try:
            if hasattr(self, "top") and self.top.winfo_exists():
                self.top.destroy()
        except:
            pass

    def pegar_data(self):
        data = self.cal.get_date()
        self.lbl_data_escolhida.configure(text=data)
        self.top.destroy()
    
    def cancelar_abastecimento(self):
        resposta = messagebox.askyesno(
            "Atenção", "Tem certeza que deseja cancelar o abastecimento?")

        if resposta:
            self.combo_lente.set("Selecione a Lente")
            self.combo_quantidade.set("Selecione a Quantidade")
            self.lbl_data_escolhida.configure(text="Nenhuma data selecionada")

    def iniciar_abastecimento(self):
        lente = self.combo_lente.get()
        quantidade = self.combo_quantidade.get()
        validade = self.lbl_data_escolhida.cget("text")
    

        if lente in ["", "Selecione a Lente", "Nenhuma lente cadastrada"]:
            messagebox.showerror("Erro", "Selecione uma lente!")
            return

        if quantidade in ["", "Selecione a Quantidade"]:
            messagebox.showerror("Erro", "Selecione a quantidade!")
            return

        if validade == "Nenhuma data selecionada":
            messagebox.showerror("Erro", "Selecione a data de validade!")
            return

        responsavel = buscar_nome_por_email(self.email_usuario)
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        dados_abastecimento = {
            "lente": lente,
            "quantidade": quantidade,
            "validade": validade,
            "responsavel": responsavel,
            "email_responsavel": self.email_usuario,
            "data_hora_abastecimento": data_hora,
            "status": "Abastecido"}

        estoque = relatorio_estoque_por_nicho()
        quantidade = int(self.combo_quantidade.get())

        # descobrir o nicho da lente automaticamente
        produtos = list(db["produtos"].find())

        nicho = buscar_nicho_por_lente(lente)

        for p in produtos:
            descricao = f'{p["fornecedor"]} | PWR {p["pwr"]} | BC {p["bc"]} | Ø {p["diam"]}'
            if descricao == lente:
                nicho = str(p.get("nicho"))
                break

        if not nicho:
            messagebox.showerror("Erro", "Nicho não encontrado para essa lente!")
            return

        atual = estoque.get(nicho, 0)
        capacidade = 7 - atual

        if quantidade > capacidade:
            messagebox.showwarning(
                "Limite excedido",
                f"Esse nicho suporta mais {capacidade} lentes")
            return
        
        cadastrar_abastecimento(dados_abastecimento)

        print("ANTES DE PISCAR:", nicho)
       # Pisca o LED do nicho
        piscar_nicho(nicho)

        messagebox.showinfo("Sucesso", "Abastecimento salvo com sucesso!")

        self.combo_lente.set("Selecione a Lente")
        self.combo_quantidade.set("Selecione a Quantidade")
        self.lbl_data_escolhida.configure(text="Nenhuma data selecionada")