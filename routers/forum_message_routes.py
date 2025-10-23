from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from controllers import websocket_manager
from controllers.forum_comment_controller import send_forum_message, delete_forum_message
from database import get_session
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_model import User
from schemas.commons_schemas import Message
from schemas.forum_schemas import CreateForumMessageSchema, GetForumMessageSchema
from security import get_current_user

forum_message_router = APIRouter(prefix='/forum_groups', tags=['forum_messages'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@forum_message_router.post('/{id_forum_group}/messages', status_code=HTTPStatus.CREATED, response_model=GetForumMessageSchema)
async def create(id_forum_group: int, comment: CreateForumMessageSchema, current_user: CurrentUser, session: Session):

    try:
        return await send_forum_message(
            id_forum_post=id_forum_group,
            content=comment.content,
            user_id=current_user.id,
            session=session
        )
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))
    except PermissionError as p:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(p))


@forum_message_router.delete('/{id_forum_group}/messages/{id_message}', response_model=Message)
async def delete(id_forum_group: int, id_message: int, current_user: CurrentUser, session: Session):
    try:
        await delete_forum_message(
            current_user_id=current_user.id,
            post_id=id_forum_group,
            comment_id=id_message,
            session=session,
        )
        return {'message': 'Mensagem apagada.'}
    except PermissionError as p:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(p))
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))

# ALTERADO
@forum_message_router.websocket("/{id_forum_group}/ws")
async def websocket_message_endpoint(websocket: WebSocket, id_forum_group: int, current_user: CurrentUser):
    # Nota: A validação do usuário logado (current_user) via Depends em um endpoint WS
    # é avançada e geralmente requer um token JWT nos headers ou cookies. 
    # Se você ainda não tem essa validação no WS, comece apenas com 'id_forum_group: int'.

    # 1. Conecta o cliente ao manager
    await websocket_manager.connect(id_forum_group, websocket)

    try:
        # Loop para manter a conexão ativa. Se o cliente enviar algo, o WS recebe.
        # Mesmo que você não processe o dado (pois o envio é via POST), o loop mantém o canal aberto.
        while True:
            # Espera por qualquer dado enviado pelo cliente WS.
            # O timeout aqui é indefinido, esperando pela desconexão.
            data = await websocket.receive_text()
            
            # OPCIONAL: Se você quiser que o cliente WS envie algo além da mensagem (ex: "digitando..."),
            # você processaria esse 'data' e faria um broadcast específico para "status".
            
    except WebSocketDisconnect:
        # 2. Desconecta o cliente
        websocket_manager.disconnect(id_forum_group, websocket)
        
    except Exception as e:
        # Lidar com outros erros e garantir a desconexão
        print(f"Erro no WebSocket: {e}")
        websocket_manager.disconnect(id_forum_group, websocket)
