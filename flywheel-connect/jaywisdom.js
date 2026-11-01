'use strict';
(() => {
  const ORIGIN='https://wallet.jsonwisdom.com';
  const EXPECTED='0xa380552a27b0a5a2874ea7aa52cac09f542002e8';
  const CHAIN=8453, BASE='0x2105';
  const DOMAIN=Object.freeze({
    name:'CoinBaseKid JayWisdom Wallet Control',version:'1',chainId:8453,
    salt:'0xad2e9ab938f28c9491eca2dac2aa2e30322e9d71f71d8ba98f7de67cd2f3c0da'
  });
  const PURPOSE='Prove current control of jaywisdom.base.eth account on Base ONLY';
  const POLICY='OFFCHAIN_CONTROL_ONLY; NO_PAYMENT; NO_TOKEN_APPROVAL; NO_LOGIN; NO_REPUTATION_CERTIFICATION; NO_GITHUB_WRITE; NO_X402_AUTHORIZATION';
  const FIELDS=[
    {name:'origin',type:'string'},{name:'account',type:'address'},
    {name:'basename',type:'string'},{name:'purpose',type:'string'},
    {name:'nonce',type:'bytes32'},{name:'issuedAt',type:'uint256'},
    {name:'expiresAt',type:'uint256'},{name:'policy',type:'string'}
  ];
  const DOMAIN_FIELDS=[
    {name:'name',type:'string'},{name:'version',type:'string'},
    {name:'chainId',type:'uint256'},{name:'salt',type:'bytes32'}
  ];
  const $=id=>document.getElementById(id);
  const connectButton=$('connect'),signButton=$('sign'),notice=$('notice');
  const accountLabel=$('account'),preview=$('preview'),previewWrap=$('previewWrap');
  const proofHero=$('proofHero'),proofAddress=$('proofAddress'),proofMethod=$('proofMethod'),proofDigest=$('proofDigest');
  const index=$('index'),indexList=$('indexList'),indexStatus=$('indexStatus');
  const copyButton=$('copyReceipt'),receiptView=$('receiptView');
  const known=new Map();
  let provider=null,connection=null,challenge=null,busy=false,epoch=0,changes=0;
  let lastReceipt=null;
  const same=(a,b)=>String(a||'').toLowerCase()===String(b||'').toLowerCase();
  const err=e=>String(e?.message||e||'Unknown wallet error').slice(0,320);
  function message(s,kind=''){notice.textContent=s;notice.className='notice '+kind;}
  function reset(s='Disconnected. No signature requested.'){
    epoch++;connection=null;challenge=null;lastReceipt=null;proofHero.hidden=true;index.hidden=true;
    copyButton.hidden=true;receiptView.hidden=true;receiptView.textContent='';
    indexList.replaceChildren();indexStatus.textContent='Waiting for local proof.';
    signButton.disabled=true;signButton.hidden=true;previewWrap.hidden=true;
    preview.textContent='';accountLabel.textContent='';
    proofAddress.textContent='';proofMethod.textContent='';proofDigest.textContent='';
    message(s);
  }
  function onChange(){changes++;if(busy)return;reset('Wallet or network changed. Connect again.');}
  window.addEventListener('eip6963:announceProvider',event=>{
    if(event?.detail?.info?.uuid&&event.detail.provider?.request)
      known.set(event.detail.info.uuid,event.detail);
  });
  function announce(){
    if(typeof window.dispatchEvent==='function'&&typeof Event==='function')
      window.dispatchEvent(new Event('eip6963:requestProvider'));
  }
  function pickProvider(){
    const coinbase=[...known.values()].filter(d=>
      /coinbase/i.test(String(d.info?.rdns||'')+' '+String(d.info?.name||'')));
    if(coinbase.length===1)return coinbase[0].provider;
    if(coinbase.length>1)throw Error('Multiple Coinbase Wallet providers. Select one wallet in its app.');
    const injected=window.ethereum;
    const list=Array.isArray(injected?.providers)?injected.providers:(injected?[injected]:[]);
    const matching=list.filter(p=>p?.request&&p.isCoinbaseWallet===true);
    if(matching.length===1)return matching[0];
    if(matching.length>1)throw Error('Multiple Coinbase Wallet providers. Try its in-app browser.');
    if(list.length===1&&list[0]?.request)return list[0];
    throw Error('No wallet provider. Open this link in Coinbase Wallet’s in-app browser and retry. Never enter your recovery phrase here.');
  }
  async function addressOf(p){
    const a=await p.request({method:'eth_accounts'});
    if(!Array.isArray(a)||!/^0x[0-9a-fA-F]{40}$/.test(a[0]||''))throw Error('Wallet account unavailable.');
    return a[0];
  }
  async function chainOf(p){
    const id=await p.request({method:'eth_chainId'});
    const n=Number(BigInt(id));
    if(!Number.isSafeInteger(n))throw Error('Invalid chain ID');
    return n;
  }
  function freshChallenge(account){
    const bytes=crypto.getRandomValues(new Uint8Array(32));
    const nonce='0x'+Array.from(bytes,x=>x.toString(16).padStart(2,'0')).join('');
    const issuedAt=Math.floor(Date.now()/1000),expiresAt=issuedAt+300;
    const domain={...DOMAIN},types={JayWisdomControl:FIELDS};
    const msg={origin:ORIGIN,account,basename:'jaywisdom.base.eth',
      purpose:PURPOSE,nonce,issuedAt,expiresAt,policy:POLICY};
    const typedData={types:{EIP712Domain:DOMAIN_FIELDS,JayWisdomControl:FIELDS},
      primaryType:'JayWisdomControl',domain,message:msg};
    return {account,domain,types,message:msg,typedData,expiresAt};
  }
  async function connect(){
    if(busy)return;
    busy=true;reset('Connecting to Coinbase Wallet…');
    const attempt=epoch,initialChange=changes;
    connectButton.disabled=true;
    try{
      if(location.origin!==ORIGIN)throw Error('Wrong website origin. Only '+ORIGIN+' can issue this challenge.');
      announce();
      const next=pickProvider();
      if(provider!==next){
        provider?.removeListener?.('accountsChanged',onChange);
        provider?.removeListener?.('chainChanged',onChange);
        provider=next;
        provider.on?.('accountsChanged',onChange);
        provider.on?.('chainChanged',onChange);
      }
      const granted=await provider.request({method:'eth_requestAccounts'});
      if(!Array.isArray(granted)||!/^0x[0-9a-fA-F]{40}$/.test(granted[0]||''))
        throw Error('Wallet did not return an account.');
      if(!same(granted[0],EXPECTED))throw Error('Different wallet selected: '+granted[0]+'. Switch to @jaywisdom ('+EXPECTED.slice(0,8)+'…) and reconnect.');
      if(await chainOf(provider)!==CHAIN){
        message('Coinbase Wallet: approve switching to Base mainnet (8453)…');
        await provider.request({method:'wallet_switchEthereumChain',params:[{chainId:BASE}]});
      }
      const changeAfterSwitch=changes;
      const a1=await addressOf(provider),c1=await chainOf(provider);
      const a2=await addressOf(provider),c2=await chainOf(provider);
      if(attempt!==epoch||changes!==changeAfterSwitch||
        !same(a1,a2)||!same(a2,EXPECTED)||c1!==CHAIN||c2!==CHAIN)
        throw Error('Account or network changed while connecting. Reconnect.');
      connection={account:a2};
      challenge=freshChallenge(a2);
      accountLabel.textContent=a2;
      preview.textContent=JSON.stringify(challenge.typedData,null,2);
      previewWrap.hidden=false;signButton.hidden=false;signButton.disabled=false;
      message('Base 8453 connected. @jaywisdom matches. Tap SIGN to open your wallet approval. No gas or transfer.','ok');
    }catch(e){
      if(attempt===epoch){
        challenge=null;connection=null;signButton.hidden=true;signButton.disabled=true;
        message(e?.code===4001?'Connection declined. Nothing signed.':err(e),'bad');
      }
    }finally{busy=false;connectButton.disabled=false;}
  }
  async function verifySignature(p,proof,signature){
    if(!window.ethers?.TypedDataEncoder?.hash||!window.ethers?.verifyTypedData)
      throw Error('EIP-712 verification library unavailable. No proof established.');
    if(typeof signature!=='string'||!/^0x(?:[0-9a-fA-F]{2})+$/.test(signature))
      throw Error('Wallet returned an unsupported signature. No proof established.');
    const digest=window.ethers.TypedDataEncoder.hash(proof.domain,proof.types,proof.message);
    const code=await p.request({method:'eth_getCode',params:[proof.account,'latest']});
    if(typeof code!=='string'||!/^0x[0-9a-fA-F]*$/.test(code))
      throw Error('Unable to determine smart-account type; verification on HOLD.');
    if(code!=='0x'&&!/^0x0+$/.test(code)){
      // ERC-1271 verifies smart-wallet signatures; a signature is NOT EOA-only.
      const abi=new window.ethers.Interface(['function isValidSignature(bytes32,bytes) view returns (bytes4)']);
      const data=abi.encodeFunctionData('isValidSignature',[digest,signature]);
      const result=await p.request({method:'eth_call',params:[{to:proof.account,data},'latest']});
      let decoded;
      try{decoded=abi.decodeFunctionResult('isValidSignature',result)[0];}
      catch{throw Error('Smart wallet did not validate this signature (ERC-1271).');}
      if(String(decoded).toLowerCase()!=='0x1626ba7e')
        throw Error('Smart wallet rejected signature. No proof established.');
      return {digest,method:'ERC-1271 / BASE ETH_CALL'};
    }
    if(!/^0x[0-9a-fA-F]{130}$/.test(signature))
      throw Error('Undeployed or non-EOA signature unsupported here. No proof established.');
    const recovered=window.ethers.verifyTypedData(proof.domain,proof.types,proof.message,signature);
    if(!same(recovered,proof.account))throw Error('Signature does not recover @jaywisdom. Rejected.');
    return {digest,method:'EIP-712 / EOA RECOVERY'};
  }
  function addLayer(row,i){
    if(!row||typeof row.title!=='string'||typeof row.status!=='string'||
      typeof row.why!=='string'||typeof row.url!=='string')return;
    if(!/^https:\/\/(github\.com|basescan\.org|wallet\.jsonwisdom\.com)\//.test(row.url))return;
    const li=document.createElement('li');
    li.className='index-row';
    li.style.animationDelay=Math.min(i*100,800)+'ms';
    const badge=document.createElement('span');badge.className='state';badge.textContent=row.status;
    const link=document.createElement('a');link.href=row.url;link.target='_blank';link.rel='noopener noreferrer';link.textContent=row.title+' ↗';
    const why=document.createElement('p');why.textContent=row.why;
    li.append(badge,link,why);
    indexList.appendChild(li);
  }
  async function revealIndex(attempt){
    try{
      const response=await fetch('/recovery-index.json',{cache:'no-store',credentials:'omit'});
      if(!response.ok)throw Error('Index temporarily unavailable');
      const data=await response.json();
      if(epoch!==attempt)return;
      if(data?.schema!=='COINBASEKID_PUBLIC_RECOVERY_INDEX_V1'||
        !same(data?.basename_controller,EXPECTED)||!Array.isArray(data?.layers))
        throw Error('Index manifest failed identity check.');
      data.layers.forEach(addLayer);
      indexStatus.textContent='Public read-only GitHub evidence; each status has a reason. No private GitHub repositories unlocked.';
    }catch(e){
      if(epoch===attempt)indexStatus.textContent='Index unavailable: '+err(e)+'. Open the public GitHub repository manually.';
    }
  }
  async function sign(){
    if(busy||!connection||!challenge||signButton.disabled||!provider)return;
    busy=true;signButton.disabled=true;connectButton.disabled=true;
    const request=challenge;challenge=null;const attempt=epoch,wasChanged=changes;
    message('Opening the Coinbase Wallet signature popup…','');
    try{
      if(Math.floor(Date.now()/1000)>request.expiresAt)throw Error('Challenge expired. Connect again for a fresh nonce.');
      if(!same(request.account,EXPECTED)||request.domain.chainId!==CHAIN||
        request.domain.salt!==DOMAIN.salt||request.message.origin!==location.origin||
        request.message.account!==request.account||request.message.policy!==POLICY)
        throw Error('Domain or account mismatch. Signature blocked.');
      if(!same(await addressOf(provider),EXPECTED)||await chainOf(provider)!==CHAIN)
        throw Error('Wallet account/network changed before signing.');
      const signature=await provider.request({method:'eth_signTypedData_v4',
        params:[request.account,JSON.stringify(request.typedData)]});
      const proof=await verifySignature(provider,request,signature);
      const first=await addressOf(provider),network1=await chainOf(provider);
      const second=await addressOf(provider),network2=await chainOf(provider);
      if(epoch!==attempt||changes!==wasChanged||!same(first,second)||
        !same(second,EXPECTED)||network1!==CHAIN||network2!==CHAIN||
        Math.floor(Date.now()/1000)>request.expiresAt)
        throw Error('Account, network or challenge changed. No verified proof.');
      proofAddress.textContent=EXPECTED;proofMethod.textContent=proof.method;
      proofDigest.textContent=proof.digest;
      lastReceipt={
        schema:'COINBASEKID_JAYWISDOM_LOCAL_SIGNED_RECEIPT_V1',
        claimed_basename:'jaywisdom.base.eth',account:EXPECTED,
        chain_id:CHAIN,verification_method:proof.method,
        typed_data:request.typedData,signature,typed_data_digest:proof.digest,
        locally_verified_at:new Date().toISOString(),
        backend_witnessed:false,issuer_nonce_confirmed:false,
        identity_certified:false,reputation_certified:false,
        export_approved:false,payment_authority:false,
        note:'Copied manually by wallet user if desired. A self-reported local receipt is not independently time-attested or globally replay-proof.'
      };
      copyButton.hidden=false;receiptView.hidden=false;
      receiptView.textContent=JSON.stringify(lastReceipt,null,2);
      proofHero.hidden=false;index.hidden=false;
      message('Locally verified. Your public evidence index is open below. No funds moved.','ok');
      await revealIndex(attempt);
      if(epoch===attempt&&typeof proofHero.scrollIntoView==='function')
        proofHero.scrollIntoView({behavior:'smooth',block:'start'});
    }catch(e){
      if(epoch===attempt){
        proofHero.hidden=true;index.hidden=true;
        message(e?.code===4001?'You declined the signature. No proof or payment.':err(e),'bad');
      }
    }finally{busy=false;connectButton.disabled=false;signButton.disabled=true;}
  }
  connectButton.addEventListener('click',connect);
  signButton.addEventListener('click',sign);
  copyButton.addEventListener('click',async()=>{
    if(!lastReceipt)return;
    try{
      if(!navigator?.clipboard?.writeText)throw Error('Clipboard unavailable');
      await navigator.clipboard.writeText(JSON.stringify(lastReceipt,null,2));
      message('Signed receipt copied. Share it only if you choose; GitHub remains unchanged.','ok');
    }catch(e){message('Clipboard unavailable. Select the visible receipt text to copy it manually.','bad');}
  });
  announce();
})();
