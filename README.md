# zhaninh.github.io

Personal website of **Nguyen Ngoc Gia Ninh (Aaron)** — Research Assistant at GREEN-X, VinUniversity.

**Live site:** https://zhaninh.github.io (English, default) · https://zhaninh.github.io/vi/ (Tiếng Việt)

## What is here

| Page | English | Tiếng Việt |
|---|---|---|
| Home | `index.html` | `vi/index.html` |
| Journey (interactive 3D map) | `journey.html` | `vi/hanh-trinh.html` |
| Research projects | `work.html`, `work/*.html` | `vi/cong-viec.html`, `vi/cong-viec/*.html` |
| Publications | `publications.html` | `vi/cong-bo.html` |
| About | `about.html` | `vi/gioi-thieu.html` |

The Journey page is a scroll-driven 3D map: each stage of study and research is a stretch of road,
and each project is an object on the map that opens its own project page.

## How it is built

A static site with no framework and no build toolchain beyond Python 3.

```
build.py              content (both languages) + page templates -> writes every .html file
assets/style.css      design tokens and all styles (design rules are in the header comment)
assets/main.js        small page effects (reveal on scroll, menu, typed line)
assets/journey3d.js   the 3D journey map
assets/three.min.js   three.js r160 (vendored)
```

To change content, edit the data at the top of `build.py` (`WORK`, `PUBS`, `JOURNEY`,
`STAGE_PROJECTS`, `ABOUT`) and regenerate:

```bash
python3 build.py
```

The `.html` files are generated; do not edit them by hand. To preview locally:

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

Pushing to `main` publishes the site through GitHub Pages.

## Credits and licences

- [three.js](https://threejs.org) r160 — MIT
- Four-leaf clover icon from [Noto Emoji](https://github.com/googlefonts/noto-emoji) — Apache 2.0
- Fonts: Newsreader, Be Vietnam Pro, JetBrains Mono — SIL Open Font License, served by Google Fonts
- All 3D models on the Journey page are drawn in code for this site.

Text, photo and CV © Nguyen Ngoc Gia Ninh. Please ask before reusing them.
