import customtkinter as ctk
from database import buscar_nome_por_email, cadastrar_pedido, listar_lentes
from database import relatorio_estoque_por_nicho, buscar_nicho_por_lente
from tkinter import messagebox
from datetime import datetime
from movimentacao import executar_separacao
import threading
 
 
 
class TelaSeparacaoPedidos(ctk.CTkFrame):
    def __init__(self, master, email_usuario):
        super().__init__(master)
        self.email_usuario = email_usuario
        self.itens_pedido = []
 
        self.pack(fill="both", expand=True)
        self.configure(fg_color="#0F293D")
        master.title("BotStock - Separação de Pedidos")
 
        # TÍTULO
        self.titulo = ctk.CTkLabel(
            self, text="Separação de Pedidos", font=ctk.CTkFont(size=35, weight="bold"),
            text_color="white")
        self.titulo.pack(anchor="w", padx=65, pady=(15, 10))
 
 
        # FRAME PRINCIPAL DIVIDIDO EM DUAS PARTES (HORIZONTALMENTE)
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="x", padx=20, pady=10)
 
 
        # FRAME DA ESQUERDA (LENTE E QUANTIDADE)
        self.frame_esquerda = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_esquerda.pack(side="left", fill="both", expand=True, padx=10, pady=10)
 
 
        # BOTÃO VOLTAR
        btn_voltar = ctk.CTkButton(
            self, text="↩", font=ctk.CTkFont(size=25), width=50, height=50,
            command=self.voltar_principal, fg_color="transparent", hover_color="#0300cc",
            text_color="white", cursor="hand2")
        btn_voltar.place(x=10, y=10)
 
 
        lentes = listar_lentes()
 
 
        # LENTE
        self.lbl_lente = ctk.CTkLabel(
            self.frame_esquerda, text="Lente:", font=ctk.CTkFont(size=20),
            text_color="white")
        self.lbl_lente.pack(anchor="w", padx=10, pady=(10, 5))
 
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
            self.frame_esquerda, text="Quantidade:", font=ctk.CTkFont(size=20),
            text_color="white")
        self.lbl_quantidade.pack(anchor="w", padx=10, pady=(10,5))
 
 
        # COMBOBOX QUANTIDADE
        self.combo_quantidade = ctk.CTkComboBox(
            self.frame_esquerda, width=250, height=40, values=["1", "2", "3", "4", "5", "6", "7"])
        self.combo_quantidade.set("Selecione a Quantidade")
        self.combo_quantidade.pack(padx=10, pady=(5, 30))
 
 
         # BOTÃO ADICIONAR ITEM
        self.btn_adicionar_item = ctk.CTkButton(
            self.frame_esquerda, text="Adicionar Item", width=250, height=40, corner_radius=10,
            fg_color="#1D6A6C", font=ctk.CTkFont(size=16), text_color="white", command=self.adicionar_item)
        self.btn_adicionar_item.pack(pady=70)
 
       
 
        # FRAME DA DIREITA (ITENS ADICIONADOS)
        self.frame_direita = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_direita.pack(side="left", fill="both", expand=True, padx=10, pady=10)
 
 
        # LABEL PARA ITENS ADICIONADOS
        self.lbl_itens_adicionados = ctk.CTkLabel(
            self.frame_direita, text="Itens Adicionados ao Pedido:", font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white")
        self.lbl_itens_adicionados.pack(pady=10)
 
 
        # LISTA DE ITENS
        self.lista_itens = ctk.CTkTextbox(self.frame_direita, width=380, height=320, font=ctk.CTkFont(size=16))
        self.lista_itens.pack(pady=10)
 
 
        # FRAME BOTÕES
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.pack(pady=30)
 
 
       # BOTÃO CANCELAR
        self.btn_cancelar = ctk.CTkButton(
            self.frame_botoes, text="Cancelar", width=250, height=50,
            corner_radius=10, fg_color="black", font=ctk.CTkFont(size=18), text_color="white",
            command=self.cancelar_selecao)
        self.btn_cancelar.pack(side="left", padx=20)
 
 
        # BOTÃO INICIAR
        self.btn_iniciar_separacao = ctk.CTkButton(
            self.frame_botoes, text="Iniciar Separação", width=250, height=50,
            corner_radius=10, fg_color="green", font=ctk.CTkFont(size=18), text_color="white",
            command=self.iniciar_separacao)
        self.btn_iniciar_separacao.pack(side="left", padx=20)
 
 
    #FUNÇÕES
    def voltar_principal(self):
        self.master.mostrar_principal(self.email_usuario)
 
    def adicionar_item(self):
        lente = self.combo_lente.get()
        quantidade = self.combo_quantidade.get()
 
        if lente in ["", "Selecione a Lente", "Nenhuma lente cadastrada"]:
            messagebox.showerror("Erro", "Selecione uma lente!")
            return
 
        if quantidade in ["", "Selecione a Quantidade"]:
            messagebox.showerror("Erro", "Selecione a quantidade!")
            return
 
        item = {
            "lente": lente,
            "quantidade": quantidade}
       
 
        self.itens_pedido.append(item)
 
        self.lista_itens.insert("end", f"Lente: {lente} |\n Quantidade: {quantidade}\n")
 
        self.combo_lente.set("Selecione a Lente")
        self.combo_quantidade.set("Selecione a Quantidade")
 
 
    def cancelar_selecao(self):
        resposta = messagebox.askyesno(
            "Atenção", "Tem certeza que deseja cancelar a separação?")
 
        if resposta:
            self.itens_pedido.clear()
            self.lista_itens.delete("1.0", "end")
 
 
    def processo_separacao(self):
 
        self.btn_iniciar_separacao.configure(state="disabled")
 
        for item in self.itens_pedido:
 
            lente = item["lente"]
            quantidade = int(item["quantidade"])
 
            nicho = buscar_nicho_por_lente(lente)
 
            executar_separacao(nicho, quantidade)
 
        # limpa tela
        self.itens_pedido.clear()
        self.lista_itens.delete("1.0", "end")
        self.combo_lente.set("Selecione a Lente")
        self.combo_quantidade.set("Selecione a Quantidade")
 
        self.btn_iniciar_separacao.configure(state="normal")
 
 
 
 
    def iniciar_separacao(self):
        if not self.itens_pedido:
            messagebox.showerror("Erro", "Nenhum item adicionado!")
            return
 
        responsavel = buscar_nome_por_email(self.email_usuario)
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
 
        dados_pedido = {
            "responsavel": responsavel,
            "email_responsavel": self.email_usuario,
            "data_hora": data_hora,
            "itens": self.itens_pedido,
            "status": "Pendente"
        }
 
        estoque = relatorio_estoque_por_nicho()
 
        # VALIDAÇÃO PARA TODOS OS ITENS
        for item in self.itens_pedido:
 
            lente = item["lente"]
            quantidade = int(item["quantidade"])
 
            nicho = buscar_nicho_por_lente(lente)
 
            atual = estoque.get(nicho, 0)
 
            if quantidade > atual:
                messagebox.showwarning(
                    "Estoque insuficiente",
                    f"Só tem {atual} lentes disponíveis para {lente}"
                )
                return
 
        # SALVA PEDIDO
        cadastrar_pedido(dados_pedido)

        messagebox.showinfo(
            "Sucesso",
            "Pedido iniciado com sucesso!")
        threading.Thread(
            target=self.processo_separacao).start()