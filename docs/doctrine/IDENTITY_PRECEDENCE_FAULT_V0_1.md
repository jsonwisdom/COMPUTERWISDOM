# Identity Precedence Fault V0.1

## Doctrine

Identity routing failure can masquerade as work failure.

When the work exists locally but a remote system refuses it, inspect the credential layer before rebuilding artifacts.

## Pattern

```text
work exists
commit exists
branch exists
remote rejects push
human assumes work failed
actual cause: wrong credential won the race
```

## GitHub Direct Instance

In the observed GitHub Direct fault, Cloud Shell had a valid GitHub CLI login for `jsonwisdom`, but an invalid environment token was selected first.

The fix was to remove the invalid environment identity and route Git through the valid GitHub CLI identity.

## Generalized Rule

This applies to developer tools that support multiple identities or credential sources.

## Operator Rule

Do not rebuild the artifact until identity routing has been inspected.

## Child Version

You had a good key and a bad key. The computer kept trying the bad key first. Throw away the bad key for that room, then use the good key.

Authority: false.  
No Fake Green: true.
Replay required: true.
