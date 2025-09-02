
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.settings import settings
from routes.fruit_routes import fruits_router

app = FastAPI()
app.include_router(fruits_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
async def read_root():
    return {'Hello': 'World'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
