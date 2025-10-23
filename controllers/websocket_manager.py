import json
from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect

# ALTERADO
# O ConnectionManager precisa ser assíncrono para usar await no send_text
class ConnectionManager:
    """
    Gerencia as conexões WebSocket, agrupadas por ID do Forum Group.
    A chave é o ID do grupo (int), o valor é uma lista de objetos WebSocket ativos.
    """
    # { forum_group_id: [websocket1, websocket2, ...] }
    active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, group_id: int, websocket: WebSocket):
        """Aceita a conexão e a adiciona ao grupo."""
        await websocket.accept()
        
        if group_id not in self.active_connections:
            self.active_connections[group_id] = []
            
        self.active_connections[group_id].append(websocket)
        # print(f"[{group_id}] Conexão estabelecida.") # Opcional
    
    # A desconexão não precisa ser async se só manipula o dicionário.
    def disconnect(self, group_id: int, websocket: WebSocket):
        """Remove a conexão do grupo."""
        if group_id in self.active_connections:
            try:
                self.active_connections[group_id].remove(websocket)
                if not self.active_connections[group_id]:
                    del self.active_connections[group_id]
                # print(f"[{group_id}] Conexão encerrada.") # Opcional
            except ValueError:
                pass
            
    async def broadcast_to_group(self, group_id: int, message: str):
        """Envia uma mensagem para todos os clientes ativos em um grupo."""
        
        if group_id in self.active_connections:
            # Lista de conexões que falharam e precisam ser removidas
            disconnected_connections = []
            
            for connection in self.active_connections[group_id]:
                try:
                    await connection.send_text(message)
                except WebSocketDisconnect:
                    # Conexão fechada durante o envio, marca para remoção
                    disconnected_connections.append(connection)
                except RuntimeError:
                    # Outro erro de conexão, marca para remoção
                    disconnected_connections.append(connection)
            
            # Remove as conexões falhas da lista
            for connection in disconnected_connections:
                self.disconnect(group_id, connection)


# Instância única para ser usada em todos os routers/controllers
websocket_manager = ConnectionManager()