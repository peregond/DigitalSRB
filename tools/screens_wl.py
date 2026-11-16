"""Concept screens for the Wallet ID (idea 47, violet) and the foreign driving licence exchange (idea 53, navy).
All names, countries and dates are examples. Importing this module registers the pairs in posta_app.PAIRS."""
from posta_app import B, PAIRS, browser, chip, ic, phone, ICONS

ICONS.setdefault("wallet", "M3 7a2 2 0 0 1 2-2h14v4M3 7v11a2 2 0 0 0 2 2h16V9H5a2 2 0 0 1-2-2zM17 14.5h.01")
ICONS.setdefault("nfc", "M6 8a8 8 0 0 1 0 8M10 6a12 12 0 0 1 0 12M14 4a16 16 0 0 1 0 16")
ICONS.setdefault("car", "M5 17H3v-5l2-5h14l2 5v5h-2M5 17a2 2 0 1 0 4 0M15 17a2 2 0 1 0 4 0M9 17h6M3 12h18")


def _row(sr, en, on):
    return f'<li class="{"on" if on else "off"}"><b>{ic("check") if on else "–"}</b>{B(sr, en)}</li>'


def s_wallet():
    rows = "".join(_row(*r) for r in [("Punoletan", "Over 18", True), ("Ime i fotografija", "Name and photo", True), ("JMBG", "Personal number", False), ("Adresa", "Address", False)])
    return phone(f"""
<div class="pa-nav"><span>{ic("back")}</span>{B("Novčanik", "Wallet", "b")}<span></span></div>
<div class="wl-card"><span class="wl-flag">{B("REPUBLIKA SRBIJA", "REPUBLIC OF SERBIA")}</span><b>{B("Lična karta i boravak", "ID and residence")}</b>
<div class="wl-id"><i></i><p>{B("IME PREZIME", "NAME SURNAME")}<small>{B("Privremeni boravak", "Temporary residence")}</small></p></div><span class="wl-nfc">{ic("nfc")}</span></div>
<div class="pa-card"><p class="pa-k">{B("Čitač traži:", "The reader asks for:")} <em class="pa-ex">{B("primer", "example")}</em></p><ul class="wl-share">{rows}</ul></div>
<button class="pa-btn primary">{B("Potvrdi i podeli", "Approve and share")}</button>
<p class="pa-fine c">{B("Deli se samo ono što je označeno.", "Only what is ticked is shared.")}</p>""", tab=None)


def w_verify():
    return browser(f"""
<div class="pa-wnav"><span class="pa-wlogo">{ic("shield")}</span><b>{B("Provera isprave", "Document check")}</b><span class="pa-wuser">{ic("nfc")}{B("Čitač spreman", "Reader ready")}</span></div>
<div class="pa-wgrid">
<div class="pa-card"><p class="pa-k">{B("Šta se traži", "What is asked")}</p>
<div class="pa-line">{B("Pitanje", "Question")}<b>{B("Da li je punoletan?", "Is the person over 18?")}</b></div>
<div class="pa-line">{B("Način", "Method")}<b>QR / NFC</b></div>{chip("blue", "ISO 18013-5", "ISO 18013-5")}</div>
<div class="pa-card"><p class="pa-k">{B("Odgovor", "The answer")}</p><div class="pa-bigamt">{B("DA", "YES")}</div>
{chip("ok", "Potvrđeno za sekundu", "Confirmed in a second")}{B("Ime, JMBG i adresa nisu primljeni.", "Name, personal number and address were not received.", "small")}</div></div>
<div class="pa-wfoot"><p class="pa-fine">{B("Isprava je važeća i ista kao kartica, a čitač vidi samo traženi podatak.", "The document is valid and equal to the card, and the reader sees only the requested fact.")}</p></div>""", url="provera.gov.rs")


def s_licence():
    def doc(sr, en, ok):
        return f'<li class="{"ok" if ok else "miss"}"><b>{ic("check") if ok else "!"}</b><div>{B(sr, en, "span")}</div></li>'
    return phone(f"""
<div class="pa-nav"><span>{ic("back")}</span>{B("Zamena dozvole", "Licence exchange", "b")}<span class="pa-step">1/3</span></div>
<div class="pa-card"><div class="pa-field">{B("Zemlja izdavanja", "Country of issue", "small")}<div class="pa-select">{B("Zemlja A (primer)", "Country A (example)")}{ic("back", "pa-chev")}</div></div>
{chip("ok", "Dozvola se priznaje", "The licence is recognised")}{chip("ok", "Polaganje nije potrebno", "No test needed")}</div>
<div class="pa-card"><p class="pa-k">{B("Dokumenta", "Documents")}</p><ul class="pa-checks case">{doc("Pasoš", "Passport", True)}{doc("Strana vozačka dozvola", "Foreign driving licence", True)}{doc("Boravišna dozvola", "Residence permit", False)}</ul></div>
<div class="pa-estimate">{B("Taksa", "Fee")}<b>{B("primer", "example")}</b></div>
<button class="pa-btn primary">{B("Nastavi", "Continue")}</button>""", tab=None)


def w_licence():
    def d(sr, en, ok):
        return f'<li class="{"ok" if ok else "miss"}"><b>{ic("check") if ok else "!"}</b>{B(sr, en)}</li>'
    return browser(f"""
<div class="pa-wnav"><span class="pa-wlogo">{ic("car")}</span><b>{B("Zamena vozačke dozvole", "Driving licence exchange")}</b><span class="pa-wuser">{ic("user")}eUprava</span></div>
<div class="pa-stepper"><span class="d">{ic("check")}{B("Zemlja", "Country")}</span><span class="n">2 {B("Dokumenta", "Documents")}</span><span>3 {B("Taksa i termin", "Fee and slot")}</span></div>
<div class="pa-wgrid">
<div class="pa-card"><p class="pa-k">{B("Potrebna dokumenta", "Required documents")}</p><ul class="pa-checks case">{d("Pasoš", "Passport", True)}{d("Strana vozačka dozvola", "Foreign licence", True)}{d("Boravišna dozvola", "Residence permit", False)}</ul></div>
<div class="pa-card"><p class="pa-k">{B("Status", "Status")} <em class="pa-ex">{B("primer", "example")}</em></p>
<div class="pa-line">{B("Pravilo", "Rule")}<b>{B("Zamena bez polaganja", "Exchange, no test")}</b></div><div class="pa-line">{B("Odluka do", "Decision by")}<b>{B("za 15 dana", "in 15 days")}</b></div>
{chip("warn", "Fali jedno dokumento", "One document missing")}</div></div>
<div class="pa-wfoot"><button class="pa-btn primary">{B("Dodaj boravišnu dozvolu", "Add the residence permit")}</button></div>""", url="euprava.gov.rs")


PAIRS["w47"] = (s_wallet, w_verify, ("Aplikacija: novčanik i deljenje", "App: the wallet and sharing"), ("Veb: provera isprave", "Web: the document check"))
PAIRS["d53"] = (s_licence, w_licence, ("Aplikacija: zamena dozvole", "App: licence exchange"), ("Veb: dokumenta i status", "Web: documents and status"))
