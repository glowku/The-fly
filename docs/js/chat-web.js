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
  var history = [];
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
      var level = info.level != null ? Number(info.level).toFixed(1) : (info.reward != null ? info.reward : "–");
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
    if (last) {
      if (last.status === "COMMITTED") { badge.textContent = "OK"; badge.className = "hud-badge badge-pass"; }
      else { badge.textContent = "ROLLBACK"; badge.className = "hud-badge badge-rollback"; }
    } else { badge.textContent = "IDLE"; badge.className = "hud-badge badge-idle"; }
  }

  async function loadSkillsJson() {
    try {
      var r = await fetch(RAW + "/state/skills.json?t=" + Date.now());
      if (r.ok) { skillsCache = await r.json(); if (skillsCache && Object.keys(skillsCache).length) renderSkillLegend(skillsCache); }
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
    var btn = this; btn.disabled = true; evoLog("Évolution en cours…");
    try {
      if (!apiBase) await probeLocal();
      if (!apiBase) throw new Error("Serveur local requis (run_chat_server.py)");
      var r = await fetch(apiBase + "/api/evolution/step", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) });
      var j = await r.json();
      if (!r.ok || j.ok === false) throw new Error(j.error || "HTTP " + r.status);
      var rec = j.record || {};
      evoLog(rec.status + " reward=" + rec.reward + " gen=" + rec.generation, rec.status === "COMMITTED");
      if (j.status) renderHud(j.status); else await loadEvolutionStatus();
    } catch (e) { evoLog("Erreur: " + e.message, false); }
    btn.disabled = false;
  };

  document.getElementById("btn-rollback").onclick = async function () {
    var btn = this; btn.disabled = true; evoLog("Rollback…");
    try {
      if (!apiBase) await probeLocal();
      if (!apiBase) throw new Error("Serveur local requis");
      var r = await fetch(apiBase + "/api/evolution/rollback", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) });
      var j = await r.json();
      evoLog(j.ok ? "Rollback OK → " + (j.checkpoint_id || "?") : "Rollback échoué", !!j.ok);
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
    if (role === "bot" && text.indexOf("```") >= 0) {
      var parts = text.split(/```/);
      d.innerHTML = "";
      parts.forEach(function (p, i) {
        if (i % 2 === 0) d.appendChild(document.createTextNode(p));
        else { var pre = document.createElement("pre"); pre.textContent = p.replace(/^\w*\n/, ""); d.appendChild(pre); }
      });
    } else d.textContent = text;
    logEl.appendChild(d);
    logEl.scrollTop = logEl.scrollHeight;
    return d;
  }

  function scrub(t) {
    return (t || "").replace(/\b(GPT-?4|ChatGPT|OpenAI|Groq|Claude)\b/gi, "moteur de langage");
  }

  function skillBoost() {
    return ["Booster skills = faire tourner l'organisme :",
      "1. skill_learn → skill_notes/ + levels",
      "2. auto_learn → nouveaux nœuds insecte filtrés",
      "3. triage → TRIE vers quarantine.json",
      "4. évolution → densify + learn sous tests + rollback",
      "5. python run_chat_server.py : boutons AGISSENT"].join("\n");
  }

  function detectMode(q) {
    var s = (q || "").toLowerCase().trim();
    if (/^(salut|hello|hi|hey|bonjour|t'es la|tes la|yo)\b/i.test(s)) return "greet";
    if (/(triage|purge|nettoie|trie les)/i.test(s)) return "act_triage";
    if (/^(skill_learn|lance skill|run skill)/i.test(s) || s === "skill_learn") return "act_skill";
    if (/^(auto_learn|apprend|lance learn|run learn)/i.test(s) || /auto_learn/i.test(s) && !/comment/.test(s)) return "act_learn";
    if (/(évolu|evolu|evolution|run evolution)/i.test(s)) return "act_evolution";
    if (/(booster?|améliorer|ameliorer).*(skill|compétence)|comment booster/i.test(s)) return "skill";
    if (/(gta\s*6|gta\s*vi|grand theft|sorti|sortie|release\s*date|aujourd.?hui|cette\s+semaine|actu|news|ransomware|breach|cve|cisa|novembre\s+202|2026)/i.test(s)) return "news";
    if (/(hack|attaque|exploit|ransomware)/i.test(s)) return "sec";
    if (/(code|coder|html|python|ascii|génère|page html)/i.test(s)) return "code";
    if (/(comment tu|qui es|t'es quel|architecture|myst)/i.test(s)) return "meta";
    if (/(vol|mouche|aile|haltere|insecte|larve|yeux)/i.test(s)) return "insect";
    return "general";
  }

  function needsWeb(q) {
    return /gta\s*6|gta\s*vi|grand theft|sorti|sortie|release|aujourd|cette\s+semaine|actu|news|ransomware|breach|cve|cisa|2026|novembre|incident|cyber/i.test(q || "");
  }

  async function clientWebSearch(q) {
    var hits = [];
    try {
      var w1 = await fetch("https://en.wikipedia.org/w/api.php?origin=*&action=opensearch&search=" + encodeURIComponent(q) + "&limit=5&namespace=0&format=json", { signal: AbortSignal.timeout(8000) });
      if (w1.ok) {
        var d1 = await w1.json();
        var titles = d1[1] || [];
        var urls = d1[3] || [];
        for (var i = 0; i < titles.length && i < 4; i++) hits.push({ title: titles[i], snippet: "", url: urls[i] || "", source: "wikipedia" });
      }
    } catch (e) {}
    if (hits.length) {
      try {
        var t = hits[0].title;
        var w2 = await fetch("https://en.wikipedia.org/api/rest_v1/page/summary/" + encodeURIComponent(t), { signal: AbortSignal.timeout(6000) });
        if (w2.ok) { var d2 = await w2.json(); if (d2.extract) hits[0].snippet = d2.extract.slice(0, 500); }
      } catch (e) {}
    }
    try {
      var ddgUrl = "https://api.duckduckgo.com/?q=" + encodeURIComponent(q) + "&format=json&no_html=1&skip_disambig=1";
      var prox = "https://api.allorigins.win/raw?url=" + encodeURIComponent(ddgUrl);
      var r = await fetch(prox, { signal: AbortSignal.timeout(10000) });
      if (r.ok) {
        var data = await r.json();
        if (data.AbstractText) hits.unshift({ title: data.Heading || q, snippet: data.AbstractText.slice(0, 500), url: data.AbstractURL || "", source: "ddg" });
        (data.RelatedTopics || []).slice(0, 4).forEach(function (t) {
          if (t && t.Text) hits.push({ title: t.Text.slice(0, 120), snippet: t.Text.slice(0, 300), url: t.FirstURL || "", source: "ddg" });
        });
      }
    } catch (e) {}
    if (/gta|grand theft/i.test(q)) {
      try {
        var jr = await fetch("https://r.jina.ai/http://www.rockstargames.com/newswire", { signal: AbortSignal.timeout(12000), headers: { "Accept": "text/plain" } });
        if (jr.ok) {
          var txt = (await jr.text()).slice(0, 2500);
          hits.unshift({ title: "Rockstar Newswire (live)", snippet: txt.replace(/\s+/g, " ").slice(0, 800), url: "https://www.rockstargames.com/newswire", source: "rockstar" });
        }
      } catch (e) {}
    }
    var seen = {};
    return hits.filter(function (h) {
      var k = (h.title || "") + (h.url || "");
      if (seen[k]) return false;
      seen[k] = 1;
      return !!(h.title || h.snippet);
    }).slice(0, 8);
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
    if (local) { st.textContent = "ACTIF · cortex local " + apiBase + " (learn/triage/évolution OK)"; st.className = "ok"; }
    else if (key) { st.textContent = "cloud + web HTTP · pas d'écriture repo sans local"; st.className = "warn"; }
    else { st.textContent = "lecture seule — clé cortex ou run_chat_server.py"; st.className = "warn"; }
    loadEvolutionStatus();
  }

  async function actLocal(path, body) {
    if (!apiBase) await probeLocal();
    if (!apiBase) throw new Error("Serveur local requis (python run_chat_server.py)");
    var r = await fetch(apiBase + path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body || {}) });
    if (!r.ok) throw new Error("HTTP " + r.status);
    return await r.json();
  }

  async function answer(q) {
    var mode = detectMode(q);
    if (mode === "greet") return { answer: "Là. Avec serveur local: triage / skill_learn / auto_learn / évolution.", sources: [], mode: "greet" };
    if (mode === "skill") return { answer: skillBoost(), sources: [], mode: "skill_arch" };
    if (mode === "meta") return { answer: "The-fly = graphe + auto_learn + skill_learn + triage + évolution + Graph-RAG + web live.", sources: [], mode: "meta" };

    if (mode === "act_triage" || mode === "act_skill" || mode === "act_learn" || mode === "act_evolution") {
      try {
        if (!apiBase) await probeLocal();
        if (apiBase) {
          var j = await actLocal("/api/chat", { question: q });
          return { answer: scrub(j.answer || JSON.stringify(j.report || j)), sources: j.sources || [], mode: j.mode || mode };
        }
        return { answer: "Action « " + mode + " » nécessite le cortex local:\n  python run_chat_server.py", sources: [], mode: "need_local" };
      } catch (e) { return { answer: "Échec action: " + e.message, sources: [], mode: "error" }; }
    }

    if (!apiBase) await probeLocal();
    if (apiBase) {
      var r = await fetch(apiBase + "/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question: q, use_arxiv: true, k: 5 }) });
      var j2 = await r.json();
      return { answer: scrub(j2.answer || ""), sources: j2.sources || [], mode: j2.mode || "local" };
    }

    var key = (localStorage.getItem("THEFLY_GROQ_KEY") || "").trim();
    if (!key) return { answer: "Sans serveur local ni clé cortex: modes skill/meta seulement.", sources: [], mode: "locked" };

    var webCtx = "";
    var webSources = [];
    if (needsWeb(q) || mode === "news" || mode === "sec") {
      try {
        var hits = await clientWebSearch(q);
        if (hits.length) { webCtx = formatHits(hits); webSources = hits.map(function (h) { return h.title || h.url; }); }
      } catch (e) { webCtx = ""; }
    }

    var sys = "Tu es THE-FLY agent graphe. Interdit de te dire GPT/Groq. Housefly=labellum pas stylet. " +
      "Tu as un bloc WEB LIVE ci-dessous quand présent. Ne dis JAMAIS que ta connaissance s'arrête en 2023/2024/2025, " +
      "ni que tu n'as pas d'accès temps réel. Base-toi sur WEB LIVE pour dates de sortie, incidents, actualité. Cite les sources. Mode=" + mode;
    var userMsg = q;
    if (webCtx) userMsg = "Question: " + q + "\n\n=== WEB LIVE (prioritaire) ===\n" + webCtx + "\n\nRéponds en français en t'appuyant sur WEB LIVE.";
    var messages = [{ role: "system", content: sys }, { role: "user", content: userMsg }];
    var rr = await fetch(API, {
      method: "POST",
      headers: { "Authorization": "Bearer " + key, "Content-Type": "application/json" },
      body: JSON.stringify({ model: MODEL, messages: messages, temperature: 0.25, max_tokens: 1100 })
    });
    if (!rr.ok) throw new Error("cortex HTTP " + rr.status);
    var text = scrub((await rr.json()).choices[0].message.content.trim());
    text = text.replace(/(ma base de connaissances|knowledge cutoff|je n'ai pas d'accès (aux? données?|temps réel)|mes connaissances s'arr[eê]tent)[^.]{0,80}\.?/gi, "");
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
      if (res.mode === "act_evolution") loadEvolutionStatus();
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
      s.textContent = (res.sources && res.sources.length ? "web: " + res.sources.slice(0,3).join(" · ") + " · " : "") + "mode: " + res.mode;
      node.appendChild(s);
      if (res.mode === "act_evolution") loadEvolutionStatus();
    } catch (e) { pending.textContent = "Erreur: " + e.message; }
  });

  add("bot", "The-fly cortex.\n• HTTP: recherche web auto avant l'IA (GTA, news, cyber)\n• python run_chat_server.py = AGIT (triage / skill / évolution)");
  loadSkillsJson().then(function(){ refreshStatus(); });
  setInterval(refreshStatus, 12000);
})();
