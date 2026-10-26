from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType
db = create_engine("sqlite:///banco.db")

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement = True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default = False)

    def __init__(self, nome, email, senha, ativo = True, admin = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

#Pedidos

class Pedido(Base):

    STATUS_PEDIDO = (
        ("PENDENTE", "Pendente"),
        ("FINALIZADO", "Finalizado"),
        ("CANCELADO", "Cancelado")
    )
    __tablename__ = "pedidos"
    id = Column("id", Integer, primary_key=True, autoincrement = True)
    usuario = Column("usuario", Integer, ForeignKey("usuarios.id"))
    status = Column("status", ChoiceType(choices = STATUS_PEDIDO))
    preco = Column("preco", Float)
    
    def __init__(self, usuario, status = "PENDENTE", preco = 0):
        self.usuario = usuario
        self.status = status
        self.preco = preco

#Item do pedido

class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    id = Column("id", Integer, primary_key=True, autoincrement = True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", Integer, ForeignKey("pedidos.id"))
    
    def __init__(self, pedido, sabor, tamanho, quantidade, preco_unitario):
        self.pedido = pedido
        self.sabor = sabor
        self.tamanho = tamanho
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario