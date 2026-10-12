# GB-GARBAGE-LIBRARY-EMPIRICAL-BAYES-2026-10-01

STATUS = WORKING EMPIRICAL-BAYES ENGINE
AUTHORITY_CREATED = FALSE

## Purpose
Estimate shrinkage strength from the Garbage Library card table instead of freezing a permanent hand-picked prior strength.

For cell (k,f):
Sbar_kf | theta_kf ~ Normal(theta_kf, sigma_e^2 / n_kf)
theta_kf ~ Normal(mu, tau^2)

Posterior shrinkage:
theta_hat_kf = mu + B_kf * (Sbar_kf - mu)
B_kf = tau^2 / (tau^2 + sigma_e^2 / n_kf)

Fat cells stay local.
Thin cells shrink toward the parent.

## Hyperparameter estimation
Estimate:
mu_hat
sigma_e_hat
tau_hat

Preferred production route once the table is large enough:
weighted random-effects model / REML on the logit score scale.

## Minimum-data rule
A board of point estimates without n_kf is not an empirical-Bayes input.

Once at least 5 cells have n >= 5:
estimate character and format variance components.

## Disclosure
Empirical Bayes uses the data to estimate the prior and then shrinks the same data.
Therefore:
- naive intervals are too tight;
- extreme thin cells can over-shrink;
- survivor-only estimation biases tau downward.

For PROMOTE / RETIRE probabilities, prefer full Bayes or bootstrap the complete EB pipeline.

## Non-collapse
EB_SHRINKAGE != TIKTOK_WEIGHT
SMALL_TAU != CHARACTERS_ARE_USELESS
SHRUNK_SCORE != QUALITY_VERDICT
REML_RESULT != RECEIPT_TRUTH
