"""Content of the detail pages for the eight main ideas.

Every visible string is a pair (Serbian, English). The numbers (cases, fees, days, databases)
come from the sources already cited in source/print.html. The step-by-step flows, FAQ answers
and "what has to change" lists are drafts that explain how the idea could work: review them.
"""

# idea number -> (slug, theme colour, darker shade)
THEMES = {
    9: ("tax-portal", "#7CA10A", "#4A6206"),
    1: ("qr-counter", "#12A150", "#0A6B36"),
    2: ("two-levels", "#0A9AAE", "#06626F"),
    22: ("business-in-a-day", "#1F6FEB", "#123F96"),
    30: ("no-papers", "#E08A00", "#8F5300"),
    21: ("posta-reform", "#F1BD40", "#1D3F72"),
    47: ("wallet-id", "#6A45F0", "#3A1FA8"),
    48: ("no-registration", "#E30613", "#8F040D"),
    50: ("fast-track", "#D1246A", "#85103F"),
    53: ("driving-licence", "#24407A", "#0F2147"),
}
ORDER = [9, 1, 2, 22, 30, 21, 47, 48, 50, 53]


def text(eb, t, p, id=None):
    return {"k": "text", "eb": eb, "t": t, "p": p, "id": id}


def cards(eb, t, items, id=None, intro=None, extra=None):
    return {"k": "cards", "eb": eb, "t": t, "items": items, "id": id, "intro": intro, "extra": extra}


def flow(eb, t, today, after, note=None, id=None, intro=None, extra=None):
    return {"k": "flow", "eb": eb, "t": t, "today": today, "after": after, "note": note, "id": id, "intro": intro, "extra": extra}


def steps(eb, t, items, id=None, intro=None, extra=None):
    return {"k": "steps", "eb": eb, "t": t, "items": items, "id": id, "intro": intro, "extra": extra}


def bars(eb, t, rows, note=None, id=None, intro=None, unit="", extra=None):
    return {"k": "bars", "eb": eb, "t": t, "rows": rows, "note": note, "id": id, "intro": intro, "unit": unit, "extra": extra}


def table(eb, t, head, rows, hl=None, id=None, intro=None):
    return {"k": "table", "eb": eb, "t": t, "head": head, "rows": rows, "hl": hl, "id": id, "intro": intro}


def check(eb, t, items, id=None, intro=None):
    return {"k": "check", "eb": eb, "t": t, "items": items, "id": id, "intro": intro}


def faq(eb, t, items, id=None):
    return {"k": "faq", "eb": eb, "t": t, "items": items, "id": id}


def custom(name, eb, t, intro=None, id=None):
    return {"k": "custom", "name": name, "eb": eb, "t": t, "intro": intro, "id": id}


PROBLEM = ("Problem", "The problem")
TODAY = ("Danas", "Today")
PROPOSAL = ("Predlog", "The proposal")
HOW = ("Kako radi", "How it works")
WHO = ("Za koga", "Who benefits")
CHANGE = ("Šta treba promeniti", "What has to change")
QA = ("Pitanja i odgovori", "Questions and answers")
NUMBERS = ("Brojke", "In numbers")

L_LAW = ("Zakon", "Law")
L_TECH = ("Tehnika", "Technology")
L_ORG = ("Organizacija", "Organisation")

PAGES = {}

# ---------------------------------------------------------------- 01 QR at every counter
PAGES[1] = {
    "stats": [],
    "related": [2, 6, 24, 30],
    "blocks": [
        {**custom("stages1", ("Pregled", "Overview"), ("Kako radi jedan QR kod", "How one QR code works"),
                  intro=("Na šalteru u MUP-u, APR-u ili opštini danas moraš sam da objasniš šta ti treba, a službenik pogađa postupak, traži papire i ručno kuca podatke. Sa QR kodom predmeta sve to nestaje.",
                         "At a MUP, APR or opština counter today you have to explain what you need, and the clerk guesses the procedure, asks for papers and types the data by hand. With a case QR code all of that goes away.")),
         "cls": "compact", "nav": ("Pregled", "Overview")},
        {**custom("versus1", ("Razlika", "The difference"), ("Na šalteru", "At the counter")), "nav": ("Razlika", "Difference")},
        {**flow(("Put do rešenja", "The path"), ("Isti šalter, dva puta", "The same counter, two ways"), [
            ("Čekaš u redu", "Wait in line"), ("Objašnjavaš šta ti treba", "Explain what you need"),
            ("Službenik pogađa postupak", "Clerk guesses the procedure"), ("Predaješ papire", "Hand over papers"),
            ("Službenik kuca podatke", "Clerk types the data"), ("Odgovor ili povratak sutra", "An answer, or come back tomorrow")],
            [("Otvaraš predmet u eUpravi", "Open the case in eUprava"), ("Pokazuješ QR kod", "Show your QR code"),
             ("Službenik skenira, predmet se otvara", "Clerk scans, the case opens"),
             ("Samo konkretna dodatna pitanja", "Only specific follow-up questions"), ("Odmah vidiš sledeći korak", "The next step is clear at once")],
            note=("Ilustrativan tok, koraci se razlikuju od službe do službe.", "Illustrative path; the steps differ from office to office."), id="c1", extra="qr_pair"),
         "nav": ("Šalter", "Counter")},
        {**cards(WHO, ("Dobiti mogu svi", "Everyone gains"), [
            ("Građani", "Citizens", "Ništa ne objašnjavaš, manje papira i manje odlazaka.", "Nothing to explain, fewer papers and fewer trips."),
            ("Stranci", "Foreigners", "Isti tok na engleskom, bez potrebe da znaš lokalni žargon.", "The same flow in English, without needing to know the local jargon."),
            ("Službenici", "Clerks", "Jedan standardan ekran, manje kucanja i manje sporova.", "One standard screen, less typing and fewer disputes."),
            ("Država", "The state", "Manje grešaka, jasan trag svakog koraka i manje prostora za „vezu”.", "Fewer errors, a clear trace of every step and less room for “connections”."),
        ]), "nav": ("Ko dobija", "Who gains")},
        {**faq(QA, ("Šta ako…", "What if…"), [
            (("Nemam pametan telefon?", "I have no smartphone?"), ("Kod može da se odštampa ili stigne kao link u SMS-u. Šalter ostaje otvoren i za one koji dođu bez ičega, samo sa dužim postupkom.", "The code can be printed or arrive as an SMS link. The counter stays open for people who arrive with nothing, just with a longer procedure.")),
            (("Je li bezbedno pokazati QR kod?", "Is it safe to show a QR code?"), ("QR sadrži samo nasumičnu oznaku predmeta. Službenik mora da bude prijavljen, a svaki pristup tvom predmetu beleži se i vidljiv ti je u aplikaciji.", "The QR holds only a random case reference. The clerk must be logged in, and every access to your case is logged and visible to you in the app.")),
            (("Sistem ne radi?", "The system is down?"), ("Postupak se vraća na današnji, papirni. QR ne uvodi novu zavisnost, samo skraćuje put.", "The procedure falls back to today's paper one. The QR adds no new dependency, it only shortens the path.")),
        ]), "nav": ("Pitanja", "Q&A")},
    ],
}

# ---------------------------------------------------------------- 09 one tax portal
PAGES[9] = {
    "stats": [],
    "related": [22, 26, 44, 17],
    "blocks": [
        {**custom("stages9", ("Pregled", "Overview"), ("Jedan portal umesto dva", "One portal instead of two"),
                  intro=("Danas firmu registruješ u jednom elektronskom sistemu, a poreze plaćaš u drugom, pa moraš da prelaziš sa portala na portal. Predlog je jedinstveni poreski portal u kome je sve to na jednom mestu.",
                         "Today you register a business in one electronic system and pay taxes in another, so you have to switch from portal to portal. The proposal is a single tax portal where it is all in one place.")),
         "cls": "compact", "nav": ("Pregled", "Overview")},
        {**custom("portal9", ("Kako izgleda", "What it looks like"), ("Jedan portal, jedan pogled", "One portal, one view"),
                  intro=("Danas ePorezi nudi tri načina prijave i programe za preuzimanje, a APR ima poseban portal sa svojim uslugama. Jedinstveni portal sve to prikazuje na jednom ekranu, na jednom nalogu.",
                         "Today ePorezi offers three ways to sign in and programs to download, and APR has its own portal with its own services. The single portal shows it all on one screen, on one account."), id="mock"),
         "nav": ("Izgled", "Layout")},
        {**flow(("Put", "The path"), ("Registracija i porezi", "Registration and taxes"), [
            ("Registruješ firmu na portalu APR-a", "You register the business on the APR portal"),
            ("Prelaziš na portal ePorezi", "You switch to the ePorezi portal"),
            ("Tamo prijavljuješ i plaćaš poreze", "There you file and pay taxes"),
            ("Status pratiš u dva sistema", "You follow the status in two systems")],
            [("Prijaviš se jednom na jedinstveni portal", "You sign in once to the single portal"),
             ("Registruješ firmu", "You register the business"),
             ("Plaćaš poreze u istom portalu", "You pay taxes in the same portal"),
             ("Jedan pregled obaveza i statusa", "One view of obligations and status")],
            note=("Ilustrativan tok, tačni koraci zavise od konkretne usluge.", "An illustrative path; the exact steps depend on the service."), id="c1", extra="t9_pair"),
         "nav": ("Portal", "The portal")},
        {**cards(("Ko šta radi", "Who does what"), ("Ustanove ostaju nezavisne", "The agencies stay independent"), [
            ("APR", "APR", "Registracija i izmene podataka, kao i do sada. Usluge su dostupne u jedinstvenom portalu.", "Registration and changes of data, as before. The services are available in the single portal."),
            ("Poreska uprava", "Poreska uprava", "Porezi, prijave i plaćanja, kao i do sada. Usluge su dostupne u jedinstvenom portalu.", "Taxes, filings and payments, as before. The services are available in the single portal."),
            ("Jedinstveni portal", "The single portal", "Jedna prijava i jedan pregled. Objedinjuju se samo elektronske usluge, ne ustanove.", "One sign-in and one view. Only the electronic services are brought together, not the agencies."),
        ], intro=("Svaka ustanova i dalje odlučuje o svojim podacima i postupcima.", "Each agency still decides on its own data and procedures.")),
         "nav": ("Ustanove", "Agencies")},
        {**faq(QA, ("Šta ako…", "What if…"), [
            (("Da li se APR i Poreska uprava spajaju?", "Are APR and Poreska uprava merged?"), ("Ne. Ustanove ostaju nezavisne. Spajaju se samo njihove elektronske usluge, na jednom portalu.", "No. The agencies stay independent. Only their electronic services are brought together, on one portal.")),
            (("Ko odgovara za podatke?", "Who is responsible for the data?"), ("Svaka ustanova za svoje podatke i odluke, kao i danas. Portal ih samo prikazuje na jednom mestu.", "Each agency for its own data and decisions, as today. The portal only shows them in one place.")),
        ]), "nav": ("Pitanja", "Q&A")},
    ],
}

# ---------------------------------------------------------------- 02 two eUprava levels
PAGES[2] = {
    "stats": [],
    "related": [3, 5, 6, 47],
    "blocks": [
        {**custom("stages2", ("Pregled", "Overview"), ("Dva nivoa umesto tri", "Two levels instead of three"),
                  intro=("Već postoji: eID ima tri načina prijave, lozinku, aplikaciju ConsentID i kvalifikovani sertifikat (čip lična karta ili oblak sertifikat). Za viši nivo aktivacioni kod se podiže na šalteru ili preko sertifikata, a tri nivoa zbunjuju ljude.",
                         "Already exists: eID has three ways to log in, a password, the ConsentID app and a qualified certificate (chip ID card or cloud certificate). For the higher level the activation code is collected at a counter or via a certificate, and three levels confuse people.")),
         "cls": "compact", "nav": ("Pregled", "Overview")},
        {**custom("versus2", ("Razlika", "The difference"), ("Koliko nivoa moraš da razumeš", "How many levels you have to understand")), "nav": ("Razlika", "Difference")},
        {**flow(("Put do punog naloga", "The path to a full account"), ("Od zbunjenosti do dva jasna nivoa", "From confusion to two clear levels"), [
            ("Biraš između lozinke, ConsentID i sertifikata", "Choose between a password, ConsentID and a certificate"),
            ("Ne znaš koji nivo ti treba", "You do not know which level you need"),
            ("Za viši nivo ideš na šalter po aktivacioni kod", "For the higher level you go to a counter for an activation code"),
            ("Tek tada koristiš sve usluge", "Only then can you use every service")],
            [("Osnovni nivo: e-pošta i snimak dokumenta", "Basic: an email and a scan of a document"),
             ("Odmah koristiš osnovne usluge", "You use the basic services at once"),
             ("Puni nivo: potvrda preko banke, čip lične karte ili pošte", "Full: confirm through a bank, a chip ID card or the pošta"),
             ("Bez dolaska na šalter, po eIDAS standardu", "With no counter visit, under the eIDAS standard")],
            note=("Stranci dobijaju osnovni pristup odmah, a puni sa boravkom.", "Foreigners get basic access at once and full access with residence."), id="c1", extra="l2_pair"),
         "nav": ("Nivoi", "Levels")},
        {**faq(QA, ("Šta ako…", "What if…"), [
            (("Nemam račun u banci?", "I do not have a bank account?"), ("Identitet možeš da potvrdiš i čip ličnom kartom ili preko pošte. Banka je samo jedna od tri mogućnosti.", "You can also confirm your identity with a chip ID card or through the pošta. The bank is just one of three options.")),
            (("Šta je sa strancima?", "What about foreigners?"), ("Dobijaju osnovni pristup odmah, a puni čim dobiju boravak.", "They get basic access at once and full access once they have residence.")),
        ]), "nav": ("Pitanja", "Q&A")},
    ],
}

# ---------------------------------------------------------------- 22 business in one day
PAGES[22] = {
    "stats": [],
    "related": [17, 23, 26, 44],
    "blocks": [
        {**custom("stages22", ("Pregled", "Overview"), ("Zatvaranje firme u četiri koraka", "Closing a business in four steps"),
                  intro=("Elektronska registracija preduzetnika već postoji, a od decembra 2023. i onlajn prijava brisanja preko portala APR-a. Problem je što konačan obračun poreza često stigne tek 2–3 meseca posle odjave.",
                         "Electronic registration of a preduzetnik (sole trader) already exists, and since December 2023 so does an online deregistration request on the APR portal. The problem is that the final tax assessment often arrives only 2–3 months after deregistration.")),
         "cls": "compact", "nav": ("Pregled", "Overview")},
        {**custom("versus22", ("Razlika", "The difference"), ("Kada saznaš koliko duguješ", "When you learn what you owe")), "nav": ("Razlika", "Difference")},
        {**flow(("Zatvaranje", "Closing"), ("Šta se menja pri zatvaranju", "What changes when you close"), [
            ("Podneseš onlajn zahtev za brisanje", "You file an online deregistration request"),
            ("Firma je obrisana, a ne znaš koliko duguješ", "The business is deleted, but you do not know what you owe"),
            ("Posle 2–3 meseca stiže rešenje o konačnom porezu", "After 2–3 months a decision with the final tax arrives"),
            ("Tek tada plaćaš", "Only then do you pay")],
            [("Podneseš zahtev onlajn", "You file the request online"),
             ("Poreska odmah računa konačan porez", "Poreska calculates the final tax at once"),
             ("Vidiš iznos i plaćaš istog dana", "You see the amount and pay the same day"),
             ("Firma je zatvorena", "The business is closed")],
            id="c1", extra="biz_c1"), "nav": ("Zatvaranje", "Closing")},
        {**flow(("Veće firme", "Larger firms"), ("Kada nedostaje mesečni izveštaj", "When a monthly report is missing"), [
            ("Zatvaranje čeka izveštaj", "Closing waits for the report"), ("Izveštaj se podnosi", "The report is filed"), ("Posle meseci stiže rešenje", "A decision arrives months later")],
            [("Plaćaš obračunato sada", "Pay what is calculated now"), ("Firma se zatvara", "The business closes"), ("Razliku doplaćuješ posle izveštaja", "Top up the difference after the report")],
            note=("Država ne gubi pravo na razliku, a firma ne čeka mesecima.", "The state keeps its right to the difference, and the firm does not wait for months."), id="lf"),
         "nav": ("Veće firme", "Larger firms")},
        {**custom("countries22", ("Primeri iz sveta", "Examples abroad"), ("Kako to rade drugi", "How others do it"), id="cn"), "nav": ("Svet", "Abroad")},
        {**faq(QA, ("Šta ako…", "What if…"), [
            (("Firma ima nepodmirene obaveze?", "The firm has unpaid obligations?"), ("Konačan obračun ih pokazuje odmah, pa nema iznenađenja posle zatvaranja. Plaćanje ide u istom koraku.", "The final assessment shows them at once, so there is no surprise after closing. Payment happens in the same step.")),
            (("Može li država da tako obračuna sve?", "Can the state calculate it all that fast?"), ("Sve što je prijavljeno već je u njenim evidencijama. Ono što fali, na primer izveštaj, rešava se doplatom razlike.", "Everything reported is already in its records. What is missing, such as a report, is handled by topping up the difference.")),
            (("Zašto ne ostati kod današnjeg?", "Why not keep today's way?"), ("Jer neizvesnost nekoliko meseci posle zatvaranja košta ljude i vreme i nervozu, a država ionako ima podatke.", "Because months of uncertainty after closing cost people time and stress, and the state has the data anyway.")),
        ]), "nav": ("Pitanja", "Q&A")},
    ],
}

# ---------------------------------------------------------------- 30 never ask for papers
PAGES[30] = {
    "stats": [],
    "related": [4, 31, 32, 44],
    "blocks": [
        {**custom("stages30", ("Pregled", "Overview"), ("Četiri pravila", "Four rules"),
                  intro=("Od 2016. Zakon o opštem upravnom postupku (čl. 9 i 103) obavezuje službe da same pribave podatke iz službenih evidencija, a eZUP povezuje 18 baza osam institucija. Pravilo se ne poštuje svuda i mnogi registri nisu u eZUP-u, pa građani i dalje nose uverenja.",
                         "Since 2016 the Law on General Administrative Procedure (ZUP, Arts. 9 and 103) obliges offices to obtain data themselves from official records, and eZUP links 18 databases of eight institutions. The rule is not followed everywhere and many registers are not in eZUP, so people still carry certificates.")),
         "cls": "compact", "nav": ("Pregled", "Overview")},
        {**custom("versus30", ("Razlika", "The difference"), ("Cena jednog papira", "The price of one paper")), "nav": ("Razlika", "Difference")},
        {**custom("network30", ("Šta već postoji", "What already exists"), ("Jedan čvor, osam izvora", "One hub, eight sources"),
                  intro=("Podaci su u državi. Predlog je da služba koja ih treba sama zakuca na vrata druge, a ne ti.", "The data is in the state. The proposal is that the office that needs it knocks on the other's door, not you."), id="net"),
         "nav": ("Registri", "Registers")},
        {**flow(("Put dokumenta", "The path of a paper"), ("Nosiš ili ne nosiš", "You carry it, or you do not"), [
            ("Služba A izdaje uverenje", "Office A issues a certificate"), ("Plaćaš taksu", "You pay a fee"),
            ("Nosiš ga u službu B", "You carry it to office B"), ("Služba B ga prima i prepisuje", "Office B accepts and retypes it")],
            [("Podnosiš jedan zahtev", "You file one request"), ("Služba B preuzima podatke iz registra", "Office B pulls the data from the register"),
             ("Odluka bez tvog nošenja papira", "A decision without you carrying paper")], id="c1", extra="n30_pair"),
         "nav": ("Tok", "Flow")},
        {**custom("board30", ("Kako merimo uspeh", "How we measure success"), ("Javna statistika po službama", "Public statistics per office"),
                  intro=("Svaka služba objavljuje koliko uverenja izda samo da bi se nosila drugoj službi.", "Every office publishes how many certificates it issues only to be carried to another office.")),
         "nav": ("Statistika", "Statistics")},
        {**faq(QA, ("Šta ako…", "What if…"), [
            (("Zar to već nije zakon?", "Isn't that already the law?"), ("Jeste, čl. 9 i 103 ZUP-a. Problem je što pravilo ne važi u praksi svuda i što mnogi registri nisu povezani, pa je potrebna primena, ne novo pravilo.", "It is, Arts. 9 and 103 of ZUP. The problem is that the rule does not hold in practice everywhere and many registers are not connected, so what is needed is enforcement, not a new rule.")),
            (("Podatka nema ni u jednom registru?", "The data is in no register?"), ("Tada ga daje građanin. Službenik ipak mora da obrazloži zašto traži papir, da se ne traži ono što država već ima.", "Then the citizen supplies it. The clerk still has to justify the request, so nothing is asked that the state already holds.")),
        ]), "nav": ("Pitanja", "Q&A")},
    ],
}

# ---------------------------------------------------------------- 21 Pošta reform
PAGES[21] = {
    "stats": [],
    "related": [4, 17, 28, 29],
    "blocks": [
        {**custom("posta_stages", ("Pregled", "Overview"), ("Četiri koraka jedne reforme", "Four steps of one reform"),
                  intro=("Pošta Srbije je mesto gde se država svakodnevno susreće sa građaninom, a veliki deo posla još ide na papiru. Predlog ima četiri koraka.",
                         "Pošta Srbije is where the state meets the citizen every day, and much of the work still runs on paper. The proposal has four steps.")), "cls": "compact"},
        steps(("1/4", "1/4"), ("Analiza svega što je još na papiru", "An audit of everything still on paper"), [
            (("Popis", "Inventory"), ("Svaki papir, obrazac, pečat i šalterski korak u pošti, na jednom spisku.", "Every paper, form, stamp and counter step in the post, on one list.")),
            (("Mapa procesa", "Process map"), ("Za svaki korak: ko ga radi, koji se podaci unose i kuda idu dalje.", "For each step: who does it, which data is entered and where it goes next.")),
            (("Novi tok", "New flow"), ("Svaki papirni korak dobija jasan digitalni, bez duplih unosa i kopija.", "Each paper step gets a clear digital one, with no double entry or copies.")),
            (("Digitalizacija", "Digitise"), ("Digitalizuje se sve što može, do cilja od 99,9% elektronskih procesa.", "Everything that can be digital goes digital, up to the target of 99.9% electronic processes.")),
        ], id="p1", extra="posta_target",
              intro=("Pre nego što gradimo nešto novo, radimo punu analizu svega što pošta danas radi na papiru i ručno, i pravimo jasan proces kako da se sve to digitalizuje. Cilj je da 99,9% procesa bude elektronsko.",
                     "Before building anything new, we run a full analysis of everything the post still does on paper and by hand, and design a clear process for digitising all of it. The goal is for 99.9% of processes to be digital.")),
        steps(("2/4", "2/4"), ("Nova aplikacija za klijente", "A new app for customers"), [], id="p2", extra="posta_part2",
              intro=("Jedna aplikacija za sve poštanske usluge: prijava preko eUprave, praćenje, preuzimanje paketa QR kodom, carina i plaćanje. U istom dizajnu kao druge državne usluge, bez papirnih obaveštenja i formulara.",
                     "One app for every postal service: sign-in through eUprava, tracking, pickup with a QR code, customs and payment. In the same design as other state services, with no paper notices or forms.")),
        steps(("3/4", "3/4"), ("Nova aplikacija za zaposlene", "A new app for staff"), [], id="p3", extra="posta_part3",
              intro=("Isti sistem iznutra: šalter, upravnik poslovnice, logistika, carina i poštar rade u jednom okruženju. Službenik skenira QR i vidi ceo slučaj, a podaci se ne kucaju ponovo. Poslovnice dobijaju skenere i digitalne procese, pa se usluga obavi za nekoliko minuta.",
                     "The same system from the inside: the counter, the branch manager, logistics, customs and the postman all work in one environment. The clerk scans a QR and sees the whole case, with no retyping of data. Branches get scanners and digital processes, so a service takes a few minutes.")),
        steps(("4/4", "4/4"), ("Sve carinske procedure onlajn i ubrzano carinjenje", "Every customs procedure online, and faster clearance"), [], id="p4", extra="posta_part4",
              intro=("Danas se deklaracija popunjava na šalteru (od 23. februara 2026. Pošta je i naplaćuje), poštar na adresi traži gotovinu, a paketi stoje na carini i više od 35 dana, bez zakonskog roka. Cilj je da sve carinske procedure budu onlajn i da 99,9% pošiljki bude ocarinjeno u roku od jednog radnog dana.",
                     "Today the declaration is filled in at the counter (since 23 February 2026 Pošta Srbije charges for it), the postman at the door wants cash, and parcels sit at customs for over 35 days with no legal deadline. The goal is for every customs procedure to be online and for 99.9% of parcels to be cleared within one working day.")),
        faq(QA, ("Šta ako…", "What if…"), [
            (("Nemam aplikaciju?", "I do not have the app?"), ("Lična karta i šalter ostaju za one koji dođu, samo sa sporijim tokom. Aplikacija je prečica, ne obaveza.", "The ID and the counter stay for people who come in, just with a slower flow. The app is a shortcut, not a duty.")),
            (("Šta ako automat pogreši?", "What if the machine is wrong?"), ("Žališ se i tada odluku pregleda čovek. Složeni slučajevi idu onlajn, a po potrebi možeš doći sa dokumentima.", "You appeal and a human reviews the decision. Complex cases go online, and if needed you can come in with documents.")),
        ]),
    ],
}

for _blk in PAGES[21]["blocks"]:
    _nav = {"p1": ("Analiza", "Analysis"), "p2": ("Klijenti", "Customers"), "p3": ("Zaposleni", "Staff"), "p4": ("Carina", "Customs")}.get(_blk.get("id"))
    if _blk["k"] == "check":
        _nav = ("Promene", "Changes")
    elif _blk["k"] == "faq":
        _nav = ("Pitanja", "Q&A")
    if _nav:
        _blk["nav"] = _nav

# ---------------------------------------------------------------- 47 ID in Wallet
PAGES[47] = {
    "stats": [],
    "related": [4, 5, 6, 11],
    "blocks": [
        {**custom("stages47", ("Pregled", "Overview"), ("Ista isprava, u telefonu", "The same document, in your phone"),
                  intro=("Fizička lična karta i boravišna dozvola gube se, zaboravljaju kod kuće i pokazuju se cele pri svakoj proveri. Predlog je digitalna isprava u Apple i Google novčaniku, po standardu ISO 18013-5 i evropskom EUDI novčaniku, sa istom pravnom snagom kao kartica.",
                         "A physical ID and residence card gets lost, is forgotten at home and is shown in full at every check. The proposal is a digital document in Apple and Google Wallet, following ISO 18013-5 and the EU EUDI wallet, with the same legal force as the card.")),
         "cls": "compact", "nav": ("Pregled", "Overview")},
        {**custom("versus47", ("Razlika", "The difference"), ("Šta pokazuješ pri proveri", "What you show at a check")), "nav": ("Razlika", "Difference")},
        {**flow(("Provera", "The check"), ("Od cele kartice do jednog podatka", "From the whole card to one fact"), [
            ("Nosiš karticu sa sobom", "You carry the card"), ("Pokazuješ celu karticu", "You show the whole card"),
            ("Provera je vizuelna i spora", "The check is visual and slow"), ("Zaboravljena ili izgubljena kartica je problem", "A forgotten or lost card is a problem")],
            [("Dodaš ispravu u novčanik", "You add the document to the wallet"), ("Prineseš telefon čitaču ili pokažeš QR", "Hold the phone to a reader or show a QR"),
             ("Čitač traži samo jedan podatak", "The reader asks for just one fact"), ("Potvrdiš na telefonu", "You approve on the phone"), ("Deli se samo taj podatak", "Only that fact is shared")],
            id="c1", extra="w47_pair"), "nav": ("Provera", "The check")},
        {**cards(WHO, ("Prednosti", "Benefits"), [
            ("Građani", "Citizens", "Dokument je uvek u telefonu i ne može da se izgubi kao kartica.", "The document is always on your phone and cannot be lost like a card."),
            ("Stranci", "Foreigners", "Boravišna dozvola uvek uz sebe, na novčaniku koji već koriste.", "The residence permit always at hand, in the wallet they already use."),
            ("Provera", "Checks", "Traje sekundu, a pokazuje se samo ono što je potrebno.", "Takes a second and shows only what is necessary."),
        ]), "nav": ("Ko dobija", "Who gains")},
        {**faq(QA, ("Šta ako…", "What if…"), [
            (("Telefon ostane bez baterije ili se izgubi?", "My phone dies or is lost?"), ("Pitanje za zakon i uslove izdavanja. Predlog daje digitalnoj ispravi istu snagu kao kartici, a da li plastična kartica ostaje uz nju odlučuje zakon.", "A question for the law and the issuing rules. The proposal gives the digital document the same force as the card, and whether the plastic card stays alongside is for the law to decide.")),
            (("Zašto baš ISO 18013-5 i EUDI?", "Why exactly ISO 18013-5 and EUDI?"), ("Zato što su to standardi koje Apple, Google i EU već koriste, pa isprava radi bez posebnih rešenja.", "Because these are the standards Apple, Google and the EU already use, so the document works without special arrangements.")),
        ]), "nav": ("Pitanja", "Q&A")},
    ],
}

# ---------------------------------------------------------------- 48 abolish registration of stay
PAGES[48] = {
    "stats": [],
    "related": [11, 49, 47, 12],
    "blocks": [
        {**custom("stages48", ("Pregled", "Overview"), ("Zašto prijava boravka ništa ne dodaje", "Why registering a stay adds nothing"),
                  intro=("Stranac mora da prijavi adresu u roku od 24 časa od dolaska i posle svake promene, a stanodavci i hoteli moraju da ga prijave policiji. To je stres za ljude, posao za stanodavce i gomila papira, bez bezbednosti koju granica već ne obezbeđuje.",
                         "A foreigner must register their address within 24 hours of arrival and after every move, and landlords and hotels must report them to the police. It means stress for people, work for landlords and piles of paper, without adding security the border does not already provide.")),
         "cls": "compact", "nav": ("Pregled", "Overview")},
        {**custom("versus48", ("Razlika", "The difference"), ("Rok za prijavu", "The deadline to register")), "nav": ("Razlika", "Difference")},
        {**flow(("Put", "The path"), ("Prijava, pa prijava, pa prijava", "Register, register, register"), [
            ("Stranac stiže", "A foreigner arrives"), ("U roku od 24 h hotel ili stanodavac prijavljuje policiji", "Within 24 h the hotel or landlord reports to the police"),
            ("Selidba na novu adresu", "A move to a new address"), ("Nova prijava u roku od 24 h", "A new registration within 24 h"), ("Rizik od kazne za svaki propušteni rok", "A risk of a fine for each missed deadline")],
            [("Stranac stiže", "A foreigner arrives"), ("Granica beleži ulazak", "The border logs the entry"), ("Nema dalje prijave, nema rokova", "No further registration, no deadlines")],
            id="c1", extra="b48_pair"), "nav": ("Put", "The path")},
        {**custom("countries48", ("Ko je to ukinuo", "Who dropped it"), ("Zemlje i predlog", "Countries and the proposal")), "nav": ("Zemlje", "Countries")},
        {**cards(WHO, ("Ko dobija olakšanje", "Who gets relief"), [
            ("Policija", "Police", "Nema papira i evidencija koje ne daju dodatnu bezbednost.", "No paperwork or records that add no extra security."),
            ("Stanodavci i hoteli", "Landlords and hotels", "Nema obaveze prijavljivanja gostiju.", "No duty to report guests."),
            ("Stranci", "Foreigners", "Nema stresa zbog roka od 24 časa i kazni.", "No stress about the 24-hour deadline and fines."),
        ], intro=("Kontrola ostaje na granici.", "Control stays at the border.")), "nav": ("Ko dobija", "Who gains")},
        {**faq(QA, ("Šta ako…", "What if…"), [
            (("Država neće znati gde stranac živi?", "The state will not know where a foreigner lives?"), ("Argument predloga je da adresna prijava ne dodaje bezbednost koju granica već ne daje: zna se ko je ušao, kada i do kada sme da ostane.", "The proposal's argument is that address registration adds no security the border does not already give: it is known who entered, when and until when they may stay.")),
            (("A boravišne dozvole?", "What about residence permits?"), ("To su zasebni postupci i zasebne ideje, na primer jasni rokovi za boravišne dozvole.", "Those are separate procedures and separate ideas, for example clear deadlines for residence permits.")),
        ]), "nav": ("Pitanja", "Q&A")},
    ],
}

# ---------------------------------------------------------------- 50 legal fast track
PAGES[50] = {
    "stats": [],
    "related": [13, 14, 49, 54],
    "blocks": [
        {**custom("stages50", ("Pregled", "Overview"), ("Tri zvanične brzine", "Three official speeds"),
                  intro=("Ko hitno treba dokument nema legalan način da ga dobije brže, pa traži „vezu”, poznanika ili nekome plati. Predlog je da hitnost postane javna: brzinu biraš pri podnošenju, taksa je zvanična, a novac ide u budžet službe.",
                         "Anyone who needs a document urgently has no legal way to get it faster, so they look for a connection, an acquaintance or someone to pay. The proposal makes urgency public: you pick the speed when filing, the fee is official and the money goes to the office budget.")),
         "cls": "compact", "nav": ("Pregled", "Overview")},
        {**custom("versus50", ("Razlika", "The difference"), ("Kako se danas ubrzava", "How it is sped up today")), "nav": ("Razlika", "Difference")},
        {**custom("speed50", ("Predlog", "The proposal"), ("Tri zvanične brzine", "Three official speeds"),
                  intro=("Brzina je izbor građanina i vidi se unapred.", "Speed is the citizen's choice and visible up front.")), "nav": ("Brzine", "Speeds")},
        {**flow(("Tok novca", "Where the money goes"), ("Od „veze” do računa", "From “connections” to a receipt"), [
            ("Hitno ti treba dokument", "You urgently need a document"), ("Tražiš vezu", "Look for a connection"), ("Plaćaš nekome u džep", "Pay into someone's pocket"), ("Ishod zavisi od poznanstva", "The result depends on who you know")],
            [("Biraš brzinu pri podnošenju", "Choose a speed when filing"), ("Plaćaš višu taksu službenim putem", "Pay the higher fee officially"), ("Novac ide u budžet službe", "The money goes to the office budget"), ("Rok je zvaničan i jasan", "The deadline is official and clear")],
            id="c1", extra="f50_pair"), "nav": ("Tok", "Flow")},
        {**bars(("Primer: Gruzija", "Example: Georgia"), ("Pasoš po brzini", "A passport by speed"), [
            (("10 radnih dana", "10 working days"), 150, ("150 lari", "150 lari"), "lo"),
            (("24 sata", "24 hours"), 300, ("300 lari", "300 lari"), ""),
            (("Isti dan", "Same day"), 350, ("350 lari", "350 lari"), "hi"),
        ], note=("Izvor: SDA (Gruzija), rokovi i takse za pasoš.", "Source: SDA (Georgia), passport terms and fees."), unit="lari"), "nav": ("Gruzija", "Georgia")},
        {**cards(("Primer: Velika Britanija", "Example: the United Kingdom"), ("Dve brže opcije za pasoš", "Two faster options for a passport"), [
            ("Fast track", "Fast track", "Pasoš za nedelju dana uz višu taksu.", "A passport in one week for a higher fee."),
            ("Premium", "Premium", "Pasoš za jedan dan uz još višu taksu.", "A passport in one day for a still higher fee."),
        ], intro=("Izvor: GOV.UK, hitno izdavanje pasoša.", "Source: GOV.UK, getting a passport urgently.")), "nav": ("UK", "UK")},
        {**faq(QA, ("Šta ako…", "What if…"), [
            (("Ovo ne pogoduje bogatima?", "This favours the rich?"), ("Standardna brzina i njena taksa ostaju. Danas hitnost već postoji, samo kroz vezu koja je nezvanična i nejednaka. Predlog je čini javnom i jednakom.", "The standard speed and its fee stay. Today urgency already exists, only through connections that are unofficial and unequal. The proposal makes it public and equal.")),
            (("Neće li standard postati sporiji?", "Won't the standard get slower?"), ("To je rizik koji treba pratiti. Zato je predlog povezan sa javnom tablom kvaliteta usluga, gde se vide stvarni rokovi.", "That is a risk to watch. This is why the proposal ties in with a public dashboard of service quality, where real deadlines show.")),
        ]), "nav": ("Pitanja", "Q&A")},
    ],
}

# ---------------------------------------------------------------- 53 exchange a foreign driving licence
PAGES[53] = {
    "stats": [],
    "related": [11, 14, 17, 49],
    "blocks": [
        {**custom("stages53", ("Pregled", "Overview"), ("Zamena strane vozačke dozvole bez nagađanja", "Exchanging a foreign licence without the guesswork"),
                  intro=("Stranac sa odobrenim stalnim boravkom, kao i državljanin koji se vraća da stalno živi u Srbiji, sme da vozi sa stranom dozvolom do šest meseci od ulaska u zemlju, a posle toga mora da je zameni ili da izvadi novu. Zvanične stranice ne opisuju kako se zamena radi.",
                         "A foreigner with approved permanent residence, like a citizen returning to live in Serbia, may drive on a foreign licence for up to six months from entering the country, and after that must exchange it or apply for a new one. The official pages do not describe how an exchange works.")),
         "cls": "compact", "nav": ("Pregled", "Overview")},
        {**custom("versus53", ("Razlika", "The difference"), ("Gde saznaješ šta ti treba", "Where you find out what you need")), "nav": ("Razlika", "Difference")},
        {**flow(("Put do dozvole", "The path"), ("Od nagađanja do jasnog toka", "From guessing to a clear flow"), [
            ("Pročitaš da dozvolu moraš da zameniš", "You read that the licence must be exchanged"), ("Tražiš dokumenta po forumima", "Search forums for the documents"),
            ("Ne znaš da li se polaže", "You do not know whether a test is needed"), ("Dođeš na šalter, nešto fali", "Go to a counter, something is missing"), ("Vraćaš se", "Come back")],
            [("Biraš zemlju izdavanja", "Pick the country of issue"), ("Vidiš pravilo i spisak dokumenata", "See the rule and the list of documents"),
             ("Podnosiš zahtev i plaćaš onlajn", "Apply and pay online"), ("Zakazuješ samo ono što mora uživo", "Book only what must be done in person"), ("Pratiš status do dozvole", "Track the status until the licence")],
            note=("Ilustrativan tok. Tačne korake određuju propisi i nadležna služba.", "Illustrative path. The exact steps are set by the regulations and the competent office."), id="c1", extra="d53_pair"),
         "nav": ("Tok", "The flow")},
        {**custom("licence53", ("Predlog", "The proposal"), ("Javna stranica po zemlji izdavanja", "A public page per country of issue"),
                  intro=("Odgovor na pitanje „šta mi treba?” treba da stoji na jednom mestu, pre nego što ikoga pitaš.", "The answer to “what do I need?” should be in one place, before you ask anyone.")),
         "nav": ("Po zemljama", "Per country")},
        {**cards(WHO, ("Koristi svima koji menjaju dozvolu", "Useful to everyone exchanging a licence"), [
            ("Stranci sa boravkom", "Foreigners with residence", "Znaju šta da ponesu i šta da očekuju pre nego što odu na šalter.", "They know what to bring and what to expect before going to a counter."),
            ("Građani koji se vraćaju", "Returning citizens", "Isto šestomesečno pravilo važi i za njih.", "The same six-month rule applies to them."),
            ("Službe", "Offices", "Manje nepotpunih zahteva i ponovnih dolazaka.", "Fewer incomplete applications and repeat visits."),
        ]), "nav": ("Ko dobija", "Who gains")},
        {**faq(QA, ("Šta ako…", "What if…"), [
            (("Menja li ovo ko mora da zameni dozvolu?", "Does this change who has to exchange a licence?"), ("Ne. Pravilo od šest meseci ostaje kakvo jeste, predlog samo čini jasnim kako se postupa.", "No. The six-month rule stays as it is; the proposal only makes it clear how to proceed.")),
            (("Šta je sa bezbednošću u saobraćaju?", "What about road safety?"), ("Provere koje danas važe ostaju. Razlika je u tome što ih unapred vidiš i što se dokumenta ne nose više puta.", "The checks that apply today stay. The difference is that you see them in advance and do not carry documents more than once.")),
        ]), "nav": ("Pitanja", "Q&A")},
    ],
}
