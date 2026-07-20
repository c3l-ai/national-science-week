# Future Minds - Creativity and ethics in the age of AI

Site for the National Science Week 2026 touring lecture series presented by
Dr Rebecca Marrone and Dr Maria Vieira, Centre for Change and Complexity in
Learning (C3L), Adelaide University.

Live at **https://national-science-week.c3l.ai**

## What is here

```
index.html      one page, all content
styles.css      design tokens and layout
script.js       map to card linking, scroll reveals
CNAME           custom domain for GitHub Pages
.nojekyll       stops Jekyll from touching the build
assets/img      portraits, poster frames, social card
assets/videos   final video files, if self hosted
```

No build step. Open `index.html` locally, or run `python3 -m http.server` in
this folder.

## Deploy

1. Create the repo and push.

   ```bash
   git init
   git add .
   git commit -m "Future Minds site"
   git branch -M main
   git remote add origin git@github.com:<org>/national-science-week.git
   git push -u origin main
   ```

2. Repo **Settings > Pages**. Source: *Deploy from a branch*, branch `main`,
   folder `/ (root)`.

3. Under **Custom domain** enter `national-science-week.c3l.ai` and save.
   The `CNAME` file in this repo already holds that value.

4. Add this record at whoever hosts DNS for `c3l.ai`:

   | Type  | Name                    | Value                  |
   |-------|-------------------------|------------------------|
   | CNAME | `national-science-week` | `<org>.github.io.`     |

5. Wait for the certificate to issue, then tick **Enforce HTTPS**.

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
