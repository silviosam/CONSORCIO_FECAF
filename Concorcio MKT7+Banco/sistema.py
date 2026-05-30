# sistema.py

# ... (validadores)
#class SistemaConsorcio:
#ef __init__(self):
# Estabelece conexão com o banco SQLite. O parâmetro check_same_thread=False 
# é necessário para que o Flask (multithread) possa acessar o banco com segurança.
#self.conn = sqlite3.connect("consorcio.db", check_same_thread=False)
#self.cursor = self.conn.cursor()
#self.criar_tabelas()

#def criar_tabelas(self):
"""Cria a estrutura do banco de dados caso o arquivo .db seja novo."""
# Tabelas normalizadas: clientes, veículos, grupos e cotas (vendas realizadas)
# ... (código das tabelas)

#def criar_grupo(self, nome, veiculo_id, quantidade_cotas, prazo_meses):
"""
Calcula o valor do crédito com base na taxa administrativa progressiva:
- Até 36 meses: 10% | Até 60 meses: 15% | Até 80 meses: 18%
- Até 100 meses: 22% | Acima de 100 meses: 25%
"""
# ... (lógica de busca do veículo e cálculo da taxa)

##def vender_cota(self, cliente_id, grupo_id):
"""
Vincula um cliente a um grupo de consórcio. 
O número da cota é gerado automaticamente usando o ID da transação.
"""
# ... (lógica de inserção e update do número da cota)

#def estatisticas_sistema(self):
"""Retorna o total de registros de cada tabela para exibição no Dashboard."""
# ... (queries de COUNT)



import sqlite3
import re

#Validadores
#validação do Email baseado no formato descrito (algo@algo.algo)
def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email)
#validação do Telefone baseado no padrão de escrita dele ((11) 98765-4321)
def validar_telefone(telefone):
    padrao = r'^\(\d{2}\)\s\d{4,5}-\d{4}$'
    return re.match(padrao, telefone)
#validação do CPF do user baseado nos 2 ultimos digitos remove pontos/traços, confere se tem 11 dígitos
def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    digito1 = (soma * 10 % 11) % 10
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    digito2 = (soma * 10 % 11) % 10
    return digito1 == int(cpf[9]) and digito2 == int(cpf[10])


#Sistema
#Esse é a base de cadastro de tudo, pega todas as infos e joga dentro dos dicionarios para guardar tudo em cache.
class SistemaConsorcio:
    def __init__(self):
        self.conn = sqlite3.connect(
            "consorcio.db",
            check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

# TABELAS
    def criar_tabelas(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf TEXT,
            telefone TEXT,
            email TEXT,
            grupo_id INTEGER)
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS veiculos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT,
            modelo TEXT,
            ano INTEGER,
            valor REAL)
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS grupos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            parcelas INTEGER,
            valor_credito REAL,
            quantidade_cotas INTEGER,
            taxa REAL)
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS cotas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER,
            cliente_id INTEGER,
            grupo_id INTEGER,
            parcelas INTEGER)
        """)
        self.conn.commit()
#classes
#Classe/formulario para o cliente responder
    def cadastrar_cliente(
        self,
        nome,
        cpf,
        telefone,
        email,
        grupo_id):
        if not validar_cpf(cpf):
            raise ValueError("CPF inválido")
        if not validar_telefone(telefone):
            raise ValueError("Telefone inválido")
        if not validar_email(email):
            raise ValueError("E-mail inválido")
        self.cursor.execute("""
        INSERT INTO clientes(
            nome,
            cpf,
            telefone,
            email,
            grupo_id)
        VALUES(?,?,?,?,?)
        """, (
            nome,
            cpf,
            telefone,
            email,
            grupo_id))
        self.conn.commit()
    def listar_clientes(self):
        self.cursor.execute(
            "SELECT * FROM clientes")
        colunas = [c[0] for c in self.cursor.description]
        return [
            dict(zip(colunas, linha))
            for linha in self.cursor.fetchall()]

    def buscar_cliente(self, cliente_id):
        self.cursor.execute(
            "SELECT * FROM clientes WHERE id=?",
            (cliente_id,))
        linha = self.cursor.fetchone()
        if linha:
            colunas = [c[0] for c in self.cursor.description]
            return dict(zip(colunas, linha))
        return None
    def excluir_cliente(self, cliente_id):
        self.cursor.execute(
            "DELETE FROM clientes WHERE id=?",
            (cliente_id,))
        self.conn.commit()
		
#Veiculos
#não tem validação para ter veiculos, ent so é um cadastro mesmo deles
    def cadastrar_veiculo(
        self,
        marca,
        modelo,
        ano,
        valor):
        self.cursor.execute("""
        INSERT INTO veiculos(
            marca,
            modelo,
            ano,
            valor)
        VALUES(?,?,?,?)
        """, (
            marca,
            modelo,
            ano,
            valor))
        self.conn.commit()
    def listar_veiculos(self):
        self.cursor.execute(
            "SELECT * FROM veiculos")
        colunas = [c[0] for c in self.cursor.description]
        return [
            dict(zip(colunas, linha))
            for linha in self.cursor.fetchall()]
    def excluir_veiculo(self, veiculo_id):
        self.cursor.execute(
            "DELETE FROM veiculos WHERE id=?",
            (veiculo_id,))
        self.conn.commit()

#Grupos
#de forma geral aqui ele realmente cria um grupo a unica coisa importante e logica das taxas
    def criar_grupo(
        self,
        nome,
        veiculo_id,
        quantidade_cotas,
        prazo_meses):
        self.cursor.execute(
            "SELECT * FROM veiculos WHERE id=?",
            (veiculo_id,))
        veiculo = self.cursor.fetchone()
        valor_veiculo = veiculo[4]
        if prazo_meses <= 36:
            taxa = 10
        elif prazo_meses <= 60:
            taxa = 15
        elif prazo_meses <= 80:
            taxa = 18
        elif prazo_meses <= 100:
            taxa = 22
        else:
            taxa = 25
        valor_credito = valor_veiculo + (
            valor_veiculo * (taxa / 100)
        )
#no final a tabela fica assim até
# 36 meses  → 10%
#até 60 meses  → 15%
#até 80 meses  → 18%
#até 100 meses → 22%
#acima de 100  → 25%

        self.cursor.execute("""
        INSERT INTO grupos(
            nome,
            parcelas,
            valor_credito,
            quantidade_cotas,
            taxa
        )
        VALUES(?,?,?,?,?)
        """, (
            nome,
            prazo_meses,
            valor_credito,
            quantidade_cotas,
            taxa))
        self.conn.commit()
    def listar_grupos(self):
        self.cursor.execute(
            "SELECT * FROM grupos")
        colunas = [c[0] for c in self.cursor.description]
        return [
            dict(zip(colunas, linha))
            for linha in self.cursor.fetchall()]
    def buscar_grupo(self, grupo_id):
        self.cursor.execute(
            "SELECT * FROM grupos WHERE id=?",
            (grupo_id,))
        linha = self.cursor.fetchone()
        if linha:
            colunas = [c[0] for c in self.cursor.description]
            return dict(zip(colunas, linha))
        return None
    def excluir_grupo(self, grupo_id):
        self.cursor.execute(
            "DELETE FROM grupos WHERE id=?",
            (grupo_id,))
        self.conn.commit()

# Cotas
#Aqui ele cadastra as cotas mas tambem pega o valor do credito e divide pelo numero de parcelas
    def vender_cota(
        self,
        cliente_id,
        grupo_id):
        grupo = self.buscar_grupo(grupo_id)
        if grupo is None:
            raise ValueError("Grupo não encontrado")
        parcelas = grupo["parcelas"]
        self.cursor.execute("""
        INSERT INTO cotas(
            numero,
            cliente_id,
            grupo_id,
            parcelas)
        VALUES(?,?,?,?)
        """, (
            0,
            cliente_id,
            grupo_id,
            parcelas))
        cota_id = self.cursor.lastrowid
        self.cursor.execute("""
        UPDATE cotas
        SET numero=?
        WHERE id=?
        """, (
            cota_id,
            cota_id))
        self.conn.commit()
    def listar_cotas(self):
        self.cursor.execute(
            "SELECT * FROM cotas")
        colunas = [c[0] for c in self.cursor.description]
        return [
            dict(zip(colunas, linha))
            for linha in self.cursor.fetchall()]
    def excluir_cota(self, cota_id):
        self.cursor.execute(
            "DELETE FROM cotas WHERE id=?",
            (cota_id,))
        self.conn.commit()
		
#Estatisticas para colocar nos cads do HTML MENU PRINCIPAL
    def estatisticas_sistema(self):
        self.cursor.execute(
            "SELECT COUNT(*) FROM clientes")
        clientes = self.cursor.fetchone()[0]
        self.cursor.execute(
            "SELECT COUNT(*) FROM veiculos")
        veiculos = self.cursor.fetchone()[0]
        self.cursor.execute(
            "SELECT COUNT(*) FROM grupos")
        grupos = self.cursor.fetchone()[0]
        self.cursor.execute(
            "SELECT COUNT(*) FROM cotas")
        cotas = self.cursor.fetchone()[0]
        return {
            "clientes": clientes,
            "veiculos": veiculos,
            "grupos": grupos,
            "cotas": cotas}