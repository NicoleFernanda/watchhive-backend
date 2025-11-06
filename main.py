

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from routers.auth_routes import auth_router
from routers.follows_routes import follows_router
from routers.forum_group_routes import forum_group_router
from routers.forum_message_routes import forum_message_router
from routers.forum_participant_routes import forum_participant_router
from routers.media_comment_routes import media_comment_router
from routers.media_routes import media_router
from routers.review_routes import review_router
from routers.user_list_routes import user_list_router
from routers.user_routes import user_router
from settings import settings

app = FastAPI(
    title='WatchHive'
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(media_router)
app.include_router(media_comment_router)
app.include_router(forum_group_router)
app.include_router(forum_message_router)
app.include_router(forum_participant_router)
app.include_router(review_router)
app.include_router(follows_router)
app.include_router(user_list_router)


class CorsFixMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Aplicar cabeçalhos CORS especificamente para endpoints problemáticos
        if request.url.path in ["/relationship/comments", "/relationship/reviews"]:
            response.headers["Access-Control-Allow-Origin"] = "https://cb2c9f90-c05a-429e-ad6d-5c4fe716793f.e1-us-east-azure.choreoapps.dev"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, Accept"
            response.headers["Access-Control-Allow-Credentials"] = "true"
        
        # Para requisições OPTIONS, retornar 200 com cabeçalhos CORS
        if request.method == "OPTIONS" and request.url.path in ["/relationship/comments", "/relationship/reviews"]:
            response = Response(status_code=200)
            response.headers["Access-Control-Allow-Origin"] = "https://cb2c9f90-c05a-429e-ad6d-5c4fe716793f.e1-us-east-azure.choreoapps.dev"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, Accept"
            response.headers["Access-Control-Allow-Credentials"] = "true"
        
        return response

# Adicionar o middleware personalizado primeiro
app.add_middleware(CorsFixMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
    allow_headers=['Authorization', 'Content-Type', 'Accept'],
)


@app.get('/')
async def read_root():
    return {'Hello': 'World'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
