/* Jason on Base: consent-only Coinbase Wallet connection + Matrix Sentinel.
   RPC ALLOWLIST: eth_requestAccounts (user click), eth_chainId (network read).
   No signing, sends, approval, balance history, payments, telemetry, or persistence. */
(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const connectButton=$("coinbase-connect");
  const disconnectButton=$("coinbase-disconnect");
  const message=$("wallet-status");
  const accountLabel=$("wallet-account");
  const chainLabel=$("wallet-chain");
  const matrix=$("clawback-matrix");
  const matrixText=$("clawback-quote");
  const levelControl=$("level");
  const discovered=[];
  let selected=null;
  let account=null;
  let chain=null;
  let generation=0;

  function isCoinbase(detail){
    if (!detail || !detail.provider || typeof detail.provider.request!=="function") return false;
    const id=String(detail.info && detail.info.rdns || "").toLowerCase();
    const name=String(detail.info && detail.info.name || "").toLowerCase();
    return detail.provider.isCoinbaseWallet===true ||
      (["com.coinbase.wallet","com.coinbase","org.base"].includes(id) && (name.includes("coinbase") || name.includes("base")));
  }
  function onAnnouncement(event){
    const detail=event && event.detail;
    if(isCoinbase(detail) && !discovered.some(x=>x.provider===detail.provider)){
      discovered.push(detail);
    }
  }
  window.addEventListener("eip6963:announceProvider",onAnnouncement);
  function announceRequest(){
    if(typeof Event==="function"){
      window.dispatchEvent(new Event("eip6963:requestProvider"));
    }
  }
  announceRequest();

  function providerPick(){
    if(discovered.length) return discovered[0].provider;
    const ev=window.ethereum;
    if(ev && Array.isArray(ev.providers)){
      return ev.providers.find(p=>p && p.isCoinbaseWallet===true && typeof p.request==="function") || null;
    }
    return ev && ev.isCoinbaseWallet===true && typeof ev.request==="function" ? ev : null;
  }
  function shorten(s){
    return s.slice(0,6)+"…"+s.slice(-4);
  }
  function formatChain(s){
    if(s==="0x2105") return "Base Mainnet · 8453";
    if(s==="0x1") return "Ethereum Mainnet · 1";
    if(s==="0x14a34") return "Base Sepolia · 84532";
    return /^0x[0-9a-f]+$/i.test(s||"") ? "Other EVM network · "+s : "Unknown network";
  }
  function render(){
    const has=Boolean(account && selected);
    accountLabel.textContent=has ? shorten(account) : "Not connected";
    chainLabel.textContent=has ? formatChain(chain) : "No network requested";
    connectButton.disabled=has;
    disconnectButton.disabled=!has;
    $("wallet-boundary").textContent=has
      ? "Address displayed in this page only. Public on-chain account activity may be discoverable elsewhere. No asset history or balances retrieved."
      : "Nothing linked. No RPC permission request until you click Connect.";
  }
  function removeListeners(){
    if(selected && typeof selected.removeListener==="function"){
      selected.removeListener("accountsChanged",onAccounts);
      selected.removeListener("chainChanged",onChain);
      selected.removeListener("disconnect",onDisconnect);
    }
  }
  function clearSession(text){
    generation++;
    removeListeners();
    selected=null;
    account=null;
    chain=null;
    message.textContent=text;
    render();
  }
  function onAccounts(accounts){
    const a=Array.isArray(accounts)?accounts[0]:null;
    if(!a || !/^0x[0-9a-fA-F]{40}$/.test(a)){
      clearSession("Wallet reports no permitted account. Local view disconnected.");
      return;
    }
    account=a;
    message.textContent="Wallet account changed. Still read-only; no transactions enabled.";
    render();
  }
  function onChain(s){
    chain=typeof s==="string" ? s.toLowerCase() : "";
    message.textContent=chain==="0x2105"
      ? "Connected to Base Mainnet. No signing or payments enabled."
      : "Connected on a non-Base or unknown network. No auto-switch, signing, or payment.";
    render();
  }
  function onDisconnect(){
    clearSession("Wallet provider disconnected. No local connection remains.");
  }
  connectButton.addEventListener("click",async ()=>{
    if(selected)return;
    announceRequest();
    const provider=providerPick();
    if(!provider){
      message.textContent="Coinbase Wallet provider not detected. Open this page in the Coinbase Wallet/Base app's built-in browser, or use its desktop extension. Ordinary Safari has no built-in wallet provider; mobile QR pairing is not included in this first version.";
      return;
    }
    const ticket=++generation;
    connectButton.disabled=true;
    message.textContent="Requesting account access in your wallet. You may reject it.";
    try{
      const accounts=await provider.request({method:"eth_requestAccounts"});
      if(ticket!==generation)return;
      const first=Array.isArray(accounts)?accounts[0]:null;
      if(typeof first!=="string" || !/^0x[0-9a-fA-F]{40}$/.test(first))throw Error("Wallet did not return a valid EVM account.");
      let network="";
      try{
        const value=await provider.request({method:"eth_chainId"});
        if(typeof value==="string")network=value.toLowerCase();
      }catch(e){network="";}
      if(ticket!==generation)return;
      selected=provider;
      account=first;
      chain=network;
      if(typeof selected.on==="function"){
        selected.on("accountsChanged",onAccounts);
        selected.on("chainChanged",onChain);
        selected.on("disconnect",onDisconnect);
      }
      message.textContent=chain==="0x2105"
        ? "Coinbase-style provider connected on Base. Account permission only."
        : "Coinbase-style provider connected. Network is not confirmed as Base; no network switch attempted.";
      render();
    }catch(e){
      if(ticket!==generation)return;
      account=null;chain=null;selected=null;
      message.textContent=e && e.code===4001
        ? "You rejected the account permission. No wallet linked."
        : "Connection not completed. No wallet linked or payment made.";
      render();
    }finally{
      if(ticket===generation)connectButton.disabled=Boolean(selected);
    }
  });
  disconnectButton.addEventListener("click",()=>{
    clearSession("Local session cleared. Wallet permissions may remain in wallet settings; revoke access in the wallet if desired.");
  });
  function renderMatrix(){
    const level=Math.max(0,Math.min(8,Number(levelControl.value)||0));
    const virtualQuarters=level*level;
    matrix.replaceChildren();
    for(let r=0;r<8;r++){
      const line=document.createElement("div");
      line.className="matrix-row";
      for(let c=0;c<8;c++){
        const pixel=document.createElement("span");
        pixel.className="matrix-pixel"+(r*8+c<virtualQuarters?" lit":"");
        pixel.setAttribute("aria-hidden","true");
        line.appendChild(pixel);
      }
      matrix.appendChild(line);
    }
    matrixText.textContent="LEVEL "+level+" · "+virtualQuarters+" VIRTUAL QUARTERS · REAL CHARGE $0.00 · QUOTE ONLY / HOLD";
    matrix.setAttribute("aria-label",virtualQuarters+" of 64 learning indicators illuminated");
  }
  levelControl.addEventListener("input",renderMatrix);
  renderMatrix();
  render();
})();