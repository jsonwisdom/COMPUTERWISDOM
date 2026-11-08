(* Run with: wolframscript -file COMPUTER_WISDOM_QUAD_ONION_V1_1_TESTS.wl *)
Get[FileNameJoin[{DirectoryName[$InputFileName],"COMPUTER_WISDOM_WOLFRAM_QUAD_ONION_V1_1.wl"}]];
msg = "Computer Wisdom CI-FIRST Wallet2 Proof 2026-11-07. Address: 0x65891F97db01C8fC9F76f4DFE65Bd44F8261f1B0. Purpose: prove control of this address only. No payments, transactions, ENS changes, contract approvals, or authority transfer. Historical A380 identity remains separate.";
expected = "0x65891F97db01C8fC9F76f4DFE65Bd44F8261f1B0";
checks = <|
 "message_bytes" -> If[Length[ToCharacterCode[msg,"UTF8"]] == 274,"PASS","FAIL"],
 "sha256" -> If[IntegerString[Hash[ByteArray[ToCharacterCode[msg,"UTF8"]],"SHA256"],16,64] == "71d49b8ef059fafa003d3b6160ba5d3be8f3ea5a866fd67bdcaef28e28b628c8","PASS","FAIL"],
 "eip191_keccak256" -> Module[{b = ToCharacterCode[msg,"UTF8"],p}, p=Join[{25},ToCharacterCode["Ethereum Signed Message:\n"<>ToString[Length[b]],"UTF8"]]; If[IntegerString[Hash[ByteArray[Join[p,b]],"Keccak256"],16,64] == "4fc1135eed8659d5500c9be5b00274d18aefab883fb0c9e7e2e7e8f368264dfe","PASS","FAIL"]],
 "missing_signature_is_unknown" -> If[cwVerify[msg,"",expected]["verdict"] == "UNKNOWN","PASS","FAIL"],
 "malformed_signature_is_unknown" -> If[cwVerify[msg,"0xZZ",expected]["verdict"] == "UNKNOWN","PASS","FAIL"],
 "invalid_r_is_fail" -> If[cwVerify[msg,StringJoin[ConstantArray["00",64]]<>"1b",expected]["verdict"] == "FAIL","PASS","FAIL"],
 "wrong_signer" -> "UNKNOWN_NEEDS_VALID_SIGNATURE_FIXTURE",
 "flipped_message_byte" -> "UNKNOWN_NEEDS_VALID_SIGNATURE_FIXTURE",
 "wallet2_live_recovery" -> "UNKNOWN_NEEDS_VALID_SIGNATURE_FIXTURE"
|>;
Print[ExportString[checks,"RawJSON"]];
