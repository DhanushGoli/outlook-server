# Private Outlook inbox (Microsoft OAuth)

Web app that signs **you** in with Microsoft and shows **your** mailboxes. Each connected account gets a unique host URL such as `https://your-domain/a/<id>`. Open that link on a new device to see that inbox without connecting Microsoft again. Keep the link private. The home page does not list all mailboxes.

## Run

```bash
pip install -r requirements.txt
export AZURE_CLIENT_ID=...
export AZURE_CLIENT_SECRET=...
export AZURE_TENANT_ID=common
export PUBLIC_BASE_URL=http://localhost:8001
export REDIRECT_URI=http://localhost:8001/auth/callback
export SESSION_SECRET=$(python -c "import secrets; print(secrets.token_urlsafe(48))")
uvicorn mail_app.app:app --host 127.0.0.1 --port 8001
```

## Deploy (Railway recommended)

Volume at `/data`. Env: `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID=common`, `SESSION_SECRET` (never change later), `PUBLIC_BASE_URL`, `REDIRECT_URI`, `HTTPS_ONLY=1`, `MAIL_DB_PATH=/data/accounts.sqlite`.

Entra Web redirect: `https://your-app/auth/callback`. Health: `/healthz`.
