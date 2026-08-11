"""Hardened DeepSeek client used by blind benchmark runs."""

from urllib.parse import urlparse

import httpx
from openai import OpenAI


OFFICIAL_DEEPSEEK_BASE_URL = "https://api.deepseek.com"
ALLOWED_API_HOST = "api.deepseek.com"
ALLOWED_API_PATH = "/chat/completions"


def validate_official_base_url(base_url: str) -> str:
    """Fail closed instead of sending papers or credentials to another host."""
    normalized = base_url.rstrip("/")
    parsed = urlparse(normalized)
    if normalized != OFFICIAL_DEEPSEEK_BASE_URL:
        raise ValueError(f"Only {OFFICIAL_DEEPSEEK_BASE_URL} is allowed")
    if (
        parsed.scheme != "https"
        or parsed.hostname != ALLOWED_API_HOST
        or parsed.port not in (None, 443)
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("DeepSeek base URL failed the official-host safety check")
    return normalized


def _assert_deepseek_request(request: httpx.Request) -> None:
    """Guard every actual HTTP request, including SDK-internal behavior."""
    if (
        request.url.scheme != "https"
        or request.url.host != ALLOWED_API_HOST
        or request.url.port not in (None, 443)
        or request.method != "POST"
        or request.url.path != ALLOWED_API_PATH
    ):
        raise RuntimeError("Blocked non-DeepSeek or unexpected outbound request")


def create_deepseek_client(
    api_key: str,
    base_url: str = OFFICIAL_DEEPSEEK_BASE_URL,
    timeout_seconds: float = 600.0,
) -> OpenAI:
    """Create a client that ignores proxy env vars and never follows redirects."""
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY is empty")
    base_url = validate_official_base_url(base_url)
    http_client = httpx.Client(
        trust_env=False,
        follow_redirects=False,
        timeout=httpx.Timeout(timeout_seconds),
        event_hooks={"request": [_assert_deepseek_request]},
    )
    return OpenAI(
        api_key=api_key,
        base_url=base_url,
        max_retries=0,
        timeout=timeout_seconds,
        http_client=http_client,
    )
