(* CI-FIRST v2: independent Wolfram model replay, NOT production enforcement. *)
ClearAll[states, valid, eligible, unsignedMutant, configs, malformed, eligibleCount, unauthorized, unsignedLeaks, malformedBlocked, result];
states = {"PASS", "FAIL", "UNKNOWN", "HOLD"};
valid[e_, h_, s_] := ListQ[e] && Length[e] === 4 &&
  AllTrue[e, MemberQ[states, #] &] &&
  (h === True || h === False) &&
  (s === True || s === False);
eligible[e_, h_, s_] := TrueQ[valid[e, h, s]] &&
  AllTrue[e, # === "PASS" &] && TrueQ[h] && TrueQ[s];
unsignedMutant[e_, h_, s_] := TrueQ[valid[e, h, s]] &&
  AllTrue[e, # === "PASS" &] && TrueQ[h];
configs = Flatten[Table[{e, p[[1]], p[[2]]}, {e, Tuples[states, 4]},
   {p, Tuples[{False, True}, 2]}], 1];
malformed = {
  {{}, True, True},
  {ConstantArray["PASS", 3], True, True},
  {ConstantArray["PASS", 5], True, True},
  {{"PASS", "PASS", "PASS", "BOGUS"}, True, True},
  {"PASS", True, True},
  {None, True, True},
  {ConstantArray["PASS", 4], "False", True},
  {ConstantArray["PASS", 4], True, "False"},
  {ConstantArray["PASS", 4], 1, True},
  {ConstantArray["PASS", 4], True, 1},
  {ConstantArray["PASS", 4], None, True},
  {ConstantArray["PASS", 4], True, None},
  {ConstantArray["PASS", 4], "True", "True"}
};
eligibleCount = Count[configs, x_ /; Apply[eligible, x]];
unauthorized = Count[configs, x_ /; Apply[eligible, x] &&
    (!TrueQ[x[[2]]] || !TrueQ[x[[3]]] || !AllTrue[x[[1]], # === "PASS" &])];
unsignedLeaks = Count[configs, x_ /; Apply[unsignedMutant, x] && !TrueQ[x[[3]]]];
malformedBlocked = Count[malformed, x_ /; !Apply[eligible, x]];
result = <|
  "configurations" -> Length[configs],
  "eligible" -> eligibleCount,
  "unauthorized" -> unauthorized,
  "unsigned_mutant_leaks" -> unsignedLeaks,
  "malformed_cases" -> Length[malformed],
  "malformed_blocked" -> malformedBlocked,
  "authority_created" -> False,
  "production_enforcement" -> "UNKNOWN"
|>;
Print[ExportString[result, "RawJSON"]];
If[Length[configs] === 1024 && eligibleCount === 1 && unauthorized === 0 &&
   unsignedLeaks === 1 && malformedBlocked === Length[malformed], Exit[0], Exit[1]];
