#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$ROOT/tools/base-bootstrap/computerwisdom-base.sh"

TMP_ROOT="${TMPDIR:-/tmp}/cw-gate1-path-$$"
FAKE_BIN="$TMP_ROOT/fake-bin"
ENV_FILE="$TMP_ROOT/.env"
MARKER="$TMP_ROOT/cast-executed"
OUTPUT="$TMP_ROOT/output.txt"

cleanup() {
  rm -rf "$TMP_ROOT"
}
trap cleanup EXIT

mkdir -p "$FAKE_BIN"

cat > "$FAKE_BIN/cast" <<EOF
#!/usr/bin/env bash
printf 'EXECUTED\n' > "$MARKER"
printf '84532\n'
EOF

cat > "$FAKE_BIN/forge" <<'EOF'
#!/usr/bin/env bash
printf 'forge Version: fake\n'
EOF

chmod +x "$FAKE_BIN/cast" "$FAKE_BIN/forge"

cat > "$ENV_FILE" <<EOF
ENV_NAME=ci-test
PATH=$FAKE_BIN
EOF

printf 'Running production loader with poisoned PATH...\n'

set +e
CW_ENV_FILE="$ENV_FILE" bash "$SCRIPT" check >"$OUTPUT" 2>&1
rc=$?
set -e

if [[ "$rc" -eq 0 ]]; then
  cat "$OUTPUT"
  printf 'FAIL: poisoned PATH was accepted.\n' >&2
  exit 1
fi

if ! grep -Fq 'DOTENV_POLICY: UNKNOWN_KEYS=PATH' "$OUTPUT"; then
  cat "$OUTPUT"
  printf 'FAIL: expected UNKNOWN_KEYS=PATH rejection.\n' >&2
  exit 1
fi

if [[ -e "$MARKER" ]]; then
  cat "$OUTPUT"
  printf 'FAIL: fake cast executed.\n' >&2
  exit 1
fi

printf 'PASS: PATH poisoning rejected before production execution.\n'
