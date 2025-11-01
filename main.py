

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['Authorization', 'Content-Type', '*'],
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


@app.get('/')
async def read_root():
    return {'Hello': 'World'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
