# AI-native workflow note

## Tools used

OpenAI Codex was used as an implementation partner for requirement decomposition, architecture selection, scaffolding, test generation, documentation, and iterative verification.

## Where AI accelerated delivery

- Converted the open-ended prompt into mandatory, optional, and deliberately excluded capabilities.
- Compared deployment-compatible architectures against the local environment and time limit.
- Generated the initial Django model, routes, templates, styles, and test cases.
- Produced a first pass of deployment and reviewer documentation.
- Helped identify authorization, import-safety, CSRF, persistence, and autosave edge cases.

## Human decisions, changes, and rejected output

- I selected a Django monolith after verifying that Node/npm were unavailable locally. This avoided spending assessment time installing an unfamiliar toolchain and aligned with my demonstrated Django experience.
- I rejected real-time collaboration because it was optional and would endanger delivery of persistence, sharing, deployment, tests, and documentation.
- I chose simulated users because the prompt explicitly permits them and the workflow is easier for reviewers to evaluate without credentials.
- I constrained imports to UTF-8 `.txt` and `.md` files and escaped their contents rather than accepting broader formats with unverified parsing behavior.
- I kept server-side access checks even though the interface hides unauthorized documents; UI visibility is not an authorization boundary.

## Verification

- Ran Django system checks and database migrations.
- Ran automated tests covering shared-user edits, unauthorized access, and invalid titles.
- Manually exercised document creation, formatting, autosave, refresh persistence, file import, sharing, user switching, and error states.
- Built static assets and tested the production deployment through its public URL.
- Opened submission and media links in a private browser session before submission.

AI materially increased speed, but generated output was treated as a draft. Final architectural choices, scope cuts, execution, and verification remained my responsibility.
