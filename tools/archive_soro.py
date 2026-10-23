#!/usr/bin/env python3
"""Archive new Soro articles into this repo (English source + cover image).

Run by GitHub Actions every hour. Existing articles are never overwritten,
so translations always match the archived English text.
"""
import json, os, re, sys, time, html, urllib.request, email.utils
import xml.etree.ElementTree as ET

FEED = "https://app.trysoro.com/api/rss/6504eb05-f7f8-40f1-803f-e28b856d64fe"
SITE = "https://qgolife.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = {"content": "http://purl.org/rss/1.0/modules/content/", "media": "http://search.yahoo.com/mrss/"}


def get(url):
    req = urllib.request.Request(url, headers={"user-agent": "qgolife-blog-archiver/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def slug_of(link, title):
    try:
        last = urllib.request.urlparse(link).path.rstrip("/").split("/")[-1]
        if last:
            return urllib.request.unquote(last).lower()
    except Exception:
        pass
    return re.sub(r"[^a-z0-9]+", "-", (title or "").lower()).strip("-")


def fix_links(h):
    h = re.sub(r"<script[\s\S]*?</script>", "", h, flags=re.I)
    h = re.sub(r"<iframe[\s\S]*?</iframe>", "", h, flags=re.I)

    def rep(m):
        s = m.group(1)
        if s in ("about", "privacy", "blog") or s.startswith("about-"):
            return SITE + "/" + s
        return SITE + "/blog/" + s
    return re.sub(r"https?://(?:www\.)?qgolife\.com/([a-z0-9-]+)(?=[\"'#?\s])", rep, h, flags=re.I)


def iso(pub):
    try:
        d = email.utils.parsedate_to_datetime(pub)
        return d.astimezone(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    except Exception:
        return None


def main():
    xml = get(FEED + "?v=" + str(int(time.time() // 600))).decode("utf-8")
    root = ET.fromstring(xml)
    os.makedirs(os.path.join(ROOT, "content", "en"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "img"), exist_ok=True)
    new = 0
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        slug = slug_of(link, title)
        if not slug or not title:
            continue
        body = it.findtext("content:encoded", namespaces=NS) or it.findtext("description") or ""
        enc = it.find("enclosure")
        image = enc.get("url") if enc is not None else ""
        if not image:
            mc = it.find("media:content", NS)
            image = mc.get("url") if mc is not None else ""
        desc = re.sub(r"<[^>]+>", "", html.unescape(it.findtext("description") or "")).strip()
        path = os.path.join(ROOT, "content", "en", slug + ".json")
        if not os.path.exists(path):
            doc = {"slug": slug, "lang": "en", "title": title, "description": desc, "html": fix_links(body),
                   "pubDate": iso(it.findtext("pubDate") or ""), "image": image,
                   "guid": (it.findtext("guid") or "").strip(), "source": "soro"}
            with open(path, "w", encoding="utf-8") as f:
                json.dump(doc, f, ensure_ascii=False, indent=1)
            new += 1
            print("archived", slug)
        if image:
            ext = os.path.splitext(urllib.request.urlparse(image).path)[1].lower() or ".webp"
            ip = os.path.join(ROOT, "img", slug + ext)
            if not os.path.exists(ip):
                try:
                    data = get(image)
                    with open(ip, "wb") as f:
                        f.write(data)
                    print("image", os.path.basename(ip), len(data))
                except Exception as e:
                    print("image failed", slug, e, file=sys.stderr)
    print("new articles:", new)


if __name__ == "__main__":
    main()
