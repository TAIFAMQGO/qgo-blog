# QGO blog translation brief

QGO (qgolife.com) is a queue-management product: customers scan a QR code, take a number on their own phone (no app download needed, works in the browser; there is also an Android app), and get alerted when their turn is near. No ticket machine, no paper tickets, 16 languages. The English blog articles were written by an SEO tool. We publish a native-quality version of every article in 15 more languages.

## Files
- English sources: `content/en/<slug>.json` (fields: slug, lang, title, description, html, pubDate, image, guid, source).
- Write each translation to `content/<lang>/<slug>.json` (create the folder), UTF-8, valid JSON, with exactly these fields:
  `{"slug": <same>, "lang": "<lang code below>", "title": ..., "description": ..., "html": ..., "pubDate": <copy exactly>, "image": <copy exactly>, "source": "soro", "translatedFrom": "en", "translatedAt": "<today's date, YYYY-MM-DD>"}`
- Write the file with a short Python script (json.dump(..., ensure_ascii=False, indent=1)) so escaping is always correct — do not hand-write JSON escapes.
- After writing a language, run `python3 tools/check_translation.py <lang>` from the repo root and fix anything marked FAIL. Every article you translated must print OK (pass the slug as a second argument to check just one).

## Call-to-action blocks
Every article (all languages, English included) contains two `<div class="qgo-cta …">` blocks that promote QGO. They are added automatically by `tools/build_index.py` from the copy in `tools/cta.py`. When translating, skip those blocks — do not translate or copy them; `check_translation.py` ignores them and `build_index.py` inserts the localized versions. To change the promo text or link, edit `tools/cta.py` and run `python3 tools/build_index.py`.

## Rules
1. Translate the meaning naturally for readers in that market — like a professional local copywriter, not word-for-word. Keep every fact; add nothing, drop nothing. No invented statistics, features or prices.
2. HTML: keep exactly the same tags in the same order (same number of <p>, <h2>, <ul>, <li>, <strong>, <a> …). Only the text between tags changes.
3. The one link `https://qgolife.com/about` must point to the localized About page: zh-tw→about-zh, zh-hk→about-zh-hk, zh-cn→about-zh-cn, ja→about-ja, ko→about-ko, tl→about-tl, fr→about-fr, es→about-es, pt→about-pt, ru→about-ru, ar→about-ar, hi→about-hi, bn→about-bn, id→about-id, th→about-th (e.g. `https://qgolife.com/about-ja`).
4. Title: a natural, search-friendly headline in the target language that keeps the article's main keyword idea (e.g. "no app queue system" → the term local people would actually search for). Description: one sentence, max ~150 characters (CJK: max ~80 characters).
5. Keep the brand as "QGO". In Chinese you may write "QGO 叫號通" (zh-tw/zh-hk) or "QGO 叫号通" (zh-cn) the first time it appears in the body, "QGO" after that. Keep "QR code"-type terms as locals write them.
6. Do not translate the slug, pubDate or image.

## Language codes and style (match the wording already used on qgolife.com)
- `zh-tw` 繁體中文（台灣）: 叫號, 號碼單, 抽號機, 排隊, 店家, 客人, 櫃台, 工作人員, 手機, QR Code. Natural Taiwanese written style.
- `zh-hk` 繁體中文（香港書面語）: 取籌/籌號, 籌號紙, 取籌機, 排隊, 商戶, 客人, 櫃枱/櫃位, 職員, 手機, QR Code; formal written HK style (毋須、亦、即可), NOT Cantonese colloquial (no 嘅/唔/喺).
- `zh-cn` 简体中文: 取号, 排队, 号码单, 取号机, 商家, 顾客, 窗口/柜台, 工作人员, 手机, 二维码.
- `ja` 日本語: です・ます調. 順番待ち, 整理券, 発券機, お客様, 店舗/お店, スタッフ, スマホ, QRコード.
- `ko` 한국어: formal 합니다체. 대기, 번호표, 번호표 발급기, 고객, 매장, 직원, 휴대폰, QR 코드.
- `th` ไทย: คิว, บัตรคิว, เครื่องกดบัตรคิว, ลูกค้า, ร้าน, พนักงาน, มือถือ, QR Code. Polite neutral tone.
- `fr` français (France): file d'attente, ticket, borne/distributeur de tickets, client, commerce, personnel, téléphone, QR code. Vous.
- `es` español (neutral Latin America, as on the site): fila, turno, dispensador de turnos, cliente, negocio, personal, teléfono, código QR. Tú.
- `pt` português do Brasil: fila, senha, máquina de senhas, cliente, loja/negócio, equipe, celular, QR code. Você.
- `ru` русский: очередь, талон, терминал для талонов, клиент, заведение/бизнес, персонал, телефон, QR-код. Вы.
- `ar` العربية الفصحى المعاصرة: طابور, تذكرة, جهاز تذاكر, العميل, المتجر/النشاط التجاري, الموظفون, الهاتف, رمز QR. Text only — the site adds dir="rtl" itself.
- `tl` Tagalog (natural Filipino; common English tech words like app, QR code, staff, customer are fine as Filipinos use them): pila, numero, tiket, tindahan/negosyo, customer, staff, phone.
- `hi` हिन्दी: कतार, टोकन, टोकन मशीन, ग्राहक, दुकान/व्यवसाय, स्टाफ़, फ़ोन, QR कोड. Natural modern Hindi (common English loanwords OK).
- `bn` বাংলা: সারি/লাইন, টোকেন, টোকেন মেশিন, গ্রাহক, দোকান/ব্যবসা, কর্মী, ফোন, QR কোড.
- `id` Bahasa Indonesia: antrean, nomor antrean, tiket, mesin tiket, pelanggan, toko/usaha, staf, ponsel, kode QR.
