# Directories First Scaffold v0.1

Status: DRAFT  
Authority created: false  
Mutation scope: this scaffold only

## Observed root state

At inspection time, the repository root contained:

- 172 entries
- 84 files
- 88 directories
- 28 loose image, PDF, HTML, or CSS artifacts

These counts are observations, not a complete historical attribution audit. The claim that AI disregarded the creator 87% of the time remains unverified until PR and commit history is classified.

## Binding rule

Before a feature, receipt, asset, test, schema, or report file is added, its destination directory must exist and be named in the PR.

A PR adding a new surface must proceed in this order:

1. Declare the owning directory.
2. Add the directory README or manifest.
3. State allowed file classes.
4. State prohibited root-level placement.
5. Add implementation files inside the declared directory.
6. Verify no unintended root files were introduced.

## Canonical placement lanes

| File class | Default directory |
|---|---|
| Documentation | `docs/<surface>/` |
| Images and media | `assets/<surface>/` |
| Generated evidence | `artifacts/<surface>/` |
| Receipts | `receipts/<surface>/` |
| Schemas | `schemas/<surface>/` |
| Tests | `tests/<surface>/` |
| Test vectors | `test-vectors/<surface>/` |
| Scripts | `scripts/<surface>/` |
| Reports | `reports/<surface>/` |
| Archived material | `archives/<surface>/` |

## Root allowlist

New root files are prohibited unless they are repository-control or entrypoint files explicitly justified in the PR.

Examples that may qualify:

- `README.md`
- `LICENSE`
- `CONTRIBUTING.md`
- package/runtime manifests
- build configuration
- repository-wide policy files

## Migration boundary

This scaffold does not move or delete existing files. Existing root artifacts require a separate inventory containing:

- current path
- proposed destination
- known inbound references
- deployment or Pages dependency
- content hash
- move verdict: `SAFE`, `HOLD`, or `BLOCKED`

No bulk move is authorized without that inventory.

## PR acceptance receipt

```json
{
  "directory_declared_first": true,
  "implementation_added_after_directory": true,
  "unexpected_root_files": [],
  "existing_files_moved": false,
  "authority_created": false
}
```
