# Yuchen Zhou's Homepage

Personal website built from scratch, without a template.

Live site: https://www.yuchenzh.com/

## Development

The site uses plain HTML and CSS, with a small script to respect reduced-motion
preferences for the demo video. There is no framework or build step.

Start a local preview from this folder:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173 in your browser.

The `refined-academic` branch contains the design in progress. Review changes
locally before merging them into `main`, which publishes automatically.

## Editing together

- **Biography:** find the `BIO:` comment in `index.html` and edit your introduction.
  Add more `<p>` elements for additional paragraphs.
- **Profile links:** edit the links in the `profile-links` list in `index.html`.
- **Appearance:** edit the color and font settings at the top of `styles.css`.
  The layout and mobile rules are labeled below them.
- **CV:** replace `assets/documents/Yuchen_Zhou_CV.pdf` to update the linked document.
- **Publications:** find the `PUBLICATIONS:` comment in `index.html`. Each `<article>`
  contains a figure, title, authors, venue, and resource links. Reorder the articles
  to change their display order. Your name uses `<strong>`; `*` marks equal contribution.
- **Paper figures:** originals are in `assets/images/publications/`. Click a thumbnail
  on the site to open the full figure. Source links and venue references are recorded
  in that folder's `SOURCES.md`.
- **Point-SAM video:** `assets/videos/point-sam-transformer.mp4` is the original
  Transformer demo from the project page. It loops silently without overlaid controls;
  the Video link opens the full recording. Autoplay is disabled for visitors who
  prefer reduced motion.
- **PartSLIP++ thumbnail:** the full comparison figure shows segmentation results
  across multiple object categories, without cropping. Click to view the original.

The current development version includes the header, biography, portrait, profile
links, three selected publications, and footer.

## Portrait

`assets/images/portrait.png` is the original 1024 × 1024 photo provided by Yuchen.
Keep this source image intact; adjust its display framing with CSS in the bio section.

## Deployment

GitHub Pages publishes the repository root automatically when changes are pushed
to `main`. No build step is required.

`CNAME` sets the custom domain to `www.yuchenzh.com`. `.nojekyll` tells GitHub Pages
to serve the files directly.
