(* Coinbase Full-History Membrane v0.1
   Deterministic metadata checks only.
   No trade execution and no private identifiers required.
*)

ClearAll[historyComplete, timestampDiffs, triggerClasses];

historyComplete[surfaces_Association] :=
  And @@ (TrueQ[Lookup[#, "ExplicitTerminus", False]] & /@ Values[surfaces]);

timestampDiffs[times_List] := Differences[Sort[DeleteMissing[times]]];

triggerClasses[state_Association] := DeleteCases[
  {
    If[TrueQ@Lookup[state, "CursorAdvanced", False], "CURSOR_ADVANCED", Nothing],
    If[TrueQ@Lookup[state, "CursorEnded", False], "CURSOR_ENDED", Nothing],
    If[TrueQ@Lookup[state, "HashChanged", False], "HASH_CHANGED", Nothing],
    If[TrueQ@Lookup[state, "SchemaDrift", False], "SCHEMA_DRIFT", Nothing],
    If[TrueQ@Lookup[state, "TimestampGap", False], "TIMESTAMP_GAP", Nothing],
    If[TrueQ@Lookup[state, "TimestampOverlap", False], "TIMESTAMP_OVERLAP", Nothing],
    If[TrueQ@Lookup[state, "DuplicateStableID", False], "DUPLICATE_STABLE_ID", Nothing],
    If[TrueQ@Lookup[state, "HistoryComplete", False], "HISTORY_COMPLETE", Nothing],
    If[TrueQ@Lookup[state, "FieldSemanticsHold", False], "FIELD_SEMANTICS_HOLD", Nothing]
  },
  Nothing
];

(* Governing law:
   TRIGGER != TRADE
   TIMESTAMP_DIFF != CAUSE
   SIGNAL != ORDER
*)
