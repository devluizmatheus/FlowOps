from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from flowops.database import get_session
from flowops.models.models import Organizations, Managements, Submanagements, Teams

from flowops.schemas import (
    ManagementsSchema,
    ManagementsPublicSchema,
    SubmanagementsSchema,
    SubmanagementsPublicSchema,
    TeamsSchema,
    TeamsPublicSchema
)


router = APIRouter(prefix='/organizational-structure', tags=['Organizational Structure'])


@router.get('/managements/list', response_model=list[ManagementsPublicSchema])
def ManagementsList(session: Session=Depends(get_session)):
    db_managements = session.execute(select(Managements)).scalars().all()
    return db_managements


@router.post('/managements/create', status_code=HTTPStatus.CREATED, response_model=ManagementsPublicSchema)
def ManagementsCreate(managements: ManagementsSchema,session: Session=Depends(get_session)):
    
    organization = session.get(
        Organizations,
        managements.organization_id
    )

    if organization is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Organização não encontrada'
        )
    
    db_managements = Managements(
        name=managements.name,
        description=managements.description,
        organization_id=managements.organization_id
    )

    session.add(db_managements)
    session.commit()
    session.refresh(db_managements)

    return db_managements


@router.put('/managements/{managements_id}', status_code=HTTPStatus.OK, response_model=ManagementsPublicSchema)
def ManagementsUpdate(managements: ManagementsSchema, managements_id: int, session: Session=Depends(get_session)):
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
    db_managements.organization_id = managements.organization_id

    session.commit()
    session.refresh(db_managements)

    return db_managements


@router.get('/managements/{managements_id}', status_code=HTTPStatus.OK, response_model=ManagementsPublicSchema)
def ManagementsGet(managements_id: int, session: Session=Depends(get_session)):
    db_managements = session.scalar(select(Managements).where(Managements.id == managements_id))

    if db_managements is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Gerência não encontrada'
        )
    
    return db_managements


@router.delete('/managements/{managements_id}', status_code=HTTPStatus.OK, response_model=ManagementsPublicSchema)
def ManagementsDelete(managements_id: int, session: Session=Depends(get_session)):
    db_managements = session.scalar(select(Managements).where(Managements.id == managements_id))

    if db_managements is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Gerência não encontrada'
        )
    
    session.delete(db_managements)
    session.commit()


    return db_managements


@router.get('/submanagements', response_model=list[SubmanagementsPublicSchema])
def SubmanagementsList(session: Session=Depends(get_session)):
    db_submanagements = session.execute(select(Submanagements)).scalars().all()
    return db_submanagements


@router.post('/submanagements', status_code=HTTPStatus.CREATED, response_model=SubmanagementsPublicSchema)
def SubmanagementsCreate(submanagements: SubmanagementsSchema, session: Session=Depends(get_session)):

    db_submanagements = Submanagements(
        name=submanagements.name,
        description=submanagements.description,
        management_id=submanagements.management_id,
    )

    session.add(db_submanagements)
    session.commit()
    session.refresh(db_submanagements)
    
    return db_submanagements


@router.put('/submanagements/{submanagements_id}', status_code=HTTPStatus.OK, response_model=SubmanagementsPublicSchema)
def SubmanagementsUpdate(submanagements_id: int, submanagements: SubmanagementsSchema, session: Session=Depends(get_session)):

    managements = session.get(Managements, submanagements.management_id)

    if managements is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Gerência não encontrada',
        )
    

    db_submanagements = session.scalar(select(Submanagements).where(Submanagements.id == submanagements_id))

    if db_submanagements is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Subgerencia não encontrada',
        )

    db_submanagements.name = submanagements.name
    db_submanagements.description = submanagements.description
    db_submanagements.management_id = submanagements.management_id

    session.commit()
    session.refresh(db_submanagements)

    return db_submanagements


@router.get('/submanagements/{submanagements_id}', response_model=SubmanagementsPublicSchema)
def SubmanagementsGet(submanagements_id: int, session: Session=Depends(get_session)):
    db_submanagements = session.scalar(select(Submanagements).where(Submanagements.id == submanagements_id))

    if db_submanagements is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Subgerência não encontrada',
        )

    return db_submanagements


@router.delete('/submanagements/{submanagements_id}', response_model=SubmanagementsPublicSchema)
def SubmanagementsDelete(submanagements_id: int, session: Session=Depends(get_session)):

    db_submanagements = session.scalar(select(Submanagements).where(Submanagements.id == submanagements_id))

    if db_submanagements is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Subgerencia não encontrada",
        )

    session.delete(db_submanagements)
    session.commit()

    return db_submanagements



@router.get('/teams', response_model=list[TeamsPublicSchema])
def TeamsList(session: Session=Depends(get_session)):
    db_teams = session.execute(select(Teams)).scalars().all()
    return db_teams


@router.post('/teams/new', status_code=HTTPStatus.CREATED, response_model=TeamsPublicSchema)
def TeamsCreate(teams: TeamsSchema, session: Session=Depends(get_session)):
    managements = session.get(Managements, teams.management_id)

    if managements is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Gerência não encontrada"
        )
    
    if teams.submanagement_id is not None:
        submanagements = session.get(
            Submanagements,
            teams.submanagement_id
        )

        if submanagements is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Subgerência não encontrada"
            )

    db_teams = Teams(
        name=teams.name,
        description=teams.description,
        management_id=teams.management_id,
        submanagement_id=teams.submanagement_id,
    )

    session.add(db_teams)
    session.commit()
    session.refresh(db_teams)

    return db_teams



@router.get('/teams/{teams_id}', response_model=TeamsPublicSchema)
def TeamsGet(teams_id: int, session: Session=Depends(get_session)):
    db_teams = session.scalar(select(Teams).where(Teams.id == teams_id))

    if db_teams is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Time não encontrado',
        )
    
    return db_teams

@router.put('/teams/{teams_id}', response_model=TeamsPublicSchema)
def TeamsUpdate(teams_id: int, teams: TeamsSchema, session: Session=Depends(get_session)):
    db_teams = session.scalar(
        select(Teams).where(Teams.id == teams_id),
    )

    if db_teams is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Time não encontrado',
        )
    
    db_teams.name = teams.name
    db_teams.description = teams.description
    db_teams.management_id = teams.management_id
    db_teams.submanagement_id = teams.submanagement_id

    session.commit()
    session.refresh(db_teams)

    return db_teams


@router.delete('/teams/{teams_id}', response_model=TeamsPublicSchema)
def TeamsDelete(teams_id: int, session: Session=Depends(get_session)):
    db_teams = session.scalar(
        select(Teams).where(Teams.id == teams_id),
    )

    if db_teams is None:
        raise HTTPException (
            status_code=HTTPStatus.NOT_FOUND,
            detail="Team não existe",
        )

    session.delete(db_teams)
    session.commit()

    return db_teams
    