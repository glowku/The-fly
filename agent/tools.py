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
        print(f"[git] cmd failed ({r.returncode}): {' '.join(cmd)}\n{err[:500]}", flush=True)
    if check and r.returncode != 0:
        raise subprocess.CalledProcessError(r.returncode, cmd, r.stdout, r.stderr)
    return r


def git_commit_push(files: list[str] | None, message: str) -> bool:
    """Add + commit + rebase propre + push. True si push OK."""
    try:
        # Toujours tout prendre (évite unstaged qui bloque rebase)
        _run(["git", "add", "-A"])

        st = _run(["git", "status", "--porcelain"])
        if not (st.stdout or "").strip():
            print("[git] nothing to commit", flush=True)
            return False

        r = _run(["git", "commit", "-m", message])
        if r.returncode != 0:
            return False

        _run(["git", "fetch", "origin", "main"])

        # rebase: si unstaged résiduels → stash
        dirty = _run(["git", "status", "--porcelain"])
        stashed = False
        if (dirty.stdout or "").strip():
            _run(["git", "stash", "push", "-u", "-m", "fly-agent-temp"])
            stashed = True

        rb = _run(["git", "pull", "--rebase", "origin", "main"])
        if rb.returncode != 0:
            print("[git] rebase failed → abort, try merge", flush=True)
            _run(["git", "rebase", "--abort"])
            _run(["git", "pull", "origin", "main", "--no-rebase", "--no-edit"])

        if stashed:
            _run(["git", "stash", "pop"])

        for attempt in range(3):
            p = _run(["git", "push", "origin", "HEAD:main"])
            if p.returncode == 0:
                print("[git] push OK", flush=True)
                return True
            print(f"[git] push attempt {attempt+1} failed", flush=True)
            _run(["git", "pull", "origin", "main", "--no-rebase", "--no-edit"])

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
