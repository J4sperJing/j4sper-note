#!/usr/bin/env python3
"""Add project defaults to newly created, untracked Markdown files.

Runs independently of the editor. Existing files and frontmatter are preserved.
"""
import argparse
from datetime import date, datetime
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time


def log(message):
    print(datetime.now().isoformat(timespec="seconds"), message, flush=True)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def signature(path):
    st = path.stat()
    return st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns


def render_properties(properties, today=None, newline="\n"):
    lines = ["---"]
    for key, value in properties.items():
        if value == "$today":
            rendered = (today or date.today()).isoformat()
        else:
            rendered = json.dumps(value, ensure_ascii=False)
        lines.append(f"{key}: {rendered}")
    lines.extend(["---", "", ""])
    return newline.join(lines)


class NoteDefaults:
    def __init__(self, root, stable_seconds=1.5):
        self.root = Path(root).resolve()
        self.config = json.loads((self.root / "note-defaults.json").read_text())
        self.content = (self.root / self.config["contentDirectory"]).resolve()
        self.content.relative_to(self.root)
        self.ignored = set(self.config["ignoredFolders"])
        self.state_path = self.root / ".local/note-defaults/state.json"
        self.pending = {}
        self.stable_seconds = stable_seconds
        self.known = None
        if self.state_path.exists():
            state = json.loads(self.state_path.read_text())
            if state.get("root") == str(self.root):
                self.known = state["known"]

    def snapshot(self):
        result = {}
        for folder, directories, filenames in os.walk(self.content, followlinks=False):
            directories[:] = [d for d in directories if not d.startswith(".")
                               and d not in self.ignored and not (Path(folder) / d).is_symlink()]
            for name in filenames:
                path = Path(folder) / name
                if name.startswith(".") or path.suffix.lower() != ".md" or path.is_symlink():
                    continue
                try:
                    result[str(path.relative_to(self.root))] = signature(path)
                except FileNotFoundError:
                    pass
        return result

    def save(self):
        write_json(self.state_path, {"version": 1, "root": str(self.root), "known": self.known})

    def seed(self):
        self.known = {key: list(stamp[:2]) for key, stamp in self.snapshot().items()}
        self.save()
        log(f"Registered {len(self.known)} existing notes without modifying them.")

    def is_tracked(self, relative):
        result = subprocess.run(
            ["/usr/bin/git", "-C", str(self.root), "ls-files", "--error-unmatch", "--", relative],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10,
        )
        if result.returncode not in (0, 1):
            raise RuntimeError("Unable to check whether a note is already tracked by Git")
        return result.returncode == 0

    def decorate(self, relative, expected):
        path = self.root / relative
        if path.is_symlink() or signature(path) != expected:
            return "retry"
        # Files arriving through Git pull already carry their author's publication choices.
        if (self.root / ".git/index.lock").exists():
            return "retry"
        if self.is_tracked(relative):
            return "preserved"
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            return "preserved"
        first_line = text.lstrip().splitlines()[0].strip() if text.strip() else ""
        # Also preserve incomplete metadata that the author is currently entering.
        if first_line in ("---", "+++"):
            return "preserved"
        newline = "\r\n" if b"\r\n" in raw else "\n"
        prefix = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
        updated = prefix + (render_properties(self.config["properties"], newline=newline) + text).encode("utf-8")
        if signature(path) != expected:
            return "retry"
        handle, temp_name = tempfile.mkstemp(prefix=".note-defaults-", dir=path.parent)
        try:
            with os.fdopen(handle, "wb") as output:
                output.write(updated)
            os.chmod(temp_name, path.stat().st_mode & 0o777)
            if path.is_symlink() or signature(path) != expected or path.read_bytes() != raw:
                return "retry"
            os.replace(temp_name, path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
        log(f"Added note properties: {relative}")
        return "updated"

    def tick(self, now=None):
        if self.known is None:
            self.seed()
            return []
        now = time.monotonic() if now is None else now
        snapshot = self.snapshot()
        old_known = dict(self.known)
        previous_identities = {tuple(identity) for identity in old_known.values()}
        updated = []
        for relative, stamp in snapshot.items():
            if relative in self.known or stamp[:2] in previous_identities:
                # Renames and ordinary atomic saves of existing notes are not new notes.
                self.known[relative] = list(stamp[:2])
                continue
            pending = self.pending.get(relative)
            if pending is None or pending[0] != stamp:
                self.pending[relative] = (stamp, now)
                continue
            if now - pending[1] < self.stable_seconds:
                continue
            try:
                result = self.decorate(relative, stamp)
                if result == "retry":
                    self.pending.pop(relative, None)
                    continue
                self.known[relative] = list(signature(self.root / relative)[:2])
                self.pending.pop(relative, None)
                if result == "updated":
                    updated.append(relative)
            except FileNotFoundError:
                self.pending.pop(relative, None)
        self.known = {key: value for key, value in self.known.items() if key in snapshot}
        self.pending = {key: value for key, value in self.pending.items() if key in snapshot}
        if self.known != old_known:
            self.save()
        return updated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--seed", action="store_true", help="Register existing notes without changing them")
    args = parser.parse_args()
    service = NoteDefaults(args.root)
    if args.seed:
        service.seed()
        return
    log(f"Watching new Markdown files in {service.content}")
    while True:
        try:
            service.tick()
        except Exception as error:
            log(f"Waiting after error: {error}")
        time.sleep(1)


if __name__ == "__main__":
    main()
