// Deterministic replay engine.
import { rollThree, seededByteSource, recordedByteSource } from './dice.js';
import { digest, sha256Hex } from './jcs.js';
import { assertValid } from './validate.js';

const BASE = { status: 'HOLD', AUTHORITY_CREATED: false, FINAL_AUTHORITY: 'JASON' };

export function makeRoll(rollId, seedDigest, r, dataLabel) {
  return assertValid('RollReceipt', { type: 'RollReceipt', version: '1.6', rollId, seedDigest,
    dice: r.dice, outcomeIndex: r.outcomeIndex, rawBytes: r.rawBytes, rejectedBytes: r.rejectedBytes, dataLabel, ...BASE });
}

function seal(seedDigest, rolls, dataLabel) {
  const body = { type: 'ReplayPacket', version: '1.6', seedDigest, rolls, dataLabel, ...BASE };
  return assertValid('ReplayPacket', { ...body, packetDigest: digest(body) });
}

/** Produce a packet of n rolls from seed material (SYNTHETIC unless caller labels otherwise). */
export function produce(seed, n, dataLabel = 'SYNTHETIC') {
  const seedDigest = 'sha256:' + sha256Hex(seed);
  const next = seededByteSource(seed);
  const rolls = [];
  for (let i = 0; i < n; i++) rolls.push(makeRoll(`roll-${i}`, seedDigest, rollThree(next), dataLabel));
  return seal(seedDigest, rolls, dataLabel);
}

/** Replay from recorded draws only and compare to the packet. Returns {ok, reasons}. */
export function replay(packet, seed) {
  const reasons = [];
  const { packetDigest, ...body } = packet;
  if (digest(body) !== packetDigest) reasons.push('packetDigest mismatch');
  for (const r of packet.rolls) {
    try {
      const re = rollThree(recordedByteSource(r.rawBytes));
      if (re.dice.join() !== r.dice.join() || re.outcomeIndex !== r.outcomeIndex) reasons.push(`${r.rollId}: recorded draws do not reproduce dice`);
      if (re.rawBytes.length !== r.rawBytes.length) reasons.push(`${r.rollId}: extra recorded bytes`);
    } catch (e) { reasons.push(`${r.rollId}: ${e.message}`); }
  }
  if (seed !== undefined) {
    const fresh = produce(seed, packet.rolls.length, packet.dataLabel);
    if (fresh.packetDigest !== packetDigest) reasons.push('seed replay digest mismatch');
  }
  return { ok: reasons.length === 0, reasons };
}
