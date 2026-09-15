#!/usr/bin/env python3
"""Install this project's new-note helper for the current macOS user."""
import argparse
import os
from pathlib import Path
import plistlib
import subprocess
import sys
from note_defaults import NoteDefaults

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
args = parser.parse_args()
root = args.root.resolve()
if sys.platform != 'darwin':
    parser.error('This installer supports macOS. Run note_defaults.py directly on other systems.')
service = NoteDefaults(root)
if service.known is None:
    service.seed()
log_dir = root / '.local/note-defaults'
log_dir.mkdir(parents=True, exist_ok=True)
label = 'com.j4sper.note-defaults'
plist = Path.home() / 'Library/LaunchAgents' / (label + '.plist')
plist.parent.mkdir(parents=True, exist_ok=True)
job = {
    'Label': label,
    'ProgramArguments': ['/usr/bin/python3', '-u', str(root / 'scripts/note_defaults.py'), '--root', str(root)],
    'WorkingDirectory': str(root),
    'RunAtLoad': True,
    'KeepAlive': True,
    'ThrottleInterval': 15,
    'ProcessType': 'Background',
    'EnvironmentVariables': {'PATH': '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'},
    'StandardOutPath': str(log_dir / 'watcher.log'),
    'StandardErrorPath': str(log_dir / 'watcher-error.log'),
}
if plist.exists():
    previous = plistlib.loads(plist.read_bytes())
    if previous.get('WorkingDirectory') != str(root):
        parser.error('A helper for a different project already uses this name; it was preserved.')
    subprocess.run(['/bin/launchctl', 'bootout', f'gui/{os.getuid()}', str(plist)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
plist.write_bytes(plistlib.dumps(job))
os.chmod(plist, 0o644)
subprocess.run(['/bin/launchctl', 'bootstrap', f'gui/{os.getuid()}', str(plist)], check=True)
print('Started new-note properties helper:', label)
print('Notes directory:', service.content)
print('It will start automatically when you log in to this Mac.')
