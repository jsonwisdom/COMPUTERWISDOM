"use strict";
(function () {
  const byId = (id) => document.getElementById(id);
  let projects = [];
  const safeRepoUrl = (input) => {
    try {
      const u = new URL(input);
      return u.protocol === "https:" && u.hostname === "github.com" && u.pathname.startsWith("/jsonwisdom/") ? u.href : null;
    } catch (_) { return null; }
  };
  const seen = (iso) => {
    if (typeof iso !== "string" || !iso.endsWith("Z")) return "Observation time not provided";
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return "Observation time not provided";
    return "Seen " + d.toISOString().replace("T", " ").slice(0, 16) + " UTC";
  };
  const node = (tag, className, text) => {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (text !== undefined) el.textContent = String(text);
    return el;
  };
  const link = (text, url) => {
    const el = node("a", "", text);
    const safe = safeRepoUrl(url);
    if (safe) el.href = safe;
    else el.removeAttribute("href");
    el.rel = "noopener noreferrer";
    return el;
  };
  function renderProjects() {
    const q = byId("search").value.trim().toLocaleLowerCase();
    const filter = byId("size-filter").value;
    const visible = projects.filter((p) => {
      if (q && !p.name.toLocaleLowerCase().includes(q) && !p.repository.toLocaleLowerCase().includes(q)) return false;
      if (filter === "nonempty" && !p.nonempty) return false;
      if (filter === "empty" && p.nonempty) return false;
      return true;
    });
    byId("result-count").textContent = "Showing " + visible.length + " of " + projects.length + " public repositories.";
    const cards = visible.map((p) => {
      const card = node("article", "project-card");
      const tag = node("div", "card-top", "PUBLIC · GITHUB");
      const title = node("h3");
      title.append(link(p.name, p.url));
      const description = node("p", "", p.nonempty ? "Repository contains files · " + p.size_kb + " KB reported" : "Empty repository · available for a new build");
      const time = node("p", "", seen(p.last_seen_utc));
      const commitLabel = p.last_commit_utc
        ? "Default-branch commit: " + p.last_commit_utc.replace("T", " ").replace("Z", " UTC")
        : "No default-branch commit recorded";
      const commit = node("p", "commit-date", commitLabel);
      const evidence = p.last_commit_url && p.last_commit_sha
        ? link("Source commit " + p.last_commit_sha.slice(0, 9) + " ↗", p.last_commit_url)
        : node("span", "tag", "No commit source available");
      card.append(tag, title, description, time, commit, evidence);
      return card;
    });
    if (!cards.length) cards.push(node("p", "empty-state", "No public repositories match this search. Clear the filter to explore the full index."));
    byId("projects-list").replaceChildren(...cards);
  }
  function renderForest(data) {
    const canonical = new Set(data.canonical_states);
    if (!Array.isArray(data.trees) || !Array.isArray(data.groves)) throw new Error("Invalid forest dataset");
    if (new Set(data.trees.map((t) => t.id)).size !== data.trees.length) throw new Error("Duplicate tree ID");
    if (data.trees.some((t) => !canonical.has(t.state))) throw new Error("Unknown canonical tree state");
    const pending = data.trees.filter((t) => t.root === "PENDING_HASH").length;
    byId("tree-count").textContent = String(data.trees.length);
    byId("forest-summary").textContent = data.trees.length + " source-defined trees · " + data.groves.length + " groves · " + pending + " roots pending · 0 computed roots claimed.";
    const cards = data.trees.map((t) => {
      const card = node("article", "tree-card");
      card.append(node("span", "pending", t.state + " / " + t.root));
      card.append(node("h3", "", t.id.replace(/^TREE_/, "").replaceAll("_", " ")));
      card.append(node("p", "", "Source path: " + t.path));
      card.append(node("p", "", t.work_item));
      card.append(link("Inspect source path ↗", t.url));
      return card;
    });
    byId("forest-list").replaceChildren(...cards);
  }
  async function load() {
    try {
      const [pResp, fResp] = await Promise.all([fetch("./projects.json", {cache:"no-store"}), fetch("./forest.json", {cache:"no-store"})]);
      if (!pResp.ok || !fResp.ok) throw new Error("Snapshot files unavailable");
      const [pData, fData] = await Promise.all([pResp.json(), fResp.json()]);
      if (pData.schema !== "computerwisdom.frontdoor.projects.v0.4" || fData.schema !== "computerwisdom.frontdoor.forest.v0.4") throw new Error("Dataset schema mismatch");
      if (!Array.isArray(pData.projects) || pData.public_count !== pData.projects.length) throw new Error("Inventory count mismatch");
      if (new Set(pData.projects.map((p) => p.repository)).size !== pData.projects.length) throw new Error("Duplicate repository");
      if (pData.projects.some((p) => p.visibility !== "public" || !safeRepoUrl(p.url))) throw new Error("Non-public or invalid project source");
      if (pData.projects.some((p) => (p.nonempty && (!p.last_commit_utc || !p.last_commit_sha || !safeRepoUrl(p.last_commit_url))) || (!p.nonempty && p.last_commit_utc !== null))) throw new Error("Missing or invalid default-branch commit provenance");
      projects = pData.projects;
      byId("repo-count").textContent = String(projects.length);
      byId("private-count").textContent = String(pData.private_excluded_count);
      const dated = projects.filter((p) => p.last_commit_utc !== null).length;
      byId("snapshot").textContent = "GitHub inventory observation: " + seen(pData.snapshot_utc) + ". Default-branch commit metadata: " + dated + " of " + projects.filter((p) => p.nonempty).length + " nonempty public repositories. Private identities excluded.";
      renderProjects();
      renderForest(fData);
    } catch (error) {
      byId("result-count").textContent = "Snapshot cannot load: " + error.message + ". Serve this directory over HTTP (for example, python3 -m http.server 8000).";
      byId("forest-summary").textContent = "Forest data unavailable.";
    }
  }
  byId("search").addEventListener("input", renderProjects);
  byId("size-filter").addEventListener("change", renderProjects);
  load();
})();
