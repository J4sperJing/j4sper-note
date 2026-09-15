import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from datetime import date

spec = importlib.util.spec_from_file_location("note_defaults", Path(__file__).with_name("note_defaults.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class NewNoteDefaultsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "content/notes").mkdir(parents=True)
        config = Path(__file__).resolve().parents[1] / "note-defaults.json"
        (self.root / "note-defaults.json").write_bytes(config.read_bytes())
        subprocess.run(["/usr/bin/git", "init", "-q", str(self.root)], check=True)
        self.old = self.root / "content/notes/existing.md"
        self.old.write_text("Already written\n")
        self.service = module.NoteDefaults(self.root)
        self.service.seed()

    def add(self, name, text):
        p = self.root / "content" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p

    def settle(self):
        self.service.tick(now=0)
        return self.service.tick(now=2)

    def test_new_note_and_existing_note(self):
        note = self.add("notes/中文笔记.md", "正文保持完整\n")
        self.settle()
        text = note.read_text()
        self.assertIn('title: ""', text)
        self.assertIn('description: ""', text)
        self.assertIn('tags: []', text)
        self.assertIn(f'date: {date.today().isoformat()}', text)
        self.assertIn('draft: true', text)
        self.assertIn('order: null', text)
        self.assertTrue(text.endswith("正文保持完整\n"))
        self.assertEqual(self.old.read_text(), "Already written\n")
        self.service.tick(now=4)
        self.assertEqual(note.read_text(), text)

    def test_frontmatter_in_progress_and_published_choices_are_preserved(self):
        notes = [self.add("notes/partial.md", "---\ntitle:"),
                 self.add("notes/import.md", "---\ndraft: false\norder: 10\n---\nBody")]
        before = [p.read_text() for p in notes]
        self.settle()
        self.assertEqual([p.read_text() for p in notes], before)

    def test_git_tracked_files_and_ignored_folders_are_preserved(self):
        tracked = self.add("notes/from-git.md", "Published upstream\n")
        subprocess.run(["/usr/bin/git", "-C", str(self.root), "add", "content/notes/from-git.md"], check=True)
        ignored = [self.add(f"{folder}/test.md", "Keep") for folder in ["templates", "private", ".obsidian", ".trash"]]
        self.settle()
        self.assertEqual(tracked.read_text(), "Published upstream\n")
        self.assertTrue(all(p.read_text() == "Keep" for p in ignored))

    def test_rename_and_restart(self):
        renamed = self.old.with_name("renamed.md")
        self.old.rename(renamed)
        self.settle()
        self.assertEqual(renamed.read_text(), "Already written\n")
        self.service = module.NoteDefaults(self.root)
        new_note = self.add("notes/after-restart.md", "")
        self.settle()
        self.assertIn("draft: true", new_note.read_text())

    def test_waits_for_writes_to_settle(self):
        p = self.add("notes/typing.md", "a")
        self.service.tick(now=0)
        p.write_text("ab")
        self.service.tick(now=1)
        self.service.tick(now=2)
        self.assertEqual(p.read_text(), "ab")
        self.service.tick(now=3)
        self.assertTrue(p.read_text().endswith("ab"))

    def test_symlink_does_not_modify_other_files(self):
        outside = self.root / "outside.md"
        outside.write_text("Do not modify")
        (self.root / "content/notes/link.md").symlink_to(outside)
        self.settle()
        self.assertEqual(outside.read_text(), "Do not modify")

    def test_date_is_generated_when_the_note_is_created(self):
        rendered = module.render_properties({"date": "$today"}, today=date(2027, 1, 2))
        self.assertIn("date: 2027-01-02", rendered)


if __name__ == "__main__":
    unittest.main()
