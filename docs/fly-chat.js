/* The-fly wiki chat — attaches to original fly-brain UI without replacing it */
(function(){
  if (window.__flyChatLoaded) return;
  window.__flyChatLoaded = true;

  const style = document.createElement("style");
  style.textContent = `
#flyChat{position:fixed;right:12px;bottom:130px;z-index:30;width:min(360px,calc(100vw - 24px));max-height:min(420px,calc(100vh - 200px));display:flex;flex-direction:column;background:rgba(8,12,8,.97);border:1px solid var(--line,#1a261a);backdrop-filter:blur(12px)}
#flyChat.collapsed{max-height:42px;overflow:hidden}
#flyChat .ch-h{display:flex;justify-content:space-between;align-items:center;padding:8px 10px;border-bottom:1px solid var(--line,#1a261a);cursor:pointer;color:var(--g,#5dba4a);font-size:11px;letter-spacing:.08em;text-transform:uppercase}
#flyChat .ch-h button{border:none;background:none;color:var(--mute,#5a6a5a);cursor:pointer;font-size:14px}
#flyChatLog{flex:1;overflow:auto;padding:10px;display:flex;flex-direction:column;gap:8px;min-height:120px;max-height:280px}
#flyChatLog .m{padding:8px 10px;border-radius:6px;font-size:11.5px;line-height:1.5;white-space:pre-wrap}
#flyChatLog .m.u{align-self:flex-end;background:#122012;border:1px solid #1e2e1e}
#flyChatLog .m.b{align-self:flex-start;background:#0a0e0a;border:1px solid var(--line,#1a261a);color:var(--text,#c4d0c4)}
#flyChatLog .m .src{margin-top:6px;color:var(--mute,#5a6a5a);font-size:10px}
#flyChatForm{display:flex;gap:6px;padding:8px;border-top:1px solid var(--line,#1a261a)}
#flyChatForm input{flex:1;background:#060906;border:1px solid var(--line,#1a261a);color:var(--text,#c4d0c4);font:inherit;padding:7px 9px}
#flyChatForm button{border:1px solid #3a5a3a;color:var(--g,#5dba4a);background:transparent;padding:6px 10px;cursor:pointer}
#flyChatStatus{padding:4px 10px 8px;font-size:10px;color:var(--mute,#5a6a5a)}
#flyChatStatus.ok{color:var(--g,#5dba4a)}
`;
  document.head.appendChild(style);

  const panel = document.createElement("div");
  panel.id = "flyChat";
  panel.innerHTML = `
    <div class="ch-h" id="flyChatToggle"><span>🪰 fly chat · wiki</span><button type="button" id="flyChatMin">–</button></div>
    <div id="flyChatLog"></div>
    <form id="flyChatForm"><input id="flyChatQ" type="text" placeholder="ex: comment vole la mouche ?" autocomplete="off"/><button type="submit">→</button></form>
    <div id="flyChatStatus">chargement…</div>`;
  document.body.appendChild(panel);

  const RAW = (typeof window.RAW === "string" && window.RAW) || "https://raw.githubusercontent.com/glowku/The-fly/main";
  const API_CANDIDATES = ["http://127.0.0.1:8765","http://localhost:8765"];
  let apiBase = null;
  const logEl = document.getElementById("flyChatLog");
  const stEl = document.getElementById("flyChatStatus");
  const form = document.getElementById("flyChatForm");
  const input = document.getElementById("flyChatQ");

  const FR_MAP = {
    vol:["flight","wing","hover","aerodynamic","insect flight","haltere","halteres"],
    vole:["flight","fly","wing","hover"],
    voler:["flight","fly","wing","hover"],
    mouche:["fly","flies","diptera","housefly","fruit fly","drosophila"],
    mouches:["fly","flies","diptera"],
    aile:["wing","insect wing","haltere","flight"],
    ailes:["wing","insect wing","haltere"],
    haltere:["haltere","halteres","insect flight"],
    halteres:["haltere","halteres","insect flight"],
    insecte:["insect","insects","entomology","arthropod"],
    insectes:["insect","insects","entomology"],
    evolution:["evolution","evolution of insects","adaptation"],
    "évolution":["evolution","evolution of insects","adaptation"],
    ecologie:["ecology","insect ecology","pollination"],
    "écologie":["ecology","insect ecology","pollination"],
    comportement:["behavior","behaviour","mating","swarm"],
    larve:["larva","maggot"],
    yeux:["compound eye","arthropod eye"],
    antenne:["antenna","antenna (zoology)"],
    pollinisation:["pollination"],
    essaim:["swarm","swarm behaviour"],
    thorax:["thorax"],
    exosquelette:["exoskeleton"]
  };

  function addMsg(role, text){
    const d = document.createElement("div");
    d.className = "m " + (role === "user" ? "u" : "b");
    d.textContent = text;
    logEl.appendChild(d);
    logEl.scrollTop = logEl.scrollHeight;
    return d;
  }

  function expandQuery(q){
    const raw = (q || "").toLowerCase();
    const words = raw.split(/[^a-z0-9àâäéèêëïîôùûüç]+/).filter(w => w.length > 1);
    const terms = new Set(words);
    for (const w of words) {
      const mapped = FR_MAP[w];
      if (mapped) mapped.forEach(t => terms.add(t.toLowerCase()));
    }
    if ([...terms].some(t => ["vol","vole","voler","mouche","mouches","aile","flight","fly"].includes(t))) {
      ["insect flight","haltere","wing","fly","diptera"].forEach(t => terms.add(t));
    }
    return [...terms];
  }

  function scoreTitle(title, terms){
    const t = (title || "").toLowerCase();
    let sc = 0;
    for (const w of terms) {
      if (t === w) sc += 6;
      else if (t.includes(w)) sc += 3;
      else {
        const parts = w.split(/\s+/);
        if (parts.length > 1 && parts.every(p => t.includes(p))) sc += 4;
      }
    }
    if (/flight|haltere|wing|fly|diptera|hover|aerodynam/i.test(t)) sc += 1.5;
    return sc;
  }

  function collectTitles(){
    const titles = new Set();
    if (typeof articles !== "undefined" && Array.isArray(articles)) {
      articles.forEach(a => a && a.title && titles.add(a.title));
    }
    if (typeof coverage !== "undefined" && coverage && coverage.nodes) {
      Object.keys(coverage.nodes).forEach(t => titles.add(t));
    }
    ["Insect flight","Halteres","Haltere","Fly","Wing","Aerodynamics","Hover","Diptera","Insect"].forEach(t => titles.add(t));
    return [...titles];
  }

  async function fetchWiki(title){
    const file = encodeURIComponent(title) + ".md";
    const urls = [`${RAW}/wiki/${file}`];
    for (const u of urls) {
      try {
        const r = await fetch(u + "?t=" + Date.now());
        if (r.ok) return await r.text();
      } catch (e) {}
    }
    return "";
  }

  function pickSnippets(md, terms, maxChars){
    maxChars = maxChars || 900;
    if (!md) return "";
    const lines = md.split(/\n+/).map(l => l.trim()).filter(l => l && !l.startsWith("#") && l.length > 40);
    const scored = lines.map(l => {
      const low = l.toLowerCase();
      let s = 0;
      for (const w of terms) if (low.includes(w)) s += 2;
      if (/flight|wing|haltere|insect|fly|aerodynam|hover/i.test(low)) s += 1;
      return { l, s };
    }).filter(x => x.s > 0).sort((a, b) => b.s - a.s);
    const out = [];
    let n = 0;
    for (const x of scored) {
      out.push("• " + x.l.replace(/^[-*]\s*/, "").slice(0, 280));
      n += x.l.length;
      if (n >= maxChars || out.length >= 5) break;
    }
    if (!out.length) {
      for (const l of lines.slice(0, 4)) {
        out.push("• " + l.slice(0, 280));
        if (out.join(" ").length > maxChars) break;
      }
    }
    return out.join("\n");
  }

  async function extractiveAnswer(q){
    const terms = expandQuery(q);
    const titles = collectTitles();
    let scored = titles.map(title => ({ title, sc: scoreTitle(title, terms) })).filter(x => x.sc > 0);
    scored.sort((a, b) => b.sc - a.sc);
    let top = scored.slice(0, 5);
    if (!top.length) {
      const fb = ["Insect flight","Halteres","Fly","Wing","Hover"].filter(t =>
        titles.some(x => x.toLowerCase() === t.toLowerCase() || x.toLowerCase().includes(t.toLowerCase()))
      );
      top = fb.map(t => ({ title: t, sc: 1 }));
    }
    if (!top.length) {
      return { answer: "Pas d'article assez proche. Essaie « insect flight », « haltere », « fly ».", sources: [] };
    }
    const chunks = [];
    const used = [];
    for (const item of top.slice(0, 3)) {
      const md = await fetchWiki(item.title);
      const sn = pickSnippets(md, terms);
      used.push(item.title);
      if (sn) chunks.push("【" + item.title + "】\n" + sn);
    }
    const answer = chunks.length
      ? ("D’après le noyau wiki The-fly :\n\n" + chunks.join("\n\n"))
      : ("Nœuds proches :\n" + top.map(x => "• " + x.title).join("\n"));
    return { answer, sources: used };
  }

  async function probeAPI(){
    for (const base of API_CANDIDATES) {
      try {
        const r = await fetch(base + "/health", { signal: AbortSignal.timeout(700) });
        if (r.ok) {
          apiBase = base;
          stEl.textContent = "LLM local OK · " + base;
          stEl.className = "ok";
          return true;
        }
      } catch (e) {}
    }
    apiBase = null;
    stEl.textContent = "mode wiki — extraits des articles appris";
    stEl.className = "";
    return false;
  }

  document.getElementById("flyChatToggle").addEventListener("click", function(e){
    if (e.target.id === "flyChatMin") return;
    panel.classList.toggle("collapsed");
  });
  document.getElementById("flyChatMin").addEventListener("click", function(e){
    e.stopPropagation();
    panel.classList.toggle("collapsed");
    e.target.textContent = panel.classList.contains("collapsed") ? "+" : "–";
  });

  form.addEventListener("submit", async function(ev){
    ev.preventDefault();
    const q = (input.value || "").trim();
    if (!q) return;
    input.value = "";
    addMsg("user", q);
    const pending = addMsg("bot", "…");
    try {
      if (!apiBase) await probeAPI();
      let res;
      if (apiBase) {
        const r = await fetch(apiBase + "/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: q, use_arxiv: true, k: 6 })
        });
        res = await r.json();
      } else {
        res = await extractiveAnswer(q);
      }
      pending.textContent = res.answer || JSON.stringify(res);
      const srcs = (res.sources || []).slice(0, 6);
      if (srcs.length) {
        const s = document.createElement("div");
        s.className = "src";
        s.textContent = "sources: " + srcs.join(" · ");
        pending.appendChild(s);
      }
      if (res.arxiv && res.arxiv.length) {
        const s = document.createElement("div");
        s.className = "src";
        s.textContent = "arXiv: " + res.arxiv.slice(0, 3).map(p => p.title).join(" · ");
        pending.appendChild(s);
      }
    } catch (err) {
      pending.textContent = "Erreur: " + err.message;
    }
  });

  addMsg("bot", "Question sur le graphe (ex: « comment vole la mouche ? »). Réponse ancrée dans les articles wiki.");
  setTimeout(probeAPI, 800);
  setTimeout(probeAPI, 2500);
})();
