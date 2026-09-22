from __future__ import annotations

import asyncio
import hmac
import os
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from mail_app import auth, graph, store
from mail_app.config import load_settings
from mail_app.sanitize import sanitize_html
from mail_app.translate import TRANSLATE_LANGS, TranslateError, translate_pair

ROOT = Path(__file__).resolve().parent
settings = load_settings()
FOLDERS = (
    ("inbox", "Inbox", "IN"),
    ("other", "Other", "OT"),
    ("sentitems", "Sent", "SN"),
    ("drafts", "Drafts", "DR"),
    ("junkemail", "Junk", "JK"),
    ("deleteditems", "Deleted", "DL"),
)
TOKEN_TTL_SECONDS = 20 * 60
FEED_TTL_SECONDS = 20
_token_cache: dict[str, tuple[float, str]] = {}
_feed_cache: dict[tuple, tuple[float, tuple]] = {}

async def keep_connected_accounts() -> int:
    """Refresh stored Microsoft tokens so mailboxes stay linked until revoked."""
    if not settings.session_secret:
        return 0
    refs = store.list_mailbox_refs()

    async def one(ref: store.MailboxRef) -> bool:
        try:
            account = store.get_account(ref.id, settings.session_secret)
        except RuntimeError:
            return False
        if not account:
            return False
        _token_cache.pop(account.id, None)
        return bool(await _token_for_account(account))

    results = await asyncio.gather(*(one(ref) for ref in refs))
    return sum(1 for ok in results if ok)
