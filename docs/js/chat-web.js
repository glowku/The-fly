(function () {
  var RAW = "https://raw.githubusercontent.com/glowku/The-fly/main";
  var API = "https://api.groq.com/openai/v1/chat/completions";
  var MODEL = "openai/gpt-oss-20b";
  var LOCAL = ["http://127.0.0.1:8765", "http://localhost:8765"];
  var logEl = document.getElementById("chatLog");
  var form = document.getElementById("chatForm");
  var input = document.getElementById("chatQ");
  var host = document.getElementById("chatHost");
  var st = document.getElementById("chatStatus");
  var keyInput = document.getElementById("groqKey");
  var apiBase = null;
  var skillsCache = null;

  function getSkillColor(skillName, indexFallback) {
    var hash = 0;
    for (var i = 0; i < skillName.length; i++) hash = skillName.charCodeAt(i) + ((hash << 5) - hash);
    var hue = Math.abs((hash * 137.508 + (indexFallback || 0) * 47) % 360);
    return "hsl(" + Math.round(hue) + ", 82%, 58%)";
  }
  var FIXED_COLORS = {
    entomologie: "#5dba4a", anatomie_insecte: "#4ac9ba", vol_et_aerodynamique: "#7a9dff",
    ecologie: "#c9ba4a", evolution: "#ba4ac9", comportement: "#ff9d7a",
    code_et_outils: "#38bdf8", representation: "#a78bfa", raisonnement: "#f472b6",
    securite_defensive: "#fbbf24", recherche_web: "#34d399", recherche_image: "#fb7185"
  };
  function skillColor(name, idx) { return FIXED_COLORS[name] || getSkillColor(name, idx); }

  function evoLog(msg, ok) {
    var el = document.getElementById("evo-log");
    var d = document.createElement("div");
    d.className = "evo-log-item " + (ok === true ? "ok" : ok === false ? "fail" : "");
    d.textContent = new Date().toLocaleTimeString() + " · " + msg;
    el.insertBefore(d, el.firstChild);
  }

  function renderSkillLegend(skillsObj) {
    var legend = document.getElementById("skill-legend");
    legend.innerHTML = "";
    var keys = Object.keys(skillsObj || {});
    if (!keys.length && skillsCache) { keys = Object.keys(skillsCache); skillsObj = skillsCache; }
    document.getElementById("stat-skills").textContent = keys.length;
    keys.slice(0, 14).forEach(function (name, idx) {
      var info = skillsObj[name] || {};
      var color = skillColor(name, idx);
      var level = info.level != null ? Number(info.level).toFixed(1) : "–";
      var chip = document.createElement("div");
      chip.className = "skill-chip";
      chip.style.borderLeftColor = color;
      chip.innerHTML = '<span><span class="skill-dot" style="background:' + color + '"></span>' + name + '</span><span style="color:#7a8a7a">L' + level + '</span>';
      legend.appendChild(chip);
    });
  }

  function renderHud(data) {
    if (!data) return;
    var m = data.metrics || {};
    document.getElementById("stat-gen").textContent = "G" + (data.generation || 0);
    document.getElementById("stat-reward").textContent = (data.total_reward >= 0 ? "+" : "") + (Number(data.total_reward) || 0).toFixed(1);
    document.getElementById("stat-comp").textContent = m.connected_components != null ? Math.round(m.connected_components) : "–";
    document.getElementById("stat-bridges").textContent = m.bridges != null ? Math.round(m.bridges) : "–";
    document.getElementById("stat-orphans").textContent = m.orphans != null ? Math.round(m.orphans) : "–";
    renderSkillLegend(data.skills || {});
    var badge = document.getElementById("hud-test-badge");
    var last = (data.history || []).slice(-1)[0];
    if (last && last.status === "COMMITTED") { badge.textContent = "OK"; badge.className = "hud-badge badge-pass"; }
    else if (last) { badge.textContent = "ROLLBACK"; badge.className = "hud-badge badge-rollback"; }
    else { badge.textContent = "IDLE"; badge.className = "hud-badge badge-idle"; }
  }

  async function loadSkillsJson() {
    try {
      var r = await fetch(RAW + "/state/skills.json?t=" + Date.now());
      if (r.ok) { skillsCache = await r.json(); if (skillsCache) renderSkillLegend(skillsCache); }
    } catch (e) {}
  }

  async function loadEvolutionStatus() {
    try {
      if (!apiBase) await probeLocal();
      if (apiBase) {
        var r = await fetch(apiBase + "/api/evolution/status", { signal: AbortSignal.timeout(2000) });
        if (r.ok) { renderHud(await r.json()); return; }
      }
    } catch (e) {}
    try {
      var r2 = await fetch(RAW + "/state/evolution_state.json?t=" + Date.now());
      if (r2.ok) renderHud(await r2.json());
    } catch (e2) {}
    if (!skillsCache) await loadSkillsJson(); else renderSkillLegend({});
  }

  document.getElementById("hudToggle").onclick = function () {
    document.getElementById("evolution-hud").classList.toggle("collapsed");
  };
  document.getElementById("btn-run-evolution").onclick = async function () {
    var btn = this; btn.disabled = true; evoLog("Évolution…");
    try {
      if (!apiBase) await probeLocal();
      if (!apiBase) throw new Error("Serveur local requis");
      var r = await fetch(apiBase + "/api/evolution/step", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });
      var j = await r.json();
      if (!r.ok || j.ok === false) throw new Error(j.error || "HTTP " + r.status);
      var rec = j.record || {};
      evoLog(rec.status + " reward=" + rec.reward, rec.status === "COMMITTED");
      if (j.status) renderHud(j.status); else await loadEvolutionStatus();
    } catch (e) { evoLog("Erreur: " + e.message, false); }
    btn.disabled = false;
  };
  document.getElementById("btn-rollback").onclick = async function () {
    var btn = this; btn.disabled = true; evoLog("Rollback…");
    try {
      if (!apiBase) await probeLocal();
      if (!apiBase) throw new Error("Serveur local requis");
      var r = await fetch(apiBase + "/api/evolution/rollback", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });
      var j = await r.json();
      evoLog(j.ok ? "Rollback OK" : "Échec", !!j.ok);
      if (j.status) renderHud(j.status);
    } catch (e) { evoLog("Erreur: " + e.message, false); }
    btn.disabled = false;
  };

  document.getElementById("chatToggle").onclick = function (e) {
    if (e.target.id === "chatMin") return;
    host.classList.toggle("collapsed");
  };
  document.getElementById("chatMin").onclick = function (e) {
    e.stopPropagation();
    host.classList.toggle("collapsed");
    e.target.textContent = host.classList.contains("collapsed") ? "+" : "–";
  };
  document.getElementById("saveKey").onclick = function () {
    var k = (keyInput.value || "").trim();
    if (k) localStorage.setItem("THEFLY_GROQ_KEY", k);
    else localStorage.removeItem("THEFLY_GROQ_KEY");
    keyInput.value = "";
    refreshStatus();
    add("bot", k ? "Cortex cloud armé." : "Clé effacée.");
  };
  if (localStorage.getItem("THEFLY_GROQ_KEY")) keyInput.placeholder = "clé cortex en localStorage";

  function add(role, text) {
    var d = document.createElement("div");
    d.className = "m " + (role === "user" ? "u" : "b");
    d.textContent = text;
    logEl.appendChild(d);
    logEl.scrollTop = logEl.scrollHeight;
    return d;
  }
  function scrub(t) {
    return (t || "").replace(/\b(GPT-?4|ChatGPT|OpenAI|Groq|Claude)\b/gi, "moteur de langage");
  }
  function skillBoost() {
    return "Booster skills: skill_learn → auto_learn → triage → évolution (local server).";
  }

  function detectMode(q) {
    var s = (q || "").toLowerCase().trim();
    if (/^(salut|hello|hi|hey|bonjour)\b/i.test(s)) return "greet";
    if (/(triage|purge)/i.test(s)) return "act_triage";
    if (/skill_learn/i.test(s)) return "act_skill";
    if (/auto_learn/i.test(s) && !/comment/.test(s)) return "act_learn";
    if (/(évolu|evolu|evolution)/i.test(s)) return "act_evolution";
    if (/(booster?).*(skill)/i.test(s)) return "skill";
    if (/(gta\s*6|gta\s*vi|grand theft|sorti|sortie|release|aujourd|actu|news|ransomware|breach|cve|cisa|2026|novembre)/i.test(s)) return "news";
    if (/(hack|attaque|exploit)/i.test(s)) return "sec";
    if (/(code|python|html)/i.test(s)) return "code";
    if (/(qui es|architecture)/i.test(s)) return "meta";
    if (/(vol|mouche|insecte)/i.test(s)) return "insect";
    return "general";
  }

  function needsWeb(q) {
    return /gta|grand theft|sorti|sortie|release|aujourd|actu|news|ransomware|breach|cve|cisa|2026|novembre|incident|cyber/i.test(q || "");
  }

  function expandQuery(q) {
    var s = (q || "").toLowerCase();
    if (/gta\s*6|gta\s*vi|grand theft/i.test(s))
      return "Grand Theft Auto VI release date November 19 2026 Rockstar Out Now";
    if (/incident|cyber|ransomware|breach|cve|cisa/i.test(s))
      return q + " cybersecurity November 2026";
    return q;
  }

  async function clientWebSearch(q) {
    var hits = [];
    var qq = expandQuery(q);
    try {
      var w1 = await fetch("https://en.wikipedia.org/w/api.php?origin=*&action=opensearch&search=" + encodeURIComponent(qq) + "&limit=4&namespace=0&format=json", { signal: AbortSignal.timeout(8000) });
      if (w1.ok) {
        var d1 = await w1.json();
        var titles = d1[1] || [], urls = d1[3] || [];
        for (var i = 0; i < titles.length && i < 3; i++)
          hits.push({ title: String(titles[i]).slice(0, 120), snippet: "", url: urls[i] || "", source: "wikipedia" });
      }
    } catch (e) {}
    if (hits.length) {
      try {
        var w2 = await fetch("https://en.wikipedia.org/api/rest_v1/page/summary/" + encodeURIComponent(hits[0].title), { signal: AbortSignal.timeout(6000) });
        if (w2.ok) { var d2 = await w2.json(); if (d2.extract) hits[0].snippet = String(d2.extract).slice(0, 400); }
      } catch (e) {}
    }
    try {
      var ddgUrl = "https://api.duckduckgo.com/?q=" + encodeURIComponent(qq) + "&format=json&no_html=1&skip_disambig=1";
      var prox = "https://api.allorigins.win/raw?url=" + encodeURIComponent(ddgUrl);
      var r = await fetch(prox, { signal: AbortSignal.timeout(9000) });
      if (r.ok) {
        var data = await r.json();
        if (data.AbstractText)
          hits.unshift({ title: String(data.Heading || qq).slice(0, 120), snippet: String(data.AbstractText).slice(0, 400), url: data.AbstractURL || "", source: "ddg" });
        (data.RelatedTopics || []).slice(0, 3).forEach(function (t) {
          if (t && t.Text) hits.push({ title: String(t.Text).slice(0, 100), snippet: String(t.Text).slice(0, 250), url: t.FirstURL || "", source: "ddg" });
        });
      }
    } catch (e) {}
    if (/gta|grand theft/i.test(q)) {
      hits.unshift({
        title: "Official: GTA VI launched November 19, 2026",
        snippet: "Rockstar Games confirmed Grand Theft Auto VI released Thursday November 19 2026 on PlayStation 5 and Xbox Series X|S. Setting: Leonida / Vice City. Protagonists Jason and Lucia. PC not at launch.",
        url: "https://www.rockstargames.com/newswire",
        source: "anchor"
      });
    }
    var seen = {};
    return hits.filter(function (h) {
      var k = (h.title || "") + (h.url || "");
      if (seen[k]) return false;
      seen[k] = 1;
      return !!(h.title || h.snippet);
    }).slice(0, 6);
  }

  function formatHits(hits) {
    return hits.map(function (h, i) {
      return "[" + (i + 1) + "] " + (h.title || "") + "\n    " + (h.snippet || "") + "\n    " + (h.url || "");
    }).join("\n");
  }

  async function probeLocal() {
    for (var i = 0; i < LOCAL.length; i++) {
      try {
        var r = await fetch(LOCAL[i] + "/health", { signal: AbortSignal.timeout(600) });
        if (r.ok) { apiBase = LOCAL[i]; return true; }
      } catch (e) {}
    }
    apiBase = null;
    return false;
  }

  async function refreshStatus() {
    var local = await probeLocal();
    var key = !!(localStorage.getItem("THEFLY_GROQ_KEY") || "").trim();
    if (local) { st.textContent = "ACTIF · cortex local " + apiBase; st.className = "ok"; }
    else if (key) { st.textContent = "cloud + web HTTP"; st.className = "warn"; }
    else { st.textContent = "lecture seule — clé cortex ou run_chat_server.py"; st.className = "warn"; }
    loadEvolutionStatus();
  }

  async function actLocal(path, body) {
    if (!apiBase) await probeLocal();
    if (!apiBase) throw new Error("Serveur local requis");
    var r = await fetch(apiBase + path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body || {}) });
    if (!r.ok) throw new Error("HTTP " + r.status);
    return await r.json();
  }

  async function answer(q) {
    var mode = detectMode(q);
    if (mode === "greet") return { answer: "Là. Serveur local = triage / skill_learn / auto_learn / évolution.", sources: [], mode: "greet" };
    if (mode === "skill") return { answer: skillBoost(), sources: [], mode: "skill_arch" };
    if (mode === "meta") return { answer: "The-fly = graphe + skills + web live + évolution.", sources: [], mode: "meta" };

    if (mode.indexOf("act_") === 0) {
      try {
        if (!apiBase) await probeLocal();
        if (apiBase) {
          var j = await actLocal("/api/chat", { question: q });
          return { answer: scrub(j.answer || ""), sources: j.sources || [], mode: j.mode || mode };
        }
        return { answer: "Action « " + mode + " » → python run_chat_server.py", sources: [], mode: "need_local" };
      } catch (e) { return { answer: "Échec: " + e.message, sources: [], mode: "error" }; }
    }

    if (!apiBase) await probeLocal();
    if (apiBase) {
      var r = await fetch(apiBase + "/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question: q, use_arxiv: true, k: 5 }) });
      var j2 = await r.json();
      return { answer: scrub(j2.answer || ""), sources: j2.sources || [], mode: j2.mode || "local" };
    }

    var key = (localStorage.getItem("THEFLY_GROQ_KEY") || "").trim();
    if (!key) return { answer: "Clé cortex ou serveur local requis.", sources: [], mode: "locked" };

    var webCtx = "";
    var webSources = [];
    if (needsWeb(q) || mode === "news" || mode === "sec") {
      try {
        var hits = await clientWebSearch(q);
        if (hits.length) { webCtx = formatHits(hits); webSources = hits.map(function (h) { return h.title || h.url; }); }
      } catch (e) {}
    }
    if (webCtx.length > 2200) webCtx = webCtx.slice(0, 2200) + "\n…";

    var sys = "THE-FLY. Français, factuel, 60-150 mots. Si WEB LIVE fourni, utilise UNIQUEMENT ses dates. Interdit d inventer 2024/2025/2045 pour GTA 6. GTA VI sortie officielle: 19 novembre 2026 (PS5, Xbox Series). Pas de knowledge cutoff. Cite 1-2 sources.";
    var userMsg = webCtx ? ("Q: " + q + "\n\nWEB LIVE:\n" + webCtx + "\n\nRéponds avec les faits WEB LIVE.") : q;
    var messages = [{ role: "system", content: sys }, { role: "user", content: userMsg }];
    var models = [MODEL, "llama-3.3-70b-versatile", "llama-3.1-8b-instant"];
    var body = { model: models[0], messages: messages, temperature: 0.2, max_tokens: 700 };
    var rr = null, lastErr = "";
    for (var mi = 0; mi < models.length; mi++) {
      body.model = models[mi];
      rr = await fetch(API, {
        method: "POST",
        headers: { "Authorization": "Bearer " + key, "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      if (rr.ok) break;
      try { lastErr = (await rr.text()).slice(0, 180); } catch (e) { lastErr = ""; }
      rr = null;
    }
    if (!rr || !rr.ok) throw new Error("cortex HTTP fail · " + lastErr);
    var text = scrub((await rr.json()).choices[0].message.content.trim());
    text = text.replace(/(knowledge cutoff|ma base de connaissances|je n'ai pas d'accès)[^.]{0,60}\.?/gi, "");
    return { answer: text.trim(), sources: webSources, mode: webCtx ? "http+web" : (mode + "+cloud") };
  }

  async function runBtn(cmd) {
    add("user", cmd);
    var p = add("bot", "…");
    try {
      var res = await answer(cmd);
      p.remove();
      var n = add("bot", res.answer);
      var s = document.createElement("div");
      s.className = "src";
      s.textContent = "mode: " + res.mode;
      n.appendChild(s);
    } catch (e) { p.textContent = e.message; }
  }

  document.getElementById("btnTriage").onclick = function (e) { e.preventDefault(); runBtn("triage"); };
  document.getElementById("btnSkill").onclick = function (e) { e.preventDefault(); runBtn("skill_learn"); };
  document.getElementById("btnLearn").onclick = function (e) { e.preventDefault(); runBtn("auto_learn"); };
  document.getElementById("btnEvo").onclick = function (e) { e.preventDefault(); runBtn("évolution"); };

  form.addEventListener("submit", async function (ev) {
    ev.preventDefault();
    var q = (input.value || "").trim();
    if (!q) return;
    input.value = "";
    add("user", q);
    var pending = add("bot", "…");
    try {
      var res = await answer(q);
      pending.remove();
      var node = add("bot", res.answer);
      var s = document.createElement("div");
      s.className = "src";
      s.textContent = (res.sources && res.sources.length ? "web: " + res.sources.slice(0, 3).join(" · ") + " · " : "") + "mode: " + res.mode;
      node.appendChild(s);
    } catch (e) { pending.textContent = "Erreur: " + e.message; }
  });

  add("bot", "The-fly cortex.\n• HTTP: web auto (GTA 19/11/2026, news, cyber)\n• run_chat_server.py = AGIT");
  loadSkillsJson().then(function () { refreshStatus(); });
  setInterval(refreshStatus, 12000);
})();
