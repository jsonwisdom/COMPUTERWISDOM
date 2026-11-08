// CI-FIRST separate JSONWisdom.io Worker backend. No wallet, payment, or DNS writes.
import original from "./supreme-origin.mjs";
const identity = Object.freeze({
  schema:"computerwisdom.ci-first.worker-identity.v1",
  namespace:"jsonwisdom.io",
  worker_service:"jw-io-supreme-v1",
  source_service:"seymour-supreme-public",
  source_sha256:"5708a044da58fdca3ec53eef0469eab0d97607b693483534f6cb7dd411516c93",
  same_cloudflare_account:true,
  independent_provider:false,
  canon:false,
  authority_created:false
});
export default {
  async fetch(request, env, ctx) {
    const u = new URL(request.url);
    if (u.pathname === "/.well-known/ci-first-backend.json") {
      if (request.method !== "GET" && request.method !== "HEAD")
        return new Response(null, {status:405,headers:{"allow":"GET, HEAD","cache-control":"no-store"}});
      return new Response(request.method === "HEAD" ? null : JSON.stringify(identity), {
        status:200,
        headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store","x-ci-first-backend":"jw-io-supreme-v1"}
      });
    }
    return original.fetch(request, env, ctx);
  }
};
