"""Génère le gabarit Word du rapport de l'évaluation 2 (proposition technique).

On repart du gabarit de l'évaluation 1 pour garder exactement les mêmes styles
(titres, consignes en gris italique, tableaux), sa page de titre et sa table des
matières. Le reste est remplacé par un rapport autonome : résumé, sections 1 à 8
et annexes A à C. Les étudiants n'ont rien à modifier dans leur rapport 1.

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


def remplacer_texte(paragraphe, texte):
    """Remplace le texte d'un paragraphe en gardant la mise en forme de son premier segment."""
    runs = paragraphe.runs
    runs[0].text = texte
    for run in runs[1:]:
        run.text = ""


def garder_debut(doc):
    """Garde la page de titre et la table des matières du gabarit de l'évaluation 1, retire le reste."""
    corps = doc.element.body
    enfants = [e for e in corps if e.tag != qn("w:sectPr")]
    coupure = next(i for i, e in enumerate(enfants) if e.xpath("string(.)").strip() == "1. Résumé")
    for e in enfants[coupure:]:
        corps.remove(e)


QUESTIONS = [
    "Q1 — Réserver et payer en ligne",
    "Q2 — Faire signer la décharge avant l'arrivée",
    "Q3 — La plateforme du site",
    "Q4 — Montrer les vidéos sans ralentir le site",
    "Q5 — Offrir le site en français et en anglais",
]


def generer():
    doc = Document(SOURCE)
    garder_debut(doc)
    p = doc.paragraphs
    remplacer_texte(p[1], "Partie 2 — Proposition technique")
    remplacer_texte(p[5], "Date : 13 janvier 2027")
    remplacer_texte(p[6], "582-A05-RI — Analyse et conception Web — Évaluation 2 (20 %)")
    remplacer_texte(p[7], "Ce gabarit est votre rapport complet pour l'évaluation 2 : vous n'avez rien à modifier dans le "
                          "rapport de l'évaluation 1. Les paragraphes en gris italique sont des consignes : remplacez-les par "
                          "votre texte, puis supprimez-les. Quand une consigne renvoie au « rapport 1 », c'est votre rapport "
                          "de l'évaluation 1 : citez la section (par exemple « rapport 1, section 4.3 ») sans la recopier. "
                          "Gardez les styles Titre 1, Titre 2 et Titre 3 pour que la table des matières se mette à jour "
                          "(Références → Mettre à jour la table).")

    doc.add_heading("Résumé", level=1)
    consigne(doc, "Une demi-page au maximum, écrite en dernier. Pour une lectrice pressée : la recommandation (le projet "
                  "est-il faisable ?), les outils retenus en une phrase, le coût (coûts uniques et coûts annuels), la date de "
                  "mise en ligne visée et les deux ou trois décisions que Mélanie doit prendre. Aucun jargon.")
    saut(doc)

    # 1 -----------------------------------------------------------------------
    doc.add_heading("1. Introduction", level=1)
    doc.add_heading("1.1 Le mandat et l'évaluation technique, en bref", level=2)
    consigne(doc, "Dix lignes au plus, pour qu'on puisse lire cette proposition sans le rapport 1 : le client, ce qu'il "
                  "demande, la date ferme du 1er mars 2027 et le budget. Puis ce que l'évaluation technique a établi : les "
                  "contraintes déterminantes et les risques de la zone rouge, une ligne chacun, avec leur numéro (rapport 1, "
                  "sections 4.3 et 5.3). La section 4 y répond.")
    doc.add_heading("1.2 Ce que couvre cette proposition", level=2)
    consigne(doc, "Ce que la proposition décide : les outils, les formats, les adaptations, le temps, les coûts sur trois ans "
                  "et la recommandation. Ce qu'elle ne couvre pas : la conception graphique et la construction du site, qui "
                  "viendront ensuite.")
    doc.add_heading("1.3 Ce que la rencontre avec la cliente a changé", level=2)
    consigne(doc, "Les questions posées à Mélanie à la séance 9 (tirées du rapport 1, section 7.2), sa réponse, et ce que ça "
                  "change dans la proposition, avec le numéro de la section touchée. Une question restée sans réponse va à la "
                  "section 7.3, comme une décision que la cliente doit prendre.")
    tableau(doc, ["Question posée", "Réponse de Mélanie", "Ce que ça change (section)"], rangees=6)
    saut(doc)

    # 2 -----------------------------------------------------------------------
    doc.add_heading("2. Les choix techniques", level=1)
    doc.add_heading("2.1 Les critères de choix", level=2)
    consigne(doc, "Ce qui compte le plus pour ce client, tiré de vos exigences (rapport 1, section 3) et de vos contraintes "
                  "(rapport 1, section 4). Poids : 3 = indispensable, 2 = important, 1 = souhaitable. Cinq à huit critères. "
                  "Un outil qui échoue à un critère de poids 3 est écarté; entre les outils qui restent, les critères de poids "
                  "2 tranchent (voir l'exemple de la boulangerie, séance 8).")
    tableau(doc, ["Critère", "D'où il vient (exigence ou contrainte du rapport 1)", "Poids (1 à 3)"], rangees=6)

    doc.add_heading("2.2 Les choix pour les cinq questions", level=2)
    consigne(doc, "Partez des tableaux de comparaison communs : ce sont les mêmes pour toutes les équipes. Pour chaque "
                  "question : l'outil ou la solution retenu, pourquoi (les critères de 2.1, les essais, les sources), ce que "
                  "vous écartez et pourquoi, et ce qui reste à vérifier avant de s'engager. Pour Q4, on choisit où héberger "
                  "et comment diffuser les vidéos; la préparation des fichiers va à la section 3.")
    for q in QUESTIONS:
        doc.add_heading(q, level=3)
        tableau(doc, ["", "Notre choix"], premiere_colonne=[
            "Outil ou solution retenu",
            "Pourquoi (critères, essais, sources)",
            "Ce que nous écartons, et pourquoi",
            "Ce qui reste à vérifier",
        ], gras_premiere=True)

    saut(doc)

    # 3 -----------------------------------------------------------------------
    doc.add_heading("3. Les formats et les règles de mise en ligne", level=1)
    doc.add_heading("3.1 Les règles par sorte de contenu", level=2)
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
    doc.add_heading("3.2 Qui fait ce travail chez le client", level=2)
    consigne(doc, "Qui préparera les photos et les vidéos après la mise en ligne, avec quel outil, combien de temps par fichier "
                  "(mesuré au Lab 07), et à quel moment de l'année. Tenez compte des 70 heures par semaine de Mélanie l'été.")
    saut(doc)

    # 4 -----------------------------------------------------------------------
    doc.add_heading("4. Les adaptations proposées", level=1)
    doc.add_heading("4.1 Les contraintes déterminantes et les risques de la zone rouge", level=2)
    consigne(doc, "Une rangée pour chaque contrainte déterminante (rapport 1, section 4.3) et chaque risque de la zone rouge "
                  "(rapport 1, section 5.3), avec son numéro. Ne recopiez pas la mesure du rapport 1 : l'adaptation est la "
                  "décision concrète de votre proposition (l'outil retenu, la fonction à activer, la façon de faire) qui "
                  "obtient le résultat visé par la mesure.")
    tableau(doc, ["Contrainte ou risque (n° dans le rapport 1)", "L'adaptation que nous proposons", "Ce que ça change pour le client"], rangees=6)
    doc.add_heading("4.2 Ce que nous ne proposons pas", level=2)
    consigne(doc, "Les demandes du mandat que vous ne retenez pas, ou pas tout de suite (l'application mobile, le niveau de la "
                  "rivière en direct, l'ouverture l'hiver…), et pourquoi, ou pour quand.")
    saut(doc)

    # 5 -----------------------------------------------------------------------
    doc.add_heading("5. Le temps", level=1)
    doc.add_heading("5.1 Les tâches et l'estimation", level=2)
    consigne(doc, "Le travail de Studio Web FC découpé en tâches, chacune estimée en trois chiffres, en heures (séance 8 et "
                  "Lab 08). N'oubliez pas la gestion de projet, les rencontres, la formation de Mélanie et les tests. Au-delà de "
                  "15 tâches, regroupez-les ici et mettez le détail à l'annexe C.")
    tableau(doc, ["Tâche", "Optimiste (h)", "Probable (h)", "Pessimiste (h)", "Estimation retenue (h)"],
            premiere_colonne=[""] * 10 + ["Total"], gras_premiere=True)
    consigne(doc, "Sous le tableau : la formule de l'estimation retenue, (optimiste + 4 × probable + pessimiste) ÷ 6, et le "
                  "projet semblable auquel vous avez comparé votre total.")
    doc.add_heading("5.2 L'échéancier", level=2)
    consigne(doc, "Un échéancier simple, par étapes, de maintenant au 1er mars 2027, avec le coussin prévu pour les imprévus "
                  "(séance 8 et Lab 08). Pour chaque étape, ce que le client doit fournir et à quelle date (accès au domaine, "
                  "textes, photos, décharge traduite…). Les cycles de travail agiles ne sont pas demandés ici.")
    tableau(doc, ["Étape", "Début", "Fin", "Ce qui est livré", "Ce que le client doit fournir, et quand"], rangees=6)
    consigne(doc, "Sous le tableau, ajoutez un diagramme de Gantt des mêmes étapes, fait avec GanttProject ou Google Sheets "
                  "(séance 8, étape 3) et inséré comme image.")
    saut(doc)

    # 6 -----------------------------------------------------------------------
    doc.add_heading("6. L'argent", level=1)
    consigne(doc, "Hypothèses communes : Studio Web FC facture 75 $ de l'heure. Tous les montants sont en dollars canadiens et "
                  "avant taxes, le budget de Mélanie compris. Un seul taux de change pour tout le rapport. Écrivez sous chaque "
                  "tableau la date de lecture des prix, le taux de change et le volume utilisé (réservations, participants).")
    doc.add_heading("6.1 Les coûts uniques", level=2)
    tableau(doc, ["Élément", "Calcul", "Montant ($ CA)"],
            premiere_colonne=["Construction du site (heures de 5.1 × 75 $)", "", "", "Total"], gras_premiere=False)
    doc.add_heading("6.2 Les coûts annuels", level=2)
    tableau(doc, ["Élément", "Année 1", "Année 2", "Année 3"], premiere_colonne=["", "", "", "", "Total"])
    doc.add_heading("6.3 Le total sur trois ans, comparé au budget", level=2)
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
    doc.add_heading("6.4 Trois façons d'entrer dans le budget", level=2)
    tableau(doc, ["Option", "Ce que nous changeons", "Économie ($ CA)", "Ce que le client perd ou reporte"], premiere_colonne=[
        "A. Enlever des fonctionnalités",
        "B. Changer d'outil",
        "C. Livrer en plusieurs étapes",
    ], gras_premiere=True)
    saut(doc)

    # 7 -----------------------------------------------------------------------
    doc.add_heading("7. La recommandation finale", level=1)
    doc.add_heading("7.1 Notre recommandation", level=2)
    consigne(doc, "Première phrase : le projet est-il faisable (oui, non, ou oui à certaines conditions) ? Puis le scénario "
                  "recommandé, en une page au plus : ce qui sera en ligne le 1er mars, ce qui viendra ensuite, le coût sur trois ans.")
    doc.add_heading("7.2 Les conditions", level=2)
    consigne(doc, "Ce qui doit être vrai pour que la recommandation tienne (par exemple : l'accès au nom de domaine est récupéré "
                  "avant telle date).")
    doc.add_heading("7.3 Ce que le client doit décider et faire", level=2)
    tableau(doc, ["Décision ou action", "Qui", "Avant quand"], rangees=6)
    saut(doc)

    # 8 -----------------------------------------------------------------------
    doc.add_heading("8. Références", level=1)
    consigne(doc, "Style APA 7, par ordre alphabétique : toutes les sources de cette proposition (pages de prix, documentation "
                  "des fournisseurs, tableaux de comparaison communs). Pour les tableaux : Studio Web FC. (2026). Tableaux de "
                  "comparaison communs : essais des équipes du groupe [Document Word]. 582-A05-RI. Votre rapport de "
                  "l'évaluation 1 se cite aussi, s'il sert de source.")
    saut(doc)

    # Annexes -----------------------------------------------------------------
    doc.add_heading("Annexe A — Déclaration d'utilisation de l'IA générative", level=1)
    consigne(doc, "Pour cette proposition seulement. Si aucun outil n'a été utilisé, écrivez : « Aucun outil d'IA générative "
                  "n'a été utilisé pour ce travail. » L'IA ne doit pas produire les choix, l'estimation ou le devis.")
    tableau(doc, ["Outil", "Ce que nous lui avons demandé", "Ce que nous avons fait de sa réponse"], rangees=2)
    doc.add_heading("Annexe B — Contribution des membres", level=1)
    consigne(doc, "Pour cette proposition seulement. Chaque membre signe.")
    tableau(doc, ["Membre", "Sections rédigées", "Autres tâches (estimation, devis, révision, mise en page…)", "Signature"],
            rangees=3)
    doc.add_heading("Annexe C — Le détail de l'estimation", level=1)
    consigne(doc, "Seulement si la liste des tâches dépasse 15 lignes dans la section 5.1 : toutes les tâches, avec leurs trois "
                  "chiffres.")
    tableau(doc, ["Tâche", "Optimiste (h)", "Probable (h)", "Pessimiste (h)", "Estimation retenue (h)"], rangees=8)

    doc.save(SORTIE)
    print(f"Gabarit écrit : {SORTIE}")


if __name__ == "__main__":
    generer()
