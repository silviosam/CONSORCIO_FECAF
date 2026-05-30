# 🚗 Sistema de Gestão de Consórcios

Uma plataforma web desenvolvida para gerenciamento de clientes, veículos, grupos de consórcio e venda de cotas, proporcionando controle eficiente das operações e simulação de processos reais utilizados por administradoras de consórcio.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-Web-green)
![SQLite](https://img.shields.io/badge/SQLite-Banco%20de%20Dados-lightgrey)
![Status](https://img.shields.io/badge/Status-Concluído-success)

---

# 📋 Índice

* Visão Geral
* Objetivo do Projeto
* Funcionalidades
* Tecnologias Utilizadas
* Arquitetura do Sistema
* Estrutura do Projeto
* Instalação
* Como Utilizar
* Regras de Negócio
* Metodologia Ágil
* Banco de Dados
* Interface do Sistema
* Melhorias Futuras
* Equipe
* Conclusão

---

# 🎯 Visão Geral

O Sistema de Gestão de Consórcios foi desenvolvido como projeto acadêmico com o objetivo de simular o funcionamento de uma administradora de consórcios de veículos.

A aplicação permite realizar o gerenciamento completo de clientes, veículos, grupos de consórcio e cotas, utilizando uma interface web moderna e intuitiva.

O sistema centraliza todas as informações em uma única plataforma, reduzindo processos manuais e facilitando a consulta e manutenção dos dados.

---

# 💡 Objetivo do Projeto

Muitas empresas ainda realizam o controle de grupos de consórcio através de planilhas eletrônicas ou processos manuais.

A proposta deste projeto é fornecer uma solução digital capaz de:

* Organizar os cadastros de clientes;
* Controlar veículos disponíveis;
* Criar grupos de consórcio;
* Calcular taxas administrativas automaticamente;
* Gerenciar vendas de cotas;
* Armazenar informações em banco de dados;
* Facilitar consultas e manutenção dos registros.

---

# ✨ Funcionalidades

## 👤 Gestão de Clientes

* Cadastro de clientes
* Validação automática de CPF
* Validação de telefone
* Validação de e-mail
* Associação a grupos de consórcio
* Exclusão de clientes

---

## 🚗 Gestão de Veículos

* Cadastro de veículos
* Marca
* Modelo
* Ano
* Valor do veículo
* Exclusão de veículos

---

## 📋 Gestão de Grupos

* Criação de grupos de consórcio
* Definição da quantidade de cotas
* Definição do prazo de pagamento
* Cálculo automático da taxa administrativa
* Cálculo automático do valor do crédito
* Exclusão de grupos

---

## 💰 Gestão de Cotas

* Venda de cotas
* Associação entre cliente e grupo
* Geração automática de parcelas
* Controle do número da cota
* Exclusão de cotas

---

## 📊 Dashboard

O sistema apresenta indicadores em tempo real:

* Total de Clientes
* Total de Veículos
* Total de Grupos
* Total de Cotas Vendidas

---

# 🛠 Tecnologias Utilizadas

## Backend

| Tecnologia  | Função              |
| ----------- | ------------------- |
| Python 3.13 | Linguagem principal |
| Flask       | Framework Web       |
| SQLite3     | Banco de Dados      |
| Jinja2      | Engine de Templates |

---

## Frontend

| Tecnologia | Função                |
| ---------- | --------------------- |
| HTML5      | Estrutura             |
| CSS3       | Estilização           |
| JavaScript | Máscaras e interações |

---

## Gerenciamento

| Ferramenta | Utilização              |
| ---------- | ----------------------- |
| Trello     | Organização das tarefas |
| Kanban     | Metodologia Ágil        |
| Git        | Controle de versão      |
| GitHub     | Hospedagem do projeto   |

---

# 🏗 Arquitetura do Sistema

O projeto foi desenvolvido seguindo conceitos de Programação Orientada a Objetos (POO).

Estrutura lógica:

Cliente
↓
Grupo
↓
Cota
↓
Parcelas

Além disso, a aplicação utiliza a arquitetura baseada em:

* Model (Sistema)
* View (Templates HTML)
* Controller (Rotas Flask)

---

# 📁 Estrutura do Projeto

consorcio/

│

├── app.py

├── sistema.py

├── banco.db

│

├── templates/

│ ├── menu_principal.html

│ ├── clientes.html

│ ├── veiculos.html

│ ├── grupos.html

│ └── cotas.html

│

├── static/

│ └── style.css

│

└── README.md

---

# 💾 Banco de Dados

O projeto utiliza SQLite3 para persistência dos dados.

Tabelas principais:

* clientes
* veiculos
* grupos
* cotas

Benefícios:

* Leve
* Gratuito
* Não necessita servidor
* Fácil manutenção

---

# ⚙️ Instalação

## 1. Clonar o Projeto

```bash
git clone https://github.com/seu-usuario/consorcio.git
```

## 2. Entrar na Pasta

```bash
cd consorcio
```

## 3. Instalar Dependências

```bash
pip install flask
```

## 4. Executar Sistema

```bash
python app.py
```

---

# 🚀 Como Utilizar

## Cadastro de Cliente

1. Acesse Clientes
2. Preencha os dados
3. Escolha um grupo
4. Clique em Cadastrar

---

## Cadastro de Veículo

1. Acesse Veículos
2. Informe os dados
3. Clique em Cadastrar

---

## Criação de Grupo

1. Escolha um veículo
2. Defina quantidade de cotas
3. Defina quantidade de parcelas
4. Clique em Criar Grupo

---

## Venda de Cota

1. Escolha um cliente
2. Escolha um grupo
3. Clique em Vender Cota

---

# 📈 Regras de Negócio

A taxa administrativa é calculada automaticamente conforme o prazo.

| Parcelas     | Taxa |
| ------------ | ---- |
| Até 36       | 10%  |
| Até 60       | 15%  |
| Até 80       | 18%  |
| Até 100      | 22%  |
| Acima de 100 | 25%  |

---

# 📌 Metodologia Ágil

Durante o desenvolvimento foi utilizado:

### Trello

Para:

* Organização das tarefas
* Controle das entregas
* Distribuição das atividades
* Acompanhamento do progresso

### Kanban

Fluxo:

Backlog
↓
A Fazer
↓
Em Desenvolvimento
↓
Em Testes
↓
Concluído

---

# 🎨 Interface

O sistema possui:

* Tema Dark
* Layout Responsivo
* Cards Informativos
* Tabelas Organizadas
* Navegação Simplificada
* Mensagens de Feedback

---

# 🔮 Melhorias Futuras

* Login e autenticação
* Controle financeiro
* Relatórios em PDF
* Dashboard avançado
* Histórico de pagamentos
* Sistema de contemplação
* Integração com APIs
* Controle de usuários

---

# 👨‍💻 Equipe

Projeto desenvolvido para a disciplina de Desenvolvimento Ágil.

Ferramentas utilizadas para organização:

* Trello
* Kanban
* GitHub

---

# 🎓 Conclusão

O Sistema de Gestão de Consórcios permitiu aplicar na prática conceitos fundamentais de desenvolvimento de software, incluindo Programação Orientada a Objetos, desenvolvimento web com Flask, banco de dados SQLite3 e metodologias ágeis.

O resultado é uma aplicação funcional capaz de simular operações reais de uma administradora de consórcios, oferecendo uma solução organizada, intuitiva e escalável para gerenciamento de clientes, veículos, grupos e cotas.
