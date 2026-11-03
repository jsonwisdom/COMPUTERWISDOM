# LIKELIHOOD / MESSAGE / PRIOR V0.1

DIAGNOSTIC VOCABULARY — NOT AUTHORITY

```text
AUTHORITY = FALSE
PROMOTION_ALLOWED = FALSE
TRUTH_SCORE = FORBIDDEN
STATUS = LESSON / DIAGNOSTIC_VOCABULARY
```

This lesson separates three spaces that must not be collapsed.

## 1. Scheduler space

[
p^*
]

(p^*) is a scheduler decision: whether to look, sample, inspect, or allocate attention.

It is outside the inference formula.

[
p^* \notin \Pr(V\mid x)
]

A scheduling threshold is not a world frequency, prior, posterior, or truth state.

## 2. Inference space

After a realized look (x), an inference may be written:

[
\Pr(V\mid x)
]

Only a realized observation may enter as evidence, and only under an explicit sampling / likelihood model.

An internal sequential belief state may be denoted (pi_k), but:

[
pi_k \not\Rightarrow \text{promotion}
]

Promotion is a separate governance action. Posterior odds are not a claim-status machine.

## 3. World space

[
\Pr(V)
]

This is the world base rate for the modeled event/class (V). It may be unknown.

[
\Pr(V) \neq q^*
]

No scheduler constant, queue rate, convenience constant, or fake flat prior may be substituted for an unknown world base rate.

[
\text{MISSING PRIOR} \neq 0
]

and

[
\text{MISSING PRIOR} \neq \text{FLAT PRIOR BY DEFAULT}
]

## Noisy-test vocabulary

For a binary message/test (m\in\{0,1\}):

[
\alpha = \Pr(m=1\mid V=0)
]

[
\beta = \Pr(m=0\mid V=1)
]

where (alpha) is a false-positive rate and (eta) is a false-negative rate.

The positive and negative likelihood ratios are:

[
LR_+ = \frac{1-\beta}{\alpha}
]

[
LR_- = \frac{\beta}{1-\alpha}
]

These quantities are legal only when their values are sourced from an appropriate likelihood source.

## Likelihood-source taxonomy

Allowed source classes:

1. RULE_PACK — a frozen rule set with explicit likelihood behavior.
2. CALIBRATION_CORPUS — observations with known labels / outcomes sufficient to estimate error rates.
3. REFERENCE_CLASS — an independently justified population matching the modeled event and sampling process.

No source:

[
\text{NO LIKELIHOOD SOURCE}
\Rightarrow
\text{NO POSTERIOR}
\Rightarrow
\text{HOLD}
]

Missing evidence does not become probability zero.

## Independence is a receipt

Sequential updating requires an independence / dependence determination.

If two messages are derived from the same underlying stream:

[
R_1 = R_2 \text{ by derivation}
\Rightarrow I=0
]

and the second representation does not earn a fresh likelihood multiplication.

Example:

[
\text{one audio stream}
\rightarrow
\begin{cases}
\text{ASR transcript A}\\
\text{ASR transcript B}
\end{cases}
]

is one underlying message unless an independent observation channel is shown.

Same stream transcribed twice (
eq) two independent observations.

## 23 Enigma — worked refusal

Split the object before inference.

### Claim C_exist

Question: does the sampled artifact contain an occurrence of the target symbol/pattern?

If the observation (x) and sampling frame are preserved, this claim can be tested directly.

[
C_{exist}: x \text{ contains target}
]

This does not require inventing a population frequency.

### Claim C_freq

Question: is the target unusually frequent in the relevant population?

This requires both a numerator and a denominator plus a justified reference class.

[
\hat f = \frac{n_{target}}{N_{eligible}}
]

Without (N_{eligible}), the frequency claim is not estimable.

[
x \text{ present},\quad N_{eligible}\text{ missing}
\Rightarrow
C_{freq}=\text{HOLD}
]

The legal result is refusal, not a flat prior and not a made-up posterior.

## Forbidden imports

Do not import:

- a flat prior as fake observation (x)
- (pi := q^*)
- scheduler probability as world base rate
- posterior odds as promotion
- a single-number truth score
- duplicate representations as independent evidence

## Librarian invariant

```text
SCHEDULER ≠ INFERENCE
INFERENCE ≠ WORLD FREQUENCY
POSTERIOR ≠ PROMOTION
MESSAGE COPY ≠ INDEPENDENT MESSAGE
MISSING ≠ ZERO
NO LIKELIHOOD SOURCE ⇒ HOLD
```

This file is a teaching vocabulary object. It does not adjudicate any rabbit-hole entry.
