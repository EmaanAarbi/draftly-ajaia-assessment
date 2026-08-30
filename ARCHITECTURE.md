# Architecture and product decisions

## Product slice

The implementation prioritizes one coherent loop: choose a user, create or import a document, format and autosave it, share it, switch users, and reopen it from the shared list. This covers every required capability without spending the timebox on optional real-time collaboration.

## Architecture

Draftly is a Django monolith. Django owns routing, persistence, validation, access checks, HTML rendering, and JSON autosave requests. The browser adds focused interactivity through Quill and a small autosave script. SQLite keeps local setup friction low; `DATABASE_URL` switches production to PostgreSQL without code changes.

The `Document` model stores rich-text HTML plus ownership and a many-to-many list of shared users. Every document read or write passes through `accessible_document`, keeping the access rule centralized. Only owners may grant access; both owners and shared users may edit.

## Deliberate tradeoffs

- **Django monolith over separate SPA/API:** one deployable unit reduced integration and CORS risk under four hours while still exercising frontend, backend, persistence, and access logic.
- **Seeded identities over authentication:** the prompt permits mocked users. A visible user switcher makes the sharing flow immediately testable.
- **Debounced autosave over manual save:** it creates a coherent editor experience while limiting writes.
- **HTML persistence over a custom document schema:** Quill HTML preserves required formatting with much less surface area. Production would sanitize it server-side.
- **Text import only:** `.txt` and `.md` provide a useful import path without adding fragile document-processing dependencies.

## Reliability and security

State-changing routes require POST and Django CSRF protection. The server validates permissions and titles; import handling allowlists extensions, limits size, requires UTF-8, and HTML-escapes content. Automated tests target the most consequential rules rather than superficial page rendering.

## With another 2–4 hours

1. Add real authentication and invitations.
2. Sanitize editor HTML using a strict allowlist.
3. Add optimistic concurrency/version checks to prevent silent overwrite.
4. Add document deletion, share revocation, and viewer/editor roles.
5. Add browser-level tests for the complete sharing flow.
