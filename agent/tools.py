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


def _clean_git_state():
    """Nettoie tout état conflictuel avant de tenter un pull/rebase."""
    # Abort rebase / merge en cours
    _run(["git", "rebase", "--abort"])
    _run(["git", "merge", "--abort"])
    # Reset des index unmerged
    _run(["git", "reset", "--merge"])
    # Si encore des fichiers unmerged → on les force en "ours"
    status = _run(["git", "status", "--porcelain"])
    if status.stdout and ("UU" in status.stdout or "AA" in status.stdout or "DD" in status.stdout):
        print("[git] unmerged files detected → force resolve with ours", flush=True)
        _run(["git", "checkout", "--ours", "."])
        _run(["git", "add", "-A"])


def git_commit_push(files: list[str] | None, message: str) -> bool:
    """
    Add + commit + rebase/merge propre + push.
    Gère les conflits unmerged et les non-fast-forward.
    Retourne True si le push a réussi.
    """
    try:
        # 1. Toujours tout prendre
        _run(["git", "add", "-A"])

        st = _run(["git", "status", "--porcelain"])
        if not (st.stdout or "").strip():
            print("[git] nothing to commit", flush=True)
            return False

        # 2. Commit
        r = _run(["git", "commit", "-m", message])
        if r.returncode != 0:
            print("[git] commit failed", flush=True)
            return False

        # 3. Fetch
        _run(["git", "fetch", "origin", "main"])

        # 4. Nettoyage préventif
        _clean_git_state()

        # 5. Stash si dirty résiduel
        dirty = _run(["git", "status", "--porcelain"])
        stashed = False
        if (dirty.stdout or "").strip():
            _run(["git", "stash", "push", "-u", "-m", "fly-agent-temp"])
            stashed = True

        # 6. Tentative rebase
        rb = _run(["git", "pull", "--rebase", "origin", "main"])
        if rb.returncode != 0:
            print("[git] rebase failed → abort + merge", flush=True)
            _run(["git", "rebase", "--abort"])
            _clean_git_state()
            # Merge à la place
            merge = _run(["git", "pull", "origin", "main", "--no-rebase", "--no-edit"])
            if merge.returncode != 0:
                print("[git] merge also failed → force resolve", flush=True)
                _clean_git_state()
                _run(["git", "add", "-A"])
                _run(["git", "commit", "-m", "resolve: auto after conflict"])

        if stashed:
            pop = _run(["git", "stash", "pop"])
            if pop.returncode != 0:
                print("[git] stash pop conflict → resolve with ours", flush=True)
                _clean_git_state()
                _run(["git", "add", "-A"])

        # 7. Push avec retries
        for attempt in range(4):
            p = _run(["git", "push", "origin", "HEAD:main"])
            if p.returncode == 0:
                print("[git] push OK", flush=True)
                return True

            print(f"[git] push attempt {attempt + 1} failed → pull + retry", flush=True)
            _clean_git_state()
            _run(["git", "pull", "origin", "main", "--no-rebase", "--no-edit"])
            # Si encore unmerged après le pull
            st2 = _run(["git", "status", "--porcelain"])
            if st2.stdout and ("UU" in st2.stdout or "AA" in st2.stdout):
                _run(["git", "checkout", "--ours", "."])
                _run(["git", "add", "-A"])
                _run(["git", "commit", "-m", "resolve: unmerged after pull"])

        print("[git] all push attempts failed", flush=True)
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
