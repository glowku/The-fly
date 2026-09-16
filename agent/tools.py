"""Outils : écriture d'articles, git commit/push, lecture."""
import subprocess
from pathlib import Path


def write_article(title: str, content: str) -> str:
    safe = title.replace("/", "-").replace("\\", "-").strip()
    path = Path(f"wiki/{safe}.md")
    path.parent.mkdir(exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return str(path)


def _run(cmd, check=False):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        err = (r.stderr or r.stdout or "").strip()
        print(f"[git] cmd failed ({r.returncode}): {' '.join(cmd)}\n{err}", flush=True)
    if check and r.returncode != 0:
        raise subprocess.CalledProcessError(r.returncode, cmd, r.stdout, r.stderr)
    return r


def git_commit_push(files: list[str], message: str) -> bool:
    """Add + commit + pull --rebase + push. True si commit+push OK."""
    try:
        existing = [f for f in files if Path(f).exists() or str(f).endswith("/")]
        if not existing:
            existing = files

        _run(["git", "add"] + existing, check=True)

        r = _run(["git", "commit", "-m", message])
        if r.returncode != 0:
            # nothing to commit
            return False

        # Sync remote first
        _run(["git", "fetch", "origin", "main"])
        rb = _run(["git", "pull", "--rebase", "origin", "main"])
        if rb.returncode != 0:
            print("[git] rebase conflict — abort & force push not used", flush=True)
            _run(["git", "rebase", "--abort"])

        # Push with retry
        for attempt in range(3):
            p = _run(["git", "push", "origin", "HEAD:main"])
            if p.returncode == 0:
                return True
            print(f"[git] push attempt {attempt+1} failed, retry…", flush=True)
            _run(["git", "pull", "--rebase", "origin", "main"])

        return False
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
