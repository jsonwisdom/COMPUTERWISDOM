"""FullMath ComputerWizard Triggered Decks: OFFLINE candidate receipt batching.

No network code, account actions, minting, payments, deployment, or publication.
Deterministic receipts are integrity evidence, NOT human approval or truth.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import zlib
from pathlib import Path

SCHEMA = 'CW_TRIGGERED_DECKS_BATCH_V0_1'
PURPOSE = 'ADULT_FICTION_SATIRE_CANDIDATE'
CANON_FREEZE = 'dcbd862c3501dfcd349aa878180fb13114c7d039'
HEX256 = re.compile(r'^[0-9a-f]{64}$')
CARD_ID = re.compile(r'^CWTD-[A-Z0-9-]{3,40}$')
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
MAX_RUN_INSTANCES = 9000
MAX_FILE_BYTES = 12_000_000

class GateError(ValueError):
    """Refuse a candidate without changing external state."""


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def no_duplicate_keys(pairs):
    result = {}
    for k, value in pairs:
        if k in result:
            raise GateError('DUPLICATE_JSON_KEY')
        result[k] = value
    return result


def strict_json(data):
    try:
        return json.loads(data, object_pairs_hook=no_duplicate_keys,
                          parse_constant=lambda _: (_ for _ in ()).throw(GateError('NONFINITE_JSON')))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise GateError('BAD_JSON') from exc


def read_relative(root, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise GateError('UNSAFE_PATH')
    p = Path(relative)
    if p.is_absolute() or any(x in ('.', '..') for x in p.parts):
        raise GateError('UNSAFE_PATH')
    root = Path(root).resolve()
    target = root.joinpath(p)
    # Reject all symlink components, including final file.
    current = root
    for part in p.parts:
        current = current / part
        if current.is_symlink():
            raise GateError('SYMLINK_FORBIDDEN')
    if not target.is_file():
        raise GateError('MISSING_FILE')
    if target.stat().st_size > MAX_FILE_BYTES:
        raise GateError('FILE_TOO_LARGE')
    return target.read_bytes()


def strict_png_size(data):
    """Check container, CRCs, RGBA8 zlib stream, scanline length, and dimensions.

    Not a substitute for review of artwork, rights, pixel border, caption or identity.
    """
    if not data.startswith(PNG_SIGNATURE):
        raise GateError('NOT_PNG')
    offset, chunks, idat, width, height, seen_iend = 8, 0, [], None, None, False
    while offset < len(data):
        if offset + 12 > len(data):
            raise GateError('TRUNCATED_PNG')
        length = struct.unpack('>I', data[offset:offset+4])[0]
        kind = data[offset+4:offset+8]
        end = offset + 12 + length
        if length > MAX_FILE_BYTES or end > len(data):
            raise GateError('TRUNCATED_PNG')
        raw = data[offset+8:offset+8+length]
        expected_crc = struct.unpack('>I', data[end-4:end])[0]
        if zlib.crc32(kind+raw) & 0xffffffff != expected_crc:
            raise GateError('PNG_CRC_MISMATCH')
        chunks += 1
        if chunks == 1:
            if kind != b'IHDR' or length != 13:
                raise GateError('PNG_INVALID_HEADER')
            width, height, depth, color, comp, filt, interlace = struct.unpack('>IIBBBBB', raw)
            if (depth, color, comp, filt, interlace) != (8, 6, 0, 0, 0):
                raise GateError('UNSUPPORTED_PNG_ENCODING')
            if not (1 <= width <= 4096 and 1 <= height <= 4096):
                raise GateError('PNG_SIZE_INVALID')
        elif kind == b'IHDR':
            raise GateError('PNG_DUPLICATE_HEADER')
        if kind == b'IDAT':
            idat.append(raw)
        if kind == b'IEND':
            if length != 0 or end != len(data):
                raise GateError('PNG_INVALID_END')
            seen_iend = True
            break
        offset = end
    if not seen_iend or not idat:
        raise GateError('PNG_INCOMPLETE')
    expected_len = height * (1 + 4*width)
    if expected_len > 80_000_000:
        raise GateError('PNG_TOO_LARGE')
    decomp = zlib.decompressobj()
    try:
        pixels = decomp.decompress(b''.join(idat), expected_len + 1)
        pixels += decomp.flush()
    except zlib.error as exc:
        raise GateError('PNG_CORRUPT_PIXELS') from exc
    if len(pixels) != expected_len or not decomp.eof or decomp.unused_data:
        raise GateError('PNG_CORRUPT_PIXELS')
    for i in range(height):
        if pixels[i*(4*width+1)] > 4:
            raise GateError('PNG_INVALID_FILTER')
    if 4*width != 3*height:
        raise GateError('PORTRAIT_RATIO_REQUIRED_3_TO_4')
    return width, height


def leaf_hash(record):
    return sha256(b'CWTD-LEAF-V1\x00' + canonical(record))


def merkle_root(hashes):
    if not hashes:
        raise GateError('EMPTY_BATCH')
    layer = [bytes.fromhex(x) for x in hashes]
    while len(layer) > 1:
        if len(layer) % 2:
            layer.append(layer[-1])
        layer = [hashlib.sha256(b'CWTD-NODE-V1\x00' + layer[i] + layer[i+1]).digest()
                 for i in range(0, len(layer), 2)]
    return layer[0].hex()


def require_fields(value, required, label):
    if not isinstance(value, dict) or set(value) != set(required):
        raise GateError('FIELDS_INVALID_' + label)


def build_candidate(manifest, root):
    require_fields(manifest, {'schema','purpose','operator','mode','family_data','canon_policy','cards'}, 'MANIFEST')
    if manifest['schema'] != SCHEMA or manifest['purpose'] != PURPOSE or manifest['operator'] != 'JAY':
        raise GateError('WRONG_SCOPE')
    if manifest['mode'] != 'DESIGN_CANDIDATE_ONLY' or manifest['family_data'] is not False:
        raise GateError('PRODUCTION_OR_FAMILY_BLOCKED')
    if manifest['canon_policy'] != 'SEPARATE_LINEAGE_NO_CANON_WRITE':
        raise GateError('FROZEN_LINEAGE_BLOCKED')
    cards = manifest['cards']
    if not isinstance(cards, list) or not cards or len(cards) > 100:
        raise GateError('CARD_COUNT_INVALID')
    if len(cards) % 3:
        raise GateError('CARD_BATCH_MUST_DIVIDE_BY_3')
    seen, leaves, masters, total = set(), [], [], 0
    for card in cards:
        require_fields(card, {'card_id','asset_path','asset_sha256','fiction_label','source_class',
                              'instances','caption','master_status'}, 'CARD')
        cid = card['card_id']
        if not isinstance(cid,str) or not CARD_ID.fullmatch(cid) or cid in seen:
            raise GateError('CARD_ID_INVALID_OR_DUPLICATE')
        seen.add(cid)
        if card['fiction_label'] != 'FICTION / SATIRE — NOT PREDICTIONS OR FACTS':
            raise GateError('FICTION_LABEL_REQUIRED')
        if card['source_class'] != 'FICTION_SATIRE' or card['master_status'] != 'CANDIDATE_NOT_APPROVED':
            raise GateError('UNVERIFIED_MASTER_BLOCKED')
        if not isinstance(card['caption'],str) or not (1<=len(card['caption'])<=160):
            raise GateError('CAPTION_INVALID')
        n = card['instances']
        if type(n) is not int or n < 1 or n > 3000 or total+n > MAX_RUN_INSTANCES:
            raise GateError('INSTANCE_LIMIT')
        total += n
        asset = read_relative(root, card['asset_path'])
        digest = sha256(asset)
        if not isinstance(card['asset_sha256'],str) or not HEX256.fullmatch(card['asset_sha256']) or digest != card['asset_sha256']:
            raise GateError('ASSET_HASH_MISMATCH')
        w,h = strict_png_size(asset)
        master = {'card_id':cid,'asset_sha256':digest,'image_dimensions':[w,h],
                  'caption':card['caption'],'fiction_label':card['fiction_label'],
                  'source_class':card['source_class'],'master_status':card['master_status']}
        master_hash = sha256(b'CWTD-MASTER-V1\x00'+canonical(master))
        masters.append({'card_id':cid,'master_hash':master_hash,'asset_sha256':digest,'dimensions':[w,h]})
        for i in range(n):
            leaves.append(leaf_hash({'master_hash':master_hash,'instance_index':i,
                                     'lineage':'CW_TRIGGERED_DECKS_NEW_ROOT',
                                     'content_type':'ADULT_FICTION_SATIRE'}))
    candidate = {'schema':SCHEMA, 'status':'CANDIDATE_INTEGRITY_ONLY',
                 'production_status':'HOLD','human_final_decision':'JASON_REQUIRED_NOT_OBSERVED',
                 'operator_approval':'JAY_DESIGN_PREPARATION_ONLY',
                 'family_data':False,'canon_freeze_unchanged':CANON_FREEZE,
                 'onchain':False,'publication':False,'sales':False,'external_send':False,
                 'batch_count_cards':len(cards),'instance_count':total,
                 'target_1m_per_min_verified':False,
                 'master_receipts':masters,'leaves':leaves,'merkle_root':merkle_root(leaves),
                 'manifest_sha256':sha256(canonical(manifest))}
    candidate['candidate_sha256'] = sha256(canonical(candidate))
    return candidate


def verify_candidate(manifest, root, candidate):
    if not isinstance(candidate, dict):
        raise GateError('CANDIDATE_NOT_OBJECT')
    original = build_candidate(manifest, root)
    if canonical(original) != canonical(candidate):
        raise GateError('REPLAY_MISMATCH')
    return {'replay_verified':True,'scope':'DETERMINISTIC_INTEGRITY_ONLY','production_status':'HOLD'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['build','verify'])
    p.add_argument('--manifest',required=True)
    p.add_argument('--root',required=True)
    p.add_argument('--report',required=True)
    a=p.parse_args(argv)
    try:
        manifest=strict_json(Path(a.manifest).read_bytes())
        if a.command=='build':
            report=build_candidate(manifest,Path(a.root))
            target=Path(a.report)
            # Local-only, fail-closed, do not overwrite any existing file.
            with target.open('x',encoding='utf-8') as f:
                f.write(canonical(report).decode('utf-8')+'\n')
            print(json.dumps({'candidate_created':str(target),'production_status':'HOLD',
                              'instance_count':report['instance_count'],'root':report['merkle_root']}))
        else:
            candidate=strict_json(Path(a.report).read_bytes())
            print(json.dumps(verify_candidate(manifest,Path(a.root),candidate),sort_keys=True))
    except (GateError,OSError,TypeError,ValueError) as exc:
        print('DENY: '+str(exc),file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
