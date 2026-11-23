import {inventory} from './inventory.mjs';
const json=(v,status=200)=>Response.json(v,{status,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
const canonical=x=>JSON.stringify(x&&typeof x==='object'?Array.isArray(x)?x.map(v=>JSON.parse(canonical(v))):Object.fromEntries(Object.keys(x).sort().map(k=>[k,JSON.parse(canonical(x[k]))])):x);
const digest=async s=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)))].map(b=>b.toString(16).padStart(2,'0')).join('');
export default {async fetch(req,env){try{const u=new URL(req.url);
if(u.pathname==='/health')return json({service:'wisdom-catalog-curator',catalog_records:inventory.records.length,commerce:'HOLD',schema:inventory.schema,source_hashes:inventory.source_hashes});
if(req.method==='GET'&&u.pathname==='/inventory'){
const view=u.searchParams.get('view')||'learning';if(!['learning','readiness','commerce','provenance'].includes(view))return json({error:'invalid_view'},400);
const sku=u.searchParams.get('sku');const rows=inventory.records.filter(x=>!sku||x.sku===sku).map(x=>view==='learning'?{sku:x.sku,title:x.title,purpose:x.description,functions:[],function_status:'UNAUTHORED',item_version:x.version}:view==='readiness'?{sku:x.sku,content_status:x.status,approved_challenge_mapping:'NOT_LOCATED',playable_content:false,review_status:'HOLD'}:view==='commerce'?{sku:x.sku,price_cents:x.price_cents,currency:x.currency,store_live_state:'NOT_FRESHLY_VERIFIED',checkout:'HOLD',price_change_status:'PROPOSAL_ONLY'}:{sku:x.sku,item_version:x.version,source_sha256:inventory.source_hashes[Number(x.sku.slice(6))<=50?'001-050':'051-500'],lineage:'SUPPLIED_CATALOG_BYTES',approval:'NOT_ESTABLISHED'});
return json({schema:inventory.schema,view,count:rows.length,source_hashes:inventory.source_hashes,records:rows});}
if(req.method==='POST'&&u.pathname==='/proposals'){
if(typeof env.ADMIN_TOKEN!=='string'||env.ADMIN_TOKEN.length<32)return json({error:'authentication_unconfigured'},503);
if(req.headers.get('Authorization')!==`Bearer ${env.ADMIN_TOKEN}`)return json({error:'unauthorized'},401);
const text=await req.text();if(text.length>8192)return json({error:'body_too_large'},413);let b;try{b=JSON.parse(text)}catch{return json({error:'invalid_json'},400)}
if(!b||canonical(Object.keys(b).sort())!==canonical(['basis','changes','expected_source_sha256','sku']))return json({error:'invalid_proposal'},400);
const original=inventory.records.find(x=>x.sku===b.sku);if(!original)return json({error:'unknown_sku'},404);
const expected=inventory.source_hashes[Number(b.sku.slice(6))<=50?'001-050':'051-500'];if(b.expected_source_sha256!==expected)return json({error:'stale_catalog'},409);
if(typeof b.basis!=='string'||!b.basis||b.basis.length>1000||!b.changes||Array.isArray(b.changes))return json({error:'invalid_proposal'},400);
const keys=Object.keys(b.changes);if(!keys.length||keys.some(k=>!['title','purpose','functions','price_cents'].includes(k)))return json({error:'invalid_fields'},400);
if(('title'in b.changes&&(typeof b.changes.title!=='string'||!b.changes.title.trim()||b.changes.title.length>160))||('purpose'in b.changes&&(typeof b.changes.purpose!=='string'||!b.changes.purpose.trim()||b.changes.purpose.length>1000))||('price_cents'in b.changes&&(!Number.isSafeInteger(b.changes.price_cents)||b.changes.price_cents<1))||('functions'in b.changes&&(!Array.isArray(b.changes.functions)||b.changes.functions.length>20||b.changes.functions.some(v=>typeof v!=='string'||v.length>160))))return json({error:'invalid_values'},400);
const event={schema:'wisdom-catalog-proposal/1',id:crypto.randomUUID(),created_at:new Date().toISOString(),actor:'authorized-test-curator',sku:b.sku,previous:original,source_sha256:expected,proposed_changes:b.changes,basis:b.basis,status:'PROPOSED',approval:null,applied:false,commerce:'UNCHANGED'};const sha=await digest(canonical(event));await env.DB.prepare('INSERT INTO catalog_events(id,sku,event_json,event_sha256) VALUES(?,?,?,?)').bind(event.id,b.sku,canonical(event),sha).run();return json({receipt:event,event_sha256:sha},201);}
return json({error:'not_found'},404);
}catch{return json({error:'internal_error'},500)}}};
