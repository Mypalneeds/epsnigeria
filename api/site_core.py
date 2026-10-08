#!/usr/bin/env python3
"""EPS shared layout. EDIT CONTACT DETAILS HERE ONLY, then re-run build_site.py and generate_pseo.py."""
import json, os, html
from PIL import Image

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://epsnigeria.com"
CO = dict(
    name="Emel Project Solutions", short="EPS",
    phone1="+234 816 438 0620", phone2="+234 803 381 8134",
    tel1="+2348164380620", tel2="+2348033818134",
    wa="2348164380620", email="info@epsnigeria.com",
    street="1, Limca Way, Isolo Industrial Estate", city="Lagos", country="Nigeria",
    lat=6.5355, lng=3.3200,  # approximate: verify on Google Maps
    hours_line="Open 24/7",
    map_url="https://www.google.com/maps/search/?api=1&query=1+Limca+Way+Isolo+Industrial+Estate+Lagos",
    social={},  # e.g. {"facebook":"https://facebook.com/...","linkedin":"..."} fills sameAs + footer icons
)
FORM_ACTION = "https://formspree.io/f/YOUR_FORM_ID"

PRODUCTS = [  # slug, name
    ("racking", "Pallet Racking"), ("high-density", "Drive-in & Shuttle Racking"), ("cantilever", "Cantilever Racking"),
    ("shelving", "Shelving & Multi-tier"), ("mezzanine", "Mezzanine Floors")]
AKA = "ECS Warehousing"  # trading name shown in the footer and schema
SERVICES = [("warehouse-solutions", "Warehouse Solutions"), ("rack-inspection", "Rack Inspection (SEMA)"),
            ("maintenance", "Maintenance"), ("installation", "Installation")]
TOP12 = ["lagos", "fct", "rivers", "ogun", "kano", "kaduna", "oyo", "delta", "anambra", "enugu", "edo", "akwa-ibom"]

def esc(s): return html.escape(s, quote=True)
def wa_url(text): return f"https://wa.me/{CO['wa']}?text=" + __import__("urllib.parse").parse.quote(text)

_dim = {}
def img(name, alt, root="", cls="", lazy=True, sizes="(max-width:768px) 100vw, 50vw", high=False):
    """name like '03-warehouse-aisle'. Uses WebP + 640w srcset, explicit width/height."""
    only_webp = name.startswith(("projects/", "clients/", "catalog"))
    if name not in _dim:
        _dim[name] = Image.open(f"{ROOT_DIR}/assets/images/{name}.{'webp' if only_webp else 'jpg'}").size
    w, h = _dim[name]
    base = f"{root}assets/images/{name}"
    if only_webp:
        c = f' class="{cls}"' if cls else ""
        return f'<img{c} src="{base}.webp" width="{w}" height="{h}" alt="{esc(alt)}" loading="lazy" decoding="async">'
    load = 'fetchpriority="high"' if high else ('loading="lazy" decoding="async"' if lazy else "")
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{base}.webp" srcset="{base}-640.webp 640w, {base}.webp {w}w" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{esc(alt)}" {load}>')

def jl(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

def org_graph():
    same = list(CO["social"].values())
    org = {"@type": "Organization", "@id": BASE + "/#org", "name": CO["name"], "alternateName": ["EPS Nigeria", AKA], "url": BASE + "/",
           "logo": BASE + "/assets/images/epslogo.png", "foundingDate": "2009",
           "slogan": "Exclusive SSI SCHÄFER partner in Nigeria",
           "contactPoint": [{"@type": "ContactPoint", "telephone": CO["phone1"], "contactType": "sales", "email": CO["email"],
                             "areaServed": "NG", "availableLanguage": "English"}]}
    if same: org["sameAs"] = same
    lb = {"@type": "LocalBusiness", "@id": BASE + "/#local", "name": CO["name"], "alternateName": AKA, "url": BASE + "/",
          "image": BASE + "/assets/images/04-warehouse-exterior.webp", "telephone": CO["phone1"], "email": CO["email"],
          "priceRange": "Quote on request",
          "address": {"@type": "PostalAddress", "streetAddress": CO["street"], "addressLocality": "Lagos", "addressRegion": "Lagos", "addressCountry": "NG"},
          "geo": {"@type": "GeoCoordinates", "latitude": CO["lat"], "longitude": CO["lng"]},
          "openingHoursSpecification": [
              {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"}],
          "areaServed": {"@type": "Country", "name": "Nigeria"}, "parent": {"@id": BASE + "/#org"}}
    site = {"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": CO["name"], "publisher": {"@id": BASE + "/#org"}, "inLanguage": "en-NG"}
    return [org, lb, site]

def breadcrumb_schema(trail, root=""):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + "/" + u} for i, (n, u) in enumerate(trail)]}

def crumbs(trail, root):
    """trail: [(name, path_from_site_root)], last item is current page."""
    li = ""
    for i, (n, u) in enumerate(trail):
        if i == len(trail) - 1: li += f'<li aria-current="page">{esc(n)}</li>'
        else: li += f'<li><a href="{root}{u or "index.html"}">{esc(n)}</a></li>'
    return f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>{li}</ol></div></nav>'

def header(root, active=""):
    r = root
    def a(k, label, href):
        return f'<li class="nav-item"><a class="nav-link{" active" if active == k else ""}" href="{r}{href}">{label}</a></li>'
    prods = "".join(f'<li><a class="dropdown-item" href="{r}products.html#{s}">{n}</a></li>' for s, n in PRODUCTS)
    servs = "".join(f'<li><a class="dropdown-item" href="{r}services.html#{s}">{n}</a></li>' for s, n in SERVICES)
    return f'''<a class="skip" href="#main">Skip to main content</a>
<div class="utility"><div class="wrap"><div class="u-l">
<a href="tel:{CO['tel1']}"><i class="fa-solid fa-phone"></i> {CO['phone1']}</a>
<a href="https://wa.me/{CO['wa']}" target="_blank" rel="noopener"><i class="fa-brands fa-whatsapp"></i> WhatsApp</a>
<a href="mailto:{CO['email']}"><i class="fa-solid fa-envelope"></i> {CO['email']}</a></div>
<span class="hrs"><i class="fa-regular fa-clock"></i> {CO['hours_line']}</span></div></div>
<header class="site-header"><nav class="navbar navbar-expand-lg" aria-label="Main"><div class="wrap d-flex w-100 align-items-center">
<a class="navbar-brand me-auto" href="{r}index.html" aria-label="Emel Project Solutions home"><img class="logo" src="{r}assets/images/epslogo.png" width="685" height="485" alt="Emel Project Solutions logo"></a>
<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav" aria-controls="nav" aria-expanded="false" aria-label="Toggle menu"><span class="navbar-toggler-icon"></span></button>
<div class="collapse navbar-collapse flex-grow-0" id="nav"><ul class="navbar-nav align-items-lg-center">
{a("home","Home","index.html")}{a("about","About","about.html")}
<li class="nav-item dropdown"><a class="nav-link dropdown-toggle{" active" if active=="products" else ""}" href="{r}products.html" role="button" data-bs-toggle="dropdown" aria-expanded="false">Products</a><ul class="dropdown-menu">{prods}<li><hr class="dropdown-divider"></li><li><a class="dropdown-item fw-bold" href="{r}products.html">All products</a></li></ul></li>
<li class="nav-item dropdown"><a class="nav-link dropdown-toggle{" active" if active=="services" else ""}" href="{r}services.html" role="button" data-bs-toggle="dropdown" aria-expanded="false">Services</a><ul class="dropdown-menu">{servs}</ul></li>
{a("projects","Projects","projects.html")}{a("locations","Locations","pages/locations/index.html")}{a("clients","Clients","clients.html")}{a("contact","Contact","contact.html")}
<li class="nav-item ms-lg-2 mt-2 mt-lg-0"><a class="btn-eps" href="{r}contact.html#quote">Get a Quote</a></li></ul></div></div></nav></header>'''

def call_chip(dark=False, label="Call us"):
    return (f'<a class="callme{" on-dark" if dark else ""}" href="tel:{CO["tel1"]}"><i class="fa-solid fa-phone" aria-hidden="true"></i>'
            f'<span><small>{label}</small><b>{CO["phone1"]}</b></span></a>')

def chip(kind, dark=False, small=False, label=None):
    """Action chips for phone, email, map and WhatsApp. One look everywhere."""
    d = {"call": (f"tel:{CO['tel1']}", "fa-solid fa-phone", label or "Call us", CO["phone1"], ""),
         "call2": (f"tel:{CO['tel2']}", "fa-solid fa-phone", label or "Second line", CO["phone2"], ""),
         "email": (f"mailto:{CO['email']}", "fa-solid fa-envelope", label or "Email us", CO["email"], ""),
         "map": (CO["map_url"], "fa-solid fa-location-dot", label or "Find us", "Open in Google Maps", ' target="_blank" rel="noopener"')}[kind]
    cls = "callme" + (" on-dark" if dark else "") + (" sm" if small else "")
    return f'<a class="{cls}" href="{d[0]}"{d[4]}><i class="{d[1]}" aria-hidden="true"></i><span><small>{d[2]}</small><b>{d[3]}</b></span></a>'

def quote_form(root, idp="q", dark=False, states=None):
    from states_data import STATES
    opts = "".join(f'<option>{n}</option>' for n in ["Lagos", "FCT (Abuja)"] + sorted(s["name"] for s in STATES.values() if s["slug"] not in ("lagos", "fct")))
    return f'''<div class="form-box"><form data-eps novalidate action="{FORM_ACTION}" method="POST" aria-label="Quote request">
<div class="row g-3"><div class="col-sm-6"><label for="{idp}n">Your name</label><input class="form-control" id="{idp}n" name="name" autocomplete="name" data-req="text"><div class="err"></div></div>
<div class="col-sm-6"><label for="{idp}p">Phone or WhatsApp</label><input class="form-control" id="{idp}p" name="phone" type="tel" autocomplete="tel" data-req="phone" placeholder="0803 000 0000"><div class="err"></div></div>
<div class="col-sm-6"><label for="{idp}s">State</label><select class="form-select" id="{idp}s" name="state" data-req="text"><option value="">Select state</option>{opts}</select><div class="err"></div></div>
<div class="col-sm-6"><label for="{idp}x">What do you need?</label><select class="form-select" id="{idp}x" name="need" data-req="text"><option value="">Choose one</option><option>Warehouse racking</option><option>Shelving or mezzanine floor</option><option>Rack inspection</option><option>Maintenance</option><option>Something else</option></select><div class="err"></div></div></div>
<input class="hp" type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="d-flex flex-wrap gap-2 mt-3"><button class="btn-eps" type="submit">Get my quote</button><a class="btn-wa wa-direct" href="https://wa.me/{CO['wa']}"><i class="fa-brands fa-whatsapp"></i> Send on WhatsApp</a></div>
<p class="small mt-3 mb-0 text-secondary">Free site visit and no-obligation quote. We are available 24/7 and usually reply within the hour.</p></form>
<div class="ok" role="status"><strong>Thanks. Your request is ready.</strong><p class="mb-2">We will call you shortly. Want a faster answer?</p><a class="btn-wa wa-fallback" href="https://wa.me/{CO['wa']}"><i class="fa-brands fa-whatsapp"></i> Or send this on WhatsApp</a></div></div>'''

def footer(root):
    from states_data import STATES
    r = root; by = {s["slug"]: s for s in STATES.values()}
    pl = "".join(f'<li><a href="{r}products.html#{s}">{n}</a></li>' for s, n in PRODUCTS)
    sl = "".join(f'<li><a href="{r}services.html#{s}">{n}</a></li>' for s, n in SERVICES)
    soc = "".join(f'<a href="{u}" aria-label="{k}" rel="noopener"><i class="fa-brands fa-{k}"></i></a>' for k, u in CO["social"].items())
    soc = f'<div class="social mt-3">{soc}</div>' if soc else ""
    return f'''<footer class="footer"><div class="wrap"><div class="row g-4 g-lg-5">
<div class="col-lg-5"><div class="brand-pair"><a class="bp-chip" href="{r}index.html"><img src="{r}assets/images/epslogo.png" width="685" height="485" alt="Emel Project Solutions" loading="lazy"></a>
<span class="bp-aka" aria-hidden="true">also<br>known as</span><span class="bp-chip"><img src="{r}assets/images/ecs-warehousing-logo.webp" width="152" height="60" alt="{AKA} logo" loading="lazy"></span></div>
<p class="mt-3 mb-0 fintro">Warehouse racking, shelving and storage systems across Nigeria since 2009. Exclusive SSI SCHÄFER partner.</p>{soc}</div>
<div class="col-6 col-lg-2"><h3>Products</h3><ul>{pl}</ul></div>
<div class="col-6 col-lg-2"><h3>Services</h3><ul>{sl}</ul></div>
<div class="col-12 col-lg-3"><h3>Contact</h3><ul class="fcontact-list">
<li><a href="tel:{CO['tel1']}">{CO['phone1']}</a></li><li><a href="https://wa.me/{CO['wa']}" target="_blank" rel="noopener">WhatsApp</a></li><li><a href="mailto:{CO['email']}">{CO['email']}</a></li>
<li><a href="{CO['map_url']}" target="_blank" rel="noopener">{CO['street']}, Lagos</a></li><li class="open247">Open 24/7</li></ul></div></div>
<div class="fbottom"><span>© <span id="yr">2026</span> Emel Project Solutions ({AKA})</span><nav class="flinks" aria-label="Footer"><a href="{r}about.html">About</a><a href="{r}projects.html">Projects</a><a href="{r}clients.html">Clients</a><a href="{r}partners.html">Partners</a><a href="{r}privacy.html">Privacy</a><a href="{r}terms.html">Terms</a></nav></div></div></footer>
<div class="wa-wrap"><div class="wa-tip" role="status">Chat with an EPS engineer</div>
<div class="wa-card" role="dialog" aria-label="WhatsApp chat"><header><strong>Emel Project Solutions</strong><small>Available 24/7. Typically replies within the hour</small></header>
<div class="qp"><p class="mb-1 small">Hello. What do you need help with?</p><a data-topic="Warehouse racking quote" href="#">Warehouse racking quote</a><a data-topic="Shelving or mezzanine quote" href="#">Shelving &amp; mezzanine quote</a><a data-topic="Rack inspection" href="#">Rack inspection</a><a data-topic="Other" href="#">Other</a></div></div>
<button class="wa-btn" aria-label="Open WhatsApp chat" aria-expanded="false"><i class="fa-brands fa-whatsapp"></i></button></div>
<nav class="mbar" aria-label="Quick contact"><a href="tel:{CO['tel1']}"><i class="fa-solid fa-phone"></i>Call</a><a data-wa="a quote" href="https://wa.me/{CO['wa']}"><i class="fa-brands fa-whatsapp"></i>WhatsApp</a><a class="q" href="{r}contact.html#quote"><i class="fa-solid fa-file-invoice"></i>Quote</a></nav>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" defer></script>
<script src="{r}assets/js/main.js" defer></script>
<script>document.getElementById("yr").textContent=new Date().getFullYear()</script>'''

def page(root, path, title, desc, body, active="", schema=None, hero_img=None, crumb_trail=None, geo=None, og_img="01-hero-warehouse"):
    """Full HTML document. path = path from site root, e.g. 'about.html' ('' for home)."""
    assert len(title) <= 60, (len(title), title)
    assert len(desc) <= 155, (len(desc), desc)
    url = f"{BASE}/{path}"
    graph = (org_graph() if (path in ("", "about.html", "contact.html")) else []) + (schema or [])
    if crumb_trail: graph.append(breadcrumb_schema(crumb_trail))
    geo = geo or {"pos": f"{CO['lat']};{CO['lng']}", "place": "Isolo, Lagos, Nigeria", "region": "NG-LA"}
    pre = f'<link rel="preload" as="image" href="{root}assets/images/{hero_img}.webp" fetchpriority="high">' if hero_img else ""
    ogimg = f"{BASE}/assets/images/{og_img}.webp"
    return f'''<!DOCTYPE html>
<html lang="en-NG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}"><link rel="alternate" hreflang="en-NG" href="{url}">
<meta name="theme-color" content="#001F3F"><meta name="geo.region" content="{geo['region']}"><meta name="geo.placename" content="{esc(geo['place'])}"><meta name="geo.position" content="{geo['pos']}"><meta name="ICBM" content="{geo['pos'].replace(';', ', ')}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Emel Project Solutions"><meta property="og:locale" content="en_NG"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{ogimg}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{ogimg}">
<link rel="icon" href="{root}assets/images/epslogo.png" type="image/webp">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin><link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="image" href="{root}assets/images/epslogo.png">{pre}
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="{root}assets/css/main.css">
{jl({"@context": "https://schema.org", "@graph": graph})}
</head><body>
{header(root, active)}
{body}
{footer(root)}
</body></html>'''

def write(path, content):
    p = os.path.join(ROOT_DIR, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)

def cta_band(root, heading, text, topic):
    return f'''<section class="sec dark" id="quote"><div class="wrap"><div class="row g-5 align-items-center"><div class="col-lg-5 rv"><span class="bar"></span><h2>{heading}</h2><p>{text}</p>
<p><a class="btn-wa" data-wa="{esc(topic)}" href="https://wa.me/{CO['wa']}"><i class="fa-brands fa-whatsapp"></i> Chat with an engineer</a></p><p class="mb-2">{call_chip(True, "Or call us. Emergency line: call or WhatsApp")}</p></div>
<div class="col-lg-7 rv">{quote_form(root, "c")}</div></div></div></section>'''
