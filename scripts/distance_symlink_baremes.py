"""Mesure la distance entre `parameters/energies` d'OFF-E et le barème IPP des énergies.

Objectif de fond : pouvoir remplacer l'arbre de paramètres d'OFF-E par un symlink vers
`parameters/taxation_indirecte/energies` du dépôt barème. Ce script mesure ce qui l'en sépare
encore, et classe chaque écart par la nature du travail qu'il demande :

- fichiers identiques octet pour octet      → rien à faire
- valeurs divergentes                       → travail juridique (dates, montants)
- métadonnées ou forme seules               → hygiène (adopter la version barème)
- index / nœuds                             → structure
- orphelins côté OFF-E                      → vestiges à supprimer

Usage : python scripts/distance_symlink_baremes.py [--baremes CHEMIN] [--ref-off REF] [--ref-bar REF]
"""

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

OFF_ROOT = "openfisca_france_entreprises/parameters/energies/"
BAR_ROOT = "parameters/taxation_indirecte/energies/"


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout


def lister(repo, ref, racine):
    """Chemins relatifs à `racine` -> SHA du blob, pour `ref`.

    Les SHA sont retenus dès le listage parce que `git show <ref>:<chemin>` est inutilisable
    ici : git résout d'abord l'argument comme un chemin du système de fichiers, et échoue en
    « Filename too long » sur Windows dès que le préfixe de la copie de travail s'allonge — un
    worktree suffit. `git cat-file blob <sha>` ne touche pas au système de fichiers.
    """
    out = git(repo, "ls-tree", "-r", ref, "--", racine.rstrip("/"))
    if out is None:
        return None
    arbre = {}
    for ligne in out.decode("utf-8").splitlines():
        meta, chemin = ligne.split("\t", 1)
        if chemin.startswith(racine):
            arbre[chemin[len(racine) :]] = meta.split()[2]
    return arbre


def charger(repo, sha):
    b = git(repo, "cat-file", "blob", sha)
    return None if b is None else b.decode("utf-8")


def valeurs(text):
    """Bloc `values` normalisé (date -> value), ou None si le fichier n'en porte pas."""
    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError:
        return "__illisible__"
    if not isinstance(doc, dict) or not isinstance(doc.get("values"), dict):
        return None
    out = {}
    for d, contenu in doc["values"].items():
        cle = d.isoformat() if hasattr(d, "isoformat") else str(d)
        out[cle] = contenu.get("value") if isinstance(contenu, dict) else contenu
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--baremes", default="../baremes-ipp-yaml", type=Path)
    ap.add_argument("--ref-off", default="HEAD")
    ap.add_argument("--ref-bar", default="master")
    a = ap.parse_args()

    off_repo = Path(__file__).resolve().parent.parent
    bar_repo = (off_repo / a.baremes).resolve()
    if not (bar_repo / ".git").exists():
        sys.exit(f"dépôt barème introuvable : {bar_repo}")

    off = lister(off_repo, a.ref_off, OFF_ROOT)
    bar = lister(bar_repo, a.ref_bar, BAR_ROOT)
    if off is None or bar is None:
        sys.exit("référence git invalide")

    communs = sorted(set(off) & set(bar))
    off_seul = sorted(set(off) - set(bar))
    bar_seul = sorted(set(bar) - set(off))

    identiques, classes = [], {"valeurs": [], "forme": [], "index": [], "illisible": []}
    for rel in communs:
        # Même blob des deux côtés : identiques sans avoir à les lire.
        if off[rel] == bar[rel]:
            identiques.append(rel)
            continue
        ta = charger(off_repo, off[rel])
        tb = charger(bar_repo, bar[rel])
        if ta == tb:
            identiques.append(rel)
            continue
        va, vb = valeurs(ta), valeurs(tb)
        if "__illisible__" in (va, vb):
            classes["illisible"].append((rel, {}, {}, {}))
        elif va is None and vb is None:
            classes["index"].append((rel, {}, {}, {}))
        elif va != vb:
            seul_off = {k: v for k, v in (va or {}).items() if k not in (vb or {})}
            seul_bar = {k: v for k, v in (vb or {}).items() if k not in (va or {})}
            div = {
                k: (va[k], vb[k])
                for k in set(va or {}) & set(vb or {})
                if va[k] != vb[k]
            }
            classes["valeurs"].append((rel, seul_off, seul_bar, div))
        else:
            classes["forme"].append((rel, {}, {}, {}))

    # orphelins : index.yaml OFF-E dont le dossier ne porte aucun autre fichier
    orphelins = [
        f
        for f in off_seul
        if f.endswith("index.yaml")
        and not any(o.startswith(f[: -len("index.yaml")]) and o != f for o in off)
    ]

    print(f"OFF-E  ({a.ref_off}) : {len(off)} fichiers")
    print(f"barème ({a.ref_bar}) : {len(bar)} fichiers\n")
    print(f"chemins communs            : {len(communs)}")
    print(f"  identiques octet à octet : {len(identiques)}")
    print(f"  valeurs divergentes      : {len(classes['valeurs'])}")
    print(f"  forme/métadonnées seules : {len(classes['forme'])}")
    print(f"  index / nœuds            : {len(classes['index'])}")
    print(f"  illisibles               : {len(classes['illisible'])}")
    print(f"\nOFF-E seul  : {len(off_seul)}  (dont {len(orphelins)} index orphelins)")
    print(f"barème seul : {len(bar_seul)}  (acquis gratuitement par le symlink)")

    print("\n=== VALEURS DIVERGENTES — seul vrai obstacle juridique ===")
    for rel, seul_off, seul_bar, div in classes["valeurs"]:
        print(f"\n  {rel}")
        for k, (x, y) in sorted(div.items())[:6]:
            print(f"      ≠ {k} : OFF {x} | barème {y}")
        if seul_off:
            print(f"      dates OFF seul    : {', '.join(sorted(seul_off))}")
        if seul_bar:
            print(f"      dates barème seul : {', '.join(sorted(seul_bar))}")

    print("\n=== OFF-E SEUL, hors index orphelins ===")
    for f in off_seul:
        if f not in orphelins:
            print(f"  {f}")

    print("\n=== INDEX ORPHELINS À SUPPRIMER ===")
    for f in orphelins:
        print(f"  {f}")


if __name__ == "__main__":
    main()
