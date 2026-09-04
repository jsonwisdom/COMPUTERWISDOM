#!/usr/bin/env node
"use strict";
const fs=require("fs"), path=require("path");
const {canonicalize,stateHash}=require("./serializer");
let failed=false; const rows=[];
const root="fixtures/replayos/canonical-serializer-v1";
for(const file of fs.readdirSync(root).filter(x=>x.endsWith(".json")).sort()){
  const fixture=JSON.parse(fs.readFileSync(path.join(root,file),"utf8"));
  const results=fixture.inputs.map(raw=>{try{const data=canonicalize(raw);return {ok:true,bytes_b64:data.toString("base64"),sha256:stateHash(data)}}catch(e){return {ok:false,error:e.code||e.message}}});
  let passed=fixture.valid?results.every(x=>x.ok):results.every(x=>!x.ok&&x.error===fixture.expected_error);
  if(fixture.expect_equal) passed=passed&&new Set(results.map(x=>x.bytes_b64)).size===1;
  if(fixture.expect_distinct) passed=passed&&new Set(results.map(x=>x.bytes_b64)).size===results.length;
  rows.push({name:fixture.name,passed,results}); failed ||= !passed;
}
console.log(JSON.stringify(rows));
process.exit(failed?1:0);
