"""PetFolio API - adopter routes.

######################      TRAINING ASSET      ################################
#  This repository contains deliberately insecure code and fake, inert         #
#  placeholder credentials for a security exercise. Isolated sandbox accounts  #
#  only. Do not deploy, reuse, or copy any part of it.                         #
################################################################################
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from db import get_session

router = APIRouter(prefix="/v1/adopters", tags=["adopters"])

ADOPTER_COLUMNS = "id, full_name, city, age, application_status, shelter_id"
ALLOWED_STATUSES = {"pending", "approved", "withdrawn"}


def _rows_to_dicts(result) -> list[dict]:
    return [dict(row._mapping) for row in result]


def _run_adopter_query(session: Session, sql: str, params: dict) -> list[dict]:
    """Execute a bound adopter query. All call sites pass bound parameters."""
    return _rows_to_dicts(session.execute(text(sql), params))


@router.get("/search")
def search_adopters(
    city: str | None = Query(None),
    min_age: int | None = Query(None, ge=0, le=120),
    status: str | None = Query(None),
    limit: int = Query(25, ge=1, le=100),
    session: Session = Depends(get_session),
) -> list[dict]:
    """Search adopters. Every user value is bound, never interpolated."""
    if status is not None and status not in ALLOWED_STATUSES:
        raise HTTPException(status_code=422, detail="invalid status")

    clauses: list[str] = []
    params: dict = {}

    if city is not None:
        clauses.append("city = :city")
        params["city"] = city
    if min_age is not None:
        clauses.append("age >= :min_age")
        params["min_age"] = min_age
    if status is not None:
        clauses.append("application_status = :status")
        params["status"] = status

    sql = f"SELECT {ADOPTER_COLUMNS} FROM adopters"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY full_name LIMIT :limit"
    params["limit"] = limit

    return _run_adopter_query(session, sql, params)


@router.get("/{adopter_id}")
def get_adopter(adopter_id: int, session: Session = Depends(get_session)) -> dict:
    rows = _run_adopter_query(
        session,
        f"SELECT {ADOPTER_COLUMNS} FROM adopters WHERE id = :adopter_id",
        {"adopter_id": adopter_id},
    )
    if not rows:
        raise HTTPException(status_code=404, detail="adopter not found")
    return rows[0]
