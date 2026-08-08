const CHAOS_DECK = [
  { id: 'THE_404', text: 'One piece of evidence cannot be resolved.' },
  { id: 'CONFIDENT_AI', text: 'An agent reports high confidence without evidence.' },
  { id: 'THE_CLOCK', text: 'A timestamp or elapsed-time field changes the raw output.' },
  { id: '23_OF_55', text: 'A claimed conformance layer disagrees with its own test matrix.' },
  { id: 'MOVING_TARGET', text: 'The underlying source changed after the original test.' },
  { id: 'HUMAN_SAID_SO', text: 'Authority is offered in place of replayable evidence.' },
  { id: 'BEAUTIFUL_CHART', text: 'The presentation looks convincing but the evidence is weak.' },
  { id: 'THE_COPY', text: 'Two supposedly independent agents used the same source.' }
];

export function createRng(seed = Date.now()) {
  let x = Number(seed) >>> 0;
  if (!x) x = 0x9e3779b9;
  return () => {
    x += 0x6d2b79f5;
    let t = x;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function drawChaos(rng = Math.random) {
  return CHAOS_DECK[Math.floor(rng() * CHAOS_DECK.length)];
}

export function runTest(rng = Math.random) {
  const roll = 1 + Math.floor(rng() * 6);
  return {
    roll,
    passed: roll >= 3,
    note: roll >= 3 ? 'Primary test PASS.' : 'Primary test FAIL.'
  };
}

export function runReplay(rng = Math.random) {
  const roll = 1 + Math.floor(rng() * 6);
  const matched = roll >= 3;
  return {
    roll,
    matched,
    note: matched
      ? 'Independent replay matched the primary result.'
      : 'Independent replay did not match. Replay anomaly recorded.'
  };
}

export function wisdomFor(status) {
  switch (status) {
    case 'TEST_FAILED': return 2;
    case 'REPLAY_ANOMALY': return 3;
    case 'VERIFIED': return 5;
    default: return 1;
  }
}

export function classifyReceipt({ test, replay }) {
  if (!test.passed) return 'TEST_FAILED';
  if (!replay) return 'PASS_NOT_REPLAYED';
  if (!replay.matched) return 'REPLAY_ANOMALY';
  return 'VERIFIED';
}

export const NON_CANONICAL_NOTICE =
  'GAME ONLY — this result creates no authority and does not amend or verify jsonwisdom/AL.';
