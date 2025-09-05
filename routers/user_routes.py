from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from schemas.user_schemas import CreateUserDatabaseSchema, CreateUserSchema, GetUserListSchema, GetUserSchema, Message

user_router = APIRouter(prefix="/users")

database = []


@user_router.post('/', status_code=HTTPStatus.CREATED, response_model=CreateUserDatabaseSchema)
def create(user: CreateUserSchema):
    user_with_id = CreateUserDatabaseSchema(
        username=user.username,
        email=user.email,
        password=user.password,
        id=len(database) + 1
    )  # ou fazer um **user.model_dump() -> transforma o modelo em um dicionario de volta, chave e valor
    database.append(user_with_id)
    return user_with_id


@user_router.get('/', status_code=HTTPStatus.OK, response_model=GetUserListSchema)
def read_all():
    return {'users': database}


@user_router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=CreateUserDatabaseSchema)
def update(user_id: int, user: CreateUserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado.'
        )

    user_with_id = CreateUserDatabaseSchema(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@user_router.delete('/{user_id}', response_model=Message)
def delete(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado.'
        )

    del database[user_id - 1]

    return {'message': 'Usuário apagado.'}


@user_router.get('/{user_id}', response_model=GetUserSchema)
def read_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado.'
        )

    return database[user_id - 1]
