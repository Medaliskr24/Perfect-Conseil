# -*- coding: utf-8 -*-
# Perfect Conseil – générateur de site statique. Usage : python build.py  → dossier "site/"
# Pour publier un article : ajoutez une entrée EN HAUT de la liste ARTICLES, relancez, puis envoyez "site/" sur l'hébergeur.
import os, re, shutil
D = "https://www.perfect-conseil.com"
OUT = "site"

ARTICLES = [
 {"slug":"normes-globales-securite-alimentaire","date":"2025-01-24","cat":"Normes",
  "title":"Les normes globales de sécurité alimentaire : FSSC 22000, ISO 22000 et BRCGS",
  "desc":"Comparaison entre FSSC 22000, ISO 22000 et BRCGS pour les entreprises agroalimentaires.",
  "body":["La sécurité alimentaire est un enjeu crucial pour les entreprises du secteur agroalimentaire.","Collez ici la suite de l'article d'origine."]},
 {"slug":"analyse-risques-hse-8-etapes","date":"2025-01-14","cat":"Sécurité alimentaire",
  "title":"Comment réaliser une analyse des risques HSE en 8 étapes clés",
  "desc":"Protéger les employés, préserver les biens et minimiser l'impact sur l'environnement.",
  "body":["L'analyse des risques HSE (Hygiène, Sécurité, Environnement) permet de protéger les employés, de préserver les biens et de minimiser l'impact sur l'environnement.","Collez ici la suite de l'article d'origine."]},
]

IC = {
"fish":'<path d="M2 12c4-6 10-7 15-3l5-3v12l-5-3c-5 4-11 3-15-3z"/><circle cx="8" cy="11" r=".8"/>',
"shield":'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
"palm":'<path d="M12 22V10"/><path d="M12 10C9 6 5 6 3 9c3-1 6 0 9 1zM12 10c3-4 7-4 9-1-3-1-6 0-9 1zM12 10c-1-3 0-6 2-7-.5 3-1 5-2 7z"/>',
"factory":'<path d="M3 21V10l6 4v-4l6 4V6h3v15z"/>',
"leaf":'<path d="M5 19C5 9 11 4 20 4c0 9-5 15-15 15z"/><path d="M5 19c3-5 6-8 10-10"/>',
"award":'<circle cx="12" cy="9" r="6"/><path d="M8.5 14L7 22l5-3 5 3-1.5-8"/>',
"clip":'<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4h6v3H9zM8.5 13l2 2 4-4"/>',
"book":'<path d="M4 5h6a2 2 0 012 2v13a2 2 0 00-2-2H4zM20 5h-6a2 2 0 00-2 2v13a2 2 0 012-2h6z"/>',
"globe":'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
"mail":'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 7 9-7"/>',
"pin":'<path d="M12 21s7-6 7-12a7 7 0 10-14 0c0 6 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
"clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
"users":'<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-4 3-6 7-6s7 2 7 6"/><path d="M16 5a3.5 3.5 0 010 7M18 14c2.5.7 4 2.5 4 6"/>',
}
IC.update({
"facebook": '<path fill="currentColor" stroke="none" d="M13.5 21v-8h2.7l.4-3.2h-3.1V7.8c0-.9.3-1.5 1.6-1.5h1.7V3.4c-.3 0-1.3-.1-2.4-.1-2.4 0-4.1 1.5-4.1 4.2v2.3H7.5V13h2.8v8z"/>',
"x": '<path fill="currentColor" stroke="none" d="M17.8 3h3.1l-6.8 7.7L22 21h-6.2l-4.9-6.3L5.3 21H2.2l7.3-8.3L2 3h6.4l4.4 5.8zM16.7 19.2h1.7L7.3 4.7H5.5z"/>',
"linkedin": '<path fill="currentColor" stroke="none" d="M4.5 8.5h3.8V20H4.5zM6.4 3a2.2 2.2 0 110 4.4 2.2 2.2 0 010-4.4zM10.4 8.5H14v1.6h.1c.5-1 1.7-1.9 3.6-1.9 3.8 0 4.5 2.5 4.5 5.7V20h-3.8v-5.3c0-1.3 0-2.9-1.8-2.9s-2.1 1.4-2.1 2.8V20h-3.8z"/>',
"phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/>',
})
SPRITE = '<svg width="0" height="0" class="hd" aria-hidden="true">' + "".join('<symbol id="%s" viewBox="0 0 24 24">%s</symbol>' % (k, v) for k, v in IC.items()) + '</svg>'
def ic(n, c="i"): return '<svg class="%s" aria-hidden="true"><use href="#%s"/></svg>' % (c, n)

NAV = [("index.html","Accueil","h"),("a-propos.html","Qui sommes-nous","a"),("prestations.html","Prestations","p"),("actualites.html","Actualités","n"),("contact.html","Contact","c")]
SOC = [("Facebook","https://www.facebook.com/perfect.conseil/"),("Twitter","https://twitter.com/perfect_Conseil"),("LinkedIn","https://tn.linkedin.com/in/mohamed-skiker-642ba785")]
PAGES = []
PHONE = ""  # Numéro de téléphone à afficher en haut du site, ex. "+216 XX XXX XXX". Laissez vide pour le masquer.
BAN = {"a-propos.html": "b1", "parcours.html": "b6", "temoignages.html": "b4", "prestations.html": "b2", "systeme-qualite.html": "b7", "assistance-technique.html": "b8", "agrement-sanitaire.html": "b3", "actualites.html": "b2", "contact.html": "b4", "faq.html": "b3", "formation.html": "b1", "global-gap.html": "b6", "bio.html": "b5"}
INJ = {}

def page(f, title, desc, body, g="", extra=""):
    if f in BAN: body = body.replace('<div class="ph">', '<div class="ph pb %s">' % BAN[f], 1)
    for _m, _h in INJ.get(f, []): body = body.replace(_m, _h + _m, 1)
    R = "../" * f.count("/")
    PAGES.append((f, g))
    nav = "".join('<a href="%s%s"%s>%s</a>' % (R, u, ' class="on" aria-current="page"' if g == k else "", t) for u, t, k in NAV)
    url = D + "/" + ("" if f == "index.html" else f)
    h = ('<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
     '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src \'self\' data:; style-src \'self\'; script-src \'self\'; connect-src \'self\'; form-action mailto:; base-uri \'none\'; frame-ancestors \'none\'">'
     '<meta name="referrer" content="no-referrer"><title>' + title + '</title><meta name="description" content="' + desc + '">'
     '<link rel="canonical" href="' + url + '"><meta property="og:type" content="website"><meta property="og:locale" content="fr_FR"><meta property="og:title" content="' + title + '"><meta property="og:description" content="' + desc + '"><meta property="og:url" content="' + url + '"><meta property="og:image" content="' + D + '/img/og.jpg"><meta name="twitter:card" content="summary_large_image">'
     '<link rel="icon" type="image/png" href="' + R + 'favicon.png"><link rel="stylesheet" href="' + R + 'style.css">' + extra + '</head><body>' + SPRITE +
     '<a class="skip" href="#m">Aller au contenu</a>' + TOPBAR + '<header><div class="w hb"><a class="brand" href="' + R + 'index.html" aria-label="Perfect Conseil – accueil"><img src="' + R + 'img/logo.webp" width="208" height="46" alt="Perfect Conseil – plus loin ensemble"></a>'
     '<button class="bg" aria-label="Menu" aria-expanded="false" aria-controls="nv"><span></span></button><nav id="nv" aria-label="Navigation">' + nav + '<a class="btn s" href="' + R + 'contact.html">Rendez-vous</a></nav></div></header>'
     '<main id="m">' + body.replace("{R}", R) + '</main>'
     '<footer><div class="w fg"><div><b>Perfect Conseil</b><p>Bureau de conseil pour l\'agro-industrie en qualité, performance et gestion professionnelle.</p></div>'
     '<div><b>Prestations</b><a href="' + R + 'systeme-qualite.html">Système qualité</a><a href="' + R + 'assistance-technique.html">Assistance technique</a><a href="' + R + 'agrement-sanitaire.html">Agrément sanitaire</a></div>'
     '<div><b>Cabinet</b><a href="' + R + 'a-propos.html">Qui sommes-nous</a><a href="' + R + 'parcours.html">Historique et carrière</a><a href="' + R + 'temoignages.html">Témoignages</a><a href="' + R + 'confidentialite.html">Confidentialité</a></div>'
     '<div><b>Suivez-nous</b>' + "".join('<a href="%s" rel="noopener noreferrer">%s</a>' % (u, n) for n, u in SOC) + '</div></div>'
     '<div class="w cp">© <span id="y">2026</span> Perfect Conseil · Kélibia, Tunisie</div></footer><script src="' + R + 'site.js"></script></body></html>')
    os.makedirs(os.path.dirname(os.path.join(OUT, f)) or OUT, exist_ok=True)
    open(os.path.join(OUT, f), "w", encoding="utf-8").write(h)

def _tb():
    l = '<a href="mailto:m.skiker@perfect-conseil.com">' + ic("mail") + 'm.skiker@perfect-conseil.com</a>'
    if PHONE: l = '<a href="tel:%s">%s%s</a>' % (re.sub(r"[^+0-9]", "", PHONE), ic("phone"), PHONE) + l
    l += '<span class="h">' + ic("clock") + 'Lun – Sam · 8h00 – 17h30</span>'
    so = "".join('<a class="so" href="%s" target="_blank" rel="noopener noreferrer" aria-label="%s">%s</a>' % (u, n, ic(k)) for (n, u), k in zip(SOC, ["facebook", "x", "linkedin"]))
    return '<div class="tb"><div class="w tbi"><div class="tbl">' + l + '</div><div class="tbr">' + so + '</div></div></div>'
TOPBAR = _tb()

def banner(t, lead, icon, crumbs):
    c = " / ".join('<a href="{R}%s">%s</a>' % (u, n) for n, u in crumbs)
    return '<div class="ph"><div class="w"><p class="bc"><a href="{R}index.html">Accueil</a> / ' + c + '</p><div class="pt">' + ic(icon, "i big") + '<div><h1>' + t + '</h1><p>' + lead + '</p></div></div></div></div>'

def card(icon, t, p, href=None):
    inner = ic(icon) + '<h3>' + t + '</h3><p>' + p + '</p>' + ('<span class="mo">En savoir plus</span>' if href else "")
    return ('<a class="cd" href="{R}%s">%s</a>' % (href, inner)) if href else '<div class="cd">' + inner + '</div>'

def pcard(key, icon, t, p, href=None):
    inner = '<img class="pi" src="{R}img/services/%s.webp" alt="%s" width="506" height="380" loading="lazy" decoding="async"><div class="pb2">' % (key, t) + ic(icon) + '<h3>' + t + '</h3><p>' + p + '</p>' + ('<span class="mo">En savoir plus</span>' if href else "") + '</div>'
    return ('<a class="cd pc" href="{R}%s">%s</a>' % (href, inner)) if href else '<div class="cd pc">' + inner + '</div>'
CTA = '<section class="cta"><div class="w"><h2>Un projet de certification ou de mise à niveau ?</h2><p>Parlons-en : réponse rapide, sans engagement.</p><a class="btn" href="{R}contact.html">Obtenir un rendez-vous</a></div></section>'


_CL = [["conserves-thon", "Conserves de thon", [210, 100]], ["gecop", "GECOP – General Conserve de Poisson", [210, 100]], ["sfbt", "SFBT Mahdia", [210, 100]], ["jenhani", "Groupe Jenhani – NCK", [210, 100]], ["haifa", "Haifa", [210, 100]], ["le-marin", "Le Marin", [210, 100]], ["zgolli", "Zgolli", [210, 100]], ["capten", "Capten Sarl", [210, 100]], ["datia", "Datia", [210, 100]], ["phenix", "SARL Phenix", [210, 100]], ["skouri", "Skouri d'exportation", [210, 100]], ["stb", "STB – Tolga El-Baraka", [210, 100]], ["sud-dattes", "Sud Dattes – Maison Zendaoui", [210, 100]], ["al-badr", "Al Badr", [210, 100]], ["bkfood", "BK Food", [210, 100]], ["sidi-daoud", "Thon Sidi Daoud", [210, 100]], ["haddoud", "Haddoud Salim Company", [210, 100]], ["horchani", "Horchani Dattes", [210, 100]], ["taooc", "TAOOC", [210, 100]], ["la-galita", "La Galita", [210, 100]]]
def _cards(items):
    return "".join('<div class="lc"><img src="{R}img/clients/%s.webp" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"></div>' % (a, w, h, n) for a, n, (w, h) in items)
CLIENTS = '<div class="cs" role="region" aria-roledescription="carousel" aria-label="Nos clients"><button class="cb pv2" aria-label="Clients précédents">‹</button><div class="ct" tabindex="0">' + _cards(_CL) + '</div><button class="cb nx2" aria-label="Clients suivants">›</button></div>'


G_SEA = '<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label="La mer à Kélibia"><defs><linearGradient id="sk1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fc0f0"/><stop offset=".75" stop-color="#ffe6b8"/></linearGradient></defs><rect width="400" height="300" fill="url(#sk1)"/><circle cx="290" cy="118" r="34" fill="#fff3c4"/><path class="cl" d="M30 70q15-18 38-8 14-14 34 2 22-2 20 14H30z" fill="#fff" opacity=".85"/><path d="M80 52q8-8 16 0M102 64q6-6 12 0M300 60q8-8 16 0" stroke="#fff" fill="none" stroke-width="2"/><rect y="150" width="400" height="150" fill="#2a86c8"/><path class="wv1" d="M-40 172q40-14 80 0t80 0 80 0 80 0 80 0 80 0V300H-40z" fill="#3a9bd9"/><g class="bt"><path d="M140 176h92l-14 20h-64z" fill="#7a52a6"/><path d="M186 176V122l34 50z" fill="#fff"/><path d="M180 176V134l-26 38z" fill="#ffd878"/></g><path class="wv2" d="M-40 204q40-14 80 0t80 0 80 0 80 0 80 0 80 0V300H-40z" fill="#2977b9"/><path class="wv1 w3" d="M-40 242q40-14 80 0t80 0 80 0 80 0 80 0 80 0V300H-40z" fill="#1f5f96"/></svg>'
G_OLIVE = '<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Oliviers"><defs><linearGradient id="sk2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe8ff"/><stop offset="1" stop-color="#f4ffe0"/></linearGradient><path id="lf1" d="M0 0q14-10 34 0-14 10-34 0z"/></defs><rect width="400" height="300" fill="url(#sk2)"/><circle cx="90" cy="70" r="26" fill="#fff6c9"/><path d="M0 190q100-60 200-20t200-30V300H0z" fill="#9ccc86"/><path d="M0 235q120-50 230-10t170-15V300H0z" fill="#5f9f58"/><path d="M168 250c8-40 2-70-6-96l22-2c-2 30 6 60 14 98z" fill="#6b4a2c"/><g class="tr3"><ellipse cx="170" cy="130" rx="74" ry="46" fill="#7f9f62"/><ellipse cx="130" cy="150" rx="48" ry="30" fill="#93b273"/><ellipse cx="215" cy="150" rx="52" ry="30" fill="#6f9055"/></g><g class="sw1"><path d="M400 70q-110 10-190 70" stroke="#6b4a2c" stroke-width="5" fill="none" stroke-linecap="round"/>'
_ol = "".join('<use href="#lf1" transform="translate(%d %d) rotate(%d)" fill="%s"/>' % (x, y, r, c) for x, y, r, c in [(372,72,200,"#4f8a3c"),(350,80,-25,"#5f9f48"),(326,92,205,"#4f8a3c"),(302,104,-20,"#6aa852"),(276,116,210,"#4f8a3c"),(252,130,-15,"#5f9f48"),(228,142,215,"#6aa852")])
_ov = "".join('<ellipse cx="%d" cy="%d" rx="7" ry="9" fill="#3d4d25"/><ellipse cx="%d" cy="%d" rx="2" ry="3" fill="#7e9a52"/>' % (x, y, x-2, y-3) for x, y in [(340,100),(312,114),(288,128),(262,142),(358,92)])
G_OLIVE += _ol + _ov + '</g></svg>'
G_DATE = '<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Palmeraie"><defs><linearGradient id="sk3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7c5fb8"/><stop offset=".55" stop-color="#ffb870"/><stop offset="1" stop-color="#ffe3a0"/></linearGradient></defs><rect width="400" height="300" fill="url(#sk3)"/><circle cx="110" cy="150" r="40" fill="#fff0b8"/><path d="M0 230q100-50 210-12t190-20V300H0z" fill="#d49a4a"/><path d="M0 262q140-40 250-8t150-10V300H0z" fill="#b87a30"/><g class="pm"><path d="M250 270c14-60 4-110-8-150" stroke="#5a3a14" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M242 120q-70-50-150-10 70-6 150 10zM242 120q60-60 140-25-66-4-140 25zM242 120q-24-56 8-96 2 58-8 96zM242 120q-82 8-122 64 66-34 122-64zM242 120q74 6 112 66-58-36-112-66z" fill="#2f7a46"/><circle cx="236" cy="134" r="7" fill="#f2a93a"/><circle cx="250" cy="140" r="7" fill="#f2a93a"/><circle cx="240" cy="150" r="7" fill="#e08f28"/></g></svg>'
G_SEA = '<img src="{R}img/gallery/sea.webp" alt="Bateaux de pêche dans le port" width="800" height="600" loading="lazy" decoding="async">'
G_OLIVE = '<img src="{R}img/gallery/olive.webp" alt="Branche d\'olivier" width="800" height="600" loading="lazy" decoding="async">'
G_DATE = '<img src="{R}img/gallery/dates.webp" alt="Palmeraie et régimes de dattes" width="800" height="600" loading="lazy" decoding="async">'
G_CONS = '<img src="{R}img/gallery/conserves.webp" alt="Chaîne de conserves de poisson" width="800" height="600" loading="lazy" decoding="async">'
G_FRUIT = '<img src="{R}img/gallery/fruits.webp" alt="Fruits sur une ligne de transformation" width="640" height="480" loading="lazy" decoding="async">'
G_BIOI = '<img src="{R}img/gallery/bio.webp" alt="Légumes biologiques" width="640" height="480" loading="lazy" decoding="async">'
GALLERY = '<section class="sec"><div class="w"><h2>Nos produits et terrains d\'intervention</h2><div class="gl">' + "".join('<figure class="gi">%s<figcaption>%s</figcaption></figure>' % (g, c) for g, c in [(G_SEA, "Produits de la mer"), (G_CONS, "Conserves de poisson"), (G_OLIVE, "Olives et huile d'olive"), (G_DATE, "Palmeraies et dattes"), (G_FRUIT, "Fruits et légumes"), (G_BIOI, "Produits bio")]) + '</div></div></section>'

exec(open("assets/sections.py", encoding="utf-8").read())
# ---------- ACCUEIL (slider) ----------
S1 = '<svg class="sc" viewBox="0 0 480 360" aria-hidden="true"><circle class="sun" cx="370" cy="85" r="44"/><path class="wa" d="M0 250q60-30 120 0t120 0 120 0 120 0V360H0z"/><use href="#fish" class="fs a" x="60" y="150" width="120" height="120"/><use href="#fish" class="fs b" x="210" y="200" width="80" height="80"/><use href="#fish" class="fs c" x="300" y="140" width="64" height="64"/><path class="wb" d="M0 295q60-30 120 0t120 0 120 0 120 0V360H0z"/></svg>'
S2 = '<svg class="sc" viewBox="0 0 480 360" aria-hidden="true"><circle class="sun" cx="110" cy="80" r="40"/><path class="gr" d="M0 320q240-50 480 0V360H0z"/><path class="tk" d="M250 330c14-60 0-120-12-190"/><path class="fr" d="M238 140q-80-60-170-10 80-5 170 10zM238 140q60-70 150-30-70 0-150 30zM238 140q-30-60 10-100 0 60-10 100zM238 140q-90 10-130 70 70-40 130-70zM238 140q80 0 120 70-60-40-120-70z"/><circle class="dt" cx="232" cy="156" r="7"/><circle class="dt" cx="246" cy="162" r="7"/><circle class="dt" cx="238" cy="172" r="7"/><circle class="dt" cx="225" cy="170" r="6"/></svg>'
S3 = '<svg class="sc" viewBox="0 0 480 360" aria-hidden="true"><circle class="rg" cx="240" cy="180" r="150"/><circle class="rg r2" cx="240" cy="180" r="110"/><use href="#shield" class="sh" x="150" y="90" width="180" height="180"/><use href="#award" class="mi" x="360" y="60" width="56" height="56"/><use href="#clip" class="mi" x="50" y="230" width="56" height="56"/><use href="#globe" class="mi" x="370" y="250" width="56" height="56"/></svg>'
S1 = S2 = S3 = ""
def slide(c, t, p, b, s, on=""):
    return '<div class="sl %s%s"><div class="w sg"><div class="tx"><h1>%s</h1><p>%s</p><a class="btn" href="%s">%s</a> <a class="btn o" href="contact.html">Rendez-vous</a></div>%s</div></div>' % (c, on, t, p, b[0], b[1], s)
home = ('<section class="hero" aria-roledescription="carousel" aria-label="Présentation">'
 + slide("s1", "Votre sécurité alimentaire, certifiée.", "ISO 22000, FSSC 22000, IFS, BRC : nous vous accompagnons de la mise en place jusqu'au jour de l'audit.", ("systeme-qualite.html", "Système qualité"), S1, " on")
 + slide("s2", "Du thon aux dattes, des unités qui tournent.", "Conserves de poisson, anchois, conditionnement des dattes : conception des plans, procédés et organisation du travail.", ("assistance-technique.html", "Assistance technique"), S2)
 + slide("s3", "Agrément sanitaire UE, dossier géré de bout en bout.", "Plan d'hygiène, manuel d'autocontrôle et suivi auprès des services vétérinaires.", ("agrement-sanitaire.html", "Agrément sanitaire"), S3)
 + '<div class="ctl"><button class="pv" aria-label="Précédent">‹</button><span class="dots"></span><button class="nx" aria-label="Suivant">›</button></div></section>'
 '<section class="band"><div class="w chips"><span>' + ic("shield") + 'ISO 22000</span><span>' + ic("shield") + 'FSSC 22000</span><span>' + ic("award") + 'IFS</span><span>' + ic("award") + 'BRC</span><span>' + ic("clip") + 'ISO 9001</span><span>' + ic("leaf") + 'ISO 14001</span><span>' + ic("globe") + 'Global GAP</span><span>' + ic("clip") + 'HACCP</span></div></section>'
 '<section class="sec"><div class="w"><h2>Nos principaux domaines d\'intervention</h2><p class="lead">Perfect Conseil, cabinet de conseil en agroalimentaire : systèmes qualité et sécurité alimentaire, amélioration de la performance et organisation du travail, avec une expérience de terrain depuis 1998.</p><div class="gd pcs">'
 + pcard("systemes", "shield", "Systèmes qualité", "Accompagnement à la certification des systèmes de management de la sécurité des denrées alimentaires et de la qualité.", "systeme-qualite.html")
 + pcard("assistance", "factory", "Assistance technique", "Conception des plans, amélioration de la qualité, paramétrage des procédés et organisation du travail.", "assistance-technique.html")
 + pcard("agrement", "fish", "Agrément sanitaire", "Plan conforme aux exigences d'hygiène, manuel d'autocontrôle, gestion du dossier auprès des services.", "agrement-sanitaire.html")
 + pcard("formation", "book", "Formation", "Audit interne, audit fournisseur, BRC, IFS, cahier des charges, conception hygiénique, HACCP selon ISO 22000.", "formation.html")
 + pcard("globalgap", "globe", "Global GAP", "Bonnes pratiques agricoles pour garantir la sécurité maximale des produits chez les distributeurs.", "global-gap.html")
 + pcard("bio", "leaf", "BIO", "Certification Agriculture Biologique : se démarquer et rassurer les consommateurs.", "bio.html")
 + '</div></div></section>' + GALLERY + '<section class="sec alt"><div class="w"><h2>Ils nous ont fait confiance</h2>' + CLIENTS + ''
 '<blockquote>« Au cours de la certification FSSC 22000, vous avez contribué à faire aboutir tous nos efforts. Votre réactivité et votre capacité d\'adaptation sont des atouts que j\'ai grandement appréciés. »<cite>Souad Djeffal, Tolga Agro Food</cite></blockquote><a href="temoignages.html">Tous les témoignages</a></div></section>' + CTA)
LD = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"ProfessionalService","name":"Perfect Conseil","slogan":"Plus Loin Ensemble","url":"' + D + '","email":"m.skiker@perfect-conseil.com","address":{"@type":"PostalAddress","streetAddress":"Rte 6071 Lahouache","addressLocality":"Kélibia","postalCode":"8090","addressRegion":"Nabeul","addressCountry":"TN"},"geo":{"@type":"GeoCoordinates","latitude":36.8402,"longitude":11.0613},"openingHours":"Mo-Sa 08:00-17:30","sameAs":["https://www.facebook.com/perfect.conseil/","https://twitter.com/perfect_Conseil","https://tn.linkedin.com/in/mohamed-skiker-642ba785"]}</script>'
page("index.html", "Perfect Conseil – Conseil en agroalimentaire en Tunisie – Plus Loin Ensemble", "Bureau de conseil en agroalimentaire en Tunisie : ISO 22000, FSSC 22000, IFS, BRC, HACCP, assistance technique et agrément sanitaire.", home.replace('href="systeme', 'href="{R}systeme').replace('href="assistance', 'href="{R}assistance').replace('href="agrement', 'href="{R}agrement').replace('href="contact', 'href="{R}contact').replace('href="temoig', 'href="{R}temoig'), "h", LD + '<link rel="preload" as="image" href="img/slides/s1.webp" fetchpriority="high">')

# ---------- QUI SOMMES-NOUS ----------
def sub(g, cur):
    return '<div class="tabs">' + "".join('<a href="{R}%s"%s>%s</a>' % (u, ' class="on"' if u == cur else "", t) for u, t in [("a-propos.html", "Présentation"), ("parcours.html", "Historique et carrière"), ("temoignages.html", "Témoignages")]) + '</div>'
page("a-propos.html", "Qui sommes-nous – Perfect Conseil, cabinet de conseil agroalimentaire", "Perfect Conseil, cabinet de conseil agroalimentaire en Tunisie : notre mission, notre approche et notre façon de travailler avec nos clients.",
 banner("Qui sommes-nous", "Nous pouvons vous aider à développer votre entreprise.", "users", []) + '<section class="sec"><div class="w nr">' + sub("a", "a-propos.html") +
 '<p>Perfect Conseil est un cabinet de conseil agroalimentaire enregistré au registre du commerce (MF : 157598/Z AM 000). Nous avons commencé avec de petits projets ; aujourd\'hui nous accompagnons des clients de plusieurs pays, grâce à la confiance qu\'ils nous accordent.</p><h2>Notre mission</h2><ul class="ck"><li>Travailler moins d\'heures et gagner plus.</li><li>Attirer et retenir des clients de qualité.</li><li>Mieux gérer son temps pour en faire plus en moins de temps.</li><li>Affûter ses compétences de leadership.</li><li>Réduire les dépenses sans sacrifier la qualité.</li><li>Automatiser l\'entreprise pour pouvoir s\'absenter des jours, des semaines, voire des mois.</li></ul>'
 '<p>Nous abordons l\'activité de chaque client comme si elle était la nôtre. Un cabinet de conseil doit être plus qu\'un conseiller : nous nous mettons à la place de nos clients, alignons nos incitations sur leurs objectifs et collaborons pour libérer le plein potentiel de leurs activités.</p><p>La bonne approche est nécessaire pour le bon résultat : nous adaptons nos conseils d\'expert à votre façon de travailler.</p></div></section>' + CTA, "a")

page("parcours.html", "Historique et carrière – Perfect Conseil", "Formations, certificats et parcours professionnel de Mohamed Skiker, ingénieur agroalimentaire, de la production au conseil.",
 banner("Historique et carrière", "Plus de vingt ans de terrain en production, qualité et conseil.", "award", [("Qui sommes-nous", "a-propos.html")]) + '<section class="sec"><div class="w nr">' + sub("a", "parcours.html") +
 '<h2>Formations et certificats</h2><ul class="ck"><li>Master food engineer – Institut National Agronomique de Tunisie</li><li>ISO 9001 – Moody, mars 2002</li><li>Techniques d\'organisation du travail – FIDUNION (CNAM), novembre 2004</li><li>ISO 22000 – SGS, février 2006</li></ul><h2>Parcours</h2>'
 '<div class="tl"><b>1998 – 2002 · Directeur de production, Horchani Dattes</b><p>Planification et réalisation de la production, gestion du système qualité, réclamations et audits clients.</p></div>'
 '<div class="tl"><b>2002 – 2009 · Responsable qualité, ABCo</b><p>Mise en place des systèmes ISO 22000 et ISO 9001, contrôle qualité produit, gestion des réclamations clients.</p></div>'
 '<div class="tl"><b>2009 – 2010 · Directeur, SODEXPO, Gabès</b><p>Mise à niveau de l\'unité de valorisation des fruits et légumes, chef de projet, production, achat de dattes.</p></div>'
 '<div class="tl"><b>2010 – 2013 · Consultant, euroconsultants, Maroc</b><p>Encadrement d\'unités de valorisation des dattes, formation, création de nouvelles unités, mise à niveau.</p></div>'
 '<p><b>Spécialités :</b> systèmes qualité, production, management, HACCP.</p></div></section>' + CTA, "a")

page("temoignages.html", "Témoignages clients – Perfect Conseil", "Ce que nos clients disent de nous : Tolga Agro Food, Socofel Export et d'autres entreprises accompagnées vers la certification.",
 banner("Témoignages clients", "Ce que nos clients disent de nous.", "users", [("Qui sommes-nous", "a-propos.html")]) + '<section class="sec"><div class="w nr">' + sub("a", "temoignages.html") +
 '<blockquote>« Je tenais à vous exprimer mes très vifs remerciements pour le professionnalisme dont vous avez fait preuve pour votre accompagnement de mise en place de système qualité. Au cours de la certification FSSC 22000, vous avez contribué à faire aboutir tous nos efforts précédents. Votre réactivité, votre capacité d\'adaptation sont des atouts que j\'ai grandement appréciés. Je vous sais gré également de la discrétion avec laquelle vous avez réalisé ce travail. Sachez que je continuerai avec un très grand plaisir à faire appel à vos compétences. »<cite>Mme Souad Djeffal, responsable management qualité, Tolga Agro Food</cite></blockquote>'
 '<blockquote>« Nous tenons à remercier M. Skiker Mohamed, auditeur, qui nous a accompagnés durant tout le processus de notre certification ISO 22000 et FSSC 22000 : professionnalisme, rigueur et abnégation, sans oublier le côté humain. Nous recommandons vivement votre accompagnement à toute société souhaitant une certification. »<cite>M. et Mme Sahour, fondateurs, Socofel Export</cite></blockquote></div></section><section class="sec alt"><div class="w"><h2>Nos références</h2>' + CLIENTS + '</div></section>' + CTA, "a")

# ---------- PRESTATIONS ----------
page("prestations.html", "Prestations – Système qualité, assistance technique, agrément sanitaire | Perfect Conseil", "Nos prestations en agroalimentaire : certification ISO 22000, FSSC 22000, IFS, BRC, assistance technique aux unités et agrément sanitaire UE.",
 banner("Prestations", "Experts en sécurité alimentaire, nous suivons les dernières évolutions réglementaires et fournissons des services adaptés et de haute qualité.", "clip", []) + '<section class="sec"><div class="w"><div class="gd">'
 + card("shield", "Système qualité", "ISO 22000, FSSC 22000, IFS, BRC, ISO 9001, ISO 14001, Global Gap, HACCP.", "systeme-qualite.html")
 + card("factory", "Assistance technique", "Conserves de poisson, anchois, conditionnement des dattes, organisation du travail.", "assistance-technique.html")
 + card("fish", "Agrément sanitaire", "Agrément sanitaire UE des produits de pêche : plan, autocontrôle, dossier.", "agrement-sanitaire.html") + card("book", "Formation", "Audit interne, audit fournisseur, BRC, IFS, HACCP.", "formation.html") + card("globe", "Global GAP", "Bonnes pratiques agricoles et accès aux marchés.", "global-gap.html") + card("leaf", "BIO", "Certification Agriculture Biologique.", "bio.html") + '</div></div></section>' + CTA, "p")

STD = [("iso-22000","shield","ISO 22000 – Sécurité des denrées alimentaires","Garantir la sûreté des produits, améliorer la notoriété par la qualité, améliorer continuellement les performances en sécurité alimentaire et le management interne."),
("fssc-22000","shield","FSSC 22000 – Food Safety System Certification","Norme reconnue internationalement, souple et applicable à toute la chaîne d'approvisionnement, intégrable à l'ISO 9001, avec un cadre d'engagement de la direction et d'amélioration continue."),
("iso-9001","clip","ISO 9001 – Management de la qualité","Accès facilité aux marchés mondiaux, avantage concurrentiel face aux concurrents non certifiés, meilleure productivité et satisfaction client, moins de dépenses liées à l'inefficacité."),
("iso-14001","leaf","ISO 14001 – Management environnemental","Prévention des risques environnementaux, réponse aux exigences légales, économies d'énergie, amélioration continue, avantage concurrentiel et nouveaux marchés."),
("brc","award","BRC – British Retail Consortium","Accès aux marchés étrangers, meilleures relations avec les distributeurs, transparence, confiance des clients, maîtrise des processus internes et réduction des risques."),
("ifs","award","IFS – International Featured Standards","Renommée par la qualité des produits, relations commerciales facilitées, moins d'audits, meilleure répartition des ressources et veille réglementaire."),
("haccp","clip","HACCP – Analyse des dangers, points critiques","Identification systématique des dangers biologiques, chimiques et physiques, mesures préventives et vérification de la maîtrise du risque."),
("global-gap","globe","Global GAP – Bonnes pratiques agricoles","Valeur ajoutée par un référentiel reconnu, nouveaux marchés et distributeurs, moindre exposition aux risques de réputation, numéro GGN pour la traçabilité.")]
page("systeme-qualite.html", "Système qualité : ISO 22000, FSSC 22000, IFS, BRC, ISO 9001 – Perfect Conseil", "Accompagnement à la certification ISO 22000, FSSC 22000, IFS, BRC, ISO 9001, ISO 14001, HACCP et Global Gap en Tunisie.",
 banner("Système qualité", "La qualité, c'est ce que le client y trouve et ce pour quoi il est prêt à payer. Tout le reste est gaspillage.", "shield", [("Prestations", "prestations.html")]) + '<section class="sec"><div class="w"><p class="lead">La qualité est l\'aptitude à répondre aux exigences des clients, explicites ou implicites. Nous vous accompagnons vers la certification de votre système de management de la sécurité des denrées alimentaires et de la qualité.</p><div class="gd">'
 + "".join('<div class="cd" id="%s">%s<h3>%s</h3><p>%s</p></div>' % (i, ic(c), t, p) for i, c, t, p in STD) + '</div></div></section>' + CTA, "p")
page("assistance-technique.html", "Assistance technique – conserves de poisson, anchois, dattes | Perfect Conseil", "Conception des plans, amélioration de la qualité, paramétrage des procédés et organisation du travail pour conserveries, anchois et dattes.",
 banner("Assistance technique", "Conception des plans, amélioration de la qualité, paramétrage des procédés et opérationnalisation des unités.", "factory", [("Prestations", "prestations.html")]) + '<section class="sec"><div class="w"><div class="gd">'
 + card("fish", "Conserves de produits de pêche", "Thon, sardines, maquereaux…") + card("fish", "Semi-conserves de produits salés", "Anchois.") + card("palm", "Conditionnement des dattes", "Organisation des lignes et qualité.") + card("users", "Organisation du travail", "Études des postes et formation.") + '</div></div></section>' + CTA, "p")
page("agrement-sanitaire.html", "Agrément sanitaire UE des produits de pêche – Perfect Conseil", "Conception du plan d'hygiène, manuel d'autocontrôle et gestion du dossier d'agrément sanitaire auprès de la Direction Générale des Services Vétérinaires.",
 banner("Agrément sanitaire", "Agrément sanitaire UE des produits de pêche.", "fish", [("Prestations", "prestations.html")]) + '<section class="sec"><div class="w nr"><p>Pour vendre, certains établissements doivent légalement présenter un agrément sanitaire, délivré par les services vétérinaires et spécifique à l\'activité ou aux produits mis sur le marché.</p><p>Le dossier, dont le Plan de Maîtrise Sanitaire (PMS), doit présenter l\'ensemble des conditions de fonctionnement et refléter exactement la réalité. L\'agrément est subordonné à une inspection sur site ne relevant aucune non-conformité majeure.</p><p>Il peut être une condition indispensable pour créer, reprendre ou développer une société, mais aussi un atout face à la concurrence.</p><h2>Nous pouvons vous aider à</h2><ul class="ck"><li>Concevoir le plan conformément aux exigences d\'hygiène</li><li>Élaborer le manuel d\'autocontrôle</li><li>Gérer le dossier auprès de la Direction Générale des Services Vétérinaires</li></ul></div></section>' + CTA, "p")

# ---------- ACTUALITES ----------
def fd(d):
    y, m, j = d.split("-"); return "%d %s %s" % (int(j), ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"][int(m)-1], y)
import json
_J = os.path.join(OUT, "data", "articles.json")
if os.path.exists(_J): ARTICLES = json.load(open(_J, encoding="utf-8"))
for _a in ARTICLES: _a.setdefault("html", "".join("<p>%s</p>" % p for p in _a.get("body", [])))
if not os.path.exists(_J):
    os.makedirs(os.path.dirname(_J), exist_ok=True)
    json.dump([{k: _a[k] for k in ("slug","date","cat","title","desc","html")} for _a in ARTICLES], open(_J, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
arts = sorted(ARTICLES, key=lambda a: a["date"], reverse=True)
def _acard(a):
    th = '<img class="th" src="{R}%s" alt="" width="200" height="112" loading="lazy">' % a["img"] if a.get("img") else ""
    return '<a class="cd ar" href="{R}actualites/%s.html">%s<span class="mt">%s · %s</span><h3>%s</h3><p>%s</p></a>' % (a["slug"], th, fd(a["date"]), a["cat"], a["title"], a["desc"])
def _cover(a):
    return '<figure class="cv"><img src="{R}%s" alt="%s" width="1200" height="675"></figure>' % (a["img"], a["title"]) if a.get("img") else ""
page("actualites.html", "Actualités – normes, sécurité alimentaire | Perfect Conseil", "Articles et actualités de Perfect Conseil sur les normes, la sécurité alimentaire et la qualité en agroalimentaire.",
 banner("Actualités", "Normes, sécurité alimentaire, qualité : nos derniers articles.", "book", []) + '<section class="sec"><div class="w nr" id="al" data-s="1"><!--LIST-->' + "".join(_acard(a) for a in arts) + '<!--/LIST--></div></section>', "n")
for a in arts:
    page("actualites/%s.html" % a["slug"], a["title"] + " | Perfect Conseil", a["desc"],
     banner(a["title"], fd(a["date"]) + " · " + a["cat"], "book", [("Actualités", "actualites.html")]) + '<article class="sec"><div class="w nr art">' + _cover(a) + a["html"] + '<p><a href="{R}actualites.html">← Toutes les actualités</a></p></div></article>' + CTA, "n")

# ---------- CONTACT / CONFIDENTIALITE ----------
_SUJ = ["Certification ISO 22000 / FSSC 22000", "IFS / BRC", "ISO 9001 / ISO 14001", "HACCP / Global GAP", "Assistance technique", "Agrément sanitaire", "Formation", "Autre demande"]
_SOCL = "".join('<a class="sp" href="%s" rel="noopener noreferrer" target="_blank">%s</a>' % (u, n) for n, u in SOC)
_MAP = ('<svg viewBox="0 0 400 230" class="mapc" role="img" aria-label="Kélibia, Nabeul"><defs><linearGradient id="mg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#cfe9fb"/><stop offset="1" stop-color="#9fd0f2"/></linearGradient></defs>'
 '<rect width="400" height="230" fill="url(#mg)"/><path d="M0 70q70-30 130 0t110 40q40 30 20 70l-20 50H0z" fill="#f1e4bd"/><path d="M0 70q70-30 130 0t110 40q40 30 20 70" fill="none" stroke="#fff" stroke-width="4" opacity=".8"/>'
 '<path d="M20 140h200M60 90v140M130 100v130M190 130v100" stroke="#fff" stroke-width="3" opacity=".7"/><path class="wv1" d="M240 60q20-10 40 0t40 0 40 0M270 90q20-10 40 0t40 0 40 0M250 30q20-10 40 0t40 0" fill="none" stroke="#fff" stroke-width="3" opacity=".7"/>'
 '<g><circle class="pl" cx="190" cy="132" r="10"/><circle class="pl p2" cx="190" cy="132" r="10"/><path d="M190 134s-17-19-17-31a17 17 0 0134 0c0 12-17 31-17 31z" fill="#7a52a6"/><circle cx="190" cy="103" r="6.5" fill="#fff"/></g>'
 '<text x="206" y="152" font-size="15" font-weight="700" fill="#14233f" font-family="Georgia,serif">Kélibia</text></svg>')
page("contact.html", "Contact – Perfect Conseil, Kélibia, Nabeul, Tunisie", "Contactez Perfect Conseil : Rte 6071 Lahouache, Kélibia 8090, Nabeul. Ouvert du lundi au samedi, 8h00 – 17h30.",
 banner("Contactez-nous", "Parlons de votre projet : certification, mise à niveau, formation.", "mail", []) + '<section class="sec"><div class="w ct2"><div>'
 + '<div class="ic2">' + ic("pin") + '<div><b>Adresse</b><p>Rte 6071 Lahouache, Kélibia 8090, Nabeul, Tunisie</p></div></div>'
 + '<div class="ic2">' + ic("mail") + '<div><b>E-mail</b><p><a href="mailto:m.skiker@perfect-conseil.com">m.skiker@perfect-conseil.com</a><br><a href="mailto:skiker.m.tc5b@gmail.com">skiker.m.tc5b@gmail.com</a></p></div></div>'
 + '<div class="ic2">' + ic("clock") + '<div><b>Horaires</b><p>Lundi au samedi, 8h00 – 17h30<br>Dimanche : fermé</p></div></div>'
 + _MAP + '<p><a class="btn" href="https://www.google.com/maps?q=36.8402,11.0613" target="_blank" rel="noopener noreferrer">Ouvrir dans Google Maps</a></p><div class="sps">' + _SOCL + '</div></div>'
 + '<form id="cf" class="cform" novalidate><h2>Envoyez-nous un message</h2><div class="fr"><div><label for="cn">Nom *</label><input id="cn" autocomplete="name" maxlength="80"></div><div><label for="cc">E-mail ou téléphone *</label><input id="cc" maxlength="80"></div></div>'
 '<div class="fr"><div><label for="cs">Société</label><input id="cs" autocomplete="organization" maxlength="80"></div><div><label for="cj">Sujet</label><select id="cj">' + "".join("<option>%s</option>" % o for o in _SUJ) + '</select></div></div>'
 '<label for="cm">Message *</label><textarea id="cm" rows="6" maxlength="2000"></textarea><p><button class="btn" type="submit">Envoyer le message</button></p><p id="cst" role="status" aria-live="polite"></p></form></div></section>', "c")

page("confidentialite.html", "Politique de confidentialité – Perfect Conseil", "Ce site n'utilise ni cookies ni outils de suivi.", banner("Politique de confidentialité", "Aucun cookie, aucun suivi.", "shield", []) + '<section class="sec"><div class="w nr"><p>Ce site ne dépose aucun cookie et n\'utilise aucun outil de suivi. Les informations saisies dans le formulaire de contact servent uniquement à répondre à votre demande.</p></div></section>', "")

# ---------- MODELE D'ARTICLE (pour le tableau de bord) ----------
page("actualites/__tpl.html", "§T§ | Perfect Conseil", "§D§", banner("§T§", "§DATE§ · §C§", "book", [("Actualités", "actualites.html")]) + '<article class="sec"><div class="w nr art">§IMG§§B§<p><a href="{R}actualites.html">← Toutes les actualités</a></p></div></article>' + CTA, "n", '<script type="application/ld+json">§J§</script>')
PAGES.pop(); _tp = os.path.join(OUT, "actualites", "__tpl.html"); TPL = open(_tp, encoding="utf-8").read(); os.remove(_tp)

# ---------- ASSETS ----------
CSS = """:root{--bg:#f5f9fa;--cd:#fff;--ink:#12262d;--mu:#52676e;--sea:#0f4c5c;--deep:#08272f;--gold:#e9b44c;--ln:#d6e2e5;--f:Georgia,'Times New Roman',serif;--s:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif}
@media(prefers-color-scheme:dark){:root{--bg:#0a1a20;--cd:#12262e;--ink:#e6f0f2;--mu:#9db3ba;--sea:#6fc0d2;--deep:#05131a;--ln:#23404a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 var(--s)}a{color:var(--sea)}
h1,h2,h3{font-family:var(--f);line-height:1.2;margin:0 0 .5em}h1{font-size:clamp(1.9rem,5vw,3.2rem)}h2{font-size:1.7rem;margin-top:1.4em}h3{font-size:1.15rem;margin-bottom:.3em}p{margin:0 0 1em}
.w{max-width:1080px;margin:0 auto;padding:0 20px}.nr{max-width:800px}.hd{position:absolute}.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:var(--gold);padding:8px;z-index:20}
:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
.i{width:24px;height:24px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round;vertical-align:middle;margin-right:8px;flex:none}.i.big{width:56px;height:56px;margin:0 18px 0 0;color:var(--gold)}
header{position:sticky;top:0;z-index:10;background:var(--deep);color:#fff}.hb{display:flex;align-items:center;justify-content:space-between;min-height:64px;gap:10px}
.brand{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font:700 1.15rem var(--f)}.brand small{display:block;font:.7rem var(--s);color:var(--gold)}.lg{width:36px;height:36px}.lg rect{fill:var(--gold)}.lg path{fill:none;stroke:var(--deep);stroke-width:3}
nav{display:flex;align-items:center;gap:2px}nav a{color:#d6e7ec;text-decoration:none;padding:8px 12px;border-radius:8px;font-size:.95rem}nav a:hover,nav a.on{background:rgba(255,255,255,.13);color:#fff}
.btn{display:inline-block;background:var(--gold);color:#1b1400;font-weight:700;padding:12px 22px;border-radius:10px;text-decoration:none;border:0;cursor:pointer;font:700 1rem var(--s)}nav a.btn{color:#1b1400;margin-left:6px;padding:8px 16px}.btn.o{background:transparent;color:#fff;border:2px solid rgba(255,255,255,.65)}
.bg{display:none;background:none;border:0;padding:12px;cursor:pointer}.bg span,.bg span:before,.bg span:after{display:block;width:24px;height:2px;background:#fff;content:'';position:relative}.bg span:before{top:-7px;position:absolute}.bg span:after{top:7px;position:absolute}
.hero{position:relative;color:#fff;overflow:hidden}.sl{display:none;padding:56px 0 76px}.sl.on{display:block}.s1{background:linear-gradient(160deg,#08272f,#0f6a80)}.s2{background:linear-gradient(160deg,#3a2a08,#b07a1c)}.s3{background:linear-gradient(160deg,#0a2a24,#1b7a63)}
.sg{display:grid;grid-template-columns:1.1fr .9fr;gap:24px;align-items:center;min-height:380px}.sl.on .tx{animation:up .7s both}.tx p{font-size:1.15rem;color:#e3f0f3;max-width:52ch}.tx .btn{margin:6px 8px 0 0}
.sc{width:100%;height:auto;max-height:380px}.sun{fill:#ffd878;opacity:.9}.wa{fill:#0b4658;opacity:.8}.wb{fill:#08303d}.fs{fill:#bfe6ee;stroke:#08272f;stroke-width:.6;animation:sw 5s ease-in-out infinite}.fs.b{animation-delay:-2s;fill:#fff}.fs.c{animation-delay:-3.5s}
.gr{fill:#6b4a12}.tk{fill:none;stroke:#4a3008;stroke-width:12;stroke-linecap:round}.fr{fill:#2f7a3d}.dt{fill:#f7c25a}.rg{fill:none;stroke:rgba(255,255,255,.25);stroke-width:2;stroke-dasharray:6 8;animation:rt 40s linear infinite;transform-origin:240px 180px}.rg.r2{animation-direction:reverse}.sh{fill:rgba(233,180,76,.15);stroke:var(--gold);stroke-width:.8}.mi{stroke:#fff;fill:none;stroke-width:1.2}
@keyframes sw{50%{transform:translateX(26px)}}@keyframes rt{to{transform:rotate(360deg)}}@keyframes up{from{opacity:0;transform:translateY(18px)}}
.ctl{position:absolute;bottom:16px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:10px}.ctl button{background:rgba(255,255,255,.18);color:#fff;border:0;width:38px;height:38px;border-radius:50%;font-size:1.4rem;cursor:pointer}.dots button{width:12px;height:12px;border-radius:50%;margin:0 4px;font-size:0;padding:0;background:rgba(255,255,255,.4);border:0;cursor:pointer}.dots button.on{background:var(--gold);width:30px;border-radius:8px}
.band{background:var(--cd);border-bottom:1px solid var(--ln)}.chips{display:flex;flex-wrap:wrap;gap:8px;padding:18px 20px;justify-content:center}.chips span{display:inline-flex;align-items:center;border:1px solid var(--ln);border-radius:99px;padding:6px 14px;font-size:.92rem;background:var(--cd)}.chips .i{margin-right:6px;width:18px;height:18px;color:var(--sea)}.c2{justify-content:flex-start;padding:0 0 20px}
.sec{padding:52px 0}.sec.alt{background:var(--cd);border-block:1px solid var(--ln)}.lead{font-size:1.1rem;color:var(--mu);max-width:70ch}
.gd{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));margin-top:22px}.cd{display:block;background:var(--cd);border:1px solid var(--ln);border-radius:14px;padding:22px;color:var(--ink);text-decoration:none;position:relative;overflow:hidden}.cd .i{width:34px;height:34px;color:var(--sea);margin:0 0 10px;display:block}.cd p{color:var(--mu);font-size:.96rem;margin:0}a.cd:hover{border-color:var(--gold);transform:translateY(-3px)}a.cd{transition:transform .2s,border-color .2s}.mo{display:block;margin-top:12px;color:var(--sea);font-weight:600}
.ph{background:linear-gradient(160deg,var(--deep),#0f6a80);color:#fff;padding:36px 0 40px}.ph p{color:#d6e7ec;margin:0;max-width:62ch}.pt{display:flex;align-items:center}.bc{font-size:.88rem;margin-bottom:14px!important}.bc a{color:var(--gold)}.ph h1{margin-bottom:.2em;font-size:clamp(1.7rem,4.5vw,2.6rem)}
.tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:28px}.tabs a{padding:8px 16px;border:1px solid var(--ln);border-radius:99px;text-decoration:none;background:var(--cd)}.tabs a.on{background:var(--sea);color:#fff;border-color:var(--sea)}
.ck{list-style:none;padding:0}.ck li{padding-left:30px;margin-bottom:.6em;position:relative}.ck li:before{content:'';position:absolute;left:0;top:.45em;width:16px;height:9px;border-left:3px solid var(--gold);border-bottom:3px solid var(--gold);transform:rotate(-45deg)}
.tl{border-left:3px solid var(--gold);padding-left:18px;margin-bottom:22px}.tl p{margin:.2em 0 0;color:var(--mu)}
blockquote{margin:22px 0;padding:20px 24px;background:var(--cd);border-left:5px solid var(--gold);border-radius:0 14px 14px 0}cite{display:block;margin-top:10px;font-style:normal;font-weight:700;color:var(--sea)}
.ar{margin-bottom:14px}.mt{color:var(--mu);font-size:.88rem}
.cta{background:linear-gradient(120deg,var(--sea),var(--deep));color:#fff;text-align:center;padding:52px 0}.cta h2{margin-top:0}.cta .btn{margin-top:6px}
.gd2{display:grid;gap:30px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}label{display:block;font-weight:600;margin:14px 0 4px}input,textarea{width:100%;padding:12px;border:1px solid var(--ln);border-radius:10px;background:var(--cd);color:var(--ink);font:inherit}form .btn{margin-top:16px}
footer{background:var(--deep);color:#b8ccd2;padding-top:36px;font-size:.93rem}.fg{display:grid;gap:24px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}footer b{color:#fff;display:block;margin-bottom:8px}footer a{display:block;color:var(--gold);text-decoration:none;padding:2px 0}.cp{padding:22px 20px;margin-top:20px;border-top:1px solid rgba(255,255,255,.12)}
@media(max-width:820px){.bg{display:block}nav{display:none;position:absolute;top:64px;left:0;right:0;background:var(--deep);flex-direction:column;align-items:stretch;padding:10px 20px 18px}nav.o{display:flex}.sg{grid-template-columns:1fr}.sc{max-height:200px}.sl{padding:36px 0 70px}.pt .i.big{display:none}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}"""
JS = """(function(){var h=document.querySelector('.hero');if(h){var s=h.querySelectorAll('.sl'),d=h.querySelector('.dots'),i=0,t;
s.forEach(function(_,k){var b=document.createElement('button');b.setAttribute('aria-label','Diapositive '+(k+1));b.onclick=function(){go(k)};d.appendChild(b)});
function go(n){i=(n+s.length)%s.length;s.forEach(function(e,k){e.classList.toggle('on',k===i);d.children[k].classList.toggle('on',k===i)})}
function run(){clearInterval(t);if(!matchMedia('(prefers-reduced-motion:reduce)').matches)t=setInterval(function(){go(i+1)},6500)}
h.querySelector('.pv').onclick=function(){go(i-1)};h.querySelector('.nx').onclick=function(){go(i+1)};
h.onmouseenter=function(){clearInterval(t)};h.onmouseleave=run;go(0);run()}
var m=document.querySelector('.bg'),n=document.getElementById('nv');if(m)m.onclick=function(){m.setAttribute('aria-expanded',n.classList.toggle('o'))};
var y=document.getElementById('y');if(y)y.textContent=new Date().getFullYear()})();"""

CSS += """
:root{--b1:#41a0de;--b2:#2977b9;--pu:#7a52a6;--gold:#6cc3f7;--sea:#2977b9;--deep:#14233f;--ink:#232a33;--grad:linear-gradient(120deg,#41a0de,#2977b9 50%,#7a52a6)}
@media(prefers-color-scheme:dark){:root{--sea:#6cc3f7;--deep:#0b1426}}
header{background:#fff;color:#232a33;box-shadow:0 2px 14px rgba(20,35,63,.12)}.brand img{display:block;height:46px;width:auto}
nav a{color:#2d3a4a}nav a:hover,nav a.on{background:#eaf3fb;color:#2977b9}.bg span,.bg span:before,.bg span:after{background:#232a33}
.btn,nav a.btn{background:var(--grad);background-size:200% 100%;color:#fff;box-shadow:0 6px 18px rgba(41,119,185,.35);position:relative;overflow:hidden;transition:background-position .5s,transform .2s}.btn:hover{background-position:100% 0;transform:translateY(-2px)}nav a.btn:hover{color:#fff}.btn.o{background:transparent;box-shadow:none}.btn:after{content:'';position:absolute;top:0;left:-70%;width:40%;height:100%;background:rgba(255,255,255,.35);transform:skewX(-20deg);animation:sh 4s 1.5s infinite}
@keyframes sh{0%,60%{left:-70%}100%{left:130%}}
.s1{background:linear-gradient(160deg,#10264a,#2977b9)}.s2{background:linear-gradient(160deg,#2b2057,#7a52a6)}.s3{background:linear-gradient(160deg,#0f3358,#41a0de)}
.hero:before,.hero:after{content:'';position:absolute;border-radius:50%;filter:blur(50px);opacity:.5;pointer-events:none;z-index:1;animation:fl 14s ease-in-out infinite alternate}.hero:before{width:340px;height:340px;background:#7a52a6;left:-80px;top:-80px}.hero:after{width:300px;height:300px;background:#41a0de;right:-60px;bottom:-60px;animation-delay:-6s}
@keyframes fl{to{transform:translate(70px,50px) scale(1.2)}}.sg,.ctl{position:relative;z-index:2}.ctl{position:absolute}
.sun{fill:#cfe9ff}.fr{fill:#3f9a6a}.sh{fill:rgba(108,195,247,.18);stroke:#6cc3f7}.sl.on .sc{animation:up 1s .15s both}
.ph{background:linear-gradient(120deg,#14233f,#2977b9,#7a52a6,#14233f);background-size:300% 100%;animation:bgm 18s ease infinite}@keyframes bgm{50%{background-position:100% 0}}.i.big{color:#9fd8fb;animation:pop 3s ease-in-out infinite}@keyframes pop{50%{transform:translateY(-5px) rotate(-4deg)}}.bc a{color:#9fd8fb}
.band{background:#fff}.chips span{border-color:#cfe3f3}.chips .i{color:var(--b2)}
.cd{border:1px solid #dbe8f3;border-top:4px solid transparent;background:linear-gradient(var(--cd),var(--cd)) padding-box,var(--grad) border-box;border-radius:16px;box-shadow:0 6px 20px rgba(20,35,63,.07);transition:transform .25s,box-shadow .25s}
.cd .i{width:52px;height:52px;padding:13px;border-radius:14px;background:var(--grad);color:#fff;stroke-width:1.8;margin-bottom:14px;transition:transform .4s}
.cd:hover{transform:translateY(-6px);box-shadow:0 16px 34px rgba(41,119,185,.25)}.cd:hover .i{transform:rotate(-8deg) scale(1.1)}
.cd:before{content:'';position:absolute;top:0;left:-80%;width:50%;height:100%;background:linear-gradient(100deg,transparent,rgba(65,160,222,.16),transparent);transform:skewX(-20deg);transition:left .7s}.cd:hover:before{left:130%}
h2:after{content:'';display:block;width:56px;height:4px;border-radius:4px;background:var(--grad);margin-top:10px}.cta h2:after{margin:10px auto 0;background:#fff}
.tabs a.on{background:var(--grad);border-color:transparent}.ck li:before{border-color:var(--b1)}.tl{border-image:var(--grad) 1}blockquote{border-left-color:var(--pu)}cite{color:var(--pu)}
.cta{background:linear-gradient(120deg,#14233f,#2977b9 60%,#7a52a6)}.dots button.on{background:#6cc3f7}.mo{color:var(--b2)}
footer{background:#14233f}footer a{color:#8fd0fa}.ar:hover h3{color:var(--b2)}
.rv{opacity:0;transform:translateY(26px);transition:opacity .7s,transform .7s}.rv.in{opacity:1;transform:none}.cd.rv.in{transition:opacity .7s,transform .25s,box-shadow .25s}
.mq{overflow:hidden;padding:0 0 20px;-webkit-mask:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent);mask:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent)}.mq .tr{display:flex;gap:10px;width:max-content;animation:mq 38s linear infinite}.mq:hover .tr{animation-play-state:paused}.mq span{white-space:nowrap}@keyframes mq{to{transform:translateX(calc(-50% - 5px))}}
@media(prefers-reduced-motion:reduce){.rv{opacity:1;transform:none}.mq .tr{flex-wrap:wrap;width:auto}}
"""
JS += """
(function(){var c=document.querySelector(".c2");if(c){var t=document.createElement("div");t.className="tr";t.innerHTML=c.innerHTML+c.innerHTML;c.innerHTML="";c.className="mq";c.appendChild(t)}
var els=document.querySelectorAll(".cd,.tl,blockquote,.sec h2,.ar");if(!("IntersectionObserver" in window)||matchMedia("(prefers-reduced-motion:reduce)").matches)return;var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");o.unobserve(e.target)}})},{threshold:.12});els.forEach(function(e,k){e.classList.add("rv");e.style.transitionDelay=(k%3)*90+"ms";o.observe(e)})})();"""
CSS += """
.lg{padding:6px 0 14px}.lg+.lg{padding-top:0}.lc{flex:none;width:190px;height:96px;background:#fff;border:1px solid #dbe8f3;border-radius:14px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(20,35,63,.06);transition:transform .25s,box-shadow .25s}.lc img{max-width:84%;height:auto;filter:grayscale(1);opacity:.8;transition:filter .3s,opacity .3s,transform .3s}.lc:hover{transform:translateY(-4px) scale(1.04);box-shadow:0 12px 26px rgba(41,119,185,.25)}.lc:hover img{filter:none;opacity:1}
.mq.rev .tr{animation-direction:reverse;animation-duration:44s}
.art h2{margin-top:1.6em}.art ul,.art ol{padding-left:1.3em}.art li{margin-bottom:.4em}.art blockquote{margin:1.2em 0}
"""
JS += """
(function(){document.querySelectorAll('.mq .tr').forEach(function(t){t.insertAdjacentHTML('beforeend',t.innerHTML)});
var L=document.getElementById('al');if(L&&window.fetch&&!L.dataset.s)fetch('data/articles.json').then(function(r){return r.json()}).then(function(a){if(!a.length)return;a.sort(function(x,y){return x.date<y.date?1:-1});L.textContent='';var M=['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre'];
a.forEach(function(x){var k=document.createElement('a');k.className='cd ar';k.href='actualites/'+encodeURIComponent(x.slug)+'.html';var p=x.date.split('-'),m=document.createElement('span');m.className='mt';m.textContent=parseInt(p[2],10)+' '+M[p[1]-1]+' '+p[0]+' · '+x.cat;var h=document.createElement('h3');h.textContent=x.title;var d=document.createElement('p');d.textContent=x.desc;if(x.img){var im=document.createElement('img');im.className='th';im.src=x.img;im.alt='';im.width=200;im.height=112;im.loading='lazy';k.appendChild(im)}k.append(m,h,d);L.appendChild(k)});if(window.fil)fil()}).catch(function(){})})();
"""
CSS += """
.lc{width:270px;height:140px;border-radius:18px}.lc img{width:auto;height:auto;max-width:210px;filter:grayscale(.5);opacity:1}.lg{padding:8px 0 16px}.mq .tr{gap:16px}.mq.lg .tr{animation-duration:52s}.mq.rev .tr{animation-duration:60s}
@media(max-width:600px){.lc{width:220px;height:118px}.lc img{max-width:170px}}
.gl{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));margin-top:22px}.gi{position:relative;margin:0;border-radius:20px;overflow:hidden;aspect-ratio:4/3;box-shadow:0 10px 28px rgba(20,35,63,.18)}.gi svg{width:100%;height:100%;display:block;transition:transform .8s}.gi:hover svg{transform:scale(1.08)}
.gi figcaption{position:absolute;left:0;right:0;bottom:0;padding:44px 18px 16px;color:#fff;font-weight:700;background:linear-gradient(transparent,rgba(12,26,52,.85))}
.wv1{animation:wv 6s ease-in-out infinite alternate}.wv2{animation:wv 8s ease-in-out infinite alternate-reverse}.w3{animation-duration:10s}.bt{animation:bob 4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}.cl{animation:wv 20s linear infinite alternate}
.sw1{animation:swy 5s ease-in-out infinite alternate;transform-origin:400px 70px}.tr3{animation:swy 7s ease-in-out infinite alternate;transform-origin:170px 250px}.pm{animation:swy 6s ease-in-out infinite alternate;transform-origin:250px 270px}
@keyframes mq{to{transform:translateX(calc(-50% - 8px))}}@keyframes wv{to{transform:translateX(-40px)}}@keyframes bob{50%{transform:translateY(-6px) rotate(2deg)}}@keyframes swy{from{transform:rotate(-1.5deg)}to{transform:rotate(1.5deg)}}
"""
CSS += """
.cs{position:relative;padding:6px 0 10px}.ct{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;padding:10px 4px 18px;-webkit-overflow-scrolling:touch}.ct::-webkit-scrollbar{display:none}
.cs .lc{width:auto;flex:0 0 calc(25% - 12px);height:150px;scroll-snap-align:start;border-radius:18px}.cs .lc img{max-width:86%;height:auto;filter:none;opacity:1}
.cb{position:absolute;top:50%;transform:translateY(-62%);z-index:3;width:46px;height:46px;border-radius:50%;border:0;background:var(--grad);color:#fff;font-size:1.7rem;line-height:1;cursor:pointer;box-shadow:0 6px 18px rgba(41,119,185,.4);transition:transform .2s}.cb:hover{transform:translateY(-62%) scale(1.1)}.pv2{left:-16px}.nx2{right:-16px}
@media(max-width:900px){.cs .lc{flex-basis:calc(33.333% - 11px)}}@media(max-width:600px){.cs .lc{flex-basis:calc(50% - 8px);height:120px}.pv2{left:2px}.nx2{right:2px}.cb{width:40px;height:40px}}
"""
JS += """
(function(){document.querySelectorAll('.cs').forEach(function(c){var t=c.querySelector('.ct'),p,
st=function(){return t.querySelector('.lc').offsetWidth+16},
go=function(d){var m=t.scrollWidth-t.clientWidth;if(d>0&&t.scrollLeft>=m-4)t.scrollTo({left:0,behavior:'smooth'});else if(d<0&&t.scrollLeft<=4)t.scrollTo({left:m,behavior:'smooth'});else t.scrollBy({left:d*st(),behavior:'smooth'})},
run=function(){clearInterval(p);if(!matchMedia('(prefers-reduced-motion:reduce)').matches)p=setInterval(function(){go(1)},2600)};
c.querySelector('.pv2').onclick=function(){go(-1);run()};c.querySelector('.nx2').onclick=function(){go(1);run()};
c.onmouseenter=function(){clearInterval(p)};c.onmouseleave=run;c.addEventListener('touchstart',function(){clearInterval(p)},{passive:true});c.addEventListener('touchend',run,{passive:true});run()})})();
"""
CSS += open("assets/extra.css", encoding="utf-8").read()
JS += open("assets/extra.js", encoding="utf-8").read()
CSS += open("assets/extra4.css", encoding="utf-8").read()
CSS += open("assets/extra3.css", encoding="utf-8").read()
CSS += open("assets/extra2.css", encoding="utf-8").read()
JS += open("assets/extra2.js", encoding="utf-8").read()
CSS += open("assets/extra6.css", encoding="utf-8").read()
CSS += open("assets/extra5.css", encoding="utf-8").read()
open(OUT + "/style.css", "w", encoding="utf-8").write(CSS)
open(OUT + "/site.js", "w", encoding="utf-8").write(JS)
os.makedirs(OUT+"/img",exist_ok=True);shutil.copytree("assets/img",OUT+"/img",dirs_exist_ok=True);shutil.copytree("assets/clients",OUT+"/img/clients",dirs_exist_ok=True);shutil.copy("assets/logo.webp",OUT+"/img/logo.webp");shutil.copy("assets/favicon.png",OUT+"/favicon.png")
_x=('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#0f4c5c"/><path d="M9 23V9h7a4.5 4.5 0 010 9H9" fill="none" stroke="#e9b44c" stroke-width="3"/></svg>')
open(OUT + "/robots.txt", "w").write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % D)
open(OUT + "/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join("<url><loc>%s/%s</loc></url>" % (D, "" if f == "index.html" else f) for f, g in PAGES) + "</urlset>")
open(OUT + "/_headers", "w").write("/*\n  Content-Security-Policy: default-src 'none'; img-src 'self' data:; style-src 'self'; script-src 'self'; connect-src 'self'; form-action mailto:; base-uri 'none'; frame-ancestors 'none'\n  Strict-Transport-Security: max-age=31536000; includeSubDomains\n  X-Content-Type-Options: nosniff\n  X-Frame-Options: DENY\n  Referrer-Policy: no-referrer\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n")
# ---------- MODE PHP + BASE DE DONNÉES ----------
_seed = json.load(open(_J, encoding="utf-8"))
_st = [f for f, g in PAGES if not f.startswith("actualites/")]
shutil.rmtree(OUT + "/actualites", ignore_errors=True)
shutil.rmtree(OUT + "/data", ignore_errors=True)
for _f in ("sitemap.xml", "_headers"):
    if os.path.exists(os.path.join(OUT, _f)): os.remove(os.path.join(OUT, _f))
shutil.copytree("assets/php", OUT, dirs_exist_ok=True)
os.makedirs(OUT + "/tpl", exist_ok=True)
open(OUT + "/tpl/article.html", "w", encoding="utf-8").write(TPL)
os.replace(OUT + "/actualites.html", OUT + "/tpl/actualites.html")
open(OUT + "/inc/seed.json", "w", encoding="utf-8").write(json.dumps([{k: a[k] for k in ("slug", "date", "cat", "title", "desc", "html")} for a in _seed], ensure_ascii=False))
open(OUT + "/inc/static_pages.json", "w", encoding="utf-8").write(json.dumps([f for f in _st if f != "actualites.html"] + ["actualites.html"]))
print(len(PAGES), "pages générées dans", OUT)
