import { readPinnedFixture, FIXTURE_SHA256 } from "../lib/evidence.js";

// Public read-only fixture delivery; bytes are pinned and checked on every request.
export default function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("X-Content-Type-Options", "nosniff");
  if (req.method !== "GET") return res.status(405).json({error:"Method not allowed"});
  try {
    const bytes = readPinnedFixture();
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.setHeader("X-Fixture-SHA256", FIXTURE_SHA256);
    return res.status(200).send(bytes.toString("utf8"));
  } catch {
    return res.status(503).json({error:"Pinned fixture unavailable or integrity check failed"});
  }
}
