# Yuchen Zhou's Homepage

Custom-designed personal website built with plain HTML and CSS.

Live site: https://www.yuchenzh.com/

## Development

The site serves plain HTML and CSS, with a small script to respect reduced-motion
preferences for demo videos. Python 3.9+ generates the page from editable templates
and publication data, using only its standard library. No packages need installing.

Build and start a local preview from this folder:

```sh
python3 scripts/build.py
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173 in your browser. After editing a template or publication
data, run the build command again and refresh the page. CSS changes only need a refresh.

The `refined-academic` branch contains the design in progress. Review changes
locally before merging them into `main`, which publishes automatically.

## Source structure

| File | Purpose |
| --- | --- |
| `data/publications.json` | Paper titles, authors, venues, links, and media |
| `templates/index.html` | Page layout, biography, and profile links |
| `templates/publication.html` | Shared layout for one publication |
| `styles.css` | Typography, colors, and responsive layout |
| `assets/js/media.js` | Reduced-motion support for demo videos |
| `scripts/build.py` | Validates data and generates the static page |
| `index.html` | Generated output committed for GitHub Pages; do not edit directly |

## Adding or editing publications

Edit `data/publications.json`. Each object is one paper, displayed in the same
order as the file. For example, add this object to the list, separated from the
previous entry by a comma:

```json
{
  "id": "new-paper",
  "name": "Short paper name",
  "title": "Full Paper Title",
  "authors": ["Yuchen Zhou*", "Coauthor*", "Another Author"],
  "venue": {"name": "Conference 2027"},
  "links": {
    "Paper": "https://example.com/paper",
    "Code": "https://github.com/example/project"
  }
}
```

Then run `python3 scripts/build.py`. No publication HTML needs copying or editing.

- Give each paper a unique `id` using lowercase letters, digits, and hyphens.
- Your name is highlighted automatically. A trailing `*` marks equal contribution;
  the footnote appears automatically when needed.
- `venue.url` is optional. Use `venue.name` for a conference, journal, or preprint label.
- `links.Paper` is required; add any other resource labels, such as `Code`, `Project`,
  `Video`, or `Slides`. The title links to `Project` when present, otherwise `Paper`.
- Text is plain text and is escaped automatically; do not add HTML tags.
- Media is optional. Without it, the paper uses the full row width.

To include a figure, add a `media` field to the paper object and put the image in
`assets/images/publications/`:

```json
"media": {
  "type": "image",
  "src": "assets/images/publications/new-paper.png",
  "width": 1600,
  "height": 900,
  "alt": "A brief description of the figure."
}
```

Use the actual image dimensions, or omit `width` and `height`. Clicking an image
opens the full figure. For an MP4 preview, use:

```json
"media": {
  "type": "video",
  "src": "assets/videos/new-paper.mp4",
  "start": 3,
  "alt": "A brief description of the demonstration."
}
```

`start` is optional and specifies the starting time in seconds. Videos loop silently
without overlaid controls; include a `Video` resource link to open the full recording.
The build checks required fields and local file paths and reports the affected paper
if something needs fixing.

## Other edits

- **Biography:** find the `BIO:` comment in `templates/index.html` and edit your introduction.
  Add more `<p>` elements for additional paragraphs.
- **Profile links:** edit the links in the `profile-links` list in `templates/index.html`.
- **Appearance:** edit the color and font settings at the top of `styles.css`.
  The layout and mobile rules are labeled below them.
- **CV:** replace `assets/documents/Yuchen_Zhou_CV.pdf` to update the linked document.
- **Paper figures:** originals are in `assets/images/publications/`. Click a thumbnail
  on the site to open the full figure. Source links and venue references are recorded
  in that folder's `SOURCES.md`.
- **Point-SAM video:** `assets/videos/point-sam-transformer.mp4` is the original
  Transformer demo from the project page. It loops silently without overlaid controls;
  the Video link opens the full recording. Autoplay is disabled for visitors who
  prefer reduced motion.
- **PartSLIP++ thumbnail:** the full comparison figure shows segmentation results
  across multiple object categories, without cropping. Click to view the original.

## Checks

```sh
python3 scripts/build.py --check
python3 -m unittest discover -s tests
node --check assets/js/media.js
```

The first command fails if the committed HTML is out of date. The tests cover adding
papers, optional media, author formatting, escaping, and invalid data. Node is only
needed for the optional JavaScript syntax check, not for building or serving the site.

## Portrait

`assets/images/portrait.png` is the original 1024 × 1024 photo provided by Yuchen.
Keep this source image intact; adjust its display framing with CSS in the bio section.

## Favicon

`assets/penn-coat-of-arms.svg` is the detailed Penn shield with two open books and
a dolphin, used as the browser-tab icon. The unmodified vector comes from
[Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Shield_of_the_University_of_Pennsylvania.svg),
which credits Penn's logo style guide as its source.

## Deployment

GitHub Pages publishes the repository root automatically when changes are pushed
to `main`. Run `python3 scripts/build.py` before committing changes to the data or
templates, and commit the generated `index.html` together with its sources. GitHub
Pages serves that file directly; it does not run the Python build.

`CNAME` sets the custom domain to `www.yuchenzh.com`. `.nojekyll` tells GitHub Pages
to serve the files directly.
