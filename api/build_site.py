#!/usr/bin/env python3
"""Builds index + all root pages. Run: python3 api/build_site.py  (then python3 api/generate_pseo.py)"""
import json
from site_core import *
from content import *
from states_data import STATES
from clients_data import CLIENTS
BYSLUG = {s["slug"]: s for s in STATES.values()}
R = ""

def faq_html(faqs, idp="f"):
    items = ""
    for i, (q, a) in enumerate(faqs):
        items += f'''<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#{idp}{i}" aria-expanded="false" aria-controls="{idp}{i}">{esc(q)}</button></h3>
<div id="{idp}{i}" class="accordion-collapse collapse" data-bs-parent="#{idp}acc"><div class="accordion-body">{esc(a)}</div></div></div>'''
    return f'<div class="accordion" id="{idp}acc">{items}</div>'

def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def pagehead(h1, intro, kicker=""):
    return f'<section class="pagehead"><div class="wrap"><span class="bar"></span><h1>{h1}</h1><p>{intro}</p></div></section>'

def related(root, items, title="Keep exploring"):
    li = "".join(f'<a href="{root}{u}">{esc(t)}</a>' for t, u in items)
    return f'<section class="sec paper"><div class="wrap"><h2 class="h4">{title}</h2><div class="linkgrid mt-3">{li}</div></div></section>'

def proj_cards(root, items):
    out = ""
    for (pid, t, sec, st, sl, scope, client, im, date) in items:
        loc = f' · <a href="{root}pages/locations/{sl}.html">{st}</a>' if sl else ""
        dt = f"<p class='mb-0'><strong>Date:</strong> {date}</p>" if date else ""
        out += f'''<div class="col-md-6 col-lg-4 rv" data-sector="{sec}"><article class="pcard"><div class="ph">{img(im, t + " for " + client, root)}</div><div class="b">
<span class="meta">{sec}{loc}</span><h3 class="mt-1">{t}</h3><p class="mb-2"><strong>Client:</strong> {client}</p>
<p class="mb-2"><strong>Work done:</strong> {scope}</p>{dt}</div></article></div>'''
    return out

def logo_wall(root, limit=None):
    items = CLIENTS[:limit] if limit else CLIENTS
    return '<ul class="logos">' + "".join(f'<li>{img("clients/" + s, n + " logo", root)}</li>' for n, s in items) + "</ul>"

CRUMB_HOME = ("Home", "")

# ---------------------------------------------------------------- HOME
def home():
    slides = [
     ("01-hero-warehouse","Exclusive SSI SCHÄFER partner","h1","Warehouse racking that carries the load.","Pallet racking, drive-in and shuttle systems from SSI SCHÄFER, installed by our own crews.",("Get my racking quote","data-wa","Warehouse racking"),("See racking","products.html#racking")),
     ("07-shuttle-racking","High density","h2","More pallets in the same floor.","Drive-in, shuttle and mobile racking for high-volume stock, laid out around your forklifts.",("Get my racking quote","data-wa","High-density racking"),("Compare racking systems","products.html#high-density")),
     ("16-rack-inspection","Safety","h2","Rack inspection by SEMA-certified engineers.","Find damaged uprights and overloaded beams before they cause an accident.",("Book a rack inspection","data-wa","Rack inspection"),("How inspection works","services.html#rack-inspection")),
     ("19-installation-team","Nationwide","h2","Installation in all 36 states and the FCT.","Our crews travel with the materials. Kano, Port Harcourt or Abuja, the process is the same.",("Chat with an engineer","data-wa","Installation outside Lagos"),("Where we work","pages/locations/index.html")),
     ("21-warehouse-project","Track record","h2","500+ projects since 2009.","200+ clients across manufacturing, logistics, retail and FMCG.",("Get a quote","contact.html#quote",""),("See our projects","projects.html")),
    ]
    sh = ""
    for i, (im, tag, h, title, vp, c1, c2) in enumerate(slides):
        first = i == 0
        b1 = (f'<a class="btn-eps" data-wa="{c1[2]}" href="#">{c1[0]}</a>' if c1[1] == "data-wa" else f'<a class="btn-eps" href="{c1[1]}">{c1[0]}</a>')
        sh += f'''<div class="slide{" on" if first else ""}" role="group" aria-roledescription="slide" aria-label="{i+1} of 5">
{img(im, "", R, "", lazy=not first, sizes="100vw", high=first) if True else ""}
<div class="wrap"><span class="tag">{tag}</span><{h} class="hl">{title}</{h}><p>{vp}</p><div class="ctas">{b1}<a class="btn-ghost" href="{c2[1]}">{c2[0]}</a></div></div></div>'''
    hero = f'''<section class="hero" aria-roledescription="carousel" aria-label="EPS highlights">{sh}
<div class="hero-ui"><div class="wrap"><div class="dots">{"".join(f'<button aria-label="Go to slide {k+1}" aria-current="{str(k==0).lower()}"></button>' for k in range(5))}</div>
<div class="arrows"><button class="prev" aria-label="Previous slide"><i class="fa-solid fa-arrow-left"></i></button><button class="next" aria-label="Next slide"><i class="fa-solid fa-arrow-right"></i></button></div></div></div></section>
<div class="proof"><div class="wrap"><ul><li><b>15+</b>years</li><li><b>500+</b>projects</li><li><b>200+</b>clients</li><li><b>36</b>states + FCT</li><li>SSI SCHÄFER partner</li></ul></div></div>'''
    intro = f'''<section class="sec who"><div class="wrap"><div class="who-grid"><div class="rv"><span class="kicker" style="color:var(--orange)">Who we are</span>
<h2>Racking and storage, from one Lagos team.</h2>
<p class="lede">Emel Project Solutions (EPS) supplies and installs warehouse racking, shelving and storage systems across Nigeria. We are the exclusive SSI SCHÄFER partner in Nigeria.</p>
<p class="mt-3">We started in 2009 as a small trading company. Clients kept asking us to fit what we sold, so we built our own crews. We measure, design, supply, install and inspect. One team, one contract.</p>
</div>
<div class="who-pic rv"><span class="since"><b>2009</b>SINCE</span><div class="main">{img("18-team-planning","EPS engineers planning a project",R,sizes="(max-width:991px) 100vw, 40vw")}</div><div class="inset">{img("19-installation-team","EPS installation crew on site",R,sizes="30vw")}</div></div></div></div></section>'''
    trust = f'<section class="sec paper" style="padding:3rem 0"><div class="wrap"><span class="kicker">Trusted by</span><h2 class="h3 mb-4">Banks, brewers, pharma and factories</h2>{logo_wall(R, 12)}<p class="mt-3"><a class="alink" href="clients.html">See all our clients <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a></p></div></section>'
    paths = f'''<section aria-labelledby="paths-h"><div class="wrap"><h2 id="paths-h" class="visually-hidden">What we do</h2></div><div class="paths">
<div class="path rv">{img("06-heavy-duty-racking","Heavy-duty pallet racking in a warehouse",R,sizes="(max-width:991px) 100vw, 55vw")}<div class="in"><span class="kicker" style="color:var(--orange)">Path 1</span><h3 class="h2">Warehouse</h3><ul><li>Selective, drive-in, shuttle and cantilever racking</li><li>Layouts drawn around your forklifts and pallets</li><li>SEMA-certified inspection and maintenance</li><li>Exclusive SSI SCHÄFER partner</li></ul><a class="btn-eps" href="services.html#warehouse-solutions">See warehouse solutions</a></div></div>
<div class="path rv">{img("16-rack-inspection","EPS engineer inspecting pallet racking",R,sizes="(max-width:991px) 100vw, 45vw")}<div class="in"><span class="kicker" style="color:var(--orange)">Path 2</span><h3 class="h2">Safety and aftercare</h3><ul><li>SEMA-certified rack inspection</li><li>Written damage report with repair priorities</li><li>Planned maintenance, repairs and spare parts</li><li>Emergency line: call or WhatsApp</li></ul><a class="btn-eps" href="services.html#rack-inspection">See rack inspection</a></div></div></div></section>'''
    mos = f'''<section class="sec"><div class="wrap"><div class="row mb-4"><div class="col-lg-7 rv"><span class="bar"></span><h2>What most clients ask us for first</h2></div></div><div class="mosaic">
<a class="tile t1 rv" href="products.html#racking">{img("06-heavy-duty-racking","Heavy-duty pallet racking",R)}<span>Pallet racking<small>Selective, heavy-duty, narrow aisle</small></span></a>
<a class="tile t2 rv" href="products.html#high-density">{img("07-shuttle-racking","Shuttle racking system",R)}<span>Drive-in &amp; shuttle<small>High-density storage</small></span></a>
<a class="tile t3 rv" href="products.html#cantilever">{img("08-cantilever-racks","Cantilever racks with long loads",R)}<span>Cantilever racking</span></a>
<a class="tile t4 rv" href="products.html#shelving">{img("22-ecommerce-warehouse","Shelving in a fulfilment warehouse",R)}<span>Shelving &amp; multi-tier</span></a>
<a class="tile t5 rv" href="products.html#mezzanine">{img("projects/dag-industries","Multi-tier platform with stairs",R)}<span>Mezzanine floors</span></a></div>
<p class="mt-4"><a class="btn-ghost on-light" href="products.html">Browse all {len(PRODUCTS)} product families</a></p></div></section>'''
    cases = "".join(f'''<article class="case rv"><div class="cp">{img(p[7], p[1] + " for " + p[6], R)}<span class="n">{i+1:02d}</span></div><div><h3>{p[1]}</h3><span class="kicker mb-1">{p[2]} · {p[3]}</span>
<dl><dt>Client</dt><dd>{p[6]}</dd><dt>Work</dt><dd>{p[5]}</dd></dl><a class="alink" href="pages/locations/{p[4]}.html">Racking in {p[3]} <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a></div></article>''' for i, p in enumerate([PBYID["west-african-cubes"], PBYID["dag-industries"]]))
    proj = f'''<section class="sec paper"><div class="wrap"><div class="row g-5"><div class="col-lg-4 rv"><span class="bar"></span><h2>Recent projects</h2><p class="lead">Real sites, real scopes. Each one started with a phone call and a site visit.</p><a class="btn-eps" href="projects.html">See all projects</a></div><div class="col-lg-8">{cases}</div></div></div></section>'''
    steps = "".join(f'<li class="{"more" if i>=5 else ""}"><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(STEPS))
    how = f'''<section class="sec"><div class="wrap"><div class="split"><div class="pic rv">{img("18-team-planning","EPS engineers planning a project",R)}</div><div class="rv"><span class="bar"></span><h2>How we work</h2><p class="answer">From first call to handover, a project runs in ten steps. The first visit costs you nothing.</p><ol class="steps">{steps}</ol>
<button class="btn-ghost on-light" id="stepsToggle" aria-expanded="false" type="button">See all 10 steps</button></div></div></div></section>'''
    ssi = f'''<section class="band"><div class="wrap"><div class="row g-5 align-items-center"><div class="col-lg-7 rv"><span class="badge-ssi">SSI SCHÄFER</span><h2 class="mt-4">The exclusive SSI SCHÄFER partner in Nigeria</h2>
<p>Emel Project Solutions supplies, installs and services SSI SCHÄFER warehouse racking in Nigeria. You deal with a local team that answers the phone, not an overseas call centre.</p><a class="btn-eps" href="partners.html">Read about the partnership</a> <a class="btn-ghost" href="products.html#racking">See racking systems</a></div>
<div class="col-lg-5 rv">{img("25-warehouse-team","EPS and warehouse team on site",R)}</div></div></div></section>'''
    serve = "".join(f'<a class="rv" href="{u}">{n}<small>{d}</small></a>' for n, d, u in SECTORS)
    who = f'<section class="sec"><div class="wrap"><span class="kicker">Who we serve</span><h2 class="mb-4">Built for working sites</h2><div class="serve">{serve}</div></div></section>'
    tq = "".join(f'''<div class="tq{" on" if i==0 else ""}"><blockquote>"{q}"</blockquote><p class="who"><strong>{n}</strong>, {r}<br>{co}, {st}</p></div>''' for i, (q, n, r, co, st) in enumerate(TESTIMONIALS))
    testi = f'''<section class="sec paper"><div class="wrap"><span class="bar"></span><h2 class="mb-4">What clients say</h2><div class="testi" aria-roledescription="carousel" aria-label="Testimonials">{tq}
<div class="dots mt-3">{"".join(f'<button aria-label="Testimonial {k+1}" aria-current="{str(k==0).lower()}" style="background:#bbb"></button>' for k in range(3))}</div></div></div></section>'''
    import os, pypdf
    mb = os.path.getsize(f"{ROOT_DIR}/assets/docs/EPS-Catalog.pdf") / 1048576
    npages = len(pypdf.PdfReader(f"{ROOT_DIR}/assets/docs/EPS-Catalog.pdf").pages)
    catalog = f'''<section class="sec catalog" id="catalog"><div class="wrap"><div class="row g-5 align-items-center"><div class="col-lg-5 rv"><div class="cat-cover">{img("catalog-cover", "Cover of the EPS product catalog", R, sizes="(max-width:991px) 70vw, 30vw")}</div></div>
<div class="col-lg-7 rv"><span class="bar"></span><h2>Download the EPS catalog</h2><p class="answer">Our racking and storage systems in one PDF, with the storage gain each layout delivers and our SSI SCHÄFER range.</p>
<div class="row g-3 mb-4"><div class="col-sm-6"><h3 class="h6 text-uppercase" style="letter-spacing:.1em">Racking systems</h3><ul class="tick"><li>Selective pallet racking</li><li>Very narrow aisle racking</li><li>Drive-in racking</li><li>Double-deep racking</li><li>Shuttle racking</li><li>Mobile pallet racking</li></ul></div>
<div class="col-sm-6"><h3 class="h6 text-uppercase" style="letter-spacing:.1em">Shelving and floors</h3><ul class="tick"><li>Light and medium duty shelving</li><li>Heavy-duty racking</li><li>Mezzanine floors</li></ul></div></div>
<div class="d-flex flex-wrap gap-2 align-items-center"><a class="btn-eps" href="assets/docs/EPS-Catalog.pdf" download="EPS-Catalog.pdf"><i class="fa-solid fa-file-arrow-down"></i> Download the catalog</a><a class="btn-ghost on-light" data-wa="a printed EPS catalog" href="#">Ask for a printed copy</a></div>
<p class="small mt-3 mb-0 text-secondary">PDF, {npages} pages, {mb:.0f} MB. Opens in your browser or phone.</p></div></div></div></section>'''
    faq = f'''<section class="sec"><div class="wrap"><div class="row g-5"><div class="col-lg-4 rv"><span class="bar"></span><h2>Questions buyers ask</h2><p class="mb-3">Still unsure? Talk to an engineer.</p>{call_chip(False, "Call us")}</div><div class="col-lg-8 rv">{faq_html(FAQS)}</div></div></div></section>'''
    cta = cta_band(R, "Tell us what you need. We will visit and quote.", "Four fields, one reply. Free site visit and no-obligation quote.", "General enquiry")
    sch = [faq_schema(FAQS), {"@type": "ItemList", "name": "EPS product families", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": f"{BASE}/products.html#{s}"} for i, (s, n) in enumerate(PRODUCTS)]}]
    body = f'<main id="main">{hero}{intro}{trust}{paths}{mos}{proj}{how}{ssi}{who}{catalog}{testi}{faq}{cta}</main>'
    return page(R, "", "Warehouse Racking Nigeria | SSI SCHÄFER Partner | EPS", "Exclusive SSI SCHÄFER partner in Nigeria. Warehouse racking, shelving, mezzanine floors and SEMA rack inspection. 500+ projects, all 36 states.", body, "home", sch, hero_img="01-hero-warehouse")

# ---------------------------------------------------------------- PRODUCTS
def products():
    secs = ""
    for i, (slug, name) in enumerate(PRODUCTS):
        d = PRODUCT_DETAIL[slug]; flip = i % 2
        specs = "".join(f"<li>{s}</li>" for s in d["specs"])
        svc = [s for s in SERVICES if s[0] == d["svc"]][0]
        secs += f'''<section class="sec{" paper" if flip else ""}" id="{slug}"><div class="wrap"><div class="row g-5 align-items-center{" flex-lg-row-reverse" if flip else ""}"><div class="col-lg-6 rv"><div class="split" style="display:block"><div class="pic">{img(d["img"], name + " by EPS", R)}</div></div></div>
<div class="col-lg-6 rv"><span class="bar"></span><h2>{name}</h2><p class="answer">{d["ans"]}</p><dl><dt>Specs</dt><dd><ul>{specs}</ul></dd><dt>Typical use</dt><dd>{d["uses"]}</dd></dl>
<a class="btn-eps" data-wa="{name}" href="#">Request a quote for this</a> <a class="btn-ghost on-light" href="services.html#{svc[0]}">{svc[1]}</a></div></div></div></section>'''
        if slug == "cantilever":
            secs += f'''<section class="sec"><div class="wrap"><span class="bar"></span><h2>Which racking system fits?</h2><p class="answer">Choose selective racking for many product types, drive-in for large volumes of one product, shuttle for the highest density, and cantilever for long loads.</p>
<div class="tscroll"><table class="cmp"><caption class="visually-hidden">Racking comparison</caption><thead><tr><th>System</th><th>Access</th><th>Space use</th><th>Best for</th></tr></thead><tbody>
<tr><td>Selective pallet racking</td><td>Every pallet, directly</td><td>Standard</td><td>Mixed SKUs, FMCG, retail distribution</td></tr>
<tr><td>Drive-in racking</td><td>Forklift enters lane, last-in first-out</td><td>High</td><td>Large volumes of one product</td></tr>
<tr><td>Shuttle racking</td><td>Powered shuttle moves pallets in lane</td><td>Very high</td><td>High-volume, deep-lane storage</td></tr>
<tr><td>Cantilever racking</td><td>Open front, arms</td><td>Standard</td><td>Pipes, timber, profiles, long loads</td></tr></tbody></table></div></div></section>'''
    ilist = {"@type": "ItemList", "name": "EPS products", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Product", "name": n, "description": PRODUCT_DETAIL[s]["ans"], "brand": {"@type": "Brand", "name": "SSI SCHÄFER" if s == "racking" else "EPS"}, "url": f"{BASE}/products.html#{s}"}} for i, (s, n) in enumerate(PRODUCTS)]}
    body = f'''<main id="main">{crumbs([CRUMB_HOME, ("Products", "products.html")], R)}{pagehead("Warehouse racking, shelving and mezzanine floors", "Five product families, supplied and installed by one Nigerian team. Warehouse racking is from SSI SCHÄFER, our exclusive partnership.")}{secs}
{related(R, [("Warehouse Solutions", "services.html#warehouse-solutions"), ("Installation service", "services.html#installation"), ("Rack inspection", "services.html#rack-inspection"), ("See our projects", "projects.html"), ("Racking in Lagos", "pages/locations/lagos.html")])}{cta_band(R, "Not sure which product? Ask an engineer.", "Send your site details. We will recommend and price it.", "Products")}</main>'''
    return page(R, "products.html", "Products: Warehouse Racking & Shelving Nigeria | EPS", "Pallet, drive-in, shuttle and cantilever racking, shelving and mezzanine floors from the exclusive SSI SCHÄFER partner in Nigeria.", body, "products", [ilist], crumb_trail=[("Home", ""), ("Products", "products.html")])

# ---------------------------------------------------------------- SERVICES
def services():
    secs, sch = "", []
    for i, (slug, name) in enumerate(SERVICES):
        d = SERVICE_DETAIL[slug]; flip = i % 2
        pts = "".join(f"<li>{p}</li>" for p in d["pts"])
        secs += f'''<section class="sec{" paper" if flip else ""}" id="{slug}"><div class="wrap"><div class="row g-5 align-items-center{" flex-lg-row-reverse" if flip else ""}"><div class="col-lg-5 rv"><div class="split" style="display:block"><div class="pic">{img(d["img"], d["name"], R)}</div></div></div>
<div class="col-lg-7 rv"><span class="bar"></span><h2>{d["name"]}</h2><p class="answer">{d["ans"]}</p><ul>{pts}</ul>
<div class="linkgrid mb-3"><a href="products.html#{d["prod"]}">{dict(PRODUCTS)[d["prod"]]}</a><a href="pages/locations/lagos.html">Lagos</a><a href="pages/locations/rivers.html">Rivers</a><a href="projects.html">Our projects</a></div>
<a class="btn-eps" data-wa="{d["cta"].replace("Get my ","").replace("Book a ","")}" href="#">{d["cta"]}</a></div></div></div></section>'''
        sch.append({"@type": "Service", "name": d["name"], "serviceType": d["name"], "description": d["ans"], "provider": {"@id": BASE + "/#org"}, "areaServed": {"@type": "Country", "name": "Nigeria"}, "url": f"{BASE}/services.html#{slug}"})
    body = f'''<main id="main">{crumbs([CRUMB_HOME, ("Services", "services.html")], R)}{pagehead("Racking, inspection, maintenance and installation", "Four services that cover a warehouse from first drawing to yearly check. Call or WhatsApp the emergency line for urgent damage.")}{secs}
{related(R, [("Warehouse racking", "products.html#racking"), ("Mezzanine floors", "products.html#mezzanine"), ("Projects we have delivered", "projects.html"), ("All states we serve", "pages/locations/index.html")])}{cta_band(R, "Book a site visit", "We visit, measure and send a written quote.", "Services")}</main>'''
    return page(R, "services.html", "Rack Inspection & Installation Services | EPS Nigeria", "Warehouse solutions, SEMA-certified rack inspection, maintenance and installation across Nigeria. Free site visit, no-obligation quote.", body, "services", sch, crumb_trail=[("Home", ""), ("Services", "services.html")])

# ---------------------------------------------------------------- PROJECTS
def projects():
    sectors = sorted({p[2] for p in PROJECTS})
    chips = '<button data-f="all" aria-pressed="true">All</button>' + "".join(f'<button data-f="{s}" aria-pressed="false">{s}</button>' for s in sectors)
    chipbar = f'<div class="fchips" role="group" aria-label="Filter by sector">{chips}</div>' if len(sectors) > 1 else ""
    body = f'''<main id="main">{crumbs([CRUMB_HOME, ("Projects", "projects.html")], R)}{pagehead("500+ projects across Nigeria", "A selection of warehouse racking projects by state. Each one started with a site visit.")}
<section class="sec"><div class="wrap">{chipbar}<div class="row g-4">{proj_cards(R, PROJECTS)}<div class="col-md-6 col-lg-4 rv"><div class="pcta"><span class="bar"></span><h3>Have a site like these?</h3><p>Send us the location and what you need. We visit, measure and quote at no cost.</p><a class="btn-eps" href="contact.html#quote">Get my quote</a> <a class="btn-ghost" data-wa="a project like the ones on your projects page" href="#"><i class="fa-brands fa-whatsapp"></i> WhatsApp us</a></div></div></div>
<h2 class="h3 mt-5 mb-3">More installations</h2><div class="row g-4">{"".join(f'<div class="col-md-4 rv"><figure class="m-0">{img(g, a, R)}<figcaption class="small mt-2">{a}</figcaption></figure></div>' for g, a in PROJECT_GALLERY)}</div></div></section>
{related(R, [("Warehouse racking", "products.html#racking"), ("Drive-in and shuttle racking", "products.html#high-density"), ("Installation service", "services.html#installation"), ("Work in Lagos", "pages/locations/lagos.html"), ("Work in Abuja", "pages/locations/fct.html")])}{cta_band(R, "Start your project", "Tell us the site and the need. We reply in working hours.", "New project")}</main>'''
    return page(R, "projects.html", "Projects: Warehouse Racking Work in Nigeria | EPS", "Browse EPS warehouse projects: heavy-duty, shuttle and multi-tier racking for manufacturers, logistics firms and distributors across Nigeria.", body, "projects", [{"@type": "CollectionPage", "name": "EPS projects", "url": BASE + "/projects.html"}], crumb_trail=[("Home", ""), ("Projects", "projects.html")])

# ---------------------------------------------------------------- ABOUT
def about():
    body = f'''<main id="main">{crumbs([CRUMB_HOME, ("About", "about.html")], R)}{pagehead("A Lagos company that installs what it sells", "Emel Project Solutions started in 2009. We now supply racking and storage systems in all 36 states and the FCT.")}
<section class="sec"><div class="wrap"><div class="row g-5 align-items-center"><div class="col-lg-6 rv"><span class="bar"></span><h2>Our story</h2><p class="answer">Emel Project Solutions was founded in Lagos in 2009 and is today the exclusive SSI SCHÄFER partner in Nigeria.</p><p>We began as a small trading company. Clients kept asking us to fit what we sold, so we built installation crews. Then they asked for warehouse racking, and we took on SSI SCHÄFER. The company now holds SEMA and ISO certifications and has completed 500+ projects.</p></div>
<div class="col-lg-6 rv"><div class="split" style="display:block"><div class="pic">{img("19-installation-team","The EPS installation team on site",R)}</div></div></div></div></div></section>
<section class="sec dark"><div class="wrap"><div class="row g-4 text-center">{"".join(f'<div class="col-6 col-md-3 stat rv"><b data-count="{n}" data-suffix="{s}">0</b>{l}</div>' for n,s,l in [(15,"+","years"),(500,"+","projects"),(200,"+","clients"),(36,"","states + FCT")])}</div></div></section>
<section class="sec"><div class="wrap"><div class="row g-5"><div class="col-lg-5 rv">{img("23-client-consultation","EPS engineer in a client consultation",R)}<div class="mt-3">{img("25-warehouse-team","EPS warehouse team",R)}</div></div>
<div class="col-lg-7 rv"><span class="bar"></span><h2>What we hold ourselves to</h2><dl><dt>Quality</dt><dd>We specify materials by load, finish and site conditions, not by price alone.</dd><dt>Integrity</dt><dd>We tell you when a cheaper option will not do the job.</dd><dt>Innovation</dt><dd>We bring in new storage systems when they suit your stock, not to look modern.</dd></dl>
<h2 class="h3 mt-4">Certifications</h2><ul><li><strong>SEMA certified.</strong> Storage Equipment Manufacturers Association certified for racking expertise.</li><li><strong>ISO certified.</strong> Quality management system.</li><li><strong>SSI SCHÄFER.</strong> <a href="partners.html">Exclusive partner in Nigeria</a>.</li></ul></div></div></div></section>
{related(R, [("Our products", "products.html"), ("Our services", "services.html"), ("Projects", "projects.html"), ("Where we work", "pages/locations/index.html"), ("Contact EPS", "contact.html")])}{cta_band(R, "Talk to the team", "Visit our Isolo office or call us.", "General enquiry")}</main>'''
    return page(R, "about.html", "About EPS: Warehouse Racking Specialists, Lagos", "Emel Project Solutions, founded 2009 in Lagos. Exclusive SSI SCHÄFER partner, SEMA and ISO certified, with 500+ projects in 36 states.", body, "about", crumb_trail=[("Home", ""), ("About", "about.html")])

# ---------------------------------------------------------------- PARTNERS / CLIENTS
def partners():
    body = f'''<main id="main">{crumbs([CRUMB_HOME, ("Partners", "partners.html")], R)}{pagehead("Our partners", "One exclusive racking partnership, backed by our certification and installation network.")}
<section class="sec"><div class="wrap"><div class="row g-5 align-items-center"><div class="col-lg-7 rv"><span class="badge-ssi">SSI SCHÄFER</span><h2 class="mt-3">Exclusive racking partner in Nigeria</h2><p class="answer">Emel Project Solutions is the exclusive SSI SCHÄFER partner in Nigeria for warehouse racking.</p><p>SSI SCHÄFER is a global maker of storage and logistics systems. Through this partnership EPS supplies, installs and services their racking in Nigeria. You get rated systems and a local team for follow-up.</p>
<ul><li>Pallet racking and shelving</li><li>Drive-in and shuttle high-density systems</li><li>Installation by EPS crews</li></ul><a class="btn-eps" data-wa="SSI SCHÄFER racking" href="#">Get my racking quote</a></div><div class="col-lg-5 rv">{img("02-modern-warehouse","Warehouse with SSI SCHÄFER-type racking",R)}</div></div></div></section>
<section class="sec paper"><div class="wrap"><h2>Supplier and certification network</h2><dl class="row"><dt class="col-md-3">Standards</dt><dd class="col-md-9">SEMA and ISO certification for inspection and quality management.</dd><dt class="col-md-3">Installation</dt><dd class="col-md-9">Our own crews, backed by contractors where a state needs local hands.</dd></dl></div></section>
{related(R, [("Racking systems", "products.html#racking"), ("Rack inspection", "services.html#rack-inspection"), ("Projects", "projects.html"), ("Lagos", "pages/locations/lagos.html")])}{cta_band(R, "Become a client", "Tell us about your site.", "Partnership")}</main>'''
    return page(R, "partners.html", "Partners: Exclusive SSI SCHÄFER Partner Nigeria | EPS", "EPS is the exclusive SSI SCHÄFER partner in Nigeria for warehouse racking. See our supplier and certification network.", body, "partners", crumb_trail=[("Home", ""), ("Partners", "partners.html")])

def clients():
    tq = "".join(f'<div class="col-md-4 rv"><div class="form-box h-100"><p>"{q}"</p><p class="small mb-0"><strong>{n}</strong>, {r}<br>{co}, {st}</p></div></div>' for q, n, r, co, st in TESTIMONIALS)
    body = f'''<main id="main">{crumbs([CRUMB_HOME, ("Clients", "clients.html")], R)}{pagehead("200+ clients across Nigeria", "Banks, brewers, pharma makers, manufacturers and distributors. A selection of the companies we have worked with.")}
<section class="sec"><div class="wrap"><span class="bar"></span><h2 class="mb-4">Companies we have worked with</h2>{logo_wall(R)}<p class="small text-secondary mt-3">Logos belong to their owners and appear here as client references.</p></div></section>
<section class="sec paper"><div class="wrap"><span class="bar"></span><h2>Industries we serve</h2><div class="serve mt-4">{"".join(f'<a href="{u}">{n}<small>{d}</small></a>' for n,d,u in SECTORS)}</div></div></section>
<section class="sec"><div class="wrap"><h2>Client feedback</h2><div class="row g-4 mt-1">{tq}</div></div></section>
{related(R, [("Projects", "projects.html"), ("Products", "products.html"), ("Services", "services.html"), ("Locations", "pages/locations/index.html")])}{cta_band(R, "Be our next reference", "Free site visit, no-obligation quote.", "General enquiry")}</main>'''
    return page(R, "clients.html", "Our Clients: 200+ Companies Across Nigeria | EPS", "EPS serves 200+ clients including Access Bank, Dangote, Nigerian Breweries, Cummins and GTBank across all 36 Nigerian states.", body, "clients", crumb_trail=[("Home", ""), ("Clients", "clients.html")])

# ---------------------------------------------------------------- CONTACT
def contact():
    body = f'''<main id="main">{crumbs([CRUMB_HOME, ("Contact", "contact.html")], R)}{pagehead("Talk to an EPS engineer", "Call, WhatsApp or send the form. We reply in working hours, usually within the hour.")}
<section class="sec" id="quote"><div class="wrap"><div class="row g-5"><div class="col-lg-7 rv">{quote_form(R, "k")}</div>
<div class="col-lg-5 rv"><h2 class="h3">Our office</h2><address>{CO['name']}<br>{CO['street']}<br>Lagos, Nigeria</address>
<div class="d-grid gap-2 mb-4" style="justify-items:start">{chip("call", False, False, "Call or WhatsApp")}{chip("call2")}{chip("email")}{chip("map")}</div>
<h2 class="h4">Hours</h2><p>Monday to Friday 8am to 5pm<br>Saturday 10am to 3pm<br>Sunday closed<br><strong>Emergency line:</strong> call or WhatsApp.</p>
<p><a class="btn-wa" href="https://wa.me/{CO['wa']}" target="_blank" rel="noopener"><i class="fa-brands fa-whatsapp"></i> Chat on WhatsApp</a></p></div></div></div></section>
{related(R, [("Products", "products.html"), ("Services", "services.html"), ("Projects", "projects.html"), ("Locations", "pages/locations/index.html")])}</main>'''
    return page(R, "contact.html", "Contact EPS: Quote, Site Visit, WhatsApp | Lagos", "Contact Emel Project Solutions, 1 Limca Way, Isolo Industrial Estate, Lagos. Call +234 816 438 0620 or WhatsApp for a free quote.", body, "contact", [{"@type": "ContactPage", "name": "Contact EPS", "url": BASE + "/contact.html"}], crumb_trail=[("Home", ""), ("Contact", "contact.html")])

def legal(slug, title, h1, paras):
    p = "".join(f"<h2 class='h4 mt-4'>{a}</h2><p>{b}</p>" for a, b in paras)
    body = f'<main id="main">{crumbs([CRUMB_HOME, (h1, slug)], R)}{pagehead(h1, "Last updated: " + "2026. Have a lawyer review before launch.")}<section class="sec"><div class="wrap" style="max-width:820px">{p}<p class="mt-4">{chip("email", False, False, "Questions about this page")}</p></div></section></main>'
    return page(R, slug, title, f"{h1} for epsnigeria.com, operated by Emel Project Solutions, Lagos.", body, "", crumb_trail=[("Home", ""), (h1, slug)])

PRIV = [("What we collect", "When you send a form or message we collect your name, phone, email, state and what you need. We use it to reply and to prepare your quote."),
        ("How we use it", "We do not sell your details. We share them only with staff and contractors who work on your enquiry."),
        ("WhatsApp and forms", "If you choose WhatsApp, your message goes through WhatsApp and is covered by its terms. Form data is handled by our form provider."),
        ("Your rights", f"You can ask us to see, correct or delete your data under the Nigeria Data Protection Act. Email {CO['email']}.")]
TERMS = [("Use of this site", "The content is for information. Specifications and availability are confirmed in a written quote."),
         ("Quotes", "Quotes are valid for the period stated on them. Prices depend on site conditions, materials and exchange rates."),
         ("Liability", "EPS is not liable for loss from use of this website. Our project terms are set out in each signed quote or contract."),
         ("Governing law", "These terms are governed by the laws of the Federal Republic of Nigeria.")]

# ---------------------------------------------------------------- RUN
if __name__ == "__main__":
    for path, html_ in {"index.html": home(), "products.html": products(), "services.html": services(), "projects.html": projects(), "about.html": about(), "partners.html": partners(), "clients.html": clients(), "contact.html": contact(),
                        "privacy.html": legal("privacy.html", "Privacy Policy | EPS Nigeria", "Privacy Policy", PRIV), "terms.html": legal("terms.html", "Terms of Use | EPS Nigeria", "Terms of Use", TERMS)}.items():
        write(path, html_)
    print("root pages built")
