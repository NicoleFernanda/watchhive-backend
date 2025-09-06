
from http import HTTPStatus

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_session
from models.user_model import User
from routers.user_routes import user_router
from security import create_access_token, verify_password
from settings import settings

app = FastAPI(
    title="WatchHive"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)


@app.get('/')
async def read_root():
    return {"Hello": "World"}


@app.post('/token')  # tipo um login
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='E-mail não cadastrado.'
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Senha incorreta.'
        )

    access_token = create_access_token(
        data={'sub': user.email}
    )

    return {'access_token': access_token, 'token_type': 'Bearer'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
