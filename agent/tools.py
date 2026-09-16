"""Outils : écriture d'articles, git commit/push, lecture."""
import subprocess
from pathlib import Path


def write_article(title: str, content: str) -> str:
    """Écrit un article Markdown dans wiki/."""
    # Sécuriser le nom de fichier
    safe = title.replace("/", "-").replace("\\", "-").strip()
    path = Path(f"wiki/{safe}.md")
    path.parent.mkdir(exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return str(path)


def git_commit_push(files: list[str], message: str) -> bool:
    """Add + commit + pull --rebase + push. Retourne True si commit effectué."""
    try:
        # Filtrer les fichiers existants
        existing = [f for f in files if Path(f).exists() or f.endswith("/")]
        if not existing:
            existing = files

        subprocess.run(["git", "add"] + existing, check=True, capture_output=True)

        r = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            # Rien à committer
            return False

        # Rebase pour éviter les conflits sur CI
        subprocess.run(
            ["git", "pull", "--rebase", "origin", "main"],
            check=False,
            capture_output=True,
        )
        subprocess.run(
            ["git", "push", "origin", "HEAD:main"],
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"[git] error: {e}", flush=True)
        return False
    except Exception as e:
        print(f"[git] unexpected: {e}", flush=True)
        return False


def read_file(path: str) -> str | None:
    p = Path(path)
    return p.read_text(encoding="utf-8") if p.exists() else None


def list_wiki_titles() -> list[str]:
    return [f.stem for f in Path("wiki").glob("*.md")]
