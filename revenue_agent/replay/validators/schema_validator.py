from __future__ import annotations

from typing import Any, Dict, List

import jsonschema

from replay.validators.base import Validator


class SchemaValidator(Validator):
    """Validate observed outputs against a concrete work-order output schema."""

    name = "schema"

    def validate(
        self,
        work_order: Dict[str, Any],
        observed_outputs: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        if not isinstance(observed_outputs, list) or any(
            not isinstance(item, dict) for item in observed_outputs
        ):
            return self.result("FAIL", 0.0, "Observed outputs must be a list of objects.")

        output_schema = work_order.get("output_schema")
        if output_schema in {None, "", "PENDING"}:
            return self.result(
                "PASS",
                1.0,
                "No concrete output_schema is declared; observed object shape is replayable, "
                "but semantic schema correctness is not asserted.",
            )

        if not isinstance(output_schema, dict):
            return self.result("FAIL", 0.0, "output_schema must be an object or PENDING.")

        try:
            validator_cls = jsonschema.validators.validator_for(output_schema)
            validator_cls.check_schema(output_schema)
            validator = validator_cls(output_schema)
            for item in observed_outputs:
                validator.validate(item)
        except jsonschema.exceptions.SchemaError as exc:
            return self.result("FAIL", 0.0, f"Invalid output_schema: {exc.message}")
        except jsonschema.exceptions.ValidationError as exc:
            return self.result("FAIL", 0.0, f"Observed output schema mismatch: {exc.message}")

        return self.result("PASS", 1.0, "All observed outputs match the declared output_schema.")
