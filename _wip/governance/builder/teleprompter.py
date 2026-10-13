#!/usr/bin/env python3
"""
Extracts the Script blocks from SPEAKER-NOTES.md into TELEPROMPTER.md.

Usage:
  python3 builder/teleprompter.py

Each "## " section of SPEAKER-NOTES.md contributes its heading and the indented paragraphs
under "- **Script**:". Lines of the form ">>> ... <<<" pass through as demo markers.
"""

import os, re, textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'SPEAKER-NOTES.md')
OUT = os.path.join(ROOT, 'TELEPROMPTER.md')

text = open(SRC, encoding='utf-8').read()
out = ['# AI Governance Demo — Teleprompter\n',
       'Generated from `SPEAKER-NOTES.md` by `builder/teleprompter.py`. Edit the notes, not this file.\n']
total = 0

for section in re.split(r'^## ', text, flags=re.M)[1:]:
    heading, _, body = section.partition('\n')
    m = re.search(r'^- \*\*Script\*\*:\n(.*?)(?=^- \*\*Land\*\*)', body, flags=re.S | re.M)
    if not m:
        continue
    script = textwrap.dedent(m.group(1)).strip()
    total += len([w for w in script.split() if not w.startswith('>>>') and w != '<<<'])
    out.append(f'\n---\n\n## {heading.strip()}\n\n{script}\n')

out.append(f'\n---\n\nSpoken words: about {total}. At 150 words a minute that is about {total // 150} minutes, before demos.\n')
open(OUT, 'w', encoding='utf-8').write(''.join(out))
print(f'wrote {OUT} ({total} words)')
