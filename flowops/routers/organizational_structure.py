from http import HTTStatus

from fastapi import APIROuter, Depends, HTTPexception
from sqlalchemy import select
from sqlalchemy.orm import Session

from flowops.database import get_session
from flowops.models.models import Managements, Submanagements, Teams


router = APIRouter(prefix='/organizational-structure', tags=['Organizational Structure'])


@router.get('/', response_model=list[ManagementsPublicSchema])
def ManagementsList(management: ManagementsSchema, session: Session=Depends(get_session)):
    db_managements = session.execute(select(Managements.id)).scalars().all()
    return db_managements


@router.post('/create', status_code=HTTPStatus.CREATED, response_model=ManagementsPublicSchema)
def ManagementsCreate(management: ManagementsSchema,session: Session=Depends(get_session)):
    db_managements = Managements(
        name=management.name,
        description=management.description,
        organization_id=management.organization_id
    )

    session.add(db_managements)
    session.commit()
    session.refresh(db_managements)

    return db_managements


@router.put('/{managements_id}', status_code=HTTPStatus.OK)
def ManagementsUpdate(management: ManagementsSchema,managements_id: int, session: Session=Depends(get_session)):
    db_managements = session.scalar(select(Managements).where(Managements.id == managements_id))

    if db_managements is None:
        raise HTTPException(
            status_code = HTTPStatus.NOT_FOUND,
            detail='Essa gerencia não existe'
        )

    organization = session.get(Organizations, managements.organization_id)

    if organization is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Organização não encontrada'
        )
    
    db_managements.name = managements.name
    db_managements.description = managements.description
    db_managements.organizations_id = managements.organizations_id

    session.commit()
    session.refresh(db_managements)

    return db


@router.get('/{managements_id}', status_code=HTTPStatus.OK, response_model=ManagementsPublicSchema)
def ManagementsGet(managements_id: int, session: Session=Depends(get_session)):
    db_managements = session.scalar(select(Managements).where(Managements.id == managements_id))

    if db_managements is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Gerência não encontrada'
        )
    
    return db_managements


@router.delete('/{managements_id}', status_code=HTTPStatus.OK, response_model=ManagementsPublicSchema)
def ManagementsDelete(managements_id: int, session: Session=Depends(get_session)):
    db_managements = session.scalar(select(Managements).where(Managements.id == managements_id))

    if db_managements is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Gerência não encontrada'
        )

    return db_managements


@router.get('/submanagements', status_code=HTTPStatus.OK, response_model=ManagementsPublicSchema)
def SubmanagementsCreate(submanagements_id: int, session: Session=Depends(get_session)):
    db_submanagements = Submanagements(
        name=organizations.name,
        description=organizations.description
    )

    session.add(db_organization)
    session.commit()
    session.refresh(db_organization)
    
    return db_submanagements


