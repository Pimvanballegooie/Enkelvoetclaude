import json, urllib.request, urllib.parse, os, time, csv, io

SHEET_ID = os.environ.get("SHEET_ID", "")
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=30) as resp:
    csv_data = resp.read().decode("utf-8")

reader = csv.DictReader(io.StringIO(csv_data))

def geocodeer(adres):
    try:
        q = urllib.parse.quote(adres + ", Nederland")
        u = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=1"
        r = urllib.request.Request(u, headers={"User-Agent": "EVN/1.0"})
        with urllib.request.urlopen(r, timeout=10) as resp:
            res = json.loads(resp.read())
        if res:
            return float(res[0]["lat"]), float(res[0]["lon"])
    except Exception as e:
        print(f"Geocoding fout: {e}")
    return None, None

locaties = []
cache = {}

for rij in reader:
    if rij.get("Status", "").strip() != "Goedgekeurd":
        continue
    tier  = rij.get("Tier", "basis").lower().strip()
    naam  = rij.get("Praktijknaam", "").strip()
    adres = rij.get("Adres", "").strip()
    if not naam or not adres:
        continue
    if adres not in cache:
        cache[adres] = geocodeer(adres)
        time.sleep(1)
    lat, lng = cache[adres]
    if not lat:
        print(f"Geen coordinaten: {adres}")
        continue
    locaties.append({
        "naam": naam,
        "adres": adres,
        "website": rij.get("Website", "").strip(),
        "telefoon": rij.get("Telefoon locatie", "").strip(),
        "email": rij.get("E-mail locatie", "").strip(),
        "disciplines": [d.strip() for d in rij.get("Disciplines", "").split(",") if d.strip()],
        "tier": tier,
        "beschrijving": rij.get("Beschrijving", "").strip() if tier in ["plus", "partner"] else "",
        "logo_url": rij.get("Logo URL", "").strip() if tier == "partner" else "",
        "lat": lat,
        "lng": lng
    })
    print(f"OK: {naam} ({tier})")

locaties.sort(key=lambda l: {"partner": 0, "plus": 1, "basis": 2}.get(l["tier"], 3))

with open("locaties.json", "w", encoding="utf-8") as f:
    json.dump(locaties, f, ensure_ascii=False, indent=2)

print(f"Klaar: {len(locaties)} locaties opgeslagen")
