"""Stdlib HTTP fetcher for the WorldMonitor public API.

Implements the live ``Fetcher`` used by the daily cron. The transform/frontmatter logic
in ``pull.py`` is fetcher-agnostic and unit-tested with a fake; this module is the thin,
network-touching edge kept deliberately separate so the tested core stays offline.

Access model (verified 2026-06-09): WorldMonitor is not keyless — an anonymous session
is minted via ``POST /api/wm-session`` (free, ~12 h cookie) which then gates the data
RPCs. ``HttpFetcher`` mints once, caches the cookie, and reuses it across the run.
Pure stdlib (urllib) — no third-party HTTP dependency.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from http.cookiejar import CookieJar
from typing import TYPE_CHECKING

from ingest import worldbank as wb

if TYPE_CHECKING:
    from datetime import datetime

DEFAULT_BASE_URL = "https://api.worldmonitor.app"
SESSION_PATH = "/api/wm-session"
DEFAULT_TIMEOUT = 30.0
DEFAULT_USER_AGENT = "azimuth-ingest/0.1 (+https://github.com/mickywin22/azimuth)"


class FetchError(RuntimeError):
    """Raised on any network / HTTP / decode failure so ``pull`` can degrade-skip it."""


class HttpFetcher:
    """Mints an anonymous WorldMonitor session, then GETs each endpoint as JSON."""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._user_agent = user_agent
        self._jar = CookieJar()
        self._opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self._jar))
        self._session_minted = False

    def _request(self, url: str, *, method: str = "GET") -> bytes:
        req = urllib.request.Request(url, method=method)
        req.add_header("User-Agent", self._user_agent)
        req.add_header("Accept", "application/json")
        try:
            with self._opener.open(req, timeout=self._timeout) as resp:
                data: bytes = resp.read()
                return data
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            raise FetchError(f"{method} {url} failed: {exc}") from exc

    def _ensure_session(self) -> None:
        if self._session_minted:
            return
        self._request(self._base_url + SESSION_PATH, method="POST")
        self._session_minted = True

    def fetch(self, endpoint: str) -> object:
        """Mint the session (once), GET the endpoint, return decoded JSON."""
        self._ensure_session()
        raw = self._request(self._base_url + endpoint)
        try:
            return json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise FetchError(f"GET {endpoint} returned non-JSON: {exc}") from exc


class WorldBankFetcher:
    """Fetches one World Bank Open Data indicator directly (no key, no session).

    The direct counterpart to ``HttpFetcher``: World Bank Open Data (``api.worldbank.org``)
    is genuinely free and keyless, so this fetcher does a plain anonymous GET — no session
    mint, no cookie. All URL/parse/flatten logic is the pure, unit-tested ``ingest.worldbank``
    core; this class is only the thin network edge. It returns the flattened latest-per-country
    rows (a list of flat dicts) so ``pull``'s generic renderer tables them like any other source.
    """

    def __init__(
        self,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
        now: datetime | None = None,
    ) -> None:
        self._timeout = timeout
        self._user_agent = user_agent
        self._now = now

    def _request(self, url: str) -> bytes:
        req = urllib.request.Request(url, method="GET")
        req.add_header("User-Agent", self._user_agent)
        req.add_header("Accept", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                data: bytes = resp.read()
                return data
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            raise FetchError(f"GET {url} failed: {exc}") from exc

    def fetch(self, endpoint: str) -> object:
        """Build the WB URL for a ``worldbank:<CODE>`` endpoint, GET it, return flat rows."""
        try:
            url = wb.build_url(endpoint, now=self._now)
        except ValueError as exc:  # not a worldbank: endpoint / missing code
            raise FetchError(f"bad world-bank endpoint {endpoint!r}: {exc}") from exc
        raw = self._request(url)
        try:
            return wb.transform(raw)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise FetchError(f"{endpoint} returned non-JSON: {exc}") from exc


class CompositeFetcher:
    """Routes each endpoint to the right fetcher by its scheme.

    A ``worldbank:`` sentinel endpoint -> the direct World Bank fetcher (no session); every
    other (``/api/...``) endpoint -> the WorldMonitor session fetcher. This keeps the
    ``Fetcher`` protocol (``fetch(endpoint)``) and the whole ``pull`` core untouched — the
    multi-source routing lives entirely in this one network-edge object.
    """

    def __init__(self, worldmonitor: HttpFetcher, world_bank: WorldBankFetcher) -> None:
        self._worldmonitor = worldmonitor
        self._world_bank = world_bank

    def fetch(self, endpoint: str) -> object:
        if endpoint.startswith(wb.ENDPOINT_PREFIX):
            return self._world_bank.fetch(endpoint)
        return self._worldmonitor.fetch(endpoint)
