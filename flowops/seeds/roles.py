from sqlalchemy import select
from sqlalchemy.orm import Session

from flowops.database import engine
from flowops.models.models import Roles


DEFAULT_ROLES = [
    {"code": "platform_admin", "name": "Administrador da Plataforma"},
    {"code": "director", "name": "Diretor"},
    {"code": "manager", "name": "Gerente"},
    {"code": "submanager", "name": "Subgerente"},
    {"code": "leader", "name": "Líder"},
    {"code": "employee", "name": "Funcionário"},
]


def seed_roles():
    with Session(engine) as session:
        for role in DEFAULT_ROLES:
            existing_role = session.scalar(
                select(Roles).where(Roles.code == role["code"])
            )

            if existing_role is None:
                session.add(Roles(**role))

        session.commit()


if __name__ == "__main__":
    seed_roles()