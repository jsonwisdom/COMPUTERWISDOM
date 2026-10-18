import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

export const manifest = JSON.parse(readFileSync(new URL('./quests.json', import.meta.url), 'utf8'));
export function score(events = []) {
  if (!Array.isArray(events)) throw new Error('Ledger must be an array');
  const completed = new Map();
  const rejected = [];
  for (const event of events) {
    const quest = manifest.quests.find(q => q.id === event?.quest_id);
    if (!quest || completed.has(quest.id) ||
        event.kind !== 'LEARNING_REVIEW' ||
        typeof event.review_ref !== 'string' || !event.review_ref.trim() ||
        typeof event.reflection !== 'string' || !event.reflection.trim() ||
        !quest.requires.every(id => completed.has(id))) {
      rejected.push(event?.quest_id ?? null);
      continue;
    }
    completed.set(quest.id, event);
  }
  return {
    classification: manifest.classification,
    authority_created: false,
    evidence_verified: false,
    score: manifest.quests.filter(q => completed.has(q.id)).reduce((n,q) => n + q.points, 0),
    maximum: manifest.quests.reduce((n,q) => n + q.points, 0),
    rejected,
    quests: manifest.quests.map(q => ({
      ...q,
      status: completed.has(q.id) ? 'LEARNING_REVIEW_RECORDED' :
        q.requires.every(id => completed.has(id)) ? 'AVAILABLE' : 'LOCKED'
    }))
  };
}
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const events = process.argv[2] ? JSON.parse(readFileSync(process.argv[2], 'utf8')) : [];
  const result = score(events);
  console.log('ENS FIRST — RePlay Wisdom Factory');
  console.log('Game feedback only. This program verifies no evidence and performs no network or wallet actions.');
  console.log('Learning score: ' + result.score + '/' + result.maximum);
  for (const q of result.quests) console.log(q.status + ' | ' + q.id + ' | ' + q.title + ' | ' + q.points + ' points\n' + q.task);
  if (result.rejected.length) console.log('Rejected ledger rows: ' + result.rejected.length);
}
