"""Synthèse : appelle Groq (gratuit) pour générer un article structuré et lié."""
import os
import re
import requests
from .memory import load_coverage

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"  # modèle actuel disponible (llama-3.3-70b déprécié)


def _get_existing_titles(limit: int = 40) -> list:
    cov = load_coverage()
    titles = list(cov.get("nodes", {}).keys())
    return titles[-limit:] if titles else []


def synthesize_article(
    title: str,
    summary: str,
    description: str = "",
    parent: str | None = None,
    sources: list | None = None,
    existing_links: list | None = None,
) -> str:
    sources = sources or []
    existing = existing_links or _get_existing_titles()
    parent_line = f"Ce concept est relié à **{parent}** dans le graphe de connaissance." if parent else ""

    link_hint = ""
    if existing:
        sample = existing[:12]
        link_hint = (
            "Liens internes déjà présents dans le wiki (utilise-les si pertinent dans 'Voir aussi') :\n"
            + ", ".join(f"[[{t}]]" for t in sample)
        )

    prompt = f"""Tu es un rédacteur d'encyclopédie. Tu écris un article structuré sur le concept « {title} ».

Description courte : {description or '(aucune)'}

Résumé source (Wikipedia, base factuelle exclusive) :
{summary[:1800]}

{parent_line}

{link_hint}

Règles strictes :
1. Écris uniquement en français, ton neutre, encyclopédique, clair.
2. Structure obligatoire :
   - Commence exactement par : # {title}
   - Une introduction de 2-4 phrases.
   - Exactement 2 ou 3 sections ## avec titres informatifs.
   - Termine par ## Voir aussi contenant 4 à 6 liens internes au format [[Titre Exact]].
3. N'invente AUCUN fait. Reste strictement fidèle au résumé fourni.
4. Longueur cible : 220-450 mots.
5. Pas de placeholders, pas de TODO.
6. Commence directement par le # titre.

Produis uniquement le Markdown de l'article."""

    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        return _fallback_article(title, summary, description, parent)

    try:
        r = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.35,
                "max_tokens": 1400,
                "top_p": 0.9,
            },
            timeout=90,
        )
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"].strip()
        content = re.sub(r"^```(?:markdown)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
        if not content.startswith("#"):
            content = f"# {title}\n\n{content}"
        return content
    except Exception as e:
        print(f"[synthesis] Groq error: {e}", flush=True)
        return _fallback_article(title, summary, description, parent)


def _fallback_article(title, summary, description, parent):
    parent_line = f"\n\nRelié à [[{parent}]]." if parent else ""
    extract = (summary or description or "Concept encyclopédique.")[:600]
    return f"""# {title}

{extract}{parent_line}

## Contexte

Ce concept a été intégré automatiquement dans le graphe de connaissance à partir de sources publiques.

## Voir aussi

[[{parent or title}]]
"""
