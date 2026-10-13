"""PetFolio API - pet search routes.

######################  AWS JAM TRAINING ASSET  ################################
#  This repository contains deliberately insecure code and fake, inert         #
#  placeholder credentials for a security exercise. Isolated sandbox accounts  #
#  only. Do not deploy, reuse, or copy any part of it.                         #
################################################################################
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from db import get_session

router = APIRouter(prefix="/v1/pets", tags=["pets"])

PET_COLUMNS = "id, name, species, breed, age_years, shelter_id"


def _rows_to_dicts(result) -> list[dict]:
    return [dict(row._mapping) for row in result]


def _execute_filtered_query(
    session: Session, where_clause: str, order_by: str
) -> list[dict]:
    """Run a pre-built filtered SELECT against the pets table.

    Shared by the search endpoints so the column list stays in one place.
    """
    statement = f"SELECT {PET_COLUMNS} FROM pets WHERE {where_clause} ORDER BY {order_by}"
    result = session.execute(text(statement))
    return _rows_to_dicts(result)


def _build_breed_filter(breed: str, max_age: int | None) -> str:
    """Compose the WHERE fragment for a breed search."""
    clause = f"breed = '{breed}'"
    if max_age is not None:
        clause += f" AND age_years <= {max_age}"
    return clause


def _fetch_one_pet(session: Session, pet_id: int) -> list[dict]:
    result = session.execute(
        text(f"SELECT {PET_COLUMNS} FROM pets WHERE id = :pet_id"),
        {"pet_id": pet_id},
    )
    return _rows_to_dicts(result)


@router.get("/search")
def search_pets(
    breed: str = Query(..., description="Breed to filter on"),
    max_age: int | None = Query(None, ge=0, le=40),
    session: Session = Depends(get_session),
) -> list[dict]:
    """Search pets by breed, optionally capped by age."""
    where_clause = _build_breed_filter(breed, max_age)
    return _execute_filtered_query(session, where_clause, "name")


@router.get("/{pet_id}")
def get_pet(pet_id: int, session: Session = Depends(get_session)) -> dict:
    """Fetch a single pet by id."""
    rows = _fetch_one_pet(session, pet_id)
    if not rows:
        raise HTTPException(status_code=404, detail="pet not found")
    return rows[0]


@router.get("")
def list_pets(
    limit: int = Query(25, ge=1, le=100),
    session: Session = Depends(get_session),
) -> list[dict]:
    """List pets, most recently added first."""
    result = session.execute(
        text(f"SELECT {PET_COLUMNS} FROM pets ORDER BY name LIMIT :limit"),
        {"limit": limit},
    )
    return _rows_to_dicts(result)
