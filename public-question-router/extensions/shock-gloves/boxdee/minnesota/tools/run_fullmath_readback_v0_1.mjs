import {readFileSync} from "node:fs";
import {auditRegistry,inspectClockFixture} from "./fullmath_guard_v0_1.mjs";
const base=new URL("../",import.meta.url);
const get=path=>JSON.parse(readFileSync(new URL(path,base),"utf8"));
const registry=auditRegistry(get("receipts/MINNESOTA_REPLAY_VALIDATION_REGISTRY_V0_1.json"));
const demo=inspectClockFixture(get("fixtures/MNK_003_SYNTHETIC_CLOCK_DEMO_V0_1.json"));
const output={project:"THE ART OF LEARING",motto:"Make Them Laugh. Make Them Think. Make Them LEAR.",civic_discovery:"REFERENCE_ONLY",registry,demo,real_minnesota_gate_tests_performed:0,proof_admission:"HOLD",facts_promoted:0,authority_created:false,live_deployments:0,stripe_charges:0};
console.log(JSON.stringify(output,null,2));
if(registry.status!=="CONSISTENT_METADATA_ONLY"||demo.status!=="SIMULATION_PASS")process.exitCode=1;
