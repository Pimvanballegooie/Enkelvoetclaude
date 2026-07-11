# VindJeFysio Netwerk — enkelvoet.net (Enkel Voet Netwerk)

Deze repo is één "spoke" in een hub-and-spoke netwerk van gespecialiseerde fysiotherapie-subsites. De hub is vindjefysio.net; spokes zijn o.a. rugnek, beenklachten, kansrijkopgroeien, mentaalgezond, chronischezorg, armklachten en deze (enkelvoet).

## Architectuur
- Statische HTML/CSS/vanilla JS op GitHub Pages, custom domein via CNAME.
- Gedeelde Supabase-backend, project islujznszevdynguhjdc, met anon key in de frontend.
- Gedeelde tabellen: therapeuten, praktijken, therapeut_subcategorieen, therapeut_praktijken, subcategorieen, categorieen.
- ⚠️ Deze repo wijkt qua opzet af van de andere spokes: het aanmeldbestand heet `therapeut-worden.html` (niet `therapeut-aanmelden.html`) en er is ook `locatie-worden.html`, `mijn-praktijk.html`, `partners.html`, `beheer.html`, `contact.html`, `faq.html`. Er is een aparte `sync_locaties.py` + `.github/workflows/sync-locaties.yml` die `locaties.json` genereert/synchroniseert, naast de gebruikelijke `sync_protocollen.py` + `.github/workflows/sync-protocollen.yml`. Er is ook een `genereer_structured_data.py` voor JSON-LD SEO-data en een `site-config.json`.
- De homepage (`index.html`) is regionaal opgezet (focus "Regio Breda e.o.") en rendert praktijken/locaties uit `locaties.json` in plaats van (alleen) live Supabase-queries zoals de andere spokes.

## Belangrijke conventies
- therapeut-worden.html (het aanmeldformulier van deze site) linkt ALTIJD relatief/lokaal binnen de eigen subsite (nooit naar vindjefysio.net).
- Praktijk/locatie-aanmelden loopt WEL centraal via vindjefysio.net/aanmelden.html?via=<domein>.
- Mails lopen via info@vindjefysio.net (let op: de beheerpagina in deze repo verstuurt ook zelf mails via Resend vanaf info@enkelvoet.net voor praktijkcode-bevestigingen).
- Therapeut-registratie zet aangemeld_via op het eigen subsite-domein en actief=false (wacht op goedkeuring); bij goedkeuring worden therapeuten hier standaard gekoppeld aan subcategorieën 45 (Enkel en voet), 47 (Revalidatie na operatie), 48 (Voorbereiding op operatie), 49 (Sport, bewegen en overbelasting).
- Deze site: palet navy #1B3A5C, teal #2A9D8F.
- Structuur = geen brede domeinindeling zoals sommige andere spokes, maar een focus op enkel & voet met anatomische protocol-zones (zie `protocollen-config.json`): enkel, achtervoet, middenvoet, voorvoet.

## Sync-pipeline
- sync_protocollen.py haalt protocollen op uit publiek gedeelde Google Docs (export-link, geen API-key), zet markdown om naar HTML, genereert protocollen/<id>-makkelijk.html (patiënt) en -complex.html (therapeut) + protocollen.html + sitemap.xml. De workflow git-add regel is hier breder dan bij de andere spokes: git add protocollen/ protocollen.html sitemap.xml robots.txt index.html.
- sync_locaties.py synchroniseert `locaties.json` (praktijken/locaties voor de homepage-kaart); de workflow git-add regel daarvoor is: git add locaties.json.
- Google Docs moeten op "iedereen met de link kan bekijken" staan.
