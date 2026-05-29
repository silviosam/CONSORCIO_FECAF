from dataclasses import dataclass
from enum import Enum
from typing import Dict, List
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

#classes
#Classe/formulario para o cliente responder
@dataclass
class Cliente:
    id: int
    nome: str
    cpf: str
    telefone: str
    email: str
    grupo_id: int

#Classe/formulario do bem que será contemplado
@dataclass
class Veiculo:
    id: int
    marca: str
    modelo: str
    ano: int
    valor: float

#Classe/formulario do consórcio em si (prazo, valor, taxa)
@dataclass
class Grupo:
    id: int
    nome: str
    parcelas: int
    valor_credito: float
    quantidade_cotas: int
    taxa: float

#O Numero de parcelas que o cliente colcou no grupo
@dataclass
class Parcela:
    numero: int
    valor: float

#O contrato do cliente no grupo com alguns dados que ele mesmo colocou
@dataclass
class Cota:
    id: int
    numero: int
    cliente_id: int
    grupo_id: int
    parcelas: List[Parcela]
    lance_ofertado: float = 0.0

#Sistema
#Esse é a base de cadastro de tudo, pega todas as infos e joga dentro dos dicionarios para guardar tudo em cache.
class SistemaConsorcio:

    def __init__(self):
        self.clientes: Dict[int, Cliente] = {}
        self.veiculos: Dict[int, Veiculo] = {}
        self.grupos: Dict[int, Grupo] = {}
        self.cotas: Dict[int, Cota] = {}
        #Esse é o contador inicial so pra n existir um ID 0
        self.id_cliente = 1
        self.id_veiculo = 1
        self.id_grupo = 1
        self.id_cota = 1

#Clientes
#roda os 3 validadores antes de salvar. Se qualquer dado for inválido, lança um ValueError e o cadastro não acontece.
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
        cliente = Cliente(
            self.id_cliente,
            nome,
            cpf,
            telefone,
            email,
            grupo_id)
#Altera o valor da id toda vez que é criado um
        self.clientes[self.id_cliente] = cliente
        self.id_cliente += 1
        return cliente
#O values() pega só os valores (os objetos Cliente), ignorando as chaves (1, 2, 3) o list() transforma isso numa lista
    def listar_clientes(self):
        return list(self.clientes.values())
#Serve pra buscar um cliente específico pelo ID o get() procura a chave no dicionário
    def buscar_cliente(self, cliente_id):
        return self.clientes.get(cliente_id)

#Veiculos
#não tem validação para ter veiculos, ent so é um cadastro mesmo deles
    def cadastrar_veiculo(
        self,
        marca,
        modelo,
        ano,
        valor):
        veiculo = Veiculo(
            self.id_veiculo,
            marca,
            modelo,
            ano,
            valor)
        self.veiculos[self.id_veiculo] = veiculo
        self.id_veiculo += 1
        return veiculo
    def listar_veiculos(self):
        return list(self.veiculos.values())

#Grupos
#de forma geral aqui ele realmente cria um grupo a unica coisa importante e logica das taxas
    def criar_grupo(
        self,
        nome,
        veiculo_id,
        quantidade_cotas,
        prazo_meses):
#no final a tabela fica assim até
# 36 meses  → 10%
#até 60 meses  → 15%
#até 80 meses  → 18%
#até 100 meses → 22%
#acima de 100  → 25%
        veiculo = self.veiculos[veiculo_id]
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
        valor_credito = veiculo.valor + (
            veiculo.valor * (taxa / 100))
#cria um novo objeto do grupo usando o molde que demos la em cima
        grupo = Grupo(
            self.id_grupo,
            nome,
            prazo_meses,
            valor_credito,
            quantidade_cotas,
            taxa)
        self.grupos[self.id_grupo] = grupo
        self.id_grupo += 1
        return grupo
#Mesma logica do Cliente um pega os valores outro puxa a ID do cliente
    def listar_grupos(self):
        return list(self.grupos.values())
    def buscar_grupo(self, grupo_id):
        return self.grupos.get(grupo_id)

# Cotas
#Aqui ele cadastra as cotas mas tambem pega o valor do credito e divide pelo numero de parcelas
    def vender_cota(
        self,
        cliente_id,
        grupo_id):
        grupo = self.grupos[grupo_id]
        valor_parcela = (
            grupo.valor_credito /
            grupo.parcelas)
#cria a lista parcelas e vai adicioanndo parcelas no loop ele n começa no 0 e sim no 1
        parcelas = []
        for i in range(grupo.parcelas):
            parcelas.append(
                Parcela(
                    numero=i + 1,
                    valor=valor_parcela))
#Cria a cota com os valores descritos.
        cota = Cota(
            id=self.id_cota,
            numero=self.id_cota,
            cliente_id=cliente_id,
            grupo_id=grupo_id,
            parcelas=parcelas)
#guardano dicionario cotas e seus valores e add mais um a lista
        self.cotas[self.id_cota] = cota
        self.id_cota += 1
        return cota
#aqui é igual clientes retoma todos os clientes ja criados!
    def listar_cotas(self):
        return list(self.cotas.values())
#Estatisticas para colocar nos cads do HTML MENU PRINCIPAL

    def estatisticas_sistema(self):
        return {
            "clientes": len(self.clientes),
            "veiculos": len(self.veiculos),
            "grupos": len(self.grupos),
            "cotas": len(self.cotas),
    }

    # EXCLUIR CLIENTE
    def excluir_cliente(self, cliente_id):
        if cliente_id in self.clientes:
            del self.clientes[cliente_id]
    # EXCLUIR VEÍCULO
    def excluir_veiculo(self, veiculo_id):
        if veiculo_id in self.veiculos:
            del self.veiculos[veiculo_id]
# EXCLUIR GRUPO
    def excluir_grupo(self, grupo_id):
        if grupo_id in self.grupos:
            del self.grupos[grupo_id]
# EXCLUIR COTA
    def excluir_cota(self, cota_id):
        if cota_id in self.cotas:
            del self.cotas[cota_id]