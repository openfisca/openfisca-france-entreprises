"""Consolidate the harvested xlsx into two long CSVs, ready for assets/elfe/."""
import glob
import os
import re

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "elfe_raw")
OUT = os.path.join(HERE, "elfe_consolide")
os.makedirs(OUT, exist_ok=True)

DIMENSIONS = {
    "regime_fiscal": "Régime fiscal",
    "secteur_economique": "Secteur économique",
    "agents": "Agents",
    "type_de_produit": "Type de produit",
    "instruments": "Instruments",
    "gaz_a_effet_de_serre": "Gaz à effet de serre",
}

simple, instruments = [], []

for path in sorted(glob.glob(os.path.join(RAW, "*.xlsx"))):
    base = os.path.basename(path)[:-5]
    perimetre, dim, annee = base.split("__")
    perimetre = perimetre.capitalize()
    annee_txt = annee.replace("star", "*")
    d = pd.read_excel(path)
    cols = list(d.columns)

    tarif_col = cols[0]
    unite_tarif = "euro/tCO2" if "tCO2" in tarif_col else "euro/MWh"

    if dim == "instruments":
        d = d.rename(columns={
            cols[0]: "tarif_effectif",
            cols[1]: "taux_taxation",
            cols[2]: "composante_carbone",
            "Boucliers et aides": "boucliers_et_aides",
            "Prix des quotas ETS": "prix_quotas_ets",
            "Prix réel des quotas ETS": "prix_reel_quotas_ets",
            "Montant remboursement indirect ETS": "remboursement_indirect_ets",
        })
        qcol = [c for c in d.columns if str(c).startswith("Quantit")][0]
        d = d.rename(columns={qcol: "quantite", "Somme_cumulee_quantites": "quantite_cumulee"})
        d.insert(0, "millesime", annee_txt)
        d.insert(0, "perimetre", perimetre)
        d["unite_tarif"] = unite_tarif
        d["unite_quantite"] = "MtCO2" if "MtCO2" in qcol else "TWh"
        instruments.append(d)
        continue

    qcol = [c for c in d.columns if str(c).startswith("Quantit")][0]
    cat_col = [c for c in cols if c not in (tarif_col, qcol, "Somme_cumulee_quantites")][0]
    d = d.rename(columns={tarif_col: "tarif", cat_col: "categorie",
                          qcol: "quantite", "Somme_cumulee_quantites": "quantite_cumulee"})
    d.insert(0, "dimension", DIMENSIONS[dim])
    d.insert(0, "millesime", annee_txt)
    d.insert(0, "perimetre", perimetre)
    d["unite_tarif"] = unite_tarif
    d["unite_quantite"] = "MtCO2" if "MtCO2" in qcol else "TWh"
    simple.append(d[["perimetre", "millesime", "dimension", "tarif", "categorie",
                     "quantite", "quantite_cumulee", "unite_tarif", "unite_quantite"]])

s = pd.concat(simple, ignore_index=True)
s.to_csv(os.path.join(OUT, "elfe.csv"), index=False, encoding="utf-8")
print("elfe.csv :", s.shape)
print(s.groupby(["perimetre", "dimension"]).size().to_string())

if instruments:
    i = pd.concat(instruments, ignore_index=True)
    i.to_csv(os.path.join(OUT, "elfe_instruments.csv"), index=False, encoding="utf-8")
    print("\nelfe_instruments.csv :", i.shape)
    print(list(i.columns))

# --- contrôle d'intégrité Tier 4 : total identique entre dimensions ---
print("\n=== totaux par (perimetre, millesime, dimension) ===")
t = s.groupby(["perimetre", "millesime", "dimension"])["quantite"].sum().unstack()
print(t.round(2).to_string())
