# Citizen Audit Vortex — Docker local prototype

This is a **static, citizen-first simulation**, not a service for uploading private evidence, collecting personal data, delivering newspapers, auditing agencies or casting votes. All gate status entries are local browser state and reset on reload. Every gate remains **0 verified** until an independent receipt verification mechanism is implemented and approved.

## Windows PowerShell (Docker Desktop Linux engine)

```powershell
cd C:\Users\jsonw\github
git clone https://github.com/jsonwisdom/COMPUTERWISDOM.git
cd .\COMPUTERWISDOM
git fetch origin agent/governance-corridor-audit-20261104
git switch --track origin/agent/governance-corridor-audit-20261104
cd .\citizen-audit-vortex
docker compose config -q
docker compose up --build -d
docker compose ps
Start-Process http://127.0.0.1:8787
```

If `COMPUTERWISDOM` already exists locally, **do not reclone or overwrite changes**. Instead inspect `git status` and use `git fetch origin` and the remote review branch in a separate worktree.

## Test and stop
```powershell
Invoke-WebRequest http://127.0.0.1:8787 -UseBasicParsing | Select-Object -ExpandProperty StatusCode
docker compose ps
docker compose down
```

The container binds to localhost only. It uses an unprivileged Nginx image, a read-only root filesystem and no added Linux capabilities. No personal records should be entered. The Docker service provides a static UI only.

### Next engineering gates
1. Approved immutable source-receipt schema and per-gate verification.
2. Private, authenticated citizen request flow and jurisdiction-specific legal guidance.
3. Privacy-preserving review/appeal workflow and printable daily paper production.
4. Security tests, independent validation and approval before any public release.

CI can prove that the image builds and serves a page. It does **not** prove due-process compliance or any allegation.
