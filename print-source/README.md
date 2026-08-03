# Εκτυπώσιμος κατάλογος — πηγαίος κώδικας

Εδώ ζει το **πηγαίο** του εκτυπώσιμου καταλόγου (το A4 PDF). Πριν, το πηγαίο είχε χαθεί
και υπήρχε μόνο το τελικό PDF· τώρα φυλάσσεται εδώ ώστε να μπορεί να ξαναφτιαχτεί/επεξεργαστεί.

## Αρχεία
- **`menu-print.html`** — Το πλήρες, αυτοτελές HTML του καταλόγου (γραμματοσειρές, λογότυπο και QR
  ενσωματωμένα ως data URIs). Αυτό είναι που γίνεται render σε PDF. Μπορείς να το ανοίξεις και σε browser.
- **`build_print.py`** — Script που παράγει το `menu-print.html` (περιεχόμενο ως δομημένα δεδομένα)
  και μετά το κάνει render σε PDF μέσω headless Chrome.
- **`assets/logo_round.png`** — Το στρογγυλό λογότυπο για το footer.

## Πώς αλλάζω τιμή / προσθέτω προϊόν

Δύο τρόποι:

**Α) Γρήγορα, με το χέρι** — άνοιξε το `menu-print.html`, βρες το προϊόν, άλλαξε τιμή/κείμενο,
και ξανακάνε render (εντολή πιο κάτω).

**Β) Καθαρά, με το script** — επεξεργάσου το `build_print.py` (το περιεχόμενο είναι λίστες `item(...)`
ανά ενότητα) και τρέξε το· ξαναγράφει το HTML και το PDF μαζί.

## Αλλαγές από το κινητό (χωρίς υπολογιστή)

Αυτό το repo έχει GitHub Action (`.github/workflows/build-pdf.yml`) που **ξαναφτιάχνει
μόνο του το PDF στο cloud** κάθε φορά που αλλάζει το μενού. Ροή από κινητό:

1. Άνοιξε το repo από την εφαρμογή **GitHub** (ή github.com).
2. Άλλαξε το `index.html` (online μενού) ή/και το `print-source/build_print.py` (τιμές/προϊόντα).
3. Κάνε **commit** στο `master`.
4. Το online μενού ενημερώνεται μέσω GitHub Pages (~1'). Το Action τρέχει, φτιάχνει ξανά το
   `MENU_Mikro_Pelion_NEOS_KATALOGOS.pdf` και το κάνει commit πίσω στο repo — κατέβασέ το από εκεί για εκτύπωση.

> Το ενημερωμένο PDF βρίσκεται πάντα στη ρίζα του repo. Ο υπολογιστής δεν χρειάζεται πια για το render.

## Render σε PDF (headless Chrome)

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="../MENU_Mikro_Pelion_NEOS_KATALOGOS.pdf" \
  "menu-print.html"
```

## Σημειώσεις
- Το layout είναι σφιχτά ρυθμισμένο για να χωράει σε 3 σελίδες A4. Αν προσθέσεις πολλά νέα προϊόντα,
  ίσως χρειαστεί μικρο-ρύθμιση στα μεγέθη/κενά (τιμές στο `CSS` του `build_print.py`).
- Χωρίς παύλες/leaders — όπως ζητήθηκε.
- Το footer QR δείχνει στο ζωντανό online μενού: https://stivakos.github.io/oniropetra-menu/
- Το `build_print.py` διαβάζει τις γραμματοσειρές GFS Didot από `/Users/stavros/oniropetra-menu/index.html`.
  Το `menu-print.html` όμως τις έχει ήδη μέσα του, οπότε για απλό render δεν χρειάζεται τίποτα άλλο.
- Το `build_print.py` χρειάζεται το πακέτο **segno** (για το QR). Αν λείπει:
  `python3 -m venv venv && ./venv/bin/pip install segno && ./venv/bin/python build_print.py`.
  Το λογότυπο του footer διαβάζεται από `assets/logo_round.png` (μέσα στον ίδιο φάκελο).
