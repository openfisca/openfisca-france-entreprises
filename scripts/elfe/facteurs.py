"""Facteurs d'émission implicites du CGDD, par régime et millésime.

MtCO2 / TWh = tCO2 / MWh exactement : le facteur se lit dans les quantités,
sans passer par les tarifs (donc sans pollution par l'ETS ni les boucliers).
"""
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
src = pd.read_csv(os.path.join(HERE, "elfe_consolide", "elfe.csv"))

d = src[src.dimension == "Régime fiscal"]
q = (d.groupby(["perimetre", "millesime", "categorie"])["quantite"].sum()
       .unstack("perimetre"))
q = q.dropna()
q = q[q["Energie"] > 1e-6]
q["facteur_tco2_par_mwh"] = q["Carbone"] / q["Energie"]

out = (q.reset_index()
        .rename(columns={"categorie": "regime", "Carbone": "quantite_mtco2",
                         "Energie": "quantite_twh"})
        [["regime", "millesime", "quantite_mtco2", "quantite_twh",
          "facteur_tco2_par_mwh"]]
        .sort_values(["regime", "millesime"]))

# stabilité temporelle, pour documenter l'effet d'incorporation des biocarburants
stat = out.groupby("regime")["facteur_tco2_par_mwh"].agg(["mean", "std", "count"])
stat["cv_pct"] = 100 * stat["std"] / stat["mean"]
out = out.merge(stat[["cv_pct"]], left_on="regime", right_index=True)
out["cv_pct"] = out["cv_pct"].round(4)
out["facteur_tco2_par_mwh"] = out["facteur_tco2_par_mwh"].round(6)

dest = os.path.join(HERE, "elfe_consolide", "facteurs_emission_cgdd.csv")
out.to_csv(dest, index=False, encoding="utf-8")
print("écrit :", dest, out.shape)
print("régimes :", out.regime.nunique(), "| millésimes :", sorted(out.millesime.unique()))
print("\nstabilité :")
print("  cv = 0        :", (stat.cv_pct.fillna(0) == 0).sum())
print("  cv < 0,5 %    :", (stat.cv_pct.fillna(0) < 0.5).sum())
print("  cv >= 0,5 %   :", (stat.cv_pct.fillna(0) >= 0.5).sum())
print("\ntête :")
print(out.head(10).to_string(index=False))
