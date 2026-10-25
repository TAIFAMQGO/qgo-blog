#!/usr/bin/env python3
"""QGO call-to-action blocks for every blog article, in all 16 languages.

Each article gets two blocks, both wrapped in <div class="qgo-cta">:
  - a short line after the first paragraph
  - a full block at the end of the article
apply() is idempotent: it removes old CTA blocks and inserts the current ones,
so editing the copy here and running tools/build_index.py updates every article.
build_index.py calls this automatically (hourly workflow and daily translation job).
"""
import re

URL = "https://qgolife.com/?utm_source=blog&utm_medium=article&utm_campaign={pos}&utm_content={lang}"

# lang: (top line before link, top link text, bottom heading, bottom paragraph, bottom button text)
CTA = {
 "en": ("With <strong>QGO</strong>, customers take a number just by scanning a QR code — no app download, no ticket machine.",
        "See how QGO works →",
        "Try QGO in your store",
        "QGO turns any counter into a smart digital queue: customers scan a QR code, take a number on their own phone, and get an alert when their turn is near. No app download, no ticket machine, no paper tickets — in 16 languages.",
        "Install QGO now — it takes one tap →"),
 "zh-tw": ("<strong>QGO 叫號通</strong>：客人掃 QR Code 就能用手機抽號，不用下載 App，也不用抽號機。",
        "馬上體驗 QGO →",
        "在你的店裡用 QGO 叫號",
        "QGO 讓任何櫃台都變成智慧叫號系統：客人掃 QR Code、用自己的手機抽號，快輪到時就會收到通知。不用下載 App、不用抽號機、不用號碼單，支援 16 種語言。",
        "立即安裝 QGO，一鍵完成 →"),
 "zh-hk": ("<strong>QGO 叫號通</strong>：客人掃描 QR Code 即可用手機取籌，毋須下載 App，亦毋須取籌機。",
        "立即體驗 QGO →",
        "在你的商戶使用 QGO",
        "QGO 令任何櫃枱都能變成智能取籌系統：客人掃描 QR Code，以自己的手機取籌，快將輪到時即會收到通知。毋須下載 App、毋須取籌機、毋須籌號紙，支援 16 種語言。",
        "立即安裝 QGO，一按即成 →"),
 "zh-cn": ("<strong>QGO 叫号通</strong>：顾客扫二维码就能用手机取号，无需下载 App，也不用取号机。",
        "立即体验 QGO →",
        "在你的店里用上 QGO",
        "QGO 让任何柜台都变成智能排队取号系统：顾客扫二维码、用自己的手机取号，快轮到时就会收到提醒。无需下载 App、无需取号机、无需号码单，支持 16 种语言。",
        "立即安装 QGO，一键完成 →"),
 "ja": ("<strong>QGO</strong>なら、お客様はQRコードを読み取るだけでスマホから順番待ちに登録できます。アプリのダウンロードも発券機も不要です。",
        "QGOを試してみる →",
        "あなたのお店でもQGOを",
        "QGOは、どんな受付でもスマートな順番待ちシステムに変えます。お客様はQRコードを読み取ってご自身のスマホで整理券を受け取り、順番が近づくと通知が届きます。アプリのダウンロード、発券機、紙の整理券は不要。16言語に対応しています。",
        "今すぐQGOをインストール（ワンタップで完了）→"),
 "ko": ("<strong>QGO</strong>를 사용하면 고객은 QR 코드를 스캔하는 것만으로 휴대폰에서 번호표를 받을 수 있습니다. 앱 다운로드도, 번호표 발급기도 필요 없습니다.",
        "QGO 알아보기 →",
        "우리 매장에도 QGO를",
        "QGO는 어떤 창구든 스마트한 대기 시스템으로 바꿔 줍니다. 고객은 QR 코드를 스캔해 자신의 휴대폰으로 번호표를 받고, 차례가 다가오면 알림을 받습니다. 앱 다운로드, 번호표 발급기, 종이 번호표가 필요 없으며 16개 언어를 지원합니다.",
        "지금 QGO 설치하기 — 한 번의 탭이면 됩니다 →"),
 "tl": ("Sa <strong>QGO</strong>, kukuha ng numero ang customer sa pag-scan lang ng QR code — walang app na kailangang i-download at walang ticket machine.",
        "Subukan ang QGO →",
        "Gamitin ang QGO sa iyong tindahan",
        "Ginagawang smart digital na pila ng QGO ang kahit anong counter: i-scan ng customer ang QR code, kukuha ng numero sa sarili niyang phone, at makakatanggap ng alert kapag malapit na ang turn niya. Walang app na ida-download, walang ticket machine, walang papel na tiket — at available sa 16 na wika.",
        "I-install ang QGO ngayon — isang tap lang →"),
 "fr": ("Avec <strong>QGO</strong>, vos clients prennent un ticket en scannant simplement un QR code, sans télécharger d'application ni passer par une borne.",
        "Découvrir QGO →",
        "Essayez QGO dans votre commerce",
        "QGO transforme n'importe quel comptoir en file d'attente numérique intelligente : le client scanne un QR code, prend un ticket sur son propre téléphone et reçoit une alerte quand son tour approche. Pas d'application à télécharger, pas de distributeur de tickets, pas de tickets papier — et 16 langues disponibles.",
        "Installez QGO maintenant, en un seul geste →"),
 "es": ("Con <strong>QGO</strong>, tus clientes toman turno escaneando un código QR, sin descargar ninguna app ni usar un dispensador de turnos.",
        "Conoce QGO →",
        "Prueba QGO en tu negocio",
        "QGO convierte cualquier mostrador en una fila digital inteligente: el cliente escanea un código QR, toma su turno desde su propio teléfono y recibe un aviso cuando se acerca su momento. Sin descargar apps, sin dispensador de turnos, sin papel, y en 16 idiomas.",
        "Instala QGO ahora con un solo toque →"),
 "pt": ("Com o <strong>QGO</strong>, seus clientes pegam senha escaneando um QR code, sem baixar aplicativo e sem máquina de senhas.",
        "Conheça o QGO →",
        "Experimente o QGO na sua loja",
        "O QGO transforma qualquer balcão em uma fila digital inteligente: o cliente escaneia um QR code, pega a senha no próprio celular e recebe um aviso quando a vez dele estiver chegando. Sem baixar aplicativo, sem máquina de senhas, sem papel — e em 16 idiomas.",
        "Instale o QGO agora com um toque →"),
 "ru": ("С <strong>QGO</strong> клиенты получают талон, просто отсканировав QR-код, — без скачивания приложения и без терминала для талонов.",
        "Узнать о QGO →",
        "Попробуйте QGO в своём заведении",
        "QGO превращает любую стойку в умную электронную очередь: клиент сканирует QR-код, получает талон на своём телефоне и уведомление, когда подходит его очередь. Не нужно скачивать приложение, ставить терминал или печатать бумажные талоны. Поддерживается 16 языков.",
        "Установите QGO прямо сейчас — в одно касание →"),
 "ar": ("مع <strong>QGO</strong> يحصل العملاء على تذكرة بمجرد مسح رمز QR، دون تنزيل أي تطبيق ودون جهاز تذاكر.",
        "تعرّف على QGO ←",
        "جرّب QGO في متجرك",
        "يحوّل QGO أي مكتب خدمة إلى طابور رقمي ذكي: يمسح العميل رمز QR، ويحصل على تذكرته على هاتفه، ويتلقى تنبيهًا عندما يقترب دوره. لا حاجة إلى تنزيل تطبيق، ولا جهاز تذاكر، ولا تذاكر ورقية، مع دعم 16 لغة.",
        "ثبّت QGO الآن بلمسة واحدة ←"),
 "hi": ("<strong>QGO</strong> के साथ ग्राहक सिर्फ़ QR कोड स्कैन करके टोकन ले सकते हैं — न ऐप डाउनलोड करने की ज़रूरत, न टोकन मशीन की।",
        "QGO के बारे में जानें →",
        "अपनी दुकान में QGO आज़माएँ",
        "QGO किसी भी काउंटर को एक स्मार्ट डिजिटल कतार में बदल देता है: ग्राहक QR कोड स्कैन करता है, अपने फ़ोन पर टोकन लेता है और बारी पास आने पर अलर्ट पाता है। कोई ऐप डाउनलोड नहीं, कोई टोकन मशीन नहीं, कोई काग़ज़ी टोकन नहीं — और 16 भाषाओं में उपलब्ध।",
        "अभी QGO इंस्टॉल करें — बस एक टैप में →"),
 "bn": ("<strong>QGO</strong>-তে গ্রাহক শুধু QR কোড স্ক্যান করেই টোকেন নিতে পারেন — কোনো অ্যাপ ডাউনলোড বা টোকেন মেশিনের দরকার নেই।",
        "QGO সম্পর্কে জানুন →",
        "আপনার দোকানে QGO ব্যবহার করে দেখুন",
        "QGO যেকোনো কাউন্টারকে একটি স্মার্ট ডিজিটাল সারিতে বদলে দেয়: গ্রাহক QR কোড স্ক্যান করেন, নিজের ফোনে টোকেন নেন এবং পালা কাছে এলে সতর্কবার্তা পান। কোনো অ্যাপ ডাউনলোড নেই, টোকেন মেশিন নেই, কাগজের টোকেন নেই — আর ১৬টি ভাষায় চলে।",
        "এখনই QGO ইনস্টল করুন — এক ট্যাপেই →"),
 "id": ("Dengan <strong>QGO</strong>, pelanggan mengambil nomor antrean cukup dengan memindai kode QR — tanpa mengunduh aplikasi dan tanpa mesin tiket.",
        "Kenali QGO →",
        "Coba QGO di toko Anda",
        "QGO mengubah loket mana pun menjadi antrean digital yang cerdas: pelanggan memindai kode QR, mengambil nomor antrean di ponselnya sendiri, dan mendapat notifikasi saat gilirannya hampir tiba. Tanpa unduh aplikasi, tanpa mesin tiket, tanpa tiket kertas — tersedia dalam 16 bahasa.",
        "Pasang QGO sekarang, cukup sekali ketuk →"),
 "th": ("ด้วย <strong>QGO</strong> ลูกค้ารับบัตรคิวได้เพียงสแกน QR Code ไม่ต้องดาวน์โหลดแอป และไม่ต้องใช้เครื่องกดบัตรคิว",
        "ทำความรู้จัก QGO →",
        "ลองใช้ QGO ที่ร้านของคุณ",
        "QGO เปลี่ยนเคาน์เตอร์ไหนก็ได้ให้เป็นระบบคิวดิจิทัลอัจฉริยะ ลูกค้าสแกน QR Code รับบัตรคิวบนมือถือของตัวเอง และได้รับแจ้งเตือนเมื่อใกล้ถึงคิว ไม่ต้องดาวน์โหลดแอป ไม่ต้องมีเครื่องกดบัตรคิว ไม่ต้องใช้บัตรคิวกระดาษ รองรับ 16 ภาษา",
        "ติดตั้ง QGO เลยตอนนี้ แตะครั้งเดียวก็เสร็จ →"),
}

BLOCK_RE = re.compile(r'\n?<div class="qgo-cta[^"]*">.*?</div>\n?', re.S)


def strip(html):
    """Remove all CTA blocks (used by the checker and before re-inserting)."""
    return BLOCK_RE.sub("\n", html).strip("\n") if html else html


def blocks(lang):
    t = CTA.get(lang, CTA["en"])
    top = (f'<div class="qgo-cta qgo-cta-top"><p>{t[0]} '
           f'<a href="{URL.format(pos="cta_top", lang=lang)}">{t[1]}</a></p></div>')
    bottom = (f'<div class="qgo-cta qgo-cta-bottom"><h2>{t[2]}</h2>\n<p>{t[3]}</p>\n'
              f'<p><strong><a href="{URL.format(pos="cta_bottom", lang=lang)}">{t[4]}</a></strong></p></div>')
    return top, bottom


def apply(html, lang):
    body = strip(html or "")
    top, bottom = blocks(lang)
    i = body.find("</p>")
    if i >= 0:
        i += 4
        body = body[:i] + "\n" + top + body[i:]
    else:
        body = top + "\n" + body
    return body + "\n" + bottom
