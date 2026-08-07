import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';
import {
  createRng,
  drawChaos,
  runTest,
  runReplay,
  wisdomFor,
  classifyReceipt,
  NON_CANONICAL_NOTICE
} from './engine.js';

const rl = readline.createInterface({ input, output });
const stateDir = path.resolve('state');
const statePath = path.join(stateDir, 'wisdom-graph.json');
const seed = process.env.WISDOM_SEED ? Number(process.env.WISDOM_SEED) : Date.now();
const rng = createRng(seed);

function freshState() {
  return {
    version: 1,
    game: 'RePlay Wisdom Factory Game',
    wisdom: 0,
    history: [],
    gameZeroUnderstood: false,
    checkpointExplanation: null
  };
}

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(statePath, 'utf8'));
  } catch {
    return freshState();
  }
}

function saveState(state) {
  fs.mkdirSync(stateDir, { recursive: true });
  fs.writeFileSync(statePath, `${JSON.stringify(state, null, 2)}\n`);
}

async function ask(prompt) {
  return (await rl.question(prompt)).trim();
}

async function finish(state, round) {
  console.log('\nREFLECTION — mandatory every round');
  const believedBefore = await ask('What did you believe before? ');
  const survived = await ask('What actually survived? ');

  round.reflection = { believedBefore, survived };
  round.completedAt = new Date().toISOString();
  state.history.push(round);
  state.wisdom += wisdomFor(round.status);
  saveState(state);

  console.log(`\nReceipt: ${round.status}`);
  console.log(`Wisdom: +${wisdomFor(round.status)} (game score only)`);
  console.log(NON_CANONICAL_NOTICE);
  return round;
}

async function playRound(state, proposer, skeptic, claim, roundNumber) {
  console.log(`\n========================================`);
  console.log(`GAME ZERO — ROUND ${roundNumber}`);
  console.log(`PROPOSER: ${proposer}`);
  console.log(`CLAIM: ${claim}`);
  console.log(`SKEPTIC: ${skeptic}`);

  const attack = await ask(`${skeptic}, attack one assumption: `);
  if (!attack) {
    return finish(state, {
      roundNumber, proposer, skeptic, claim, attack,
      status: 'NO_ATTACK',
      chaos: null,
      test: null,
      replay: null
    });
  }

  const prediction = (await ask('Predict the primary test (PASS/FAIL): ')).toUpperCase();
  if (!['PASS', 'FAIL'].includes(prediction)) {
    return finish(state, {
      roundNumber, proposer, skeptic, claim, attack, prediction,
      status: 'INVALID_PREDICTION',
      chaos: null,
      test: null,
      replay: null
    });
  }

  const chaos = drawChaos(rng);
  console.log(`\nCHAOS CARD: ${chaos.id}`);
  console.log(chaos.text);

  const test = runTest(rng);
  console.log(`\nTESTER rolled ${test.roll}: ${test.note}`);

  if (!test.passed) {
    return finish(state, {
      roundNumber, proposer, skeptic, claim, attack, prediction,
      chaos, test, replay: null,
      status: classifyReceipt({ test, replay: null })
    });
  }

  console.log('\nPASS is not VERIFIED. The Factory requires REPLAY!');
  const replayChoice = (await ask('Run independent REPLAY? (yes/no): ')).toLowerCase();
  if (!['y', 'yes'].includes(replayChoice)) {
    return finish(state, {
      roundNumber, proposer, skeptic, claim, attack, prediction,
      chaos, test, replay: null,
      status: classifyReceipt({ test, replay: null })
    });
  }

  const replay = runReplay(rng);
  console.log(`REPLAYER rolled ${replay.roll}: ${replay.note}`);

  if (!replay.matched) {
    return finish(state, {
      roundNumber, proposer, skeptic, claim, attack, prediction,
      chaos, test, replay,
      status: classifyReceipt({ test, replay })
    });
  }

  const evidence = await ask('Name one piece of evidence that should be traceable: ');
  if (!evidence) {
    return finish(state, {
      roundNumber, proposer, skeptic, claim, attack, prediction,
      chaos, test, replay, evidence,
      status: 'EVIDENCE_INCOMPLETE'
    });
  }

  const receipt = await ask('SCRIBE: give this game receipt a short label: ');
  if (!receipt) {
    return finish(state, {
      roundNumber, proposer, skeptic, claim, attack, prediction,
      chaos, test, replay, evidence, receipt,
      status: 'RECEIPT_INCOMPLETE'
    });
  }

  return finish(state, {
    roundNumber, proposer, skeptic, claim, attack, prediction,
    chaos, test, replay, evidence, receipt,
    status: classifyReceipt({ test, replay })
  });
}

async function gameZeroCheckpoint(state, playerOne, playerTwo) {
  console.log('\n========================================');
  console.log('GAME ZERO CHECKPOINT');
  console.log('Getting VERIFIED is not the win condition. Understanding is.');

  const one = await ask(`${playerOne}: Why does VERIFIED require more than PASS? `);
  const two = await ask(`${playerTwo}: Why does VERIFIED require more than PASS? `);
  const shared = (await ask('Do you both agree you can explain the difference? (yes/no): ')).toLowerCase();

  state.checkpointExplanation = {
    [playerOne]: one,
    [playerTwo]: two,
    sharedAgreement: ['y', 'yes'].includes(shared),
    recordedAt: new Date().toISOString()
  };

  state.gameZeroUnderstood = Boolean(
    one && two && state.checkpointExplanation.sharedAgreement
  );
  saveState(state);

  console.log(`\nGAME ZERO UNDERSTOOD: ${state.gameZeroUnderstood ? 'YES' : 'NOT YET'}`);
  console.log(NON_CANONICAL_NOTICE);
}

async function main() {
  const state = loadState();

  console.log('\n⚙️  RePlay Wisdom Factory Game');
  console.log('An agentic game about claims that must survive attack, test, replay, and reflection.');
  console.log(NON_CANONICAL_NOTICE);
  console.log(`Seed: ${seed}`);

  const playerOne = (await ask('\nPlayer 1 name [Jay]: ')) || 'Jay';
  const playerTwo = (await ask('Player 2 name [David]: ')) || 'David';

  const claimOne = await ask(`${playerOne}, enter one claim you believe is true: `);
  const claimTwo = await ask(`${playerTwo}, enter one claim you believe is true: `);

  await playRound(state, playerOne, playerTwo, claimOne || 'Unspecified claim', 1);
  await playRound(state, playerTwo, playerOne, claimTwo || 'Unspecified claim', 2);
  await gameZeroCheckpoint(state, playerOne, playerTwo);

  console.log('\nGame Zero complete.');
  console.log(`Session state: ${statePath}`);
}

main()
  .catch((error) => {
    console.error('\nFactory error:', error);
    process.exitCode = 1;
  })
  .finally(() => rl.close());
