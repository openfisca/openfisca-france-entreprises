"""Localise, par AST, toute lecture d'un parametre energies dans les formules de main.

Resout les alias (`p = parameters(period).energies...accise` puis `p.carburants.x`) et les
appels multi-lignes, puis croise avec la liste des parametres infra-annuels pour produire la
liste de travail de l'enveloppement en `tarif_moyen_annuel`.
"""
import ast
import re
import sys
from pathlib import Path

REPO = Path(r"c:\Users\p.dutronc\Documents\projets\openfisca-france-entreprises")
FORMULES = REPO / "openfisca_france_entreprises" / "variables" / "taxes" / "taxation_energies"
PARAMS = REPO / "openfisca_france_entreprises" / "parameters" / "energies"

DATE = re.compile(r"^(\s*)([12]\d{3})-(\d{2})-(\d{2}):")


# ---------------------------------------------------------------- parametres infra-annuels
def infra_annuels():
    out = {}
    for p in sorted(PARAMS.rglob("*.yaml")):
        if p.name == "index.yaml":
            continue
        text = p.read_text(encoding="utf-8")
        if not re.search(r"^values:", text, re.M):
            continue
        in_values, dates = False, []
        for line in text.splitlines():
            if re.match(r"^values:\s*$", line):
                in_values = True
                continue
            if in_values and re.match(r"^\S", line):
                in_values = False
            if not in_values:
                continue
            m = DATE.match(line)
            if m and len(m.group(1)) == 2:
                dates.append((m.group(2), m.group(3), m.group(4)))
        hors = [f"{a}-{m}-{j}" for a, m, j in dates if (m, j) != ("01", "01")]
        if hors:
            noeud = p.relative_to(PARAMS).with_suffix("").as_posix().replace("/", ".")
            out[noeud] = sorted(set(hors))
    return out


# ---------------------------------------------------------------- resolution des chaines
def chaine(node):
    """Deplie une chaine d'attributs en (base_node, [attrs...])."""
    attrs = []
    while isinstance(node, ast.Attribute):
        attrs.append(node.attr)
        node = node.value
    return node, list(reversed(attrs))


def est_appel_parameters(node):
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "parameters"
    )


def periode_lue(node):
    """Nom de la periode passee a parameters(...) — 'period', 'mois', autre."""
    if not node.args:
        return "?"
    a = node.args[0]
    return a.id if isinstance(a, ast.Name) else ast.unparse(a)


class Visiteur(ast.NodeVisitor):
    def __init__(self, chemin):
        self.chemin = chemin
        self.alias = {}       # nom -> (prefixe_noeud, periode)
        self.lectures = []    # (ligne, noeud_complet, periode, sous_enveloppe)
        self.pile_enveloppe = []

    # --- suivi de l'enveloppement existant
    def visit_Call(self, node):
        enveloppe = (
            isinstance(node.func, ast.Name) and node.func.id == "tarif_moyen_annuel"
        )
        if enveloppe:
            self.pile_enveloppe.append(True)
        self.generic_visit(node)
        if enveloppe:
            self.pile_enveloppe.pop()

    # --- alias : p = parameters(period).energies.x.y
    def visit_Assign(self, node):
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            base, attrs = chaine(node.value)
            if est_appel_parameters(base) and attrs[:1] == ["energies"]:
                self.alias[node.targets[0].id] = (
                    ".".join(attrs[1:]),
                    periode_lue(base),
                )
        self.generic_visit(node)

    # --- lectures
    def visit_Attribute(self, node):
        base, attrs = chaine(node)
        noeud = periode = None
        if est_appel_parameters(base) and attrs[:1] == ["energies"]:
            noeud, periode = ".".join(attrs[1:]), periode_lue(base)
        elif isinstance(base, ast.Name) and base.id in self.alias:
            prefixe, periode = self.alias[base.id]
            noeud = ".".join([prefixe, *attrs]) if prefixe else ".".join(attrs)
        if noeud:
            self.lectures.append(
                (node.lineno, noeud, periode, bool(self.pile_enveloppe)),
            )
            return  # ne pas redescendre : la chaine est deja capturee
        self.generic_visit(node)


def analyser():
    infra = infra_annuels()
    resultats = []
    for f in sorted(FORMULES.glob("*.py")):
        arbre = ast.parse(f.read_text(encoding="utf-8"))
        v = Visiteur(f.name)
        v.visit(arbre)
        for ligne, noeud, periode, enveloppe in v.lectures:
            # une lecture peut viser un noeud parent ; on retient le match le plus long
            cible = None
            for candidat in infra:
                if noeud == candidat or noeud.startswith(candidat + "."):
                    if cible is None or len(candidat) > len(cible):
                        cible = candidat
            if cible:
                resultats.append((f.name, ligne, noeud, cible, periode, enveloppe))
    return infra, resultats


if __name__ == "__main__":
    infra, res = analyser()
    a_faire = [r for r in res if not r[5]]
    deja = [r for r in res if r[5]]
    print(f"parametres infra-annuels           : {len(infra)}")
    print(f"lectures les visant                : {len(res)}")
    print(f"  deja en moyenne mensuelle        : {len(deja)}")
    print(f"  A ENVELOPPER                     : {len(a_faire)}\n")

    par_fichier = {}
    for nom, ligne, noeud, cible, periode, _ in a_faire:
        par_fichier.setdefault(nom, []).append((ligne, noeud, cible, periode))
    for nom in sorted(par_fichier):
        entrees = par_fichier[nom]
        print(f"### {nom}  ({len(entrees)} lectures)")
        vus = {}
        for ligne, noeud, cible, periode in entrees:
            vus.setdefault(cible, []).append(ligne)
        for cible in sorted(vus):
            lignes = vus[cible]
            print(f"  {cible}")
            print(f"      {len(lignes)} lecture(s) : lignes {', '.join(map(str, lignes[:12]))}"
                  + (" …" if len(lignes) > 12 else ""))
            print(f"      dates infra-annuelles : {', '.join(infra[cible])}")
        print()

    touches = {r[3] for r in res}
    jamais_lus = sorted(set(infra) - touches)
    print(f"### parametres infra-annuels jamais lus par une formule ({len(jamais_lus)})")
    for n in jamais_lus:
        print(f"  {n}  [{', '.join(infra[n])}]")
