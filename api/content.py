"""Shared copy: FAQs, steps, projects, products, services. Facts come from the existing EPS site only."""
FAQS = [
("How much does warehouse racking cost in Nigeria?",
 "Price depends on pallet positions, beam load, height and steel grade, so we quote per project. Imported SSI SCHÄFER systems cost more than local fabrication but last longer and carry rated loads. Send your pallet count and ceiling height and we will price it after a free site visit."),
("How long does racking installation take?",
 "A typical single-warehouse job takes days to a few weeks, depending on pallet positions, building access and crew size. We confirm the programme in your quote. Installation starts after the floor is checked for flatness and the rack layout is signed off by your team."),
("Do you install outside Lagos?",
 "Yes. We have delivered and installed in all 36 states and the FCT. Our installation crews travel with the materials and tools, so a project in Kano, Port Harcourt or Abuja follows the same process as one in Lagos. Tell us the state when you request your quote."),
("How often should warehouse racks be inspected?",
 "Inspect racks at least once a year with a competent person, and check visually every week. Inspect straight away after any forklift impact. SEMA guidance supports this routine. EPS carries out SEMA-certified rack inspections and gives you a written damage report with repair priorities."),
("Are you the SSI SCHÄFER distributor in Nigeria?",
 "Yes. Emel Project Solutions is the exclusive SSI SCHÄFER partner in Nigeria for warehouse racking. We supply, install and service the systems. If another company claims to sell SSI SCHÄFER racking in Nigeria, ask them for written authorisation and contact us to confirm."),
("What is the difference between selective and drive-in racking?",
 "Selective racking gives direct access to every pallet and suits many different products. Drive-in racking packs pallets several deep in lanes that forklifts enter, so it saves floor space but works best for large volumes of one product. Pick selective for variety and drive-in for volume."),
("Do you supply shelving and mezzanine floors?",
 "Yes. Alongside pallet racking we supply light and medium duty shelving, multi-tier systems and mezzanine floors. A mezzanine adds floor area inside your existing building, can be moved or resized later, and comes with steel or concrete decking."),
("Can you inspect and repair racks you did not install?",
 "Yes. Our SEMA-certified inspectors assess any pallet racking, whoever supplied it. You get a report with damage photos, load capacity notes and a repair list. We can then replace damaged uprights and beams, or set up a planned maintenance schedule for the site."),
]
STEPS = [
("Enquiry and brief","You call, WhatsApp or fill the form. We ask what you store, the site location and your deadline."),
("Site visit","An EPS engineer visits, measures the building and checks floor and access. The visit is free."),
("Design and layout","We draw the rack layout around your pallets and forklifts and agree it with you."),
("Quotation","You get a written, no-obligation quote with scope, materials and programme."),
("Approval and order","You approve the drawing and quote. We place the order and plan delivery."),
("Supply","Racking comes from SSI SCHÄFER or our wider supplier network."),
("Delivery to site","We deliver and stage materials safely at your site, in any state."),
("Installation","Our crews install to the approved drawing, with safety checks as they go."),
("Inspection and handover","We check the finished work, test, and hand over load notices and documents."),
("After-sales support","Planned inspections, maintenance and spare parts when you need them."),
]
PROJECTS = [  # id, title, sector, state, state_slug, work done, client, image, date. Source: EPS project pages.
("west-african-cubes","Heavy-duty and shuttle racking","Warehousing","Ogun","ogun","Heavy-duty racking and a shuttle racking system.","West African Cubes, Shagamu","projects/west-african-cubes","Feb 2023 to Apr 2023"),
("dag-industries","Multi-tier racking","Warehousing","Ogun","ogun","Heavy-duty racking with a multi-tier platform and stairs.","DAG Industries, Shagamu","projects/dag-industries","Feb 2023 to Apr 2023"),
]
PROJECT_GALLERY = [("projects/cold-store-warehouse","Warehouse with heavy-duty racking")]
PBYID = {p[0]: p for p in PROJECTS}
PRODUCT_DETAIL = {
"racking":dict(img="06-heavy-duty-racking",ans="Emel Project Solutions is the exclusive SSI SCHÄFER partner in Nigeria. We supply, install and inspect selective and heavy-duty pallet racking, laid out around your pallets and forklifts.",specs=["Selective racking with direct access to every pallet","Heavy-duty beams and uprights for rated loads","Very narrow aisle layouts for 40-50% more storage","Double-deep runs for 30-40% more density"],uses="Factories, 3PL and logistics, retail distribution, e-commerce, FMCG.",svc="warehouse-solutions"),
"high-density":dict(img="07-shuttle-racking",ans="Drive-in, shuttle and mobile pallet racking pack more pallets into the same floor, for large volumes of fewer product lines.",specs=["Drive-in racking: about 60% more storage, LIFO operation","Shuttle racking: about 70% more storage, FIFO or FILO","Mobile pallet racking: up to 90% of floor space used","Best for high volumes and a low number of SKUs"],uses="Beverage plants, FMCG, cold stores and bulk distribution.",svc="warehouse-solutions"),
"cantilever":dict(img="08-cantilever-racks",ans="Cantilever racks hold long loads on open-fronted arms, so pipes, profiles and steel sections load from the side with nothing in the way.",specs=["Open front with no uprights in the loading face","Arms sized for pipes, profiles, timber and steel sections","Single- and double-sided runs","Suits side-loading forklifts and overhead cranes"],uses="Steel stockists, pipe yards and oil and gas supply bases.",svc="warehouse-solutions"),
"shelving":dict(img="22-ecommerce-warehouse",ans="Light and medium duty shelving and multi-tier systems store small parts and hand-picked items, with pick faces at working height.",specs=["Light and medium duty shelving","Multi-tier systems with stairs and walkways","Pick faces for e-commerce and spare parts","Adjustable shelf levels as stock changes"],uses="E-commerce fulfilment, spare parts, pharma and retail stock rooms.",svc="installation"),
"mezzanine":dict(img="projects/dag-industries",ans="A mezzanine floor adds usable floor area inside your existing warehouse, without moving or building new.",specs=["More floor area within the existing space","Cost-effective for manufacturing or storage","Quick, clean install; can be moved or resized later","Steel or concrete decking options"],uses="Warehouses, factories and stores that have height but no spare floor.",svc="installation"),
}
SERVICE_DETAIL = {
"warehouse-solutions":dict(name="Warehouse Solutions",img="03-warehouse-aisle",ans="We plan, supply and install warehouse racking as the exclusive SSI SCHÄFER partner in Nigeria, starting from your stock profile and building layout.",pts=["Pallet count and stock profile review","Rack layout drawing with aisle widths for your forklifts","Selective, drive-in, shuttle, cantilever and shelving systems","Floor, load and safety notices at handover"],prod="racking",cta="Get my racking quote"),
"rack-inspection":dict(name="Rack Inspection (SEMA)",img="16-rack-inspection",ans="EPS carries out SEMA-certified inspections of pallet racking, whoever installed it, and gives you a written report with repair priorities.",pts=["Check of uprights, beams, bracing and base plates","Damage photos and severity rating","Load capacity and notice check","Written report you can show your insurer"],prod="racking",cta="Book a rack inspection"),
"maintenance":dict(name="Maintenance",img="20-maintenance",ans="We keep racking safe and working with planned maintenance, repairs and spare parts. For urgent damage, call or WhatsApp the emergency line.",pts=["Planned inspection and repair visits","Replacement uprights, beams and guards","Re-levelling and re-aligning racks","Emergency line: call or WhatsApp"],prod="racking",cta="Ask about maintenance"),
"installation":dict(name="Installation",img="19-installation-team",ans="Our own crews install pallet racking, shelving, multi-tier systems and mezzanine floors in all 36 states and the FCT.",pts=["Floor and site check before install","Crews with the right tools and safety gear","Work to the approved drawing","Checks, load notices and handover after install"],prod="mezzanine",cta="Request an installation quote"),
}
SECTORS = [("Manufacturing","Raw material and finished goods racking.","services.html#warehouse-solutions"),
("Logistics","Pallet density for 3PL and distribution.","pages/locations/lagos.html"),
("Retail","Stock rooms and distribution centres.","products.html#shelving"),
("E-commerce","Shelving and pick-face layouts.","projects.html"),
("Oil and gas","Cantilever racks for pipes and spares.","products.html#cantilever"),
("FMCG","Fast-moving pallet storage.","products.html#racking")]

# SAMPLE testimonials: replace names, roles, companies and quotes with real ones, then re-run build_site.py
TESTIMONIALS = [
("The racking went in on the dates we agreed. Forklifts move freely and our pallet count went up. The EPS crew kept the site tidy.","Chidi Okafor","Warehouse Manager","Okafor Foods Ltd","Ogun"),
("We needed more pallet positions without moving site. EPS drew a drive-in layout and the new lanes were working before our peak season.","Amina Bello","Operations Manager","Northgate Distribution","FCT (Abuja)"),
("We asked for a rack inspection after a forklift hit. The report was clear, with photos and a repair list we could act on the same week.","Tunde Adeyemi","Facility Manager","Swiftline Logistics","Lagos"),
]
