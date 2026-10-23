#!/usr/bin/env python3
"""List which archived articles are still missing which translations."""
import os, glob, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ["zh-tw", "zh-hk", "zh-cn", "ja", "ko", "tl", "fr", "es", "pt", "ru", "ar", "hi", "bn", "id", "th"]
todo = {}
for p in sorted(glob.glob(os.path.join(ROOT, "content", "en", "*.json"))):
    s = os.path.basename(p)[:-5]
    miss = [l for l in LANGS if not os.path.exists(os.path.join(ROOT, "content", l, s + ".json"))]
    if miss:
        todo[s] = miss
print(json.dumps(todo, indent=1) if todo else "All articles are translated into all 15 languages.")
