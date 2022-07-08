"""The Api adaptors provide sources and stores using API endpoints.
Requires the requests library to be installed.
"""
try:
    import requests  # type: ignore
except ImportError:
    HAS_REQUESTS = False
else:
    HAS_REQUESTS = True

from sinai.exceptions import SourceError
from sinai.models.source import Source
from sinai.models.store import Store
from sinai.types import JDict, MonitorInstance, RequestHeader


class ApiConnection:
    """Base class to share common connection information between API Stores and Sources"""

    ...


class ApiStore(Store):
    """Store data using an API (not implemented)"""

    ...


class ApiSource(Source):
    """Get data from an API endpoint."""

    url: str = ""
    content: JDict = {}
    headers: RequestHeader = {}
    token: str = ""

    def __init__(self, monitor: MonitorInstance):
        super().__init__(monitor)
        if not HAS_REQUESTS:
            raise SourceError("Requests library required for API calls.")
        self.get()

    def get_headers(self) -> RequestHeader:
        """The required authentication, by default uses a bearer token."""
        if self.token:
            return self.bearer_headers(self.token)
        return self.headers

    @staticmethod
    def bearer_headers(token: str) -> RequestHeader:
        """Headers for APIs with bearer token authentication."""
        return {
            "accept": "application/json",
            "Authorization": "Bearer " + token,
        }

    def get(self) -> None:
        """Get the required data from the specified API."""
        response = requests.get(self.url, headers=self.get_headers())
        if response.status_code == 200:
            self.content = response.json()
        else:
            raise SourceError(
                f"The URL {self.url} returned status {response.status_code}."
            )
