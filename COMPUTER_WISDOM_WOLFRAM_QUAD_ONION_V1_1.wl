(* Computer Wisdom — Quad Onion v1.1; read-only EIP-191 secp256k1 recovery. *)
(* Inputs: UTF-8 message string, 65-byte signature hex, expected address hex. *)
(* No network, keys, payments, changes, or signing. *)
ClearAll[cwHexBytes, cwModInverse, cwPointAdd, cwPointMul, cwRecover, cwVerify, cwTest];
cwP = 2^256 - 2^32 - 977;
cwN = 16^^FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141;
cwG = {16^^79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
 16^^483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8};
cwInfinity = {"Infinity", "Infinity"};
cwHexBytes[s_String] := Module[{h = StringReplace[s, StartOfString ~~ "0x" -> ""]},
 If[! StringMatchQ[h, RegularExpression["(?i)[0-9a-f]*"]] || OddQ[StringLength[h]], Return[$Failed]];
 FromDigits[#, 16] & /@ StringPartition[h, 2]
];
cwModInverse[x_Integer, n_Integer] := If[Mod[x, n] == 0, $Failed, PowerMod[Mod[x, n], -1, n]];
cwPointAdd[a_List, b_List] := Module[{s, x, y, den},
 If[a === cwInfinity, Return[b]]; If[b === cwInfinity, Return[a]];
 If[a[[1]] == b[[1]] && Mod[a[[2]] + b[[2]], cwP] == 0, Return[cwInfinity]];
 If[a == b, den = Mod[2 a[[2]], cwP];
  If[den == 0, Return[cwInfinity]];
  s = Mod[3 a[[1]]^2 cwModInverse[den, cwP], cwP],
  den = Mod[b[[1]] - a[[1]], cwP];
  If[den == 0, Return[cwInfinity]];
  s = Mod[(b[[2]] - a[[2]]) cwModInverse[den, cwP], cwP]
 ];
 x = Mod[s^2 - a[[1]] - b[[1]], cwP];
 y = Mod[s (a[[1]] - x) - a[[2]], cwP]; {x,y}
];
cwPointMul[k_Integer, p_List] := Module[{r = cwInfinity, q = p, t = k},
 If[t < 0, Return[cwPointMul[-t, {p[[1]], Mod[-p[[2]], cwP]}]]];
 While[t > 0, If[OddQ[t], r = cwPointAdd[r, q]]; q = cwPointAdd[q, q]; t = Quotient[t, 2]]; r
];
cwToBytes[x_Integer, count_Integer] := IntegerDigits[x, 256, count];
cwRecover[hashBytes_List, sigHex_String] := Module[
 {sig = cwHexBytes[sigHex], r, s, v, rec, j, x, a, y, R, e, q, pubBytes, addrBytes},
 If[sig === $Failed || Length[sig] != 65, Return[<|"verdict" -> "UNKNOWN", "reason" -> "MISSING_OR_MALFORMED_SIGNATURE"|>]];
 r = FromDigits[sig[[1;;32]], 256]; s = FromDigits[sig[[33;;64]],256]; v = sig[[65]];
 If[! (1 <= r < cwN && 1 <= s <= Quotient[cwN, 2]), Return[<|"verdict" -> "FAIL", "reason" -> "INVALID_OR_HIGH_S"|>]];
 rec = Which[MemberQ[{27,28},v], v-27, MemberQ[{0,1},v], v, True, -1];
 If[rec < 0, Return[<|"verdict" -> "FAIL", "reason" -> "UNSUPPORTED_RECOVERY_ID"|>]];
 j = Quotient[rec,2]; x = r + j cwN;
 If[x >= cwP, Return[<|"verdict" -> "FAIL", "reason" -> "X_OUT_OF_FIELD"|>]];
 a = Mod[x^3+7,cwP]; y = PowerMod[a, Quotient[cwP+1,4],cwP];
 If[Mod[y^2,cwP] != a, Return[<|"verdict" -> "FAIL", "reason" -> "NO_CURVE_POINT"|>]];
 If[Mod[y,2] != Mod[rec,2], y = Mod[-y,cwP]];
 R = {x,y};
 If[cwPointMul[cwN,R] =!= cwInfinity, Return[<|"verdict" -> "FAIL", "reason" -> "INVALID_POINT_ORDER"|>]];
 e = FromDigits[hashBytes,256];
 q = cwPointMul[PowerMod[r,-1,cwN], cwPointAdd[cwPointMul[s,R],cwPointMul[-Mod[e,cwN],cwG]]];
 If[q === cwInfinity, Return[<|"verdict" -> "FAIL", "reason" -> "INFINITY_PUBLIC_KEY"|>]];
 pubBytes = Join[cwToBytes[q[[1]],32],cwToBytes[q[[2]],32]];
 addrBytes = Take[IntegerDigits[Hash[ByteArray[pubBytes],"Keccak256"],256,32],-20];
 <|"verdict" -> "PASS", "recovered_address" -> "0x"<>ToLowerCase[StringJoin[IntegerString[#,16,2]& /@ addrBytes]]|>
];
cwVerify[msg_String, sigHex_String, expectedAddress_String] := Module[
 {mb, prefix, digest, recovery, actual, expected},
 mb = ToCharacterCode[msg,"UTF8"];
 prefix = Join[{25},ToCharacterCode["Ethereum Signed Message:\n"<>ToString[Length[mb]],"UTF8"]];
 digest = IntegerDigits[Hash[ByteArray[Join[prefix,mb]],"Keccak256"],256,32];
 recovery = cwRecover[digest,sigHex];
 If[recovery["verdict"] =!= "PASS", Return[Join[<|"schema" -> "computer-wisdom.quad-onion.v1.1", "authority_granted" -> False|>,recovery]]];
 actual = ToLowerCase[recovery["recovered_address"]]; expected = ToLowerCase[expectedAddress];
 Join[<|"schema" -> "computer-wisdom.quad-onion.v1.1", "authority_granted" -> False,
   "eip191_keccak256" -> IntegerString[FromDigits[digest,256],16,64],
   "message_bytes" -> Length[mb]|>, recovery,
  <|"expected_address" -> expected, "verdict" -> If[actual === expected, "PASS", "FAIL"]|>]
];
(* No real signature is embedded. Live Wallet2 signer recovery remains UNKNOWN until a
   separately supplied, publicly safe message/signature fixture is verified. *)
