"""Pilote : extrait, contrôle et écrit les tables du Voies et Moyens tome II.

    python -m scripts.vmt2.cli extraire [--de 2009] [--a 2025]
    python -m scripts.vmt2.cli crosswalk
"""
from __future__ import annotations

import argparse
import csv
import os
import sys

from . import annexe, controles, cout_par_impot, crosswalk, regime_b, regime_c
from .commun import (CHAMPS_CHIFFRAGE, CHAMPS_FICHE, DEPENSE_FISCALE,
                     REGIMES, SOURCES, texte)

#: racine du dépôt, deux niveaux au-dessus de scripts/vmt2/
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#: texte extrait par pdftotext, reconstruit à la demande et jamais versionné
CACHE = os.path.join(RACINE, '.cache', 'vmt2')
SORTIE = os.path.join(RACINE, 'assets', 'vmt2')

#: le régime A (PLF 2001-2008) n'est pas implémenté : cf. VMT2.md
PARSEURS = {'B': regime_b, 'C': regime_c}


def extraire(de: int, a: int):
    toutes, journal, recoup, couts = [], [], [], []
    for plf in range(de, a + 1):
        if plf not in SOURCES:
            journal.append(f"PLF{plf} : absent du fonds documentaire")
            continue
        if REGIMES[plf] not in PARSEURS:
            journal.append(f"PLF{plf} : régime {REGIMES[plf]} non implémenté")
            continue
        mod = PARSEURS[REGIMES[plf]]
        lignes = texte(plf, CACHE)
        fiches = mod.parse(lignes, plf)
        attendu = mod.nb_attendu(lignes)
        journal += controles.exhaustivite(fiches, attendu, plf)
        journal += controles.structure(fiches, plf)
        r = annexe.recoupement(fiches, annexe.parse(lignes, plf), plf)
        recoup.append(r)
        couts += cout_par_impot.recoupement(fiches, cout_par_impot.parse(lignes, plf), plf)
        n = len({f['numero'] for f in fiches if f.get('numero')})
        ndf = len({f['numero'] for f in fiches if f.get('perimetre') == DEPENSE_FISCALE})
        note = ('annexe absente' if not r['disponible'] else
                f"annexe {r['accords']}/{r['compares']} concordants")
        modal = f", {n - ndf:3d} modalités de calcul" if n != ndf else ''
        print(f"  PLF{plf} [{REGIMES[plf]}] {ndf:4d} dépenses fiscales{modal} "
              f"({n:4d} fiches / {attendu:4d} attendues) — {note}")
        toutes += [f for f in fiches if f.get('annee')]
    return toutes, journal, recoup, couts


def ecrire(fiches: list[dict]) -> tuple[str, str]:
    """Écrit les deux tables : les chiffrages, et les fiches qui les portent.

    Une fiche décrit trois années : répéter son libellé et ses métadonnées sur
    chaque ligne de chiffrage multiplierait par cinq le volume versionné, pour
    la même information. La jointure se fait sur (plf, numero).
    """
    os.makedirs(SORTIE, exist_ok=True)
    dest_c = os.path.join(SORTIE, 'chiffrages.csv')
    with open(dest_c, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=CHAMPS_CHIFFRAGE, delimiter=';',
                           extrasaction='ignore')
        w.writeheader()
        w.writerows(sorted(fiches, key=lambda f: (f['numero'], f['annee'], f['plf'])))

    vues = {}
    for f in fiches:
        vues.setdefault((f['plf'], f['numero']), f)
    dest_f = os.path.join(SORTIE, 'fiches.csv')
    with open(dest_f, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=CHAMPS_FICHE, delimiter=';',
                           extrasaction='ignore')
        w.writeheader()
        w.writerows(vues[k] for k in sorted(vues, key=lambda k: (k[1], k[0])))
    return dest_c, dest_f


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('commande', choices=['extraire', 'crosswalk'])
    p.add_argument('--de', type=int, default=2009)
    p.add_argument('--a', type=int, default=2025)
    args = p.parse_args(argv)

    if args.commande == 'extraire':
        print(f"Extraction PLF {args.de}-{args.a}")
        fiches, journal, recoup, couts = extraire(args.de, args.a)
        dest_c, dest_f = ecrire(fiches)
        print(f"-> {dest_c} : {len(fiches)} chiffrages")
        print(f"-> {dest_f} : {len({(f['plf'], f['numero']) for f in fiches})} fiches")

        print(f"\nContrôles de structure : {len(journal)} anomalie(s)")
        for m in journal[:40]:
            print('  !', m)

        des = [d for r in recoup if r['disponible'] for d in r['desaccords']]
        print(f"\nRecoupement fiche / annexe mission-programme : {len(des)} désaccord(s)")
        for d in des[:25]:
            print(f"  ! PLF{d['plf']} {d['numero']} : fiche {d['fiche']} "
                  f"({d['fiche_chiffrage']}) vs annexe {d['annexe']} "
                  f"({d['annexe_chiffrage']})  {d['libelle'][:55]}")
        for r in recoup:
            if r['disponible'] and r['absents_annexe']:
                print(f"  ! PLF{r['plf']} : {len(r['absents_annexe'])} DF sans "
                      f"contrepartie en annexe {r['absents_annexe'][:8]}")
        # Une mesure listée en annexe sans fiche n'est pas une anomalie : c'est
        # une modalité de calcul de l'impôt (mesure déclassée), que le document
        # continue de rattacher à un programme sans la chiffrer comme dépense.
        sans_fiche = sorted({(r['plf'], n) for r in recoup if r['disponible']
                             for n in r['absents_fiches']})
        if sans_fiche:
            print(f"\nMesures en annexe sans fiche (modalités de calcul de l'impôt) : "
                  f"{len({n for _, n in sans_fiche})} numéros")
            with open(os.path.join(SORTIE, 'mesures_sans_fiche.csv'), 'w',
                      encoding='utf-8', newline='') as fh:
                w = csv.writer(fh, delimiter=';')
                w.writerow(['plf', 'numero'])
                w.writerows(sans_fiche)
        if des:
            with open(os.path.join(SORTIE, 'desaccords_annexe.csv'), 'w',
                      encoding='utf-8', newline='') as fh:
                w = csv.DictWriter(fh, fieldnames=list(des[0]), delimiter=';')
                w.writeheader(); w.writerows(des)

        if couts:
            with open(os.path.join(SORTIE, 'controle_cout_par_impot.csv'), 'w',
                      encoding='utf-8', newline='') as fh:
                w = csv.DictWriter(fh, fieldnames=list(couts[0]), delimiter=';')
                w.writeheader(); w.writerows(couts)
            gros = [c for c in couts if abs(c['ecart']) > 0.005 * max(c['publie'], 1)
                    and abs(c['ecart']) > 50]
            print(f"\nContrôle « coût par impôt » : {len(couts)} postes-années recoupés, "
                  f"{len(gros)} écart(s) > 0,5 % et > 50 M€")
            print("  (contrôle à tolérance : les mesures nc ne sont pas sommables "
                  "et les epsilon valent moins de 0,5 M EUR)")
            for c in sorted(gros, key=lambda c: -abs(c['ecart']))[:20]:
                print(f"  ! PLF{c['plf']} impôt {c['impot']} {c['annee']} : "
                      f"extrait {c['extrait']} vs publié {c['publie']} "
                      f"({c['ecart']:+d} M€, {c['n_nc']} nc / {c['n_mesures']} mesures)")

        rev = controles.revisions(fiches)
        print(f"\nRévisions prévision initiale -> réalisation : {len(rev)} couples chiffrés")
        with open(os.path.join(SORTIE, 'revisions.csv'), 'w', encoding='utf-8',
                  newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=list(rev[0]), delimiter=';')
            w.writeheader(); w.writerows(rev)
        return 0 if not journal and not des else 1

    if args.commande == 'crosswalk':
        return crosswalk.construire(CACHE, SORTIE, args.de, args.a)
    return 0


if __name__ == '__main__':
    sys.exit(main())
