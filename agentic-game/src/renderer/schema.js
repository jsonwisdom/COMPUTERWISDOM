import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
import Ajv2020 from 'ajv/dist/2020.js';
import { RendererError } from './errors.js';

const schemaPath = fileURLToPath(
  new URL('../../../revenue_agent/schemas/receipt.schema.json', import.meta.url),
);
const receiptSchema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));

const ajv = new Ajv2020({ strict: true, allErrors: true });
const validate = ajv.compile(receiptSchema);

export function validateReceipt(receipt) {
  if (!validate(receipt)) {
    throw new RendererError(
      `Receipt schema validation failed: ${ajv.errorsText(validate.errors)}`,
      'SCHEMA_INVALID',
    );
  }
  return true;
}
