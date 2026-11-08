#!/usr/bin/env python3
"""JSONWisdom CI-FIRST: offline, standard-library-only EIP-191 batch proof verifier.

Read-only. No wallet connection, RPC calls, transactions, or secret handling.
"""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

MASK = (1 << 64) - 1
ROT = ((0, 36, 3, 41, 18), (1, 44, 10, 45, 2), (62, 6, 43, 15, 61), (28, 55, 25, 21, 56), (27, 20, 39, 8, 14))
RC = (0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
      0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
      0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
      0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
      0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
      0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008)
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

def rot(x, n):
    return ((x << n) | (x >> (64 - n))) & MASK if n else x

def permute(a):
    for rc in RC:
        c = [a[x] ^ a[x+5] ^ a[x+10] ^ a[x+15] ^ a[x+20] for x in range(5)]
        d = [c[(x-1)%5] ^ rot(c[(x+1)%5], 1) for x in range(5)]
        for y in range(5):
            for x in range(5):
                a[x+5*y] ^= d[x]
        b = [0]*25
        for y in range(5):
            for x in range(5):
                b[y+5*((2*x+3*y)%5)] = rot(a[x+5*y], ROT[x][y])
        for y in range(5):
            for x in range(5):
                a[x+5*y] = b[x+5*y] ^ ((~b[(x+1)%5+5*y]) & b[(x+2)%5+5*y])
        a[0] ^= rc

def keccak256(data):
    rate = 136
    padded = bytearray(data)
    padded.append(0x01)  # Keccak domain padding, NOT FIPS SHA3's 0x06
    while len(padded) % rate:
        padded.append(0)
    padded[-1] |= 0x80
    a = [0]*25
    for start in range(0, len(padded), rate):
        block = padded[start:start+rate]
        for i in range(rate//8):
            a[i] ^= int.from_bytes(block[8*i:8*i+8], 'little')
        permute(a)
    return b''.join(v.to_bytes(8,'little') for v in a)[:32]

def inv(x, modulus):
    return pow(x % modulus, -1, modulus)

def add(a, b):
    if a is None: return b
    if b is None: return a
    x1,y1=a; x2,y2=b
    if x1 == x2 and (y1+y2)%P == 0: return None
    if a == b:
        slope = (3*x1*x1 * inv(2*y1,P)) % P
    else:
        slope = ((y2-y1)*inv(x2-x1,P)) % P
    x3 = (slope*slope-x1-x2)%P
    return (x3,(slope*(x1-x3)-y1)%P)

def mul(k, point):
    result = None
    while k:
        if k & 1: result = add(result,point)
        point = add(point,point)
        k >>= 1
    return result

def neg(point):
    return (point[0],(-point[1])%P)

def address(pubkey):
    x,y=pubkey
    digest=keccak256(x.to_bytes(32,'big')+y.to_bytes(32,'big'))
    return '0x'+digest[-20:].hex()

def eip191_digest(message):
    raw=message.encode('utf-8')
    return keccak256(b'\x19Ethereum Signed Message:\n' + str(len(raw)).encode('ascii') + raw)

def recover(message, signature):
    if not isinstance(signature,str) or not signature.startswith('0x') or len(signature)!=132:
        raise ValueError('signature must be a 65-byte 0x-prefixed hex string')
    try: sig=bytes.fromhex(signature[2:])
    except ValueError: raise ValueError('invalid signature hex')
    r=int.from_bytes(sig[:32],'big'); s=int.from_bytes(sig[32:64],'big'); v=sig[64]
    if not(1<=r<N and 1<=s<N): raise ValueError('invalid r or s')
    if v in (27,28): recid=v-27
    elif v in (0,1): recid=v
    else: raise ValueError('unsupported recovery id (expected 0, 1, 27, or 28)')
    x=r  # standard Ethereum recovery 0/1
    if x>=P: raise ValueError('invalid recovery x')
    beta=pow((pow(x,3,P)+7)%P,(P+1)//4,P)
    if pow(beta,2,P)!=(pow(x,3,P)+7)%P: raise ValueError('point is not on curve')
    y=beta if beta%2==recid else P-beta
    R=(x,y)
    if mul(N,R) is not None: raise ValueError('invalid ephemeral point')
    z=int.from_bytes(eip191_digest(message),'big')
    q=mul(inv(r,N), add(mul(s,R),neg(mul(z%N,G))))
    if q is None: raise ValueError('recovered point is infinity')
    # Explicit ECDSA verification
    w=inv(s,N); u1=(z*w)%N; u2=(r*w)%N
    check=add(mul(u1,G),mul(u2,q))
    if check is None or check[0]%N != r: raise ValueError('signature verification failed')
    return address(q)

def verify_entry(entry):
    ident=entry.get('id','unnamed')
    base={'id':ident,'chain':'Base (EVM / EIP-191)','status':'UNKNOWN', 'authority_granted':False}
    if entry.get('scheme')!='eip191_personal_sign':
        return {**base,'reason':'unsupported or unspecified signature scheme'}
    expected=entry.get('expected_address'); msg=entry.get('message'); sig=entry.get('signature')
    if not isinstance(expected,str) or not expected.startswith('0x') or len(expected)!=42:
        return {**base,'reason':'missing/invalid expected address'}
    try: bytes.fromhex(expected[2:])
    except ValueError: return {**base,'reason':'nonhex expected address'}
    if not isinstance(msg,str): return {**base,'reason':'exact message missing'}
    if not sig: return {**base,'reason':'signature not supplied'}
    base['message_sha256']='0x'+hashlib.sha256(msg.encode('utf-8')).hexdigest()
    base['message_eip191_keccak256']='0x'+eip191_digest(msg).hex()
    base['signature_sha256']='0x'+hashlib.sha256(bytes.fromhex(sig[2:])).hexdigest() if isinstance(sig,str) and sig.startswith('0x') and len(sig)==132 and all(c in '0123456789abcdefABCDEF' for c in sig[2:]) else None
    try: signer=recover(msg,sig)
    except (ValueError,ZeroDivisionError) as exc:
        return {**base,'status':'FAIL','reason':str(exc)}
    base['recovered_address']=signer
    base['status']='PASS' if signer.lower()==expected.lower() else 'FAIL'
    base['reason']='signer matches expected address' if base['status']=='PASS' else 'recovered signer differs from expected address'
    return base

def self_test():
    assert keccak256(b'').hex() == 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'
    assert keccak256(b'abc').hex() == '4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45'
    assert address(G)=='0x7e5f4552091a69125d5dfcb7b8c2659029395bdf'
    # Deterministic local key-derived test signature (private test key = 1, never an account credential).
    msg='CI-FIRST self-test'; z=int.from_bytes(eip191_digest(msg),'big'); k=2
    rx,ry=mul(k,G); r=rx%N; s=(inv(k,N)*(z+r))%N
    sig='0x'+r.to_bytes(32,'big').hex()+s.to_bytes(32,'big').hex()+bytes([27+(ry%2)]).hex()
    assert recover(msg,sig)==address(G)
    return True

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input',nargs='?',help='Batch JSON input file')
    ap.add_argument('--output',help='Receipt JSON output path')
    ap.add_argument('--self-test',action='store_true')
    args=ap.parse_args()
    self_test()
    if args.self_test and not args.input:
        print('PASS: Keccak256 vectors, secp256k1 address, EIP-191 recovery'); return
    if not args.input: ap.error('input required unless --self-test')
    doc=json.loads(Path(args.input).read_text(encoding='utf-8'))
    results=[verify_entry(p) for p in doc['proofs']]
    receipt={'schema':'jsonwisdom.ci-first.batch-proof.v1','generated_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
             'mode':'read-only/offline','network_context':'Base mainnet 8453','verifier':'pure-python-stdlib/EIP-191',
             'checks':results,'counts':{s:sum(p['status']==s for p in results) for s in ('PASS','FAIL','UNKNOWN')},
             'authority_granted':False,'note':'Proves control of an EVM key for an exact message only. No ENS, deployment, payment, or historical other-wallet authority.'}
    output=json.dumps(receipt,indent=2,ensure_ascii=False)+'\n'
    if args.output: Path(args.output).write_text(output,encoding='utf-8')
    print(output)
    if any(r['status']=='FAIL' for r in results): raise SystemExit(1)
    if any(r['status']=='UNKNOWN' for r in results): raise SystemExit(2)
if __name__=='__main__': main()
