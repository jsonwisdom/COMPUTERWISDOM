/* Six light public-safe family learning pages. No persistence/network/identity proof. */
(()=>{"use strict";
const $=id=>document.getElementById(id);
const pick=(list)=>list[Math.floor(Math.random()*list.length)];
const prompts=[
{question:"A screenshot says a claim is true. What do we need?",answer:"An identifiable original source and relevant context.",type:"SOURCE"},
{question:"A relative asks to share a family photo. What happens first?",answer:"Ask each relevant person's permission. No public upload by default.",type:"CONSENT"},
{question:"A token balance changed. Was it a trade?",answer:"Not necessarily. Compare fills, swaps, transfers, rewards and fees before concluding.",type:"RECEIPT"},
{question:"Two news sources disagree. Which wins?",answer:"Neither automatically. Preserve both and test dated evidence.",type:"COLLISION"},
{question:"A math result is correct. Does that make the underlying accusation true?",answer:"No. Correct computation is not proof of its real-world inputs.",type:"FULLMATH"}
];
function fillText(id,text){const n=$(id);if(n)n.textContent=text;}
const draw=$("draw-card"),reveal=$("reveal-card");let cardIndex=-1;
if(draw&&reveal){
draw.addEventListener("click",()=>{
 cardIndex=(cardIndex+1)%prompts.length;
 const p=prompts[cardIndex];fillText("card-question",p.type+": "+p.question);
 fillText("card-answer","Answer hidden until reveal.");reveal.disabled=false;
});
reveal.addEventListener("click",()=>{
 if(cardIndex<0)return;
 fillText("card-answer",prompts[cardIndex].answer+" STATUS=LEARNING_ONLY");
});
}
const roll=$("crisscross-roll");if(roll){
const stages=[
{a:"CLAIM",b:"SOURCE",q:"Does the cited source support exactly the claim stated?"},
{a:"SOURCE",b:"TIME",q:"Was the source available at the event time or published later?"},
{a:"ACTOR",b:"RELATION",q:"Does a link to a person prove that another person belongs to an organization?"},
{a:"RECEIPT",b:"AUTHORITY",q:"Does preserving a record create legal or financial authority?"},
{a:"PUBLIC",b:"PRIVATE",q:"Does a public HTTP 200 authorize viewing a family record?"}
];let k=-1;
roll.addEventListener("click",()=>{
 k=(k+1)%stages.length;
 const v=stages[k];fillText("rail-a",v.a);fillText("rail-b",v.b);
 fillText("cross-question",v.q);
 fillText("cross-answer","Decide before replaying Seymour.");
});
$("crisscross-replay").addEventListener("click",()=>{
 if(k<0)return;
 fillText("cross-answer","HOLD — comparison alone creates no evidence, identity, permission or authority. Verify both typed rails and document unresolved differences.");
});
}
const syntax=$("syntax-input");if(syntax){
$("syntax-parse").addEventListener("click",()=>{
 const input=syntax.value.trim();
 // Illustrative classroom grammar: not an authentication system or secret input.
 const m=/^::joy::\/(observe|protect|replay|repair)\/(local|public-safe)$/.exec(input);
 if(!m){fillText("syntax-output","HOLD: unrecognized public grammar. Never enter a password, recovery phrase, private name or family secret here.");return;}
 if(m[2]==="public-safe"&&m[1]==="observe"){
 fillText("syntax-output","HOLD: observation isn't permission for public release. Family consent still required.");return;
 }
 fillText("syntax-output",JSON.stringify({parser:"PUBLIC_GAME_DEMO_ONLY",action:m[1].toUpperCase(),scope:m[2].toUpperCase(),person_id:null,permission_created:false,authority:false},null,2));
});
}
const square=$("wolfram-level");if(square){
const update=()=>{
 const n=Math.max(0,Math.min(8,Number(square.value)||0));
 const q=n*n, delta=2*n+1;
 fillText("wolfram-output","LEVEL "+n+" → "+q+" virtual quarter units. Next-level increase = "+delta+" units. Verified symbolic rule: (n+1)² - n² = 2n+1. Real charge $0.00. No tokens moved.");
};square.addEventListener("input",update);update();
}
const seymour=$("seymour-mode");if(seymour){
 $("seymour-replay").addEventListener("click",()=>{
 const flag=seymour.value;
 const outcome=flag==="claim"?"UNVERIFIED_CLAIM":flag==="source"?"SOURCE_POINTER_NOT_PROOF":"PUBLICATION_NOT_PERMISSION";
 fillText("seymour-result","V1 DISTINCT → V2 CHECK COUPLING → V3 COLLISION OPEN → V4 HUMAN REVIEW. "+outcome+". FINDING=HOLD · AUTHORITY=FALSE.");
 });
}
})();