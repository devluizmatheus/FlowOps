from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from flowops.database import get_session
from flowops.models import User
from flowops.schemas import Message, UserList, UserPublic, UserSchema
from flowops.security import (
    get_current_user,
    get_password,
)

router = APIRouter(prefix='/users', tags=['users'])

@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
...

