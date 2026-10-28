from pydantic import BaseModel, field_validator
from typing import Optional, List

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

class ResponsePedidoSchema(BaseModel):
    id: int
    status: str 
    preco: float
    itens: List[ItemPedidoSchema]

    @field_validator("status", mode="before")
    def converter_status(cls, v):
        return v.value if hasattr(v, "value") else str(v)

    class Config:
        from_attributes = True