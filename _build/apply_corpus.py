"""Rewrite corpus-derived claims in hand-maintained pages, in place.

Surfaces without a deck builder (akka-verify, website industry pages) keep the
number visible in the file inside a marker, and this script rewrites what's
inside the marker from the live corpus. The files stay directly editable and
viewable; only the marked number is machine-owned.

Markers:
    text       <!--corpus:regulations-->190<!--/corpus-->
    attribute  <div data-corpus="regulations" data-count="190">

Run with --check to fail instead of writing (for verifying a deck is current).
"""

import os
import re
import sys
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus_counts

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

TARGETS = [
    'akka-overview/index.html',
    'akka-sdk/index.html',
    'akka-verify/index.html',
    'akka-verify/risk-survey/index.html',
    'website/industry-*.html',
    'website/industry-*.md',
]

TEXT_MARKER = re.compile(r'(<!--corpus:([a-z-]+)-->)(.*?)(<!--/corpus-->)', re.S)
TAGGED_ELEMENT = re.compile(r'<[^>]*\bdata-corpus="([a-z-]+)"[^>]*>')
DATA_COUNT = re.compile(r'(\bdata-count=")[^"]*(")')


def substitute(text, values, path, problems):
    def text_repl(m):
        open_tag, name, _old, close_tag = m.groups()
        if name not in values:
            problems.append(f'{path}: unknown corpus claim "{name}"')
            return m.group(0)
        return f'{open_tag}{values[name]}{close_tag}'

    def attr_repl(m):
        tag, name = m.group(0), m.group(1)
        if name not in values:
            problems.append(f'{path}: unknown corpus claim "{name}"')
            return tag
        if not DATA_COUNT.search(tag):
            problems.append(f'{path}: data-corpus="{name}" with no data-count to rewrite')
            return tag
        return DATA_COUNT.sub(lambda d: f'{d.group(1)}{values[name]}{d.group(2)}', tag)

    text = TEXT_MARKER.sub(text_repl, text)
    return TAGGED_ELEMENT.sub(attr_repl, text)


def main():
    check_only = '--check' in sys.argv
    values = corpus_counts.values()

    # Paths on the command line narrow the run to those files.
    targets = [a for a in sys.argv[1:] if not a.startswith('--')] or TARGETS
    problems, changed, scanned = [], [], 0
    for pattern in targets:
        for path in sorted(glob.glob(os.path.join(ROOT, pattern))):
            scanned += 1
            with open(path, encoding='utf-8') as f:
                before = f.read()
            after = substitute(before, values, os.path.relpath(path, ROOT), problems)
            if after == before:
                continue
            changed.append(os.path.relpath(path, ROOT))
            if not check_only:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(after)

    for p in problems:
        print(f'ERROR: {p}')

    print(f'corpus: {"  ".join(f"{k}={v}" for k, v in sorted(values.items()))}')
    print(f'scanned {scanned} files, {len(changed)} {"stale" if check_only else "updated"}')
    for c in changed:
        print(f'  {c}')

    if problems:
        sys.exit(1)
    if check_only and changed:
        print('\nRun without --check to update.')
        sys.exit(1)


if __name__ == '__main__':
    main()
