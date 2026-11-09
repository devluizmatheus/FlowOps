from datetime import datetime
from pydantic import BaseModel, EmailStr

from flowops.models.models import TaskStatus, TaskPriority


# JWT
class Token(BaseModel):
    access_token: str
    token_type: str


class OrganizationSchema(BaseModel):
    name: str
    description: str | None = None


class OrganizationPublicSchema(OrganizationSchema):
    id: int

    model_config = {"from_attributes": True}


class RolesSchema(BaseModel):
    id: int
    code: str
    name: str

    model_config = {"from_attributes": True}


class ManagementsSchema(BaseModel):
    name: str
    description: str | None = None
    
    organization_id: int


class ManagementsPublicSchema(ManagementsSchema):
    id: int 

    model_config = {"from_attributes": True}


class SubmanagementsSchema(BaseModel):
    name: str
    description: str | None = None

    organization_id: int
    management_id: int


class SubmanagementsPublicSchema(SubmanagementsSchema):
    id: int

    model_config = {"from_attributes": True}


class TeamsSchema(BaseModel):
    name: str
    description: str | None = None

    management_id: int
    submanagement_id: int | None = None


class TeamsPublicSchema(TeamsSchema):
    id: int

    model_config = {"from_attributes": True}


class UsersSchema(BaseModel):
    name: str
    email: EmailStr


    role_id: int
    organization_id: int | None = None # Service para verificar se a role dele é admin
    management_id: int | None = None
    submanagement_id: int | None = None
    team_id: int | None = None


class UsersCreateSchema(UsersSchema):
    password: str


class UsersPublicSchema(UsersSchema):
    id: int

    model_config = {"from_attributes": True}


class ManagementResponsibilitiesSchema(BaseModel):
    management_id: int
    user_id: int


class ManagementResponsibilitiesPublicSchema(ManagementResponsibilitiesSchema):
    id: int
    started_at: datetime
    ended_at: datetime | None = None

    model_config = {"from_attributes": True}


class SubmanagementResponsibilitiesSchema(BaseModel):
    submanagement_id: int
    user_id: int


class SubmanagementResponsibilitiesPublicSchema(SubmanagementResponsibilitiesSchema):
    id: int
    started_at: datetime
    ended_at: datetime | None = None

    model_config = {"from_attributes": True}


class TeamsResponsibilitiesSchema(BaseModel):
    team_id: int
    user_id: int


class TeamsResponsibilitiesPublicSchema(TeamsResponsibilitiesSchema):
    id: int
    started_at: datetime
    ended_at: datetime | None = None

    model_config = {"from_attributes": True}


class OrganizationDirectorshipsSchema(BaseModel):
    organization_id: int
    user_id: int


class OrganizationDirectorshipsPublicSchema(OrganizationDirectorshipsSchema):
    id: int
    started_at: datetime
    ended_at: datetime | None = None

    model_config = {"from_attributes": True}


class TasksSchema(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None

    management_id: int
    submanagement_id: int | None = None
    team_id: int | None = None
    assigned_to_id: int | None = None

    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.LOW


class TasksPublicSchema(TasksSchema):
    id: int
    organization_id: int
    created_by_id: int
    completed_at: datetime | None = None
    deleted_at: datetime | None = None

    model_config = {"from_attributes": True}


class DocumentsSchema(BaseModel):
    name: str
    description: str | None = None

    management_id: int | None = None


class DocumentsPublicSchema(DocumentsSchema):
    id: int
    organization_id: int
    uploaded_by_id: int

    model_config = {"from_attributes": True}


class TaskCommentsSchema(BaseModel):
    content: str

    task_id: int


class TaskCommentsPublicSchema(TaskCommentsSchema):
    id: int
    user_id: int

    model_config = {"from_attributes": True}


class TaskHistorySchema(BaseModel):
    content: str
    field_change: str
    old_value: str | None = None
    new_value: str | None = None

    task_id: int


class TaskHistoryPublicSchema(TaskHistorySchema):
    id: int

    model_config = {"from_attributes": True}


class TaskDocumentSchema(BaseModel):
    task_id: int
    document_id: int


class TaskDocumentPublicSchema(TaskDocumentSchema):
    id: int
    linked_by_id: int

    model_config = {"from_attributes": True}