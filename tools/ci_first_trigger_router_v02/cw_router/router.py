"""Deterministic, read-only operator vernacular routing.

Keyword matches describe a navigation hypothesis; they never grant authority,
modify thoughts, verify content truth, create consent, or trigger remote actions.
Only bounded metadata is accepted and output; source text is not echoed.
"""
from __future__ import annotations
import hashlib
import json
import re
import unicodedata
from datetime import datetime

VERSION = 'CW_TRIGGER_REPLAY_V0_2'
# Routing table is a vocabulary, NOT an access control list or consent source.
LEXICON = (
    ('big fucking giant replay', 'BIG_REPLAY', 'COMPUTERWISDOM', 'replay'),
    ('big giant replay', 'BIG_REPLAY', 'COMPUTERWISDOM', 'replay'),
    ('giant replay', 'BIG_REPLAY', 'COMPUTERWISDOM', 'replay'),
    ('reverse replay', 'BIG_REPLAY', 'COMPUTERWISDOM', 'replay'),
    ('ci first', 'CI_FIRST', 'COMPUTERWISDOM', 'test'),
    ('ci-first', 'CI_FIRST', 'COMPUTERWISDOM', 'test'),
    ('ooda loop', 'OODA', 'COMPUTERWISDOM', 'observe'),
    ('ooda', 'OODA', 'COMPUTERWISDOM', 'observe'),
    ('ens emergencies', 'ENS_EMERGENCY', 'ENS', 'inspect'),
    ('ens emergency', 'ENS_EMERGENCY', 'ENS', 'inspect'),
    ('ens', 'ENS_DISCOVERY', 'ENS', 'lookup'),
    ('super secret sister sidecars', 'SISTER_SIDECAR', 'JOY', 'preserve_continue_route'),
    ('super secret sister', 'SISTER_SIDECAR', 'JOY', 'preserve_continue_route'),
    ('sidcars', 'SISTER_SIDECAR', 'JOY', 'preserve_continue_route'),
    ('sister sidecars', 'SISTER_SIDECAR', 'JOY', 'preserve_continue_route'),
    ('leahprime', 'LEAHPRIME', 'JOY', 'cluster_review'),
    ('leahprime187', 'LEAHPRIME187', 'JOY', 'story_review'),
    ('wolfram', 'WOLFRAM', 'COMPUTERWISDOM', 'calculate'),
    ('github', 'GITHUB', 'COMPUTERWISDOM', 'inspect'),
    ('cloudflare', 'CLOUDFLARE', 'COMPUTERWISDOM', 'inspect'),
    ('google drive', 'GOOGLE_DRIVE', 'COMPUTERWISDOM', 'inspect'),
    ('chatgpt', 'CHATGPT', 'COMPUTERWISDOM', 'inspect'),
    ('jason auth', 'JASON_AUTH', 'JASON', 'request_review'),
)
SAFE_PROVIDERS = frozenset(('github', 'google_drive', 'cloudflare', 'chat_export', 'wolfram', 'ens', 'local'))
SAFE_SIDECARS = frozenset(('SISTER_SIDECAR',))


def canon(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), sort_keys=True, allow_nan=False).encode('utf-8')


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def normalize(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError('query must be a string')
    return unicodedata.normalize('NFKC', value).casefold()


def _candidates(query: str) -> list[dict]:
    text = normalize(query)
    possible = []
    for phrase, code, lane, operation in LEXICON:
        pattern = r'(?<!\w)' + re.escape(normalize(phrase)).replace(r'\ ', r'\s+') + r'(?!\w)'
        for match in re.finditer(pattern, text):
            possible.append({'span': (match.start(), match.end()), 'phrase': phrase, 'code': code,
                             'lane': lane, 'operation': operation})
    possible.sort(key=lambda x: (-(x['span'][1] - x['span'][0]), x['span'][0], x['code']))
    accepted = []
    for candidate in possible:
        if not any(candidate['span'][0] < o['span'][1] and o['span'][0] < candidate['span'][1]
                   for o in accepted):
            accepted.append(candidate)
    return sorted(accepted, key=lambda x: (x['span'][0], x['code']))


def _validate_timestamp(timestamp: str) -> str:
    if not isinstance(timestamp, str):
        raise ValueError('timestamp must be string')
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    except ValueError as err:
        raise ValueError('invalid observed_at ISO-8601') from err
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError('timestamps require timezone')
    return dt.isoformat(timespec='microseconds')


def _verify_metadata(records: list[dict]) -> dict:
    if not isinstance(records, list) or len(records) > 500:
        raise ValueError('records must be list with at most 500 items')
    errors = []
    ordered = []
    seen = set()
    collisions = set()
    by_location = {}
    for idx, raw in enumerate(records):
        if not isinstance(raw, dict):
            errors.append({'index': idx, 'code': 'INVALID_RECORD_TYPE'})
            continue
        provider = raw.get('provider')
        object_id = raw.get('object_id')
        stamp = raw.get('observed_at')
        checksum = raw.get('sha256')
        if provider not in SAFE_PROVIDERS or not isinstance(object_id, str) or not object_id.strip() or len(object_id) > 300:
            errors.append({'index': idx, 'code': 'INVALID_LOCATOR'})
            continue
        if not isinstance(checksum, str) or re.fullmatch(r'[0-9a-fA-F]{64}', checksum) is None:
            errors.append({'index': idx, 'code': 'INVALID_DIGEST'})
            continue
        try:
            time = _validate_timestamp(stamp)
        except ValueError:
            errors.append({'index': idx, 'code': 'INVALID_TIMESTAMP'})
            continue
        locator = digest(canon([provider, object_id]))
        entry = {'provider': provider, 'locator_sha256': locator, 'observed_at': time,
                 'recorded_sha256': checksum.lower(), 'verification': 'RECORDED_ONLY'}
        key = (provider, locator, time, checksum.lower())
        if key in seen:
            continue
        seen.add(key)
        location = (provider, locator, time)
        if location in by_location and by_location[location] != checksum.lower():
            collisions.add(location)
        by_location[location] = checksum.lower()
        ordered.append(entry)
    ordered.sort(key=lambda e: (e['observed_at'], e['provider'], e['locator_sha256'], e['recorded_sha256']))
    return {'records': ordered, 'count': len(ordered), 'duplicates_removed': len(records) - len(ordered) - len(errors),
            'metadata_errors': errors, 'same_instant_digest_conflicts': len(collisions)}


def replay(query: str, records: list[dict] | None = None) -> dict:
    if not isinstance(query, str) or len(query) > 10000:
        raise ValueError('query must be text of at most 10000 characters')
    entries = _candidates(query)
    lanes = sorted(set(e['lane'] for e in entries))
    codes = sorted(set(e['code'] for e in entries))
    evidence = _verify_metadata(records or [])
    sidecar = bool(SAFE_SIDECARS.intersection(codes))
    routing_status = 'PASS' if entries else 'NO_TRIGGER'
    metadata_status = ('FAIL' if evidence['metadata_errors'] or evidence['same_instant_digest_conflicts']
                       else 'PASS' if evidence['count'] else 'NOT_EVALUATED')
    decision = {
        'version': VERSION,
        'query_sha256': digest(query.encode('utf-8')),
        'matched_triggers': [{'code': e['code'], 'phrase': e['phrase'], 'lane': e['lane'], 'operation': e['operation']}
                             for e in entries],
        'route_lanes': lanes,
        'classification': {
            'routing': routing_status,
            'metadata_integrity': metadata_status,
            'content_truth': 'NOT_EVALUATED',
            'source_authenticity': 'NOT_EVALUATED',
            'remote_execution': 'NOT_RUN',
        },
        'ooda': {
            'observe': 'INDEX_ONLY',
            'orient': 'SOURCE_BOUND_METADATA_ONLY',
            'decide': 'HUMAN_REVIEW',
            'act': 'READ_ONLY_LOCAL_REPLAY',
        },
        'sister_sidecar': {'private_by_default': sidecar, 'sequence': ['PRESERVE', 'CONTINUE', 'ROUTE'] if sidecar else [],
                           'terminal_hold': False, 'owns_people': False},
        'leahprime': {'synthetic_cluster_reviewer': 'LEAHPRIME' in codes or 'LEAHPRIME187' in codes,
                     'replay_status': 'NOT_RUN', 'content_truth_status': 'NOT_EVALUATED', 'private_by_default': True},
        'jason_auth': {
            'principal': 'HUMAN_OPERATOR', 'research_route': True,
            'identity_verified_by_keyword': False, 'granted_write_capabilities': [],
            'approval_required_for_mutations': True,
        },
        'evidence': evidence,
        'authority_created': False,
        'consent_created': False,
        'secrets_collected': False,
        'publication': 'NONE',
        'external_calls': 0,
        'system_mutations': 0,
    }
    decision['replay_sha256'] = digest(canon(decision))
    return decision
