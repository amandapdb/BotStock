# BotStock

## Sistema de automação de estoque com robô cartesiano para montagem de pedidos de lentes de contato para o setor varejista

Projeto de Trabalho de Conclusão de Curso (TCC) desenvolvido no curso de Engenharia de Controle e Automação da Faculdade Engenheiro Salvador Arena (FESA), com o objetivo de automatizar o processo de armazenamento, controle de estoque e separação de pedidos de lentes de contato por meio de um robô cartesiano integrado a uma interface gráfica e banco de dados.

---

## Objetivo
Desenvolver um sistema automatizado de estoque, integrado a uma interface gráfica (GUI) executável com controle de dados e um ASRS (Sistema Automatizado de Armazenamento e Recuperação) para automatizar o processo de separação de pedidos, aumentando a eficiência operacional e reduzindo falhas no processo.

## Tecnologias Utilizadas

### Software
- Python
- CustomTkinter
- MongoDB
- Matplotlib
- FigureCanvasTkAgg

### Hardware
- Arduino Uno
- Arduino Nano
- CNC Shield V3
- Drivers DVR8825
- Motores de passo NEMA 17
- Servo motor para garra
- LEDs indicadores de nicho
- Fonte 12V
- Fonte 5V
- Correias GT2
- Atuadores

### Controle
- GRBL
- Comunicação Serial USB

---

## Funcionalidades

- Cadastro de novos produtos
- Cadastro de fornecedores
- Controle de usuários
- Abastecimento de mercadorias
- Controle de estoque por nicho
- Separação automatizada de pedidos
- Registro de movimentações
- Relatórios operacionais
- Monitoramento do estoque em tempo real

---

## Estrutura do Repositório

```text
BotStock/
│
├── BotStock_VSCode/
│   └── Código-fonte Python
│
├── BotStock_MongoDB/
│   └── Estrutura e coleções do banco de dados
│
├── BotStock_Arduino/
│   └── Código do Arduino para controle da garra e LEDs
│
├── BotStock_GRBL/
│   └── Configuração dos parâmetros do controlador GRBL
│
├── TCC_Escrito/
│   └── Documento final do TCC
│
├── TCC_ApresentacaoBanca/
│   └── Slides utilizados na apresentação
│
├── README.md
└── .gitignore
```

---

## Arquitetura do Sistema

O sistema é composto por três camadas principais:

1. Interface gráfica desenvolvida em Python;
2. Banco de dados MongoDB para armazenamento das informações;
3. Robô cartesiano controlado por Arduino Uno, CNC Shield e GRBL.

A comunicação entre software e hardware ocorre por meio de comunicação serial.

---

## Fluxo de Funcionamento

1. Cadastro dos novos produtos no sistema;
2. Abastecimento dos nichos do estoque;
3. Registro das informações no MongoDB;
4. Criação dos pedidos;
5. Verificação automática de disponibilidade;
6. Movimentação do robô até o nicho correspondente;
7. Retirada do produto;
8. Entrega na área de coleta;
9. Atualização automática do estoque e dos relatórios.

---

## Banco de Dados

O banco de dados utiliza MongoDB e é composto pelas seguintes coleções:

- usuarios
- fornecedores
- produtos
- pedidos
- abastecimentos

---

## Resultados Esperados

- Redução de erros na separação de pedidos;
- Maior confiabilidade operacional;
- Melhor rastreabilidade das movimentações;
- Redução do tempo de processamento dos pedidos;
- Automatização das operações de estoque;
- Acompanhamento dos resultados de forma visual.

---

## Equipe

- Amanda Perini
- Arthur Delgado
- Beatriz Ashiley
- Henrique Lopes

---

## Instituição

Faculdade Engenheiro Salvador Arena (FESA)
Curso: Engenharia de Controle e Automação
Ano: 2026

---

## Licença

Projeto acadêmico desenvolvido exclusivamente para fins educacionais e de pesquisa.
