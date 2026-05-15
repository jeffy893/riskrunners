"""
Project Crucible — NERIS API Client
Handles OAuth2 authentication and incident data retrieval from the NERIS API.
"""

import requests
from typing import Optional

from config import API_BASE_URL, NERIS_CLIENT_ID, NERIS_CLIENT_SECRET


class NERISClient:
    """Client for the NERIS (National Emergency Response Information System) API."""

    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        self.client_id = client_id or NERIS_CLIENT_ID
        self.client_secret = client_secret or NERIS_CLIENT_SECRET
        self.base_url = API_BASE_URL
        self.token: Optional[str] = None
        self.session = requests.Session()

    def authenticate(self) -> str:
        """
        Acquire an OAuth2 access token via client_credentials grant.
        POST /token with HTTPBasic auth header containing client_id:client_secret.
        """
        token_url = f"{self.base_url}/token"
        response = self.session.post(
            token_url,
            data={"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret),
        )
        response.raise_for_status()
        token_data = response.json()
        self.token = token_data["access_token"]
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        return self.token

    def _ensure_authenticated(self):
        """Ensure we have a valid token before making API calls."""
        if not self.token:
            self.authenticate()

    def list_incidents(
        self,
        state: str = "AZ",
        incident_types: str = "FIRE",
        page_size: int = 100,
        cursor: Optional[str] = None,
    ) -> dict:
        """
        Fetch fire incidents from the NERIS API.

        Args:
            state: Two-letter state code (default: AZ)
            incident_types: Incident type filter (default: FIRE)
            page_size: Number of results per page (default: 100)
            cursor: Pagination cursor for next page

        Returns:
            Raw JSON response with incidents and pagination info.
        """
        self._ensure_authenticated()

        params = {
            "state": state,
            "incident_types": incident_types,
            "geo_format": "geojson",
            "page_size": page_size,
        }
        if cursor:
            params["cursor"] = cursor

        response = self.session.get(f"{self.base_url}/incident", params=params)
        response.raise_for_status()
        return response.json()

    def list_all_incidents(
        self,
        state: str = "AZ",
        incident_types: str = "FIRE",
        page_size: int = 100,
    ) -> list:
        """
        Fetch all fire incidents, handling pagination automatically.

        Returns:
            List of all incident records.
        """
        all_incidents = []
        cursor = None

        while True:
            data = self.list_incidents(
                state=state,
                incident_types=incident_types,
                page_size=page_size,
                cursor=cursor,
            )
            incidents = data.get("items", data.get("incidents", []))
            all_incidents.extend(incidents)

            cursor = data.get("next_cursor") or data.get("pagination", {}).get("next_cursor")
            if not cursor or not incidents:
                break

        return all_incidents

    def list_entities(self, state: str = "AZ") -> dict:
        """
        Fetch fire department entities for a given state.

        Args:
            state: Two-letter state code

        Returns:
            Raw JSON response with entity data.
        """
        self._ensure_authenticated()

        params = {"state": state}
        response = self.session.get(f"{self.base_url}/entity", params=params)
        response.raise_for_status()
        return response.json()
