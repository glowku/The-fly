"""Densify edges: attache les orphelins et renforce les sous-branches."""
from __future__ import annotations
import re
from collections import defaultdict
from difflib import SequenceMatcher
from .memory import load_coverage, save_coverage, log_event
from .skills import score_relevance, is_hard_junk

def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())

def _similar(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()

KEYWORDS = {
    "evolution": ["evolution", "adaptive", "radiation", "speciation", "phylogen", "devonian", "neoptera", "paleoptera", "basal", "coevolution"],
    "vol_et_aerodynamique": ["flight", "wing", "aerodynam", "haltere", "hover", "wingbeat", "aileron"],
    "anatomie_insecte": ["morpholog", "exoskeleton", "antenna", "thorax", "eye", "spiracle", "mouthpart", "leg", "labellum"],
    "ecologie": ["ecology", "pollinat", "parasitoid", "larva", "maggot", "decomposer", "pest", "abundance"],
    "comportement": ["behaviour", "behavior", "swarm", "mating", "courtship", "foraging", "mimicry", "agonistic"],
    "entomologie": ["insect", "diptera", "fly", "mosquito", "housefly", "hoverfly", "blowfly", "tachinid", "alate"],
}

def _skill_of(title: str) -> str:
    t = (title or "").lower()
    best, sc = "entomologie", 0
    for sk, kws in KEYWORDS.items():
        s = sum(1 for k in kws if k in t)
        if s > sc:
            sc, best = s, sk
    return best

def densify_edges(max_new: int = 90) -> dict:
    """Attache les nœuds orphelins à un parent pertinent et crée des arêtes manquantes.
    Retourne un rapport {added, orphans_before, edges_after}.
    """
    cov = load_coverage()
    nodes = cov.get("nodes", {})
    edges = list(cov.get("edges", []))
    edge_set = {(e.get("from"), e.get("to")) for e in edges if e.get("from") and e.get("to")}

    children = defaultdict(list)
    for e in edges:
        children[e["from"]].append(e["to"])

    connected = set()
    for e in edges:
        connected.add(e.get("from"))
        connected.add(e.get("to"))
    orphans = [n for n in nodes if n not in connected and not is_hard_junk(n)]

    parent_candidates = sorted(
        [t for t in nodes if not is_hard_junk(t)],
        key=lambda t: (len(children[t]), -score_relevance(t)),
    )

    added = 0
    for orphan in orphans:
        if score_relevance(orphan) < 0.25:
            continue
        osk = _skill_of(orphan)
        best_p, best_sc = None, -1.0
        for p in parent_candidates:
            if p == orphan:
                continue
            psk = _skill_of(p)
            sc = 0.0
            if psk == osk:
                sc += 3.2
            ow = set(re.findall(r"[a-z]{4,}", orphan.lower()))
            pw = set(re.findall(r"[a-z]{4,}", p.lower()))
            sc += len(ow & pw) * 2.1
            sc += _similar(orphan, p) * 4.5
            sc += min(2.5, len(children[p]) * 0.25)
            # bonus si parent a déjà des enfants (hub) ou est feuille à ramifier
            if len(children[p]) == 0:
                sc += 1.8  # favorise la création de sous-branche sur feuille
            if sc > best_sc:
                best_sc, best_p = sc, p
        if best_p and best_sc >= 3.2 and (best_p, orphan) not in edge_set:
            edges.append({"from": best_p, "to": orphan})
            edge_set.add((best_p, orphan))
            children[best_p].append(orphan)
            added += 1
            if added >= max_new:
                break

    # Second pass: feuilles solides sans enfants → tenter 1-2 liens vers frontier/relevant
    # (léger, pour créer des sous-branches)
    leaves = [n for n in nodes if len(children[n]) == 0 and score_relevance(n) >= 0.4]
    for leaf in leaves[:25]:
        if added >= max_new:
            break
        for cand in list(cov.get("frontier", []))[:8] + list(nodes.keys())[:30]:
            if cand == leaf or (leaf, cand) in edge_set:
                continue
            if is_hard_junk(cand) or score_relevance(cand) < 0.35:
                continue
            if _skill_of(leaf) == _skill_of(cand) or _similar(leaf, cand) > 0.35:
                edges.append({"from": leaf, "to": cand})
                edge_set.add((leaf, cand))
                children[leaf].append(cand)
                added += 1
                break

    cov["edges"] = edges
    save_coverage(cov)
    log_event("densify_edges", {"added": added, "orphans_before": len(orphans), "edges_after": len(edges)})
    return {"added": added, "orphans_before": len(orphans), "edges_after": len(edges)}
