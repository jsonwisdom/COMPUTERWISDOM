/**
 * Parse a boolean environment variable with NO default.
 *
 * Unset, empty, or anything other than the exact strings "true" / "false"
 * throws, so callers fail closed instead of inheriting a silent default.
 */
export function parseExplicitBoolean(name: string, raw: string | undefined): boolean {
  if (raw === "true") return true;
  if (raw === "false") return false;
  if (raw === undefined || raw === "") {
    throw new Error(`${name} is required and has no default; set it to "true" or "false".`);
  }
  throw new Error(`${name} must be the exact string "true" or "false".`);
}
