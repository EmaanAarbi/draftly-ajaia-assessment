# Draftly

Draftly is a deliberately scoped collaborative document workspace built for the Ajaia AI-Native Full Stack Developer assessment. Users can create and rename documents, edit formatted content, import text files, and share documents between three simulated workspace users.

## Live application

Add deployed URL here before submission.

## Demo users

Use the **Demo user** selector in the dashboard to switch between:

- Emaan Aarbi
- Alex Morgan
- Sam Lee

No password is required. This is an explicit assessment scope decision that makes sharing behavior quick to evaluate.

## Features

- Create, rename, save, and reopen documents
- Rich-text headings, bold, italic, underline, and lists
- Debounced autosave with visible saving and error states
- Import UTF-8 `.txt` and `.md` files up to 1 MB
- Owner and shared-document dashboard sections
- Owner-controlled sharing with simulated users
- Server-side authorization, validation, and persistent storage
- Responsive interface
- Automated tests for sharing, authorization, and validation

## Technology

- Django 6.1
- Django templates and lightweight browser JavaScript
- Quill 2 rich-text editor loaded from a public CDN
- SQLite locally; PostgreSQL in production
- WhiteNoise and Gunicorn for production delivery
- Render Blueprint for deployment

## Local setup

Requires Python 3.12+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Demo users are created automatically on the first dashboard request.

## Tests

```powershell
python manage.py test
```

The test suite verifies that a shared user can edit, an unshared user cannot access a document, and blank titles are rejected.

## Deployment

The included `render.yaml` provisions a Django web service and PostgreSQL database. In Render, create a new Blueprint from the GitHub repository. If Render assigns a different hostname, update `CSRF_TRUSTED_ORIGINS` to the resulting HTTPS origin.

## Supported imports

Only UTF-8 `.txt` and `.md` files up to 1 MB are supported. Imported source is converted to escaped HTML paragraphs, preventing uploaded markup from executing as HTML.

## Known limitations

- Demo identity switching is not production authentication.
- Sharing grants edit access; viewer/editor roles are not implemented.
- Concurrent edits use last-write-wins behavior.
- Rich-text HTML is trusted from the editor in this assessment build; production would sanitize HTML server-side with an allowlist.
- Quill currently loads through a CDN and requires internet access.

See [ARCHITECTURE.md](ARCHITECTURE.md) for decisions and future work.
