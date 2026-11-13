from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from flowops.database import get_session
from flowops.models.models import Users as User
from flowops.schemas import UsersCreateSchema, UsersPublicSchema
from flowops.security import (
    get_password_hash,
)

router = APIRouter(prefix='/users', tags=['users'])

@router.post('/', response_model=list[UserPublicSchema])
def UserList(session: Session=Depends(get_session))
    db_user = session.execute(select(User)).scalars().all()
    return db_user


@router.post('/create', status_code=HTTPStatus.CREATED, response_model=UsersPublicSchema)
def UserCreate(user: UsersCreateSchema, session: Session = Depends(get_session)):

    hashed_password = get_password_hash(user.password)

    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        role_id=user.role_id,
        icon=user.icon,
        organization_id=user.organization_id,
        management_id=user.management_id,
        submanagement_id=user.submanagement_id,
        team_id=user.team_id
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user




