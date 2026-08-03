# -*- coding: utf-8 -*-
import re, base64, io, html as htmlmod, subprocess, os
import segno
from menu_data import load_menu

# Paths resolve relative to this script so it runs anywhere (local Mac or GitHub cloud).
HERE = os.path.dirname(os.path.abspath(__file__))
def _first(*paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return paths[0]
# GFS Didot @font-face source: sibling index.html in the repo, else the Mac clone.
WEB = _first(os.path.join(HERE, "..", "index.html"), "/Users/stavros/oniropetra-menu/index.html")
LOGO = os.path.join(HERE, "assets", "logo_round.png")
OUTDIR = HERE
PDF = os.path.abspath(os.path.join(HERE, "..", "MENU_Mikro_Pelion_NEOS_KATALOGOS.pdf"))
LIVE_URL = "https://stivakos.github.io/oniropetra-menu/"
MENU = os.path.join(HERE, "..", "menu.txt")

os.makedirs(OUTDIR, exist_ok=True)
web = open(WEB, encoding="utf-8").read()

# --- fonts (GFS Didot @font-face blocks) ---
faces = re.findall(r'@font-face\s*\{[^}]*\}', web)
faces = [f for f in faces if "GFS Didot" in f]
FONTS = "\n".join(faces)

# --- logo data uri ---
logo_b64 = base64.b64encode(open(LOGO, "rb").read()).decode()
LOGO_URI = f"data:image/png;base64,{logo_b64}"

# --- QR data uri (live menu) ---
buf = io.BytesIO()
segno.make(LIVE_URL, error="h").save(buf, kind="png", scale=10, border=1, dark="#24384B", light="#FFFFFF")
QR_URI = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def esc(s): return htmlmod.escape(s, quote=False)

def item(gr, en=None, price=None, dgr=None, den=None):
    name = f'<span class="gr">{esc(gr)}</span>'
    if en: name += f'<span class="en">{esc(en)}</span>'
    line = f'<div class="il">{name}<span class="pr">{esc(price)}</span></div>' if price else f'<div class="il">{name}</div>'
    desc = ""
    if dgr or den:
        if dgr:
            d = esc(dgr)
            if den: d += f' <span class="den">/ {esc(den)}</span>'
        else:
            d = f'<span class="den">{esc(den)}</span>'
        desc = f'<p class="ds">{d}</p>'
    return f'<li class="it">{line}{desc}</li>'

def section(gr, en, items):
    head = f'<div class="sh"><h2>{esc(gr)}</h2>'
    if en: head += f'<span class="enl">{esc(en)}</span>'
    head += '</div>'
    return f'<section>{head}<ul class="items">{"".join(items)}</ul></section>'

# ---------------- CONTENT (from menu.txt) ----------------
CATS = {c["gr"]: c for c in load_menu(MENU)}

def sec(cat_gr, items=None, en=None):
    c = CATS[cat_gr]
    src = c["items"] if items is None else items
    lis = [item(it["gr"], it["en"] or None, it["price"] or None,
                it["dgr"] or None, it["den"] or None) for it in src]
    return section(c["gr"], c["en"] if en is None else en, lis)

coffee   = sec("Καφές")
refresh  = sec("Ροφήματα")
alcohol  = sec("Ποτά")
breakfast= sec("Πρωινό")
barbites = sec("Σνακ")
burgers  = sec("Burgers")
pizzas   = sec("Πίτσες")
salads   = sec("Σαλάτες")
mains    = sec("Μερίδες Φαγητού")
pasta    = sec("Μακαρονάδες")
# Γλυκά: split across the two page-3 columns for balance
_gl = CATS["Γλυκά"]["items"]
_half = (len(_gl) + 1) // 2
dessert_l = sec("Γλυκά", items=_gl[:_half])
dessert_r = sec("Γλυκά", items=_gl[_half:], en="Dessert (συν.)")

# ---------------- HEADER / FOOTER ----------------
HEADER = '''<header class="cove">
  <div class="cove-sun"></div>
  <h1 class="brand">MENU</h1>
  <svg class="cove-waves" viewBox="0 0 800 110" preserveAspectRatio="none">
    <path d="M0,58 C140,28 260,88 400,62 C540,36 660,80 800,50 L800,110 L0,110 Z" fill="var(--wave-1)" opacity="0.55"/>
    <path d="M0,76 C160,50 300,100 460,74 C600,52 700,92 800,70 L800,110 L0,110 Z" fill="var(--wave-2)" opacity="0.8"/>
    <path d="M0,92 C150,72 320,108 480,90 C620,74 720,102 800,88 L800,110 L0,110 Z" fill="var(--wave-3)"/>
  </svg>
</header>'''

FOOTER = f'''<div class="foot">
  <img class="foot-logo" src="{LOGO_URI}" alt="">
  <p class="foot-brand">Oniropetra's Snack Box</p>
  <p class="foot-place">Mikro | Pelion</p>
  <p class="foot-phone">Τηλ. Παραγγελιών: <b>6972182284</b></p>
  <div class="legal">
    <p>Οι τιμές περιλαμβάνουν όλους τους νόμιμους φόρους. Ο καταναλωτής δεν έχει την υποχρέωση να πληρώσει εάν δε λάβει το νόμιμο παραστατικό στοιχείο (απόδειξη-τιμολόγιο).</p>
    <p><i>Prices are inclusive of all taxes. The consumer is not obliged to pay if the notice of the payment has not been received (receipt-invoice).</i></p>
    <p>Αγορανομικός υπεύθυνος / Liable towards health authorities: Κουρτέσης Γεώργιος</p>
  </div>
  <div class="qr"><img src="{QR_URI}" alt=""><span>Δες το μενού online</span></div>
</div>'''

# ---------------- CSS ----------------
CSS = f'''
{FONTS}
:root {{
  --paper:#F7F5EF; --ink:#24384B; --muted:#4E657C; --faint:#6E8398;
  --sea:#56718A; --sand-deep:#B49A5C; --hairline:#DAE1E7; --sun:#E3CE97;
  --wave-1:#A8BCCC; --wave-2:#C7D4DE; --wave-3:#DCE5EC;
  --display:"GFS Didot","Palatino Linotype",Palatino,Georgia,serif;
  --body:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
}}
* {{ box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
@page {{ size:A4; margin:0; }}
html,body {{ margin:0; padding:0; background:#fff; color:var(--ink); font-family:var(--body); }}
.page {{ width:210mm; height:297mm; position:relative; overflow:hidden; background:var(--paper); page-break-after:always; }}
.page:last-child {{ page-break-after:auto; }}
.pad {{ padding:7mm 13mm 8mm; }}

/* header */
.cove {{ position:relative; overflow:hidden; background:linear-gradient(var(--wave-3),var(--paper)); text-align:center; padding:9mm 12mm 0; }}
.cove-sun {{ position:absolute; top:6mm; right:13%; width:21mm; height:21mm; border-radius:50%; background:var(--sun); opacity:.85; }}
.brand {{ position:relative; font-family:var(--display); font-weight:400; font-size:31pt; line-height:1; letter-spacing:.06em; margin:0; }}
.cove-waves {{ display:block; width:100%; height:10mm; margin-top:3mm; }}

/* sections & items */
section {{ margin-top:3.0mm; }}
section:first-child {{ margin-top:0; }}
.sh {{ display:flex; align-items:baseline; gap:3mm; border-bottom:1.5pt solid var(--ink); padding-bottom:.6mm; }}
.sh h2 {{ font-family:var(--display); font-weight:400; font-size:13.5pt; margin:0; letter-spacing:.01em; }}
.enl {{ margin-left:auto; font-size:6.2pt; font-weight:700; letter-spacing:.18em; text-transform:uppercase; color:var(--sand-deep); white-space:nowrap; }}
.items {{ list-style:none; margin:0; padding:0; }}
.it {{ padding:.6mm 0; border-bottom:.6pt solid var(--hairline); }}
.it:last-child {{ border-bottom:none; }}
.il {{ display:flex; align-items:baseline; gap:2mm; }}
.gr {{ font-weight:600; font-size:8.6pt; }}
.en {{ color:var(--faint); font-weight:400; font-size:8.6pt; }}
.en::before {{ content:" / "; }}
.pr {{ margin-left:auto; font-variant-numeric:tabular-nums; font-weight:650; font-size:9pt; white-space:nowrap; }}
.ds {{ margin:.35mm 0 0; font-size:6.9pt; line-height:1.24; color:var(--muted); font-style:italic; }}
.den {{ color:var(--faint); }}

/* two-column pages */
.cols {{ display:flex; gap:8mm; }}
.col {{ flex:1 1 0; min-width:0; }}

/* footer */
.p3pad {{ display:flex; flex-direction:column; height:100%; }}
.foot {{ margin-top:auto; text-align:center; position:relative; padding-top:7mm; border-top:1pt solid var(--hairline); }}
.foot-logo {{ width:20mm; height:20mm; border-radius:50%; object-fit:cover; display:block; margin:0 auto 3mm; }}
.foot-brand {{ font-family:var(--display); font-size:17pt; margin:0 0 1mm; color:var(--ink); }}
.foot-place {{ font-size:7pt; font-weight:700; letter-spacing:.28em; text-indent:.28em; text-transform:uppercase; color:var(--sea); margin:0 0 4mm; }}
.foot-phone {{ font-size:9pt; margin:0 0 4mm; color:var(--ink); }}
.legal {{ max-width:150mm; margin:0 auto; font-size:7pt; line-height:1.55; color:var(--muted); }}
.legal p {{ margin:1mm 0; }}
.qr {{ margin-top:5mm; display:flex; flex-direction:column; align-items:center; gap:1.5mm; }}
.qr img {{ width:22mm; height:22mm; }}
.qr span {{ font-size:7pt; color:var(--muted); }}
'''

# ---------------- ASSEMBLE ----------------
page1 = f'{HEADER}<div class="pad">{coffee}{refresh}{alcohol}</div>'
page2 = f'<div class="pad"><div class="cols"><div class="col">{breakfast}{barbites}</div><div class="col">{burgers}{pizzas}{salads}{mains}{pasta}</div></div></div>'
page3 = f'<div class="pad p3pad"><div class="cols"><div class="col">{dessert_l}</div><div class="col">{dessert_r}</div></div>{FOOTER}</div>'

DOC = f'''<!doctype html><html lang="el"><head><meta charset="utf-8"><title>Menu</title><style>{CSS}</style></head>
<body>
<div class="page">{page1}</div>
<div class="page">{page2}</div>
<div class="page">{page3}</div>
</body></html>'''

htmlpath = os.path.join(OUTDIR, "menu-print.html")
open(htmlpath, "w", encoding="utf-8").write(DOC)
print("wrote", htmlpath, len(DOC), "bytes")

# render via headless Chrome (CHROME_BIN lets CI point at its own Chromium)
chrome = os.environ.get("CHROME_BIN") or "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([chrome,"--headless","--no-sandbox","--disable-gpu","--disable-dev-shm-usage",
                "--no-pdf-header-footer",
                f"--print-to-pdf={PDF}", f"file://{htmlpath}"], check=True)
print("rendered", PDF)
