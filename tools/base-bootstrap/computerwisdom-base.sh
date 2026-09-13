#!/usr/bin/env bash
set -Eeuo pipefail

die(){ printf 'COMPUTERWISDOM: %s\n' "$*" >&2; exit 1; }
need(){ command -v "$1" >/dev/null 2>&1 || die "'$1' is required."; }
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${CW_ENV_FILE:-$SCRIPT_DIR/.env}"
ACTION="${1:-check}"; shift || true
CHAIN=""; TO=""; SIG=""; VALUE=0; DATA=0x; ALLOW_SEND=0; RECEIPT_ID=""; OBSERVED_AT=""; RECEIPT_OUT=""
ARGS=()
while (($#)); do
  case "$1" in
    --chain) CHAIN="$2"; shift 2;; --to) TO="$2"; shift 2;; --sig) SIG="$2"; shift 2;;
    --arg) ARGS+=("$2"); shift 2;; --value) VALUE="$2"; shift 2;; --data) DATA="$2"; shift 2;;
    --receipt-id) RECEIPT_ID="$2"; shift 2;; --observed-at-utc) OBSERVED_AT="$2"; shift 2;;
    --receipt-out) RECEIPT_OUT="$2"; shift 2;; --allow-send) ALLOW_SEND=1; shift;; *) die "Unknown option: $1";;
  esac
done
POLICY_FILE="$SCRIPT_DIR/config/allowed-environments.json"
[[ -f "$POLICY_FILE" ]] || die "DOTENV_POLICY: missing policy file '$POLICY_FILE'."

DEFAULT_ENV_NAME="$(
  sed -n 's/.*"default"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$POLICY_FILE" |
    head -n 1
)"

[[ -n "$DEFAULT_ENV_NAME" ]] ||
  die 'DOTENV_POLICY: invalid default ENV_NAME.'

read_policy_array() {
  policy_key="$1"

  awk -v wanted="\"$policy_key\"" '
    index($0, wanted) {
      inside = 1
      next
    }

    inside && index($0, "]") {
      exit
    }

    inside {
      line = $0

      sub(/^[[:space:]]*"/, "", line)
      sub(/",[[:space:]]*$/, "", line)
      sub(/"[[:space:]]*$/, "", line)

      if (length(line) > 0) {
        print line
      }
    }
  ' "$POLICY_FILE"
}

ALLOWED_ENV_NAMES="$(read_policy_array allowed_env_names)"
ALLOWED_DOTENV_KEYS="$(read_policy_array allowed_dotenv_keys)"

list_contains() {
  wanted="$1"
  values="$2"

  while IFS= read -r item; do
    if [[ "$item" == "$wanted" ]]; then
      return 0
    fi
  done <<EOF
$values
EOF

  return 1
}

list_contains "$DEFAULT_ENV_NAME" "$ALLOWED_ENV_NAMES" ||
  die 'DOTENV_POLICY: invalid default ENV_NAME.'

DOTENV_NAMES=()
DOTENV_VALUES=()
UNKNOWN_KEYS=()

if [[ -f "$ENV_FILE" ]]; then
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"

    [[ -z "$line" ]] && continue

    case "$line" in
      \#*)
        continue
        ;;
    esac

    case "$line" in
      *=*)
        name="${line%%=*}"
        val="${line#*=}"
        ;;
      *)
        die 'DOTENV_POLICY: MALFORMED_LINE'
        ;;
    esac

    case "$name" in
      [A-Z]*)
        ;;
      *)
        die 'DOTENV_POLICY: MALFORMED_LINE'
        ;;
    esac

    case "$name" in
      *[!A-Z0-9_]*)
        die 'DOTENV_POLICY: MALFORMED_LINE'
        ;;
    esac

    i=0
    while (( i < ${#DOTENV_NAMES[@]} )); do
      if [[ "${DOTENV_NAMES[$i]}" == "$name" ]]; then
        die "DOTENV_POLICY: DUPLICATE_KEY=$name"
      fi
      i=$((i + 1))
    done

    case "$name" in
      *PRIVATE*|*SECRET*|*MNEMONIC*|*SEED*|*PASSWORD*|*TOKEN*)
        die "DOTENV_POLICY: SECRET_LIKE_KEY=$name"
        ;;
    esac

    if ! list_contains "$name" "$ALLOWED_DOTENV_KEYS"; then
      UNKNOWN_KEYS+=("$name")
    fi

    val="${val%\"}"
    val="${val#\"}"
    val="${val%\'}"
    val="${val#\'}"

    DOTENV_NAMES+=("$name")
    DOTENV_VALUES+=("$val")

  done < "$ENV_FILE"
fi

if (( ${#UNKNOWN_KEYS[@]} > 0 )); then
  old_ifs="$IFS"
  IFS=,
  unknown_joined="${UNKNOWN_KEYS[*]}"
  IFS="$old_ifs"

  die "DOTENV_POLICY: UNKNOWN_KEYS=$unknown_joined"
fi

ENV_NAME_VALUE="$DEFAULT_ENV_NAME"

i=0
while (( i < ${#DOTENV_NAMES[@]} )); do
  if [[ "${DOTENV_NAMES[$i]}" == "ENV_NAME" ]]; then
    ENV_NAME_VALUE="${DOTENV_VALUES[$i]}"
  fi
  i=$((i + 1))
done

list_contains "$ENV_NAME_VALUE" "$ALLOWED_ENV_NAMES" ||
  die "ENV_NAME_INVALID: $ENV_NAME_VALUE"

i=0
while (( i < ${#DOTENV_NAMES[@]} )); do
  name="${DOTENV_NAMES[$i]}"
  val="${DOTENV_VALUES[$i]}"

  printf -v "$name" '%s' "$val"
  export "$name"

  i=$((i + 1))
done

found_env_name=0

i=0
while (( i < ${#DOTENV_NAMES[@]} )); do
  if [[ "${DOTENV_NAMES[$i]}" == "ENV_NAME" ]]; then
    found_env_name=1
  fi
  i=$((i + 1))
done

if (( found_env_name == 0 )); then
  ENV_NAME="$DEFAULT_ENV_NAME"
  export ENV_NAME
fi
CHAIN="${CHAIN:-${CW_CHAIN:-base-sepolia}}"
need cast; need forge
case "$CHAIN" in base) EXPECTED=8453; RPC="${CW_BASE_RPC_URL:-}";; base-sepolia) EXPECTED=84532; RPC="${CW_BASE_SEPOLIA_RPC_URL:-}";; *) die 'chain must be base or base-sepolia';; esac
[[ -n "$RPC" && "$RPC" != *YOUR_* ]] || die 'Set the selected RPC URL.'
ACTUAL="$(cast chain-id --rpc-url "$RPC")"; [[ "$ACTUAL" == "$EXPECTED" ]] || die "RPC chain ID '$ACTUAL' does not equal '$EXPECTED'."
valid_address(){ [[ "$1" =~ ^0x[0-9a-fA-F]{40}$ ]] || die "$2 must be a 20-byte EVM address."; }
wallet_address(){
  case "${CW_WALLET_MODE:-}" in
    keystore) [[ -f "${CW_KEYSTORE:-}" ]] || die 'CW_KEYSTORE must identify an encrypted keystore.'; cast wallet address --keystore "$CW_KEYSTORE";;
    hardware) [[ -n "${CW_WALLET_ADDRESS:-}" ]] || die 'CW_WALLET_ADDRESS is required.'; printf '%s\n' "$CW_WALLET_ADDRESS";;
    *) die "CW_WALLET_MODE must be 'keystore' or 'hardware'.";;
  esac
}
ADDRESS=""; [[ "$ACTION" == check ]] || ADDRESS="$(wallet_address)"; [[ -z "$ADDRESS" ]] || valid_address "$ADDRESS" 'wallet address'
tx_args(){ TX=(--from "$ADDRESS" --value "$VALUE"); [[ -n "$SIG" ]] && TX+=("$SIG" "${ARGS[@]}") || [[ "$DATA" == 0x ]] || TX+=(--data "$DATA"); }
case "$ACTION" in
  check) printf '{"action":"check","chain":"%s","chain_id":%s,"transaction_sent":false,"authority_created":false}\n' "$CHAIN" "$ACTUAL";;
  address) printf '%s\n' "$ADDRESS";;
  balance) cast balance "$ADDRESS" --ether --rpc-url "$RPC";;
  read) valid_address "$TO" 'contract address'; [[ -n "$SIG" ]] || die 'read requires --sig'; cast call "$TO" "$SIG" "${ARGS[@]}" --rpc-url "$RPC";;
  simulate) valid_address "$TO" 'destination address'; tx_args; cast call "$TO" "${TX[@]}" --rpc-url "$RPC"; printf '{"action":"simulate","transaction_sent":false,"authority_created":false}\n';;
  send)
    valid_address "$TO" 'destination address'; ((ALLOW_SEND)) || die 'Send disabled: simulate first, then explicitly add --allow-send.'
    read -r -p "Type SEND $EXPECTED: " CONFIRM; [[ "$CONFIRM" == "SEND $EXPECTED" ]] || die 'Confirmation mismatch; nothing was sent.'
    tx_args
    if [[ "${CW_WALLET_MODE:-}" == keystore ]]; then SIGNER=(--keystore "$CW_KEYSTORE"); else HW="${CW_HARDWARE_WALLET:-ledger}"; [[ "$HW" =~ ^(ledger|trezor)$ ]] || die 'hardware wallet must be ledger or trezor'; SIGNER=(--"$HW"); fi
    cast send "$TO" "${TX[@]}" "${SIGNER[@]}" --chain "$EXPECTED" --rpc-url "$RPC";;
  receipt)
    [[ "$RECEIPT_ID" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{2,127}$ ]] || die 'receipt requires a stable --receipt-id.'
    [[ "$OBSERVED_AT" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ]] || die 'receipt requires --observed-at-utc as YYYY-MM-DDTHH:MM:SSZ.'
    [[ -n "$RECEIPT_OUT" ]] || die 'receipt requires --receipt-out.'
    LOWER_ADDRESS="$(printf '%s' "$ADDRESS" | tr '[:upper:]' '[:lower:]')"
    JSON="$(printf '{\"schema\":\"computerwisdom.base-bootstrap-receipt.v1\",\"receipt_id\":\"%s\",\"observed_at_utc\":\"%s\",\"chain\":\"%s\",\"chain_id\":%s,\"wallet_address\":\"%s\",\"action\":\"boundary_check\",\"transaction_sent\":false,\"payment\":false,\"automatic_signing\":false,\"merge\":false,\"push\":false,\"authority_created\":false}' "$RECEIPT_ID" "$OBSERVED_AT" "$CHAIN" "$EXPECTED" "$LOWER_ADDRESS")"
    printf '%s\n' "$JSON" > "$RECEIPT_OUT"; printf '%s\n' "$JSON";;
  *) die 'action must be check, address, balance, read, simulate, send, or receipt';;
esac


