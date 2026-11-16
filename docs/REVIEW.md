# Review checklist for the drafted text

The detail pages mix **your ideas and sourced figures** with **text I drafted** to explain how an idea could work: the steps,
the before/after lists, the answers to "what if", the card texts and the comparisons. The drafted text has not been checked
against real procedures. Please read it and tick or fix each line. Texts live in `tools/pages_data.py` and `tools/build_pages.py`;
after editing run `python3 tools/build.py`.

**Always examples, never data:** names, amounts, dates, branches, countries ("Country A"), ID numbers and the "bank" names on the
screens and in the portal mock are made up and labelled "example". The old ePorezi and APR pictures are real screenshots (personal data removed).

## What I am least sure about

- **QR at the counter (idea 1):** a printed code or an SMS link for people without a smartphone, and the "system is down, fall back to paper" answer are my assumptions.
- **Business closing (idea 22):** that the state can calculate the final tax on the same day, and the larger-firm rule (pay now, top up after the report), are the proposal's logic, not an existing procedure. The 2-3 months figure and the Georgia/Estonia examples are sourced.
- **Papers the state already has (idea 30):** the 18 databases, eight institutions and the EUR 50 property sheet are sourced; "a clerk must justify a request in writing" and the public statistics per office are the proposal.
- **Wallet ID (idea 47):** ISO 18013-5 and EUDI are named in your text; the "share only what is needed" flow follows those standards but the screens are a concept.
- **Registration of stay (idea 48):** Kazakhstan (2020) and the UK (2022) come from your sources; the claim that the border database is enough is your argument, presented as such.
- **Fast track (idea 50):** 30 / 15 / 7 days with +50% and double fee are from your text; the Georgian passport prices and the UK options are sourced. The sample fee amounts on the screens are invented.
- **Driving licence (idea 53):** the six-month rule is sourced (Welcome to Serbia). I found **no official list of countries or procedure**, so the page proposes a public page per country and does not claim any country is recognised.
- **Single tax portal (idea 9):** how ePorezi and APR look today comes from screenshots you supplied; that agencies stay independent is your condition. The portal screens are a concept.

---

## Merge the APR and ePorezi portals
`/idea/tax-portal/`

### Merge the APR and ePorezi portals
- [ ] Register a business and pay taxes on one portal.

### One portal instead of two
- [ ] Today you register a business in one electronic system and pay taxes in another, so you have to switch from portal to portal. The proposal is a single tax portal where it is all in one place.
- [ ] One entry point
- [ ] A single tax portal, one sign-in.
- [ ] Register a business
- [ ] Registration and changes of data in the same portal.
- [ ] Pay taxes
- [ ] Filings and payments without moving to another system.
- [ ] Agencies stay independent
- [ ] Only the electronic services are brought together.

### One portal, one view
- [ ] What it looks like
- [ ] Today ePorezi offers three ways to sign in and programs to download, and APR has its own portal with its own services. The single portal shows it all on one screen, on one account.

### Registration and taxes
- [ ] The path
- [ ] You register the business on the APR portal
- [ ] You switch to the ePorezi portal
- [ ] There you file and pay taxes
- [ ] You follow the status in two systems
- [ ] You sign in once to the single portal
- [ ] You register the business
- [ ] You pay taxes in the same portal
- [ ] One view of obligations and status
- [ ] An illustrative path; the exact steps depend on the service.

### The agencies stay independent
- [ ] Who does what
- [ ] Each agency still decides on its own data and procedures.
- [ ] APR
- [ ] Registration and changes of data, as before. The services are available in the single portal.
- [ ] Poreska uprava
- [ ] Taxes, filings and payments, as before. The services are available in the single portal.
- [ ] The single portal
- [ ] One sign-in and one view. Only the electronic services are brought together, not the agencies.

### What if…
- [ ] Questions and answers
- [ ] Are APR and Poreska uprava merged?
- [ ] No. The agencies stay independent. Only their electronic services are brought together, on one portal.
- [ ] Who is responsible for the data?
- [ ] Each agency for its own data and decisions, as today. The portal only shows them in one place.

## One QR code for every counter
`/idea/qr-counter/`

### One QR code for every counter
- [ ] Scan once. The clerk already knows your case.

### How one QR code works
- [ ] At a MUP, APR or opština counter today you have to explain what you need, and the clerk guesses the procedure, asks for papers and types the data by hand. With a case QR code all of that goes away.
- [ ] A QR code per case
- [ ] In eUprava every case has a personal QR code.
- [ ] Show it at the counter
- [ ] On your phone, printed or as an SMS link.
- [ ] The clerk scans
- [ ] Your case opens: its history and status.
- [ ] Only what is missing
- [ ] The clerk asks only what is specific, and you see the new status.

### At the counter
- [ ] The difference
- [ ] You explain
- [ ] The same story at every counter, while the clerk guesses the procedure and retypes the data.
- [ ] You scan
- [ ] The clerk sees your case at once and you explain nothing.

### The same counter, two ways
- [ ] The path
- [ ] Wait in line
- [ ] Explain what you need
- [ ] Clerk guesses the procedure
- [ ] Hand over papers
- [ ] Clerk types the data
- [ ] An answer, or come back tomorrow
- [ ] Open the case in eUprava
- [ ] Show your QR code
- [ ] Clerk scans, the case opens
- [ ] Only specific follow-up questions
- [ ] The next step is clear at once
- [ ] Illustrative path; the steps differ from office to office.

### Everyone gains
- [ ] Who benefits
- [ ] Citizens
- [ ] Nothing to explain, fewer papers and fewer trips.
- [ ] Foreigners
- [ ] The same flow in English, without needing to know the local jargon.
- [ ] Clerks
- [ ] One standard screen, less typing and fewer disputes.
- [ ] The state
- [ ] Fewer errors, a clear trace of every step and less room for “connections”.

### What if…
- [ ] Questions and answers
- [ ] I have no smartphone?
- [ ] The code can be printed or arrive as an SMS link. The counter stays open for people who arrive with nothing, just with a longer procedure.
- [ ] Is it safe to show a QR code?
- [ ] The QR holds only a random case reference. The clerk must be logged in, and every access to your case is logged and visible to you in the app.
- [ ] The system is down?
- [ ] The procedure falls back to today's paper one. The QR adds no new dependency, it only shortens the path.

## Two eUprava levels instead of three
`/idea/two-levels/`

### Two eUprava levels instead of three
- [ ] Two account levels instead of three, with no counter visit.

### Two levels instead of three
- [ ] Already exists: eID has three ways to log in, a password, the ConsentID app and a qualified certificate (chip ID card or cloud certificate). For the higher level the activation code is collected at a counter or via a certificate, and three levels confuse people.
- [ ] Basic level
- [ ] An email and a document scan, at once and also for foreigners.
- [ ] Full level
- [ ] Confirmation through a bank, a chip ID card or the pošta.
- [ ] No counter
- [ ] No counter visit and no activation code.
- [ ] For foreigners
- [ ] Basic access at once, full access with residence.

### How many levels you have to understand
- [ ] The difference
- [ ] ways
- [ ] A password, ConsentID and a certificate, and the higher level needs a counter.
- [ ] levels
- [ ] Basic and full, with no counter visit.
- [ ] Source: the eID portal, sign-in by password, the ConsentID app or a certificate.

### From confusion to two clear levels
- [ ] The path to a full account
- [ ] Choose between a password, ConsentID and a certificate
- [ ] You do not know which level you need
- [ ] For the higher level you go to a counter for an activation code
- [ ] Only then can you use every service
- [ ] Basic: an email and a scan of a document
- [ ] You use the basic services at once
- [ ] Full: confirm through a bank, a chip ID card or the pošta
- [ ] With no counter visit, under the eIDAS standard
- [ ] Foreigners get basic access at once and full access with residence.

### What if…
- [ ] Questions and answers
- [ ] I do not have a bank account?
- [ ] You can also confirm your identity with a chip ID card or through the pošta. The bank is just one of three options.
- [ ] What about foreigners?
- [ ] They get basic access at once and full access once they have residence.

### Sources on this page
- eID portal: prijava lozinkom, aplikacijom ConsentID ili sertifikatom

## Open and close a business in one day, taxes settled at once
`/idea/business-in-a-day/`

### Open and close a business in one day, taxes settled at once
- [ ] Opening and closing a business in one working day, with the final tax shown and paid at once, not months later.

### Closing a business in four steps
- [ ] Electronic registration of a preduzetnik (sole trader) already exists, and since December 2023 so does an online deregistration request on the APR portal. The problem is that the final tax assessment often arrives only 2–3 months after deregistration.
- [ ] Request online
- [ ] One request at APR, no counter.
- [ ] Tax at once
- [ ] Poreska works out the final tax from its own data.
- [ ] You see and pay
- [ ] The amount is on screen at deregistration, with no decision months later.
- [ ] Closed in a day
- [ ] Deletion and payment in the same working day.

### When you learn what you owe
- [ ] The difference
- [ ] months
- [ ] The final tax assessment only arrives after deregistration.
- [ ] day
- [ ] You see and pay the final tax when you close.

### What changes when you close
- [ ] Closing
- [ ] You file an online deregistration request
- [ ] The business is deleted, but you do not know what you owe
- [ ] After 2–3 months a decision with the final tax arrives
- [ ] Only then do you pay
- [ ] You file the request online
- [ ] Poreska calculates the final tax at once
- [ ] You see the amount and pay the same day
- [ ] The business is closed

### When a monthly report is missing
- [ ] Larger firms
- [ ] Closing waits for the report
- [ ] The report is filed
- [ ] A decision arrives months later
- [ ] Pay what is calculated now
- [ ] The business closes
- [ ] Top up the difference after the report
- [ ] The state keeps its right to the difference, and the firm does not wait for months.

### How others do it
- [ ] Examples abroad
- [ ] Serbia today
- [ ] An online deregistration request, assessment after 2–3 months.
- [ ] Georgia
- [ ] Registration and deletion in 1 working day.
- [ ] Estonia
- [ ] Online deletion of a company.
- [ ] The proposal for Serbia
- [ ] One day, the final tax settled at once.

### What if…
- [ ] Questions and answers
- [ ] The firm has unpaid obligations?
- [ ] The final assessment shows them at once, so there is no surprise after closing. Payment happens in the same step.
- [ ] Can the state calculate it all that fast?
- [ ] Everything reported is already in its records. What is missing, such as a report, is handled by topping up the difference.
- [ ] Why not keep today's way?
- [ ] Because months of uncertainty after closing cost people time and stress, and the state has the data anyway.

### Sources on this page
- NAPR (Gruzija): takse i rokovi, registracija i brisanje za 1 radni dan
- RIK (Estonija): brisanje firme onlajn
- Biznis.rs (dec. 2023): APR, onlajn promene i brisanje preduzetnika

## Never ask for papers the state already has
`/idea/no-papers/`

### Never ask for papers the state already has
- [ ] The state already has your papers. Stop carrying them.

### Four rules
- [ ] Since 2016 the Law on General Administrative Procedure (ZUP, Arts. 9 and 103) obliges offices to obtain data themselves from official records, and eZUP links 18 databases of eight institutions. The rule is not followed everywhere and many registers are not in eZUP, so people still carry certificates.
- [ ] Every register in eZUP
- [ ] Including local registers and public companies.
- [ ] A paper only with a reason
- [ ] A clerk who asks for a paper must justify it in writing.
- [ ] Complain online
- [ ] The citizen complains without going to a counter.
- [ ] Public statistics
- [ ] Per office: how many certificates are issued only to be carried on.

### The price of one paper
- [ ] The difference
- [ ] up to €50
- [ ] What a list nepokretnosti (property sheet) costs when you carry it from one office to another.
- [ ] The office pulls the data from the register itself, and you carry nothing.
- [ ] Source: Novosti, a property sheet up to €50 instead of 0 din.

### One hub, eight sources
- [ ] What already exists
- [ ] The data is in the state. The proposal is that the office that needs it knocks on the other's door, not you.
- [ ] Civil registers
- [ ] MUP
- [ ] Poreska uprava
- [ ] PIO
- [ ] NSZ
- [ ] CROSO
- [ ] RGZ
- [ ] Judiciary

### You carry it, or you do not
- [ ] The path of a paper
- [ ] Office A issues a certificate
- [ ] You pay a fee
- [ ] You carry it to office B
- [ ] Office B accepts and retypes it
- [ ] You file one request
- [ ] Office B pulls the data from the register
- [ ] A decision without you carrying paper

### Public statistics per office
- [ ] How we measure success
- [ ] Every office publishes how many certificates it issues only to be carried to another office.

### What if…
- [ ] Questions and answers
- [ ] Isn't that already the law?
- [ ] It is, Arts. 9 and 103 of ZUP. The problem is that the rule does not hold in practice everywhere and many registers are not connected, so what is needed is enforcement, not a new rule.
- [ ] The data is in no register?
- [ ] Then the citizen supplies it. The clerk still has to justify the request, so nothing is asked that the state already holds.

### Sources on this page
- Novosti: list nepokretnosti do 50 € umesto 0 din
- Pravni portal: ZUP čl. 9 i 103, organ sam pribavlja podatke
- MDULS: reforma upravnog postupka i eZUP (18 baza, 8 institucija)

## Pošta reform
`/idea/posta-reform/`

### Pošta reform
- [ ] We digitalise what is still done on paper and remove the manual work that slows every stage of the post: from sending and processing to delivery and pickup.

### Four steps of one reform
- [ ] Pošta Srbije is where the state meets the citizen every day, and much of the work still runs on paper. The proposal has four steps.
- [ ] Analysis and processes
- [ ] An inventory of everything on paper and a clear digitisation plan, aiming at 99.9%.
- [ ] App for customers
- [ ] Every service and a parcel with one QR code, in one app.
- [ ] App for staff
- [ ] The counter, branch, logistics, customs and postman in one system.
- [ ] Customs online and in a day
- [ ] Every procedure online, 99.9% of parcels cleared in one working day.

### An audit of everything still on paper
- [ ] Before building anything new, we run a full analysis of everything the post still does on paper and by hand, and design a clear process for digitising all of it. The goal is for 99.9% of processes to be digital.
- [ ] Inventory
- [ ] Every paper, form, stamp and counter step in the post, on one list.
- [ ] Process map
- [ ] For each step: who does it, which data is entered and where it goes next.
- [ ] New flow
- [ ] Each paper step gets a clear digital one, with no double entry or copies.
- [ ] Digitise
- [ ] Everything that can be digital goes digital, up to the target of 99.9% electronic processes.
- [ ] Target: digital
- [ ] 99.9%
- [ ] Paper
- [ ] 0.1%
- [ ] The share of the post's processes that are electronic. Paper stays only where a regulation expressly requires it.

### A new app for customers
- [ ] One app for every postal service: sign-in through eUprava, tracking, pickup with a QR code, customs and payment. In the same design as other state services, with no paper notices or forms.
- [ ] A parcel with one QR code
- [ ] The QR is verified in advance because the app login is already two-factor. The same QR works for payments and other state services at the post office.
- [ ] Bring a paper notice
- [ ] The clerk types the data
- [ ] Takes and copies your ID
- [ ] Everything from scratch for every service
- [ ] Log in to the app via eUprava with 2FA
- [ ] The parcel has a pickup QR code
- [ ] The clerk scans, types nothing
- [ ] Extra check: a four-digit code on your phone
- [ ] ID only for duty or fees, as a separate step

### A new app for staff
- [ ] The same system from the inside: the counter, the branch manager, logistics, customs and the postman all work in one environment. The clerk scans a QR and sees the whole case, with no retyping of data. Branches get scanners and digital processes, so a service takes a few minutes.
- [ ] The counter
- [ ] The clerk scans the QR and sees the whole case at once, and accepting a parcel runs on the data from the app.
- [ ] Branch and logistics
- [ ] The manager sees the queue, the wait and the share of paper in real time, and logistics sees the flow of every parcel and only the exceptions.
- [ ] The postman
- [ ] The day's route, the address and a top-up at the door by an NBS IPS QR.

### Every customs procedure online, and faster clearance
- [ ] Today the declaration is filled in at the counter (since 23 February 2026 Pošta Srbije charges for it), the postman at the door wants cash, and parcels sit at customs for over 35 days with no legal deadline. The goal is for every customs procedure to be online and for 99.9% of parcels to be cleared within one working day.
- [ ] Declaration and payment online
- [ ] You declare in the app, see a public calculation up front and pay online, and if something is still due at the door you use an NBS IPS QR.
- [ ] Clearance within one working day
- [ ] The system is almost fully automated, and you can appeal an automatic decision so a human reviews it.
- [ ] 35+ days
- [ ] Target
- [ ] 1 working day
- [ ] Today there is no legal deadline for clearance. Source: Kurir, parcels at customs for over 35 days.
- [ ] Inside the customs service
- [ ] The system makes most decisions, and the officer reviews only the appeals.

### What if…
- [ ] Questions and answers
- [ ] I do not have the app?
- [ ] The ID and the counter stay for people who come in, just with a slower flow. The app is a shortcut, not a duty.
- [ ] What if the machine is wrong?
- [ ] You appeal and a human reviews the decision. Complex cases go online, and if needed you can come in with documents.

### Sources on this page
- 021: Pošta Srbije uvela naplatu carinske deklaracije
- Kurir: pošiljke na carini i više od 35 dana

## ID and residence card in Apple and Google Wallet
`/idea/wallet-id/`

### ID and residence card in Apple and Google Wallet
- [ ] Your ID and residence card in your phone wallet.

### The same document, in your phone
- [ ] A physical ID and residence card gets lost, is forgotten at home and is shown in full at every check. The proposal is a digital document in Apple and Google Wallet, following ISO 18013-5 and the EU EUDI wallet, with the same legal force as the card.
- [ ] The document in the wallet
- [ ] ID and residence card in Apple and Google Wallet.
- [ ] A check in a second
- [ ] QR or NFC, without taking out a card.
- [ ] Share only what is needed
- [ ] For example only that you are over 18.
- [ ] The same legal force
- [ ] As the card, under ISO 18013-5 and EUDI.

### What you show at a check
- [ ] The difference
- [ ] The whole card
- [ ] At every check you show everything printed on it.
- [ ] One fact
- [ ] The reader gets only what it asks for, for example that you are over 18.

### From the whole card to one fact
- [ ] The check
- [ ] You carry the card
- [ ] You show the whole card
- [ ] The check is visual and slow
- [ ] A forgotten or lost card is a problem
- [ ] You add the document to the wallet
- [ ] Hold the phone to a reader or show a QR
- [ ] The reader asks for just one fact
- [ ] You approve on the phone
- [ ] Only that fact is shared

### Benefits
- [ ] Who benefits
- [ ] Citizens
- [ ] The document is always on your phone and cannot be lost like a card.
- [ ] Foreigners
- [ ] The residence permit always at hand, in the wallet they already use.
- [ ] Checks
- [ ] Takes a second and shows only what is necessary.

### What if…
- [ ] Questions and answers
- [ ] My phone dies or is lost?
- [ ] A question for the law and the issuing rules. The proposal gives the digital document the same force as the card, and whether the plastic card stays alongside is for the law to decide.
- [ ] Why exactly ISO 18013-5 and EUDI?
- [ ] Because these are the standards Apple, Google and the EU already use, so the document works without special arrangements.

## Abolish registration of stay for foreigners
`/idea/no-registration/`

### Abolish registration of stay for foreigners
- [ ] No more 24-hour registration of stay for foreigners.

### Why registering a stay adds nothing
- [ ] A foreigner must register their address within 24 hours of arrival and after every move, and landlords and hotels must report them to the police. It means stress for people, work for landlords and piles of paper, without adding security the border does not already provide.
- [ ] The border logs the entry
- [ ] Who entered, when and on what basis.
- [ ] The system counts the days
- [ ] Visa-free 90/180, a visa or a permit: the days left are calculated by themselves.
- [ ] No registration of stay
- [ ] Not on paper or online, not from hotels or landlords.
- [ ] Control stays at the border
- [ ] Security is not reduced and the paperwork is gone.

### The deadline to register
- [ ] The difference
- [ ] That is how long a foreigner has to register an address, and again after every move.
- [ ] No registration of stay, on paper or online. The border database is enough.
- [ ] Source: the Serbian MFA, foreigners register stay within 24 hours.

### Register, register, register
- [ ] The path
- [ ] A foreigner arrives
- [ ] Within 24 h the hotel or landlord reports to the police
- [ ] A move to a new address
- [ ] A new registration within 24 h
- [ ] A risk of a fine for each missed deadline
- [ ] The border logs the entry
- [ ] No further registration, no deadlines

### Countries and the proposal
- [ ] Who dropped it
- [ ] Serbia today
- [ ] Register within 24 h and after every move.
- [ ] Kazakhstan, 2020
- [ ] Registration dropped for stays up to 30 days.
- [ ] United Kingdom, 2022
- [ ] Police registration of foreigners dropped.
- [ ] The proposal for Serbia
- [ ] Abolish fully, paper and online.

### Who gets relief
- [ ] Who benefits
- [ ] Control stays at the border.
- [ ] Police
- [ ] No paperwork or records that add no extra security.
- [ ] Landlords and hotels
- [ ] No duty to report guests.
- [ ] Foreigners
- [ ] No stress about the 24-hour deadline and fines.

### What if…
- [ ] Questions and answers
- [ ] The state will not know where a foreigner lives?
- [ ] The proposal's argument is that address registration adds no security the border does not already give: it is known who entered, when and until when they may stay.
- [ ] What about residence permits?
- [ ] Those are separate procedures and separate ideas, for example clear deadlines for residence permits.

### Sources on this page
- MSP Srbije: prijava boravka stranaca u roku od 24 časa
- Astana Times: Kazahstan ukida obaveznu registraciju za boravak do 30 dana (2020)
- Lewis Silkin: UK ukida prijavu stranaca policiji (2022)

## Legal fast track for documents
`/idea/fast-track/`

### Legal fast track for documents
- [ ] Three official speeds. The fee goes to the budget, not a pocket.

### Three official speeds
- [ ] Anyone who needs a document urgently has no legal way to get it faster, so they look for a connection, an acquaintance or someone to pay. The proposal makes urgency public: you pick the speed when filing, the fee is official and the money goes to the office budget.
- [ ] Three speeds
- [ ] Standard 30 days, 15 days for +50% and 7 days for double the fee.
- [ ] Pick when filing
- [ ] The speed and the fee are visible up front.
- [ ] Pay officially
- [ ] An official payment and receipt, without “connections”.
- [ ] Money to the budget
- [ ] The fee goes to the office budget, not into someone's pocket.

### How it is sped up today
- [ ] The difference
- [ ] A connection
- [ ] Urgency exists, but informally: an acquaintance, a favour or money into a pocket.
- [ ] A receipt
- [ ] The same urgency, but public, equal for all and with an official receipt.

### Three official speeds
- [ ] The proposal
- [ ] Speed is the citizen's choice and visible up front.
- [ ] Fee
- [ ] days
- [ ] Standard
- [ ] Faster
- [ ] Urgent

### From “connections” to a receipt
- [ ] Where the money goes
- [ ] You urgently need a document
- [ ] Look for a connection
- [ ] Pay into someone's pocket
- [ ] The result depends on who you know
- [ ] Choose a speed when filing
- [ ] Pay the higher fee officially
- [ ] The money goes to the office budget
- [ ] The deadline is official and clear

### A passport by speed
- [ ] Example: Georgia
- [ ] 10 working days
- [ ] 150 lari
- [ ] 24 hours
- [ ] 300 lari
- [ ] Same day
- [ ] 350 lari
- [ ] Source: SDA (Georgia), passport terms and fees.

### Two faster options for a passport
- [ ] Example: the United Kingdom
- [ ] Source: GOV.UK, getting a passport urgently.
- [ ] Fast track
- [ ] A passport in one week for a higher fee.
- [ ] Premium
- [ ] A passport in one day for a still higher fee.

### What if…
- [ ] Questions and answers
- [ ] This favours the rich?
- [ ] The standard speed and its fee stay. Today urgency already exists, only through connections that are unofficial and unequal. The proposal makes it public and equal.
- [ ] Won't the standard get slower?
- [ ] That is a risk to watch. This is why the proposal ties in with a public dashboard of service quality, where real deadlines show.

### Sources on this page
- SDA (Gruzija): rokovi i takse za pasoš
- GOV.UK: hitno izdavanje pasoša (fast track i premium)

## Exchanging a foreign driving licence
`/idea/driving-licence/`

### Exchanging a foreign driving licence
- [ ] Exchange a foreign driving licence without the guesswork.

### Exchanging a foreign licence without the guesswork
- [ ] A foreigner with approved permanent residence, like a citizen returning to live in Serbia, may drive on a foreign licence for up to six months from entering the country, and after that must exchange it or apply for a new one. The official pages do not describe how an exchange works.
- [ ] Rules per country
- [ ] Whether the licence is recognised, a test, documents and the fee.
- [ ] One online flow
- [ ] The application, documents and fee in one step.
- [ ] In person only what must be
- [ ] An appointment only for the step that cannot be done online.
- [ ] Status and deadline
- [ ] You see where it stands and when a decision is due.

### Where you find out what you need
- [ ] The difference
- [ ] Forums
- [ ] You look for the answer to “what do I need?” on blogs and forums.
- [ ] One page
- [ ] The rules, documents and fee for your country, in one place.

### From guessing to a clear flow
- [ ] The path
- [ ] You read that the licence must be exchanged
- [ ] Search forums for the documents
- [ ] You do not know whether a test is needed
- [ ] Go to a counter, something is missing
- [ ] Come back
- [ ] Pick the country of issue
- [ ] See the rule and the list of documents
- [ ] Apply and pay online
- [ ] Book only what must be done in person
- [ ] Track the status until the licence
- [ ] Illustrative path. The exact steps are set by the regulations and the competent office.

### A public page per country of issue
- [ ] The proposal
- [ ] The answer to “what do I need?” should be in one place, before you ask anyone.
- [ ] Country of issue
- [ ] The licence is recognised
- [ ] No test needed
- [ ] Documents: a list with upload
- [ ] Fee: the amount and online payment
- [ ] The licence is not recognised
- [ ] Alternative route: clear steps
- [ ] A layout example. The countries and rules here are placeholders, not real data.

### Useful to everyone exchanging a licence
- [ ] Who benefits
- [ ] Foreigners with residence
- [ ] They know what to bring and what to expect before going to a counter.
- [ ] Returning citizens
- [ ] The same six-month rule applies to them.
- [ ] Offices
- [ ] Fewer incomplete applications and repeat visits.

### What if…
- [ ] Questions and answers
- [ ] Does this change who has to exchange a licence?
- [ ] No. The six-month rule stays as it is; the proposal only makes it clear how to proceed.
- [ ] What about road safety?
- [ ] The checks that apply today stay. The difference is that you see them in advance and do not carry documents more than once.

### Sources on this page
- Welcome to Serbia: vozačka dozvola i osiguranje vozila

