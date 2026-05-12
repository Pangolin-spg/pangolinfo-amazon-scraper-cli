from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


class PangolinfoError(RuntimeError):
    pass


@dataclass(frozen=True)
class PangolinfoClient:
    base_url: str = "https://scrapeapi.pangolinfo.com"
    user_agent: str = "pangolinfo-amazon-scraper-cli/0.1"

    def auth(self, *, email: str, password: str, timeout_s: int = 30) -> str:
        url = f"{self.base_url}/api/v1/auth"
        resp = requests.post(
            url,
            headers={"Content-Type": "application/json", "User-Agent": self.user_agent},
            json={"email": email, "password": password},
            timeout=timeout_s,
        )
        payload = self._parse_json(resp, url=url)
        self._raise_if_api_error(payload, url=url)
        token = payload.get("data")
        if not isinstance(token, str) or not token.strip():
            raise PangolinfoError(f"Unexpected auth response shape from {url}")
        return token

    def post(
        self,
        *,
        path: str,
        token: str,
        json_body: Dict[str, Any],
        timeout_s: int = 60,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        if dry_run:
            return {"url": url, "json": json_body}

        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": self.user_agent,
        }
        resp = requests.post(url, headers=headers, json=json_body, timeout=timeout_s)
        payload = self._parse_json(resp, url=url)
        self._raise_if_api_error(payload, url=url)
        return payload

    def _parse_json(self, resp: requests.Response, *, url: str) -> Dict[str, Any]:
        try:
            payload = resp.json()
        except Exception as e:
            raise PangolinfoError(
                f"Non-JSON response from {url} (status={resp.status_code})"
            ) from e

        if not isinstance(payload, dict):
            raise PangolinfoError(
                f"Unexpected JSON type from {url}: {type(payload).__name__}"
            )
        return payload

    def _raise_if_api_error(self, payload: Dict[str, Any], *, url: str) -> None:
        code = payload.get("code")
        if code == 0:
            return

        message = payload.get("message")
        details: Optional[str] = None
        if message is None:
            details = f"API returned code={code}"
        else:
            details = f"API returned code={code}, message={message}"
        raise PangolinfoError(f"{details} ({url})")
