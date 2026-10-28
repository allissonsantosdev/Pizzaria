from dependencies import pegar_sessao, verificar_token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from models import Pedido, Usuario, ItemPedido
from typing import List

order_router = APIRouter(prefix="/pedidos", tags=["Pedidos"], dependencies=[Depends(verificar_token)])


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

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para cancelar este pedido")
    pedido.status = "CANCELADO"
    session.commit()
    return {"mensagem": f"Pedido número: {pedido.id} cancelado com sucesso", "pedido": pedido}

@order_router.get("/listar")
async def pedidos_listar(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para fazer essa operação")
    else:
        pedidos = session.query(Pedido).all()
    return {"mensagem": "Lista de pedidos", "pedidos": pedidos}

@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para adicionar itens a este pedido")
    item_pedido = ItemPedido(
        pedido=id_pedido,
        sabor=item_pedido_schema.sabor,
        tamanho=item_pedido_schema.tamanho,
        quantidade=item_pedido_schema.quantidade,
        preco_unitario=item_pedido_schema.preco_unitario
    )
    if pedido.preco is None:
        pedido.preco = 0.0
    pedido.preco += item_pedido.calcular_preco()
    session.add(item_pedido)

    session.commit()
    return {"mensagem": "Item adicionado com sucesso", "item_pedido": item_pedido.id, "preco_total": pedido.preco}

@order_router.post("/pedido/remover/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item do pedido não encontrado")

    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para remover itens deste pedido")

    if pedido.preco is not None:
        pedido.preco -= item_pedido.calcular_preco()
        if pedido.preco < 0:
            pedido.preco = 0.0

    session.delete(item_pedido)
    session.commit()
    return {"mensagem": "Item removido com sucesso", 
    "quantidade_itens": len(pedido.itens),
    "Pedido": pedido}

#Finalizar um pedido
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para finalizar este pedido")
    pedido.status = "FINALIZADO"
    session.commit()
    return {"mensagem": f"Pedido número: {pedido.id} finalizado com sucesso", "pedido": pedido}

# Visualizar 1 pedido
@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para visualizar este pedido")
    return {"mensagem": "Pedido visualizado com sucesso", "pedido": pedido}


# Visualizar todos os pedidos do usuário autenticado
@order_router.get("/listar/pedidos-usuario", response_model=list[ResponsePedidoSchema])
async def listar_pedidos_usuario(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    return pedidos

