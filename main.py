"""PetFolio API - application entrypoint.

######################       TRAINING ASSET     ################################
#  This repository contains deliberately insecure code and fake, inert         #
#  placeholder credentials for a security exercise. Isolated sandbox accounts  #
#  only. Do not deploy, reuse, or copy any part of it.                         #
################################################################################
"""

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

import routes_adopters
import routes_pets
from db import get_session

app = FastAPI(
    title="PetFolio API",
    version="1.4.0",
    description="Pet adoption records for the PetFolio platform.",
)

app.include_router(routes_pets.router)
app.include_router(routes_adopters.router)


@app.get("/healthz")
def healthz(session: Session = Depends(get_session)) -> dict:
    try:
        session.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
    return {
        "status": "ok" if db_ok else "degraded",
        "database": db_ok,
        "version": app.version,
    }
