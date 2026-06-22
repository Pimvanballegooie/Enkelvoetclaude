import json, os

with open('locaties.json', 'r', encoding='utf-8') as f:
    locaties = json.load(f)

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# ─────────────────────────────────────────────
# 1. Organization structured data voor het netwerk
# ─────────────────────────────────────────────
organization_schema = {
    "@context": "https://schema.org",
    "@type": "MedicalOrganization",
    "name": "Enkel Voet Netwerk",
    "alternateName": "EVN Breda",
    "url": "https://enkelvoet.net",
    "logo": "https://enkelvoet.net/EVN_Logo_transparant.png",
    "description": "Het Enkel Voet Netwerk is een samenwerkingsverband van fysiotherapeuten en zorgverleners gespecialiseerd in enkel- en voetklachten in de regio Breda en omgeving.",
    "areaServed": {
        "@type": "AdministrativeArea",
        "name": "Breda en omgeving"
    },
    "medicalSpecialty": "Physiotherapy",
    "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer service",
        "url": "https://enkelvoet.net/contact.html",
        "areaServed": "NL",
        "availableLanguage": "Dutch"
    },
    "sameAs": [
        "https://enkelvoet.net"
    ]
}

# ─────────────────────────────────────────────
# 2. LocalBusiness structured data per locatie
# ─────────────────────────────────────────────
locatie_schemas = []
for loc in locaties:
    adres_delen = loc.get('adres', '').split(',')
    straat = adres_delen[0].strip() if adres_delen else loc.get('adres', '')
    stad = adres_delen[1].strip() if len(adres_delen) > 1 else 'Breda'

    disciplines = loc.get('disciplines', [])
    specialiteiten = []
    if 'Fysiotherapeut' in disciplines:
        specialiteiten.append('Physiotherapy')
    if 'Ergotherapeut' in disciplines:
        specialiteiten.append('OccupationalTherapy')

    schema = {
        "@context": "https://schema.org",
        "@type": "MedicalBusiness",
        "name": loc.get('naam', ''),
        "description": loc.get('beschrijving', ''),
        "url": loc.get('website', ''),
        "telephone": loc.get('telefoon', ''),
        "email": loc.get('email', ''),
        "image": loc.get('logo_url', ''),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": straat,
            "addressLocality": stad,
            "addressCountry": "NL"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": loc.get('lat', ''),
            "longitude": loc.get('lng', '')
        },
        "parentOrganization": {
            "@type": "MedicalOrganization",
            "name": "Enkel Voet Netwerk",
            "url": "https://enkelvoet.net"
        }
    }

    if specialiteiten:
        schema["medicalSpecialty"] = specialiteiten if len(specialiteiten) > 1 else specialiteiten[0]

    locatie_schemas.append(schema)

# ─────────────────────────────────────────────
# 3. Combineer alles in één @graph blok
# ─────────────────────────────────────────────
combined_schema = {
    "@context": "https://schema.org",
    "@graph": [organization_schema] + locatie_schemas
}

schema_tag = f'''<script type="application/ld+json">
{json.dumps(combined_schema, ensure_ascii=False, indent=2)}
</script>'''

# ─────────────────────────────────────────────
# 4. Injecteren in index.html
# ─────────────────────────────────────────────
MARKER_START = '<!-- STRUCTURED_DATA_START -->'
MARKER_END = '<!-- STRUCTURED_DATA_END -->'

if MARKER_START in index_html:
    start = index_html.index(MARKER_START)
    end = index_html.index(MARKER_END) + len(MARKER_END)
    index_html = index_html[:start] + MARKER_START + '\n' + schema_tag + '\n' + MARKER_END + index_html[end:]
    print("OK: structured data bijgewerkt in index.html")
elif '</head>' in index_html:
    schema_block = MARKER_START + '\n' + schema_tag + '\n' + MARKER_END + '\n'
    index_html = index_html.replace('</head>', schema_block + '</head>')
    print("OK: structured data toegevoegd aan index.html")
else:
    print("WAARSCHUWING: </head> niet gevonden in index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print(f"OK: {len(locatie_schemas)} locaties verwerkt in structured data")
