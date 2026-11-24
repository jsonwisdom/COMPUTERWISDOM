"""Read-only Computer Wisdom architecture guard. No external authority is created."""
import json, sys, hashlib
from pathlib import Path

def check(doc):
    failures = []
    rails = doc.get('rails', {})
    secure, public = rails.get('secure', {}), rails.get('public', {})
    if secure.get('identity') != 'jaywisdom.eth': failures.append('secure_identity_mismatch')
    if public.get('identity') != 'jaywisdom.base.eth': failures.append('public_identity_mismatch')
    if secure.get('visibility') != 'PRIVATE_BY_DEFAULT': failures.append('secure_visibility_mismatch')
    if public.get('visibility') != 'PUBLIC_BY_DESIGN': failures.append('public_visibility_mismatch')
    for rail in (secure, public):
        for forbidden in ('publish_secrets', 'export_credentials', 'silent_signing'):
            if forbidden in rail.get('allowed', []): failures.append('forbidden_capability_'+forbidden)
    if doc.get('build_authority') != 'ENABLED': failures.append('build_disabled')
    if doc.get('global_project_hold') is not False: failures.append('global_hold')
    if doc.get('continuity',{}).get('financial_actions') != 'EXPLICIT_HUMAN_APPROVAL': failures.append('financial_authority')
    if doc.get('wallets',{}).get('a380',{}).get('address','').lower() == doc.get('wallets',{}).get('pc',{}).get('address','').lower(): failures.append('wallet_conflation')
    if doc.get('restoration_scope') != 'LOCAL_ARCHITECTURE_ARTIFACT_ONLY_NOT_LIVE_WALLET_RESTORATION': failures.append('false_live_restoration')
    return failures

def run(path):
    data = Path(path).read_bytes()
    d = json.loads(data)
    f = check(d)
    print(json.dumps({'artifact_sha256':hashlib.sha256(data).hexdigest(),'status':'PASS' if not f else 'FAIL','checks':12,'failures':f,'scope':'LOCAL_READ_ONLY'},sort_keys=True))
    return 0 if not f else 1

if __name__ == '__main__': sys.exit(run(sys.argv[1] if len(sys.argv)>1 else 'architecture.json'))
