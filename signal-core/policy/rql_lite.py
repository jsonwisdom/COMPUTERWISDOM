from pathlib import Path


class PolicyError(ValueError):
    pass


def parse_value(raw):
    raw = raw.strip()
    if raw in ('true', 'True'):
        return True
    if raw in ('false', 'False'):
        return False
    if raw in ('null', 'None'):
        return None
    if len(raw) >= 2 and raw[0] in ('"', "'") and raw[-1] == raw[0]:
        return raw[1:-1]
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        return raw


def parse_line(line, idx):
    parts = line.split()
    if len(parts) < 4:
        raise PolicyError(f'invalid policy line {idx}: {line}')
    action, path, op = parts[0], parts[1], parts[2]
    expected = parse_value(' '.join(parts[3:]))
    if action not in ('REQUIRE', 'DENY'):
        raise PolicyError(f'invalid action line {idx}: {action}')
    if op not in ('==', '!=', '>=', '<=', '>', '<'):
        raise PolicyError(f'invalid operator line {idx}: {op}')
    return (action, path, op, expected, idx)


def parse_policy(text):
    rules = []
    for idx, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        rules.append(parse_line(line, idx))
    return rules


def get_path(obj, dotted):
    cur = obj
    for part in dotted.split('.'):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            raise PolicyError(f'missing path: {dotted}')
    return cur


def compare(actual, op, expected):
    if op == '==':
        return actual == expected
    if op == '!=':
        return actual != expected
    if not isinstance(actual, (int, float)) or not isinstance(expected, (int, float)):
        raise PolicyError('ordered comparison requires numbers')
    if op == '>=':
        return actual >= expected
    if op == '<=':
        return actual <= expected
    if op == '>':
        return actual > expected
    if op == '<':
        return actual < expected
    raise PolicyError(f'unsupported operator: {op}')


def evaluate_policy(receipt, rules):
    for action, path, op, expected, idx in rules:
        actual = get_path(receipt, path)
        ok = compare(actual, op, expected)
        if action == 'REQUIRE' and not ok:
            raise PolicyError(f'REQUIRE failed line {idx}: {path} {op} {expected}; actual={actual}')
        if action == 'DENY' and ok:
            raise PolicyError(f'DENY failed line {idx}: {path} {op} {expected}; actual={actual}')
    return True


def evaluate_policy_file(receipt, policy_path):
    return evaluate_policy(receipt, parse_policy(Path(policy_path).read_text(encoding='utf-8')))
