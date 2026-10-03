# GB-GARBAGE-LIBRARY-HIERARCHICAL-BAYES-2026-10-01

STATUS = WORKING HIERARCHICAL MODEL
AUTHORITY_CREATED = FALSE

## Core problem
One Beta per character collapses format, hook, length, time, and character-format interactions into a mascot score.

## Model
For video i:
g(S_i) = logit(S_i)

g(S_i) =
mu_t
+ a_character[i]
+ b_format[i]
+ c_hook[i]
+ d_character_format[i]
+ gamma * length_i
+ epsilon_i

a_k ~ Normal(0, sigma_a^2)
b_f ~ Normal(0, sigma_b^2)
c_h ~ Normal(0, sigma_h^2)
d_kf ~ Normal(0, sigma_d^2)

mu_t = moving platform/lab intercept.

## Interpretation
sigma_a = portable character effect
sigma_b = portable format effect
sigma_h = portable hook effect
sigma_d = pairing-specific interaction

Large sigma_d with small sigma_a:
characters may be costumes; pairings do the work.

Large sigma_a with small sigma_d:
character effect travels across formats.

## Autopilot
Draw posterior-predictive score for each recipe:
S_tilde(k,f,h,len)

70% = high expected score with tolerable uncertainty
20% = neighboring recipes
10% = high-variance recipes where the model is ignorant

Retire cells, not mascots, unless evidence accumulates across formats.

## Time
Platform drift belongs in mu_t or explicit regime changes.
Do not force time drift into character variance.

## Non-collapse
HIERARCHY != TIKTOK_SOURCE_CODE
POSTERIOR_EFFECT != PLATFORM_CAUSE
FORMAT_EFFECT != RECEIPT_QUALITY
MODEL_AGREEMENT != INDEPENDENT_CORROBORATION
