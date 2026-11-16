"""Thematic categories of the 59 ideas. The numbers stay as ids, the topic is what readers browse by."""

CATEGORIES = [
    {"id": "identity", "ideas": [2, 3, 5, 6, 7, 8, 18, 36, 47],
     "sr": ("Identitet i eUprava", "Jedan nalog za ceo život, jednostavna prijava i aplikacija koja radi svuda."),
     "en": ("Identity and eUprava", "One account for life, simple login and an app that works everywhere.")},
    {"id": "counters", "ideas": [1, 13, 24],
     "sr": ("Šalteri i transparentnost", "Manje čekanja, jasan status i javni podaci o kvalitetu usluga."),
     "en": ("Counters and transparency", "Less waiting, a clear status and public data on service quality.")},
    {"id": "documents", "ideas": [4, 30, 34, 46, 54, 55],
     "sr": ("Dokumenta i papiri", "Država ne traži papire koje već ima, a svaki dokument se proverava za sekundu."),
     "en": ("Documents and paperwork", "The state does not ask for papers it already has, and any document is checked in a second.")},
    {"id": "foreigners", "ideas": [11, 12, 14, 35, 37, 48, 49, 51, 53],
     "sr": ("Stranci", "Jasna pravila, jasni rokovi i usluge na engleskom."),
     "en": ("Foreigners", "Clear rules, clear deadlines and services in English.")},
    {"id": "business", "ideas": [9, 22, 26, 27, 43, 44],
     "sr": ("Porezi i biznis", "Jedan portal, firma za dan, jedan izveštaj i jednostavni porezi."),
     "en": ("Taxes and business", "One portal, a firm in a day, one report and simpler taxes.")},
    {"id": "payments", "ideas": [17, 23, 28, 29, 42],
     "sr": ("Plaćanja", "Računi i takse na jednom mestu, i za one bez domaće kartice."),
     "en": ("Payments", "Bills and fees in one place, also for people without a local card.")},
    {"id": "health", "ideas": [10, 33, 40, 41, 60],
     "sr": ("Zdravlje", "Jedna aplikacija, jedna lista čekanja i rezultati svuda."),
     "en": ("Health", "One app, one waiting list and results everywhere.")},
    {"id": "family", "ideas": [15, 16, 32, 38, 39],
     "sr": ("Porodica i socijala", "Vrtići, bolovanje, penzije i davanja bez šaltera."),
     "en": ("Family and benefits", "Kindergartens, sick leave, pensions and benefits without counters.")},
    {"id": "home", "ideas": [31, 45, 56, 57],
     "sr": ("Dom i nekretnine", "Katastar, priključci, promena adrese i nasleđe bez višemesečnog čekanja."),
     "en": ("Home and property", "The cadastre, utility connections, a change of address and inheritance without months of waiting.")},
    {"id": "justice", "ideas": [50, 52, 58],
     "sr": ("Beležnici i pravo", "Overe, punomoćja i legalno ubrzanje dokumenata."),
     "en": ("Notaries and legal", "Certifications, powers of attorney and a legal fast track for documents.")},
    {"id": "transport", "ideas": [19, 20, 59],
     "sr": ("Saobraćaj", "Karte, parking i vozila bez gužve i bez papirnih nalepnica."),
     "en": ("Transport", "Tickets, parking and vehicles without the crush and without paper stickers.")},
    {"id": "post", "ideas": [21],
     "sr": ("Pošta i carina", "Pošta Srbije kao normalna aplikacija, paket jednim QR kodom i carinjenje za jedan dan."),
     "en": ("Post and customs", "Pošta Srbije as a proper app, a parcel with one QR code and customs clearance in a day.")},
]

_ALL = sorted(i for c in CATEGORIES for i in c["ideas"])
REMOVED = {25}  # merged into idea 9; the other numbers stay as they are so votes keep their ideas
assert _ALL == [i for i in range(1, 61) if i not in REMOVED], "every idea must be in exactly one category"


def cat_of(n):
    return next(c for c in CATEGORIES if n in c["ideas"])


# line icons (24x24, stroke) for the topic tiles on the home page
ICONS = {
    "identity": "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10zM9 12l2 2 4-4",
    "counters": "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 6v6l4 2",
    "documents": "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M8 13h8M8 17h6",
    "foreigners": "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20",
    "business": "M3 7h18v13H3zM8 7V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v3M3 13h18",
    "payments": "M2 6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2zM2 10h20",
    "health": "M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z",
    "family": "M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8",
    "home": "M3 11l9-8 9 8v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z",
    "justice": "M12 3v18M5 21h14M5 7h14M5 7l-3 8a3.5 3.5 0 0 0 6 0zM19 7l-3 8a3.5 3.5 0 0 0 6 0z",
    "transport": "M5 16V6a3 3 0 0 1 3-3h8a3 3 0 0 1 3 3v10zM5 16v3h3v-3M16 16v3h3v-3M5 11h14M8 13.5h.01M16 13.5h.01",
    "post": "M3 5h18v14H3zM3 7l9 7 9-7",
}
assert all(c["id"] in ICONS for c in CATEGORIES), [c["id"] for c in CATEGORIES if c["id"] not in ICONS]
