# GB-GARBAGE-LIBRARY-BAYES-PRIORS-2026-10-01

STATUS = WORKING BAYESIAN CONTROL MODEL
AUTHORITY_CREATED = FALSE

## Core law
Character scores are beliefs, not leaderboards.

For character k:
theta_k ~ Beta(alpha_k, beta_k)
mu_k = alpha_k / (alpha_k + beta_k)

Initial regularizer:
n0 = alpha + beta = 12

## Update
Clip S_v to (0.01, 0.99).
Let lambda in [0,1] represent metric trust / sample sufficiency.

alpha <- alpha + lambda * S_v
beta  <- beta  + lambda * (1 - S_v)

## Decay
Weekly:
alpha, beta <- rho * alpha, rho * beta
rho = 0.92

Interpretation: memory decays; an old winner does not own a new platform regime.

## Thompson sampling
For each slot:
theta_tilde_k ~ Beta(alpha_k, beta_k)

Use posterior draws to drive exploration, while retaining the hard 70/20/10 mix.

## Promotion controls
PROMOTE if P(theta > 0.80) > 0.70 and n_eff >= 15.
HOLD if 95% interval width > 0.20.
RETIRE if P(theta < 0.55) > 0.80 and n_eff >= 20.

## Non-collapse
POSTERIOR_MEAN != TRUTH
VIRAL_DRAW != RECEIPT_QUALITY
COMMENT_RATE != CONSENSUS
CHARACTER_SCORE != PLATFORM_WEIGHT
