(* BLACKBARPRESS / Computer Wisdom - CI-FIRST evidence graph v1
   Model proof, not certification of real flight, passenger, payment or misconduct claims.
   Reproduce in Wolfram Language: Get["proofs/blackbarpress_evidence_graph_v1.wl"]
   Each receipt below is fictitious test data.
*)
ClearAll[ciVerdict, ciClaimStatus];
ciVerdict[s_List] := Which[
 MemberQ[s, "FAIL"], "FAIL",
 AllTrue[s, # === "PASS" &], "PASS",
 True, "UNKNOWN"
];
ciClaimStatus[requirements_List, receipts_Association] :=
 ciVerdict[Lookup[receipts, requirements, "UNKNOWN"]];
ciStates = {"PASS", "FAIL", "UNKNOWN"};
ciTriples = Tuples[ciStates, 3];
ciEdges = {
 DirectedEdge["Tail", "Serial"], DirectedEdge["Serial", "Model"],
 DirectedEdge["Serial", "SpecificCabin"], DirectedEdge["Tail", "Flight"],
 DirectedEdge["Flight", "TravelApproval"], DirectedEdge["TravelApproval", "Payment"],
 DirectedEdge["Payment", "CourtExhibit"], DirectedEdge["CourtExhibit", "Evidence"]
};
ciGraph = Graph[ciEdges, DirectedEdges -> True];
ciReceipts = <|
 "tail_to_serial" -> "PASS", "serial_to_model" -> "PASS",
 "flight_to_approval" -> "PASS", "approval_to_payment" -> "PASS"
|>;
ciChecks = <|
 "completeTriplePassIffAllPass" ->
  AllTrue[ciTriples,
   (ciVerdict[#] === "PASS") == AllTrue[#, # === "PASS" &] &],
 "contradictedTripleFailIffSomeFail" ->
  AllTrue[ciTriples,
   (ciVerdict[#] === "FAIL") == MemberQ[#, "FAIL"] &],
 "unresolvedTripleUnknownIffMissingAndNotContradicted" ->
  AllTrue[ciTriples,
   (ciVerdict[#] === "UNKNOWN") ==
    (MemberQ[#, "UNKNOWN"] && ! MemberQ[#, "FAIL"]) &],
 "independentModelProven" ->
  (ciClaimStatus[{"tail_to_serial", "serial_to_model"}, ciReceipts] === "PASS"),
 "specificCabinNotInferredFromModel" ->
  (ciClaimStatus[{"tail_to_serial", "serial_to_cabin"}, ciReceipts] === "UNKNOWN"),
 "unrelatedMissingCabinDoesNotErasePaymentPath" ->
  (ciClaimStatus[{"flight_to_approval", "approval_to_payment"}, ciReceipts] === "PASS"),
 "flightNotEvidenceOfPassengerIdentity" ->
  (ciClaimStatus[{"flight_to_passenger"}, ciReceipts] === "UNKNOWN"),
 "graphIsAcyclic" -> AcyclicGraphQ[ciGraph],
 "hasCandidatePathTailToPayment" ->
  (Length[FindPath[ciGraph, "Tail", "Payment", Infinity, 1]] > 0)
|>;
ciProofResult = <|
 "combinations" -> Length[ciTriples], "checks" -> ciChecks,
 "allChecksPass" -> And @@ Values[ciChecks]
|>;
ciProofResult
