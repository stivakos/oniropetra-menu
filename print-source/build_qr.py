# -*- coding: utf-8 -*-
"""Παράγει το QR code που δείχνει στο ζωντανό online μενού.
Το ίδιο URL με το QR του footer στο PDF. Τρέξε: python print-source/build_qr.py"""

import os
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
URL = "https://stivakos.github.io/oniropetra-menu/"

qr = segno.make(URL, error="h")
png = os.path.join(ROOT, "Oniropetra_QR.png")
svg = os.path.join(ROOT, "Oniropetra_QR.svg")
qr.save(png, scale=12, border=2, dark="#24384B", light="#FFFFFF")
qr.save(svg, scale=12, border=2, dark="#24384B", light="#FFFFFF")
print("wrote", png)
print("wrote", svg)
