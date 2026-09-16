"""Planification intelligente : priorise par valeur attendue (trou + qualité + centralité)."""
from .memory import load_coverage, load_quality, log_event


def _score_candidate(title: str, cov: dict, qual: dict) -> float:
    """Score de priorité pour un candidat (plus haut = plus urgent)."""
    score = 0.0

    # 1. Qualité faible → priorité réparation élevée
    if title in qual:
        q = qual[title].get("score", 10)
        if q < 4.0:
            return 100.0 + (4.0 - q) * 10  # très prioritaire
        if q < 6.0:
            score += (6.0 - q) * 5

    # 2. Dans la frontière → à explorer
    if title in cov.get("frontier", []) and title not in cov.get("nodes", {}):
        score += 40.0
        # Préférer concepts courts / généraux
        score += max(0, 20 - len(title) * 0.4)

    # 3. Profondeur faible (proche de la racine) = plus de valeur structurelle
    node = cov.get("nodes", {}).get(title)
    if node:
        depth = node.get("depth", 5)
        score += max(0, 15 - depth * 2)
    else:
        # Nouveau : bonus si lié à beaucoup de nœuds existants (centralité estimée)
        incoming = sum(1 for e in cov.get("edges", []) if e.get("to") == title)
        score += min(incoming * 3, 15)

    # 4. Éviter les titres trop longs / trop spécifiques
    if len(title) > 60:
        score -= 10
    if title.count(" ") > 5:
        score -= 5

    return score


def pick_next_target(strategy: str = "value"):
    """Retourne le prochain titre à traiter avec raison et action."""
    cov = load_coverage()
    qual = load_quality()

    candidates = []

    # Collecter tous les candidats potentiels
    # a) articles à faible qualité
    for title, info in qual.items():
        if info.get("score", 10) < 6.5:
            candidates.append((title, "repair", info.get("score", 0)))

    # b) frontière
    for t in cov.get("frontier", []):
        if t not in cov.get("nodes", {}):
            candidates.append((t, "expand", 0))

    # c) re-expand depuis nœuds peu connectés
    for title, node in cov.get("nodes", {}).items():
        out_degree = sum(1 for e in cov.get("edges", []) if e.get("from") == title)
        if out_degree < 3:
            candidates.append((title, "re-expand", out_degree))

    if not candidates:
        # Bootstrap
        root = cov.get("root", "Fly")
        return {
            "title": root,
            "reason": "bootstrap",
            "action": "expand",
            "priority": 999,
        }

    # Scorer et trier
    scored = []
    for title, action, extra in candidates:
        prio = _score_candidate(title, cov, qual)
        if action == "repair":
            prio += 50
        scored.append((prio, title, action, extra))

    scored.sort(reverse=True)
    best = scored[0]
    prio, title, action, extra = best

    reason_map = {
        "repair": f"low_quality={extra:.1f}",
        "expand": "frontier_gap",
        "re-expand": f"low_outdegree={extra}",
    }
    reason = reason_map.get(action, action)

    log_event("plan", {"title": title, "action": action, "priority": round(prio, 1), "reason": reason})

    return {
        "title": title,
        "reason": reason,
        "action": action,
        "priority": round(prio, 1),
    }


def register_discovered(title: str, depth: int, parent: str | None = None):
    """Ajoute un titre découvert à la frontière du graphe."""
    cov = load_coverage()
    if title in cov["nodes"] or title in cov.get("frontier", []):
        # Mettre à jour edge si besoin
        if parent:
            edge = {"from": parent, "to": title}
            if edge not in cov["edges"]:
                cov["edges"].append(edge)
                from .memory import save_coverage
                save_coverage(cov)
        return

    if title not in cov["frontier"]:
        cov["frontier"].append(title)
    if parent:
        edge = {"from": parent, "to": title}
        if edge not in cov["edges"]:
            cov["edges"].append(edge)
    from .memory import save_coverage
    save_coverage(cov)


def register_processed(title: str, depth: int, sources: list):
    """Marque un titre comme traité."""
    from datetime import datetime, timezone
    cov = load_coverage()
    cov["nodes"][title] = {
        "depth": depth,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sources": sources,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    cov["frontier"] = [t for t in cov.get("frontier", []) if t != title]
    cov["max_depth"] = max(cov.get("max_depth", 0), depth)
    from .memory import save_coverage
    save_coverage(cov)
