import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
import { project, RendererError } from '../index.js';

const fixturePath = fileURLToPath(new URL('./fixtures/validReceipt.json', import.meta.url));
const validReceipt = JSON.parse(fs.readFileSync(fixturePath, 'utf8'));

function expectRendererCode(receipt, code) {
  try {
    project(receipt);
    throw new Error(`Expected renderer error ${code}`);
  } catch (error) {
    expect(error).toBeInstanceOf(RendererError);
    expect(error.code).toBe(code);
  }
}

describe('GAME_RECEIPT_RENDERER_V0_1', () => {
  it('T08: rejects any authority-related field, regardless of value or nesting', () => {
    expectRendererCode({ ...validReceipt, authority_created: true }, 'AUTHORITY_FIELD_PRESENT');
    expectRendererCode({ ...validReceipt, authority_created: false }, 'AUTHORITY_FIELD_PRESENT');
    expectRendererCode({ ...validReceipt, authority: 'admin' }, 'AUTHORITY_FIELD_PRESENT');

    const nested = structuredClone(validReceipt);
    nested.observed_outputs[0].authority_claim = 'smuggled';
    expectRendererCode(nested, 'AUTHORITY_FIELD_PRESENT');

    expect(() => project(validReceipt)).not.toThrow();
  });

  it('T10: copies receipt_digest unchanged and never recomputes it', () => {
    const projection = project(validReceipt);
    expect(projection.receipt_digest).toBe(validReceipt.receipt_digest);
  });

  it('T11: omits schema-valid protocol fields outside the projection whitelist', () => {
    const source = structuredClone(validReceipt);
    const projection = project(source);

    expect(projection).not.toHaveProperty('parent_id');
    expect(projection).not.toHaveProperty('quadratic_weight');
    expect(projection).not.toHaveProperty('execution_trace');
    expect(source.parent_id).toBe(validReceipt.parent_id);
    expect(source.execution_trace).toEqual(validReceipt.execution_trace);
  });

  it('rejects unknown top-level protocol fields because the canonical schema is closed', () => {
    expectRendererCode({ ...validReceipt, future_field: 'some_value' }, 'SCHEMA_INVALID');
  });

  it('T12: projection is deeply immutable and does not leak source references', () => {
    const source = structuredClone(validReceipt);
    const projection = project(source);

    expect(() => { projection.work_order_id = 'HACKED'; }).toThrow();
    expect(() => { projection.anomalies.push({ type: 'injected' }); }).toThrow();
    expect(() => { projection.observed_outputs[0].value = 'HACKED'; }).toThrow();

    expect(source.work_order_id).toBe('JOY-CD8D67E3');
    expect(source.anomalies).toEqual([]);
    expect(source.observed_outputs[0].value).toBe('observable only');
  });

  it('T13: malformed digest fails closed with DIGEST_MALFORMED', () => {
    expectRendererCode({ ...validReceipt, receipt_digest: 'short' }, 'DIGEST_MALFORMED');
  });

  it('projects only the approved safe fields', () => {
    expect(Object.keys(project(validReceipt)).sort()).toEqual([
      'anomalies',
      'baseline_anchor',
      'evidence_refs',
      'observed_outputs',
      'receipt_digest',
      'semantic_validation',
      'work_order_id',
    ]);
  });
});
