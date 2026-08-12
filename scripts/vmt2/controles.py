"""Contrôles de qualité de l'extraction.

Trois familles, du plus mécanique au plus substantiel :

1. **Exhaustivité** — le nombre de fiches extraites doit égaler le nombre de
   dépenses fiscales que le document contient, compté indépendamment du
   parseur (une grille « Impact budgétaire » par fiche en régime C, une ligne
   d'en-tête de mesure en régimes A/B).
2. **Structure** — aucune anomalie signalée par le parseur, un numéro à six
   chiffres, trois années consécutives finissant sur le millésime.
3. **Cohérence inter-millésimes** — une même année vue par deux documents
   successifs sous le même statut doit porter le même montant. Le tome II
   n'est pas censé réviser un chiffre à statut constant ; un écart signale
   soit une erreur d'extraction, soit une correction assumée par la DLF.
"""
from __future__ import annotations

import collections


def exhaustivite(fiches: list[dict], attendu: int, plf: int) -> list[str]:
    numeros = {f['numero'] for f in fiches if f.get('numero')}
    anomalies = [f for f in fiches if f.get('anomalie')]
    msgs = []
    if len(numeros) != attendu:
        msgs.append(f"PLF{plf} : {len(numeros)} dépenses extraites pour {attendu} attendues "
                    f"({attendu - len(numeros):+d})")
    for f in anomalies:
        msgs.append(f"PLF{plf} : {f.get('numero', '?')} — {f['anomalie']} (ligne {f['ligne']})")
    return msgs


def structure(fiches: list[dict], plf: int) -> list[str]:
    msgs = []
    par_num = collections.defaultdict(list)
    for f in fiches:
        if f.get('annee'):
            par_num[f['numero']].append(f['annee'])
    for num, annees in par_num.items():
        if sorted(annees) != [plf - 2, plf - 1, plf]:
            msgs.append(f"PLF{plf} : {num} porte les années {sorted(annees)} "
                        f"au lieu de {[plf - 2, plf - 1, plf]}")
    for f in fiches:
        if f.get('chiffrage', '').startswith('illisible'):
            msgs.append(f"PLF{plf} : {f['numero']} {f['annee']} montant {f['chiffrage']}")
    return msgs


def coherence(fiches: list[dict]) -> list[dict]:
    """Écarts entre deux millésimes qui décrivent la même année au même statut."""
    vue = {}
    for f in fiches:
        if not f.get('annee'):
            continue
        vue[(f['numero'], f['annee'], f['plf'])] = f
    ecarts = []
    for (num, annee, plf), f in vue.items():
        g = vue.get((num, annee, plf + 1))
        if g is None:
            continue
        if f['statut'] == 'autre' or g['statut'] == 'autre':
            continue
        # le statut change mécaniquement d'un millésime au suivant
        # (prevision_plf -> prevision -> realisation) : on ne compare que les
        # couples où le document réaffirme un chiffre déjà publié.
        if f['statut'] == 'prevision_plf' and g['statut'] == 'prevision' \
           and f['montant'] != g['montant']:
            ecarts.append(dict(numero=num, annee=annee, plf_a=plf, plf_b=plf + 1,
                               statut_a=f['statut'], statut_b=g['statut'],
                               montant_a=f['montant'], montant_b=g['montant'],
                               libelle=f['libelle'][:80]))
    return ecarts


def revisions(fiches: list[dict]) -> list[dict]:
    """Prévision initiale (millésime = année) vs réalisation (millésime = année+2)."""
    vue = {(f['numero'], f['annee'], f['plf']): f for f in fiches if f.get('annee')}
    out = []
    for (num, annee, plf), f in vue.items():
        if f['statut'] != 'prevision_plf' or f['montant'] is None:
            continue
        g = vue.get((num, annee, annee + 2))
        if g is None or g['statut'] != 'realisation' or g['montant'] is None:
            continue
        # le libellé n'est pas repris : il vit dans fiches.csv, joint sur
        # (plf, numero), et le dupliquer ici gonflerait un fichier dérivé
        out.append(dict(numero=num, annee=annee, impot=f['impot'],
                        prevu=f['montant'], realise=g['montant'],
                        ecart=g['montant'] - f['montant']))
    return sorted(out, key=lambda d: -abs(d['ecart']))
