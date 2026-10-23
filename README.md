# qgo-blog

Articles for the QGO blog at **https://qgolife.com/blog**, in 16 languages.

- `content/en/` — English originals, archived automatically from Soro every hour (`.github/workflows/archive-soro.yml`).
- `content/<lang>/` — translations (zh-tw, zh-hk, zh-cn, ja, ko, tl, fr, es, pt, ru, ar, hi, bn, id, th), added daily.
- `img/` — cover images.
- `index.json` — the list the website reads; rebuilt by `tools/build_index.py`.

The website (Cloudflare Worker `qgo`, file `blog.js`) reads this repository directly, so a new commit here appears on qgolife.com within about 10 minutes. Archived articles stay online even if Soro stops.

Translation rules: `TRANSLATION_BRIEF.md`. Check a language: `python3 tools/check_translation.py <lang>`. See what is missing: `python3 tools/status.py`.
