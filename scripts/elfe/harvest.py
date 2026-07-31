"""Harvest every (choix_1, choix_2, choix_3) combination of the ELFE dataviz as xlsx."""
import json
import os
import re
import time

import websocket

from shiny_client import Elfe, HOST, PATH

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "elfe_raw")
os.makedirs(OUT, exist_ok=True)

CLIENT_GRAPH = {
    ".clientdata_output_graphique_width": 1200,
    ".clientdata_output_graphique_height": 600,
    ".clientdata_output_graphique_hidden": False,
    ".clientdata_output_graphique_bg": "white",
    ".clientdata_output_graphique_fg": "black",
}

CHOIX_1 = ["Carbone", "Energie"]
CHOIX_2 = ["Régime fiscal", "Secteur économique", "Agents", "Type de produit",
           "Instruments", "Gaz à effet de serre"]
CHOIX_3 = ["2024*", "2023", "2022", "2021", "2020", "2019", "2018", "2017",
           "2016", "2015", "2014"]


def slug(s):
    s = (s.replace("é", "e").replace("è", "e").replace("à", "a").replace("*", "star")
          .replace("É", "E"))
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").lower()


def new_session():
    e = Elfe(verbose=False)
    e.ws.send(json.dumps({"method": "update", "data": dict(CLIENT_GRAPH)}))
    e.drain(3)
    e.set_inputs(navbar="Datavisualisation")
    return e


def wait_for_graph(e, max_s=45):
    """Read frames until a fresh `graphique` value lands (or timeout)."""
    t0 = time.time()
    while time.time() - t0 < max_s:
        try:
            m = e.ws.recv()
        except websocket.WebSocketTimeoutException:
            continue
        except Exception:
            return False
        if not m:
            continue
        try:
            d = json.loads(m)
        except Exception:
            continue
        if isinstance(d, dict) and d.get("values"):
            e.values.update(d["values"])
            if "graphique" in d["values"]:
                return True
            if d["values"].get("downloadData"):
                return True
    return False


def main():
    combos = [(a, b, c) for a in CHOIX_1 for b in CHOIX_2 for c in CHOIX_3]
    manifest = []
    e = new_session()
    done = fail = 0
    for i, (c1, c2, c3) in enumerate(combos, 1):
        name = f"{slug(c1)}__{slug(c2)}__{slug(c3)}.xlsx"
        path = os.path.join(OUT, name)
        if os.path.exists(path) and os.path.getsize(path) > 2000:
            done += 1
            continue
        for attempt in (1, 2):
            try:
                e.ws.send(json.dumps({"method": "update", "data": {
                    "choix_1": c1, "choix_2": c2, "choix_3": c3}}))
                wait_for_graph(e)
                url = e.values.get("downloadData")
                full = f"https://{HOST}{PATH}/_w_{e.worker}/{url}"
                r = e.s.get(full, timeout=180)
                if r.status_code == 200 and len(r.content) > 2000:
                    open(path, "wb").write(r.content)
                    manifest.append({"choix_1": c1, "choix_2": c2, "choix_3": c3,
                                     "fichier": name, "octets": len(r.content)})
                    done += 1
                    print(f"[{i}/{len(combos)}] OK   {name} ({len(r.content)} o)", flush=True)
                    break
                raise RuntimeError(f"HTTP {r.status_code} len={len(r.content)}")
            except Exception as ex:
                print(f"[{i}/{len(combos)}] retry {attempt} {name}: {ex}", flush=True)
                try:
                    e.ws.close()
                except Exception:
                    pass
                time.sleep(2)
                e = new_session()
        else:
            fail += 1
            print(f"[{i}/{len(combos)}] FAIL {name}", flush=True)

    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print(f"\nterminé : {done} ok, {fail} échecs, {len(combos)} combinaisons")


if __name__ == "__main__":
    main()
