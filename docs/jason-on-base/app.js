/* Jason on Base teaching replay v0.1. NO network collection. NO wallet API. */
(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const entries = [];
  const sources = Object.freeze({
    ushmm: {title:"USHMM: German civilians at Buchenwald, April 1945",
      url:"https://encyclopedia.ushmm.org/content/en/film/german-civilians-forced-to-view-atrocities-committed-in-buchenwald",
      text:"April 1945 film preserved by the US Holocaust Memorial Museum. Historic film may contain disturbing material."},
    loc: {title:"Library of Congress: National Screening Room",
      url:"https://www.loc.gov/programs/national-film-preservation-board/film-registry/watch-films-on-the-national-film-registry/",
      text:"A gateway to historical films. Select a specific film on the Library site; streaming and download permissions vary."},
    cia: {title:"CIA: History of CIA and OSS",
      url:"https://www.cia.gov/legacy/cia-history",
      text:"Reading source, not a film. OSS dates to 1942; CIA was created in September 1947."}
  });
  let localFileObjectUrl = null;
  const film = $("film"), player = $("local-player");
  const setSource = () => {
    const chosen = sources[film.value] || sources.ushmm;
    $("film-context").textContent = chosen.text;
    $("film-link").href = chosen.url;
  };
  film.addEventListener("change",setSource);
  setSource();
  $("local-film").addEventListener("change",event => {
    if(localFileObjectUrl){ URL.revokeObjectURL(localFileObjectUrl); localFileObjectUrl=null; }
    const file = event.target.files && event.target.files[0];
    if(!file){ player.removeAttribute("src"); player.hidden=true; return; }
    if(!file.type.startsWith("video/")){
      $("marker-feedback").textContent="Select a local video file.";
      event.target.value="";
      return;
    }
    localFileObjectUrl = URL.createObjectURL(file);
    player.src = localFileObjectUrl;
    player.hidden = false;
  });
  function parseManualTime(value){
    if(!value.trim())return null;
    const parts = value.trim().split(":");
    if(!(parts.length===2||parts.length===3) || !parts.every(x=>/^\d+$/.test(x)))throw Error("Movie time must be MM:SS or HH:MM:SS.");
    const nums=parts.map(Number);
    if(nums.some(n=>!Number.isSafeInteger(n)))throw Error("Movie time is too large.");
    if(nums[nums.length-1]>=60 || (parts.length===3&&nums[1]>=60))throw Error("Seconds and minutes must be below 60.");
    const valueSeconds=nums.reduce((sum,n)=>sum*60+n,0);
    if(valueSeconds>86400)throw Error("Movie time must be within 24 hours.");
    return valueSeconds;
  }
  function render(){
    const holder=$("entries");
    holder.replaceChildren();
    if(!entries.length){
      const p=document.createElement("p");p.className="small";p.textContent="No reflections yet.";holder.appendChild(p);
    }
    entries.slice().reverse().forEach((entry,i)=>{
      const d=document.createElement("div");d.className="record";
      const heading=document.createElement("b");heading.textContent="#" + (entries.length-i) + " · I DIDN'T KNOW · " + entry.scene_id;d.appendChild(heading);
      const meta=document.createElement("div");meta.className="small";
      meta.textContent="Local record: " + entry.recorded_at_utc + " · Film time: " + (entry.movie_timestamp_seconds===null?"not specified":entry.movie_timestamp_seconds+"s");
      d.appendChild(meta);
      if(entry.user_note){const p=document.createElement("p");p.textContent=entry.user_note;d.appendChild(p);}
      holder.appendChild(d);
    });
    $("export").disabled=!entries.length;
    $("clear").disabled=!entries.length;
  }
  $("didnt-know").addEventListener("click",()=>{
    const status=$("marker-feedback");
    let timestamp=null;
    try { timestamp=parseManualTime($("film-time").value); }
    catch(err){ status.textContent=err.message; return; }
    const source=sources[film.value]||sources.ushmm;
    if(localFileObjectUrl && Number.isFinite(player.currentTime) && player.readyState>=1){
      timestamp=Math.floor(player.currentTime);
    }
    const scene=$("scene").value.trim();
    if(!scene){status.textContent="Add a scene or chapter label first.";return;}
    const id=(typeof crypto!=="undefined"&&crypto.randomUUID)?crypto.randomUUID():("local-"+Date.now()+"-"+entries.length);
    const record={
      schema:"JASON_ON_BASE_PRIVATE_REFLECTION_V0_1",
      local_event_id:id,
      source_title:localFileObjectUrl?"Local film, user supplied and source unverified":source.title,
      film_reference:localFileObjectUrl?"LOCAL_VIDEO_USER_SUPPLIED_UNVERIFIED":source.url,
      selected_research_reference:source.url,
      source_identity_verified:false,
      scene_id:scene,
      movie_timestamp_seconds:timestamp,
      recorded_at_utc:new Date().toISOString(),
      response:"I_DIDNT_KNOW",
      user_note:$("note").value.trim()||null,
      provenance_state:"USER_REFLECTION_ONLY_NOT_HISTORICAL_PROOF",
      recorded_on_server:false,
      location_collected:false
    };
    entries.push(record);
    $("note").value="";
    status.textContent="Saved locally in this page only. No one else has received it.";
    render();
  });
  $("export").addEventListener("click",()=>{
    if(!entries.length)return;
    const payload={
      schema:"JASON_ON_BASE_PERSONAL_REPLAY_EXPORT_V0_1",
      exported_at_utc:new Date().toISOString(),
      collection_scope:"THIS_BROWSER_PAGE_SESSION_ONLY",
      events:entries.slice(),
      warning:"Private user annotations, not certified historical facts, demographic observations or evidence of other viewers."
    };
    const blob=new Blob([JSON.stringify(payload,null,2)+"\n"],{type:"application/json"});
    const link=document.createElement("a");
    const url=URL.createObjectURL(blob);
    link.href=url;
    link.download="jason-on-base-my-private-replay.json";
    document.body.appendChild(link);
    link.click();
    link.remove();
    requestAnimationFrame(()=>requestAnimationFrame(()=>URL.revokeObjectURL(url)));
    $("marker-feedback").textContent="Personal JSON export requested. Nothing was sent to this site.";
  });
  $("clear").addEventListener("click",()=>{
    entries.length=0;
    render();
    $("marker-feedback").textContent="This page's reflection records were erased.";
  });

  // Public-source registry only; user questions are never sent in requests.
  let librarianRecords=null;
  const librarianHolder=$("librarian-results");
  const librarianStatus=$("librarian-status");
  const lNode=(tag,content,cls)=>{
    const node=document.createElement(tag);
    if(content!==undefined)node.textContent=content;
    if(cls)node.className=cls;
    return node;
  };
  function sourceItem(entry,includeClaim){
    const box=lNode("div",undefined,"record");
    box.appendChild(lNode("b",entry.title));
    box.appendChild(lNode("p",entry.organization+" · "+entry.category+" · "+entry.temporal_scope,"small"));
    if(includeClaim)box.appendChild(lNode("p",entry.claim));
    const link=lNode("a","Open original source ↗");
    link.href=entry.source;link.target="_blank";link.rel="noopener noreferrer";
    box.appendChild(link);
    box.appendChild(lNode("p","Scope limit: "+entry.not_a_claim,"small"));
    return box;
  }
  async function loadLibrarian(){
    try {
      const response=await fetch("librarian-v0.1.json",{cache:"no-store"});
      if(!response.ok)throw Error("Public-source registry HTTP "+response.status);
      const body=await response.json();
      if(body.schema!=="JASON_ON_BASE_LIBRARIAN_INDEX_V0_1"||!Array.isArray(body.records))throw Error("Librarian registry schema invalid");
      librarianRecords=body.records;
      librarianStatus.textContent="Static registry loaded: "+librarianRecords.length+" public source pointers. Completeness and freshness NOT verified.";
    }catch(err){ librarianRecords=null; librarianStatus.textContent="HOLD: "+err.message+"; no source claims loaded."; }
  }
  $("ask-librarian").addEventListener("click",()=>{
    librarianHolder.replaceChildren();
    if(!librarianRecords){librarianHolder.appendChild(lNode("p","HOLD: source registry unavailable."));return;}
    const q=$("librarian-question").value.trim().toLowerCase();
    if(!q){librarianHolder.appendChild(lNode("p","Type a question first."));return;}
    const words=q.split(/[^a-z0-9]+/).filter(w=>w.length>2);
    const ranked=librarianRecords.map(entry=>{
      const keywords=(entry.keywords||[]).join(" ").toLowerCase();
      const hay=(entry.title+" "+keywords+" "+entry.category).toLowerCase();
      return {entry,score:words.reduce((s,w)=>s+(hay.includes(w)?1:0),0)};
    }).filter(v=>v.score>0).sort((a,b)=>b.score-a.score).slice(0,6);
    if(!ranked.length){
      librarianHolder.appendChild(lNode("p","HOLD: no matching curated source in this registry. That does not prove no such records exist."));
      return;
    }
    ranked.forEach(({entry})=>librarianHolder.appendChild(sourceItem(entry,true)));
    librarianHolder.appendChild(lNode("p","This is keyword retrieval, NOT AI reasoning, fact-checking or comprehensive archival search.","small"));
  });
  $("daily-brief").addEventListener("click",()=>{
    librarianHolder.replaceChildren();
    if(!librarianRecords){librarianHolder.appendChild(lNode("p","HOLD: source registry unavailable."));return;}
    librarianHolder.appendChild(lNode("b","SAMPLE DAILY STUDY CARD — NOT CURRENT NEWS"));
    librarianHolder.appendChild(lNode("p","Today's actual content has not been collected, checked or released. Here are curated sources that can be studied at any time."));
    librarianRecords.slice(0,3).forEach(entry=>librarianHolder.appendChild(sourceItem(entry,false)));
    librarianHolder.appendChild(lNode("p","DAILY_PUBLIC_BRIEF=NOT_LIVE; SOURCE_FRESHNESS=NOT_VERIFIED; HUMAN_RELEASE=HOLD.","small"));
  });
  loadLibrarian();

  // Supreme Seymour: a deterministic local evidence organizer, not a legal AI adviser.
  // All private case content stays in page memory until user initiates an export.
  let seymourPacket=null;
  const seymourHolder=$("seymour-results");
  const seymourStatus=$("seymour-status");
  function renderSeymour(){
    seymourHolder.replaceChildren();
    $("seymour-export").disabled=!seymourPacket;
    if(!seymourPacket){
      seymourHolder.appendChild(lNode("p","No case loaded. V1 Distinctions → V2 Hidden coupling → V3 Collision → V4 Resolution attempts.","small"));
      return;
    }
    seymourHolder.appendChild(lNode("b","CASE "+seymourPacket.case_id+" · HOLD"));
    seymourHolder.appendChild(lNode("p","Question (user-reported): "+seymourPacket.question));
    seymourHolder.appendChild(lNode("p","Jurisdiction: "+seymourPacket.jurisdiction+" · Unknowns remain unresolved.","small"));
    const steps=[
      ["V1 Distinctions","The supplied question is not a verified fact. Confirm actors, alleged act, object and date with evidence."],
      ["V2 Hidden coupling","Check that names, accounts, institutions, dates and propositions have not been improperly merged."],
      ["V3 Collisions","Search for independent contrary records. One pointer cannot prove no contradiction exists."],
      ["V4 Resolution attempts","Identify legal scope and primary authority, authenticate originals and preserve competing interpretations for human review."]
    ];
    steps.forEach(([heading,detail])=>{
      const panel=lNode("div",undefined,"record");
      panel.appendChild(lNode("b",heading));
      panel.appendChild(lNode("p",detail,"small"));
      seymourHolder.appendChild(panel);
    });
    if(seymourPacket.source_url){
      const link=lNode("a","User-supplied source pointer (NOT VERIFIED) ↗");
      link.href=seymourPacket.source_url;link.target="_blank";link.rel="noopener noreferrer";
      seymourHolder.appendChild(link);
    }
    seymourHolder.appendChild(lNode("p","OUTPUT=HOLD · LEGAL_ADVICE=FALSE · CASE_OUTCOME=UNKNOWN · COURT_ADMISSIBILITY=NOT_ASSESSED · HUMAN_REVIEW=REQUIRED.","small"));
  }
  $("seymour-assess").addEventListener("click",()=>{
    const question=$("justice-question").value.trim();
    if(!question){seymourStatus.textContent="Enter a single claim or evidence question first.";return;}
    const jurisdiction=$("justice-jurisdiction").value.trim()||"UNKNOWN";
    const pointer=$("justice-source").value.trim();
    if(pointer){
      try {
        const u=new URL(pointer);
        if(!["https:","http:"].includes(u.protocol))throw Error("Not HTTP URL");
      }catch(err){seymourStatus.textContent="Use an HTTP(S) evidence URL or leave the field blank.";return;}
    }
    const now=new Date().toISOString();
    const id=(typeof crypto!=="undefined"&&crypto.randomUUID)?crypto.randomUUID():("user-"+Date.now());
    // A fresh note is intentional; previous notes must be exported if they matter.
    seymourPacket={
      schema:"JASON_ON_BASE_SEYMOUR_CASE_NOTE_V0_1",
      case_id:id,created_at_utc:now,question:question,jurisdiction:jurisdiction,
      source_url:pointer||null,source_class:"USER_REPORTED",
      evidence_inspected:false,source_hash_recomputed:false,
      counterevidence_checked:false,applicable_law_verified:false,
      provenance:"USER_ENTERED_NOT_AUTHENTICATED",
      steps:["V1_DISTINCTIONS","V2_HIDDEN_COUPLING","V3_COLLISION_CHECK_REQUIRED","V4_RESOLUTION_ATTEMPTS_ONLY"],
      case_state:"HOLD",human_decision_status:"NOT_PROVIDED",
      court_admissibility:"NOT_ASSESSED",lawyer_review:false,
      legal_protection_guarantee:false,authority_created:false
    };
    renderSeymour();
    seymourStatus.textContent="Case question organized locally. No legal research, court action, verification, or advice performed.";
  });
  $("seymour-export").addEventListener("click",()=>{
    if(!seymourPacket)return;
    const output=JSON.stringify(seymourPacket,null,2)+"\n";
    const url=URL.createObjectURL(new Blob([output],{type:"application/json"}));
    const link=document.createElement("a");
    link.href=url;link.download="seymour-private-case-hold.json";
    document.body.appendChild(link);link.click();link.remove();
    requestAnimationFrame(()=>requestAnimationFrame(()=>URL.revokeObjectURL(url)));
    seymourStatus.textContent="Private HOLD case packet export requested. No network upload.";
  });
  $("seymour-import").addEventListener("change",async event=>{
    const file=event.target.files && event.target.files[0];
    if(!file)return;
    if(file.size>100000){seymourStatus.textContent="File exceeds 100 KB import limit.";event.target.value="";return;}
    try{
      const candidate=JSON.parse(await file.text());
      if(!candidate||candidate.schema!=="JASON_ON_BASE_SEYMOUR_CASE_NOTE_V0_1" ||
         typeof candidate.question!=="string" || candidate.question.length>1200 ||
         typeof candidate.jurisdiction!=="string" || candidate.jurisdiction.length>100 ||
         typeof candidate.case_id!=="string" || candidate.case_id.length>150){
         throw Error("Case packet schema or field length invalid.");
      }
      if(candidate.source_url!==null && candidate.source_url!==undefined){
        const u=new URL(candidate.source_url);
        if(!["http:","https:"].includes(u.protocol))throw Error("Invalid source URL.");
      }
      // Never inherit claims of verification, verdict, privilege or authority from
      // uploaded content, even if the file falsely contains such fields.
      seymourPacket={
        schema:"JASON_ON_BASE_SEYMOUR_CASE_NOTE_V0_1",
        case_id:candidate.case_id,
        created_at_utc:typeof candidate.created_at_utc==="string"?candidate.created_at_utc:"UNKNOWN",
        question:candidate.question,jurisdiction:candidate.jurisdiction,
        source_url:candidate.source_url||null,
        source_class:"USER_REPORTED",
        evidence_inspected:false,source_hash_recomputed:false,
        counterevidence_checked:false,applicable_law_verified:false,
        provenance:"IMPORTED_USER_FILE_NOT_AUTHENTICATED",
        steps:["V1_DISTINCTIONS","V2_HIDDEN_COUPLING","V3_COLLISION_CHECK_REQUIRED","V4_RESOLUTION_ATTEMPTS_ONLY"],
        case_state:"HOLD",human_decision_status:"NOT_PROVIDED",court_admissibility:"NOT_ASSESSED",
        lawyer_review:false,legal_protection_guarantee:false,authority_created:false
      };
      seymourStatus.textContent="User packet reloaded as HOLD; the import did not verify its claims.";
      renderSeymour();
    }catch(err){seymourStatus.textContent="HOLD: "+err.message;}
    event.target.value="";
  });
  const setView = mode=>{
    if(!["boomer","arcade","evidence"].includes(mode))return;
    document.body.dataset.view=mode;
    ["boomer","arcade","evidence"].forEach(v=>{
      const button=$("view-"+v);
      const active=v===mode;
      button.setAttribute("aria-pressed",String(active));
      button.classList.toggle("secondary",!active);
    });
  };
  ["boomer","arcade","evidence"].forEach(mode=>{
    $("view-"+mode).addEventListener("click",()=>setView(mode));
  });
  const setLevel=()=>{
    const level=Math.max(0,Math.min(8,Number($("level").value)||0));
    $("qout").textContent="LEVEL " + level + " → " + (level*level) + " virtual quarters · $0 charged · 0 prize entries";
  };
  $("level").addEventListener("input",setLevel);
  setLevel();
  window.addEventListener("pagehide",()=>{
    if(localFileObjectUrl){ URL.revokeObjectURL(localFileObjectUrl);localFileObjectUrl=null; }
  });
})();