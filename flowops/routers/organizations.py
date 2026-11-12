from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from flowops.database import get_session
from flowops.models.models import Organizations
from flowops.schemas import OrganizationSchema, OrganizationPublicSchema


router = APIRouter(prefix='/organizations', tags=['organizations'])


@router.get('/list', response_model=list[OrganizationPublicSchema])
def OrganizationsList(session: Session=Depends(get_session)):
    db_organizations = session.execute(select(Organizations)).scalars().all()
    return db_organizations


@router.post('/create', status_code=HTTPStatus.CREATED, response_model=OrganizationPublicSchema)
def OrganizationCreate(organizations: OrganizationSchema, session: Session=Depends(get_session)):
    db_organization = Organizations(
        name=organizations.name,
        description=organizations.description
    )

    session.add(db_organization)
    session.commit()
    session.refresh(db_organization)

    return db_organization


@router.put('update/{organization_id}', status_code=HTTPStatus.OK, response_model=OrganizationPublicSchema)
def OrganizationUpdate(organization_id: int, organization: OrganizationSchema, session: Session = Depends(get_session)):
    db_organization = session.scalar(
        select(Organizations).where(Organizations.id == organization_id)
    )

    if db_organization is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Organização não encontrada'
        )

    db_organization.name = organization.name
    db_organization.description = organization.description

    session.commit()
    session.refresh(db_organization)

    return db_organization


@router.get('/{organization_id}', status_code=HTTPStatus.OK, response_model=OrganizationPublicSchema)
def OrganizationGet(organization_id: int, session: Session=Depends(get_session)):
    db_organization = session.scalar(select(Organizations).where(Organizations.id == organization_id))
    
    if db_organization is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Organização não encontrada'
        )

    return db_organization


@router.delete('/{organization_id}', response_model=OrganizationPublicSchema)
def OrganizationDelete(organization_id: int, session: Session=Depends(get_session)):
    db_organization = session.scalar(select(Organizations).where(Organizations.id == organization_id))

    if db_organization is None:
        raise HTTPException(
            status_code=HTTStatus.NOT_FOUND,
            detail="Organização não encontrada"
        )

    session.delete(db_organization)
    session.commit()

    return db_organization