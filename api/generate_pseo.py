#!/usr/bin/env python3
"""EPS location pages. Run from anywhere:  python3 api/generate_pseo.py
Writes pages/locations/index.html + 37 state pages (36 states + FCT), sitemap.xml, robots.txt, llms.txt.
Needs: pip install pillow  (used to read image sizes). Data lives in states_data.py, layout in site_core.py."""
import datetime, re
from site_core import *
from content import *
from states_data import STATES
from clients_data import CLIENTS
from build_site import faq_html, faq_schema, pagehead, related, proj_cards, CRUMB_HOME

R = "../../"
BYSLUG = {s["slug"]: s for s in STATES.values()}
ISO = dict(abia="AB", adamawa="AD", **{"akwa-ibom": "AK"}, anambra="AN", bauchi="BA", bayelsa="BY", benue="BE", borno="BO", **{"cross-river": "CR"}, delta="DE", ebonyi="EB", edo="ED", ekiti="EK", enugu="EN", gombe="GO", imo="IM", jigawa="JI", kaduna="KD", kano="KN", katsina="KT", kebbi="KE", kogi="KO", kwara="KW", lagos="LA", nasarawa="NA", niger="NI", ogun="OG", ondo="ON", osun="OS", oyo="OY", plateau="PL", rivers="RI", sokoto="SO", taraba="TA", yobe="YO", zamfara="ZA", fct="FC")
REGION_ORDER = ["Southwest", "South-South", "Southeast", "North-Central", "Northwest", "Northeast"]

REG = {
"Southwest": dict(proj="west-african-cubes", uses=["Port and import distribution, with racking sized for container-load pallets", "FMCG and beverage plants that need fast pallet turnover", "E-commerce fulfilment centres with shelving and pick faces", "Pharma and healthcare distributors needing organised shelving and pick faces"],
  p1="The southwest is Nigeria's densest market for storage. Factories, distributors and retailers here need pallet positions close to the Lagos ports and the Lagos-Ibadan corridor, and they need them quickly.",
  p2="Because our head office and stores are in Isolo, Lagos, projects in {name} are the shortest trips we run. Our engineers can visit, measure and return a drawing in the same week, and our installation crews are usually on site soon after approval.",
  env="Humidity and coastal air near the Lagos lagoon speed up corrosion, so we specify galvanised or powder-coated steel for racking where the site is close to water."),
"South-South": dict(proj="dag-industries", uses=["Oil and gas support yards and supply bases needing rated heavy-duty racking", "Port-side warehouses handling imports and project cargo", "Distributors and retailers needing pallet racking and shelving close to their market", "Cantilever racks for pipes, tubulars and long steel sections"],
  p1="The south-south runs on oil and gas support, ports and the businesses that serve them. Storage here is often heavy and long: pipe, spares, drums and project cargo, as well as ordinary pallets.",
  p2="We plan these jobs around site access, security rules and permit-to-work systems. Many yards need contractors to hold safety inductions, so we confirm requirements before our crews and materials leave Lagos.",
  env="Heavy rain, flooding risk and salty air mean we check floor levels and drainage first, and we use corrosion-resistant finishes on racking and frames."),
"Southeast": dict(proj="dag-industries", uses=["Market-city distribution warehouses with dense pallet storage", "Manufacturing and auto-parts stores with shelving for small items", "Pharma and healthcare stores needing shelving and multi-tier systems", "Wholesale traders needing mezzanine floors to add space in the same building"],
  p1="The southeast is a trading and making region. Warehouses here hold a wide mix of goods, from spare parts to food, so flexible racking and strong shelving matter more than one-product lanes.",
  p2="We supply from Lagos and route trucks along the main southeast corridors. Installation crews stay on site until handover, so you are not left to finish alone.",
  env="Seasonal heavy rain is the main site risk. We schedule deliveries around it and protect racking components in transit and on site."),
"North-Central": dict(proj="west-african-cubes", uses=["Abuja FMCG and pharma depots needing selective pallet racking", "Government and institutional supply stores needing shelving and racking", "Distribution depots serving the north and the south, with pallet racking", "Agro-processing stores needing racking and shelving"],
  p1="North-central Nigeria connects the north and the south. Abuja drives commercial growth, and the states around it carry freight, distribution and agro-processing.",
  p2="We have delivered across the region from our Lagos base. For new warehouses in the FCT and neighbouring states we coordinate with your main contractor on programme, so racking installation fits the build sequence.",
  env="Heat in the dry season and heavy rain in the wet season both affect site work. We plan installation windows around them and specify finishes that hold colour in strong sun."),
"Northwest": dict(proj="west-african-cubes", uses=["Agro-processing and grain storage with pallet racking", "Textile, food and commodity warehouses in industrial estates", "Food and beverage plants needing high-density drive-in or shuttle racking", "Distribution depots supplying the wider north"],
  p1="The northwest is Nigeria's largest farming and trading belt. Grain, groundnut, hides and manufactured goods all move through its warehouses, and many sites want more storage in the same footprint.",
  p2="We ship racking and shelving to the northwest on a planned schedule, and our crews install on site. For long hauls we confirm delivery dates in the quote so your site team knows when to expect trucks.",
  env="Dust and harmattan haze are the main site conditions. We keep installation areas clean and choose finishes that clean easily."),
"Northeast": dict(proj="dag-industries", uses=["Trade and humanitarian logistics warehouses needing secure pallet storage", "Agro and livestock product stores with shelving and racking", "Medical and public supply stores needing shelving and clear stock control", "Commercial warehouses needing mezzanine floors to add storage space"],
  p1="The northeast needs dependable storage close to its trade routes. Warehouses here support commerce, agriculture and relief supply chains, and they need racking that is safe, simple and quick to fit.",
  p2="We plan northeast projects carefully around security, road conditions and delivery routes, and we confirm the programme in writing. Our team will tell you plainly if a date is at risk and what we are doing about it.",
  env="Very hot, dry conditions affect site work and finishes. We plan site work for cooler periods and choose finishes suited to strong sun."),
}

def state_page(s):
    n, slug, rg = s["name"], s["slug"], REG[s["region"]]
    short = n.replace(" (Abuja)", "")
    cities = ", ".join(s["cities"][:-1]) + " and " + s["cities"][-1] if len(s["cities"]) > 1 else s["cities"][0]
    nbs = [BYSLUG[x] for x in s["nb"][:4]]
    nb_links = ", ".join(f'<a href="{slug_}.html">{b["name"]}</a>' for b in nbs for slug_ in [b["slug"]])
    nb_pl = "".join(f'<a href="{b["slug"]}.html">Racking and shelving in {b["name"]}</a>' for b in nbs[:3])
    proj = PBYID[rg["proj"]]
    faqs = [
      (f"Do you install warehouse racking in {short}?", f"Yes. EPS supplies and installs warehouse racking in {short} and across {s['region']} Nigeria. We visit your site in {s['cities'][0]}, draw a layout for your pallets and forklifts, and install with our own crews. Send your pallet count and ceiling height to start."),
      (f"Can you supply shelving and mezzanine floors in {short}?", f"Yes. We supply and install light and medium duty shelving, multi-tier systems and mezzanine floors in {cities}. A mezzanine adds floor area inside your existing building, with steel or concrete decking. Your quote lists every bay, level and load before you approve."),
      (f"Who inspects pallet racking in {short}?", f"EPS carries out SEMA-certified rack inspections in {short}, whoever installed the racks. You receive a written report with photos of damage and a repair priority list. Check racks weekly yourself and book a full inspection at least once a year."),
    ]
    body = f'''<main id="main">{crumbs([CRUMB_HOME, ("Locations", "pages/locations/index.html"), (n, f"pages/locations/{slug}.html")], R)}
{pagehead(f"Warehouse racking and storage systems in {short}", f"Emel Project Solutions supplies and installs warehouse racking, shelving and mezzanine floors in {short}, with a free site visit.")}
<section class="sec"><div class="wrap"><div class="row g-5"><div class="col-lg-7 rv"><p class="answer">Emel Project Solutions (EPS) supplies and installs warehouse racking and storage systems in {n}. We are the exclusive SSI SCHÄFER partner in Nigeria and carry out SEMA-certified rack inspections in {cities}.</p>
<p>{rg["p1"]}</p><p>In {short}, our work centres on {s["focus"]}.</p><p>{rg["p2"].format(name=short)}</p><p>{rg["env"]}</p></div>
<div class="col-lg-5 rv"><dl><dt>Region</dt><dd>{s["region"]}</dd><dt>Main cities we serve</dt><dd>{cities}</dd><dt>Based in</dt><dd>Isolo, Lagos</dd><dt>Call</dt><dd>{call_chip(False, 'Call us')}</dd><dt>Response</dt><dd>Free site visit and no-obligation quote</dd></dl>
<a class="btn-eps" data-wa="a quote in {short}" href="#">Get my {short} quote</a></div></div></div></section>
<section class="sec paper"><div class="wrap"><span class="bar"></span><h2>What clients in {short} usually need</h2><ul class="fs-5">{"".join(f"<li>{u}</li>" for u in rg["uses"])}</ul>
<p>See the systems: <a href="../../products.html#racking">warehouse racking</a>, <a href="../../products.html#high-density">drive-in and shuttle racking</a>, <a href="../../products.html#cantilever">cantilever racking</a>, <a href="../../products.html#shelving">shelving</a> and <a href="../../products.html#mezzanine">mezzanine floors</a>. Services: <a href="../../services.html#warehouse-solutions">warehouse solutions</a>, <a href="../../services.html#rack-inspection">rack inspection</a>, <a href="../../services.html#maintenance">maintenance</a> and <a href="../../services.html#installation">installation</a>.</p></div></section>
<section class="sec"><div class="wrap"><h2 class="mb-4">Recent EPS work</h2><div class="row g-4">{proj_cards(R, [proj])}<div class="col-md-6 col-lg-8 rv"><h3>How a job in {short} runs</h3><ol><li>You call or WhatsApp with your site and need.</li><li>We visit {s["cities"][0]} and measure.</li><li>You approve a drawing and written quote.</li><li>We deliver, install, inspect and hand over.</li></ol><p class="mb-2"><strong>Nearby states</strong></p><div class="linkgrid">{nb_links}</div><p class="mt-3 d-flex gap-3 flex-wrap"><a class="alink" href="index.html">All locations <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a><a class="alink" href="../../contact.html">Contact us <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a></p></div></div></div></section>
<section class="sec paper"><div class="wrap"><div class="row g-5"><div class="col-lg-4"><span class="bar"></span><h2>Questions from {short}</h2></div><div class="col-lg-8">{faq_html(faqs, "s")}</div></div></div></section>
<section class="sec"><div class="wrap"><h2 class="h4">Also covering {s["region"]}</h2><div class="linkgrid mt-3">{nb_pl}<a href="../../projects.html">All projects</a><a href="../../about.html">About EPS</a></div></div></section>
{cta_band(R, f"Get a quote for {short}", "Tell us the site and the need. We are available 24/7.", "a quote in " + short)}</main>'''
    sch = [faq_schema(faqs), {"@type": "Service", "name": f"Warehouse racking and storage systems in {short}", "provider": {"@id": BASE + "/#org"}, "areaServed": {"@type": "State" if slug != "fct" else "AdministrativeArea", "name": short},
          "description": f"Supply and installation of warehouse racking, shelving and mezzanine floors in {short}, Nigeria."}]
    title = f"Warehouse Racking & Shelving in {short} | EPS"
    desc = f"Warehouse racking, shelving, mezzanine floors and rack inspection in {short}. Exclusive SSI SCHÄFER partner in Nigeria. Free site visit."
    geo = {"pos": f"{s['lat']};{s['lng']}", "place": f"{short}, Nigeria", "region": f"NG-{ISO[slug]}"}
    return page(R, f"pages/locations/{slug}.html", title, desc, body, "locations", sch, crumb_trail=[("Home", ""), ("Locations", "pages/locations/index.html"), (n, f"pages/locations/{slug}.html")], geo=geo)

def hub():
    groups = ""
    for rg in REGION_ORDER:
        items = "".join(f'<a href="{s["slug"]}.html">{s["name"]}<small class="d-block fw-normal text-secondary">{", ".join(s["cities"][:2])}</small></a>' for s in sorted(STATES.values(), key=lambda x: x["name"]) if s["region"] == rg)
        groups += f'<section class="sec{" paper" if REGION_ORDER.index(rg) % 2 else ""}" style="padding:3rem 0"><div class="wrap"><h2 class="h3">{rg}</h2><div class="linkgrid mt-3">{items}</div></div></section>'
    ilist = {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s["name"], "url": f"{BASE}/pages/locations/{s['slug']}.html"} for i, s in enumerate(sorted(STATES.values(), key=lambda x: x["name"]))]}
    body = f'''<main id="main">{crumbs([CRUMB_HOME, ("Locations", "pages/locations/index.html")], R)}{pagehead("Warehouse racking in all 36 states", "EPS delivers and installs in every Nigerian state and the FCT. Pick your state to see what we do there.")}
<section class="sec" style="padding-bottom:1rem"><div class="wrap"><p class="answer">Emel Project Solutions is based in Isolo, Lagos and works in all 36 states and the FCT. Our crews travel with the materials, so the process is the same in Lagos, Kano, Port Harcourt or Abuja.</p></div></section>{groups}
{related(R, [("Racking", "products.html#racking"), ("Shelving", "products.html#shelving"), ("Installation", "services.html#installation"), ("Projects", "projects.html"), ("Contact", "contact.html")])}{cta_band(R, "Not sure we cover your town?", "We do. Tell us where the site is.", "Locations")}</main>'''
    return page(R, "pages/locations/index.html", "Where We Work: All 36 States + FCT | EPS Nigeria", "EPS installs warehouse racking, shelving and mezzanine floors in all 36 Nigerian states and the FCT. Find your state page.", body, "locations", [{"@type": "CollectionPage", "name": "EPS locations", "url": BASE + "/pages/locations/index.html"}, ilist], crumb_trail=[("Home", ""), ("Locations", "pages/locations/index.html")])

def sitemap():
    today = datetime.date.today().isoformat()
    urls = [("", "1.0"), ("products.html", "0.9"), ("services.html", "0.9"), ("projects.html", "0.8"), ("about.html", "0.7"), ("partners.html", "0.6"), ("clients.html", "0.6"), ("contact.html", "0.8"), ("privacy.html", "0.2"), ("terms.html", "0.2"), ("pages/locations/index.html", "0.8")]
    urls += [(f"pages/locations/{s['slug']}.html", "0.6") for s in sorted(STATES.values(), key=lambda x: x["slug"])]
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    x += "".join(f"  <url><loc>{BASE}/{u}</loc><lastmod>{today}</lastmod><priority>{p}</priority></url>\n" for u, p in urls)
    return x + "</urlset>\n"

ROBOTS = f"""User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: {BASE}/sitemap.xml
"""

def llms():
    st = "\n".join(f"- [{s['name']}]({BASE}/pages/locations/{s['slug']}.html): {s['region']}, {', '.join(s['cities'][:2])}" for s in sorted(STATES.values(), key=lambda x: x["name"]))
    return f"""# Emel Project Solutions (EPS), also known as {AKA}

> Emel Project Solutions, also known as {AKA}, is the exclusive SSI SCHÄFER partner in Nigeria. EPS supplies and installs warehouse racking, shelving and mezzanine floors in all 36 states and the FCT. It also provides SEMA-certified rack inspection and maintenance. Founded 2009. 500+ projects, 200+ clients.

## Facts
- Head office: {CO['street']}, Lagos, Nigeria
- Phone: {CO['phone1']} | {CO['phone2']}
- WhatsApp: https://wa.me/{CO['wa']}
- Email: {CO['email']}
- Hours: Open 24/7. Emergency line: call or WhatsApp.
- Certifications: SEMA certified

## Key pages
- [Home]({BASE}/): overview and FAQ
- [Products]({BASE}/products.html): pallet racking, drive-in and shuttle racking, cantilever racking, shelving and multi-tier, mezzanine floors
- [Services]({BASE}/services.html): warehouse solutions, rack inspection, maintenance, installation
- [Projects]({BASE}/projects.html)
- [Partners]({BASE}/partners.html): SSI SCHÄFER exclusive partnership
- [About]({BASE}/about.html)
- [Contact]({BASE}/contact.html)
- [All locations]({BASE}/pages/locations/index.html)

## Selected clients
{', '.join(n for n, _ in CLIENTS)}

## Locations
{st}
"""

def words(html_):
    t = re.sub(r"<(script|style)[\s\S]*?</\1>", "", html_); t = re.sub(r"<[^>]+>", " ", t)
    return len(t.split())

if __name__ == "__main__":
    mn = 9999
    for s in STATES.values():
        h = state_page(s); write(f"pages/locations/{s['slug']}.html", h)
        body = h.split('<main id="main">')[1].split("</main>")[0]; mn = min(mn, words(body))
    write("pages/locations/index.html", hub()); write("sitemap.xml", sitemap()); write("robots.txt", ROBOTS); write("llms.txt", llms())
    print("37 state pages + hub written. Fewest words on a state page:", mn)
