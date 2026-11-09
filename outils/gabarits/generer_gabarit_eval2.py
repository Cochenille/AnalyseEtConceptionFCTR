"""Génère le gabarit Word de la partie 2 du rapport (évaluation 2).

On repart du gabarit de l'évaluation 1 pour garder exactement les mêmes styles
(titres, consignes en gris italique, tableaux), puis on remplace son contenu
par les nouvelles sections 8 à 13 et l'annexe D.

    python outils/gabarits/generer_gabarit_eval2.py

Sortie : docs/public/fiches/eval2-gabarit-proposition.docx
"""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import RGBColor

RACINE = Path(__file__).resolve().parents[2]
SOURCE = RACINE / "docs" / "public" / "fiches" / "eval1-gabarit-rapport.docx"
SORTIE = RACINE / "docs" / "public" / "fiches" / "eval2-gabarit-proposition.docx"

GRIS = RGBColor(0x56, 0x61, 0x6C)
BLEU_ENTETE = "E0E7FF"


def vider(doc):
    corps = doc.element.body
    for enfant in list(corps):
        if enfant.tag != qn("w:sectPr"):
            corps.remove(enfant)


def consigne(doc, texte):
    run = doc.add_paragraph().add_run(texte)
    run.italic = True
    run.font.color.rgb = GRIS


def ombrer(cellule):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), BLEU_ENTETE)
    cellule._tc.get_or_add_tcPr().append(shd)


def tableau(doc, entetes, rangees=3, premiere_colonne=None, gras_premiere=False):
    """Un tableau à remplir : en-têtes en bleu, rangées vides ou dont la première case est donnée."""
    textes = premiere_colonne or [""] * rangees
    t = doc.add_table(rows=1 + len(textes), cols=len(entetes))
    t.style = "Table Grid"
    for cellule, titre in zip(t.rows[0].cells, entetes):
        cellule.paragraphs[0].add_run(titre).bold = True
        ombrer(cellule)
    for rangee, texte in zip(t.rows[1:], textes):
        if texte:
            run = rangee.cells[0].paragraphs[0].add_run(texte)
            run.bold = gras_premiere
    doc.add_paragraph()
    return t


def saut(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


QUESTIONS = [
    "Q1 — Réserver et payer en ligne",
    "Q2 — Faire signer la décharge avant l'arrivée",
    "Q3 — La plateforme du site",
    "Q4 — Montrer les vidéos sans ralentir le site",
    "Q5 — Offrir le site en français et en anglais",
]


def generer():
    doc = Document(SOURCE)
    vider(doc)

    doc.add_paragraph("Rapport de faisabilité technique", style="Title")
    doc.add_paragraph("Partie 2 — Proposition technique : les sections à ajouter")
    doc.add_paragraph("582-A05-RI — Analyse et conception Web — Évaluation 2 (20 %)")
    consigne(doc, "Ce gabarit contient seulement les nouvelles sections. Copiez-les dans votre rapport de l'évaluation 1, "
                  "entre la section 7 et les références, qui deviennent la section 14. Les paragraphes en gris italique sont "
                  "des consignes : remplacez-les par votre texte, puis supprimez-les. Gardez les styles Titre 1, Titre 2 et "
                  "Titre 3 pour que la table des matières se mette à jour.")
    consigne(doc, "Dans la partie 1 : mettez à jour la page de titre (retirez « Partie 1 — Évaluation technique »), réécrivez "
                  "le résumé pour tout le rapport (il donne maintenant la recommandation, le coût et la date de mise en ligne), "
                  "mettez à jour la portée (2.3) et la section 7, et appliquez les commentaires reçus pour l'évaluation 1.")
    saut(doc)

    # 8 -----------------------------------------------------------------------
    doc.add_heading("8. Les choix techniques", level=1)
    doc.add_heading("8.1 Les critères de choix", level=2)
    consigne(doc, "Ce qui compte le plus pour ce client, tiré de vos exigences (section 3) et de vos contraintes (section 4). "
                  "Poids : 3 = indispensable, 2 = important, 1 = souhaitable. Cinq à huit critères. Un outil qui échoue à un "
                  "critère de poids 3 est écarté; entre les outils qui restent, les critères de poids 2 tranchent (voir "
                  "l'exemple de l'énoncé).")
    tableau(doc, ["Critère", "D'où il vient (exigence ou contrainte)", "Poids (1 à 3)"], rangees=6)

    doc.add_heading("8.2 Les choix pour les cinq questions", level=2)
    consigne(doc, "Pour chaque question : l'outil ou la solution retenu, pourquoi (les critères de 8.1, vos essais, vos sources), "
                  "ce que vous écartez et pourquoi, et ce qui reste à vérifier. Pour les questions que vous n'avez pas essayées, "
                  "dites sur quoi repose le choix et ce qu'un essai devra confirmer avant de s'engager. Pour Q4, on choisit où "
                  "héberger et comment diffuser les vidéos; la préparation des fichiers va à la section 9.")
    for q in QUESTIONS:
        doc.add_heading(q, level=3)
        tableau(doc, ["", "Notre choix"], premiere_colonne=[
            "Outil ou solution retenu",
            "Pourquoi (critères, essais, sources)",
            "Ce que nous écartons, et pourquoi",
            "Ce qui reste à vérifier",
        ], gras_premiere=True)

    doc.add_heading("8.3 Comment les outils fonctionnent ensemble", level=2)
    consigne(doc, "Un schéma simple (fait dans Word, PowerPoint ou draw.io) : le site, la réservation, la décharge, Square, Viator, "
                  "Google Workspace et le nom de domaine. Une flèche pour ce qui passe d'un outil à l'autre (une réservation, "
                  "un paiement, une liste de participants). Indiquez les liens qui demandent une manipulation à la main. "
                  "Sous le schéma, quelques lignes pour Mélanie : ce qui se fait tout seul, et ce qu'elle ou Karine devra faire.")
    saut(doc)

    # 9 -----------------------------------------------------------------------
    doc.add_heading("9. Les formats et les règles de mise en ligne", level=1)
    doc.add_heading("9.1 Les règles par sorte de contenu", level=2)
    consigne(doc, "Tirées de la séance 7 et de vos résultats du Lab 07. Ajoutez des rangées au besoin.")
    tableau(doc, ["Sorte de contenu", "Format", "Largeur", "Poids maximal", "Outil", "Règle d'accessibilité"], premiere_colonne=[
        "Photo pleine largeur",
        "Photo dans le texte",
        "Vignette",
        "Logo et icônes",
        "Vidéo d'arrière-plan",
        "Vidéo où l'on parle",
        "Tarifs, horaires, conditions",
        "Document à imprimer ou à signer",
    ], gras_premiere=True)
    doc.add_heading("9.2 Qui fait ce travail chez le client", level=2)
    consigne(doc, "Qui préparera les photos et les vidéos après la mise en ligne, avec quel outil, combien de temps par fichier "
                  "(mesuré au Lab 07), et à quel moment de l'année. Tenez compte des 70 heures par semaine de Mélanie l'été.")
    saut(doc)

    # 10 ----------------------------------------------------------------------
    doc.add_heading("10. Les adaptations proposées", level=1)
    doc.add_heading("10.1 Les contraintes déterminantes et les risques de la zone rouge", level=2)
    consigne(doc, "Une rangée pour chaque contrainte déterminante (section 4.3) et chaque risque de la zone rouge (section 5.3), "
                  "avec son numéro. Ne recopiez pas la mesure de la section 5.3 : l'adaptation est la décision concrète de votre "
                  "proposition (l'outil retenu, la fonction à activer, la façon de faire) qui obtient le résultat visé par la mesure.")
    tableau(doc, ["Contrainte ou risque (n°)", "L'adaptation que nous proposons", "Ce que ça change pour le client"], rangees=6)
    doc.add_heading("10.2 Ce que nous ne proposons pas", level=2)
    consigne(doc, "Les demandes du mandat que vous ne retenez pas, ou pas tout de suite (l'application mobile, le niveau de la "
                  "rivière en direct, l'ouverture l'hiver…), et pourquoi, ou pour quand.")
    saut(doc)

    # 11 ----------------------------------------------------------------------
    doc.add_heading("11. Le temps", level=1)
    doc.add_heading("11.1 Les tâches et l'estimation", level=2)
    consigne(doc, "Le travail de Studio Web FC découpé en tâches, chacune estimée en trois chiffres, en heures (vu à la séance 8). "
                  "N'oubliez pas la gestion de projet, les rencontres, la formation de Mélanie et les tests. Au-delà de 15 tâches, "
                  "regroupez-les ici et mettez le détail à l'annexe D.")
    tableau(doc, ["Tâche", "Optimiste (h)", "Probable (h)", "Pessimiste (h)", "Estimation retenue (h)"],
            premiere_colonne=[""] * 10 + ["Total"], gras_premiere=True)
    consigne(doc, "Sous le tableau : comment l'estimation retenue est calculée, et à quoi vous l'avez comparée.")
    doc.add_heading("11.2 L'échéancier", level=2)
    consigne(doc, "Un échéancier simple, par étapes, de maintenant au 1er mars 2027, avec le coussin prévu pour les imprévus "
                  "(vu à la séance 8). Pour chaque étape, ce que le client doit fournir et à quelle date (accès au domaine, textes, "
                  "photos, décharge traduite…). Les cycles de travail agiles ne sont pas demandés ici.")
    tableau(doc, ["Étape", "Début", "Fin", "Ce qui est livré", "Ce que le client doit fournir, et quand"], rangees=6)
    saut(doc)

    # 12 ----------------------------------------------------------------------
    doc.add_heading("12. L'argent", level=1)
    consigne(doc, "Hypothèses communes : Studio Web FC facture 75 $ de l'heure. Tous les montants sont en dollars canadiens et "
                  "avant taxes, le budget de Mélanie compris. Un seul taux de change pour tout le rapport. Écrivez sous chaque "
                  "tableau la date de lecture des prix, le taux de change et le volume utilisé (réservations, participants).")
    doc.add_heading("12.1 Les coûts uniques", level=2)
    tableau(doc, ["Élément", "Calcul", "Montant ($ CA)"], premiere_colonne=["Construction du site (heures de 11.1 × 75 $)", "", "", "Total"], gras_premiere=False)
    doc.add_heading("12.2 Les coûts annuels", level=2)
    tableau(doc, ["Élément", "Année 1", "Année 2", "Année 3"], premiere_colonne=["", "", "", "", "Total"])
    doc.add_heading("12.3 Le total sur trois ans, comparé au budget", level=2)
    consigne(doc, "Le total sur trois ans, à titre d'information : c'est ce que le projet coûtera vraiment.")
    tableau(doc, ["", "Année 1", "Année 2", "Année 3", "Total"], premiere_colonne=[
        "Coûts uniques",
        "Coûts annuels",
        "Total",
    ], gras_premiere=True)
    consigne(doc, "La comparaison au budget. Le budget de Mélanie sert à la construction : on y compare les coûts uniques. "
                  "Elle n'a pas prévu de coûts annuels : on les compare à ce que l'entreprise paie aujourd'hui pour son site "
                  "(environ 300 $ par année pour Wix, selon elle).")
    tableau(doc, ["", "Nos coûts", "Budget ou repère", "Écart"], premiere_colonne=[
        "Coûts uniques, budget de base",
        "Coûts uniques, subvention accordée",
        "Coûts annuels (par année)",
    ], gras_premiere=True)
    t = doc.tables[-1]
    for rangee, repere in zip(t.rows[1:], ["8 000 $", "13 000 $", "environ 300 $"]):
        rangee.cells[2].paragraphs[0].add_run(repere)
    consigne(doc, "Quelques lignes pour Mélanie : ce que ces chiffres veulent dire pour l'entreprise, et combien elle devra prévoir "
                  "chaque année.")
    doc.add_heading("12.4 Trois façons d'entrer dans le budget", level=2)
    tableau(doc, ["Option", "Ce que nous changeons", "Économie ($ CA)", "Ce que le client perd ou reporte"], premiere_colonne=[
        "A. Enlever des fonctionnalités",
        "B. Changer d'outil",
        "C. Livrer en plusieurs étapes",
    ], gras_premiere=True)
    saut(doc)

    # 13 ----------------------------------------------------------------------
    doc.add_heading("13. La recommandation finale", level=1)
    doc.add_heading("13.1 Notre recommandation", level=2)
    consigne(doc, "Première phrase : le projet est-il faisable (oui, non, ou oui à certaines conditions) ? Puis le scénario "
                  "recommandé, en une page au plus : ce qui sera en ligne le 1er mars, ce qui viendra ensuite, le coût sur trois ans.")
    doc.add_heading("13.2 Les conditions", level=2)
    consigne(doc, "Ce qui doit être vrai pour que la recommandation tienne (par exemple : l'accès au nom de domaine est récupéré "
                  "avant telle date).")
    doc.add_heading("13.3 Ce que le client doit décider et faire", level=2)
    tableau(doc, ["Décision ou action", "Qui", "Avant quand"], rangees=6)
    saut(doc)

    # Annexes -----------------------------------------------------------------
    doc.add_heading("Annexe D — Le détail de l'estimation", level=1)
    consigne(doc, "Seulement si la liste des tâches dépasse 15 lignes dans la section 11.1 : toutes les tâches, avec leurs trois "
                  "chiffres. Dans les annexes B (IA générative) et C (contribution des membres) de votre rapport, gardez la "
                  "partie de l'évaluation 1 (B.1, C.1) et ajoutez à la suite une partie B.2 et une partie C.2 pour "
                  "l'évaluation 2.")
    tableau(doc, ["Tâche", "Optimiste (h)", "Probable (h)", "Pessimiste (h)", "Estimation retenue (h)"], rangees=8)

    doc.save(SORTIE)
    print(f"Gabarit écrit : {SORTIE}")


if __name__ == "__main__":
    generer()
