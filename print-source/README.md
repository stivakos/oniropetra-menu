# Μενού Ονειρόπετρα — πηγαίος κώδικας

## ⭐ Το μόνο αρχείο που πειράζεις: `menu.txt` (στη ρίζα του repo)

Όλα τα προϊόντα και οι τιμές ζουν στο **`menu.txt`**. Είναι απλό κείμενο:

```
## Καφές | Coffee
Espresso Μονό | Espresso | 2,00 €
Freddo Espresso |  | 3,00 €
Ομελέτα | Omelette | 7,50 € | 3 αυγά, σαλάτα | 3 eggs, salad
```

- **Κατηγορία:** γραμμή που ξεκινά με `## ` → `## Ελληνικό | English`
- **Προϊόν:** μία γραμμή, πεδία με `|` → `Ελληνικό | English | Τιμή | Περιγραφή GR | Περιγραφή EN`
- Πεδίο που δεν χρειάζεσαι → άφησέ το **κενό** ανάμεσα στα `|`
- **Διαγραφή:** σβήσε τη γραμμή. **Προσθήκη:** γράψε νέα γραμμή. **Αλλαγή τιμής:** άλλαξε τον αριθμό.

Από το `menu.txt` παράγονται **αυτόματα** και το online μενού (`index.html`) και το εκτυπώσιμο PDF.

## Αλλαγές από το κινητό (χωρίς υπολογιστή)

1. Άνοιξε το repo από την εφαρμογή **GitHub** (ή github.com) → άνοιξε το **`menu.txt`**.
2. Πάτα το μολύβι ✏️, κάνε την αλλαγή, **Commit**.
3. Το GitHub Action ξαναχτίζει μόνο του site + PDF. Σε ~1' το online ενημερώνεται· το νέο PDF βρίσκεται στη ρίζα του repo.

## Πώς δουλεύει (τα scripts)

- **`menu.txt`** → η πηγή αλήθειας.
- **`print-source/menu_data.py`** → διαβάζει το `menu.txt`.
- **`print-source/build_web.py`** → ξαναγράφει τα προϊόντα + τα chips πλοήγησης **μέσα** στο `index.html`
  (μόνο ανάμεσα στα markers `<!-- MENU:START/END -->` και `<!-- MENU:RAIL:START/END -->` — τίποτα άλλο δεν πειράζεται).
- **`print-source/build_print.py`** → φτιάχνει το `menu-print.html` και το κάνει render σε PDF μέσω headless Chrome.
- **`.github/workflows/build-pdf.yml`** → τρέχει τα δύο παραπάνω στο cloud σε κάθε αλλαγή του `menu.txt`.

## Τοπικό build (από Mac, προαιρετικό)

Μέσα στον φάκελο του repo:

```
python3 -m venv venv && ./venv/bin/pip install segno
./venv/bin/python print-source/build_web.py     # ενημερώνει το index.html
./venv/bin/python print-source/build_print.py   # ενημερώνει το PDF
```

## Σημειώσεις

- Το layout του PDF είναι σφιχτά ρυθμισμένο για 3 σελίδες A4. Αν προσθέσεις πολλά προϊόντα, ίσως χρειαστεί
  μικρο-ρύθμιση στα μεγέθη/κενά (στο `CSS` του `build_print.py`).
- Χωρίς παύλες/leaders στο PDF — όπως ζητήθηκε.
- Το footer QR δείχνει στο ζωντανό online μενού: https://stivakos.github.io/oniropetra-menu/
- Το `build_print.py` διαβάζει τις γραμματοσειρές GFS Didot από το `index.html`, και το λογότυπο από `assets/logo_round.png`.
