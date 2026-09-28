# Yuchen Zhou's Homepage

Personal website built from scratch, without a template.

Live site: https://www.yuchenzh.com/

## Development

The site uses plain HTML and CSS, with no framework or build step.

Start a local preview from this folder:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173 in your browser.

The `refined-academic` branch contains the design in progress. Review changes
locally before merging them into `main`, which publishes automatically.

## Editing together

- **Biography:** find the `BIO:` comment in `index.html` and replace the placeholder
  paragraph with your introduction. Add more `<p>` elements for additional paragraphs.
- **Profile links:** edit the links in the `profile-links` list in `index.html`.
- **Appearance:** edit the color and font settings at the top of `styles.css`.
  The layout and mobile rules are labeled below them.
- **CV:** replace `assets/documents/Yuchen_Zhou_CV.pdf` to update the linked document.

This first development pass includes the header, biography, portrait, profile links,
and footer. News and publications will be added in a later pass.

## Portrait

`assets/images/portrait.png` is the original 1024 × 1024 photo provided by Yuchen.
Keep this source image intact; adjust its display framing with CSS in the bio section.

## Deployment

GitHub Pages publishes the repository root automatically when changes are pushed
to `main`. No build step is required.

`CNAME` sets the custom domain to `www.yuchenzh.com`. `.nojekyll` tells GitHub Pages
to serve the files directly.
