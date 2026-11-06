from pydantic import BaseModel


class OrganizationSchema(BaseModel):
    name: str


class OrganizationUpdateSchema(OrganizationSchema):
    id: int
    model_config = {"from_attributes": True}
