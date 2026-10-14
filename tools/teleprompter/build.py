#!/usr/bin/env python3
"""
Builds teleprompter files from a deck's SPEAKER-NOTES.md.

Usage:
  python3 tools/teleprompter/build.py DECK_DIR [DECK_DIR ...]
  python3 tools/teleprompter/build.py --all
  python3 tools/teleprompter/build.py DECK_DIR --presenter smitty [--presenter tyler]

Output, in DECK_DIR/teleprompter/:
  <deck>.md  <deck>.textream                     generic intro
  <deck>-<presenter>.md  <deck>-<presenter>.textream   one pair per --presenter

<deck> is the deck folder's name, lowercased, underscores turned to hyphens. The .textream
file is the Textream app's save format: a JSON array with one string per page.

Notes format (the contract each deck's SPEAKER-NOTES.md follows):
  - Each "## " section contributes its heading and the indented paragraphs under
    "- **Script**:".
  - A line of three hyphens inside a script starts a new page.
  - A line of the form ">>> ... <<<" is a demo marker and passes through. ">>> DEMO ... <<<"
    opens a demo and ">>> BACK TO DECK <<<" closes it; words between them count as demo time.
  - A line that is entirely "[like this]" is an on-screen cue. It passes through and is not
    counted as spoken.
  - A "- **Teleprompter**: omitted" line skips the section.
  - {{presenter-intro}} becomes "I'm <first name>, <title>." for a presenter, taken from
    DECK_DIR/presenters/<presenter>.json ("CEO, Akka" is spoken as "CEO at Akka"), and
    "Thank you for joining me." when no presenter is given.
"""

import argparse, json, os, re, sys, textwrap

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = {'.git', '.venv', 'node_modules', 'generated', '__pycache__'}
GENERIC_INTRO = 'Thank you for joining me.'


def find_decks():
    decks = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if 'SPEAKER-NOTES.md' in files:
            decks.append(root)
    return sorted(decks)


def presenter_intro(deck_dir, slug):
    path = os.path.join(deck_dir, 'presenters', f'{slug}.json')
    if not os.path.exists(path):
        sys.exit(f'No presenter file: {path}')
    p = json.load(open(path, encoding='utf-8'))
    title = p['title'].replace(', ', ' at ', 1)
    return f"I'm {p['name'].split()[0]}, {title}."


def count_words(script):
    """Spoken words in a script, as (slide words, demo words). Markers and cues are not spoken."""
    slide = demo = 0
    in_demo = False
    for line in script.splitlines():
        s = line.strip()
        if s.startswith('>>> DEMO'):
            in_demo = True
        elif s.startswith('>>> BACK TO DECK'):
            in_demo = False
        elif s and s != '---' and not (s.startswith('[') and s.endswith(']')):
            if in_demo:
                demo += len(s.split())
            else:
                slide += len(s.split())
    return slide, demo


def build(deck_dir, slug=None):
    deck = os.path.basename(os.path.abspath(deck_dir)).lower().replace('_', '-')
    stem = f'{deck}-{slug}' if slug else deck
    intro = presenter_intro(deck_dir, slug) if slug else GENERIC_INTRO
    text = open(os.path.join(deck_dir, 'SPEAKER-NOTES.md'), encoding='utf-8').read()

    md = [f'# {deck} — Teleprompter' + (f' ({slug})' if slug else '') + '\n',
          'Generated from `SPEAKER-NOTES.md` by `tools/teleprompter/build.py`. Edit the notes, not this file.\n']
    pages = []
    slide_words = demo_words = 0
    for section in re.split(r'^## ', text, flags=re.M)[1:]:
        heading, _, body = section.partition('\n')
        if re.search(r'^- \*\*Teleprompter\*\*: omitted', body, flags=re.M):
            continue
        m = re.search(r'^- \*\*Script\*\*:\n(.*?)(?=^- \*\*Land\*\*)', body, flags=re.S | re.M)
        if not m:
            continue
        script = textwrap.dedent(m.group(1)).strip().replace('{{presenter-intro}}', intro)
        sw, dw = count_words(script)
        slide_words += sw
        demo_words += dw
        md.append(f'\n---\n\n## {heading.strip()}\n\n{script}\n')
        pages.extend(p.strip() for p in re.split(r'^---$', script, flags=re.M))
    total = slide_words + demo_words
    md.append(f'\n---\n\nSpoken words: about {total} ({slide_words} on slides, {demo_words} in demos). '
              f'At 150 words a minute that is about {slide_words // 150} minutes on slides and '
              f'{demo_words // 150} in demos, plus time spent clicking.\n')

    out_dir = os.path.join(deck_dir, 'teleprompter')
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, f'{stem}.md'), 'w', encoding='utf-8').write(''.join(md))
    open(os.path.join(out_dir, f'{stem}.textream'), 'w', encoding='utf-8').write(
        json.dumps(pages, ensure_ascii=False, separators=(',', ':')))
    print(f'{os.path.relpath(out_dir, REPO)}/{stem}.{{md,textream}}  ({total} words, {len(pages)} pages)')


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('decks', nargs='*', help='deck folders containing SPEAKER-NOTES.md')
ap.add_argument('--all', action='store_true', help='every folder in the repo with a SPEAKER-NOTES.md')
ap.add_argument('--presenter', action='append', default=[], metavar='SLUG',
                help='also build a version for this presenter (repeatable)')
args = ap.parse_args()

decks = find_decks() if args.all else [os.path.abspath(d) for d in args.decks]
if not decks:
    ap.error('give a deck folder or --all')
for d in decks:
    build(d)
    for slug in args.presenter:
        build(d, slug)
