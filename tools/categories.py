"""Thematic categories of the 60 ideas. The numbers stay as ids, the topic is what readers browse by."""

CATEGORIES = [
    {"id": "identity", "ideas": [2, 3, 5, 6, 7, 8, 18, 36, 47],
     "sr": ("Identitet i eUprava", "Jedan nalog za ceo život, jednostavna prijava i aplikacija koja radi svuda."),
     "en": ("Identity and eUprava", "One account for life, simple login and an app that works everywhere.")},
    {"id": "counters", "ideas": [1, 9, 13, 24],
     "sr": ("Šalteri i transparentnost", "Manje čekanja, pošteno zakazivanje, jasan status i javni podaci o kvalitetu usluga."),
     "en": ("Counters and transparency", "Less waiting, fair booking, a clear status and public data on service quality.")},
    {"id": "documents", "ideas": [4, 30, 34, 46, 54, 55],
     "sr": ("Dokumenta i papiri", "Država ne traži papire koje već ima, a svaki dokument se proverava za sekundu."),
     "en": ("Documents and paperwork", "The state does not ask for papers it already has, and any document is checked in a second.")},
    {"id": "foreigners", "ideas": [11, 12, 14, 35, 37, 48, 49, 51, 53],
     "sr": ("Stranci", "Jasna pravila, jasni rokovi i usluge na engleskom."),
     "en": ("Foreigners", "Clear rules, clear deadlines and services in English.")},
    {"id": "business", "ideas": [22, 25, 26, 27, 43, 44],
     "sr": ("Porezi i biznis", "Otvaranje i zatvaranje firme za dan, jedan izveštaj i jednostavni porezi."),
     "en": ("Taxes and business", "Opening and closing a firm in a day, one report and simpler taxes.")},
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
assert _ALL == list(range(1, 61)), "every idea must be in exactly one category"


def cat_of(n):
    return next(c for c in CATEGORIES if n in c["ideas"])
