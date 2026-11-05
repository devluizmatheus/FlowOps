from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, registry

from flowops.models.models_mixins import ActiveMixin, TimestampMixin


table_registry = registry()


@mapped_as_dataclass(registry=table_registry)
class Organizations(TimestampMixin, ActiveMixin):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)


@mapped_as_dataclass(registry=table_registry)
class Roles:
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)


@mapped_as_dataclass(registry=table_registry)
class Managements:
    __tablename__ = "managements"
    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    name : Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


@mapped_as_dataclass(registry=table_registry)
class Submanagements:
    __tablename__ = "submanagements"
    id: Mapped[int] = mapped_column(primary_key=True)
    management_id: Mapped[int] = mapped_column(ForeignKey("managements.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


@mapped_as_dataclass(registry=table_registrty)
class Teams:
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(primary_key=True)
    management_id: Mapped[int] = mapped_column(ForeignKey("managements.id"), nullable=False)
    submaangement_id: Mapped[int] = mapped_column(ForeignKey("submanagements.id"))
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)


@mapped_as_dataclass(registry=table_registry)
class Users(TimestampMixin, ActiveMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    management_id: Mapped[int] = mapped_column(ForeignKey("managements.id"))
    submanagement_id: Mapped[int] = mapped_column(ForeignKey("submanagements.id"))
    teams_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

