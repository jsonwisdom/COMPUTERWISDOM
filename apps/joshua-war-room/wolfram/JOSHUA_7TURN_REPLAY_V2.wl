(* JOSHUA War Room, CW-JOSHUA-STACK-001, independent seven-turn arithmetic.
   Inputs transcribed from user's 2026-11-16 exported replay.
   No assertion of the original play event, wallet signature, EIP-191 recovery, or file provenance.
   This aggregate model is valid for these values because no state cap is reached. *)
ClearAll[rolls, modifiers, expectedPasses, passes, defense, trust, intel, points, report];
rolls = {1, 12, 13, 14, 8, 3, 15};
modifiers = {4, 3, 2, 3, 4, 3, 2};
expectedPasses = {False, True, True, True, True, False, True};
passes = MapThread[#1 + #2 >= 12 &, {rolls, modifiers}];
defense = 60 + 14 + 14 - 7 - Total[{7, 9, 5, 7, 9, 5, 7}];
trust = 60 - 7 + 14 - Total[{2, 4, 2, 4, 2, 4, 2}];
intel = 30 + 14 + 14;
points = Total[If[#, 20, 5] & /@ passes];
report = TestReport[{
  VerificationTest[passes, expectedPasses, TestID -> "Seven D20 outcomes"],
  VerificationTest[{defense, trust, intel, points}, {32, 47, 58, 110},
    TestID -> "Seven-turn final game totals"],
  VerificationTest[Length[rolls] + 1, 8, TestID -> "Expected next turn"],
  VerificationTest[Last[rolls], 15, TestID -> "Last D20 roll"]
}];
report
