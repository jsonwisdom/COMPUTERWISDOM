/* Jaywisdom CoinBaseKidsWebDesign — pure replay helpers, no wallet RPC, network or storage. */
export const VERSION="COINBASEKIDSWEB_NO_SPEND_V0_1";
export const CATALOG_VERSION="JAYWISDOM_PUBLIC_ZORA_CONCEPT_SNAPSHOT_V0_1";
const SPACE=0x100000000;
export function drawIndex(n,rand32){
  if(!Number.isSafeInteger(n)||n<1||n>65536)throw Error("Invalid catalog size");
  const limit=Math.floor(SPACE/n)*n;
  for(let attempts=0;attempts<128;attempts++){
    const word=rand32();
    if(!Number.isSafeInteger(word)||word<0||word>=SPACE)throw Error("Invalid random word");
    if(word<limit)return {index:word%n,randomWord:word,catalogCount:n,method:"UINT32_REJECTION_SAMPLING",attempts:attempts+1};
  }
  throw Error("Entropy source did not produce an accepted sample");
}
export function browserRand32(){
  if(!globalThis.crypto||typeof globalThis.crypto.getRandomValues!=="function")throw Error("Secure randomness unavailable");
  const a=new Uint32Array(1);
  globalThis.crypto.getRandomValues(a);
  return a[0];
}
export function createReceipt(draw,item,{liked=false}={}){
 if(!item||typeof item.id!=="string")throw Error("Missing public concept");
 return {
  schema:VERSION,kind:"FREE_ART_REVEAL_RECEIPT",catalog_version:CATALOG_VERSION,
  concept_id:item.id,public_reference:item.url,selected_index:draw.index,
  accepted_random_word:draw.randomWord,catalog_count:draw.catalogCount,
  draw_method:draw.method,liked:Boolean(liked),
  no_money:true,prize_value_usd:0,crypto_transfer:false,wallet_identity:null,
  entropy_proof:false,server_attestation:false,authority:false
 };
}
export function replayReceipt(receipt,items){
 if(!receipt||!Array.isArray(items)||!items.length)return {valid:false,reason:"MISSING_RECORD"};
 if(receipt.schema!==VERSION||receipt.kind!=="FREE_ART_REVEAL_RECEIPT"||receipt.catalog_version!==CATALOG_VERSION)return {valid:false,reason:"SCHEMA"};
 if(receipt.no_money!==true||receipt.prize_value_usd!==0||receipt.crypto_transfer!==false||receipt.wallet_identity!==null||receipt.authority!==false)return {valid:false,reason:"BOUNDS"};
 if(receipt.server_attestation!==false||receipt.entropy_proof!==false||typeof receipt.liked!=="boolean")return {valid:false,reason:"BOUNDS"};
 if(receipt.catalog_count!==items.length)return {valid:false,reason:"CATALOG_COUNT_MISMATCH"};
 const word=receipt.accepted_random_word,limit=Math.floor(SPACE/items.length)*items.length;
 if(!Number.isSafeInteger(word)||word<0||word>=limit)return {valid:false,reason:"BAD_RANDOM_WORD"};
 const index=word%items.length;
 if(receipt.selected_index!==index||items[index]?.id!==receipt.concept_id||items[index]?.url!==receipt.public_reference)return {valid:false,reason:"SELECTION_MISMATCH"};
 return {valid:true,concept:items[index],reason:"DETERMINISTIC_REPLAY_ONLY_NOT_ENTROPY_ATTESTATION"};
}
export function svgCard(item){
 if(!item||typeof item.gag!=="string")throw Error("Missing card");
 const esc=s=>String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&apos;");
 const gag=esc(item.gag),title=esc(item.title),frame=esc(item.frame);
 return '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="480" viewBox="0 0 360 480" role="img" aria-label="A satirical retro trading card for '+title+'">'+
 '<rect width="360" height="480" fill="#071526"/><rect x="8" y="8" width="344" height="464" fill="#162b40" stroke="#fff3ca" stroke-width="8"/>'+
 '<rect x="20" y="20" width="320" height="48" fill="#e1e58d"/><text x="180" y="51" text-anchor="middle" font-family="monospace" font-size="17" font-weight="bold" fill="#172238">TRIGGERDECK · JAY</text>'+
 '<rect x="29" y="89" width="302" height="258" fill="#31506b" stroke="#a9f5d9" stroke-width="4"/>'+
 '<path d="M75 289 L104 151 L146 225 L185 124 L239 219 L279 148 L299 296Z" fill="#dca0e2" stroke="#071526" stroke-width="8"/>'+
 '<circle cx="145" cy="230" r="16" fill="#14202e"/><circle cx="231" cy="230" r="16" fill="#14202e"/>'+
 '<path d="M143 280 Q186 315 235 280" fill="none" stroke="#15202b" stroke-width="10"/>'+
 '<path d="M60 114h35v12H60zM265 105h35v12h-35zM90 310h24v12H90zM260 310h26v12h-26z" fill="#ffe39d"/>'+
 '<rect x="30" y="364" width="300" height="48" fill="#d2f4e3"/><text x="180" y="384" text-anchor="middle" font-family="monospace" font-size="14" font-weight="bold" fill="#172238" textLength="285" lengthAdjust="spacingAndGlyphs">'+gag+'</text>'+
 '<text x="180" y="433" text-anchor="middle" font-family="monospace" font-size="13" fill="#fff2c9" textLength="312" lengthAdjust="spacingAndGlyphs">'+frame+'</text>'+
 '<text x="180" y="453" text-anchor="middle" font-family="monospace" font-size="10" fill="#a9f5d9">FREE ART · $0 · NO TOKEN REWARD</text></svg>';
}