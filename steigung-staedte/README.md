# Steigungsatlas deutscher Großstädte

Welche deutschen Großstädte (> 100.000 EW) haben pro Straßenkilometer die meiste bzw. steilste Steigung?
Pipeline in Python, Ergebnis als CSV/JSON plus eine selbstenthaltene interaktive Seite (`index.html`).

## Ausführen

```bash
cd steigung-staedte
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python run_analysis.py --test      # Testlauf: Wuppertal, Münster, Stuttgart
python run_analysis.py             # alle 85 Städte (~15 min mit 4 Workern, Downloads gecacht)
# dann index.html im Browser öffnen (läuft offline, alle Bibliotheken und Schriften sind eingebettet)
```

Weitere Optionen: `--cities Essen Aachen`, `--workers 4`, `--skip-analysis` (nur Auswertung + HTML aus dem Cache).
Downloads (Overture-Segmente, DEM-Kacheln) und berechnete Netze landen in `cache/` (nicht versioniert, ca. 3 GB).

## Ergebnisse

| Datei | Inhalt |
|---|---|
| `data/staedte.csv` | Städteliste inkl. Einwohner (OSM), Grenztyp, Fläche, Status Großstadt/Grenzfall |
| `results/staedte_kennzahlen.csv` | alle Kennzahlen je Stadt (drive + bike, Copernicus + SRTM), Histogramm-km je Klasse |
| `results/top_staedte.json` | Top 3, flachste Stadt, beide Rankings, Methodik, bekannte Grenzen |
| `results/validierung.json` | Stichprobe bekannter Straßen mit Höhenprofil |
| `index.html` | interaktive Visualisierung (3,4 MB, offline) |

### Top 10 nach Höhenmetern pro Straßenkilometer (Netz „drive“, Copernicus GLO-30)

| # | Stadt | Hm/km | Ø Steigung | Median | P90 | > 6 % | > 10 % | > 15 % | Rang > 6 % | Hm/km SRTM (Rang) |
|--:|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | Wuppertal | 20,8 | 4,2 % | 3,2 % | 9,0 % | 25,2 % | 7,6 % | 1,6 % | 1 | 19,1 (3) |
| 2 | Remscheid | 20,7 | 4,1 % | 3,2 % | 9,0 % | 23,9 % | 7,5 % | 1,5 % | 2 | 19,4 (2) |
| 3 | Siegen ° | 20,1 | 4,0 % | 2,7 % | 9,5 % | 23,6 % | 9,0 % | 2,3 % | 3 | 19,6 (1) |
| 4 | Hagen | 18,8 | 3,8 % | 2,6 % | 8,8 % | 20,6 % | 7,2 % | 1,9 % | 4 | 17,8 (4) |
| 5 | Solingen | 17,8 | 3,6 % | 2,8 % | 7,5 % | 18,1 % | 3,7 % | 0,7 % | 5 | 16,7 (6) |
| 6 | Pforzheim | 17,3 | 3,5 % | 2,4 % | 7,7 % | 17,4 % | 4,8 % | 1,3 % | 6 | 17,2 (5) |
| 7 | Würzburg | 16,9 | 3,4 % | 2,2 % | 7,8 % | 17,0 % | 5,6 % | 1,6 % | 8 | 15,9 (8) |
| 8 | Jena | 16,8 | 3,4 % | 2,2 % | 8,4 % | 17,1 % | 5,7 % | 1,3 % | 7 | 15,9 (7) |
| 9 | Bergisch Gladbach | 15,9 | 3,2 % | 2,4 % | 7,0 % | 14,3 % | 3,5 % | 0,9 % | 10 | 14,0 (12) |
| 10 | Stuttgart | 15,5 | 3,1 % | 2,1 % | 7,0 % | 14,2 % | 3,8 % | 0,8 % | 11 | 15,2 (10) |

° Siegen liegt laut OSM bei 99.403 EW und ist als Grenzfall markiert. Für die Top 3 der Visualisierung zählen nur
Städte ≥ 100.000 EW, deshalb rückt Hagen auf Platz 3.

Flachste Großstadt: **Moers** (5,0 Hm/km), knapp vor Hamm (5,1) und Krefeld (5,2).

### Was die Daten sagen

- **Bergisches Land vorne.** Wuppertal, Remscheid, (Siegen), Hagen, Solingen. Wuppertal und Remscheid trennen 0,2 Hm/km,
  das ist weniger als die Messunsicherheit. Mit SRTM lautet die Reihenfolge Siegen, Remscheid, Wuppertal. Robust ist die Gruppe, nicht der Platz.
- **Stuttgart nur auf Platz 10.** Die steilen Hanglagen sind da, aber Neckartal, Filder und Talkessel-Boden haben viel flaches Netz,
  das den Schnitt drückt. Pro Straßenkilometer gemessen ist Stuttgart hügelig, nicht extrem.
- **Die erwarteten flachen Städte sind nicht die flachsten.** Berlin (Rang 42, 8,9 Hm/km), Hamburg (53), Bremen (68), Münster (73),
  Leipzig (74) liegen deutlich über Moers/Hamm/Krefeld. Ein Teil ist echte Topografie (Moränenkanten, Elbhang), ein großer Teil ist
  Rauschen des Oberflächenmodells (Gebäude, Bäume, viele Brücken). Mit SRTM sinken Berlin auf 7,5 und Hamburg auf 6,9.
  Unterhalb von ca. 7–8 Hm/km sind Rangunterschiede kaum aussagekräftig.
- **Ranking nach Anteil > 6 % ist fast identisch** (Spearman ρ = 0,98). Größere Verschiebungen: Heidelberg (21 → 12) und Karlsruhe
  (49 → 37) haben wenige, aber steile Hanglagen am Stadtrand; Osnabrück (38 → 51), Recklinghausen, Wolfsburg haben flächig sanfte Wellen ohne steile Abschnitte.
- **Copernicus vs. SRTM**: Spearman ρ = 0,97 über alle Städte. Copernicus liegt fast überall leicht höher (mehr Oberflächenrauschen).
- **Radnetz („bike“)** ist überall steiler als das Autonetz (Wuppertal 25,4 Hm/km), weil Wald- und Feldwege an Hängen dazukommen.

## Methodik

1. **Straßen**: Overture Maps Transportation (Release 2026-09-23.1), aus OpenStreetMap abgeleitet, per Bounding Box aus GeoParquet
   auf S3 gelesen. *Abweichung vom Plan:* Overpass/Nominatim (und damit `osmnx.graph_from_polygon`/`geocode_to_gdf`) waren in der
   Ausführungsumgebung blockiert. Die Netzlogik ist OSMnx nachgebaut: Filter „drive“ (motorway … residential, living_street,
   unclassified, service ohne parking_aisle/driveway, ohne access=private/no) und „bike“ (ohne motorway, footway, steps, bridleway).
2. **Grenzen**: Overture Divisions (OSM-Verwaltungsgrenzen). Kreisfreie Städte = county, kreisangehörige = locality, Berlin/Hamburg = region.
3. **Städteliste**: Overture Divisions, `locality` mit `class=city` und OSM-Tag `population ≥ 100.000` (79 Städte).
   Wikipedia/Destatis waren ebenfalls nicht erreichbar. 6 Orte mit 97.000–99.999 EW laut OSM sind als „Grenzfall“ mitgerechnet.
4. **Höhe**: Copernicus DEM GLO-30 (Kacheln von AWS Open Data, gecacht), bilinear direkt in der Originalkachel interpoliert.
   Gegenprüfung mit SRTM 1″ (AWS Terrain Tiles, Skadi) für alle Städte.
5. **Netz**: Segmente an Connectoren (OSM-Knoten) geteilt, ungerichteter Graph, Knoten mit Grad 2 entfernt (wie `osmnx.simplify_graph`).
   Jede Straße zählt einmal, unabhängig von Fahrtrichtungen.
6. **Brücken/Tunnel**: Knoten, die nur an Brücken-/Tunnelkanten hängen, bekommen eine entlang des Netzes linear zwischen den
   Bauwerksenden interpolierte Höhe statt des DEM-Werts.
7. **Kanten < 10 m** werden kontrahiert (Endknoten verschmolzen, Höhe gemittelt).
8. **Steigung** je Kante = |Δh| / Länge. Kanten > 40 % werden markiert, gezählt (`ausreisser_n`, `ausreisser_km`) und aus den
   Kennzahlen ausgenommen; `hm_pro_km_inkl_ausreisser` zeigt den Wert mit ihnen. Alle Kennzahlen längengewichtet.
9. **Hm/km** = Σ positiver Höhenmeter, über beide Fahrtrichtungen gemittelt (= Σ|Δh|/2), geteilt durch Straßen-km.
10. **Steilste Strecke**: zusammenhängende Kantenfolge gleichen Namens, 100–800 m, maximale Netto-Steigung. Konservativ bewertet:
    Minimum aus Copernicus und SRTM, beide müssen in dieselbe Richtung steigen. Brücken, Tunnel und Ausreißer sind ausgeschlossen.

### Was gemessen und was geschätzt ist

- **Gemessen** (aus den Daten berechnet): alle Kennzahlen, Rankings, Histogramme, Profile, Straßen-km.
- **Abgeleitet/geschätzt**: Höhen auf Brücken/in Tunneln (linear interpoliert), Höhen verschmolzener Knoten (Mittelwert),
  Einwohnerzahlen (OSM-Tag, gemischte Stichtage, nicht Destatis).
- **Referenzwerte der Stichprobe** stammen aus Online-Quellen (komoot, climbfinder), nicht aus eigener Vermessung.

### Stichprobe (Qualitätssicherung)

| Straße | Referenz | DEM Copernicus | DEM SRTM | Urteil |
|---|---|---|---|---|
| Hauptstraße, Aachen-Burtscheid (333 m) | Ø 9 %, steilster Abschnitt 13,3 % | Ø 9,7 %, max. 14,2 % (100 m) | Ø 7,3 %, max. 13,3 % | passt |
| Stotznocken, Essen-Werden (101 m) | ca. 30 % Spitze | Ø 17,2 %, max. 27,0 % (50 m) | Ø 17,0 %, max. 25,3 % | Spitze plausibel, aber Straße ist nur gut 3 Pixel lang |
| Neue Weinsteige, Stuttgart (1,3-km-Teilstück) | Talkessel → Degerloch (≈ 470 m) | 294 → 360 m, Ø 5,1 % | 292 → 361 m, Ø 5,3 % | Δh plausibel, kein Prozent-Referenzwert gefunden |

### Bekannte Grenzen

- **Hm/km und mittlere Steigung sind dasselbe Maß.** Bei knotenbasierter Methode gilt Hm/km = 5 × mittlere Steigung (%).
  Das Primärranking ist damit identisch mit dem Ranking nach mittlerer Steigung; ein unabhängiges zweites Maß ist nur „Anteil > 6 %“.
- **Copernicus GLO-30 ist ein Oberflächenmodell (DSM)**, kein Geländemodell. Gebäude, Bäume und Brückendecks fließen ein. Das
  erzeugt in flachen Städten ein Grundrauschen von ca. 5 Hm/km (≈ 1 % mittlere Steigung). Ein echtes Geländemodell (DGM1 der
  Länder) wäre genauer, ist aber nicht bundesweit einheitlich frei verfügbar und war hier nicht erreichbar.
- **30-m-Raster**: Rampen ab ca. 100 m werden gut getroffen. Kürzere Abschnitte schwanken um mehrere Prozentpunkte, Rampen unter 30 m sind unsichtbar.
- **Nur Knotenhöhen**: Kuppen und Senken zwischen zwei Kreuzungen fehlen; lange Kanten werden unterschätzt.
- **Unter Brücken**: Straßen, die unter einer Brücke durchführen, können im DSM die Deckhöhe bekommen (nicht korrigiert).
- **Stadtzuschnitt**: Verwaltungsgrenze. Eingemeindete ländliche Ortsteile oder flache Talböden verändern das Ergebnis.

## Datenquellen und Lizenzen

- Straßen und Grenzen: © OpenStreetMap-Mitwirkende (ODbL), bereitgestellt über [Overture Maps](https://overturemaps.org)
- Copernicus DEM GLO-30 © DLR e.V. 2010–2014 und © Airbus Defence and Space GmbH 2014–2018, bereitgestellt unter COPERNICUS durch die EU und ESA
- SRTM (NASA/USGS) über AWS Terrain Tiles
- Eingebettet in `index.html`: three.js (MIT), d3 (ISC), Chakra Petch und JetBrains Mono (SIL OFL)

## Aufbau

```
run_analysis.py          Einstieg: Städteliste -> Netze -> Kennzahlen -> Report -> Validierung -> HTML
steigung/overture.py     Overture-Zugriff (S3, BBox-Filter, Cache)
steigung/cities.py       Großstädte + Verwaltungsgrenzen
steigung/dem.py          DEM-Kacheln laden, cachen, bilinear samplen
steigung/network.py      Netzfilter, Teilen an Connectoren, Brücken/Tunnel, Vereinfachung, Kontraktion
steigung/metrics.py      längengewichtete Kennzahlen, Histogramm, steilste Strecke
steigung/report.py       CSV/JSON inkl. Methodik und Grenzen
steigung/validate.py     Stichprobe bekannter Straßen
steigung/viz_export.py   Datenaufbereitung + Einbetten in index.html
web/template.html        Seite (HTML/CSS/JS), web/vendor/ eingebettete Bibliotheken und Schriften
```
