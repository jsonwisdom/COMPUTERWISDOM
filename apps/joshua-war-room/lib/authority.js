export const OWNER = "0x65891F97db01C8fC9F76f4DFE65Bd44F8261f1B0";
export const CASE_ID = "CW-JOSHUA-STACK-001";
const phrases=["Falken launches an information challenge.","Falken increases resource pressure.","Falken offers a difficult compromise."];
const specs={DIPLOMACY:{key:"trust",mod:4},FORTIFY:{key:"defense",mod:3},RECON:{key:"intel",mod:2}};
const clamp=n=>Math.max(0,Math.min(100,n));
export function canAuthorize(session,host,now=Date.now()){
 return !!session && typeof session==="object" && session.host===host &&
 typeof session.address==="string" && session.address.toLowerCase()===OWNER.toLowerCase() &&
 Number.isFinite(session.expiresAt) && session.expiresAt>now &&
 Number.isFinite(Date.parse(session.verifiedAt)) && Date.parse(session.verifiedAt)<=now &&
 ["EIP-191 EOA","Base wallet (EIP-1271/6492 compatible)"].includes(session.verification) &&
 typeof session.proofDigest==="string" && /^[a-f0-9]{64}$/.test(session.proofDigest);
}
export function verifyReplay(replay){
 if(!replay || typeof replay!=="object" || replay.case!==CASE_ID || replay.simulation!=="fictional" ||
 !replay.state || typeof replay.state!=="object") return {ok:false,reason:"Case, simulation, or state invalid"};
 const data=replay.state;
 if(!Array.isArray(data.history) || data.history.length<1 || data.history.length>64)
  return {ok:false,reason:"History must contain between 1 and 64 turns"};
 const state={turn:1,defense:60,trust:60,intel:30,points:0,roll:null,status:"TRAINING READY"};
 for(const entry of data.history){
  if(typeof entry!=="string" || entry.length>190) return {ok:false,reason:"Invalid history entry"};
  if(state.defense===0 || state.trust===0)return {ok:false,reason:"Turns continued after the game ended"};
  const match=/^T([1-9]\d*) (DIPLOMACY|FORTIFY|RECON) d20=(\d{1,2}) \+([234]) => (PASS|FAIL) \| (.+)$/.exec(entry);
  if(!match)return {ok:false,reason:"Malformed history line"};
  const [_,turnS,name,rollS,modS,outcome,pressure]=match;
  const turn=Number(turnS), roll=Number(rollS), mod=Number(modS), spec=specs[name];
  if(turn!==state.turn || roll<1 || roll>20 || mod!==spec.mod || pressure!==phrases[(turn-1)%3])
   return {ok:false,reason:"History turn, D20, modifier, or Falken counter-move inconsistent"};
  const pass=roll+mod>=12;
  if((pass?"PASS":"FAIL")!==outcome)return {ok:false,reason:"Roll outcome inconsistent"};
  state.roll=roll;state.points+=pass?20:5;
  state[spec.key]=clamp(state[spec.key]+(pass?14:-7));
  state.defense=clamp(state.defense-(5+turn%3*2));
  state.trust=clamp(state.trust-(turn%2?2:4));
  state.status=state.trust===0||state.defense===0?"SCENARIO LOST — REBUILD TRUST":state.points>=240?
   "SCENARIO WON — CONFLICT DE-ESCALATED":pass?"PASS — CIVILIAN SAFETY IMPROVED":"SETBACK — RETRY STRATEGY";
  state.turn++;
 }
 for(const key of ["turn","defense","trust","intel","points","roll","status"]){
  if(data[key]!==state[key])return {ok:false,reason:"Calculated "+key+" does not match claimed state"};
 }
 return {ok:true,turns:data.history.length,final:state,scope:"Simulation rules consistency only. Not proof of original user actions or wallet signing of turns."};
}
