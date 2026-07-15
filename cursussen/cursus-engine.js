// ─────────────────────────────────────────────────────────────
// CURSUS-ENGINE — gedeeld door alle cursusmodules
// Vereist dat het inladende bestand vooraf een const CURSUS = {...} definieert.
// ─────────────────────────────────────────────────────────────
const SUPABASE_URL = 'https://islujznszevdynguhjdc.supabase.co';
const ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlzbHVqem5zemV2ZHluZ3VoamRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE2NDYzMDAsImV4cCI6MjA5NzIyMjMwMH0.wh3RXZRKfpfArr3YBYu8ktE7xv1inwDD72Vq3LJl3QQ';

// ─────────────────────────────────────────────────────────────
// DEMO THERAPEUTEN — vervang later door Supabase lookup
// ─────────────────────────────────────────────────────────────
const THERAPEUTEN = {
  "DEMO":    { naam: "Demo Therapeut",     praktijk: "Enkel Voet Netwerk",     locatie: "Breda" },
  "EVN-001": { naam: "Lisa van den Berg",  praktijk: "Fysiotherapie Centrum",  locatie: "Breda" },
  "EVN-002": { naam: "Marco Smits",        praktijk: "Bewegingscentrum Zuid",  locatie: "Breda" }
};

// ─────────────────────────────────────────────────────────────
// STATE
// ─────────────────────────────────────────────────────────────
let huidigeTherapeut = null;
let blokState = {};
let openBlok = null;

function initState() {
  blokState = {};
  CURSUS.blokken.forEach(blok => {
    const vraagVolgorde = shuffleArr(blok.vragen.map((_, i) => i));
    const optieVolgorde = {};
    blok.vragen.forEach((v, vi) => {
      optieVolgorde[vi] = shuffleArr(v.opties.map((_, oi) => oi));
    });
    blokState[blok.id] = {
      antwoorden: {},
      afgerond: false,
      vraagVolgorde,
      optieVolgorde
    };
  });
  openBlok = CURSUS.blokken[0].id;
}

function shuffleArr(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// Herstel sessie van mijn-profiel.html
function herstelSessie() {
  const opgeslagen = sessionStorage.getItem('evn_therapeut');
  if (!opgeslagen) return false;
  try {
    const data = JSON.parse(opgeslagen);
    if (!data || !data.naam) return false;
    huidigeTherapeut = data;
    initState();
    const el = id => document.getElementById(id);
    if (el('scherm-inlog')) el('scherm-inlog').style.display = 'none';
    if (el('scherm-cursus')) el('scherm-cursus').style.display = 'block';
    if (el('header-naam')) el('header-naam').textContent = huidigeTherapeut.naam;
    if (el('header-praktijk')) el('header-praktijk').textContent = (huidigeTherapeut.praktijk || '') + ' · ' + (huidigeTherapeut.locatie || '');
    if (el('header-therapeut')) el('header-therapeut').classList.add('zichtbaar');
    if (el('btn-uitloggen')) el('btn-uitloggen').classList.add('zichtbaar');
    setTimeout(() => renderCursus(), 50);
    return true;
  } catch(e) {
    console.error('Sessie herstel mislukt:', e);
    return false;
  }
}

// ─────────────────────────────────────────────────────────────
// INLOGGEN / UITLOGGEN
// ─────────────────────────────────────────────────────────────
function inloggen() {
  const code = document.getElementById('inp-code').value.trim().toUpperCase();
  const therapeut = THERAPEUTEN[code];
  if (!therapeut) {
    document.getElementById('inlog-fout').classList.add('zichtbaar');
    return;
  }
  huidigeTherapeut = { ...therapeut, code };
  initState();
  document.getElementById('scherm-inlog').style.display = 'none';
  document.getElementById('scherm-cursus').style.display = 'block';
  document.getElementById('header-naam').textContent = therapeut.naam;
  document.getElementById('header-praktijk').textContent = therapeut.praktijk + ' · ' + therapeut.locatie;
  document.getElementById('header-therapeut').classList.add('zichtbaar');
  document.getElementById('btn-uitloggen').classList.add('zichtbaar');
  renderCursus();
}

function uitloggen() {
  huidigeTherapeut = null;
  blokState = {};
  document.getElementById('scherm-inlog').style.display = 'block';
  document.getElementById('scherm-cursus').style.display = 'none';
  document.getElementById('header-therapeut').classList.remove('zichtbaar');
  document.getElementById('btn-uitloggen').classList.remove('zichtbaar');
  document.getElementById('inp-code').value = '';
  document.getElementById('inlog-fout').classList.remove('zichtbaar');
  document.getElementById('cert-banner').classList.remove('zichtbaar');
}

// ─────────────────────────────────────────────────────────────
// RENDER
// ─────────────────────────────────────────────────────────────
function renderCursus() {
  renderVoortgang();
  renderBlokken();
  checkAllesAfgerond();
}

function renderVoortgang() {
  const afgerond = CURSUS.blokken.filter(b => blokState[b.id]?.afgerond).length;
  const totaal = CURSUS.blokken.length;
  const pct = Math.round(afgerond / totaal * 100);
  document.getElementById('voortgang-fill').style.width = pct + '%';
  document.getElementById('voortgang-tekst').textContent = afgerond + ' van ' + totaal + ' blokken afgerond';
  document.getElementById('voortgang-pct').textContent = pct + '%';
}

function renderBlokken() {
  const container = document.getElementById('blokken-container');
  container.innerHTML = '';
  CURSUS.blokken.forEach((blok, idx) => {
    const vorigeAfgerond = idx === 0 || blokState[CURSUS.blokken[idx - 1].id]?.afgerond;
    const isLocked = !vorigeAfgerond;
    const isOpen = openBlok === blok.id && !isLocked;
    const state = blokState[blok.id];
    container.appendChild(maakBlokEl(blok, state, isOpen, isLocked));
  });
}

function maakBlokEl(blok, state, isOpen, isLocked) {
  const el = document.createElement('div');
  el.className = 'blok';
  el.id = 'blok-el-' + blok.id;

  const aantalVragen = blok.vragen.length;
  const beantwoord = Object.keys(state.antwoorden).length;
  const score = berekenScore(blok, state);

  let numKlasse = (state.afgerond && state.geslaagd) ? 'klaar' : (state.afgerond && !state.geslaagd) ? 'gezakt' : isLocked ? 'vergrendeld' : 'actief';
  let numIcon = (state.afgerond && state.geslaagd) ? '✓' : (state.afgerond && !state.geslaagd) ? '✗' : blok.nummer;
  let statusTekst = (state.afgerond && state.geslaagd)
    ? 'Geslaagd — ' + score + '/' + aantalVragen
    : (state.afgerond && !state.geslaagd)
      ? 'Niet geslaagd — ' + score + '/' + aantalVragen
      : isLocked ? 'Vergrendeld'
      : beantwoord + '/' + aantalVragen + ' beantwoord';

  el.innerHTML =
    '<div class="blok-header ' + (isLocked ? 'vergrendeld' : '') + '" onclick="toggleBlok(\'' + blok.id + '\', ' + isLocked + ')">' +
      '<div class="blok-num ' + numKlasse + '">' + numIcon + '</div>' +
      '<div class="blok-info">' +
        '<div class="blok-titel">' + blok.titel + '</div>' +
        '<div class="blok-sub">' + blok.theorie.length + ' theoriestukken · ' + aantalVragen + ' vragen</div>' +
      '</div>' +
      '<div class="blok-status">' + statusTekst + '</div>' +
    '</div>' +
    '<div class="blok-body' + (isOpen ? ' open' : '') + '" id="body-' + blok.id + '">' +
      renderBlokBody(blok, state) +
    '</div>';

  return el;
}

function renderBlokBody(blok, state) {
  let html = '';

  blok.theorie.forEach(t => {
    html += '<div class="theorie-blok">';
    html += '<div class="theorie-kop">' + t.kop + '</div>';
    html += '<div class="theorie-tekst">' + t.tekst + '</div>';
    if (t.lijst) {
      html += '<ul class="theorie-lijst">' + t.lijst.map(li => '<li>' + li + '</li>').join('') + '</ul>';
    }
    html += '</div>';
  });

  html += '<div class="vragen-label">Toetsvragen</div>';

  const letters = ['A', 'B', 'C', 'D'];
  state.vraagVolgorde.forEach((origIdx, displayIdx) => {
    const vraag = blok.vragen[origIdx];
    const antwoord = state.antwoorden[origIdx];
    const beantwoord = antwoord !== undefined;
    const optieVolgorde = state.optieVolgorde[origIdx];

    html += '<div class="vraag-wrap">';
    html += '<div class="vraag-meta">';
    html += '<span class="niveau-badge ' + vraag.niveau + '">' + (vraag.niveau === 'verdiepend' ? 'Verdiepend' : 'Basis') + '</span>';
    html += '<span class="vraag-num">Vraag ' + (displayIdx + 1) + ' van ' + blok.vragen.length + '</span>';
    html += '</div>';
    html += '<div class="vraag-tekst">' + vraag.tekst + '</div>';

    optieVolgorde.forEach((origOptIdx, displayOptIdx) => {
      const opt = vraag.opties[origOptIdx];
      let klasse = 'optie';
      if (beantwoord && !state.afgerond) {
        if (origOptIdx === antwoord) klasse += ' geselecteerd';
      } else if (beantwoord && state.afgerond) {
        klasse += ' disabled';
        if (opt.correct) klasse += ' correct';
        else if (origOptIdx === antwoord && !opt.correct) klasse += ' fout';
      }
      html += '<div class="' + klasse + '" onclick="kiesAntwoord(\'' + blok.id + '\',' + origIdx + ',' + origOptIdx + ')">';
      html += '<span class="optie-letter">' + letters[displayOptIdx] + '</span>';
      html += '<span>' + opt.tekst + '</span>';
      html += '</div>';
    });

    if (beantwoord && state.afgerond) {
      const isCorrect = vraag.opties[antwoord]?.correct;
      html += '<div class="feedback ' + (isCorrect ? 'correct' : 'fout') + '">';
      html += isCorrect ? vraag.feedback_correct : vraag.feedback_fout;
      html += '</div>';
      if (vraag.bron) {
        html += '<div class="bron">Bron: ' + vraag.bron + '</div>';
      }
    }
    html += '</div>';
  });

  const aantalVragen = blok.vragen.length;
  const aantalBeantwoord = Object.keys(state.antwoorden).length;
  const alleBeantwoord = aantalBeantwoord === aantalVragen;
  const score = berekenScore(blok, state);

  if (!state.afgerond) {
    html += '<div class="blok-footer">';
    html += '<div class="blok-score">' + aantalBeantwoord + ' van ' + aantalVragen + ' vragen ingevuld</div>';
    html += '<button class="btn-afronden" onclick="rondBlokAf(\'' + blok.id + '\')" ' + (alleBeantwoord ? '' : 'disabled') + '>Blok afronden →</button>';
    html += '</div>';
  } else {
    const pct = Math.round(score / aantalVragen * 100);
    const geslaagd = pct >= 80;
    html += '<div class="blok-resultaat ' + (geslaagd ? 'geslaagd' : 'gezakt') + '">';
    html += '<div class="resultaat-score">' + (geslaagd ? '✓' : '✗') + ' Score: ' + score + '/' + aantalVragen + ' (' + pct + '%)</div>';
    html += '<div class="resultaat-tekst">' + (geslaagd ? 'Geslaagd — minimaal 80% behaald.' : 'Niet geslaagd — minimaal 80% vereist. Probeer het blok opnieuw.') + '</div>';
    if (!geslaagd) {
      html += '<button class="btn-opnieuw" onclick="herlaadBlok(\'' + blok.id + '\')">Opnieuw proberen →</button>';
    }
    html += '</div>';
  }

  return html;
}

function berekenScore(blok, state) {
  return blok.vragen.reduce((acc, v, vi) => {
    const a = state.antwoorden[vi];
    return acc + (a !== undefined && v.opties[a]?.correct ? 1 : 0);
  }, 0);
}

// ─────────────────────────────────────────────────────────────
// ACTIES
// ─────────────────────────────────────────────────────────────
function toggleBlok(blokId, isLocked) {
  if (isLocked) return;
  openBlok = openBlok === blokId ? null : blokId;
  renderBlokken();
}

function kiesAntwoord(blokId, vraagIdx, optieIdx) {
  const state = blokState[blokId];
  if (state.afgerond) return;
  state.antwoorden[vraagIdx] = optieIdx;
  document.getElementById('body-' + blokId).innerHTML = renderBlokBody(
    CURSUS.blokken.find(b => b.id === blokId), state
  );
  renderVoortgang();

  const blokData = CURSUS.blokken.find(b=>b.id===blokId);
  fetch(`${SUPABASE_URL}/rest/v1/cursus_antwoorden`, {
    method: 'POST',
    headers: { 'apikey': ANON_KEY, 'Authorization': `Bearer ${ANON_KEY}`, 'Content-Type': 'application/json', 'Prefer': 'return=minimal' },
    body: JSON.stringify({
      therapeut_code: huidigeTherapeut.code,
      cursus_id: CURSUS.id,
      blok_id: blokId,
      vraag_id: blokData.vragen[vraagIdx].id,
      correct: blokData.vragen[vraagIdx].opties[optieIdx].correct
    })
  }).catch(e => console.warn('Antwoord opslaan mislukt:', e));
}

function rondBlokAf(blokId) {
  const blok = CURSUS.blokken.find(b => b.id === blokId);
  const state = blokState[blokId];
  const score = berekenScore(blok, state);
  const pct = Math.round(score / blok.vragen.length * 100);
  const geslaagd = pct >= 80;

  blokState[blokId].afgerond = true;
  blokState[blokId].geslaagd = geslaagd;

  if (geslaagd) {
    const idx = CURSUS.blokken.findIndex(b => b.id === blokId);
    const volgende = CURSUS.blokken[idx + 1];
    if (volgende) {
      openBlok = volgende.id;
      renderCursus();
      setTimeout(() => {
        const el = document.getElementById('blok-el-' + volgende.id);
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } else {
      renderCursus();
    }
  } else {
    blokState[blokId].afgerond = true;
    blokState[blokId].geslaagd = false;
    renderCursus();
    const container = document.getElementById('blokken-container');
    const resetDiv = document.createElement('div');
    resetDiv.id = 'cursus-reset';
    resetDiv.style.cssText = 'background:var(--red-light);border:1px solid var(--red-border);border-radius:12px;padding:20px 24px;margin-top:16px;text-align:center';
    resetDiv.innerHTML = '<div style="font-size:1rem;font-weight:700;color:var(--red);margin-bottom:8px">✗ Cursus niet geslaagd</div>' +
      '<div style="font-size:0.85rem;color:var(--red);margin-bottom:16px">U heeft niet alle blokken met minimaal 80% afgerond. U kunt de hele cursus opnieuw proberen.</div>' +
      '<button onclick="herlaadCursus()" style="background:var(--red);color:white;border:none;border-radius:8px;padding:10px 22px;font-family:Inter,sans-serif;font-size:0.88rem;font-weight:700;cursor:pointer">Cursus opnieuw beginnen →</button>';
    container.appendChild(resetDiv);
    setTimeout(() => {
      resetDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  }

  fetch(`${SUPABASE_URL}/rest/v1/cursus_voortgang`, {
    method: 'POST',
    headers: { 'apikey': ANON_KEY, 'Authorization': `Bearer ${ANON_KEY}`, 'Content-Type': 'application/json', 'Prefer': 'resolution=merge-duplicates,return=minimal' },
    body: JSON.stringify({
      therapeut_code: huidigeTherapeut.code,
      cursus_id: CURSUS.id,
      blok_id: blokId,
      score: score,
      geslaagd: geslaagd,
      datum_afgerond: new Date().toISOString()
    })
  }).catch(e => console.warn('Voortgang opslaan mislukt:', e));
}

function herlaadCursus() {
  const resetEl = document.getElementById('cursus-reset');
  if (resetEl) resetEl.remove();
  CURSUS.blokken.forEach(blok => {
    const vraagVolgorde = shuffleArr(blok.vragen.map((_, i) => i));
    const optieVolgorde = {};
    blok.vragen.forEach((v, vi) => {
      optieVolgorde[vi] = shuffleArr(v.opties.map((_, oi) => oi));
    });
    blokState[blok.id] = { antwoorden: {}, afgerond: false, geslaagd: false, vraagVolgorde, optieVolgorde };
  });
  openBlok = CURSUS.blokken[0].id;
  document.getElementById('cert-banner').classList.remove('zichtbaar');
  renderCursus();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function herlaadBlok(blokId) {
  const blok = CURSUS.blokken.find(b => b.id === blokId);
  const vraagVolgorde = shuffleArr(blok.vragen.map((_, i) => i));
  const optieVolgorde = {};
  blok.vragen.forEach((v, vi) => {
    optieVolgorde[vi] = shuffleArr(v.opties.map((_, oi) => oi));
  });
  blokState[blokId] = {
    antwoorden: {},
    afgerond: false,
    geslaagd: false,
    vraagVolgorde,
    optieVolgorde
  };
  openBlok = blokId;
  renderCursus();
  setTimeout(() => {
    const el = document.getElementById('blok-el-' + blokId);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 100);
}

function checkAllesAfgerond() {
  const alles = CURSUS.blokken.every(b => blokState[b.id]?.afgerond && blokState[b.id]?.geslaagd);
  if (alles) {
    document.getElementById('cert-tekst').textContent =
      huidigeTherapeut.naam + ' heeft de module ' + CURSUS.titel + ' succesvol doorlopen. Dit wordt automatisch vastgelegd in het EVN-systeem.';
    document.getElementById('cert-banner').classList.add('zichtbaar');
    if (huidigeTherapeut) {
      if (!huidigeTherapeut.afgerond) huidigeTherapeut.afgerond = [];
      if (!huidigeTherapeut.afgerond.includes(CURSUS.id)) {
        huidigeTherapeut.afgerond.push(CURSUS.id);
        sessionStorage.setItem('evn_therapeut', JSON.stringify(huidigeTherapeut));
      }
    }
  }
}

// Probeer sessie direct te herstellen (moet na alle functiedefinities staan)
herstelSessie();
