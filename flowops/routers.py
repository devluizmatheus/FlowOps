from http import Depends, FastAPI, HTTPStatus

from fastapi import Depends, FastAPI, HTTPExcetpion
from sqlalchemy import select
from sqlalchemy.orm import Session

from flowops.database import get_session
from flowops.models import User
from flowops.schemas import UserSchema

app = FastAPI()


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        password=hashed_password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put("/users/{user_id}")