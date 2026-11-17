(* CI-FIRST: jaywisdom.eth Quad Onion. Read-only identity-separation and ENS namehash self-test. *)
(* No RPC, signing, transactions, private keys, transfers or authority writes. *)
ClearAll[to32,cwKeccak,cwStep];
to32[n_Integer] := IntegerDigits[n, 256, 32];
cwKeccak[bytes_List] := to32[Hash[ByteArray[bytes], "Keccak256"]];
cwStep[node_List,label_String] := cwKeccak[Join[node,cwKeccak[ToCharacterCode[label, "UTF8"]]]];
name = "jaywisdom.eth";
expectedNode = "0x611c283ca81f9d335749611d7b09f9809fd390244cb61a9d77318ba5612aae8e";
computedNode = "0x" <> StringJoin[IntegerString[#,16,2]& /@ Fold[cwStep,ConstantArray[0,32],Reverse[StringSplit[name, "."]]]];
wallets = ToLowerCase /@ {
  "0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8",
  "0x65891F97db01C8fC9F76f4DFE65Bd44F8261f1B0",
  "0x0f7018fea1dc9ba32ae817d896211f72f1197ad8",
  "0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5"
};
verdict = <|
 "scope" -> name,
 "ens_namehash" -> computedNode,
 "namehash_contract" -> If[computedNode===expectedNode, "PASS", "FAIL"],
 "wallet_identity_separation" -> If[Length[DeleteDuplicates[wallets]]===4, "PASS", "FAIL"],
 "ens_current_owner" -> "UNKNOWN_NOT_READ_ONCHAIN",
 "ens_current_manager" -> "UNKNOWN_NOT_READ_ONCHAIN",
 "current_windows_signing" -> "UNKNOWN_NO_FRESH_SIGNATURE",
 "historical_pc_wallet2_eip191" -> "PASS_PRIOR_AUDIT",
 "authority_created" -> False,
 "safe_to_transfer" -> False
|>;
Print["JAYWISDOM_ETH_CI_FIRST_QUAD_ONION=" <> ExportString[verdict, "RawJSON"]];
