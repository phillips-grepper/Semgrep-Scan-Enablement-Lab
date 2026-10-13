"""PetFolio API - database layer.

######################       TRAINING ASSET     ################################
#  This repository contains deliberately insecure code and fake, inert         #
#  placeholder credentials for a security exercise. Isolated sandbox accounts  #
#  only. Do not deploy, reuse, or copy any part of it.                         #
################################################################################

Database credentials are resolved from AWS Secrets Manager at import time via
the instance role. Nothing here holds a credential literal.
"""

import json
import os
from functools import lru_cache

import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_HOST = os.environ.get("PETFOLIO_DB_HOST", "localhost")
DB_PORT = int(os.environ.get("PETFOLIO_DB_PORT", "5432"))
DB_NAME = os.environ.get("PETFOLIO_DB_NAME", "petfolio")
SECRET_ARN = os.environ.get("PETFOLIO_DB_SECRET_ARN", "")


@lru_cache(maxsize=1)
def _credentials() -> tuple[str, str]:
    client = boto3.client(
        "secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    payload = json.loads(
        client.get_secret_value(SecretId=SECRET_ARN)["SecretString"]
    )
    return payload["username"], payload["password"]


def _database_url() -> str:
    user, password = _credentials()
    return f"postgresql+psycopg://{user}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


ENGINE = create_engine(_database_url(), pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, future=True)


def get_session():
    """FastAPI dependency that yields a database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
