(* CW-JOSHUA-STACK-001 / Wolfram verification notebook, 2026-11-16.
   Read-only. Receipt metadata and proposed owner-authorization logic only.
   No recovered EIP-191 signature bytes; no assertion of independent wallet-signature verification.
   This verifies an abstract policy rule, NOT its enforcement in the deployed API. *)
ClearAll[v, a, e, p, allowed, receiptMs, expiryMs, digest, owner, checks];
digest = "eb51df8ed3cc1552678f36270bd9c23ac9c6f9be9697aa94e92233688b74e845";
owner = "0x65891F97db01C8fC9F76f4DFE65Bd44F8261f1B0";
receiptMs = Round[1000 (AbsoluteTime[DateObject[{2026,11,16,23,13,12.657},TimeZone->0]] -
    AbsoluteTime[DateObject[{1970,1,1,0,0,0},TimeZone->0]])];
expiryMs = 1794872592657;
allowed = v && a && e && p;
checks = {
  VerificationTest[expiryMs - receiptMs == 30*60*1000, True,
    TestID -> "Receipt duration exactly 30 minutes"],
  VerificationTest[StringMatchQ[digest, RegularExpression["[0-9a-f]{64}"]], True,
    TestID -> "Receipt SHA-256 hexadecimal structure only"],
  VerificationTest[StringMatchQ[owner, RegularExpression["0x[0-9a-fA-F]{40}"]], True,
    TestID -> "Expected account address format"],
  VerificationTest[Resolve[ForAll[{v,a,e,p}, Implies[Not[v], Not[allowed]]], Booleans], True,
    TestID -> "Reject unverified session"],
  VerificationTest[Resolve[ForAll[{v,a,e,p}, Implies[Not[e], Not[allowed]]], Booleans], True,
    TestID -> "Reject expired session"],
  VerificationTest[Resolve[ForAll[{v,a,e,p}, Implies[Not[a], Not[allowed]]], Booleans], True,
    TestID -> "Reject wrong wallet"],
  VerificationTest[Resolve[ForAll[{v,a,e,p}, Implies[Not[p], Not[allowed]]], Booleans], True,
    TestID -> "Reject forbidden operation"]
};
TestReport[checks]
