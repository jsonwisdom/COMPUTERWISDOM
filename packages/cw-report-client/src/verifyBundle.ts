import crypto from 'crypto';
import { canonicalize } from './canonicalJson.js';

export function verifyBundle(bundle: any): { ok: boolean; root: string; errors: string[] } {
  const errors: string[] = [];

  if (!Array.isArray(bundle.objects)) {
    return { ok: false, root: '0x00', errors: ['bundle.objects missing or invalid'] };
  }

  const leaves = bundle.objects.map((obj: any) => {
    const canonical = canonicalize(obj.payload);
    const hash = crypto.createHash('sha256').update(canonical).digest('hex');

    if (hash !== obj.sha256) {
      errors.push(`Hash mismatch for object ${obj.id}`);
    }

    return Buffer.from(hash, 'hex');
  });

  if (errors.length > 0) {
    return { ok: false, root: '0x00', errors };
  }

  function merkle(nodes: Buffer[]): Buffer {
    if (nodes.length === 1) return nodes[0];

    const next: Buffer[] = [];

    for (let i = 0; i < nodes.length; i += 2) {
      const left = nodes[i];
      const right = nodes[i + 1] || nodes[i];

      next.push(
        crypto
          .createHash('sha256')
          .update(Buffer.concat([left, right]))
          .digest()
      );
    }

    return merkle(next);
  }

  const root = '0x' + merkle(leaves).toString('hex');

  return {
    ok: true,
    root,
    errors: []
  };
}
