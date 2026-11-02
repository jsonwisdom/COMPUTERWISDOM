// CWaaS staging reconciliation Worker. No payment collection without separate release.
// Bind D1 as ORDERS. Set ADMIN_TOKEN (secret), BASE_RPC_URL, PAY_TO, and
// an operator secret. Defaults refuse all state-changing operations.
//
// FACILITATOR SCAFFOLD: Optional facilitator_proof is accepted and lightly checked.
// On-chain USDC Transfer remains the authoritative settlement ground truth.
// Full x402 facilitator /verify + /settle integration is still required before release.
const USDC = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913";
const TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef";
const PRICE = 89000000n;
const HEX40 = /^0x[0-9a-f]{40}$/i, HEX64=/^0x[0-9a-f]{64}$/i;
const response=(obj,status=200)=>new Response(JSON.stringify(obj),{status,headers:{"content-type":"application/json","cache-control":"no-store","x-content-type-options":"nosniff"}});
const normalize = v=>String(v||"").toLowerCase();
const topicAddress=v=>"0x"+v.slice(-40).toLowerCase();
const safeEqual=(a,b)=>{ if(!a||!b)return false;const x=new TextEncoder().encode(a),y=new TextEncoder().encode(b);let z=x.length^y.length;for(let i=0;i<Math.max(x.length,y.length);i++)z|=(x[i]||0)^(y[i]||0);return z===0;};
async function rpc(env,method,params) { const r=await fetch(env.BASE_RPC_URL,{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({jsonrpc:"2.0",id:1,method,params})}); if(!r.ok)throw Error("RPC_HTTP");const x=await r.json();if(x.error)throw Error("RPC_ERROR");return x.result; }
async function digest(v) {const h=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(v));return Array.from(new Uint8Array(h),x=>x.toString(16).padStart(2,"0")).join("");}

// SCAFFOLD: lightweight facilitator-proof check. Replace with real /verify call + schema validation.
function checkFacilitatorProof(proof, order, tx) {
  if (!proof || typeof proof !== "object") return { ok: false, error: "FACILITATOR_PROOF_REQUIRED" };
  // Expect at minimum: scheme, network, txHash or paymentPayload reference, and isValid
  if (proof.isValid !== true && proof.valid !== true) return { ok: false, error: "FACILITATOR_INVALID" };
  if (proof.network && proof.network !== "eip155:8453") return { ok: false, error: "FACILITATOR_WRONG_NETWORK" };
  if (proof.txHash && normalize(proof.txHash) !== tx) return { ok: false, error: "FACILITATOR_TX_MISMATCH" };
  // Order correlation stub: if orderId present it must match
  if (proof.orderId && proof.orderId !== order.order_id) return { ok: false, error: "FACILITATOR_ORDER_MISMATCH" };
  return { ok: true };
}

export default {async fetch(req,env) {
 const url=new URL(req.url);
 if(req.method==="GET"&&(url.pathname==="/health"||url.pathname==="/release")) {let schema=false;try{schema=Boolean((await env.ORDERS.prepare("SELECT count(*) n FROM sqlite_master WHERE type='table' AND name='orders'").first())?.n)}catch{}return response({phase:"STAGING",checkout:"HOLD",payments_enabled:false,verified_settlement:false,order_schema_ready:schema,price_atomic:"89000000",network:"eip155:8453",report_delivery:"GATED",facilitator_proof:"SCAFFOLD"},schema?200:503);}
 if(req.method==="GET"&&url.pathname.startsWith("/report/")) {
   const id=url.pathname.slice(8),token=req.headers.get("x-cwaas-delivery-token");
   if(!/^[a-f0-9-]{36}$/.test(id)||!token)return response({error:"NOT_FOUND"},404);
   const order=await env.ORDERS.prepare("SELECT state, delivery_sha256, receipt_sha256, report_body, download_token_sha256 FROM orders WHERE order_id=?").bind(id).first();
   if(!order||order.state!=="DELIVERED"||!order.report_body||!safeEqual(await digest(token),order.download_token_sha256))return response({error:"NOT_AUTHORIZED"},403);
   if(await digest(order.report_body)!==order.delivery_sha256)return response({error:"INTEGRITY_FAILURE"},503);
   return response({order_id:id,report:JSON.parse(order.report_body),sha256:order.delivery_sha256,settlement_receipt_sha256:order.receipt_sha256});
 }
 // In staging, public POST can never initiate a payment, even with admin token.
 if(req.method!=="POST"||!["/internal/orders","/internal/reconcile","/internal/deliver"].includes(url.pathname))return response({error:"PAYMENT_DISABLED",checkout:"HOLD"},503);
 if(!env.ADMIN_TOKEN||!safeEqual(req.headers.get("authorization"),"Bearer "+env.ADMIN_TOKEN))return response({error:"UNAUTHORIZED"},401);
 if(!env.BASE_RPC_URL||!HEX40.test(env.PAY_TO)||!env.MIN_CONFIRMATIONS)return response({error:"NOT_CONFIGURED"},503);
 let data;try{data=await req.json()}catch{return response({error:"INVALID_JSON"},400)}
 if(url.pathname==="/internal/orders") {
   if(!HEX40.test(data.payer))return response({error:"INVALID_PAYER"},400);
   const id=crypto.randomUUID();await env.ORDERS.prepare("INSERT INTO orders(order_id,product_id,amount_atomic,chain_id,state,payer_address) VALUES (?,'cwaas-verification-report',89000000,8453,'CREATED',?)").bind(id,normalize(data.payer)).run();
   return response({order_id:id,state:"CREATED",payment_collection_enabled:false},201);
 }
 const id=data.order_id;if(typeof id!=="string")return response({error:"INVALID_ORDER"},400);
 const order=await env.ORDERS.prepare("SELECT * FROM orders WHERE order_id=?").bind(id).first();
 if(!order)return response({error:"NOT_FOUND"},404);
 if(url.pathname==="/internal/reconcile"){
   const tx=normalize(data.tx_hash);if(!HEX64.test(tx))return response({error:"INVALID_TX"},400);
   if(order.state==="PAYMENT_VERIFIED"||order.state==="DELIVERED")return response({error:"ALREADY_VERIFIED"},409);

   // SCAFFOLD: require or accept facilitator proof when present
   if (data.facilitator_proof) {
     const fp = checkFacilitatorProof(data.facilitator_proof, order, tx);
     if (!fp.ok) return response({error: fp.error}, 422);
   } else if (env.REQUIRE_FACILITATOR_PROOF === "true") {
     return response({error: "FACILITATOR_PROOF_REQUIRED"}, 422);
   }

   let receipt,tip,chain;try{[receipt,tip,chain]=await Promise.all([rpc(env,"eth_getTransactionReceipt",[tx]),rpc(env,"eth_blockNumber",[]),rpc(env,"eth_chainId",[])])}catch{return response({error:"RPC_UNAVAILABLE"},503)}
   if(chain!=="0x2105")return response({error:"WRONG_RPC_CHAIN"},422);
   if(!receipt||receipt.status!=="0x1"||normalize(receipt.transactionHash)!==tx)return response({error:"NOT_SETTLED"},422);
   const confirmations=Number(BigInt(tip)-BigInt(receipt.blockNumber))+1;if(confirmations<Number(env.MIN_CONFIRMATIONS||6))return response({error:"CONFIRMATIONS_PENDING",confirmations},409);
   let matching=0;
   for(const log of receipt.logs||[]){
     if(normalize(log.address)!==USDC||normalize(log.topics?.[0])!==TRANSFER||log.topics?.length!==3)continue;
     if(topicAddress(log.topics[1])!==normalize(order.payer_address)||topicAddress(log.topics[2])!==normalize(env.PAY_TO))continue;
     if(BigInt(log.data)!==PRICE)continue;
     matching++;
   }
   if(matching!==1)return response({error:"PAYMENT_MATCH_FAILED"},422);
   const fingerprint=await digest(JSON.stringify({order_id:id,tx,asset:USDC,price:"89000000",chain:8453,payer:order.payer_address,pay_to:normalize(env.PAY_TO)}));
   try {const x=await env.ORDERS.prepare("UPDATE orders SET state='PAYMENT_VERIFIED',settlement_tx=?,receipt_sha256=?,updated_at=CURRENT_TIMESTAMP WHERE order_id=? AND state='CREATED' AND settlement_tx IS NULL").bind(tx,fingerprint,id).run();if(x.meta.changes!==1)return response({error:"RECONCILIATION_CONFLICT"},409)}
   catch{return response({error:"DUPLICATE_SETTLEMENT_OR_DB_FAILURE"},409)}
   return response({order_id:id,state:"PAYMENT_VERIFIED",tx_hash:tx,receipt_sha256:fingerprint,confirmations,facilitator_checked:Boolean(data.facilitator_proof)});
 }
 if(order.state!=="PAYMENT_VERIFIED")return response({error:"PAYMENT_NOT_VERIFIED"},409);
 if(!data.report||typeof data.report!=="object"||Array.isArray(data.report))return response({error:"REPORT_REQUIRED"},400);
 const report=JSON.stringify(data.report);if(report.length>200000)return response({error:"REPORT_TOO_LARGE"},413);
 const deliveryHash=await digest(report),token=Array.from(crypto.getRandomValues(new Uint8Array(32)),x=>x.toString(16).padStart(2,"0")).join("");
 const tokenHash=await digest(token);
 const x=await env.ORDERS.prepare("UPDATE orders SET report_body=?,delivery_sha256=?,download_token_sha256=?,state='DELIVERED',updated_at=CURRENT_TIMESTAMP WHERE order_id=? AND state='PAYMENT_VERIFIED'").bind(report,deliveryHash,tokenHash,id).run();
 if(x.meta.changes!==1)return response({error:"DELIVERY_CONFLICT"},409);
 return response({order_id:id,state:"DELIVERED",delivery_sha256:deliveryHash,report_url:new URL("/report/"+id,req.url).toString(),download_token:token,download_header:"x-cwaas-delivery-token"});
 }};
