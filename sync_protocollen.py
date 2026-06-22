import json, urllib.request, urllib.parse, re, os
from html.parser import HTMLParser
from datetime import date

with open('protocollen-config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

with open('locaties.json', 'r', encoding='utf-8') as f:
    locaties = json.load(f)

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Locatie worden – Enkel Voet Netwerk Breda e.o.</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --navy: #1B3A5C; --teal: #2A9D8F; --teal-light: #E8F5F4;
      --grey-bg: #F5F7FA; --grey-border: #DDE3EC;
      --text: #1A1A2E; --text-muted: #6B7A99; --white: #FFFFFF;
      --gold: #C9940A; --gold-light: #FEF9E7;
      --radius: 10px; --shadow: 0 2px 16px rgba(27,58,92,0.08);
    }
    html { scroll-behavior: smooth; }
    body { font-family: 'Inter', sans-serif; font-size: 16px; color: var(--text); background: var(--white); line-height: 1.6; }

    header { background: var(--navy); position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 12px rgba(0,0,0,0.15); }
    .header-inner { max-width: 1100px; margin: 0 auto; padding: 0 24px; display: flex; align-items: center; justify-content: space-between; height: 68px; }
    .logo { display: flex; align-items: center; gap: 12px; text-decoration: none; }
    .logo-icon { width: 40px; height: 40px; }
    .logo-text { color: var(--white); font-weight: 700; font-size: 1.05rem; line-height: 1.2; }
    .logo-text span { display: block; font-weight: 300; font-size: 0.75rem; opacity: 0.7; letter-spacing: 0.04em; }
    nav { display: flex; gap: 6px; }
    nav a { color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.875rem; font-weight: 500; padding: 8px 14px; border-radius: 6px; transition: background 0.2s, color 0.2s; }
    nav a:hover { background: rgba(255,255,255,0.12); color: var(--white); }
    nav a.cta { background: var(--teal); color: var(--white); margin-left: 8px; }
    nav a.cta:hover { background: #238a7e; }
    .hamburger { display: none; flex-direction: column; gap: 5px; cursor: pointer; padding: 4px; }
    .hamburger span { display: block; width: 24px; height: 2px; background: var(--white); border-radius: 2px; }

    .hero { background: linear-gradient(135deg, var(--navy) 0%, #2A4A73 100%); color: var(--white); padding: 72px 24px 0; text-align: center; position: relative; }
    .hero-inner { max-width: 640px; margin: 0 auto; position: relative; padding-bottom: 72px; }
    .hero-wave { display: block; width: 100%; height: 60px; }
    .hero-badge { display: inline-block; background: rgba(42,157,143,0.25); border: 1px solid rgba(42,157,143,0.5); color: #7FDED5; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; padding: 5px 14px; border-radius: 999px; margin-bottom: 20px; }
    .hero h1 { font-size: clamp(1.8rem, 4.5vw, 2.6rem); font-weight: 700; line-height: 1.15; margin-bottom: 16px; letter-spacing: -0.02em; }
    .hero h1 em { font-style: normal; color: #7FDED5; }
    .hero p { font-size: 1rem; opacity: 0.85; max-width: 520px; margin: 0 auto; line-height: 1.7; }

    section { padding: 64px 24px; }
    .section-inner { max-width: 1100px; margin: 0 auto; }
    .section-eyebrow { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--teal); margin-bottom: 10px; }
    .section-header { margin-bottom: 40px; }
    .section-header h2 { font-size: clamp(1.5rem, 3vw, 2rem); font-weight: 700; color: var(--navy); letter-spacing: -0.02em; }
    .section-header p { margin-top: 10px; color: var(--text-muted); max-width: 520px; font-size: 0.95rem; }

    .tiers { background: var(--grey-bg); }
    .tier-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
    .tier-card { background: var(--white); border: 2px solid var(--grey-border); border-radius: 16px; padding: 28px 24px; cursor: pointer; transition: all 0.2s; position: relative; }
    .tier-card:hover { border-color: var(--teal); box-shadow: var(--shadow); transform: translateY(-2px); }
    .tier-card.geselecteerd { border-color: var(--teal); box-shadow: 0 0 0 3px rgba(42,157,143,0.15); }
    .tier-card.geselecteerd.partner { border-color: var(--gold); box-shadow: 0 0 0 3px rgba(201,148,10,0.15); }
    .tier-badge { display: inline-block; font-size: 0.7rem; font-weight: 700; padding: 3px 10px; border-radius: 999px; margin-bottom: 14px; text-transform: uppercase; letter-spacing: 0.06em; }
    .tier-badge.basis   { background: var(--teal-light); color: var(--teal); }
    .tier-badge.plus    { background: #EAF0FB; color: #1A5276; }
    .tier-badge.partner { background: var(--gold-light); color: var(--gold); }
    .tier-card h3 { font-size: 1.1rem; font-weight: 700; color: var(--navy); margin-bottom: 10px; }
    .tier-features { list-style: none; margin-top: 16px; display: flex; flex-direction: column; gap: 8px; }
    .tier-features li { font-size: 0.875rem; color: var(--text-muted); display: flex; align-items: flex-start; gap: 8px; }
    .tier-features li::before { content: '✓'; color: var(--teal); font-weight: 700; flex-shrink: 0; margin-top: 1px; }
    .tier-features li.nee { color: #BCC5D3; }
    .tier-features li.nee::before { content: '–'; color: #BCC5D3; }
    .tier-card.partner .tier-features li::before { color: var(--gold); }
    .tier-check { position: absolute; top: 16px; right: 16px; width: 22px; height: 22px; border-radius: 50%; border: 2px solid var(--grey-border); display: flex; align-items: center; justify-content: center; transition: all 0.2s; }
    .tier-card.geselecteerd .tier-check { background: var(--teal); border-color: var(--teal); color: var(--white); font-size: 0.7rem; }
    .tier-card.geselecteerd.partner .tier-check { background: var(--gold); border-color: var(--gold); }
    .partner-label { background: linear-gradient(135deg, var(--gold), #E8A800); color: var(--white); font-size: 0.65rem; font-weight: 700; padding: 2px 8px; border-radius: 999px; position: absolute; top: -10px; left: 50%; transform: translateX(-50%); white-space: nowrap; letter-spacing: 0.05em; }

    .formulier { background: var(--white); }
    .form-wrap { max-width: 720px; }
    .form-section { background: var(--grey-bg); border: 1px solid var(--grey-border); border-radius: 16px; padding: 32px; margin-bottom: 24px; }
    .form-section-title { font-size: 1rem; font-weight: 700; color: var(--navy); margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid var(--grey-border); }
    .locatie-blok { background: var(--grey-bg); border: 1px solid var(--grey-border); border-radius: 16px; padding: 32px; margin-bottom: 16px; }
    .locatie-blok-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid var(--grey-border); }
    .locatie-blok-title { font-size: 1rem; font-weight: 700; color: var(--navy); }
    .btn-verwijder { background: none; border: 1px solid var(--grey-border); border-radius: 6px; padding: 4px 10px; font-size: 0.78rem; color: var(--text-muted); cursor: pointer; transition: all 0.15s; }
    .btn-verwijder:hover { border-color: #E74C3C; color: #E74C3C; }
    .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .form-group { margin-bottom: 20px; }
    .form-group:last-child { margin-bottom: 0; }
    .form-group label { display: block; font-size: 0.83rem; font-weight: 600; color: var(--navy); margin-bottom: 6px; }
    .form-group label .req { color: var(--teal); margin-left: 2px; }
    .form-group input, .form-group textarea { width: 100%; padding: 11px 14px; border: 1.5px solid var(--grey-border); border-radius: 8px; font-family: 'Inter', sans-serif; font-size: 0.9rem; color: var(--text); background: var(--white); transition: border-color 0.2s, box-shadow 0.2s; outline: none; }
    .form-group input:focus, .form-group textarea:focus { border-color: var(--teal); box-shadow: 0 0 0 3px rgba(42,157,143,0.12); }
    .form-group textarea { resize: vertical; min-height: 90px; }
    .beschrijving-sectie { display: none; }
    .beschrijving-sectie.zichtbaar { display: block; }
    .btn-toevoegen { display: flex; align-items: center; gap: 8px; padding: 12px 20px; border: 2px dashed var(--grey-border); border-radius: 12px; background: none; color: var(--text-muted); font-family: 'Inter', sans-serif; font-size: 0.9rem; font-weight: 600; cursor: pointer; width: 100%; justify-content: center; transition: all 0.2s; margin-bottom: 24px; }
    .btn-toevoegen:hover { border-color: var(--teal); color: var(--teal); background: var(--teal-light); }
    .checkbox-group { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 24px; }
    .checkbox-group input[type="checkbox"] { width: 18px; height: 18px; accent-color: var(--teal); margin-top: 2px; flex-shrink: 0; cursor: pointer; }
    .checkbox-group label { font-size: 0.85rem; color: var(--text-muted); cursor: pointer; }
    .btn-submit { width: 100%; padding: 14px; background: var(--teal); color: var(--white); border: none; border-radius: 8px; font-family: 'Inter', sans-serif; font-size: 1rem; font-weight: 700; cursor: pointer; transition: background 0.2s, transform 0.15s; }
    .btn-submit:hover { background: #238a7e; transform: translateY(-1px); }
    .form-success { display: none; text-align: center; padding: 40px 20px; }
    .form-success .success-icon { font-size: 3rem; margin-bottom: 16px; }
    .form-success h3 { font-size: 1.3rem; font-weight: 700; color: var(--navy); margin-bottom: 10px; }
    .form-success p { color: var(--text-muted); font-size: 0.9rem; }

    .disciplines-info { display: flex; align-items: flex-start; gap: 10px; padding: 12px 16px; background: var(--teal-light); border: 1px solid rgba(42,157,143,0.3); border-radius: 8px; font-size: 0.83rem; color: #1a6b62; margin-top: 4px; }

    footer { background: #0F2340; color: rgba(255,255,255,0.5); text-align: center; padding: 28px 24px; font-size: 0.82rem; }
    footer a { color: rgba(255,255,255,0.7); text-decoration: none; }
    footer a:hover { color: var(--white); }

    @media (max-width: 700px) {
      .hamburger { display: flex; }
      nav { display: none; position: absolute; top: 68px; left: 0; right: 0; background: var(--navy); flex-direction: column; padding: 12px 16px 20px; gap: 4px; box-shadow: 0 8px 24px rgba(0,0,0,0.2); }
      nav.open { display: flex; }
      nav a { padding: 10px 16px; border-radius: 8px; }
      nav a.cta { margin-left: 0; margin-top: 8px; text-align: center; }
      .form-row { grid-template-columns: 1fr; }
      .form-section, .locatie-blok { padding: 20px; }
      .tier-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

<header>
  <div class="header-inner">
    <a href="index.html" class="logo">
      <img class="logo-icon" src="EVN_Logo_transparant.png" alt="EVN Logo" />
      <div class="logo-text">Enkel Voet Netwerk<span>Breda e.o.</span></div>
    </a>
    <div class="hamburger" onclick="toggleNav()"><span></span><span></span><span></span></div>
    <nav id="main-nav">
      <a href="index.html#protocollen">Protocollen</a>
      <a href="index.html#locaties">Locaties</a>
      <a href="partners.html">Partners</a>
      <a href="therapeut-worden.html">Aanmelden als therapeut</a>
      <a href="locatie-worden.html" class="cta">Locatie worden</a>
    </nav>
  </div>
</header>

<section class="hero">
  <div class="hero-inner">
    <div class="hero-badge">Netwerk uitbreiden</div>
    <h1>Word onderdeel van het<br><em>Enkel Voet Netwerk</em></h1>
    <p>Kies het pakket dat bij uw praktijk past en meld u aan via het formulier onderaan deze pagina.</p>
  </div>
  <svg class="hero-wave" viewBox="0 0 1440 60" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M0,30 C360,60 1080,0 1440,30 L1440,60 L0,60 Z" fill="#F5F7FA"/>
  </svg>
</section>

<!-- TIERS -->
<section class="tiers">
  <div class="section-inner">
    <div class="section-header">
      <div class="section-eyebrow">Pakketten</div>
      <h2>Kies uw aansluiting</h2>
      <p>Selecteer het pakket dat het beste bij uw praktijk past. U kunt later altijd upgraden.</p>
    </div>
    <div class="tier-grid">
      <div class="tier-card" id="tier-basis" onclick="selecteerTier('basis')">
        <div class="tier-check" id="check-basis"></div>
        <div class="tier-badge basis">Basis</div>
        <h3>Vermeld op de kaart</h3>
        <div style="margin:12px 0 4px"><span style="font-size:1.8rem;font-weight:700;color:var(--navy)">€5</span><span style="font-size:0.82rem;color:var(--text-muted)"> / locatie / maand</span></div>
        <p style="font-size:0.78rem;color:var(--text-muted);margin-bottom:8px">€3/maand per extra locatie</p>
        <p style="font-size:0.875rem;color:var(--text-muted)">Uw praktijk is zichtbaar op de locatiekaart en in de praktijkenlijst op de website.</p>
        <ul class="tier-features">
          <li>Vermelding op de interactieve kaart</li>
          <li>Naam, adres en contactgegevens</li>
          <li>Disciplines automatisch via therapeuten</li>
          <li class="nee">Beschrijving onder uw kaart</li>
          <li class="nee">Voorrangspositie in de lijst</li>
          <li class="nee">Vermelding op de partnerpagina</li>
        </ul>
      </div>
      <div class="tier-card" id="tier-plus" onclick="selecteerTier('plus')">
        <div class="tier-check" id="check-plus"></div>
        <div class="tier-badge plus">Plus</div>
        <h3>Met beschrijving</h3>
        <div style="margin:12px 0 4px"><span style="font-size:1.8rem;font-weight:700;color:var(--navy)">€10</span><span style="font-size:0.82rem;color:var(--text-muted)"> / locatie / maand</span></div>
        <p style="font-size:0.78rem;color:var(--text-muted);margin-bottom:8px">€6/maand per extra locatie</p>
        <p style="font-size:0.875rem;color:var(--text-muted)">Alles van Basis, plus een korte beschrijving van uw praktijk onder uw vermelding.</p>
        <ul class="tier-features">
          <li>Vermelding op de interactieve kaart</li>
          <li>Naam, adres en contactgegevens</li>
          <li>Disciplines automatisch via therapeuten</li>
          <li>Beschrijving onder uw kaart</li>
          <li class="nee">Voorrangspositie in de lijst</li>
          <li class="nee">Vermelding op de partnerpagina</li>
        </ul>
      </div>
      <div class="tier-card partner" id="tier-partner" onclick="selecteerTier('partner')">
        <div class="partner-label">⭐ Meest compleet</div>
        <div class="tier-check" id="check-partner"></div>
        <div class="tier-badge partner">Partner</div>
        <h3>Volledig partnerschap</h3>
        <div style="margin:12px 0 4px"><span style="font-size:1.8rem;font-weight:700;color:var(--gold)">€50</span><span style="font-size:0.82rem;color:var(--text-muted)"> / locatie / maand</span></div>
        <p style="font-size:0.78rem;color:var(--text-muted);margin-bottom:8px">€25/maand per extra locatie</p>
        <p style="font-size:0.875rem;color:var(--text-muted)">De meest prominente positie in het netwerk, inclusief vermelding op de exclusieve partnerpagina.</p>
        <ul class="tier-features">
          <li>Vermelding op de interactieve kaart</li>
          <li>Naam, adres en contactgegevens</li>
          <li>Disciplines automatisch via therapeuten</li>
          <li>Beschrijving onder uw kaart</li>
          <li>Bovenaan de praktijkenlijst</li>
          <li>Logo + profiel op de partnerpagina</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- FORMULIER -->
<section class="formulier" id="aanmelden">
  <div class="section-inner">
    <div class="section-header">
      <div class="section-eyebrow">Aanmelden</div>
      <h2>Meld uw praktijk aan</h2>
      <p>Vul het formulier in en we nemen spoedig contact met u op.</p>
    </div>
    <div class="form-wrap">
      <div id="form-content">
<input type="text" name="website_url" id="website_url" style="display:none" tabindex="-1" autocomplete="off" />
        <div class="form-section" id="pakket-sectie" style="border-color: var(--teal);">
          <div class="form-section-title">Gekozen pakket</div>
          <p id="pakket-weergave" style="color:var(--text-muted);font-size:0.9rem;">Selecteer hierboven een pakket om verder te gaan.</p>
        </div>

        <div class="form-section">
          <div class="form-section-title">Uw contactgegevens</div>
          <div class="form-row">
            <div class="form-group"><label>Voornaam <span class="req">*</span></label><input type="text" id="voornaam" placeholder="Jan" /></div>
            <div class="form-group"><label>Achternaam <span class="req">*</span></label><input type="text" id="achternaam" placeholder="Jansen" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>E-mailadres <span class="req">*</span></label><input type="email" id="email" placeholder="info@praktijk.nl" /></div>
            <div class="form-group"><label>Telefoonnummer</label><input type="tel" id="telefoon" placeholder="076-0000000" /></div>
          </div>
        </div>

        <div id="locaties-container"></div>

        <button type="button" class="btn-toevoegen" onclick="voegLocatieToe()">+ Nog een locatie toevoegen</button>

        <div class="form-section beschrijving-sectie" id="beschrijving-sectie">
          <div class="form-section-title">Beschrijving van uw praktijk</div>
          <div class="form-group">
            <label>Korte beschrijving <span class="req">*</span></label>
            <textarea id="beschrijving" placeholder="Beschrijf uw praktijk in 2-3 zinnen." style="min-height:120px;" maxlength="500" oninput="telTekens(this)"></textarea>
            <p style="font-size:0.75rem;color:var(--text-muted);margin-top:4px"><span id="tekens-teller">0</span>/500 tekens</p>
          </div>
          <div id="hoofdlocatie-sectie" style="display:none">
            <div style="background:var(--gold-light);border:1px solid var(--gold);border-radius:8px;padding:14px 16px;margin-bottom:20px;font-size:0.85rem;color:#7a5800">
              ⭐ Als partner wordt u weergegeven als één praktijk op de partnerpagina.
            </div>
            <div class="form-group"><label>Hoofdadres voor partnerpagina <span class="req">*</span></label><input type="text" id="partner-adres" placeholder="Industriekade 10, 4815 HD Breda" /></div>
            <div class="form-row">
              <div class="form-group"><label>Telefoon voor partnerpagina</label><input type="tel" id="partner-telefoon" placeholder="076-0000000" /></div>
              <div class="form-group"><label>E-mail voor partnerpagina</label><input type="email" id="partner-email" placeholder="info@praktijk.nl" /></div>
            </div>
            <div class="form-group">
              <label>Website URL logo</label>
              <input type="url" id="logo-url" placeholder="https://www.uwpraktijk.nl/logo.png" />
              <p style="font-size:0.78rem;color:var(--text-muted);margin-top:6px">Vul de URL in van uw logo (PNG of SVG).</p>
            </div>
          </div>
        </div>

        <div class="form-section">
          <div class="form-section-title">Overige informatie</div>
          <div class="form-group">
            <label>Toelichting</label>
            <textarea id="toelichting" placeholder="Heeft u vragen of wilt u iets toelichten?"></textarea>
          </div>
        </div>

        <div class="checkbox-group">
          <input type="checkbox" id="akkoord" />
          <label for="akkoord">Ik ga akkoord met de verwerking van mijn gegevens voor zichtbaarheid binnen het Enkel Voet Netwerk, zoals beschreven in onze <a href="privacy.html" style="color:var(--teal)">privacyverklaring</a>.</label>
        </div>

        <button class="btn-submit" onclick="verstuurFormulier()">Aanmelding versturen →</button>
      </div>

      <div class="form-success" id="form-success">
        <div class="success-icon">✅</div>
        <h3>Aanmelding ontvangen!</h3>
        <p>Bedankt voor uw aanmelding. We nemen binnen twee werkdagen contact met u op.</p>
      </div>
    </div>
  </div>
</section>

<footer>
  <p>© 2025 Enkel Voet Netwerk Breda e.o. &nbsp;·&nbsp; <a href="index.html">Terug naar home</a> &nbsp;·&nbsp; <a href="privacy.html">Privacyverklaring</a></p>
</footer>

<script>
  const SUPABASE_URL = 'https://islujznszevdynguhjdc.supabase.co';
  const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlzbHVqem5zemV2ZHluZ3VoamRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE2NDYzMDAsImV4cCI6MjA5NzIyMjMwMH0.wh3RXZRKfpfArr3YBYu8ktE7xv1inwDD72Vq3LJl3QQ';

  let locatieCount = 0;
  let geselecteerdeTier = '';

  function fixUrl(url) {
    url = url.trim();
    if (!url) return '';
    if (!url.startsWith('http://') && !url.startsWith('https://')) url = 'https://' + url;
    url = url.replace('http://', 'https://');
    return url;
  }

  function telTekens(el) {
    document.getElementById('tekens-teller').textContent = el.value.length;
  }

  function selecteerTier(tier) {
    geselecteerdeTier = tier;
    ['basis','plus','partner'].forEach(t => {
      document.getElementById(`tier-${t}`).classList.remove('geselecteerd');
      document.getElementById(`check-${t}`).textContent = '';
    });
    document.getElementById(`tier-${tier}`).classList.add('geselecteerd');
    document.getElementById(`check-${tier}`).textContent = '✓';
    const namen = { basis: '📍 Basis — Vermelding op de kaart', plus: '📝 Plus — Met beschrijving', partner: '⭐ Partner — Volledig partnerschap' };
    document.getElementById('pakket-weergave').innerHTML = `<strong style="color:var(--navy)">${namen[tier]}</strong>`;
    const beschSectie = document.getElementById('beschrijving-sectie');
    const hoofdlocatieSectie = document.getElementById('hoofdlocatie-sectie');
    if (tier === 'plus' || tier === 'partner') {
      beschSectie.classList.add('zichtbaar');
      hoofdlocatieSectie.style.display = tier === 'partner' ? 'block' : 'none';
    } else {
      beschSectie.classList.remove('zichtbaar');
      hoofdlocatieSectie.style.display = 'none';
    }
  }

  function voegLocatieToe() {
    locatieCount++;
    const nr = locatieCount;
    const container = document.getElementById('locaties-container');
    const blok = document.createElement('div');
    blok.className = 'locatie-blok';
    blok.id = `locatie-${nr}`;
    blok.innerHTML = `
      <div class="locatie-blok-header">
        <div class="locatie-blok-title">Locatie ${nr}</div>
        ${nr > 1 ? `<button type="button" class="btn-verwijder" onclick="verwijderLocatie(${nr})">✕ Verwijderen</button>` : ''}
      </div>
      <div class="form-group"><label>Naam praktijk <span class="req">*</span></label><input type="text" id="praktijk-${nr}" placeholder="Fysiotherapie De Voet" /></div>
      <div class="form-group"><label>Adres <span class="req">*</span></label><input type="text" id="adres-${nr}" placeholder="Straat 1, 4800 AB Breda" /></div>
      <div class="form-group"><label>Website</label><input type="url" id="website-${nr}" placeholder="https://www.jouwpraktijk.nl" /></div>
      <div class="form-row">
        <div class="form-group"><label>Telefoonnummer locatie</label><input type="tel" id="tel-locatie-${nr}" placeholder="076-0000000" /></div>
        <div class="form-group"><label>E-mail locatie</label><input type="email" id="email-locatie-${nr}" placeholder="info@praktijk.nl" /></div>
      </div>
      <div class="disciplines-info">
        ℹ️ De disciplines van uw locatie worden automatisch bepaald op basis van de therapeuten die zich aanmelden bij deze praktijk.
      </div>`;
    container.appendChild(blok);
    hernummerLocaties();
  }

  function verwijderLocatie(nr) { document.getElementById(`locatie-${nr}`).remove(); hernummerLocaties(); }
  function hernummerLocaties() {
    document.querySelectorAll('.locatie-blok').forEach((blok, i) => {
      blok.querySelector('.locatie-blok-title').textContent = `Locatie ${i + 1}`;
    });
  }
  function toggleNav() { document.getElementById('main-nav').classList.toggle('open'); }

  async function schrijfNaarSupabase(tabel, data) {
    const resp = await fetch(`${SUPABASE_URL}/rest/v1/${tabel}`, {
      method: 'POST',
      headers: {
        'apikey': SUPABASE_KEY,
        'Authorization': `Bearer ${SUPABASE_KEY}`,
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
      },
      body: JSON.stringify(data)
    });
    if (!resp.ok) {
      const err = await resp.text();
      throw new Error(`Supabase fout (${tabel}): ${err}`);
    }
    return await resp.json();
  }

  async function verstuurFormulier() {
    if (document.getElementById('website_url').value !== '') return;
    if (!geselecteerdeTier) { alert('Selecteer eerst een pakket.'); return; }

    const verplicht = ['voornaam','achternaam','email'];
    let geldig = true;
    verplicht.forEach(id => {
      const el = document.getElementById(id);
      if (!el.value.trim()) { el.style.borderColor = '#E74C3C'; geldig = false; }
      else { el.style.borderColor = ''; }
    });

    const blokken = document.querySelectorAll('.locatie-blok');
    if (blokken.length === 0) { alert('Voeg minimaal één locatie toe.'); return; }

    blokken.forEach(blok => {
      const nr = blok.id.replace('locatie-','');
      const praktijk = document.getElementById(`praktijk-${nr}`);
      const adres = document.getElementById(`adres-${nr}`);
      if (!praktijk.value.trim()) { praktijk.style.borderColor = '#E74C3C'; geldig = false; } else { praktijk.style.borderColor = ''; }
      if (!adres.value.trim()) { adres.style.borderColor = '#E74C3C'; geldig = false; } else { adres.style.borderColor = ''; }
    });

    if ((geselecteerdeTier === 'plus' || geselecteerdeTier === 'partner') && !document.getElementById('beschrijving').value.trim()) {
      document.getElementById('beschrijving').style.borderColor = '#E74C3C'; geldig = false;
    }

    if (!document.getElementById('akkoord').checked) { alert('Vink het akkoordvakje aan.'); return; }
    if (!geldig) { alert('Vul alle verplichte velden in.'); return; }

    const knop = document.querySelector('.btn-submit');
    knop.textContent = 'Versturen…';
    knop.disabled = true;

    try {
      for (const blok of blokken) {
        const nr = blok.id.replace('locatie-','');
        const adresRaw = document.getElementById(`adres-${nr}`).value.trim();

        const praktijkData = {
          naam:         document.getElementById(`praktijk-${nr}`).value.trim(),
          straat:       adresRaw,
          postcode:     '',
          stad:         '',
          telefoon:     document.getElementById(`tel-locatie-${nr}`).value.trim(),
          email:        document.getElementById(`email-locatie-${nr}`).value.trim(),
          website:      fixUrl(document.getElementById(`website-${nr}`).value || ''),
          aangemeld_via: 'enkelvoet.net',
          tier:         geselecteerdeTier,
          beschrijving: (geselecteerdeTier === 'plus' || geselecteerdeTier === 'partner')
                          ? document.getElementById('beschrijving').value.trim() : '',
          logo_url: geselecteerdeTier === 'partner'
            ? valideerFotoUrl(fixUrl(document.getElementById('logo-url').value || '')) : '',
          disciplines:  [], // wordt automatisch gevuld via therapeuten
          contact_voornaam: document.getElementById('voornaam').value.trim(),
          contact_achternaam: document.getElementById('achternaam').value.trim(),
          contact_email: document.getElementById('email').value.trim(),
          contact_telefoon: document.getElementById('telefoon').value.trim(),
          toelichting:  document.getElementById('toelichting').value.trim(),
          actief:       false
        };

        await schrijfNaarSupabase('praktijken', praktijkData);
      }

      document.getElementById('form-content').style.display = 'none';
      document.getElementById('form-success').style.display = 'block';

    } catch (err) {
      console.error(err);
      alert('Er ging iets mis bij het versturen. Probeer het opnieuw.');
      knop.textContent = 'Aanmelding versturen →';
      knop.disabled = false;
    }
  }

  voegLocatieToe();
</script>
</body>
</html>

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
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    body = re.sub(r'<img[^>]*/?>', '', body)
    body = re.sub(r'<figure[^>]*>.*?</figure>', '', body, flags=re.DOTALL)

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

    body = re.sub(r' style="[^"]*"', '', body)
    body = re.sub(r' class="[^"]*"', '', body)
    body = re.sub(r' id="[^"]*"', '', body)
    body = re.sub(r'<hr[^>]*>', '<hr>', body)
    body = re.sub(r'\n{3,}', '\n\n', body)

    def maak_knop_van_link(match):
        url = match.group(1)
        linktekst = re.sub(r'<[^>]+>', '', match.group(2)).strip()
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

    body = re.sub(r'<span>\s*</span>', '', body)
    body = re.sub(r'<span>(.*?)</span>', r'\1', body)
    body = re.sub(r'<p>\s*</p>', '', body)
    body = re.sub(r'<div>\s*</div>', '', body)

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
    body = re.sub(r'https?://(?:www\.)?fysioefeningen\.nl/[^\s<>"\']+', '', body)

    return body.strip()

def extraheer_preview(body, max_alineas=3):
    body = opschonen_html(body)
    blokken = re.findall(r'<(p|h1|h2|h3)[^>]*>.*?</\1>', body, re.DOTALL | re.IGNORECASE)
    blokken = [b for b in blokken if len(re.sub(r'<[^>]+>', '', b).strip()) > 10]
    return '\n'.join(blokken[:max_alineas])

def extraheer_oefenfilmpjes_ruw(rauwe_html_niveaus):
    gezien = set()
    links = []
    for rauwe_html in rauwe_html_niveaus:
        tekst = re.sub(r'<[^>]+>', ' ', rauwe_html)
        tekst = re.sub(r'\s+', ' ', tekst)
        gevonden = re.findall(r'\[VIDEO:\s*([^|\]]+)\|\s*(https?://[^\]]+)\]', tekst)
        for naam, url in gevonden:
            naam = naam.strip()
            url = url.strip()
            if url not in gezien:
                gezien.add(url)
                links.append((url, naam))
    return links

# ─────────────────────────────────────────────────────────────
# Hulpfuncties voor volledige HTML-pagina's per protocol
# ─────────────────────────────────────────────────────────────

def maak_protocol_titel(protocol_naam, niveau):
    niveau_labels = {
        'makkelijk': 'basisinformatie',
        'gemiddeld': 'voor zorgverleners',
        'complex': 'verdiepend'
    }
    label = niveau_labels.get(niveau, niveau)
    return f"{protocol_naam} — {label} | Enkel Voet Netwerk"

def maak_meta_description(protocol_naam, niveau, body_schoon):
    niveau_intro = {
        'makkelijk': 'Begrijpelijke uitleg over',
        'gemiddeld': 'Behandelprotocol voor',
        'complex': 'Verdiepend behandelprotocol voor'
    }
    intro = niveau_intro.get(niveau, 'Behandelprotocol voor')
    extractor = TextExtractor()
    extractor.feed(body_schoon)
    tekst = extractor.get_text()[:200].strip()
    if tekst:
        return f"{intro} {protocol_naam.lower()}. {tekst}..."
    return f"{intro} {protocol_naam.lower()}. Fysiotherapie Breda — Enkel Voet Netwerk."

def maak_niveau_label(niveau):
    labels = {'makkelijk': '📗 Makkelijk', 'gemiddeld': '📘 Gemiddeld', 'complex': '📕 Complex'}
    return labels.get(niveau, niveau.capitalize())

def maak_cta_blok():
    """Genereer een vast CTA-blok onderaan elke protocolpagina"""
    return '''
<div class="cta-blok">
  <div class="cta-sectie cta-afspraak">
    <h2 class="cta-titel">Klaar om aan de slag te gaan?</h2>
    <p class="cta-sub">Vind een aangesloten therapeut bij jou in de buurt en maak een afspraak.</p>
    <div class="cta-knoppen">
      <a href="../locaties.html" class="btn-primary">🗺 Vind een locatie bij mij in de buurt</a>
      <a href="../locatie-worden.html" class="btn-outline">Locatie aanmelden</a>
    </div>
  </div>
</div>

<style>
  .cta-blok { margin-top: 3rem; border-top: 2px solid var(--teal-light); padding-top: 2rem; }
  .cta-sectie { border-radius: 14px; padding: 2rem; }
  .cta-titel { font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem; }
  .cta-sub { font-size: 0.88rem; margin-bottom: 1.5rem; }
  .cta-afspraak { background: #1B3A5C; }
  .cta-afspraak .cta-titel { color: white; }
  .cta-afspraak .cta-sub { color: rgba(255,255,255,0.7); }
  .cta-knoppen { display: flex; gap: 10px; flex-wrap: wrap; }
  .btn-primary { background: var(--teal); color: white; padding: 11px 22px; border-radius: 8px; font-size: 0.9rem; font-weight: 700; text-decoration: none; transition: background 0.2s; }
  .btn-primary:hover { background: #238a7e; }
  .btn-outline { background: transparent; color: rgba(255,255,255,0.8); border: 1.5px solid rgba(255,255,255,0.3); padding: 11px 22px; border-radius: 8px; font-size: 0.9rem; font-weight: 600; text-decoration: none; transition: all 0.2s; }
  .btn-outline:hover { border-color: white; color: white; }
</style>'''

def extraheer_fysioefeningen_urls(body_schoon):
    """Haal alle fysioefeningen.nl URLs op uit de opgeschoonde body"""
    return re.findall(
        r'href="(https?://(?:www\.)?fysioefeningen\.nl/[^"]+)"',
        body_schoon
    )

def maak_html_pagina(protocol_naam, protocol_id, niveau, body_schoon, zone_naam):
    titel = maak_protocol_titel(protocol_naam, niveau)
    description = maak_meta_description(protocol_naam, niveau, body_schoon)
    niveau_label = maak_niveau_label(niveau)

    andere_niveaus = [n for n in ['makkelijk', 'gemiddeld', 'complex'] if n != niveau]
    andere_niveaus_html = ''
    for n in andere_niveaus:
        andere_niveaus_html += f'<a href="{protocol_id}-{n}.html" class="niveau-badge link">{maak_niveau_label(n)}</a>\n'

    cta_blok = maak_cta_blok()

    # Haal fysioefeningen.nl URLs op voor structured data
    fysio_urls = extraheer_fysioefeningen_urls(body_schoon)
    if fysio_urls:
        fysio_links = ',\n    '.join([f'"relatedLink": "{u}"' for u in fysio_urls])
        structured_data_extra = f',\n    {fysio_links}'
    else:
        structured_data_extra = ''

    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{titel}</title>
  <meta name="description" content="{description}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://enkelvoet.net/protocollen/{protocol_id}-{niveau}.html" />
  <meta property="og:title" content="{titel}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:type" content="article" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{ --navy: #1B3A5C; --teal: #2A9D8F; --teal-light: #E8F5F4; --grey-bg: #F5F7FA; --grey-border: #DDE3EC; --text: #1A1A2E; --text-muted: #6B7A99; --white: #FFFFFF; }}
    body {{ font-family: "Inter", sans-serif; font-size: 16px; color: var(--text); background: var(--grey-bg); line-height: 1.6; }}
    header {{ background: var(--navy); position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 12px rgba(0,0,0,0.15); }}
    .header-inner {{ max-width: 1200px; margin: 0 auto; padding: 0 clamp(1rem, 4vw, 3rem); display: flex; align-items: center; justify-content: space-between; height: 68px; }}
    .logo {{ display: flex; align-items: center; gap: 12px; text-decoration: none; }}
    .logo-icon {{ width: 40px; height: 40px; }}
    .logo-text {{ color: var(--white); font-weight: 700; font-size: 1.05rem; line-height: 1.2; }}
    .logo-text span {{ display: block; font-weight: 300; font-size: 0.75rem; opacity: 0.7; }}
    nav {{ display: flex; gap: 6px; }}
    nav a {{ color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.875rem; font-weight: 500; padding: 8px 14px; border-radius: 6px; transition: background 0.2s; }}
    nav a:hover {{ background: rgba(255,255,255,0.12); color: var(--white); }}
    .breadcrumb {{ max-width: 860px; margin: 24px auto 0; padding: 0 clamp(1rem, 4vw, 3rem); font-size: 0.82rem; color: var(--text-muted); }}
    .breadcrumb a {{ color: var(--teal); text-decoration: none; }}
    .breadcrumb a:hover {{ text-decoration: underline; }}
    .page-header {{ max-width: 860px; margin: 16px auto 0; padding: 0 clamp(1rem, 4vw, 3rem); }}
    .zone-badge {{ display: inline-block; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--teal); background: var(--teal-light); padding: 2px 10px; border-radius: 999px; margin-bottom: 10px; }}
    h1 {{ font-size: clamp(1.5rem, 3vw, 2rem); font-weight: 700; color: var(--navy); line-height: 1.25; margin-bottom: 12px; }}
    .niveau-badges {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px; }}
    .niveau-badge {{ padding: 6px 14px; border-radius: 6px; font-size: 0.78rem; font-weight: 600; text-decoration: none; }}
    .niveau-badge.actief {{ background: var(--navy); color: white; cursor: default; }}
    .niveau-badge.link {{ background: var(--grey-bg); color: var(--text-muted); border: 1px solid var(--grey-border); }}
    .niveau-badge.link:hover {{ background: var(--grey-border); }}
    .content-wrap {{ max-width: 860px; margin: 0 auto 64px; padding: 0 clamp(1rem, 4vw, 3rem); }}
    .disclaimer {{ background: #FEF9E7; border: 1px solid #F0D060; border-radius: 8px; padding: 12px 16px; font-size: 0.82rem; color: #7D6608; margin-bottom: 24px; }}
    .terug-link {{ display: inline-flex; align-items: center; gap: 6px; color: var(--teal); font-size: 0.85rem; font-weight: 600; text-decoration: none; margin-bottom: 20px; }}
    .terug-link:hover {{ text-decoration: underline; }}
    .content {{ background: var(--white); border: 1px solid var(--grey-border); border-radius: 14px; padding: clamp(1.5rem, 4vw, 3rem); font-size: 0.92rem; line-height: 1.8; }}
    .content h2 {{ font-size: 1.15rem; font-weight: 700; color: var(--navy); margin: 1.6em 0 0.5em; padding-bottom: 6px; border-bottom: 2px solid var(--teal-light); }}
    .content h3 {{ font-size: 1rem; font-weight: 700; color: var(--navy); margin: 1.2em 0 0.4em; }}
    .content h4 {{ font-size: 0.9rem; font-weight: 700; color: var(--text-muted); margin: 1em 0 0.3em; text-transform: uppercase; letter-spacing: 0.05em; }}
    .content p {{ margin-bottom: 0.9em; }}
    .content ul, .content ol {{ margin: 0.4em 0 0.9em 1.6em; }}
    .content li {{ margin-bottom: 0.35em; }}
    .content hr {{ border: none; border-top: 1px solid var(--grey-border); margin: 1.8em 0; }}
    .content table {{ width: 100%; border-collapse: collapse; margin: 1em 0; font-size: 0.85rem; }}
    .content td, .content th {{ border: 1px solid var(--grey-border); padding: 8px 12px; text-align: left; }}
    .content th {{ background: var(--grey-bg); font-weight: 600; }}
    footer {{ background: #0F2340; color: rgba(255,255,255,0.5); text-align: center; padding: 28px 24px; font-size: 0.82rem; }}
    footer a {{ color: rgba(255,255,255,0.7); text-decoration: none; }}
    @media (max-width: 700px) {{ nav {{ display: none; }} }}
  </style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "MedicalWebPage",
    "name": "{titel}",
    "description": "{description}",
    "url": "https://enkelvoet.net/protocollen/{protocol_id}-{niveau}.html",
    "inLanguage": "nl",
    "isPartOf": {{"@type": "WebSite", "name": "Enkel Voet Netwerk", "url": "https://enkelvoet.net"}}{structured_data_extra}
  }}
  </script>
</head>
<body>
<header>
  <div class="header-inner">
    <a href="../index.html" class="logo">
      <img class="logo-icon" src="../EVN_Logo_transparant.png" alt="EVN Logo" />
      <div class="logo-text">Enkel Voet Netwerk<span>Breda e.o.</span></div>
    </a>
    <nav>
      <a href="../protocollen.html">Protocollen</a>
      <a href="../index.html#locaties">Locaties</a>
      <a href="../partners.html">Partners</a>
    </nav>
  </div>
</header>

<div class="breadcrumb">
  <a href="../index.html">Home</a> &rsaquo;
  <a href="../protocollen.html">Protocollen</a> &rsaquo;
  {protocol_naam}
</div>

<div class="page-header">
  <div class="zone-badge">{zone_naam}</div>
  <h1>{protocol_naam}</h1>
  <div class="niveau-badges">
    <span class="niveau-badge actief">{niveau_label}</span>
    {andere_niveaus_html}
  </div>
</div>

<div class="content-wrap">
  <div class="disclaimer">
    ⚠️ Dit protocol is algemene informatie voor zorgverleners en patiënten. Het vervangt geen persoonlijk advies van een arts of fysiotherapeut.
  </div>
  <a href="../protocollen.html" class="terug-link">&#8592; Terug naar alle protocollen</a>
  <div class="content">
    {body_schoon}
  </div>
  {cta_blok}
</div>

<footer>
  <p>&copy; 2025 Enkel Voet Netwerk Breda e.o. &nbsp;&middot;&nbsp; <a href="../index.html">Home</a> &nbsp;&middot;&nbsp; <a href="../protocollen.html">Protocollen</a></p>
</footer>
</body>
</html>'''

# ─────────────────────────────────────────────────────────────

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
    protocol_ruwe_html = {}

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

                zone_naam_display = ZONES.get(protocol.get('zone', ''), 'Enkel & voet')
                volledige_pagina = maak_html_pagina(
                    protocol_naam=protocol['naam'],
                    protocol_id=protocol['id'],
                    niveau=niveau,
                    body_schoon=body_schoon,
                    zone_naam=zone_naam_display
                )
                with open(bestandsnaam, 'w', encoding='utf-8') as out:
                    out.write(volledige_pagina)

                print(f"OK: {bestandsnaam}")
                extractor = TextExtractor()
                extractor.feed(body_schoon)
                protocol_teksten[niveau] = extractor.get_text()[:2000]
                protocol_previews[niveau] = extraheer_preview(body, max_alineas=3)
                protocol_volledige_html[niveau] = body_schoon
                protocol_ruwe_html[niveau] = body
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

    oefenfilmpjes_html = ''
    links = extraheer_oefenfilmpjes_ruw(list(p['ruwe_html'].values()))
    if links:
        links_tonen = links[:4]
        grid_class = "oefenfilmpjes-grid" if len(links_tonen) > 1 else "oefenfilmpjes-grid enkelvoudig"
        oefenfilmpjes_html = f'<div class="oefenfilmpjes-zijbalk"><div class="oefenfilmpjes-titel">📹 Oefenfilmpjes</div><div class="{grid_class}">'
        for url, naam in links_tonen:
            if not naam or naam.startswith('http'):
                naam = url.replace('https://www.fysioefeningen.nl/', '').replace('https://fysioefeningen.nl/', '').replace('-', ' ').strip().capitalize()
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
  <p style="margin-top:14px;font-size:0.78rem;opacity:0.65;max-width:520px;margin-left:auto;margin-right:auto">⚠️ Deze protocollen zijn algemene informatie voor zorgverleners en patiënten. Ze vervangen geen persoonlijk advies van een arts of fysiotherapeut. Bij twijfel of alarmsymptomen altijd contact opnemen met een zorgverlener.</p>
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

# ─────────────────────────────────────────────────────────────
# Genereer sitemap.xml
# ─────────────────────────────────────────────────────────────
print("Genereer sitemap.xml...")
vandaag = date.today().isoformat()

sitemap_urls = [
    f'  <url><loc>https://enkelvoet.net/</loc><changefreq>monthly</changefreq><priority>1.0</priority></url>',
    f'  <url><loc>https://enkelvoet.net/protocollen.html</loc><lastmod>{vandaag}</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>',
    f'  <url><loc>https://enkelvoet.net/locaties.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>',
    f'  <url><loc>https://enkelvoet.net/partners.html</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>',
]

for p in protocol_data:
    for niveau in p['teksten'].keys():
        url = f"https://enkelvoet.net/protocollen/{p['id']}-{niveau}.html"
        sitemap_urls.append(f'  <url><loc>{url}</loc><lastmod>{vandaag}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>')

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += '\n'.join(sitemap_urls)
sitemap += '\n</urlset>'

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)
print(f"OK: sitemap.xml gegenereerd met {len(sitemap_urls)} URLs")

# ─────────────────────────────────────────────────────────────
# Genereer robots.txt
# ─────────────────────────────────────────────────────────────
print("Genereer robots.txt...")

robots = """User-agent: *
Allow: /
Sitemap: https://enkelvoet.net/sitemap.xml"""

with open('robots.txt', 'w', encoding='utf-8') as f:
    f.write(robots)
print("OK: robots.txt gegenereerd")

if fouten:
    print(f"WAARSCHUWING: {len(fouten)} fouten")
