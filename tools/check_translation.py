#!/usr/bin/env python3
"""Check translations: python3 tools/check_translation.py <lang> [slug] — compares content/<lang>/*.json with the English HTML structure."""
import json, re, sys, os, glob
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'tools')); import cta  # CTA blocks are added by build_index.py and ignored here
ABOUT = {'zh-tw':'about-zh','zh-hk':'about-zh-hk','zh-cn':'about-zh-cn','ja':'about-ja','ko':'about-ko','tl':'about-tl','fr':'about-fr','es':'about-es','pt':'about-pt','ru':'about-ru','ar':'about-ar','hi':'about-hi','bn':'about-bn','id':'about-id','th':'about-th'}
def tags(h): return re.findall(r'</?([a-zA-Z0-9]+)', h)
lang = sys.argv[1]; only = sys.argv[2] if len(sys.argv) > 2 else None; bad = 0
for en in sorted(glob.glob(f'{BASE}/content/en/*.json')):
    if only and os.path.basename(en) != only + '.json': continue
    s = os.path.basename(en); p = f'{BASE}/content/{lang}/{s}'
    E = json.load(open(en, encoding='utf-8'))
    if not os.path.exists(p): print('MISSING', lang, s); bad += 1; continue
    try: T = json.load(open(p, encoding='utf-8'))
    except Exception as e: print('BADJSON', p, e); bad += 1; continue
    E['html'] = cta.strip(E['html']); T['html'] = cta.strip(T.get('html', ''))
    errs = []
    for k in ('slug','lang','title','description','html','pubDate','image'):
        if not T.get(k): errs.append('no '+k)
    if T.get('slug') != E['slug']: errs.append('slug')
    if T.get('lang') != lang: errs.append('lang')
    if T.get('pubDate') != E['pubDate'] or T.get('image') != E['image']: errs.append('pubDate/image changed')
    if tags(T.get('html','')) != tags(E['html']): errs.append(f"tag structure differs ({len(tags(T.get('html','')))} vs {len(tags(E['html']))})")
    if 'qgolife.com/about"' in T.get('html',''): errs.append('about link not localized')
    if f'https://qgolife.com/{ABOUT[lang]}"' not in T.get('html',''): errs.append('missing localized about link')
    latin = len(re.findall(r'[A-Za-z]', re.sub(r'<[^>]+>', '', T.get('html','')))) / max(1, len(re.sub(r'<[^>]+>', '', T.get('html',''))))
    if lang not in ('fr','es','pt','tl','id') and latin > 0.25: errs.append(f'too much Latin text ({latin:.0%}) — untranslated?')
    if len(T.get('description','')) > 200: errs.append('description too long')
    print(('OK  ' if not errs else 'FAIL'), lang, s, '; '.join(errs)); bad += bool(errs)
sys.exit(1 if bad else 0)
