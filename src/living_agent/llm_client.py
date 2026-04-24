"""Thin client for KoboldCPP's /api/v1/generate endpoint."""
from __future__ import annotations

import time
from typing import List, Optional

import requests


class KoboldClient:
    """Minimal synchronous client for a local KoboldCPP server."""

    def __init__(self, endpoint: str = "http://localhost:5001/api/v1/generate",
                 max_context: int = 131072,
                 max_retries: int = 3,
                 retry_delay: float = 5.0,
                 timeout: float = 120.0):
        self.endpoint = endpoint
        self.max_context = max_context
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout

    def generate(self, prompt: str, max_tokens: int = 512,
                 temperature: float = 0.7, top_p: float = 0.9,
                 rep_pen: float = 1.1,
                 stop_sequence: Optional[List[str]] = None) -> str:
        payload = {
            "prompt": prompt,
            "max_context_length": self.max_context,
            "max_length": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "rep_pen": rep_pen,
            "stop_sequence": stop_sequence or ["\n\n", "###"],
        }
        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries):
            try:
                r = requests.post(self.endpoint, json=payload, timeout=self.timeout)
                r.raise_for_status()
                data = r.json()
                return data["results"][0]["text"].strip()
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        raise RuntimeError(f"KoboldCPP request failed after {self.max_retries} attempts: {last_exc}")
