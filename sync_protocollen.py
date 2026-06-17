import json, urllib.request, urllib.parse, re, sys, os
from html.parser import HTMLParser

with open('protocollen-config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ('style', 'script'):
            self.skip = True
    def handle_endtag(self, tag):
        if tag in ('style', 'script'):
            self.skip = False
        if tag in ('p', 'li', 'h1', 'h2', 'h3', 'br', 'tr'):
            self.text.append(' ')
    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)
    def get_text(self):
        return ' '.join(' '.join(self.text).split())

def opschonen_html(body):
    """Schoon Google Docs HTML op naar leesbare HTML"""
    # Verwijder style en script tags
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    # Verwijder afbeeldingen en figure tags
    body = re.sub(r'<img[^>]*/?>', '', body)
    body = re.sub(r'<figure[^>]*>.*?</figure>', '', body, flags=re.DOTALL)

    # FIX: Google redirect URLs omzetten naar echte URLs
    def ontgoogle(match):
        href = match.group(1)
        if 'google.com/url' in href:
            href = href.replace('&amp;', '&')
            parsed = urllib.parse.urlparse(href)
            params = urllib.parse.parse_qs(parsed.query)
            echte_url = params.get('q', [href])[0]
            return f'href="{echte_url}"'
        return match.group(0)
    body = re.sub(r'href="([^"]*)"', ontgoogle, body)

    # Verwijder inline stijlen, classes, ids
    body = re.sub(r' style="[^"]*"', '', body)
    body = re.sub(r' class="[^"]*"', '', body)
    body = re.sub(r' id="[^"]*"', '', body)
    body = re.sub(r'<hr[^>]*>', '<hr>', body)
    body = re.sub(r'\n{3,}', '\n\n', body)

    # FIX: fysioefeningen.nl links EERST omzetten naar knoppen, dan pas spans opruimen
    # (anders worden de linkteksten in <span> tags weggegooid voor we ze kunnen gebruiken)
    # Gebruik de linktekst uit het doc als naam (niet de URL-slug)
    def maak_knop_van_link(match):
        url = match.group(1)
        linktekst = re.sub(r'<[^>]+>', '', match.group(2)).strip()
        # Verwijder emoji als die al in de linktekst zit (bij dubbele sync runs)
        linktekst = linktekst.replace('\U0001f4f9', '').replace('&#128249;', '').strip()
        naam = linktekst if linktekst and not linktekst.startswith('http') else \
               url.replace('https://www.fysioefeningen.nl/', '') \
                  .replace('https://fysioefeningen.nl/', '') \
                  .replace('-', ' ').strip().capitalize()
        return (
            '<a href="' + url + '" target="_blank" rel="noopener" '
            'style="display:inline-flex;align-items:center;gap:8px;margin:6px 0;padding:10px 18px;'
            'background:#E8F5F4;color:#2A9D8F;border:2px solid #2A9D8F;border-radius:8px;'
            'font-size:0.875rem;font-weight:600;text-decoration:none;">&#128249; ' + naam + '</a>'
        )

    body = re.sub(
        r'<a href="(https?://(?:www\.)?fysioefeningen\.nl/[^"]+)"[^>]*>(.*?)</a>',
        maak_knop_van_link,
        body,
        flags=re.DOTALL
    )

    # Nu pas spans opruimen (na knop-conversie zodat linkteksten behouden blijven)
    body = re.sub(r'<span>\s*</span>', '', body)
    body = re.sub(r'<span>(.*?)</span>', r'\1', body)
    body = re.sub(r'<p>\s*</p>', '', body)
    body = re.sub(r'<div>\s*</div>', '', body)

    # Vervang [VIDEO: Naam | URL] patronen door knoppen in de tekst
    def maak_video_knop(match):
        naam = match.group(1).strip()
        url = match.group(2).strip()
        return (
            '<a href="' + url + '" target="_blank" rel="noopener" '
            'style="display:inline-flex;align-items:center;gap:6px;margin:4px 0;padding:6px 14px;'
            'background:#E8F5F4;color:#2A9D8F;border:1.5px solid #2A9D8F;border-radius:6px;'
            'font-size:0.8rem;font-weight:600;text-decoration:none;">📹 ' + naam + '</a>'
        )
    body = re.sub(r'\[VIDEO:\s*([^|\]]+)\|\s*(https?://[^\]]+)\]', maak_video_knop, body)

    # Verwijder losse fysioefeningen URLs als platte tekst (backup)
    body = re.sub(r'https?://(?:www\.)?fysioefeningen\.nl/[^\s<>"\']+', '', body)

    return body.strip()

def extraheer_preview(body, max_alineas=3):
    """Haal eerste alineas op als opgeschoonde HTML"""
    body = opschonen_html(body)
    blokken = re.findall(r'<(p|h1|h2|h3)[^>]*>.*?</\1>', body, re.DOTALL | re.IGNORECASE)
    blokken = [b for b in blokken if len(re.sub(r'<[^>]+>', '', b).strip()) > 10]
    return '\n'.join(blokken[:max_alineas])

def extraheer_oefenfilmpjes_ruw(rauwe_html_niveaus):
    """Zoek [VIDEO: Naam | URL] patronen in ruwe HTML, dedupliceer op URL"""
    gezien = set()
    links = []
    for rauwe_html in rauwe_html_niveaus:
        # Strip HTML tags zodat we platte tekst hebben
        tekst = re.sub(r'<[^>]+>', ' ', rauwe_html)
        tekst = re.sub(r'\s+', ' ', tekst)
        # Zoek [VIDEO: Naam | URL]
        gevonden = re.findall(r'\[VIDEO:\s*([^|\]]+)\|\s*(https?://[^\]]+)\]', tekst)
        for naam, url in gevonden:
            naam = naam.strip()
            url = url.strip()
            if url not in gezien:
                gezien.add(url)
                links.append((url, naam))
    return links

ZONES = {
    'enkel': 'Enkel',
    'achtervoet': 'Achtervoet',
    'middenvoet': 'Middenvoet',
    'voorvoet': 'Voorvoet',
}

os.makedirs('protocollen', exist_ok=True)
fouten = []
protocol_data = []

for protocol in config['protocollen']:
    protocol_teksten = {}
    protocol_previews = {}
    protocol_volledige_html = {}
    protocol_ruwe_html = {}  # voor oefenfilmpjes extractie

    for niveau, doc_id in protocol['niveaus'].items():
        if not doc_id or doc_id == 'INVULLEN':
            print(f"Overgeslagen: {protocol['id']} - {niveau}")
            continue
        url = f"https://docs.google.com/document/d/{doc_id}/export?format=html"
        bestandsnaam = f"protocollen/{protocol['id']}-{niveau}.html"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                html = resp.read().decode('utf-8')
            body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
            if body_match:
                body = body_match.group(1)
                body_schoon = opschonen_html(body)
                with open(bestandsnaam, 'w', encoding='utf-8') as out:
                    out.write(body_schoon)
                print(f"OK: {bestandsnaam}")
                extractor = TextExtractor()
                extractor.feed(body_schoon)
                protocol_teksten[niveau] = extractor.get_text()[:2000]
                protocol_previews[niveau] = extraheer_preview(body, max_alineas=3)
                protocol_volledige_html[niveau] = body_schoon
                protocol_ruwe_html[niveau] = body  # bewaar ruwe HTML voor filmpjes
            else:
                fouten.append(bestandsnaam)
        except Exception as e:
            fouten.append(f"{bestandsnaam}: {e}")
            print(f"Fout: {bestandsnaam}: {e}")

    protocol_data.append({
        'id': protocol['id'],
        'naam': protocol['naam'],
        'zone': protocol.get('zone', ''),
        'teksten': protocol_teksten,
        'previews': protocol_previews,
        'volledige_html': protocol_volledige_html,
        'ruwe_html': protocol_ruwe_html
    })

print("Genereer protocollen.html...")

protocol_kaarten = ''
for p in protocol_data:
    zone_id = p['zone']
    zone_naam = ZONES.get(zone_id, zone_id.capitalize())
    preview_html = p['previews'].get('makkelijk', p['previews'].get('gemiddeld', '<p>Geen preview beschikbaar.</p>'))
    tekst_data = p['teksten'].get('makkelijk', p['teksten'].get('gemiddeld', ''))
    tekst_data = tekst_data[:500].lower().replace('"', '').replace("'", '')

    import json as jsonlib
    volledige_json = jsonlib.dumps(p['volledige_html'])

    niveau_labels = {'makkelijk': 'Makkelijk', 'gemiddeld': 'Gemiddeld', 'complex': 'Complex'}
    niveau_emojis = {'makkelijk': '📗', 'gemiddeld': '📘', 'complex': '📕'}

    niveaus_html = ''
    for n in p['teksten'].keys():
        emoji = niveau_emojis.get(n, '')
        label = niveau_labels.get(n, n.capitalize())
        niveaus_html += f'<button class="niveau-btn niveau-{n}" onclick="openProtocol(\'{p["id"]}\', \'{n}\')">{emoji} {label}</button>\n'

    # FIX: zoek oefenfilmpjes in ALLE niveaus, niet alleen makkelijk
    oefenfilmpjes_html = ''
    links = extraheer_oefenfilmpjes_ruw(list(p['ruwe_html'].values()))
    if links:
        # Max 4 links tonen (2 rijen van 2), grid-class aanpassen op aantal
        links_tonen = links[:4]
        grid_class = "oefenfilmpjes-grid" if len(links_tonen) > 1 else "oefenfilmpjes-grid enkelvoudig"
        oefenfilmpjes_html = f'<div class="oefenfilmpjes-zijbalk"><div class="oefenfilmpjes-titel">📹 Oefenfilmpjes</div><div class="{grid_class}">'
        for url, naam in links_tonen:
            # Gebruik slug als naam leeg of URL is
            if not naam or naam.startswith('http'):
                naam = slug_naar_naam(url)
            naam_kort = naam[:18] + '…' if len(naam) > 18 else naam
            oefenfilmpjes_html += f'<a href="{url}" target="_blank" rel="noopener" class="oefenfilmpje-knop" title="{naam}">{naam_kort}</a>'
        oefenfilmpjes_html += '</div><p class="oefenfilmpjes-disclaimer">Begeleiding van een therapeut is noodzakelijk.</p>'
        oefenfilmpjes_html += '</div>'

    protocol_kaarten += f'''<div class="protocol-kaart" id="kaart-{p['id']}" data-naam="{p['naam'].lower()}" data-zone="{zone_id}" data-tekst="{tekst_data}" data-html="{volledige_json.replace('"', '&quot;')}">
  <div class="kaart-top">
    <div class="kaart-links">
      <div class="protocol-zone-badge">{zone_naam}</div>
      <h2 class="protocol-naam">{p['naam']}</h2>
      <div class="protocol-preview">{preview_html}</div>
      <div class="protocol-niveaus">
        {niveaus_html}
      </div>
    </div>
    {oefenfilmpjes_html}
  </div>
  <div class="protocol-viewer" id="viewer-{p['id']}" style="display:none">
    <div class="viewer-header">
      <span id="viewer-titel-{p['id']}"></span>
      <button onclick="sluitProtocol('{p['id']}')" style="background:none;border:none;cursor:pointer;font-size:1.2rem;color:var(--text-muted)">✕</button>
    </div>
    <div class="viewer-inhoud" id="viewer-inhoud-{p['id']}"></div>
  </div>
</div>'''

html_pagina = '''<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Alle behandelprotocollen enkel & voet - Enkel Voet Netwerk Breda</title>
  <meta name="description" content="Overzicht van alle behandelprotocollen voor enkel en voet aandoeningen. Enkelverzwikking, achillespees, slijtage, hielspoor en meer. Fysiotherapie Breda." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root { --navy: #1B3A5C; --teal: #2A9D8F; --teal-light: #E8F5F4; --grey-bg: #F5F7FA; --grey-border: #DDE3EC; --text: #1A1A2E; --text-muted: #6B7A99; --white: #FFFFFF; }
    html { scroll-behavior: smooth; }
    body { font-family: "Inter", sans-serif; font-size: 16px; color: var(--text); background: var(--grey-bg); line-height: 1.6; }
    header { background: var(--navy); position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 12px rgba(0,0,0,0.15); }
    .header-inner { max-width: 1200px; margin: 0 auto; padding: 0 clamp(1rem, 4vw, 3rem); display: flex; align-items: center; justify-content: space-between; height: 68px; }
    .logo { display: flex; align-items: center; gap: 12px; text-decoration: none; }
    .logo-icon { width: 40px; height: 40px; }
    .logo-text { color: var(--white); font-weight: 700; font-size: 1.05rem; line-height: 1.2; }
    .logo-text span { display: block; font-weight: 300; font-size: 0.75rem; opacity: 0.7; }
    nav { display: flex; gap: 6px; }
    nav a { color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.875rem; font-weight: 500; padding: 8px 14px; border-radius: 6px; transition: background 0.2s; }
    nav a:hover { background: rgba(255,255,255,0.12); color: var(--white); }
    nav a.cta { background: var(--teal); color: var(--white); margin-left: 8px; }
    .hero { background: linear-gradient(135deg, var(--navy) 0%, #2A4A73 100%); color: var(--white); padding: 56px 24px 48px; text-align: center; }
    .hero h1 { font-size: clamp(1.8rem, 4vw, 2.4rem); font-weight: 700; margin-bottom: 12px; letter-spacing: -0.02em; }
    .hero h1 em { font-style: normal; color: #7FDED5; }
    .hero p { opacity: 0.85; max-width: 560px; margin: 0 auto 28px; font-size: 0.95rem; }
    .zoekbalk-wrap { max-width: 600px; margin: 0 auto; }
    .zoekbalk { display: flex; background: var(--white); border-radius: 10px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.15); }
    .zoekbalk input { flex: 1; padding: 14px 20px; border: none; outline: none; font-family: inherit; font-size: 1rem; color: var(--text); }
    .zoekbalk button { padding: 14px 24px; background: var(--teal); color: white; border: none; cursor: pointer; font-weight: 700; font-size: 0.9rem; transition: background 0.2s; }
    .zoekbalk button:hover { background: #238a7e; }
    .filter-wrap { max-width: 1200px; margin: 32px auto 0; padding: 0 clamp(1rem, 4vw, 3rem); display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
    .filter-label { font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-right: 4px; }
    .zone-btn { padding: 6px 16px; border-radius: 999px; border: 2px solid var(--grey-border); background: var(--white); color: var(--text-muted); font-size: 0.82rem; font-weight: 600; cursor: pointer; transition: all 0.2s; }
    .zone-btn:hover, .zone-btn.actief { background: var(--navy); border-color: var(--navy); color: var(--white); }
    .container { max-width: 1200px; margin: 32px auto 64px; padding: 0 clamp(1rem, 4vw, 3rem); }
    .resultaat-info { font-size: 0.85rem; color: var(--text-muted); margin-bottom: 20px; }
    .protocollen-grid { display: flex; flex-direction: column; gap: 16px; }
    .protocol-kaart { background: var(--white); border: 1px solid var(--grey-border); border-radius: 14px; padding: 28px 32px; transition: box-shadow 0.2s; display: flex; flex-direction: column; }
    .protocol-kaart:hover { box-shadow: 0 4px 20px rgba(27,58,92,0.10); }
    .protocol-kaart.verborgen { display: none; }
    .kaart-top { display: flex; gap: 24px; align-items: flex-start; }
    .kaart-links { flex: 1; }
    .oefenfilmpjes-zijbalk { width: 180px; flex-shrink: 0; background: var(--teal-light); border-radius: 10px; padding: 12px; box-sizing: border-box; }
    .oefenfilmpjes-titel { font-size: 0.72rem; font-weight: 700; color: var(--teal); margin-bottom: 6px; }
    .oefenfilmpjes-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; width: 100%; }
    .oefenfilmpjes-grid.enkelvoudig { grid-template-columns: 1fr; }
    .oefenfilmpje-knop { display: flex; align-items: center; justify-content: center; text-align: center; padding: 4px 6px; background: white; color: var(--teal); border: 1.5px solid var(--teal); border-radius: 5px; font-size: 0.65rem; font-weight: 600; text-decoration: none; transition: all 0.2s; line-height: 1.25; min-height: 32px; word-break: break-word; hyphens: auto; }
    .oefenfilmpje-knop:hover { background: var(--teal); color: white; }
    .oefenfilmpjes-disclaimer { font-size: 0.62rem; color: var(--text-muted); margin-top: 6px; line-height: 1.3; font-style: italic; }
    @media (max-width: 700px) { .kaart-top { flex-direction: column; } .oefenfilmpjes-zijbalk { width: 100%; margin-top: 12px; } .oefenfilmpjes-grid { grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); } }
    .protocol-zone-badge { display: inline-block; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--teal); background: var(--teal-light); padding: 2px 10px; border-radius: 999px; margin-bottom: 10px; }
    .protocol-naam { font-size: 1.05rem; font-weight: 700; color: var(--navy); margin-bottom: 12px; line-height: 1.3; }
    .protocol-preview { font-size: 0.85rem; color: var(--text-muted); line-height: 1.65; margin-bottom: 16px; flex: 1; overflow: hidden; max-height: 120px; position: relative; }
    .protocol-preview::after { content: ""; position: absolute; bottom: 0; left: 0; right: 0; height: 40px; background: linear-gradient(transparent, white); }
    .protocol-preview h1, .protocol-preview h2, .protocol-preview h3 { color: var(--navy); font-size: 0.88rem; font-weight: 700; margin-bottom: 4px; margin-top: 8px; }
    .protocol-preview p { margin-bottom: 6px; }
    .protocol-niveaus { display: flex; gap: 8px; flex-wrap: wrap; padding-top: 14px; border-top: 1px solid var(--grey-border); margin-top: auto; }
    .niveau-btn { padding: 6px 14px; border-radius: 6px; font-size: 0.78rem; font-weight: 600; transition: all 0.15s; cursor: pointer; border: none; display: inline-block; }
    .niveau-makkelijk { background: #EAF7F0; color: #1E8449; }
    .niveau-makkelijk:hover { background: #1E8449; color: white; }
    .niveau-gemiddeld { background: #FEF9E7; color: #B7770D; }
    .niveau-gemiddeld:hover { background: #B7770D; color: white; }
    .niveau-complex { background: #EAF0FB; color: #1A5276; }
    .niveau-complex:hover { background: #1A5276; color: white; }
    .protocol-viewer { margin-top: 20px; border-top: 2px solid var(--teal); padding-top: 16px; }
    .viewer-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
    .viewer-header span { font-size: 0.85rem; font-weight: 700; color: var(--teal); }
    .viewer-inhoud { font-size: 0.9rem; line-height: 1.75; color: var(--text); padding-right: 8px; }
    .viewer-inhoud h1 { font-size: 1.2rem; font-weight: 700; color: var(--navy); margin: 1em 0 0.5em; }
    .viewer-inhoud h2 { font-size: 1rem; font-weight: 700; color: var(--navy); margin: 1em 0 0.4em; }
    .viewer-inhoud h3 { font-size: 0.9rem; font-weight: 700; color: var(--navy); margin: 0.8em 0 0.3em; }
    .viewer-inhoud p { margin-bottom: 0.8em; }
    .viewer-inhoud ul, .viewer-inhoud ol { margin: 0.4em 0 0.8em 1.5em; }
    .viewer-inhoud li { margin-bottom: 0.3em; }
    .viewer-inhoud table { width: 100%; border-collapse: collapse; margin: 1em 0; font-size: 0.85rem; }
    .viewer-inhoud td, .viewer-inhoud th { border: 1px solid var(--grey-border); padding: 6px 10px; text-align: left; }
    .viewer-inhoud th { background: var(--grey-bg); font-weight: 600; }
    .geen-resultaten { text-align: center; padding: 64px 24px; color: var(--text-muted); display: none; }
    footer { background: #0F2340; color: rgba(255,255,255,0.5); text-align: center; padding: 28px 24px; font-size: 0.82rem; }
    footer a { color: rgba(255,255,255,0.7); text-decoration: none; }
    @media (max-width: 700px) { nav { display: none; } .protocollen-grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
<header>
  <div class="header-inner">
    <a href="index.html" class="logo">
      <img class="logo-icon" src="EVN_Logo_transparant.png" alt="EVN Logo" />
      <div class="logo-text">Enkel Voet Netwerk<span>Breda e.o.</span></div>
    </a>
    <nav>
      <a href="protocollen.html">Protocollen</a>
      <a href="index.html#locaties">Locaties</a>
      <a href="partners.html">Partners</a>
      <a href="therapeut-worden.html">Aanmelden als therapeut</a>
      <a href="locatie-worden.html" class="cta">Locatie worden</a>
    </nav>
  </div>
</header>
<div class="hero">
  <h1>Alle behandelprotocollen<br><em>enkel & voet</em></h1>
  <p>Zoek op aandoening, klacht of behandeling. Beschikbaar op drie leesniveaus.</p>
  <div class="zoekbalk-wrap">
    <div class="zoekbalk">
      <input type="text" id="zoek-input" placeholder="Zoek bijv. enkelverzwikking, achillespees, slijtage..." oninput="zoek()" />
      <button onclick="zoek()">🔍 Zoeken</button>
    </div>
  </div>
</div>
<div class="filter-wrap">
  <span class="filter-label">Zone:</span>
  <button class="zone-btn actief" onclick="filterZone(this, \'alle\')">Alle zones</button>
  <button class="zone-btn" onclick="filterZone(this, \'enkel\')">🦵 Enkel</button>
  <button class="zone-btn" onclick="filterZone(this, \'achtervoet\')">🦶 Achtervoet</button>
  <button class="zone-btn" onclick="filterZone(this, \'middenvoet\')">👣 Middenvoet</button>
  <button class="zone-btn" onclick="filterZone(this, \'voorvoet\')">👣 Voorvoet</button>
</div>
<div class="container">
  <div class="resultaat-info" id="resultaat-info"></div>
  <div class="protocollen-grid" id="protocollen-grid">
    PROTOCOL_KAARTEN
  </div>
  <div class="geen-resultaten" id="geen-resultaten">
    <div style="font-size:3rem;margin-bottom:12px">🔍</div>
    <div>Geen protocollen gevonden voor deze zoekopdracht.</div>
  </div>
</div>
<footer>
  <p>2025 Enkel Voet Netwerk Breda e.o. &nbsp;·&nbsp; <a href="index.html">Terug naar home</a></p>
</footer>
<script>
  let actieveZone = "alle";
  function openProtocol(id, niveau) {
    const kaart = document.getElementById("kaart-" + id);
    const viewer = document.getElementById("viewer-" + id);
    const inhoud = document.getElementById("viewer-inhoud-" + id);
    const titel = document.getElementById("viewer-titel-" + id);
    const niveauLabels = {makkelijk: "📗 Makkelijk", gemiddeld: "📘 Gemiddeld", complex: "📕 Complex"};
    document.querySelectorAll(".protocol-viewer").forEach(v => {
      if (v.id !== "viewer-" + id) v.style.display = "none";
    });
    try {
      const htmlData = JSON.parse(kaart.dataset.html.replace(/&quot;/g, \'"\'));
      const html = htmlData[niveau] || "<p>Dit niveau is nog niet beschikbaar.</p>";
      inhoud.innerHTML = html;
      titel.textContent = niveauLabels[niveau] || niveau;
      viewer.style.display = "block";
      viewer.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } catch(e) {
      inhoud.innerHTML = "<p>Protocol kon niet worden geladen.</p>";
      viewer.style.display = "block";
    }
  }
  function sluitProtocol(id) {
    document.getElementById("viewer-" + id).style.display = "none";
  }
  function normaliseer(t) { return t.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); }
  function zoek() {
    const zoekterm = normaliseer(document.getElementById("zoek-input").value);
    const kaarten = document.querySelectorAll(".protocol-kaart");
    let zichtbaar = 0;
    kaarten.forEach(k => {
      const naam = normaliseer(k.dataset.naam);
      const tekst = normaliseer(k.dataset.tekst);
      const zoneMatch = actieveZone === "alle" || k.dataset.zone === actieveZone;
      const zoekMatch = !zoekterm || naam.includes(zoekterm) || tekst.includes(zoekterm);
      k.classList.toggle("verborgen", !(zoneMatch && zoekMatch));
      if (zoneMatch && zoekMatch) zichtbaar++;
    });
    document.getElementById("resultaat-info").textContent = zoekterm || actieveZone !== "alle" ? zichtbaar + " protocollen gevonden" : "";
    document.getElementById("geen-resultaten").style.display = zichtbaar === 0 ? "block" : "none";
  }
  function filterZone(btn, zone) {
    actieveZone = zone;
    document.querySelectorAll(".zone-btn").forEach(b => b.classList.remove("actief"));
    btn.classList.add("actief");
    zoek();
  }
</script>
</body>
</html>'''

html_pagina = html_pagina.replace('PROTOCOL_KAARTEN', protocol_kaarten)

with open('protocollen.html', 'w', encoding='utf-8') as f:
    f.write(html_pagina)
print(f"OK: protocollen.html gegenereerd met {len(protocol_data)} protocollen")

if fouten:
    print(f"WAARSCHUWING: {len(fouten)} fouten")
