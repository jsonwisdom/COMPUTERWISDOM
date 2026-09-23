# Gray Baby Series 004 — Mission 004-033 — The Tax Table v0.1

Status: `OPEN / DRAFT / UNMERGED`  
Authority created: `FALSE`  
Membrane intact: `TRUE`

## Mission

Read a public tax table without collapsing rate, levy, assessed value, equalized value, jurisdiction, year, or final household tax bill into one number.

## Kid question

> “What kind of tax number is this, for which place and year, and what would we need before saying what somebody actually paid?”

## Mission card

**LOOK**  
Record the visible row, column labels, value, unit, year, and named jurisdiction.

**GUESS**  
Keep separate any assumption that the table proves a household bill, a spending decision, an individual tax burden, or misconduct.

**SOURCE**  
Use the public table or official tax/finance surface and preserve the exact publication context.

**ENVIRONMENT / BOUNDARY CONDITIONS**

```text
tax_year_or_fiscal_year
jurisdiction
municipality_or_district
county_context
assessed_vs_equalized_value
rate_unit
levy_type
exemptions_or_credits_when_material
source_version
publication_date
```

**RECEIPT**

```text
ROW / COLUMN LABELS
+ VALUE
+ UNIT
+ YEAR
+ JURISDICTION
+ SOURCE
+ TABLE VERSION / DATE
```

**TRUE / FALSE / HOLD**  
`HOLD` when two values are being compared across incompatible years, jurisdictions, units, valuation bases, or tax categories.

**FIRST GAP**  
The first missing dimension needed to interpret the number correctly.

**PARENT-SAFE REPLAY**  
“Before we compare these numbers, are they the same kind of number for the same place and year?”

**TAKEAWAY**

```text
TAX_RATE != TAX_BILL
LEVY != EXPENDITURE
ASSESSED_VALUE != EQUALIZED_VALUE
SAME_DOLLAR_SIGN != SAME_MEANING
SAME_RATE_LABEL != SAME_TAX_CONTEXT
NUMBER_FOUND != MONEY_AUDITED
```

## CrissCross

Forward:

```text
PUBLIC TABLE
-> OWNER / JURISDICTION
-> YEAR
-> NUMBER TYPE
-> UNIT / VALUATION BASIS
-> RECEIPT
-> COMPARISON
```

Reverse:

```text
COMPARISON CLAIM
-> RECEIPT
-> UNIT / BASIS
-> NUMBER TYPE
-> YEAR
-> JURISDICTION
-> PUBLIC TABLE
```

Stop at the first unresolved edge.

## Current state

```text
MISSION = 004-033 / TAX_TABLE
ENVIRONMENTAL_LAYER = REQUIRED
COMPARISON_REQUIRES_COMPATIBLE_DIMENSIONS = TRUE
AUTHORITY_CREATED = FALSE
```
