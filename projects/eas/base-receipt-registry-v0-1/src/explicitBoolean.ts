export function parseExplicitBoolean(
  name: string,
  raw: string | undefined,
  fallback: "true" | "false",
): boolean {
  const value = raw ?? fallback;
  if (value === "true") return true;
  if (value === "false") return false;
  throw new Error(`${name} must be the exact string "true" or "false".`);
}
