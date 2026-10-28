from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    admin: Optional[bool]
    ativo: Optional[bool]

    class Config:
        from_attributes = True

"""class ItemPedidoSchema(BaseModel):
    id: Optional[int]
    pedido_id: int
    sabor: str
    tamanho: str
    quantidade: int
    preco_unitario: float
    
    class Config:
        from_attributes = True"""

class PedidoSchema(BaseModel):
    id_usuario: int
    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str
    
    class Config:
        from_attributes = True

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float
    
    class Config:
        from_attributes = True