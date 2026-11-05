# Independent (non-JS) canonicalizer cross-check for SYN-002 (strings/ints only; BMP keys, so codepoint order == UTF-16 order).
import json, hashlib, pathlib
o = json.loads(pathlib.Path(__file__).parent.parent.joinpath('fixtures/SYN-002.json').read_text('utf-8'))
s = json.dumps(o, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
print('sha256:' + hashlib.sha256(s.encode('utf-8')).hexdigest())
