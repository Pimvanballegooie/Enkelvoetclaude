import json, urllib.request, re, sys, os
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
            self.text.append('\n')
    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)
    def get_text(self):
        return ' '.join(' '.join(self.text).split())

ZONES = {
    'enkel':      'Enkel',
    'achtervoet': 'Achtervoet',
    'middenvoet': 'Middenvoet',
    'voorvoet':   'Voorvoet',
}

os.makedirs('protocollen', exist_ok=True)
fouten = []
protocol_data = []

for protocol in config['protocollen']:
    protocol_teksten = {}
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
                body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
                with open(bestandsnaam, 'w', encoding='utf-8') as out:
                    out.write(body)
                print(f"OK: {bestandsnaam}")
                extractor = TextExtractor()
                extractor.feed(body)
                protocol_teksten[niveau] = extractor.get_text()[:2000]
            else:
                fouten.append(bestandsnaam)
        except Exception as e:
            fouten.append(f"{bestandsnaam}: {e}")
            print(f"Fout: {bestandsnaam}: {e}")

    protocol_data.append({
        'id': protocol['id'],
        'naam': protocol['naam'],
        'zone': protocol.get('zone', ''),
        'teksten': protocol_teksten
    })

# Genereer protocollen.html
print("Genereer protocollen.html...")

protocol_kaarten = ''
for p in protocol_data:
    zone_id = p['zone']
    zone_naam = ZONES.get(zone_id, zone_id.capitalize())
    tekst = p['teksten'].get('makkelijk', p['teksten'].get('gemiddeld', ''))
    tekst_kort = tekst[:300] + '…' if len(tekst) > 300 else tekst
    tekst_data = tekst[:500].lower().replace('"', '').replace("'", '')

    niveaus_html = ''
    for n in p['teksten'].keys():
        emoji = '📗' if n == 'makkelijk' else '📘' if n == 'gemiddeld' else '📕'
        niveaus_html += f'<a href="index.html" class="niveau-btn niveau-{n}">{emoji} {n.capitalize()}</a>'

    protocol_kaarten += f'''
<div class="protocol-kaart" data-naam="{p['naam'].lower()}" data-zone="{zone_id}" data-tekst="{tekst_data}">
  <div class="protocol-zone-badge">{zone_naam}</div>
  <h2 class="protocol-naam">{p['naam']}</h2>
  <p class="protocol-tekst">{tekst_kort}</p>
  <div class="protocol-niveaus">
    {niveaus_html}
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
    :root {
      --navy: #1B3A5C; --teal: #2A9D8F; --teal-light: #E8F5F4;
      --grey-bg: #F5F7FA; --grey-border: #DDE3EC;
      --text: #1A1A2E; --text-muted: #6B7A99; --white: #FFFFFF;
    }
    html { scroll-behavior: smooth; }
    body { font-family: "Inter", sans-serif; font-size: 16px; color: var(--text); background: var(--grey-bg); line-height: 1.6; }
    header { background: var(--navy); position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 12px rgba(0,0,0,0.15); }
    .header-inner { max-width: 1100px; margin: 0 auto; padding: 0 24px; display: flex; align-items: center; justify-content: space-between; height: 68px; }
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
    .filter-wrap { max-width: 1100px; margin: 32px auto 0; padding: 0 24px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
    .filter-label { font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-right: 4px; }
    .zone-btn { padding: 6px 16px; border-radius: 999px; border: 2px solid var(--grey-border); background: var(--white); color: var(--text-muted); font-size: 0.82rem; font-weight: 600; cursor: pointer; transition: all 0.2s; }
    .zone-btn:hover, .zone-btn.actief { background: var(--navy); border-color: var(--navy); color: var(--white); }
    .container { max-width: 1100px; margin: 32px auto 64px; padding: 0 24px; }
    .resultaat-info { font-size: 0.85rem; color: var(--text-muted); margin-bottom: 20px; }
    .protocollen-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }
    .protocol-kaart { background: var(--white); border: 1px solid var(--grey-border); border-radius: 14px; padding: 24px; transition: box-shadow 0.2s, transform 0.2s; }
    .protocol-kaart:hover { box-shadow: 0 4px 20px rgba(27,58,92,0.10); transform: translateY(-2px); }
    .protocol-kaart.verborgen { display: none; }
    .protocol-zone-badge { display: inline-block; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--teal); background: var(--teal-light); padding: 2px 10px; border-radius: 999px; margin-bottom: 10px; }
    .protocol-naam { font-size: 1.05rem; font-weight: 700; color: var(--navy); margin-bottom: 10px; line-height: 1.3; }
    .protocol-tekst { font-size: 0.85rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 16px; }
    .protocol-niveaus { display: flex; gap: 8px; flex-wrap: wrap; padding-top: 14px; border-top: 1px solid var(--grey-border); }
    .niveau-btn { padding: 6px 14px; border-radius: 6px; font-size: 0.78rem; font-weight: 600; text-decoration: none; transition: all 0.15s; cursor: pointer; border: none; display: inline-block; }
    .niveau-makkelijk { background: #EAF7F0; color: #1E8449; }
    .niveau-makkelijk:hover { background: #1E8449; color: white; }
    .niveau-gemiddeld { background: #FEF9E7; color: #B7770D; }
    .niveau-gemiddeld:hover { background: #B7770D; color: white; }
    .niveau-complex { background: #EAF0FB; color: #1A5276; }
    .niveau-complex:hover { background: #1A5276; color: white; }
    .geen-resultaten { text-align: center; padding: 64px 24px; color: var(--text-muted); display: none; }
    .geen-resultaten .icon { font-size: 3rem; margin-bottom: 12px; }
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
      <a href="index.html#protocollen">Protocollen</a>
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
      <button onclick="zoek()">Zoeken</button>
    </div>
  </div>
</div>
<div class="filter-wrap">
  <span class="filter-label">Zone:</span>
  <button class="zone-btn actief" onclick="filterZone(this, 'alle')">Alle zones</button>
  <button class="zone-btn" onclick="filterZone(this, 'enkel')">Enkel</button>
  <button class="zone-btn" onclick="filterZone(this, 'achtervoet')">Achtervoet</button>
  <button class="zone-btn" onclick="filterZone(this, 'middenvoet')">Middenvoet</button>
  <button class="zone-btn" onclick="filterZone(this, 'voorvoet')">Voorvoet</button>
</div>
<div class="container">
  <div class="resultaat-info" id="resultaat-info"></div>
  <div class="protocollen-grid" id="protocollen-grid">
    PROTOCOL_KAARTEN
  </div>
  <div class="geen-resultaten" id="geen-resultaten">
    <div class="icon">Geen resultaten</div>
    <div>Geen protocollen gevonden voor deze zoekopdracht.</div>
  </div>
</div>
<footer>
  <p>2025 Enkel Voet Netwerk Breda e.o. - <a href="index.html">Terug naar home</a></p>
</footer>
<script>
  let actieveZone = "alle";
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
    print(f"WAARSCHUWING: {len(fouten)} fouten maar doorgaan")
