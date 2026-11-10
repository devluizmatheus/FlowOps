from datetime import datetime
from enum import Enum

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
    UniqueConstraint,
    CheckConstraint,
    Index,
    text
)

from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, registry

from sqlalchemy import Enum as SQLEnum

from flowops.models.models_mixins import ActiveMixin, TimestampMixin


table_registry = registry()


@mapped_as_dataclass(table_registry)
class Organizations(TimestampMixin, ActiveMixin):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, default=None)


@mapped_as_dataclass(table_registry)
class Roles:
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)


@mapped_as_dataclass(table_registry)
class Managements:
    __tablename__ = "managements"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    name : Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, default=None)

    __table_args__ = (
        UniqueConstraint(
            "organization_id", 
            "name", 
            name="uq_organization_name"
        ),
    )


@mapped_as_dataclass(table_registry)
class Submanagements:
    __tablename__ = "submanagements"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    management_id: Mapped[int] = mapped_column(ForeignKey("managements.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, default=None)

    __table_args__ = (
        UniqueConstraint(
            "management_id",
            "name",
            name="uq_management_name",
        ),
    )


@mapped_as_dataclass(table_registry)
class Teams:
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    management_id: Mapped[int] = mapped_column(ForeignKey("managements.id"), nullable=True)
    submanagement_id: Mapped[int | None] = mapped_column(ForeignKey("submanagements.id"), default=None)
    description: Mapped[str | None] = mapped_column(Text, default=None)

    __table_args__ = (
        UniqueConstraint(
            "management_id",
            "name",
            name="uq_teams_management_name",
        ),
    )


@mapped_as_dataclass(table_registry)
class Users(TimestampMixin, ActiveMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    icon: Mapped[str | None] = mapped_column(String(255), default=None)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"), default=None)
    management_id: Mapped[int | None] = mapped_column(ForeignKey("managements.id"), default=None)
    submanagement_id: Mapped[int | None] = mapped_column(ForeignKey("submanagements.id"), default=None)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), default=None)


@mapped_as_dataclass(table_registry)
class ManagementResponsibilities:

    __tablename__ = "managements_responsibilities"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    management_id: Mapped[int] = mapped_column(ForeignKey("managements.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), init=False, nullable=False, server_default=func.now())
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)


@mapped_as_dataclass(table_registry)
class SubmanagementResponsibilities:

    __tablename__ = "submanagements_responsibilities"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    submanagement_id: Mapped[int] = mapped_column(ForeignKey("submanagements.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), init=False, nullable=False, server_default=func.now())
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)


@mapped_as_dataclass(table_registry)
class TeamsResponsibilities:

    __tablename__ = "teams_responsibilities"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), init=False, nullable=False, server_default=func.now())
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)


@mapped_as_dataclass(table_registry)
class OrganizationDirectorships:

    __tablename__ = "organization_directorships"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), init=False, nullable=False, server_default=func.now())
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    
    __table_args__ = (
        Index(
            "uq_active_director_per_organization",
            "organization_id",
            unique=True,
            postgresql_where=text("ended_at IS NULL"),
            sqlite_where=text("ended_at IS NULL"),
        ),
    )

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@mapped_as_dataclass(table_registry)
class Tasks(TimestampMixin):

    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    management_id: Mapped[int] = mapped_column(ForeignKey("managements.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(
            TaskStatus, 
            native_enum=False,
            values_callable=lambda enum: [item.value for item in enum],
            length=30
        ), 
        default=TaskStatus.TODO, nullable=False
    )
    priority: Mapped[TaskPriority] = mapped_column(
        SQLEnum(
            TaskPriority,
            native_enum=False,
            values_callable=lambda enum: [item.value for item in enum],
            length=20
        ),
        default=TaskPriority.LOW,
        nullable=False
    )
    assigned_to_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), default=None)
    submanagement_id: Mapped[int | None] = mapped_column(ForeignKey("submanagements.id"), default=None) 
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), default=None)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    __table_args__ = (
        CheckConstraint(
            "status IN ('todo', 'in_progress', 'in_review', 'done')",
            name="check_status",
        ),
        CheckConstraint(
            "priority IN ('low', 'medium', 'high')",
            name="check_priority"
        )
    )


@mapped_as_dataclass(table_registry)
class Documents(TimestampMixin):

    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    uploaded_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_key: Mapped[str] = mapped_column(String(500), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(150), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    visibility: Mapped[str] = mapped_column(String(20), nullable=False)
    management_id: Mapped[int | None] = mapped_column(ForeignKey("managements.id"), default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    __table_args__ = (
        CheckConstraint(
            "visibility IN ('private', 'management')",
            name="check_visibility",
        ),
        CheckConstraint(
            """
            (visibility = 'private' AND management_id IS NULL)
            OR
            (visibility = 'management' AND management_id IS NOT NULL)
            """,
            name="check_management_id_for_management_visibility",
        ),
        CheckConstraint(
            "size_bytes >= 0",
            name="check_document_size",
        ),
    )


@mapped_as_dataclass(table_registry)
class TaskComments(TimestampMixin):
    
    __tablename__ = "task_comments"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)


@mapped_as_dataclass(table_registry)
class TaskHistory(TimestampMixin):

    __tablename__ = "task_history"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    field_changed: Mapped[str] = mapped_column(String(100), nullable=False)
    old_value: Mapped[str | None] = mapped_column(Text, default=None)
    new_value: Mapped[str | None] = mapped_column(Text, default=None)


@mapped_as_dataclass(table_registry)
class TaskDocument(TimestampMixin):

    __tablename__ = "task_documents"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False)
    linked_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "task_id",
            "document_id",
            name="uq_task_document",
        ),
    )
