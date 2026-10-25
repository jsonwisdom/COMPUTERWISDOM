// Runs the suite, writes evidence/{junit.xml,test-output.tap,summary.json,vectors.json,SHA256SUMS}.
import { spawnSync, execSync } from 'node:child_process';
import { writeFileSync, readFileSync, readdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { verifyAll } from '../src/vectors.js';

const r = spawnSync(process.execPath, ['--test', '--test-concurrency=1',
  '--test-reporter=tap', '--test-reporter-destination=evidence/test-output.tap',
  '--test-reporter=junit', '--test-reporter-destination=evidence/junit.xml', 'test/'], { encoding: 'utf8' });
const tap = readFileSync('evidence/test-output.tap', 'utf8');
const n = (k) => Number((tap.match(new RegExp(`^# ${k} (\\d+)`, 'm')) || [])[1] ?? NaN);
const py = spawnSync('python3', ['scripts/crosscheck_syn002.py'], { encoding: 'utf8' });
const sh = (c) => { try { return execSync(c, { encoding: 'utf8' }).trim(); } catch { return 'UNAVAILABLE'; } };
const summary = {
  project: 'democracy-dice', version: '1.6.0-hold', status: 'HOLD', AUTHORITY_CREATED: false, FINAL_AUTHORITY: 'JASON',
  generatedAt: new Date().toISOString(), node: process.version, python: sh('python3 --version'),
  baseCommit: sh('git rev-parse HEAD'), exitCode: r.status,
  tests: { total: n('tests'), pass: n('pass'), fail: n('fail'), cancelled: n('cancelled'), skipped: n('skipped') },
  vectors: verifyAll(), syn002PythonCrosscheck: py.stdout.trim(),
  labels: { rolls: 'SYNTHETIC', adapters: 'LIVE_UNAVAILABLE (NOT_CONFIGURED)', adapterStatusMappingTests: 'MOCK fetch' },
};
writeFileSync('evidence/summary.json', JSON.stringify(summary, null, 2) + '\n');
const files = readdirSync('evidence').filter((f) => f !== 'SHA256SUMS').sort();
writeFileSync('evidence/SHA256SUMS', files.map((f) => createHash('sha256').update(readFileSync('evidence/' + f)).digest('hex') + '  ' + f).join('\n') + '\n');
console.log(JSON.stringify(summary.tests), 'exit', r.status);
process.exit(r.status ?? 1);
