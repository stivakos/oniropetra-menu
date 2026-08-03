# -*- coding: utf-8 -*-
"""Ξαναχτίζει τα προϊόντα και το μενού πλοήγησης (chips) μέσα στο index.html,
από το menu.txt. Αγγίζει ΜΟΝΟ τις περιοχές ανάμεσα στα markers — τίποτα άλλο
(header, styles, footer, scripts) δεν πειράζεται."""

import os, re, html as H
from menu_data import load_menu, slug_for

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
MENU = os.path.join(ROOT, "menu.txt")
INDEX = os.path.join(ROOT, "index.html")


def esc(s):
    return H.escape(s, quote=False)


def web_item(it):
    gr, en, price, dgr, den = it["gr"], it["en"], it["price"], it["dgr"], it["den"]
    name = f'<span class="gr">{esc(gr)} <span class="en">{esc(en)}</span></span>' if en \
        else f'<span class="gr">{esc(gr)}</span>'
    line = f'<div class="item-line">{name}<span class="dots"></span><span class="price">{esc(price)}</span></div>'
    if dgr and den:
        desc = f'\n        <p class="desc" lang="el">{esc(dgr)} <span class="desc-en" lang="en">— {esc(den)}</span></p>'
    elif den:
        desc = f'\n        <p class="desc" lang="en">{esc(den)}</p>'
    elif dgr:
        desc = f'\n        <p class="desc" lang="el">{esc(dgr)}</p>'
    else:
        desc = ""
    if desc:
        return f'      <li class="item">\n        {line}{desc}\n      </li>'
    return f'      <li class="item">{line}</li>'


def web_section(cat):
    gr, en, latin = cat["gr"], cat["en"], cat["latin"]
    slug = slug_for(gr)
    items = "\n".join(web_item(it) for it in cat["items"])
    if latin:
        h2 = f'<h2 id="h-{slug}">{esc(gr)}' + (f' / {esc(en)}' if en else '') + '</h2>'
        head = f'    <div class="sec-head">\n      {h2}\n    </div>'
    else:
        head = f'    <div class="sec-head">\n      <h2 id="h-{slug}" lang="el">{esc(gr)}</h2>'
        if en:
            head += f'\n      <span class="en-label">{esc(en)}</span>'
        head += '\n    </div>'
    return (f'  <section id="{slug}" aria-labelledby="h-{slug}">\n{head}\n'
            f'    <ul class="items">\n{items}\n    </ul>\n  </section>')


def web_chip(cat):
    gr, en, latin = cat["gr"], cat["en"], cat["latin"]
    slug = slug_for(gr)
    if en and not latin:
        return f'    <a class="chip" href="#{slug}">{esc(gr)}<span class="chip-en">{esc(en)}</span></a>'
    return f'    <a class="chip" href="#{slug}">{esc(gr)}</a>'


def replace_region(text, start, end, inner):
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    new = start + "\n" + inner + "\n" + end
    out, n = pat.subn(lambda m: new, text, count=1)
    if n != 1:
        raise SystemExit(f"Δεν βρέθηκαν τα markers: {start} … {end}")
    return out


def main():
    cats = load_menu(MENU)
    html = open(INDEX, encoding="utf-8").read()
    chips = "\n".join(web_chip(c) for c in cats)
    sections = "\n\n".join(web_section(c) for c in cats)
    html = replace_region(html, "<!-- MENU:RAIL:START -->", "<!-- MENU:RAIL:END -->", chips)
    html = replace_region(html, "<!-- MENU:START -->", "<!-- MENU:END -->", sections)
    open(INDEX, "w", encoding="utf-8").write(html)
    print(f"updated {INDEX}: {len(cats)} categories, {sum(len(c['items']) for c in cats)} items")


if __name__ == "__main__":
    main()
