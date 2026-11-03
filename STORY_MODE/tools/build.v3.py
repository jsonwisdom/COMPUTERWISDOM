#!/usr/bin/env python3
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'08-replay'/'story-mode.manifest.v3.json'
ROOT_NOTE=ROOT/'08-replay'/'merkle-root.v1.json'
REPLAY_RESULT=ROOT/'08-replay'/'replay-result.v3.json'
EXCLUDED={MANIFEST,ROOT_NOTE,REPLAY_RESULT}
LEAF_DOMAIN=b'JSONWISDOM_STORY_MODE_LEAF_V1\x00'
NODE_DOMAIN=b'JSONWISDOM_STORY_MODE_NODE_V1\x00'

def source_files():
    return [p for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p not in EXCLUDED]

def leaf(path,sha_hex):
    rel=path.relative_to(ROOT).as_posix().encode('utf-8')
    return hashlib.sha256(LEAF_DOMAIN+rel+b'\x00'+bytes.fromhex(sha_hex)).digest()

def merkle_root(nodes):
    if not nodes: return hashlib.sha256(b'JSONWISDOM_STORY_MODE_EMPTY_V1').digest()
    level=list(nodes)
    while len(level)>1:
        if len(level)%2: level.append(level[-1])
        level=[hashlib.sha256(NODE_DOMAIN+level[i]+level[i+1]).digest() for i in range(0,len(level),2)]
    return level[0]

def main():
    check=subprocess.run([sys.executable,str(ROOT/'tools'/'validate.v2.py')])
    if check.returncode: return check.returncode
    entries=[]; leaves=[]
    for path in source_files():
        raw=path.read_bytes(); sha=hashlib.sha256(raw).hexdigest()
        entries.append({'path':path.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':sha})
        leaves.append(leaf(path,sha))
    root=merkle_root(leaves).hex()
    manifest={'manifest_id':'JSONWISDOM-STORY-MODE-MANIFEST-v3','version':'3.0.0','algorithm':'sha256','entry_order':'path_ascending','leaf_domain':LEAF_DOMAIN[:-1].decode(),'node_domain':NODE_DOMAIN[:-1].decode(),'odd_node_rule':'duplicate_last','entries':entries,'authority_created':False}
    note={'object_id':'merkle:jsonwisdom-story-mode:v1','object_type':'PUBLIC_MERKLE_ROOT','version':'1.0.0','algorithm':'sha256','leaf_count':len(leaves),'merkle_root':root,'manifest':'story-mode.manifest.v3.json','commit_binding':'ROOT_IS_COMMITTED_BY_THE_GIT_COMMIT_CONTAINING_THIS_FILE','eas_attestation':'NOT_CREATED','authority_created':False}
    MANIFEST.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    ROOT_NOTE.write_text(json.dumps(note,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(f'MERKLE_BUILD=PASS LEAVES={len(leaves)} ROOT={root} AUTHORITY_CREATED=false')
    return 0

if __name__=='__main__': raise SystemExit(main())
