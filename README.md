# Future Minds - Creativity and ethics in the age of AI

Site for the National Science Week 2026 touring lecture series presented by
Dr Rebecca Marrone and Dr Maria Vieira, Centre for Change and Complexity in
Learning (C3L), Adelaide University.

Live at **https://c3l-ai.github.io/national-science-week/**

## What is here

```
index.html      one page, all content
styles.css      design tokens and layout
script.js       map to card linking, scroll reveals
.nojekyll       stops Jekyll from touching the build
assets/img      portraits, poster frames, social card
assets/videos   final video files, if self hosted
tools/          pre-deploy link and integrity check
.github/        deployment workflow
```

No build step. Open `index.html` locally, or run `python3 -m http.server` in
this folder.

## Deploy

Every push to `main` publishes the site. The workflow is
`.github/workflows/deploy.yml`: one job that checks the site, uploads the repo
as-is, and deploys it. No build step, no Jekyll.

The check step runs `tools/check_links.py`, which fails the build if a local
file reference is broken, an `#anchor` points nowhere, or a map pin and its
event card have drifted apart. That last one matters, because event data lives
in the markup twice and is tied together by `data-stop`.

### Setup

1. Push to `main`.

   ```bash
   git init
   git add .
   git commit -m "Future Minds site"
   git branch -M main
   git remote add origin git@github.com:c3l-ai/national-science-week.git
   git push -u origin main
   ```

2. **Settings > Pages > Build and deployment > Source: GitHub Actions.**

   Pages has to be switched on here before anything publishes. Until it is, the
   `configure-pages` step has nothing to configure and the site 404s at the
   `github.io` URL.

3. Push again, or **Actions > Deploy to GitHub Pages > Run workflow**.

### Running the check locally

```bash
python3 tools/check_links.py              # local refs, exits 1 on failure
python3 tools/check_links.py --external   # pings booking links too
```

Worth running before pushing any change to dates or venues. To make it
automatic:

```bash
printf '#!/bin/sh\npython3 tools/check_links.py\n' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Adding the custom domain later

The site is on the default `github.io` URL for now. When you want
`national-science-week.c3l.ai`:

1. Add a DNS record at whoever hosts `c3l.ai`:

   | Type  | Name                    | Value                |
   |-------|-------------------------|----------------------|
   | CNAME | `national-science-week` | `c3l-ai.github.io.`  |

2. **Settings > Pages > Custom domain**, enter the domain, save. GitHub commits
   a `CNAME` file to the repo for you.

3. Update `og:url` in `index.html` to the new address.

4. Wait for the domain check to pass and the certificate to issue, then tick
   **Enforce HTTPS**.

All asset paths in the site are relative, so it works at both the subpath and
the apex without edits.

### If a run hangs on "waiting for a runner"

That is Actions capacity or account state, not the site. Check
githubstatus.com, then org Settings > Actions > General. Nothing in the repo
will fix it. Branch deployment (Settings > Pages > Source: Deploy from a
branch, `main`, `/ (root)`) publishes without a runner if you need the site up
in the meantime.

## Adding the videos

Each card in the `#research` section is a placeholder. To turn one on, replace
the `.vcard__frame` div with an embed and drop the `is-pending` class:

```html
<article class="vcard">
  <div class="vcard__frame">
    <iframe src="https://www.youtube.com/embed/VIDEO_ID"
            title="Creativity and machines"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture"
            allowfullscreen style="width:100%;height:100%;border:0"></iframe>
  </div>
  <h3>Creativity and machines</h3>
  <p>How generative tools change what counts as an original idea.</p>
</article>
```

For self hosted files use `<video controls poster="assets/img/poster-01.jpg" src="assets/videos/01-....mp4">`.

## Adding the portraits

In `#presenters`, swap the placeholder div for an image. The CSS already applies
a duotone-ish grayscale treatment and hides the placeholder label once an `img`
is present.

```html
<div class="pcard__portrait">
  <img src="assets/img/rebecca-marrone.jpg" alt="Dr Rebecca Marrone">
</div>
```

## Editing the event list

Event data lives in the markup twice, on purpose, so there is no JS dependency:

- the SVG map, in the `.pins` group, one `<g class="pin" data-stop="...">` per stop
- the card list, one `<li class="stop" data-stop="...">` per stop

The `data-stop` value ties the two together. Keep them matching and the hover
linking keeps working.

## Design notes

Two-ink risograph poster: process blue `#2438E0` and fluoro pink `#FF3D8A` on an
oat stock `#E7E7E0`, with a paper grain overlay and halftone dot fields standing
in for the ink screens. Bricolage Grotesque for display, Newsreader for body,
IBM Plex Mono for dates and labels. The signature element is the halftone map of
South Australia with the five stops numbered in calendar order.

## Source of event details

Listings on scienceweek.net.au, retrieved July 2026. Check dates and booking
links against the official listings before promoting the site.
