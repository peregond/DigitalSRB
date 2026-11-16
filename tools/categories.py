"""Thematic categories of the 60 ideas. The numbers stay as ids, the topic is what readers browse by."""

CATEGORIES = [
    {"id": "identity", "ideas": [2, 3, 5, 6, 7, 8, 18, 47],
     "sr": ("Identitet i eUprava", "Jedan nalog za ceo život, jednostavna prijava i aplikacija koja radi svuda."),
     "en": ("Identity and eUprava", "One account for life, simple login and an app that works everywhere.")},
    {"id": "counters", "ideas": [1, 9, 13, 24, 31],
     "sr": ("Šalteri i redovi", "Manje čekanja, pošteno zakazivanje i jasan status predmeta."),
     "en": ("Counters and queues", "Less waiting, fair booking and a clear status for every case.")},
    {"id": "documents", "ideas": [4, 30, 36, 46, 54, 55],
     "sr": ("Dokumenta i papiri", "Država ne traži papire koje već ima, a svaki dokument se proverava za sekundu."),
     "en": ("Documents and paperwork", "The state does not ask for papers it already has, and any document is checked in a second.")},
    {"id": "foreigners", "ideas": [11, 12, 14, 35, 37, 48, 49, 51],
     "sr": ("Stranci", "Jasna pravila, jasni rokovi i usluge na engleskom."),
     "en": ("Foreigners", "Clear rules, clear deadlines and services in English.")},
    {"id": "business", "ideas": [22, 25, 26, 27, 43, 44, 45],
     "sr": ("Porezi i biznis", "Otvaranje i zatvaranje firme za dan, jedan izveštaj i jednostavni porezi."),
     "en": ("Taxes and business", "Opening and closing a firm in a day, one report and simpler taxes.")},
    {"id": "payments", "ideas": [17, 23, 28, 29, 42],
     "sr": ("Plaćanja", "Računi i takse na jednom mestu, i za one bez domaće kartice."),
     "en": ("Payments", "Bills and fees in one place, also for people without a local card.")},
    {"id": "health", "ideas": [10, 33, 40, 41, 60],
     "sr": ("Zdravlje", "Jedna aplikacija, jedna lista čekanja i rezultati svuda."),
     "en": ("Health", "One app, one waiting list and results everywhere.")},
    {"id": "family", "ideas": [15, 16, 32, 38, 39, 56],
     "sr": ("Porodica i socijala", "Manje šaltera za život: vrtići, bolovanje, penzija, davanja i promena adrese."),
     "en": ("Family and benefits", "Fewer counters for life: kindergartens, sick leave, pensions, benefits and a change of address.")},
    {"id": "justice", "ideas": [34, 50, 52, 53, 57, 58],
     "sr": ("Pravosuđe i integritet", "Sudovi, javni beležnici i zapošljavanje bez „veze”."),
     "en": ("Justice and integrity", "Courts, notaries and hiring without “connections”.")},
    {"id": "transport", "ideas": [19, 20, 21, 59],
     "sr": ("Saobraćaj i pošta", "Karte, parking, vozila i pošta bez gužve."),
     "en": ("Transport and post", "Tickets, parking, vehicles and the post without the crush.")},
]

_ALL = sorted(i for c in CATEGORIES for i in c["ideas"])
assert _ALL == list(range(1, 61)), "every idea must be in exactly one category"


def cat_of(n):
    return next(c for c in CATEGORIES if n in c["ideas"])
