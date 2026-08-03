# -*- coding: utf-8 -*-
"""Διαβάζει το menu.txt (το αρχείο-πηγή) και το επιστρέφει ως δομημένα δεδομένα.
Το χρησιμοποιούν και το build_web.py (online μενού) και το build_print.py (PDF),
ώστε να υπάρχει ΜΙΑ πηγή αλήθειας."""

import os


def _has_greek(s):
    return any('Ͱ' <= c <= 'Ͽ' or 'ἀ' <= c <= '῿' for c in s)


def _split(line, n):
    parts = [p.strip() for p in line.split("|")]
    parts += [""] * (n - len(parts))
    return parts[:n]


def load_menu(path):
    """Επιστρέφει λίστα κατηγοριών. Κάθε κατηγορία:
        {"gr":..., "en":..., "latin":bool, "items":[{gr,en,price,dgr,den}, ...]}"""
    cats = []
    cur = None
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if not line.strip():
                continue
            if line.startswith("##"):
                gr, en = _split(line[2:].strip(), 2)
                cur = {"gr": gr, "en": en, "latin": not _has_greek(gr), "items": []}
                cats.append(cur)
            elif line.lstrip().startswith("#"):
                continue  # σχόλιο
            else:
                if cur is None:
                    continue
                gr, en, price, dgr, den = _split(line, 5)
                cur["items"].append({"gr": gr, "en": en, "price": price, "dgr": dgr, "den": den})
    return cats


# Σταθερά slugs για τις υπάρχουσες κατηγορίες (κρατούν τα ίδια #anchors στο site).
SLUGS = {
    "Καφές": "kafes", "Ροφήματα": "rofimata", "Ποτά": "pota", "Πρωινό": "proino",
    "Σνακ": "snack", "Burgers": "burgers", "Πίτσες": "pitses", "Σαλάτες": "salates",
    "Μερίδες Φαγητού": "merides", "Μακαρονάδες": "makaronades", "Γλυκά": "glyka",
}

_TRANS = {
    "α": "a", "β": "v", "γ": "g", "δ": "d", "ε": "e", "ζ": "z", "η": "i", "θ": "th",
    "ι": "i", "κ": "k", "λ": "l", "μ": "m", "ν": "n", "ξ": "x", "ο": "o", "π": "p",
    "ρ": "r", "σ": "s", "ς": "s", "τ": "t", "υ": "y", "φ": "f", "χ": "ch", "ψ": "ps",
    "ω": "o", "ά": "a", "έ": "e", "ή": "i", "ί": "i", "ό": "o", "ύ": "y", "ώ": "o",
    "ϊ": "i", "ϋ": "y", "ΐ": "i", "ΰ": "y", " ": "-",
}


def slug_for(gr):
    """Slug για μια κατηγορία: σταθερό για τις γνωστές, αλλιώς greeklish."""
    if gr in SLUGS:
        return SLUGS[gr]
    out = "".join(_TRANS.get(c, c) for c in gr.lower())
    out = "".join(c for c in out if c.isalnum() or c == "-")
    return out.strip("-") or "cat"
