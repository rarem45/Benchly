"""Benchly admin API helpers."""

import requests


class BenchlyAPI:
    def __init__(self, server_url: str):
        self.server_url = server_url.rstrip("/")

    def _endpoint(self, path: str) -> str:
        return f"{self.server_url}{path}"

    def get_leaderboard(self, limit: int = 100, timeout: int = 10) -> dict:
        url = self._endpoint("/leaderboard")
        resp = requests.get(url, params={"limit": limit}, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
