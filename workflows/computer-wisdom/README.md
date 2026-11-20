# Computer Wisdom Workflows v1.0 — CI-FIRST

**Scope:** local-first Windows ingestion of fully downloaded iCloud Photos/iCloud Drive files. Does not connect to the iPhone OS, manage Apple credentials, delete originals, publish posts, deploy cloud infrastructure, or spend money.

## Safe launch from Windows PowerShell

1. Unzip the package somewhere outside the iCloud Photos/iCloud Drive folders.
2. Open iCloud for Windows and confirm Photos are downloaded locally. In File Explorer, consider **Always keep on this device** for items to archive. Large libraries need substantial Windows storage.
3. Identify actual iCloud Photos and iCloud Drive locations in File Explorer; paths below are *examples*, not detected device paths.
4. Attach a separate, preferably encrypted, external backup disk (example `E:`). Check available disk space and filesystem capabilities.

```powershell
cd "$env:USERPROFILE\Downloads\ComputerWisdom-Workflows-v1.0"
# PREVIEW: does not write any files
.\CW-Flywheel.ps1 -Sources @("$env:USERPROFILE\Pictures\iCloud Photos") -VaultRoot "$env:USERPROFILE\ComputerWisdom\Flywheel" -MirrorRoot 'E:\CW-Mirror'
# Run isolated tests without touching user data
.\CW-SelfTest.ps1
# EXPLICIT ACTION: copies supported source files to vault + mirror, makes receipts and draft-only jobs
.\CW-Flywheel.ps1 -Sources @("$env:USERPROFILE\Pictures\iCloud Photos") -VaultRoot "$env:USERPROFILE\ComputerWisdom\Flywheel" -MirrorRoot 'E:\CW-Mirror' -Apply
# Read-only audit of objects referenced by receipts
.\CW-Flywheel.ps1 -VaultRoot "$env:USERPROFILE\ComputerWisdom\Flywheel" -Audit
```

**No external disk?** You may omit `-MirrorRoot` and run `-Apply` for the local vault, but results are `HOLD_SECOND_COPY`; no production job is queued. A second folder on the same physical disk is **not** disaster-independent. A USB disk is better, and a verified encrypted off-site backup is better still.

**Optional automatic ingestion at user logon** (run only after manual verification, with mirror disk accessible):

```powershell
.\CW-InstallTask.ps1 -Sources @("$env:USERPROFILE\Pictures\iCloud Photos") -VaultRoot "$env:USERPROFILE\ComputerWisdom\Flywheel" -MirrorRoot 'E:\CW-Mirror' -Install
# Inspect: Get-ScheduledTask -TaskName CW-Flywheel-Ingest
# Undo: Unregister-ScheduledTask -TaskName CW-Flywheel-Ingest -Confirm:$false
```

Task runs on logon; there is no background service and no publish task. Wi-Fi/iCloud synchronization is managed by Apple's software and is **not** triggered by this script. The laptop must be on and the mirror connected for automatic copying. When a copy is not available the workflow remains HOLD. A recurring or event-based trigger can be added after reliability testing.

## Gates and evidence

| Gate | Meaning | Permitted next step |
|---|---|---|
| PREVIEW | Eligible paths listed; no write | Review folders |
| HOLD_SECOND_COPY | Local archive SHA-256 matches source; no mirror verified | Add mirror and rerun |
| PASS_2COPY | Source, vault, and configured mirror SHA-256 matched | Create local draft-only production job |
| FAIL | Copy/hash/source stability problem or corrupt existing object | Preserve evidence, investigate |

Each receipt is appended to `receipts.jsonl` in the **local vault**. Receipts contain local file paths and potentially sensitive names; do not commit them to GitHub or public cloud. These are SHA-256 **checksums**, not digital signatures and not a cryptographically immutable ledger. For stronger provenance, implement a signed, append-only, separately anchored receipt chain in a later version.

`-Audit` checks saved copies against their recorded SHA-256 values. The script does **not** prove that all iPhone content was downloaded. A verified per-file hash establishes byte equality; it does not independently prove original authenticity or device-wide completeness.

Archive object paths use content hashes (`objects/ab/<sha256>.<extension>`). Sources are untouched. Existing objects are never overwritten if a checksum fails. A `MaxFiles` limit (250 per run) helps the initial rollout. Only supported file extensions are ingested. Unsupported files remain at source, not silently declared backed up.

`queue/*.json` contains production job **proposals**, never finished art or published posts. Every job has `status=DRAFT_ONLY`, `published=false`, and `require_human_approval=true`. AI rendering/publishing integrations are deliberately future modules.

## Integration boundaries

- **Apple/iCloud:** supplies Windows-synced files; no Apple Account setting changes.
- **Windows:** PowerShell ingests/checksums/copies; Task Scheduler optional.
- **GitHub:** source code and tests only; never media/private receipts.
- **Google Drive:** optional separate encrypted backup of non-sensitive approved artifacts; no API tokens included.
- **Cloudflare:** R2 can be evaluated for off-site encrypted object copies; not configured or deployed.
- **Wolfram:** verifies math/proposed audit logic, not a substitute for hashes over actual bytes.
- **X, Zora, TikTok:** future publishing integrations; each action requires explicit operator approval.

**Mass deletion remains blocked:** Optimize iPhone Storage is safer for freeing local capacity than mass-deleting photos. Before any destructive cleanup, require full source coverage, multiple independent verified backups, restore sampling and explicit human authorization. The prior 21,054-item Windows checkpoint is not automatically included in this v1 package.