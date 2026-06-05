#!/usr/bin/env python3
"""Hot list skill script (Python stdlib only)."""

from __future__ import annotations

import json
import os
import ssl
import sys
import time
from typing import Any, Dict, NoReturn
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://developer.zhihu.com"
REQUEST_TIMEOUT_SECONDS = 30


def print_usage() -> None:
    print(
        "Usage:\n"
        '  python3 hot-list.py \'{"limit":10}\'\n\n'
        "Environment:\n"
        "  ZHIHU_ACCESS_SECRET   Bearer auth secret (required)\n"
        "  ZHIHU_OPENAPI_BASE_URL Optional, default https://developer.zhihu.com\n"
        "  ZHIHU_HOT_LIST_URL    Optional full endpoint override\n"
        "  ZHIHU_REQUIRE_TLS_VERIFY Optional, 1=force strict\n"
        "  ZHIHU_SKIP_TLS_VERIFY    Optional, 1=skip verification silently\n"
    )


def die(message: str, *, body: Any | None = None) -> NoReturn:
    payload: Dict[str, Any] = {"error": message, "exit_code": 1}
    if body is not None:
        payload["body"] = body
    print(json.dumps(payload, ensure_ascii=False))
    raise SystemExit(1)


def parse_payload(raw: str) -> Dict[str, Any]:
    if not raw.strip():
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        die("Invalid JSON payload")
    if not isinstance(payload, dict):
        die("Invalid JSON payload")
    return payload


def parse_limit(payload: Dict[str, Any]) -> int:
    raw = payload.get("limit", payload.get("Limit", 30))
    try:
        limit = int(raw)
    except (TypeError, ValueError):
        limit = 30
    return max(1, min(30, limit))


def get_endpoint() -> str:
    explicit = os.getenv("ZHIHU_HOT_LIST_URL", "").strip()
    if explicit:
        return explicit
    base_url = os.getenv("ZHIHU_OPENAPI_BASE_URL", DEFAULT_BASE_URL).strip()
    return f"{base_url.rstrip('/')}/api/v1/content/hot_list"


def make_ssl_context():
    if os.getenv("ZHIHU_SKIP_TLS_VERIFY", "").strip() == "1":
        return _insecure_context(silent=True)
    if os.getenv("ZHIHU_REQUIRE_TLS_VERIFY", "").strip() == "1":
        return None
    try:
        import certifi  # type: ignore
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    return _insecure_context(silent=False)


_insecure_warning_shown = False


def _insecure_context(*, silent: bool = False):
    global _insecure_warning_shown
    if not silent and not _insecure_warning_shown:
        sys.stderr.write(
            "[pi-zhihu-search] WARNING: TLS verification disabled. "
            "Install 'certifi' or set ZHIHU_REQUIRE_TLS_VERIFY=1 to enforce.\n"
        )
        _insecure_warning_shown = True
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def request_hot_list(limit: int) -> Dict[str, Any]:
    secret = os.getenv("ZHIHU_ACCESS_SECRET", "").strip()
    if not secret:
        die("Set ZHIHU_ACCESS_SECRET first (Bearer auth only)")
    query = urlencode({"Limit": str(limit)})
    request = Request(
        url=f"{get_endpoint()}?{query}",
        method="GET",
        headers={
            "Authorization": f"Bearer {secret}",
            "X-Request-Timestamp": str(int(time.time())),
            "User-Agent": "pi-zhihu-search/1.0.2",
        },
    )
    ssl_ctx = make_ssl_context()
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS, context=ssl_ctx) as resp:
            body_text = resp.read().decode("utf-8", errors="replace")
    except HTTPError as err:
        body_text = err.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(body_text)
        except json.JSONDecodeError:
            body = body_text
        die(f"HTTP {err.code}", body=body)
    except (URLError, TimeoutError) as err:
        msg = str(err) or "timeout or network error"
        if "CERTIFICATE_VERIFY_FAILED" in msg or "certificate verify failed" in msg.lower():
            die(
                "SSL certificate verify failed",
                body="Run: pip install --upgrade certifi",
            )
        if isinstance(err, TimeoutError) or "timed out" in msg.lower() or "timeout" in msg.lower():
            die("HTTP request failed (timeout or network error)")
        die(f"HTTP request failed: {msg}")

    try:
        return json.loads(body_text)
    except json.JSONDecodeError:
        die("Non-JSON response from API")


def main() -> None:
    if len(sys.argv) >= 2 and sys.argv[1] in {"-h", "--help"}:
        print_usage()
        return
    payload = parse_payload(sys.argv[1] if len(sys.argv) >= 2 else "{}")
    response = request_hot_list(parse_limit(payload))
    data = response.get("Data") if isinstance(response.get("Data"), dict) else {}
    items = data.get("Items") if isinstance(data.get("Items"), list) else []
    normalized_items = [
        {
            "title": item.get("Title", ""),
            "url": item.get("Url", ""),
            "thumbnail_url": item.get("ThumbnailUrl", ""),
            "summary": item.get("Summary", ""),
        }
        for item in items
        if isinstance(item, dict)
    ]
    result = {
        "code": response.get("Code", -1),
        "message": response.get("Message", ""),
        "total": data.get("Total", len(items)),
        "item_count": len(normalized_items),
        "items": normalized_items,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
