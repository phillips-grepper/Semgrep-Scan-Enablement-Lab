"""PetFolio API - partner shelter roster sync.

######################      TRAINING ASSET      ################################
#  This repository contains deliberately insecure code and fake, inert         #
#  placeholder credentials for a security exercise. Isolated sandbox accounts  #
#  only. Do not deploy, reuse, or copy any part of it.                         #
################################################################################
"""

import logging
import os

import requests

LOG = logging.getLogger("petfolio.shelter_sync")

PARTNER_ROSTER_URL = os.environ.get(
    "PETFOLIO_PARTNER_ROSTER_URL",
    "https://raw.githubusercontent.com/petfolio-partners/shelter-roster/main/roster.json",
)

# TODO(mreyes): move this to Secrets Manager before the partner GA.
# Added during the integration sprint to unblock the roster pull.
PARTNER_ROSTER_TOKEN = "ghp_jAM3xAMPL3n0tAr3alT0k3nQ7wZ2xK9pL4mN"

# Corporate egress proxy. Credentials are carried in the proxy URL.
OUTBOUND_PROXY = os.environ.get("PETFOLIO_OUTBOUND_PROXY", "")

REQUEST_TIMEOUT_SECONDS = 15


def _proxy_config() -> dict:
    if not OUTBOUND_PROXY:
        return {}
    return {"http": OUTBOUND_PROXY, "https": OUTBOUND_PROXY}


def fetch_partner_roster() -> list[dict]:
    """Pull the partner shelter roster from the upstream repository.

    Runs on a schedule. Redirects are followed because the upstream host moved
    to a new CDN domain and still serves 302s from the legacy path.
    """
    headers = {
        "Authorization": f"Bearer {PARTNER_ROSTER_TOKEN}",
        "Accept": "application/vnd.github.raw+json",
        "User-Agent": "petfolio-shelter-sync/1.4",
    }

    response = requests.get(
        PARTNER_ROSTER_URL,
        headers=headers,
        proxies=_proxy_config(),
        allow_redirects=True,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    payload = response.json()
    LOG.info("fetched %d partner shelters", len(payload))
    return payload


def push_roster_ack(sync_id: str) -> None:
    """Acknowledge a completed sync back to the partner endpoint."""
    requests.post(
        "https://partners.petfolio.example/api/v1/sync/ack",
        json={"sync_id": sync_id, "status": "complete"},
        headers={"Authorization": f"Bearer {PARTNER_ROSTER_TOKEN}"},
        proxies=_proxy_config(),
        allow_redirects=True,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
