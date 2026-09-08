# Pushdown Automaton (PDA) — Explanation v0.1

Status: explanation only. No parser instantiated. No stack object created. No transition system inferred from Ziggy/LeahPrime rails. `AUTHORITY_CREATED = false`.

## Core idea

A pushdown automaton (PDA) is a finite-state machine plus one stack.

The finite control has only finitely many modes. The stack is unbounded, but only the top symbol may be inspected and rewritten. That extra memory is what supports nested structure such as matched parentheses, if/else blocks, and languages like `{ a^n b^n | n >= 0 }`.

A useful operational sentence is:

> push = incur a nested obligation; pop = discharge the most recent obligation.

One stack handles nested debt well. It does not, in general, handle two independent synchronized debts.

## Why the stack matters

A DFA cannot remember an unbounded exact count unless that count is encoded into a finite number of states. A PDA can push one marker per input symbol and later pop them, so the count is represented by stack height/content rather than by the number of control states.

With one stack, a PDA still cannot recognize every language. Standard non-context-free examples include `{ a^n b^n c^n }` and `{ ww }`.

## Formal definition

A nondeterministic PDA is

`P = (Q, Sigma, Gamma, delta, q0, Z0, F)`

where:

- `Q` = finite control states
- `Sigma` = input alphabet
- `Gamma` = stack alphabet
- `delta` = transition relation
- `q0` = start state
- `Z0` = initial/bottom stack symbol
- `F` = accepting states (for final-state acceptance)

A move may inspect the current state, the next input symbol (or epsilon), and the top stack symbol, then move to a new state while replacing that top symbol with a string of stack symbols.

## Instantaneous description

A configuration may be written as:

`(q, w, gamma)`

meaning: control state `q`, unread input `w`, and stack contents `gamma`.

One-step evolution is commonly written with `|-` (or the turnstile relation), and its reflexive-transitive closure with `|-*`.

## Example: `{ a^n b^n | n >= 0 }`

Use a push phase for `a` symbols and a pop phase for `b` symbols:

1. read each `a` and push `A`
2. on the first `b`, enter the pop phase
3. read each `b` and pop one `A`
4. accept when the input is consumed and only the bottom marker remains (or the stack is empty, depending on the chosen acceptance convention)

Thus `aabb` succeeds, while strings such as `aab`, `abb`, or `abab` fail under the intended machine.

## PDA and CFG equivalence

Nondeterministic pushdown automata and context-free grammars have the same expressive power:

`NPDA languages = context-free languages`.

A CFG can be simulated by an NPDA whose stack holds sentential forms; conversely, an NPDA can be encoded as a CFG using variables that represent state/stack-state relationships.

## Deterministic vs nondeterministic PDA

Unlike DFA vs NFA, determinism changes expressive power for pushdown automata.

For a DPDA, determinism is stronger than merely having at most one transition for `(q, a, X)`. If an epsilon transition is available for a given `(q, X)` configuration, a consuming transition may not compete with it from that same configuration.

Deterministic context-free languages form a strict subset of all context-free languages.

## One stack vs more memory

- DFA: finite control only
- PDA: finite control + one stack
- two-stack PDA: Turing-power equivalent

The single stack gives last-in/first-out access, not arbitrary random access.

## Precision notes

- The CFL pumping result is usually called the **Bar-Hillel pumping lemma**.
- **Parikh's theorem** is a separate result concerning semilinear symbol-count vectors of context-free languages.
- A one-stack PDA is well matched to tree-shaped or nested obligations.

## Boundary receipt

```text
PDA_EXPLANATION = ACCEPT
MACHINE_INSTANCE = NONE
STACK = NONE
TRANSITIONS = NONE
ZIGGY_LEAHPRIME_INFERENCE = NONE
CANON = FALSE
AUTHORITY_CREATED = false
```
