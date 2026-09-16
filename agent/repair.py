"""Auto-correction : détecte articles faibles, liens cassés, orphelins et répare."""
import re
from pathlib import Path
from .memory import load_coverage, load_quality, save_quality, log_event, save_coverage
from .evaluation import score_article
from .synthesis import synthesize_article
from .perception import get_summary


def find_broken_links() -> list[tuple[str, str]]:
    """Détecte les [[Liens]] qui ne correspondent à aucun article existant."""
    wiki = Path("wiki")
    existing = {f.stem for f in wiki.glob("*.md")}
    broken = []
    for article in wiki.glob("*.md"):
        content = article.read_text(encoding="utf-8")
        for link in re.findall(r"\[\[([^\]]+)\]\]", content):
            # Normaliser un peu
            clean = link.strip()
            if clean not in existing and clean.replace(" ", "_") not in existing:
                broken.append((article.stem, clean))
    return broken


def repair_low_quality(threshold: float = 5.5, max_repairs: int = 4) -> list[str]:
    """Régénère les articles dont le score est sous le seuil."""
    quality = load_quality()
    repaired = []
    # Trier par score croissant
    candidates = sorted(
        [(t, info) for t, info in quality.items() if info.get("score", 10) < threshold],
        key=lambda x: x[1].get("score", 0),
    )

    for title, info in candidates:
        if len(repaired) >= max_repairs:
            break

        summary = get_summary(title)
        if not summary:
            # Essayer avec le stem exact
            continue

        parent = None
        cov = load_coverage()
        for edge in cov.get("edges", []):
            if edge.get("to") == title:
                parent = edge.get("from")
                break

        new_content = synthesize_article(
            title,
            summary.get("extract") or "",
            summary.get("description") or "",
            parent=parent,
            sources=[summary.get("url")] if summary.get("url") else None,
        )
        new_score = score_article(new_content)

        if new_score["score"] > info.get("score", 0):
            path = Path(f"wiki/{title}.md")
            path.parent.mkdir(exist_ok=True)
            path.write_text(new_content, encoding="utf-8")
            quality[title] = new_score
            repaired.append(title)
            log_event("repair", {
                "title": title,
                "old_score": info.get("score"),
                "new_score": new_score["score"],
                "delta": round(new_score["score"] - info.get("score", 0), 2),
            })
            print(f"[repair] {title}: {info.get('score'):.1f} → {new_score['score']:.1f}", flush=True)
        else:
            print(f"[repair] {title}: pas d'amélioration ({new_score['score']:.1f})", flush=True)

    save_quality(quality)
    return repaired


def promote_broken_links_to_frontier(max_new: int = 15) -> int:
    """Ajoute les cibles de liens cassés à la frontière pour exploration future."""
    broken = find_broken_links()
    cov = load_coverage()
    added = 0
    seen = set(cov.get("frontier", [])) | set(cov.get("nodes", {}).keys())
    for _, target in broken:
        if target not in seen and added < max_new:
            cov["frontier"].append(target)
            seen.add(target)
            added += 1
    if added:
        save_coverage(cov)
        log_event("promote_broken", {"count": added})
    return added


def delete_orphans(keep_root: bool = True) -> list[str]:
    """Supprime les articles qui ne sont référencés par personne (sauf racine)."""
    wiki = Path("wiki")
    coverage = load_coverage()
    root = coverage.get("root", "Fly")
    referenced = set()
    for article in wiki.glob("*.md"):
        content = article.read_text(encoding="utf-8")
        referenced.update(re.findall(r"\[\[([^\]]+)\]\]", content))

    # Aussi considérer les edges du graphe
    for edge in coverage.get("edges", []):
        referenced.add(edge.get("from", ""))
        referenced.add(edge.get("to", ""))

    deleted = []
    quality = load_quality()
    for article in list(wiki.glob("*.md")):
        stem = article.stem
        if keep_root and stem == root:
            continue
        if stem not in referenced and stem not in coverage.get("nodes", {}):
            # Double check: si pas dans nodes et pas référencé → orphelin
            article.unlink()
            deleted.append(stem)
            if stem in quality:
                del quality[stem]
            log_event("delete_orphan", {"title": stem})

    if deleted:
        # Nettoyer coverage
        for t in deleted:
            coverage["nodes"].pop(t, None)
            coverage["frontier"] = [x for x in coverage.get("frontier", []) if x != t]
        save_coverage(coverage)
        save_quality(quality)
    return deleted


def full_repair_pass(max_repairs: int = 5) -> dict:
    """Passe complète de réparation."""
    repaired = repair_low_quality(max_repairs=max_repairs)
    promoted = promote_broken_links_to_frontier()
    orphans = delete_orphans()
    broken = find_broken_links()
    return {
        "repaired": repaired,
        "promoted_to_frontier": promoted,
        "orphans_deleted": orphans,
        "remaining_broken_links": len(broken),
    }
