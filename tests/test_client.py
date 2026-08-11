import httpx
import pytest

from deepseek_autoreviewer.client import (
    _assert_deepseek_request,
    validate_official_base_url,
)


@pytest.mark.parametrize(
    "url",
    [
        "http://api.deepseek.com",
        "https://api.deepseek.com.evil.example",
        "https://api.deepseek.com@evil.example",
        "https://api.deepseek.com/v1",
        "https://api.deepseek.com?redirect=evil.example",
    ],
)
def test_only_exact_official_base_url_is_allowed(url):
    with pytest.raises(ValueError):
        validate_official_base_url(url)


def test_official_base_url_normalizes_one_trailing_slash():
    assert validate_official_base_url("https://api.deepseek.com/") == (
        "https://api.deepseek.com"
    )


def test_request_guard_accepts_only_expected_completion_endpoint():
    allowed = httpx.Request(
        "POST", "https://api.deepseek.com/chat/completions"
    )
    _assert_deepseek_request(allowed)

    blocked = [
        httpx.Request("GET", "https://api.deepseek.com/chat/completions"),
        httpx.Request("POST", "https://api.deepseek.com/v1/chat/completions"),
        httpx.Request("POST", "https://example.com/chat/completions"),
        httpx.Request("POST", "http://api.deepseek.com/chat/completions"),
    ]
    for request in blocked:
        with pytest.raises(RuntimeError, match="Blocked"):
            _assert_deepseek_request(request)
