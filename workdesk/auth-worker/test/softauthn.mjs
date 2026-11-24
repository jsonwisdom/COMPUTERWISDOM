// Synthetic software WebAuthn authenticator for tests only. Keys are generated in-process
// and discarded; no real YubiKey, no exported hardware key, no persistent secret.
import {generateKeyPairSync, createHash, sign, randomBytes} from 'node:crypto';
const b64u = b => Buffer.from(b).toString('base64url');
const sha = b => createHash('sha256').update(b).digest();
function cbor(v) {
 const head=(major,n)=>{
  if(n<24)return Buffer.from([major<<5|n]);
  if(n<256)return Buffer.from([major<<5|24,n]);
  if(n<65536){const b=Buffer.alloc(3);b[0]=major<<5|25;b.writeUInt16BE(n,1);return b;}
  const b=Buffer.alloc(5);b[0]=major<<5|26;b.writeUInt32BE(n,1);return b;
 };
 if(typeof v==='number')return v>=0?head(0,v):head(1,-1-v);
 if(typeof v==='string'){const s=Buffer.from(v,'utf8');return Buffer.concat([head(3,s.length),s]);}
 if(Buffer.isBuffer(v)||v instanceof Uint8Array){return Buffer.concat([head(2,v.length),Buffer.from(v)]);}
 if(v instanceof Map){const parts=[head(5,v.size)];for(const [k,x] of v){parts.push(cbor(k),cbor(x));}return Buffer.concat(parts);}
 throw Error('cbor type');
}
export class SoftAuthenticator {
 constructor(name,{aaguid}={}) {
  this.name=name;
  const {privateKey,publicKey}=generateKeyPairSync('ec',{namedCurve:'P-256'});
  this.privateKey=privateKey; this.jwk=publicKey.export({format:'jwk'});
  this.credentialId=randomBytes(32);
  this.aaguid=aaguid||randomBytes(16);
  this.counter=0;
 }
 get id(){return b64u(this.credentialId);}
 authData(rpId,flags,counter,attested) {
  const c=Buffer.alloc(4);c.writeUInt32BE(counter>>>0);
  const parts=[sha(Buffer.from(rpId)),Buffer.from([flags]),c];
  if(attested){
   const len=Buffer.alloc(2);len.writeUInt16BE(this.credentialId.length);
   const cose=cbor(new Map([[1,2],[3,-7],[-1,1],[-2,Buffer.from(this.jwk.x,'base64url')],[-3,Buffer.from(this.jwk.y,'base64url')]]));
   parts.push(this.aaguid,len,this.credentialId,cose);
  }
  return Buffer.concat(parts);
 }
 // navigator.credentials.create() equivalent, serialized like PublicKeyCredential.toJSON().
 create(options,{origin,uv=true}={}) {
  const clientDataJSON=Buffer.from(JSON.stringify({type:'webauthn.create',challenge:options.challenge,origin,crossOrigin:false}));
  const authData=this.authData(options.rp.id,0x01|(uv?0x04:0)|0x40,this.counter,true);
  const attestationObject=cbor(new Map([['fmt','none'],['attStmt',new Map()],['authData',authData]]));
  return {id:this.id,rawId:this.id,type:'public-key',clientExtensionResults:{},authenticatorAttachment:'cross-platform',
   response:{clientDataJSON:b64u(clientDataJSON),attestationObject:b64u(attestationObject),transports:['usb','nfc']}};
 }
 // navigator.credentials.get() equivalent. Options let tests forge or corrupt assertions.
 get(options,{origin,rpId:rpIdOverride,uv=true,counter,signWith,asId}={}) {
  if(counter===undefined)counter=++this.counter;
  const clientDataJSON=Buffer.from(JSON.stringify({type:'webauthn.get',challenge:options.challenge,origin,crossOrigin:false}));
  const authenticatorData=this.authData(rpIdOverride||options.rpId,0x01|(uv?0x04:0),counter,false);
  const signature=sign('sha256',Buffer.concat([authenticatorData,sha(clientDataJSON)]),{key:(signWith||this).privateKey,dsaEncoding:'der'});
  const id=asId||this.id;
  return {id,rawId:id,type:'public-key',clientExtensionResults:{},authenticatorAttachment:'cross-platform',
   response:{clientDataJSON:b64u(clientDataJSON),authenticatorData:b64u(authenticatorData),signature:b64u(signature),userHandle:b64u(Buffer.from('jason-workdesk-owner'))}};
 }
}
