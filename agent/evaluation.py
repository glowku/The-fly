"""Évaluation multi-critères de la qualité d'un article (self-judgment)."""
import re
from datetime import datetime, timezone


def score_article(content: str) -> dict:
    """Retourne un score de 0 à 10 + métriques détaillées."""
    if not content or not content.strip():
        return {
            "score": 0.0,
            "metrics": {"error": "empty"},
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

    metrics = {}

    # 1. Longueur (mots)
    words = len(re.findall(r"\b\w+\b", content, flags=re.UNICODE))
    metrics["words"] = words
    # Idéal ~280-400 → max 2.5 pts
    if words < 80:
        length_score = 0.3
    elif words < 180:
        length_score = 1.2
    elif words <= 450:
        length_score = 2.5
    else:
        length_score = 2.0  # trop long pénalisé légèrement

    # 2. Structure (sections ##)
    sections = len(re.findall(r"^##\s+.+$", content, flags=re.MULTILINE))
    metrics["sections"] = sections
    structure_score = min(sections / 3.0, 1.0) * 2.0  # max 2.0

    # 3. Liens internes [[Titre]]
    links = re.findall(r"\[\[([^\]]+)\]\]", content)
    unique_links = set(links)
    metrics["links"] = len(unique_links)
    metrics["link_list"] = list(unique_links)[:15]
    link_score = min(len(unique_links) / 4.0, 1.0) * 2.0  # max 2.0

    # 4. Diversité lexicale (mots > 3 lettres)
    word_list = [w.lower() for w in re.findall(r"\b\w+\b", content, flags=re.UNICODE) if len(w) > 3]
    unique_words = len(set(word_list))
    diversity = unique_words / max(len(word_list), 1)
    metrics["diversity"] = round(diversity, 3)
    diversity_score = min(diversity / 0.55, 1.0) * 1.8  # max 1.8

    # 5. Propreté (pas de placeholders)
    bad_patterns = [
        r"\[à compléter\]", r"TODO", r"FIXME", r"lorem ipsum",
        r"\.\.\.\s*\.\.\.", r"placeholder", r"à remplir", r"xxx",
    ]
    has_placeholder = any(re.search(p, content, re.IGNORECASE) for p in bad_patterns)
    metrics["has_placeholder"] = has_placeholder
    cleanliness_score = 0.0 if has_placeholder else 1.2

    # 6. Présence d'un vrai titre # et d'une intro
    has_h1 = bool(re.search(r"^#\s+.+$", content, flags=re.MULTILINE))
    metrics["has_h1"] = has_h1
    title_score = 0.5 if has_h1 else 0.0

    total = (
        length_score
        + structure_score
        + link_score
        + diversity_score
        + cleanliness_score
        + title_score
    )
    total = min(round(total, 2), 10.0)

    return {
        "score": total,
        "metrics": metrics,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def is_acceptable(score_result: dict, threshold: float = 5.8) -> bool:
    """Critère d'acceptation pour commit."""
    return score_result.get("score", 0) >= threshold


def explain_score(score_result: dict) -> str:
    """Résumé textuel pour logs."""
    m = score_result.get("metrics", {})
    return (
        f"score={score_result.get('score')}/10 | "
        f"words={m.get('words')} sections={m.get('sections')} "
        f"links={m.get('links')} diversity={m.get('diversity')}"
    )
