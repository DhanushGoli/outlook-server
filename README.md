# outlook-server

Host inbox: Microsoft OAuth, unique mailbox links, Railway/Render deploy.

**Railway:** do not set a start command of `uvicorn ... --port ${PORT:-8001}`.
Use `python start.py` only (or leave start command empty so Docker CMD runs).

See [mail_app/README.md](mail_app/README.md).

Health check: `/healthz`
