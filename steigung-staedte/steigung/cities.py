"""Liste der deutschen Großstädte (>100k EW) + österreichische Landeshauptstädte, inkl. Verwaltungsgrenze."""
from __future__ import annotations

import logging

import geopandas as gpd
import pandas as pd

from . import config
from .overture import fetch_city_candidates, fetch_named_divisions

log = logging.getLogger(__name__)

SUBTYPE_PRIO = {"county": 0, "locality": 1, "region": 2}


# Österreich: die neun Landeshauptstädte (Wien ist zugleich Bundeshauptstadt)
AT_CAPITALS = {  # Anzeigename -> Wikidata-ID (Ort und Grenze heißen in OSM teils verschieden)
    "Wien": "Q1741", "Graz": "Q13298", "Linz": "Q41329", "Salzburg": "Q34713",
    "Innsbruck": "Q1735", "Klagenfurt": "Q41753", "St. Pölten": "Q82500",
    "Bregenz": "Q1737", "Eisenstadt": "Q126321",
}


def build_city_table() -> gpd.GeoDataFrame:
    de = build_de_table()
    de["land"] = "DE"
    at = build_at_table()
    return pd.concat([de, at], ignore_index=True).pipe(gpd.GeoDataFrame, crs=4326)


def build_at_table() -> gpd.GeoDataFrame:
    names = ["Wien", "Graz", "Linz", "Salzburg", "Innsbruck", "Klagenfurt", "Klagenfurt am Wörthersee",
             "St. Pölten", "Bregenz", "Eisenstadt"]
    div, areas = fetch_named_divisions("AT", names, "at")
    areas = areas[areas["class"] == "land"].copy()
    areas["km2"] = areas.to_crs(config.METRIC_CRS).area / 1e6
    rows = []
    for stadt, qid in AT_CAPITALS.items():
        d = div[div["wikidata"] == qid]
        loc = d[d["subtype"] == "locality"].sort_values("population", ascending=False)
        cand = areas[areas["division_id"].isin(d["id"])].copy()
        if cand.empty or loc.empty:
            log.warning("Keine Grenze/Ort für %s", stadt)
            continue
        cand["prio"] = cand["subtype"].map(SUBTYPE_PRIO)
        best = cand.sort_values(["prio", "km2"], ascending=[True, False]).iloc[0]
        c = loc.iloc[0]
        rows.append(dict(
            stadt=stadt, name_osm=c["name"], bundesland=c["region"],
            einwohner_osm=None if pd.isna(c["population"]) else int(c["population"]),
            einwohner_kreis_osm=None, status="Landeshauptstadt AT", wikidata=qid,
            division_area_id=best["id"], grenze_typ=best["subtype"], flaeche_km2=round(best["km2"], 1),
            geometry=best.geometry, land="AT",
        ))
    return gpd.GeoDataFrame(rows, crs=4326)


def build_de_table() -> gpd.GeoDataFrame:
    div, areas = fetch_city_candidates()
    areas = areas[areas["class"] == "land"].copy()
    areas["km2"] = areas.to_crs(config.METRIC_CRS).area / 1e6

    loc = div[(div["subtype"] == "locality") & (div["class"] == "city")].copy()
    county_pop = div[div["subtype"] == "county"].groupby("wikidata")["population"].max()
    loc["pop_county"] = loc["wikidata"].map(county_pop)
    loc["pop_max"] = loc[["population", "pop_county"]].max(axis=1)
    loc = loc[loc["pop_max"] >= config.BORDERLINE_POP]

    rows = []
    for _, c in loc.iterrows():
        cand = areas[(areas["name"] == c["name"]) & areas.contains(c.geometry)].copy()
        if cand.empty:
            log.warning("Keine Grenze für %s gefunden", c["name"])
            continue
        cand["prio"] = cand["subtype"].map(SUBTYPE_PRIO)
        best = cand.sort_values(["prio", "km2"], ascending=[True, False]).iloc[0]
        if c["population"] >= config.MIN_POP:
            status = "Großstadt"
        else:
            status = "Grenzfall"
        rows.append(dict(
            stadt=c["name"].replace("Cottbus - Chóśebuz", "Cottbus"),
            name_osm=c["name"], bundesland=c["region"], einwohner_osm=int(c["population"]),
            einwohner_kreis_osm=None if pd.isna(c["pop_county"]) else int(c["pop_county"]),
            status=status, wikidata=c["wikidata"], division_area_id=best["id"],
            grenze_typ=best["subtype"], flaeche_km2=round(best["km2"], 1),
            geometry=best.geometry,
        ))
    g = gpd.GeoDataFrame(rows, crs=4326).sort_values("einwohner_osm", ascending=False).reset_index(drop=True)
    return g


def slug(name: str) -> str:
    tr = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue"})
    s = name.translate(tr).lower()
    return "".join(ch if ch.isalnum() else "_" for ch in s).strip("_").replace("__", "_")
