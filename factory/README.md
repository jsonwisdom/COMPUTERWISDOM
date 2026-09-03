# Garbage General factory launcher

This directory is the local control plane for Jason Wisdom's three active
repository streams. It inventories real checkouts, performs scoped machine
checks, and emits a reverse-replay receipt. It does not merge, publish, message
family members, or create authority.

Runtime order:

```text
Garbage Jason
  -> Garbage General
       -> ChatGPT
       -> Grok
       -> Grok Bots
       -> PowerShell
```

Garbage Jason is the human mission owner. Garbage General is the orchestrator.
The four workers return observations and receipts; they do not inherit Jason's
identity or authority.

The human portion runs in the terminal. After machine replay, the launcher asks
Jason for `ACKNOWLEDGE`, `HOLD`, or `STOP` and records the answer. Acknowledging
a receipt does not merge or publish anything.

Run from the `COMPUTERWISDOM` checkout:

```powershell
.\factory\Invoke-GarbageGeneral.ps1 `
  -MissionOwner "Jason Wisdom" `
  -IdentityAnchor "jaywisdom.base.eth" `
  -Repos COMPUTERWISDOM,GPKMONSTER,JOY `
  -ReverseReplay `
  -RunMachineChecks `
  -EmitGeneralReceipt
```

Missing repositories return `HOLD_CHECKOUT_MISSING`. A Git diff check is a
scoped machine result, not proof that a repository's full test suite passed.
