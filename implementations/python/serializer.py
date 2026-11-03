"""ReplayOS canonical snapshot serializer v1 (Python).

Profile: RFC 8785-style canonical JSON with an explicit signed-int53-only
number policy. This implementation is intentionally independent of JavaScript.
"""
import hashlib
import json

REQUIRED = {"schema_version", "serializer_version", "builder_version", "lanes"}
FORBIDDEN = {"wall_clock", "timestamp", "updated_at", "created_at", "now", "rng"}
INT53 = 9007199254740991

class CanonicalError(ValueError):
    pass

def _pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise CanonicalError("DUPLICATE_KEY")
        out[key] = value
    return out

def _integer(text):
    value = int(text)
    if abs(value) > INT53:
        raise CanonicalError("ILLEGAL_NUMBER")
    return value

def _float(_text):
    raise CanonicalError("ILLEGAL_NUMBER")

def parse_strict(raw):
    try:
        return json.loads(raw, object_pairs_hook=_pairs, parse_int=_integer,
                          parse_float=_float,
                          parse_constant=lambda _x: (_ for _ in ()).throw(CanonicalError("ILLEGAL_NUMBER")))
    except CanonicalError:
        raise
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise CanonicalError("INVALID_JSON") from exc

def _check_unicode(text):
    for i, char in enumerate(text):
        code = ord(char)
        if 0xD800 <= code <= 0xDBFF:
            if i + 1 >= len(text) or not 0xDC00 <= ord(text[i + 1]) <= 0xDFFF:
                raise CanonicalError("LONE_SURROGATE")
        elif 0xDC00 <= code <= 0xDFFF:
            if i == 0 or not 0xD800 <= ord(text[i - 1]) <= 0xDBFF:
                raise CanonicalError("LONE_SURROGATE")

def _utf16_key(text):
    _check_unicode(text)
    return text.encode("utf-16-be")

def _encode(value):
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int) and not isinstance(value, bool):
        if abs(value) > INT53:
            raise CanonicalError("ILLEGAL_NUMBER")
        return str(value)
    if isinstance(value, float):
        raise CanonicalError("ILLEGAL_NUMBER")
    if isinstance(value, str):
        _check_unicode(value)
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, list):
        return "[" + ",".join(_encode(item) for item in value) + "]"
    if isinstance(value, dict):
        pieces = []
        for key in sorted(value, key=_utf16_key):
            if not isinstance(key, str):
                raise CanonicalError("NON_STRING_KEY")
            pieces.append(_encode(key) + ":" + _encode(value[key]))
        return "{" + ",".join(pieces) + "}"
    raise CanonicalError("UNSUPPORTED_TYPE")

def validate_envelope(value):
    if not isinstance(value, dict):
        raise CanonicalError("ENVELOPE_NOT_OBJECT")
    forbidden = set(value) & FORBIDDEN
    if forbidden:
        raise CanonicalError("WALL_CLOCK_IN_SNAPSHOT")
    unknown = set(value) - REQUIRED
    if unknown:
        raise CanonicalError("UNKNOWN_FIELD")
    missing = REQUIRED - set(value)
    if missing:
        raise CanonicalError("VERSIONLESS_ENVELOPE")
    if value["schema_version"] != "replayos-snapshot/1":
        raise CanonicalError("SCHEMA_VERSION_UNSUPPORTED")
    if value["serializer_version"] != "rfc8785-jcs-int53/1":
        raise CanonicalError("SERIALIZER_VERSION_UNSUPPORTED")
    if value["builder_version"] != "replayos-snapshot-builder/1":
        raise CanonicalError("BUILDER_VERSION_UNSUPPORTED")
    if not isinstance(value["lanes"], dict):
        raise CanonicalError("LANES_NOT_OBJECT")

def canonicalize(raw):
    value = parse_strict(raw)
    validate_envelope(value)
    data = _encode(value).encode("utf-8")
    return data

def state_hash(data):
    return hashlib.sha256(data).hexdigest()
