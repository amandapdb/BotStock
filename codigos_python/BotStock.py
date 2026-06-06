import customtkinter as ctk
from tela_login import TelaLogin
from tela_principal import TelaPrincipal
from tela_cadastro import TelaCadastroProduto
from tela_abastec_merc import TelaAbastecimentoMercadorias
from tela_separacao import TelaSeparacaoPedidos
from tela_relatorios import TelaRelatorios
from movimentacao import conectar

# CONFIGURAÇÃO DE CORES PADRÃO
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.state("zoomed")
        conectar()

        self.tela = None
        self.mostrar_login()

    def limpar_tela(self):
        if self.tela:
            # chama o "destruidor" se existir
            if hasattr(self.tela, "on_close"):
                self.tela.on_close()

            self.tela.destroy()

    def mostrar_login(self):
        self.limpar_tela()
        self.tela = TelaLogin(self)

    def mostrar_principal(self, email):
        self.limpar_tela()
        self.tela = TelaPrincipal(self, email)

    def mostrar_cadastro(self, email):
        self.limpar_tela()
        self.tela = TelaCadastroProduto(self, email)

    def mostrar_entrada(self, email):
        self.limpar_tela()
        self.tela = TelaAbastecimentoMercadorias(self, email)

    def mostrar_pedidos(self, email):
        self.limpar_tela()
        self.tela = TelaSeparacaoPedidos(self, email)

    def mostrar_relatorios(self, email):
        self.limpar_tela()
        self.tela = TelaRelatorios(self, email)



# EXECUÇÃO
if __name__ == "__main__":
    app = App()
    app.mainloop()