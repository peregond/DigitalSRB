"""The single tax portal block (idea 9): ready-made images, rendered by tools/shots.py.

Left: simplified, deliberately dated views of today's ePorezi and APR sites. Right: the proposed portal.
The Serbian image of the proposal is the default; the English one is shown when the language is switched.
"""
from posta_app import B


def portal_html():
    base = "../../assets/shots/"
    ai = '<span class="pa-aitag">AI</span>'
    note = (f'<div class="pa-ai"><span class="pa-ai-tag">AI</span>'
            f'{B("Vizualizacija je napravljena uz pomoć veštačke inteligencije (AI) i predstavlja koncept. Prikaz današnjih sajtova je uprošćen i nije tačna kopija. Iznosi i datumi su primeri.", "This visual was created with the help of AI and shows a concept. The view of today’s sites is simplified and not an exact copy. Amounts and dates are examples.", "p", "pa-note")}</div>')

    def old(file, sr, en, alt_sr, alt_en):
        return (f'<figure class="shot"><a href="{base}{file}" target="_blank" rel="noopener"><img src="{base}{file}" alt="{alt_en}" loading="lazy" width="2160" height="1215"></a>'
                f'<figcaption><span class="pa-n">{B("DANAS", "TODAY")}{ai}</span>{B(sr, en, "b")}</figcaption></figure>')

    olds = (old("old-eporezi.webp", "ePorezi: tri načina prijave i programi za preuzimanje", "ePorezi: three ways to sign in and programs to download", "", "Simplified view of today's ePorezi start page")
            + old("old-apr.webp", "APR: poseban portal sa svojim uslugama", "APR: a separate portal with its own services", "", "Simplified view of today's APR site"))
    new = (f'<figure class="shot new"><a href="{base}portal-sr.webp" target="_blank" rel="noopener" lang="sr-Latn">'
           f'<img src="{base}portal-sr.webp" alt="Jedinstveni poreski portal: pregled firme, obaveze i rokovi" width="2160" height="1215"></a>'
           f'<a href="{base}portal-en.webp" target="_blank" rel="noopener" lang="en">'
           f'<img src="{base}portal-en.webp" alt="The single tax portal: business overview, obligations and deadlines" loading="lazy" width="2160" height="1215"></a>'
           f'<figcaption><span class="pa-n">{B("PREDLOG", "PROPOSAL")}{ai}</span>'
           f'{B("Jedinstveni poreski portal: registracija, porezi i obaveze na jednom ekranu", "The single tax portal: registration, taxes and obligations on one screen", "b")}</figcaption></figure>')
    return f'<div class="pa pa-portal">{note}<div class="pa-shots"><div class="shots-old">{olds}</div>{new}</div></div>'
