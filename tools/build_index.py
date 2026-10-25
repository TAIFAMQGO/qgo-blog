#!/usr/bin/env python3
"""Rebuild index.json (the list the website reads) from content/<lang>/<slug>.json."""
import json, os, glob, datetime, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import cta

# Add / refresh the QGO call-to-action blocks in every article (all languages).
for q in glob.glob(os.path.join(ROOT, "content", "*", "*.json")):
    lang = os.path.basename(os.path.dirname(q))
    d = json.load(open(q, encoding="utf-8"))
    if not d.get("html"):
        continue
    h = cta.apply(d["html"], lang)
    if h != d["html"]:
        d["html"] = h
        with open(q, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
LANGS = ["en", "zh-tw", "zh-hk", "zh-cn", "ja", "ko", "tl", "fr", "es", "pt", "ru", "ar", "hi", "bn", "id", "th"]
arts = []
for p in glob.glob(os.path.join(ROOT, "content", "en", "*.json")):
    en = json.load(open(p, encoding="utf-8"))
    slug = en["slug"]
    langs = {}
    for l in LANGS:
        q = os.path.join(ROOT, "content", l, slug + ".json")
        if os.path.exists(q):
            d = json.load(open(q, encoding="utf-8"))
            if d.get("title") and d.get("html"):
                langs[l] = {"title": d["title"], "description": d.get("description", "")}
    img = ""
    for ext in (".webp", ".png", ".jpg", ".jpeg", ".avif", ".gif"):
        if os.path.exists(os.path.join(ROOT, "img", slug + ext)):
            img = "img/" + slug + ext
            break
    arts.append({"slug": slug, "pubDate": en.get("pubDate"), "img": img, "imageOrig": en.get("image", ""), "langs": langs})
arts.sort(key=lambda a: a.get("pubDate") or "", reverse=True)
out = {"articles": arts, "languages": LANGS}
path = os.path.join(ROOT, "index.json")
old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
new = json.dumps(out, ensure_ascii=False, indent=1)
if old != new:
    open(path, "w", encoding="utf-8").write(new)
print(len(arts), "articles;", {l: sum(1 for a in arts if l in a["langs"]) for l in LANGS})
