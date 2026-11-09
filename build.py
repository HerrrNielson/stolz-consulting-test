# -*- coding: utf-8 -*-
"""
Stolz Consulting – statischer Seitengenerator.

Erzeugt alle HTML-Seiten (Deutsch unter /, Englisch unter /en/) aus den
Inhalten in dieser Datei. Nach einer Textänderung einfach neu ausführen:

    python build.py

Inhalte stammen 1:1 von https://www.stolz-consulting.net/ (Stand Nov. 2026);
die englischen Texte sind Übersetzungen davon.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent
DOMAIN = "https://www.stolz-consulting.net"

# --------------------------------------------------------------------------
# Seitenstruktur: key -> (Pfad DE, Pfad EN)
# --------------------------------------------------------------------------
PATHS = {
    "home":        ("",             "en/"),
    "profil":      ("profil/",      "en/profile/"),
    "referenzen":  ("referenzen/",  "en/references/"),
    "kontakt":     ("kontakt/",     "en/contact/"),
    "impressum":   ("impressum/",   "en/imprint/"),
    "datenschutz": ("datenschutz/", "en/privacy/"),
}
LANGS = ("de", "en")

CONTACT = {
    "phone_display": {"de": "0664/5302624", "en": "+43 664 5302624"},
    "phone_href": "tel:+436645302624",
    "email": "office@stolz-consulting.net",
    "street": "Brünngraben 10",
    "city": "8444 St. Andrä-Höch",
    "country": {"de": "Österreich", "en": "Austria"},
}

# Referenzen in der Reihenfolge des Originals; None = kein Logo vorhanden
REFERENCES = [
    ("ams - austriamicrosystems AG", "ams.svg"),
    ("ATB Austria Antriebstechnik AG", "atb.svg"),
    ("AVL List GmbH", "avl.png"),
    ("BFI Steiermark", "bfi.jpg"),
    ("Efkon AG", "efkon.jpeg"),
    ("FH Campus 02", "campus-02.jpeg"),
    ("FH Hamburg", "fh-hamburg.png"),
    ("Frauenthal Holding AG", "frauenthal.jpeg"),
    ("Kurzentrum Althofen GmbH", "kurzentrum-althofen.png"),
    ("Land- und forstwirtschaftliche Ausbildungsstätte Steiermark", None),
    ("Meadwestvaco GmbH", "meadwestvaco.png"),
    ("Pädagogische Hochschule Steiermark", "ph-steiermark.svg"),
    ("Saubermacher Dienstleistungs AG", "saubermacher.jpeg"),
    ("Security KAG", "security-kag.png"),
    ("VAE GmbH", "vae.png"),
    ("voestalpine AG", "voestalpine.png"),
    ("Universität Graz", "universitaet-graz.svg"),
    ("WIFI Steiermark", "wifi.png"),
    ("ZAT GmbH", None),
]

# --------------------------------------------------------------------------
# UI-Texte
# --------------------------------------------------------------------------
T = {
    "de": {
        "nav": [("profil", "Profil"), ("referenzen", "Referenzen"), ("kontakt", "Kontakt")],
        "skip": "Zum Inhalt springen",
        "menu": "Menü öffnen",
        "nav_label": "Hauptnavigation",
        "lang_label": "Sprache",
        "brand_sub": "Mag. Dr. Sabine Stolz, MSc",
        "home_label": "Stolz Consulting – Startseite",
        "footer_kicker": "Stolz Consulting",
        "footer_claim": "Unternehmensberatung mit Struktur, Erfahrung und internationalem Blick.",
        "phone": "Telefon", "email": "E-Mail", "address": "Adresse",
        "imprint": "Impressum", "privacy": "Datenschutz",
        "other_lang": "English",
        "contact_cta": "Kontakt aufnehmen",
        "og_locale": "de_AT",
    },
    "en": {
        "nav": [("profil", "Profile"), ("referenzen", "References"), ("kontakt", "Contact")],
        "skip": "Skip to content",
        "menu": "Open menu",
        "nav_label": "Main navigation",
        "lang_label": "Language",
        "brand_sub": "Mag. Dr. Sabine Stolz, MSc",
        "home_label": "Stolz Consulting – Home",
        "footer_kicker": "Stolz Consulting",
        "footer_claim": "Management consulting with structure, experience and an international perspective.",
        "phone": "Phone", "email": "Email", "address": "Address",
        "imprint": "Imprint", "privacy": "Privacy policy",
        "other_lang": "Deutsch",
        "contact_cta": "Get in touch",
        "og_locale": "en_GB",
    },
}

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICON_PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'


def rel(from_key, lang, to_key, to_lang=None):
    """Relativer Link von einer Seite zu einer anderen."""
    to_lang = to_lang or lang
    src = PATHS[from_key][LANGS.index(lang)]
    dst = PATHS[to_key][LANGS.index(to_lang)]
    depth = src.count("/")
    return ("../" * depth + dst) or "./"


def asset(key, lang, path):
    depth = PATHS[key][LANGS.index(lang)].count("/")
    return "../" * depth + "assets/" + path


def logo_grid(key, lang, items, names=False):
    out = []
    for name, file in items:
        if file:
            img = f'<img src="{asset(key, lang, "img/referenzen/" + file)}" alt="{escape(name)}" loading="lazy">'
            cap = f'<span class="logo-name">{escape(name)}</span>' if names else ""
            out.append(f"<li>{img}{cap}</li>")
        else:
            out.append(f'<li><span class="logo-text">{escape(name)}</span></li>')
    cls = "logo-grid logo-grid--names" if names else "logo-grid"
    return f'<ul class="{cls} reveal">' + "".join(out) + "</ul>"


# --------------------------------------------------------------------------
# Seiteninhalte
# --------------------------------------------------------------------------
def page_home(lang):
    k = "home"
    a = lambda p: asset(k, lang, p)
    L = lambda to: rel(k, lang, to)
    logos = [r for r in REFERENCES if r[1]][:12]
    if lang == "de":
        return dict(
            title="Stolz Consulting – Unternehmensberatung | Mag. Dr. Sabine Stolz, MSc",
            desc="Unternehmensberatung von Mag. Dr. Sabine Stolz, MSc: Management, Controlling, Finanzierung, Internationalisierung und IT-Lösungen für KMU – seit 2005.",
            body=f"""
    <section class="hero">
      <div class="container hero__grid">
        <div class="reveal">
          <p class="eyebrow">Unternehmensberatung</p>
          <p class="hero__name">Mag. Dr. Sabine Stolz, MSc</p>
          <h1 class="h1">Lassen Sie keine kostbare Zeit <em>vergehen!</em></h1>
          <blockquote class="hero__quote">„Wer das Ziel kennt, findet seinen Weg!“</blockquote>
          <div class="hero__text">
            <p class="intro">Sie haben eine Vision des Erfolgs Ihrer Firma? Nur der Weg dahin ist noch offen?</p>
            <p>Der Umgang mit komplexen Managementsituationen, Controllingstrategien, internationalen Herausforderungen und die Umsetzung zu benutzerfreundlichen IT-Lösungen sowie die Entwicklung kosteneffektiver Pläne zur Steigerung der Produktivität Ihres Unternehmens sind meine Spezialgebiete.</p>
          </div>
          <div class="hero__actions">
            <a class="btn btn--primary" href="{L('kontakt')}">Kontakt aufnehmen {ARROW}</a>
            <a class="btn btn--ghost" href="{L('profil')}">Profil ansehen</a>
          </div>
        </div>
        <div class="hero__media reveal">
          <picture>
            <source type="image/webp" srcset="{a('img/portrait.webp')}">
            <img src="{a('img/portrait.jpg')}" alt="Portrait von Mag. Dr. Sabine Stolz, MSc" width="313" height="474" fetchpriority="high">
          </picture>
          <div class="hero__badge"><span>Seit 2005</span><strong>Beratung für KMU, Finanzen und IT</strong></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container services__grid">
        <div class="reveal">
          <p class="eyebrow">Leistungsschwerpunkte</p>
          <h2 class="h2">Passende Unterstützung von Strategie bis <em>Umsetzung.</em></h2>
        </div>
        <ul class="service-list reveal">
          <li>Innovative und individuelle IT-Lösungen</li>
          <li>Maßgeschneiderte Finanzierungen</li>
          <li>Kurzzeitige und langfristige Beratung</li>
          <li>Set-up und Training</li>
          <li>Technologie, Management und Support</li>
        </ul>
      </div>
    </section>

    <section class="section section--cream">
      <div class="container split">
        <div class="split__media reveal">
          <picture>
            <source type="image/webp" srcset="{a('img/city.webp')}">
            <img src="{a('img/city.jpg')}" alt="Stadtansicht als Symbol für internationale Unternehmensberatung" width="999" height="520" loading="lazy">
          </picture>
        </div>
        <div class="split__text reveal">
          <p class="eyebrow">Arbeitsweise</p>
          <h2 class="h2">Klar, individuell und auf nachhaltige Wirkung ausgerichtet.</h2>
          <div class="prose">
            <p>Ich begleite Unternehmen bei komplexen wirtschaftlichen Fragestellungen mit einer Verbindung aus fundierter Finanzkompetenz, internationaler Erfahrung und praxisnahen IT-Lösungen.</p>
            <p>Im Mittelpunkt stehen tragfähige Konzepte, umsetzbare Strategien und eine Beratung, die sowohl kurzfristige Herausforderungen als auch langfristige Entwicklungen Ihres Unternehmens im Blick behält.</p>
          </div>
          <a class="link-arrow" href="{L('profil')}">Zum Profil {ARROW}</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head section__head--row reveal">
          <div>
            <p class="eyebrow">Referenzen</p>
            <h2 class="h2">Auswahl bisheriger Zusammenarbeit</h2>
          </div>
          <a class="link-arrow" href="{L('referenzen')}">Alle Referenzen {ARROW}</a>
        </div>
        {logo_grid(k, lang, logos)}
      </div>
    </section>

    <section class="section section--dark">
      <div class="container cta reveal">
        <div>
          <p class="eyebrow">Kontakt</p>
          <h2 class="h2">Sie interessieren sich für meine Leistungen?</h2>
        </div>
        <a class="btn btn--light" href="{L('kontakt')}">Kontakt aufnehmen {ARROW}</a>
      </div>
    </section>""")
    return dict(
        title="Stolz Consulting – Management Consulting | Mag. Dr. Sabine Stolz, MSc",
        desc="Management consulting by Mag. Dr. Sabine Stolz, MSc: management, controlling, financing, internationalisation and IT solutions for SMEs – since 2005.",
        body=f"""
    <section class="hero">
      <div class="container hero__grid">
        <div class="reveal">
          <p class="eyebrow">Management consulting</p>
          <p class="hero__name">Mag. Dr. Sabine Stolz, MSc</p>
          <h1 class="h1">Don’t let valuable time <em>slip away!</em></h1>
          <blockquote class="hero__quote">“Those who know the goal will find their way!”</blockquote>
          <div class="hero__text">
            <p class="intro">You have a vision of your company’s success? Only the path to get there is still open?</p>
            <p>Handling complex management situations, controlling strategies and international challenges, implementing user-friendly IT solutions and developing cost-effective plans to increase your company’s productivity are my areas of expertise.</p>
          </div>
          <div class="hero__actions">
            <a class="btn btn--primary" href="{L('kontakt')}">Get in touch {ARROW}</a>
            <a class="btn btn--ghost" href="{L('profil')}">View profile</a>
          </div>
        </div>
        <div class="hero__media reveal">
          <picture>
            <source type="image/webp" srcset="{a('img/portrait.webp')}">
            <img src="{a('img/portrait.jpg')}" alt="Portrait of Mag. Dr. Sabine Stolz, MSc" width="313" height="474" fetchpriority="high">
          </picture>
          <div class="hero__badge"><span>Since 2005</span><strong>Consulting for SMEs, finance and IT</strong></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container services__grid">
        <div class="reveal">
          <p class="eyebrow">Key services</p>
          <h2 class="h2">The right support, from strategy to <em>implementation.</em></h2>
        </div>
        <ul class="service-list reveal">
          <li>Innovative and individual IT solutions</li>
          <li>Tailor-made financing</li>
          <li>Short-term and long-term consulting</li>
          <li>Set-up and training</li>
          <li>Technology, management and support</li>
        </ul>
      </div>
    </section>

    <section class="section section--cream">
      <div class="container split">
        <div class="split__media reveal">
          <picture>
            <source type="image/webp" srcset="{a('img/city.webp')}">
            <img src="{a('img/city.jpg')}" alt="City skyline as a symbol of international management consulting" width="999" height="520" loading="lazy">
          </picture>
        </div>
        <div class="split__text reveal">
          <p class="eyebrow">Approach</p>
          <h2 class="h2">Clear, individual and focused on lasting impact.</h2>
          <div class="prose">
            <p>I support companies with complex business challenges, combining sound financial expertise, international experience and practical IT solutions.</p>
            <p>The focus is on viable concepts, actionable strategies and advice that keeps both your company’s short-term challenges and its long-term development in view.</p>
          </div>
          <a class="link-arrow" href="{L('profil')}">View profile {ARROW}</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head section__head--row reveal">
          <div>
            <p class="eyebrow">References</p>
            <h2 class="h2">A selection of past collaborations</h2>
          </div>
          <a class="link-arrow" href="{L('referenzen')}">All references {ARROW}</a>
        </div>
        {logo_grid(k, lang, logos)}
      </div>
    </section>

    <section class="section section--dark">
      <div class="container cta reveal">
        <div>
          <p class="eyebrow">Contact</p>
          <h2 class="h2">Interested in my services?</h2>
        </div>
        <a class="btn btn--light" href="{L('kontakt')}">Get in touch {ARROW}</a>
      </div>
    </section>""")


def page_profil(lang):
    k = "profil"
    a = lambda p: asset(k, lang, p)
    de = lang == "de"
    if de:
        edu = [("Angewandte Betriebswirtschaft", "Spezialisierung Controlling, Finanzierung, Steuern"),
               ("Wirtschaftspädagogik", "Spezialisierung Didaktik, Wirtschaftsethik"),
               ("Internationales Management", "Doktoratsstudium")]
        career = [("VAE AG", "Konzerncontrolling, Auslandsaufenthalte in Russland und im Baltikum", False),
                  ("AVL", "Spartencontrolling, Auslandsaufenthalte in Russland, China, USA und Frankreich", False),
                  ("ZAT", "Leitung Finanzen", False),
                  ("Ceram Catalysts", "Finanzprokurist, Financial Report Analyst Manager, Auslandsaufenthalte in Frankreich und Deutschland", False),
                  ("Seit 2005", "Selbständige Unternehmensberaterin, Beratung von KMU, Vortragstätigkeit an Fachhochschulen und Weiterbildungsakademien", True),
                  ("Laufend", "Lehraufträge an internationalen Bildungseinrichtungen in den Bereichen Finanzen, Bilanzierung, Steuerrecht und ERP-Software", True)]
        tags = ["SAP-Module: FI, CO, TR, EC, IM", "Hyperion-Administrator-Ausbildung", "BMD Buchhaltung und Kostenrechnung", "Cognos", "Navision"]
        checks = ["Fachseminare in Controlling, Steuerrecht, Finanzierungen, Liquiditätsmanagement, Internationalisierung, Projektmanagement und Wirtschaftsethik",
                  "Seit 2018 zertifizierte Lehrbeauftragte in der Jugend- und Erwachsenenbildung"]
        t = dict(title="Profil – Mag. Dr. Sabine Stolz, MSc | Stolz Consulting",
                 desc="Ausbildung, berufliche Laufbahn und Zusatzqualifikationen von Mag. Dr. Sabine Stolz, MSc – selbständige Unternehmensberaterin seit 2005.",
                 eyebrow="Profil", h1="Warum mein <em>Unternehmen?</em>",
                 lead="Profitieren Sie von meiner umfangreichen nationalen und internationalen Erfahrung bei komplexen wirtschaftlichen Problemstellungen.",
                 role="Unternehmensberatung", langs_k="Sprachen", langs_v="Englisch, Französisch, Russisch",
                 since_k="Selbständig", since_v="Seit 2005",
                 h_edu="Ausbildung", h_career="Berufliche Laufbahn", h_extra="Zusatzqualifikationen",
                 alt="Mag. Dr. Sabine Stolz, MSc")
    else:
        edu = [("Applied Business Administration", "Specialisation in controlling, financing, taxation"),
               ("Business Education", "Specialisation in didactics, business ethics"),
               ("International Management", "Doctoral studies")]
        career = [("VAE AG", "Group controlling, assignments abroad in Russia and the Baltic states", False),
                  ("AVL", "Divisional controlling, assignments abroad in Russia, China, the USA and France", False),
                  ("ZAT", "Head of Finance", False),
                  ("Ceram Catalysts", "Authorised signatory (Prokurist) for finance, Financial Report Analyst Manager, assignments abroad in France and Germany", False),
                  ("Since 2005", "Self-employed management consultant, consulting for SMEs, lecturing at universities of applied sciences and further education academies", True),
                  ("Ongoing", "Teaching assignments at international educational institutions in finance, accounting, tax law and ERP software", True)]
        tags = ["SAP modules: FI, CO, TR, EC, IM", "Hyperion administrator training", "BMD accounting and cost accounting", "Cognos", "Navision"]
        checks = ["Specialist seminars in controlling, tax law, financing, liquidity management, internationalisation, project management and business ethics",
                  "Since 2018: certified lecturer in youth and adult education"]
        t = dict(title="Profile – Mag. Dr. Sabine Stolz, MSc | Stolz Consulting",
                 desc="Education, career and additional qualifications of Mag. Dr. Sabine Stolz, MSc – self-employed management consultant since 2005.",
                 eyebrow="Profile", h1="Why choose <em>my firm?</em>",
                 lead="Benefit from my extensive national and international experience with complex business challenges.",
                 role="Management consulting", langs_k="Languages", langs_v="English, French, Russian",
                 since_k="Self-employed", since_v="Since 2005",
                 h_edu="Education", h_career="Career", h_extra="Additional qualifications",
                 alt="Mag. Dr. Sabine Stolz, MSc")

    edu_html = "".join(f"<li><strong>{escape(x)}</strong><span>{escape(y)}</span></li>" for x, y in edu)
    cur = ' class="is-current"'
    car_html = "".join(f'<li{cur if c else ""}><strong>{escape(x)}</strong><span>{escape(y)}</span></li>' for x, y, c in career)
    tag_html = "".join(f"<li>{escape(x)}</li>" for x in tags)
    chk_html = "".join(f"<li>{escape(x)}</li>" for x in checks)
    return dict(title=t["title"], desc=t["desc"], body=f"""
    <section class="page-hero">
      <div class="container reveal">
        <p class="eyebrow">{t['eyebrow']}</p>
        <h1 class="h1">{t['h1']}</h1>
        <p class="lead">{t['lead']}</p>
      </div>
    </section>

    <section class="section">
      <div class="container profile">
        <aside class="profile__aside reveal">
          <picture>
            <source type="image/webp" srcset="{a('img/portrait.webp')}">
            <img src="{a('img/portrait.jpg')}" alt="{t['alt']}" width="313" height="474">
          </picture>
          <div class="profile__card">
            <p class="name">Mag. Dr. Sabine Stolz, MSc</p>
            <p class="role">{t['role']}</p>
            <dl>
              <dt>{t['langs_k']}</dt><dd>{t['langs_v']}</dd>
              <dt>{t['since_k']}</dt><dd>{t['since_v']}</dd>
            </dl>
          </div>
        </aside>

        <div>
          <div class="profile__block reveal">
            <p class="eyebrow">01</p>
            <h2 class="h3">{t['h_edu']}</h2>
            <ul class="edu-list">{edu_html}</ul>
          </div>
          <div class="profile__block reveal">
            <p class="eyebrow">02</p>
            <h2 class="h3">{t['h_career']}</h2>
            <ol class="timeline">{car_html}</ol>
          </div>
          <div class="profile__block reveal">
            <p class="eyebrow">03</p>
            <h2 class="h3">{t['h_extra']}</h2>
            <ul class="tags">{tag_html}</ul>
            <ul class="check-list">{chk_html}</ul>
          </div>
        </div>
      </div>
    </section>
{cta_block(k, lang)}""")


def cta_block(k, lang):
    if lang == "de":
        h, b = "Sie interessieren sich für meine Leistungen?", "Kontakt aufnehmen"
        e = "Kontakt"
    else:
        h, b = "Interested in my services?", "Get in touch"
        e = "Contact"
    return f"""
    <section class="section section--dark">
      <div class="container cta reveal">
        <div>
          <p class="eyebrow">{e}</p>
          <h2 class="h2">{h}</h2>
        </div>
        <a class="btn btn--light" href="{rel(k, lang, 'kontakt')}">{b} {ARROW}</a>
      </div>
    </section>"""


def page_referenzen(lang):
    k = "referenzen"
    if lang == "de":
        t = dict(title="Referenzen – Stolz Consulting | Mag. Dr. Sabine Stolz, MSc",
                 desc="Schwerpunkte, Erfahrung und eine Auswahl bisheriger Zusammenarbeit von Stolz Consulting.",
                 eyebrow="Referenzen", h1="Schwerpunkte und <em>Erfahrung</em>",
                 lead="Langjährige nationale und internationale Erfahrung in betriebswirtschaftlichen, finanziellen und IT-nahen Fragestellungen.",
                 label="Erfahrung", e2="Unternehmen und Institutionen", h2="Auswahl bisheriger Zusammenarbeit", more="u. v. m.")
        items = [("Controlling und Finanzsteuerung", "Begleitung bei Planung, Steuerung, Reporting und wirtschaftlicher Weiterentwicklung."),
                 ("Internationalisierung und Wachstumsbegleitung", "Unterstützung bei internationalen Herausforderungen, Expansion und organisatorischer Entwicklung."),
                 ("ERP-nahe Prozess- und IT-Beratung", "Verbindung betriebswirtschaftlicher Anforderungen mit benutzerfreundlichen und praxistauglichen IT-Lösungen."),
                 ("Training, Vorträge und Wissenstransfer", "Lehraufträge, Seminare und praxisnahe Vermittlung komplexer wirtschaftlicher Inhalte.")]
    else:
        t = dict(title="References – Stolz Consulting | Mag. Dr. Sabine Stolz, MSc",
                 desc="Areas of focus, experience and a selection of past collaborations of Stolz Consulting.",
                 eyebrow="References", h1="Focus areas and <em>experience</em>",
                 lead="Many years of national and international experience in business, financial and IT-related matters.",
                 label="Experience", e2="Companies and institutions", h2="A selection of past collaborations", more="and many more")
        items = [("Controlling and financial management", "Support with planning, management, reporting and economic development."),
                 ("Internationalisation and growth support", "Support with international challenges, expansion and organisational development."),
                 ("ERP-related process and IT consulting", "Combining business requirements with user-friendly and practical IT solutions."),
                 ("Training, lectures and knowledge transfer", "Teaching assignments, seminars and practical communication of complex business content.")]
    cards = "".join(f'<li class="reveal"><span class="label">{t["label"]}</span><h3>{escape(h)}</h3><p>{escape(p)}</p></li>' for h, p in items)
    refs = REFERENCES + [(t["more"], None)]
    return dict(title=t["title"], desc=t["desc"], body=f"""
    <section class="page-hero">
      <div class="container reveal">
        <p class="eyebrow">{t['eyebrow']}</p>
        <h1 class="h1">{t['h1']}</h1>
        <p class="lead">{t['lead']}</p>
      </div>
    </section>

    <section class="section section--soft">
      <div class="container">
        <ul class="expertise">{cards}</ul>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head reveal">
          <p class="eyebrow">{t['e2']}</p>
          <h2 class="h2">{t['h2']}</h2>
        </div>
        {logo_grid(k, lang, refs, names=True)}
      </div>
    </section>
{cta_block(k, lang)}""")


def page_kontakt(lang):
    k = "kontakt"
    de = lang == "de"
    action = asset(k, lang, "../contact.php").replace("assets/../", "")
    privacy = rel(k, lang, "datenschutz")
    if de:
        t = dict(title="Kontakt – Stolz Consulting | Mag. Dr. Sabine Stolz, MSc",
                 desc="Kontakt zu Stolz Consulting, Mag. Dr. Sabine Stolz, MSc – Brünngraben 10, 8444 St. Andrä-Höch.",
                 eyebrow="Kontakt", h1="Kontaktieren Sie <em>mich</em>",
                 lead="Sie interessieren sich für meine Leistungen? Schreiben Sie mir gerne über das Formular oder nutzen Sie die direkten Kontaktdaten.",
                 name="Name", company="Unternehmen", email="E-Mail-Adresse", phone="Telefon", msg="Nachricht",
                 opt="(optional)", send="Nachricht senden",
                 consent=f'Ich habe die <a href="{privacy}">Datenschutzerklärung</a> gelesen und bin einverstanden, dass meine Angaben zur Bearbeitung meiner Anfrage verwendet werden.',
                 subject="Anfrage über stolz-consulting.net",
                 ok="Vielen Dank für Ihre Nachricht. Ich melde mich in Kürze bei Ihnen.",
                 err="Die Nachricht konnte leider nicht gesendet werden. Bitte schreiben Sie direkt an office@stolz-consulting.net.",
                 mailto="Ihr E-Mail-Programm wurde mit Ihrer Nachricht geöffnet. Bitte senden Sie die E-Mail dort ab.",
                 info="Kontaktinformationen", role="Unternehmensberatung")
    else:
        t = dict(title="Contact – Stolz Consulting | Mag. Dr. Sabine Stolz, MSc",
                 desc="Contact Stolz Consulting, Mag. Dr. Sabine Stolz, MSc – Brünngraben 10, 8444 St. Andrä-Höch, Austria.",
                 eyebrow="Contact", h1="Get in <em>touch</em>",
                 lead="Interested in my services? Feel free to write to me using the form or use the direct contact details.",
                 name="Name", company="Company", email="Email address", phone="Phone", msg="Message",
                 opt="(optional)", send="Send message",
                 consent=f'I have read the <a href="{privacy}">privacy policy</a> and agree that my details will be used to process my enquiry.',
                 subject="Enquiry via stolz-consulting.net",
                 ok="Thank you for your message. I will get back to you shortly.",
                 err="Unfortunately, your message could not be sent. Please write directly to office@stolz-consulting.net.",
                 mailto="Your email program has been opened with your message. Please send the email from there.",
                 info="Contact information", role="Management consulting")
    c = CONTACT
    return dict(title=t["title"], desc=t["desc"], body=f"""
    <section class="page-hero">
      <div class="container reveal">
        <p class="eyebrow">{t['eyebrow']}</p>
        <h1 class="h1">{t['h1']}</h1>
        <p class="lead">{t['lead']}</p>
      </div>
    </section>

    <section class="section">
      <div class="container contact-grid">
        <form class="form reveal" action="{action}" method="post" novalidate data-contact-form
              data-mailto="{c['email']}" data-subject="{t['subject']}"
              data-msg-ok="{t['ok']}" data-msg-error="{t['err']}" data-msg-mailto="{t['mailto']}">
          <input type="hidden" name="lang" value="{lang}">
          <div class="form__row">
            <div class="field">
              <label for="f-name">{t['name']}</label>
              <input id="f-name" name="name" type="text" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="f-company">{t['company']} <span class="opt">{t['opt']}</span></label>
              <input id="f-company" name="company" type="text" autocomplete="organization">
            </div>
          </div>
          <div class="form__row">
            <div class="field">
              <label for="f-email">{t['email']}</label>
              <input id="f-email" name="email" type="email" autocomplete="email" required>
            </div>
            <div class="field">
              <label for="f-phone">{t['phone']} <span class="opt">{t['opt']}</span></label>
              <input id="f-phone" name="phone" type="tel" autocomplete="tel">
            </div>
          </div>
          <div class="field">
            <label for="f-message">{t['msg']}</label>
            <textarea id="f-message" name="message" rows="6" required></textarea>
          </div>
          <div class="hp" aria-hidden="true">
            <label for="f-website">Website</label>
            <input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off">
          </div>
          <label class="check">
            <input type="checkbox" name="consent" value="1" required>
            <span>{t['consent']}</span>
          </label>
          <button class="btn btn--primary" type="submit">{t['send']} {ARROW}</button>
          <p class="form__status" role="status" aria-live="polite"></p>
        </form>

        <aside class="contact-info reveal" aria-label="{t['info']}">
          <p class="name">Stolz Consulting</p>
          <p class="role">Mag. Dr. Sabine Stolz, MSc · {t['role']}</p>
          <ul>
            <li>{ICON_PHONE}<div><span class="k">{T[lang]['phone']}</span><a href="{c['phone_href']}">{c['phone_display'][lang]}</a></div></li>
            <li>{ICON_MAIL}<div><span class="k">{T[lang]['email']}</span><a href="mailto:{c['email']}">{c['email']}</a></div></li>
            <li>{ICON_PIN}<div><span class="k">{T[lang]['address']}</span><address>{c['street']}<br>{c['city']}<br>{c['country'][lang]}</address></div></li>
          </ul>
        </aside>
      </div>
    </section>""")


def page_impressum(lang):
    c = CONTACT
    if lang == "de":
        return dict(title="Impressum – Stolz Consulting", desc="Impressum von Stolz Consulting, Mag. Dr. Sabine Stolz, MSc.", body=f"""
    <section class="page-hero">
      <div class="container container--narrow">
        <p class="eyebrow">Rechtliches</p>
        <h1 class="h1">Impressum</h1>
      </div>
    </section>
    <section class="section">
      <div class="container container--narrow legal">
        <h2>Angaben gemäß österreichischen Informationspflichten</h2>
        <address>Stolz Consulting<br>Mag. Dr. Sabine Stolz, MSc<br>Unternehmensberatung<br>{c['street']}<br>{c['city']}</address>
        <dl>
          <dt>Telefon:</dt><dd><a href="{c['phone_href']}">{c['phone_display']['de']}</a></dd>
          <dt>E-Mail:</dt><dd><a href="mailto:{c['email']}">{c['email']}</a></dd>
          <dt>Website:</dt><dd><a href="{DOMAIN}/">{DOMAIN}/</a></dd>
        </dl>
        <h2>Haftung für Inhalte</h2>
        <p>Die Inhalte dieser Website werden mit größtmöglicher Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte wird jedoch keine Gewähr übernommen.</p>
        <h2>Haftung für Links</h2>
        <p>Diese Website kann Links zu externen Websites enthalten. Für deren Inhalte ist ausschließlich der jeweilige Anbieter verantwortlich. Zum Zeitpunkt der Verlinkung waren keine Rechtsverstöße erkennbar.</p>
        <h2>Urheberrecht</h2>
        <p>Die auf dieser Website veröffentlichten Inhalte und Werke unterliegen dem Urheberrecht. Jede Art der Verwertung außerhalb der Grenzen des Urheberrechts bedarf der vorherigen schriftlichen Zustimmung der jeweiligen Rechteinhaberin oder des jeweiligen Rechteinhabers.</p>
      </div>
    </section>""")
    return dict(title="Imprint – Stolz Consulting", desc="Imprint of Stolz Consulting, Mag. Dr. Sabine Stolz, MSc.", body=f"""
    <section class="page-hero">
      <div class="container container--narrow">
        <p class="eyebrow">Legal</p>
        <h1 class="h1">Imprint</h1>
      </div>
    </section>
    <section class="section">
      <div class="container container--narrow legal">
        <h2>Information pursuant to Austrian disclosure requirements</h2>
        <address>Stolz Consulting<br>Mag. Dr. Sabine Stolz, MSc<br>Management consulting<br>{c['street']}<br>{c['city']}<br>{c['country']['en']}</address>
        <dl>
          <dt>Phone:</dt><dd><a href="{c['phone_href']}">{c['phone_display']['en']}</a></dd>
          <dt>Email:</dt><dd><a href="mailto:{c['email']}">{c['email']}</a></dd>
          <dt>Website:</dt><dd><a href="{DOMAIN}/">{DOMAIN}/</a></dd>
        </dl>
        <h2>Liability for content</h2>
        <p>The content of this website has been created with the greatest possible care. However, no guarantee is given for the accuracy, completeness or timeliness of the content.</p>
        <h2>Liability for links</h2>
        <p>This website may contain links to external websites. The respective provider is solely responsible for their content. No legal violations were apparent at the time of linking.</p>
        <h2>Copyright</h2>
        <p>The content and works published on this website are subject to copyright. Any use beyond the limits of copyright law requires the prior written consent of the respective rights holder.</p>
      </div>
    </section>""")


def page_datenschutz(lang):
    c = CONTACT
    if lang == "de":
        return dict(title="Datenschutz – Stolz Consulting", desc="Datenschutzerklärung von Stolz Consulting.", body=f"""
    <section class="page-hero">
      <div class="container container--narrow">
        <p class="eyebrow">Rechtliches</p>
        <h1 class="h1">Datenschutz</h1>
      </div>
    </section>
    <section class="section">
      <div class="container container--narrow legal">
        <h2>Verantwortliche Stelle</h2>
        <address>Stolz Consulting<br>Mag. Dr. Sabine Stolz, MSc<br>{c['street']}<br>{c['city']}</address>
        <dl>
          <dt>E-Mail:</dt><dd><a href="mailto:{c['email']}">{c['email']}</a></dd>
          <dt>Telefon:</dt><dd><a href="{c['phone_href']}">{c['phone_display']['de']}</a></dd>
        </dl>
        <h2>Allgemeines zur Datenverarbeitung</h2>
        <p>Der Schutz Ihrer persönlichen Daten ist uns ein besonderes Anliegen. Wir verarbeiten Ihre Daten ausschließlich auf Grundlage der gesetzlichen Bestimmungen, insbesondere der DSGVO und der einschlägigen österreichischen Vorschriften.</p>
        <h2>Kontaktaufnahme</h2>
        <p>Wenn Sie per Formular auf der Website oder per E-Mail Kontakt aufnehmen, werden die von Ihnen angegebenen Daten zur Bearbeitung der Anfrage und für den Fall von Anschlussfragen verarbeitet.</p>
        <p>Rechtsgrundlage ist in der Regel die Durchführung vorvertraglicher Maßnahmen oder unser berechtigtes Interesse an einer effizienten Kommunikation.</p>
        <h2>Server-Logfiles</h2>
        <p>Beim Besuch dieser Website können aus technischen Gründen Verbindungsdaten wie IP-Adresse, Zeitpunkt des Zugriffs, aufgerufene Seite und Browserinformationen verarbeitet werden. Diese Verarbeitung dient der technischen Sicherheit und dem stabilen Betrieb der Website.</p>
        <h2>Speicherdauer</h2>
        <p>Personenbezogene Daten werden nur so lange gespeichert, wie dies für die jeweiligen Zwecke erforderlich ist oder gesetzliche Aufbewahrungspflichten bestehen.</p>
        <h2>Ihre Rechte</h2>
        <p>Ihnen stehen grundsätzlich die Rechte auf Auskunft, Berichtigung, Löschung, Einschränkung, Datenübertragbarkeit, Widerruf und Widerspruch zu. Wenn Sie der Ansicht sind, dass die Verarbeitung Ihrer Daten gegen das Datenschutzrecht verstößt, können Sie sich bei der zuständigen Datenschutzbehörde beschweren.</p>
      </div>
    </section>""")
    return dict(title="Privacy policy – Stolz Consulting", desc="Privacy policy of Stolz Consulting.", body=f"""
    <section class="page-hero">
      <div class="container container--narrow">
        <p class="eyebrow">Legal</p>
        <h1 class="h1">Privacy policy</h1>
      </div>
    </section>
    <section class="section">
      <div class="container container--narrow legal">
        <h2>Controller</h2>
        <address>Stolz Consulting<br>Mag. Dr. Sabine Stolz, MSc<br>{c['street']}<br>{c['city']}<br>{c['country']['en']}</address>
        <dl>
          <dt>Email:</dt><dd><a href="mailto:{c['email']}">{c['email']}</a></dd>
          <dt>Phone:</dt><dd><a href="{c['phone_href']}">{c['phone_display']['en']}</a></dd>
        </dl>
        <h2>General information on data processing</h2>
        <p>The protection of your personal data is of particular concern to us. We process your data exclusively on the basis of the statutory provisions, in particular the GDPR and the relevant Austrian regulations.</p>
        <h2>Contacting us</h2>
        <p>If you contact us via the form on the website or by email, the data you provide will be processed in order to handle your enquiry and in case of follow-up questions.</p>
        <p>The legal basis is generally the performance of pre-contractual measures or our legitimate interest in efficient communication.</p>
        <h2>Server log files</h2>
        <p>When you visit this website, connection data such as your IP address, time of access, page visited and browser information may be processed for technical reasons. This processing serves the technical security and stable operation of the website.</p>
        <h2>Storage period</h2>
        <p>Personal data is only stored for as long as is necessary for the respective purposes or as required by statutory retention obligations.</p>
        <h2>Your rights</h2>
        <p>In principle, you have the right to information, rectification, erasure, restriction, data portability, revocation and objection. If you believe that the processing of your data violates data protection law, you can lodge a complaint with the competent data protection authority.</p>
      </div>
    </section>""")


PAGES = {
    "home": page_home, "profil": page_profil, "referenzen": page_referenzen,
    "kontakt": page_kontakt, "impressum": page_impressum, "datenschutz": page_datenschutz,
}


# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------
def layout(key, lang, p):
    t = T[lang]
    other = "en" if lang == "de" else "de"
    url_de = DOMAIN + "/" + PATHS[key][0]
    url_en = DOMAIN + "/" + PATHS[key][1]
    canonical = url_de if lang == "de" else url_en
    a = lambda path: asset(key, lang, path)
    L = lambda to, lg=None: rel(key, lang, to, lg)

    current = ' aria-current="page"'
    nav = "".join(
        f'<li><a class="nav__link" href="{L(k)}"{current if k == key else ""}>{label}</a></li>'
        for k, label in t["nav"])
    if lang == "de":
        lang_sw = f'<span aria-current="true" lang="de">DE</span><a href="{L(key, "en")}" lang="en" hreflang="en">EN</a>'
    else:
        lang_sw = f'<a href="{L(key, "de")}" lang="de" hreflang="de">DE</a><span aria-current="true" lang="en">EN</span>'
    c = CONTACT

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{p['title']}</title>
  <meta name="description" content="{escape(p['desc'])}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="de" href="{url_de}">
  <link rel="alternate" hreflang="en" href="{url_en}">
  <link rel="alternate" hreflang="x-default" href="{url_de}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{t['og_locale']}">
  <meta property="og:title" content="{p['title']}">
  <meta property="og:description" content="{escape(p['desc'])}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{DOMAIN}/assets/img/og-image.jpg">
  <meta name="theme-color" content="#221b11">
  <link rel="icon" type="image/svg+xml" href="{a('img/favicon.svg')}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;1,8..60,400&display=swap">
  <link rel="stylesheet" href="{a('css/style.css')}">
</head>
<body>
  <a class="skip-link" href="#main">{t['skip']}</a>

  <header class="site-header">
    <div class="container">
      <a class="brand" href="{L('home')}" aria-label="{t['home_label']}">
        <span class="brand__name">Stolz Consulting</span>
        <span class="brand__sub">{t['brand_sub']}</span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="{t['menu']}"><span></span></button>
      <nav class="nav" id="nav" aria-label="{t['nav_label']}">
        <ul class="nav__list">{nav}</ul>
        <div class="lang" aria-label="{t['lang_label']}">{lang_sw}</div>
      </nav>
    </div>
  </header>

  <main id="main">{p['body']}
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="site-footer__top">
        <div>
          <p class="kicker">{t['footer_kicker']}</p>
          <p class="h2">{t['footer_claim']}</p>
        </div>
        <div class="site-footer__contact">
          <div><span class="k">{t['phone']}</span><a href="{c['phone_href']}">{c['phone_display'][lang]}</a></div>
          <div><span class="k">{t['email']}</span><a href="mailto:{c['email']}">{c['email']}</a></div>
          <div><span class="k">{t['address']}</span><address>{c['street']}<br>{c['city']}</address></div>
        </div>
      </div>
      <div class="site-footer__bottom">
        <span>© <span data-year>2026</span> Stolz Consulting · Mag. Dr. Sabine Stolz, MSc</span>
        <nav class="site-footer__links" aria-label="Footer">
          <a href="{L('impressum')}">{t['imprint']}</a>
          <a href="{L('datenschutz')}">{t['privacy']}</a>
          <a href="{L(key, other)}" lang="{other}" hreflang="{other}">{t['other_lang']}</a>
        </nav>
      </div>
    </div>
  </footer>

  <script src="{a('js/main.js')}" defer></script>
</body>
</html>
"""


def main():
    for key, fn in PAGES.items():
        for i, lang in enumerate(LANGS):
            out = ROOT / PATHS[key][i] / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(layout(key, lang, fn(lang)), encoding="utf-8")
            print("geschrieben:", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
