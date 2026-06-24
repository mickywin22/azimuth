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

DEFAULT_BASE_URL = "https://api.worldmonitor.app"
SESSION_PATH = "/api/wm-session"
DEFAULT_TIMEOUT = 30.0


class FetchError(RuntimeError):
    """Raised on any network / HTTP / decode failure so ``pull`` can degrade-skip it."""


class HttpFetcher:
    """Mints an anonymous WorldMonitor session, then GETs each endpoint as JSON."""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = "azimuth-ingest/0.1 (+https://github.com/mickywin22/azimuth)",
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
