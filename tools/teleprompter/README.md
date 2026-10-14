# Teleprompter builder

Turns a deck's `SPEAKER-NOTES.md` into word-for-word teleprompter files, including the
`.textream` format that the [Textream](https://github.com/f/textream) app opens.

```bash
python3 tools/teleprompter/build.py _wip/governance                      # generic intro
python3 tools/teleprompter/build.py _wip/governance --presenter smitty   # adds a smitty version
python3 tools/teleprompter/build.py --all                                # every deck with a SPEAKER-NOTES.md
```

`--presenter` is repeatable and takes a slug from the deck's `presenters/` folder.

## Output

Files land in `<deck>/teleprompter/` and are generated. Edit the notes, not these files;
the next run overwrites them. They are committed so nobody needs Python to load a script.

| File | Use |
|---|---|
| `<deck>.textream` | Open in Textream. Generic intro. |
| `<deck>-<presenter>.textream` | Open in Textream. Intro names the presenter. |
| `<deck>.md`, `<deck>-<presenter>.md` | Readable copy, with slide headings and a word count. |

`<deck>` is the deck folder's name, lowercase, with underscores turned into hyphens
(`_wip/governance` gives `governance`).

## What the notes file has to contain

`<deck>/SPEAKER-NOTES.md` is the single source. The builder reads it like this:

- Each `## ` section is one slide. It must carry a `- **Script**:` block followed by a
  `- **Land**` line. The script text is indented under the Script bullet.
- A line of three hyphens (`---`) inside a script starts a new teleprompter page. A slide
  with no break is one page.
- A line of the form `>>> ... <<<` is a demo cue. It passes through unchanged, so it shows
  on the prompter.
- A line that is entirely `[like this]` is an on-screen cue. It passes through, shows on the
  prompter in brackets, and isn't counted as spoken words.
- `>>> DEMO ... <<<` opens a demo and `>>> BACK TO DECK <<<` closes it. Words between them
  are reported as demo words in the footer of the readable copy.
- `- **Teleprompter**: omitted` anywhere in a section skips it. The governance deck uses
  this for the customer-specific slide.
- `{{presenter-intro}}` becomes `I'm <first name>, <title>.` for a presenter, using
  `name` and `title` from `<deck>/presenters/<slug>.json`. The first `, ` in the title
  is spoken as ` at `, so "Field CTO, Akka" becomes "Field CTO at Akka". With no
  presenter it becomes "Thank you for joining me." An unknown slug stops the build.

Write scripts for the ear: plain sentences, numbers spelled out, no abbreviations the
speaker would stumble on, and no stage directions inside the prose.

## The .textream format

A `.textream` file is a JSON array of strings, one string per page, with no other
structure. The Textream README doesn't document the format. This was learned from a file
saved by the app. The builder writes it compact, with the text left as UTF-8.

The README also says bracketed text gets a "cue color" in the app. The builder doesn't use
square brackets, and `>>> ... <<<` demo cues show as ordinary text. I haven't tried
brackets.

## Working with edits made in Textream

Textream edits its own copy of the script. A change made there doesn't flow back. If you
edit in the app, copy the wording into `SPEAKER-NOTES.md` and regenerate; otherwise the
next run overwrites it.
