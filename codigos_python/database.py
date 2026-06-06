from pymongo import MongoClient

# COMUNICAÇÃO COM O MONGODB
client = MongoClient("mongodb://localhost:27017/")
db = client["BotStock"]
usuarios = db["usuarios"]


# DADOS PARA LOGIN
def validar_login(email, senha):
    usuario = usuarios.find_one({"email": email, "senha": senha})
    return usuario

# DADOS PARA NOME DO RESPONSÁVEL
def buscar_nome_por_email(email):
    usuario = usuarios.find_one({"email": email})
    if usuario:
        return usuario.get("nome_completo", "Usuário")
    return "Usuário"

# DADOS PARA VER QUEM ABRE OS REGISTROS
def buscar_tipo_usuario(email):
    usuario = usuarios.find_one({"email": email})
    if usuario:
        return usuario.get("tipo", "funcionario")
    return "funcionario"

#PUXANDO A LISTA DE USUÁRIOS
def listar_usuarios():
    lista = []
    for u in usuarios.find():
        lista.append(u["email"])
    return lista

#DELETANDO A LISTA DE USUÁRIOS
def deletar_usuario(email):
    usuarios.delete_one({"email": email})


#CADASTRO DE USUÁRIOS
def cadastrar_usuario(email, senha, tipo, nome_completo):
    if usuarios.find_one({"email": email}):
        return False

    usuarios.insert_one({
        "email": email,
        "senha": senha,
        "tipo": tipo,
        "nome_completo": nome_completo
    })

    return True

#DADOS DE FORNECEDORES
def cadastrar_fornecedor(nome):
    if db["fornecedores"].find_one({"nome": nome}):
        return False
    db["fornecedores"].insert_one({"nome": nome})
    return True

#LISTA DE FORNECEDORES
def listar_fornecedores():
    lista = []
    for f in db["fornecedores"].find():
        lista.append(f["nome"])
    return lista

#DELETANDO DA LISTA
def deletar_fornecedor(nome):
    db["fornecedores"].delete_one({"nome": nome})


#DADOS DE CADASTRO DE LENTES
def cadastrar_produto(dados):
    db["produtos"].insert_one(dados)


# DADOS UNIFICADOS 
def listar_lentes():
    produtos = db["produtos"].find()

    lista = []
    for produto in produtos:
        descricao = f'{produto["fornecedor"]} | PWR {produto["pwr"]} | BC {produto["bc"]} | Ø {produto["diam"]}'
        lista.append(descricao)

    return sorted(lista)

# DADOS SALVOS DOS PEDIDOS
def cadastrar_pedido(dados):
    db["pedidos"].insert_one(dados)

# DADOS SALVOS DOS ABASTECIMENTOS
def cadastrar_abastecimento(dados):
    db["abastecimentos"].insert_one(dados)

# DADOS PARA CRIAR DESCRIÇÃO DAS LENTES
def montar_descricao_lente(produto):
    return f'{produto["fornecedor"]} | PWR {produto["pwr"]} | BC {produto["bc"]} | Ø {produto["diam"]}'

# DADOS PARA O RELATÓRIO
def relatorio_estoque_por_nicho():
    produtos = list(db["produtos"].find())
    abastecimentos = list(db["abastecimentos"].find())
    pedidos = list(db["pedidos"].find())

    mapa_lente_nicho = {}

    for produto in produtos:
        descricao = montar_descricao_lente(produto)
        nicho = str(produto.get("nicho", ""))
        if nicho:
            mapa_lente_nicho[descricao] = nicho

    estoque_nichos = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0
    }

    # SOMA ABASTECIMENTOS
    for abastecimento in abastecimentos:
        lente = abastecimento.get("lente", "")
        quantidade = int(abastecimento.get("quantidade", 0))

        nicho = mapa_lente_nicho.get(lente)
        if nicho in estoque_nichos:
            estoque_nichos[nicho] += quantidade

    # SUBTRAI SAÍDAS
    for pedido in pedidos:
        itens = pedido.get("itens", [])

        for item in itens:
            lente = item.get("lente", "")
            quantidade = int(item.get("quantidade", 0))

            nicho = mapa_lente_nicho.get(lente)
            if nicho in estoque_nichos:
                estoque_nichos[nicho] -= quantidade

    # IMPEDE VALOR NEGATIVO
    for nicho in estoque_nichos:
        if estoque_nichos[nicho] < 0:
            estoque_nichos[nicho] = 0

    return estoque_nichos

# DADOS PARA BUSCAR NICHO PELA DESCRIÇÃO
def buscar_nicho_por_lente(lente):
    produtos = db["produtos"].find()

    for p in produtos:
        descricao = f'{p["fornecedor"]} | PWR {p["pwr"]} | BC {p["bc"]} | Ø {p["diam"]}'
        if descricao == lente:
            return str(p.get("nicho"))

    return None

# HISTÓRICO DE MOVIMENTAÇÃO
def buscar_ultima_movimentacao():

    # busca último pedido
    pedido = list(
        db["pedidos"]
        .find()
        .sort("data_hora", -1)
        .limit(1)
    )
    print(pedido)
    # se tiver pedido
    
    if pedido:
        return "Retirada", pedido[0]

    # se não tiver nada
    return None, None