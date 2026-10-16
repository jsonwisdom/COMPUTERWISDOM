/* Public Index Audit v0.1 — three independent public repositories.
   GitHub source freshness is not deployment verification or authority.
   Fail closed on missing evidence; no write APIs, credentials, or workflow control. */
(function () {
  "use strict";
  const owner = "jsonwisdom";
  const names = ["JOY", "AL", "COMPUTERWISDOM"];
  const own = document.querySelector("script[data-wisdom-index]")?.getAttribute("data-wisdom-index") || "UNKNOWN";
  const base = "https://jsonwisdom.github.io/";
  const panel = document.createElement("section");
  panel.id = "wisdom-public-index";
  panel.setAttribute("aria-label", "Public repository index and evidence audit");
  const css = document.createElement("style");
  css.textContent = "#wisdom-public-index{box-sizing:border-box;margin:20px auto;max-width:1120px;padding:22px;border:2px solid #526e87;border-radius:18px;background:#0e1928;color:#f5f9ff;font:15px/1.5 system-ui,sans-serif;overflow-wrap:anywhere}#wisdom-public-index *{box-sizing:border-box}#wisdom-public-index h2{font-size:1.35rem;line-height:1.3;margin:0 0 7px;color:#fff}#wisdom-public-index p{margin:8px 0;color:#d7e5f2}#wisdom-public-index a{color:#8cdbff;text-decoration:underline}#wisdom-public-index .wi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:12px;margin:16px 0}#wisdom-public-index .wi-card{background:#18283a;border:1px solid #53647a;border-radius:12px;padding:14px;min-width:0}#wisdom-public-index .wi-card h3{margin:0 0 8px;font-size:1.1rem;color:#fff}#wisdom-public-index .wi-card p{margin:7px 0;font-size:.91rem}#wisdom-public-index .wi-state{font-weight:750;color:#ffe2a1}#wisdom-public-index .wi-proof{font-weight:750}#wisdom-public-index button{background:#b1e4ff;color:#071524;border:0;border-radius:8px;padding:10px 14px;font-weight:800;cursor:pointer}#wisdom-public-index button:disabled{opacity:.6;cursor:wait}#wisdom-public-index .wi-small{font-size:.82rem;color:#d7e5f2}#wisdom-public-index .wi-question{padding:10px;border-left:3px solid #ffe2a1;background:#15283c}";
  document.head.appendChild(css);
  panel.innerHTML = '<h2>LIVE PUBLIC INDEX · JOY / AL / COMPUTERWISDOM</h2>' +
    '<p>Three independent repositories. Each card reads the latest public GitHub commit and tests its published index bytes against the committed index. No self-awarded approval.</p>' +
    '<p class="wi-question"><strong>School of Wisdom audit question:</strong> Can a human open all three indexes, inspect source receipts, and verify the served homepage is the committed homepage? Missing evidence means HOLD, not green.</p>' +
    '<div class="wi-grid" id="wi-repo-grid"></div>' +
    '<p id="wi-school-audit">School of Wisdom audit receipt: NOT_CHECKED</p>' +
    '<button id="wi-refresh" type="button">Refresh public evidence</button>' +
    '<p id="wi-checked" class="wi-small">Source, served-page bytes, and human visual acceptance are separate checks. Visual approval: HUMAN_HOLD.</p>';
  const mount = document.querySelector("main") || document.body;
  mount.insertBefore(panel, mount.firstChild);
  const grid = panel.querySelector("#wi-repo-grid");
  const cards = {};
  names.forEach(function (name) {
    const section = document.createElement("article");
    section.className = "wi-card";
    const heading = document.createElement("h3");
    const site = document.createElement("a");
    site.href = base + name + "/";
    site.textContent = name + " · Public index ↗";
    heading.appendChild(site);
    const links = document.createElement("p");
    const source = document.createElement("a");
    source.href = "https://github.com/" + owner + "/" + name;
    source.textContent = "GitHub source";
    const docs = document.createElement("a");
    docs.href = base + name + "/docs/";
    docs.textContent = "Docs";
    links.append(source, document.createTextNode(" · "), docs);
    const commit = document.createElement("p");
    commit.textContent = "Source HEAD: NOT_CHECKED";
    const served = document.createElement("p");
    served.className = "wi-state";
    served.textContent = "Public byte check: NOT_CHECKED";
    const evidence = document.createElement("p");
    evidence.className = "wi-small";
    evidence.textContent = "Human visual acceptance: HOLD";
    const changes = document.createElement("div");
    changes.className = "wi-small";
    changes.textContent = "Latest changed paths: NOT_CHECKED";
    const historyLink = document.createElement("a");
    historyLink.href = "https://github.com/" + owner + "/" + name + "/commits/" + (name === "JOY" ? "main" : "master");
    historyLink.textContent = "Full change history";
    links.append(document.createTextNode(" · "), historyLink);
    section.append(heading, links, commit, served, evidence, changes);
    grid.appendChild(section);
    cards[name] = { commit: commit, served: served, evidence: evidence, changes: changes };
  });
  function central(date) {
    if (!date) return "date unavailable";
    const d = new Date(date);
    return Number.isNaN(d.getTime()) ? "date unavailable" :
      d.toLocaleString("en-US", {timeZone:"America/Chicago",year:"numeric",month:"short",day:"numeric",hour:"numeric",minute:"2-digit",timeZoneName:"short"});
  }
  async function jsonAt(url) {
    const resp = await fetch(url, {cache:"no-store", headers:{Accept:"application/vnd.github+json"}});
    if (!resp.ok) throw new Error("HTTP " + resp.status);
    return resp.json();
  }
  async function gitBlobSha1(bytes) {
    if (!globalThis.crypto?.subtle) throw new Error("browser SHA-1 unavailable");
    const prefix = new TextEncoder().encode("blob " + bytes.length + "\0");
    const input = new Uint8Array(prefix.length + bytes.length);
    input.set(prefix);
    input.set(bytes, prefix.length);
    const hash = new Uint8Array(await crypto.subtle.digest("SHA-1", input));
    return Array.from(hash, function (b) { return b.toString(16).padStart(2,"0"); }).join("");
  }
  async function check(name) {
    const card = cards[name];
    card.commit.textContent = "Source HEAD: CHECKING";
    card.changes.textContent = "Latest changed paths: CHECKING";
    card.served.textContent = "Public byte check: CHECKING";
    card.evidence.textContent = "Human visual acceptance: HOLD";
    try {
      const repoUrl = "https://api.github.com/repos/" + owner + "/" + name;
      const head = await jsonAt(repoUrl + "/commits/" + (name === "JOY" ? "main" : "master"));
      if (!head?.sha) throw new Error("No commit receipt");
      const sha = head.sha;
      const message = head.commit?.message?.split("\n")[0] || "message unavailable";
      card.commit.textContent = "Source HEAD: " + sha.slice(0,12) + " · " +
        central(head.commit?.committer?.date) + " · " + message;
      const changedFiles = Array.isArray(head.files) ? head.files : [];
      card.changes.replaceChildren(document.createTextNode("Latest changed paths: "));
      if (changedFiles.length === 0) card.changes.append(document.createTextNode("NOT_AVAILABLE"));
      changedFiles.slice(0,6).forEach(function (file, i) {
        if (i) card.changes.append(document.createTextNode(" · "));
        const link = document.createElement("a");
        link.href = "https://github.com/" + owner + "/" + name + "/blob/" + sha + "/" + file.filename.split("/").map(encodeURIComponent).join("/");
        link.textContent = file.filename;
        card.changes.append(link);
      });
      if (changedFiles.length > 6) card.changes.append(document.createTextNode(" · +" + (changedFiles.length - 6) + " more in commit history"));

      const detail = await jsonAt(repoUrl + "/contents/index.html?ref=" + encodeURIComponent(sha));
      if (!/^[a-f0-9]{40}$/i.test(detail.sha || "")) throw new Error("Missing committed blob SHA");
      const url = base + name + "/index.html?evidence_check=" + Date.now();
      const response = await fetch(url, {cache:"no-store"});
      if (!response.ok) throw new Error("Published HTTP " + response.status);
      const servedSha = await gitBlobSha1(new Uint8Array(await response.arrayBuffer()));
      if (servedSha.toLowerCase() === detail.sha.toLowerCase()) {
        card.served.textContent = "PUBLIC INDEX BYTES MATCH COMMIT · HTTP " + response.status;
        card.served.style.color = "#bfffd1";
        card.evidence.textContent = "Blob " + detail.sha.slice(0,12) + " matches published bytes. Visual acceptance: HUMAN_HOLD.";
      } else {
        card.served.textContent = "HOLD: LIVE INDEX DIFFERS FROM COMMITTED SOURCE";
        card.served.style.color = "#ffbaba";
        card.evidence.textContent = "Git blob " + detail.sha.slice(0,12) + " · served blob " + servedSha.slice(0,12) + ". Check deployment/cache before approval.";
      }
    } catch (err) {
      card.served.textContent = "HOLD: PUBLIC BYTE PROOF UNAVAILABLE";
      card.served.style.color = "#ffe2a1";
      card.evidence.textContent = "Check blocked: " + String(err.message || err).slice(0,90) + ". No inferred PASS.";
      if (card.commit.textContent === "Source HEAD: CHECKING") {
        card.commit.textContent = "Source HEAD: UNVERIFIED";
        card.changes.textContent = "Latest changed paths: HOLD";
      }
    }
  }
  async function schoolAudit() {
    const target = panel.querySelector("#wi-school-audit");
    const topDate = document.getElementById("wisdom-latest-audit");
    try {
      const data = await jsonAt(base + "JOY/docs/school-of-wisdom/compression-audit.latest.json?v=" + Date.now());
      if (!data.run_at || typeof data.queries_total !== "number") throw new Error("Invalid audit receipt");
      target.textContent = "School of Wisdom audit RECEIPT: " + central(data.run_at) +
        " · scoped checks " + data.queries_passed + "/" + data.queries_total +
        " · global standard " + (data.school_standard || "UNVERIFIED") +
        " · authority_created=" + String(data.authority_created) +
        " · audit is not approval.";
      if (topDate) topDate.textContent = central(data.run_at) + " · audit only";
    } catch (err) {
      target.textContent = "School of Wisdom audit receipt: HOLD — " + String(err.message || err).slice(0,90);
      if (topDate) topDate.textContent = "HOLD · receipt unavailable";
    }
  }
  const button = panel.querySelector("#wi-refresh");
  let busy = false;
  let lastCheck = 0;
  async function refresh() {
    if (busy) return;
    busy = true;
    button.disabled = true;
    try {
      await Promise.all(names.map(check).concat([schoolAudit()]));
      lastCheck = Date.now();
      panel.querySelector("#wi-checked").textContent = "Evidence checked " + central(new Date().toISOString()) +
        ". Recheck on page load or every 10 minutes while visible. Approval remains HUMAN_HOLD.";
    } finally {
      busy = false;
      button.disabled = false;
    }
  }
  button.addEventListener("click", refresh);
  document.addEventListener("visibilitychange", function () {
    if (!document.hidden && Date.now() - lastCheck > 600000) refresh();
  });
  setInterval(function () { if (!document.hidden && Date.now() - lastCheck > 600000) refresh(); }, 600000);
  refresh();
})();
