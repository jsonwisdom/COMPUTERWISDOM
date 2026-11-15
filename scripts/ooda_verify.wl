(* Wolfram Language / CI-FIRST: independent replay of public HTTP body evidence. *)
ClearAll[CWVerifyOODA];
CWVerifyOODA[file_String] := Module[{d,rs,bytesVerified,validSchema,boundary,parity},
 d=Quiet@Check[Import[file,"RawJSON"],$Failed];
 If[!AssociationQ[d],Return[<|"result"->"INVALID_JSON"|>]];
 rs=Lookup[d,"routes",{}];
 If[Length[rs]!=2,Return[<|"result"->"INVALID_ROUTE_COUNT"|>]];
 bytesVerified=AllTrue[rs,Function[r,Module[{raw,b64},
   b64=Lookup[r,"body_base64",None];
   If[!StringQ[b64],Return[False]];
   raw=Quiet@Check[ImportString[b64,"Base64"],$Failed];
   StringQ[raw] && Hash[raw,"SHA256","HexString"]===Lookup[r,"body_sha256",None]
 ]]];
 validSchema=AllTrue[rs,Function[r,
   Lookup[r,"status",None]==="PASS" &&
   Lookup[r,"http",None]===200 &&
   Lookup[r,"schema",None]==="cw-ooda-emergency-estate/0.1" &&
   Lookup[r,"state_count",None]===50
 ]];
 boundary=Lookup[d,"authority_created",None]===False &&
   Lookup[d,"cross_provider_failover",None]==="NOT_ESTABLISHED" &&
   Lookup[d,"live_emergency_feed",None]==="NOT_ESTABLISHED";
 parity=rs[[1,"body_sha256"]]===rs[[2,"body_sha256"]];
 <|"bytes_verified"->bytesVerified,"schema_50states"->validSchema,
   "authority_boundary"->boundary,"body_parity"->parity,
   "result"->If[TrueQ[bytesVerified&&validSchema&&boundary&&parity],"PASS","HOLD"],
   "current_emergency_authority"->"NOT_ESTABLISHED"|>
];
(* Example: CWVerifyOODA["C:\\receipts\\cw-ooda-2026....json"] *)
