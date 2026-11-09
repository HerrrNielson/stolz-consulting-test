# Stolz Consulting – Website

Statische Neuauflage von [stolz-consulting.net](https://www.stolz-consulting.net/)
(Mag. Dr. Sabine Stolz, MSc) – zweisprachig: Deutsch unter `/`, Englisch unter `/en/`.

Inhalte, Farben und Bilder stammen von der bestehenden Website. Die englischen Texte
sind Übersetzungen der deutschen Originaltexte.

## Seiten

| Deutsch | Englisch |
|---|---|
| `/` | `/en/` |
| `/profil/` | `/en/profile/` |
| `/referenzen/` | `/en/references/` |
| `/kontakt/` | `/en/contact/` |
| `/impressum/` | `/en/imprint/` |
| `/datenschutz/` | `/en/privacy/` |

## Struktur

```
build.py              Seitengenerator – alle Texte (DE + EN) stehen hier
contact.php           Handler für das Kontaktformular (versendet per PHP mail())
assets/css/style.css  Stylesheet
assets/js/main.js     Menü, Einblendungen, Formular-Versand
assets/img/           Optimierte Bilder; original/ = unveränderte Downloads
index.html, */        Generierte Seiten (nicht direkt bearbeiten)
```

## Texte ändern

Texte in `build.py` anpassen, dann alle Seiten neu erzeugen:

```bash
python build.py
```

## Lokal ansehen

```bash
python -m http.server 8080
```

Dann <http://localhost:8080> öffnen.

## Kontaktformular

Das Formular sendet an `contact.php`, das die Anfrage an `office@stolz-consulting.net`
weiterleitet. Voraussetzung ist ein Webspace mit PHP und funktionierendem Mailversand.
Ist kein PHP verfügbar (z. B. bei rein statischem Hosting), öffnet sich als Fallback
das E-Mail-Programm des Besuchers mit der vorausgefüllten Nachricht.

Noch offen: Mailversand auf dem Zielserver testen.

## Design

- Farben aus dem Original-Theme: Creme `#f5f1ea`, Gold `#b88b4a` / `#8f6934`,
  Dunkelbraun `#221b11`
- Schriften (Google Fonts): Source Serif 4 für Überschriften, Inter für Fließtext
