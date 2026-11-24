import test from "node:test";
import assert from "node:assert/strict";
import {OWNER,canAuthorize,verifyReplay,CASE_ID} from "../lib/authority.js";
const host="joshua-war-room.vercel.app",now=1794870792657;
const session={address:OWNER,host,verifiedAt:"2026-11-16T23:13:12.657Z",expiresAt:now+1800000,proofDigest:"eb51df8ed3cc1552678f36270bd9c23ac9c6f9be9697aa94e92233688b74e845",verification:"EIP-191 EOA"};
const replay={case:CASE_ID,simulation:"fictional",state:{turn:6,defense:51,trust:53,intel:44,points:85,roll:8,status:"PASS — CIVILIAN SAFETY IMPROVED",history:[
"T1 DIPLOMACY d20=1 +4 => FAIL | Falken launches an information challenge.",
"T2 FORTIFY d20=12 +3 => PASS | Falken increases resource pressure.",
"T3 RECON d20=13 +2 => PASS | Falken offers a difficult compromise.",
"T4 FORTIFY d20=14 +3 => PASS | Falken launches an information challenge.",
"T5 DIPLOMACY d20=8 +4 => PASS | Falken increases resource pressure."
]}};
test("valid recorded 5-turn replay",()=>assert.equal(verifyReplay(replay).ok,true));
test("forged score fails",()=>{const x=structuredClone(replay);x.state.points=999;assert.equal(verifyReplay(x).ok,false)});
test("forged D20 outcome fails",()=>{const x=structuredClone(replay);x.state.history[0]=x.state.history[0].replace("FAIL","PASS");assert.equal(verifyReplay(x).ok,false)});
test("invalid turn number fails",()=>{const x=structuredClone(replay);x.state.history[0]=x.state.history[0].replace("T1 ","T7 ");assert.equal(verifyReplay(x).ok,false)});
test("correct session permits access",()=>assert.equal(canAuthorize(session,host,now),true));
test("no session is denied",()=>assert.equal(canAuthorize(null,host,now),false));
test("expired session is denied",()=>assert.equal(canAuthorize(session,host,session.expiresAt),false));
test("wrong wallet is denied",()=>assert.equal(canAuthorize({...session,address:"0x0000000000000000000000000000000000000001"},host,now),false));
test("wrong host is denied",()=>assert.equal(canAuthorize(session,"attacker.example",now),false));
test("missing proof digest is denied",()=>assert.equal(canAuthorize({...session,proofDigest:""},host,now),false));
