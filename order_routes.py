from dependencies import pegar_sessao
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import PedidoSchema
from models import Pedido
order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.get("/")
async def pedidos():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de atuenticação
    """
    return {"mensagem": "Você acessou a rota de pedidos"}
    
@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    """
    Essa é a rota padrão de criação de pedidos do nosso sistema.
    """
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}
    