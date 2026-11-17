"""Génère les tableaux de comparaison communs remis avec la correction de l'évaluation 1.

Un tableau par question (Q1 à Q5) qui regroupe les essais de toutes les équipes, avec les
coûts sur trois ans recalculés selon les mêmes hypothèses. Ce document sert de base égale
à chaque équipe pour la section 8.2 de l'évaluation 2.

    python outils/gabarits/generer_tableaux_communs.py

Sortie : docs/public/fiches/eval2-tableaux-communs.docx

Conventions dans le contenu :
- un texte qui commence par « ◆ » a été ajouté par l'enseignant d'après la documentation du
  fournisseur, lue en novembre 2026 : il s'affiche en gris italique;
- R = réussi, É = échoué, P = partiel, NV = non vérifiable (résultats des essais des équipes).
- Chaque case donne un seul prix et un seul coût; quand deux équipes diffèrent, la case dit
  laquelle a mesuré quoi.
"""

from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

RACINE = Path(__file__).resolve().parents[2]
SOURCE = RACINE / "docs" / "public" / "fiches" / "eval1-gabarit-rapport.docx"
SORTIE = RACINE / "docs" / "public" / "fiches" / "eval2-tableaux-communs.docx"

GRIS = RGBColor(0x56, 0x61, 0x6C)
BLEU_ENTETE = "E0E7FF"
GRIS_CRITERE = "F1F5F9"
TAILLE_TABLEAU = Pt(8.5)

LIGNES = [
    "Famille de solution",
    "Essayé par",
    "Ce que les essais ont montré",
    "Échecs et limites observés",
    "Ce que les essais n'ont pas couvert",
    "Forfait retenu pour le calcul",
    "Coût sur 3 ans ($ CA, hypothèses communes)",
    "Temps pour apprendre (mesuré)",
]

# ---------------------------------------------------------------------------
# Contenu
# ---------------------------------------------------------------------------

QUESTIONS = [
    {
        "titre": "Q1 — Réserver et payer en ligne",
        "besoin": "Afficher les départs et les places qui restent, empêcher les doubles réservations, encaisser le "
                  "paiement (Square est déjà utilisé sur place), recevoir les réservations Viator dans le même horaire, "
                  "confirmer par courriel et gérer les groupes (soumission, dépôt de 30 %). Mélanie modifie seule les "
                  "prix et les horaires.",
        "outils": ["Bookeo", "Rezgo", "SimplyBook.me", "Bókun", "Rezdy"],
        "cases": {
            "Famille de solution": ["Service spécialisé (SaaS)"] * 5,
            "Essayé par": [
                "2 équipes",
                "1 équipe",
                "1 équipe",
                "1 équipe",
                "1 équipe",
            ],
            "Ce que les essais ont montré": [
                "Places restantes à jour après une réservation de 5 sur 10 (R). Plage complète impossible à "
                "sélectionner (R). Courriel de confirmation reçu par la cliente (R). Réservation faite en moins de "
                "5 min, en français (R). Tarif créé en moins de 1 min. Réservation de groupe, ajout d'une décharge "
                "et paiement à la réservation possibles.",
                "Réservation de groupe possible. Décharge ajoutée à la réservation. Produits ajoutés à "
                "l'inventaire. Paiement à la réservation. Tutoriel disponible.",
                "Réservation faite en moins de 5 min (R). Tarif créé en moins de 1 min. Réservation de groupe, "
                "ajout d'une décharge, vue d'ensemble des réservations et paiement à la réservation possibles.",
                "Places restantes à jour (R). Plage complète impossible à sélectionner (R), mais le nombre de "
                "places restantes n'est pas affiché.",
                "Plage complète impossible à sélectionner (R). Un réglage de paiement Square existe dans les "
                "paramètres.",
            ],
            "Échecs et limites observés": [
                "Annuler un départ complet : 2 min 26 s, avec aide. Création d'un événement difficile à trouver. "
                "Aide et tutoriels en anglais seulement.",
                "Une réservation de kayak a pris 10 min. Parcours de réservation en français : É.",
                "Parcours de réservation en français : É. ◆ Le fournisseur n'offre le français au client que par "
                "une traduction automatique (Google Traduction) ajoutée à la page. Frais de plateforme de 1 à 2 % "
                "par paiement sur les forfaits Basic et Standard. Textos et WhatsApp payés en crédits.",
                "Annuler un départ : 10 min 37 s, avec aide (É). Aucun courriel de confirmation (É). Paiement "
                "Square non offert (É). Chaque action ouvre une nouvelle fenêtre.",
                "Annuler : 1 min 43 s, mais impossible de modifier une réservation, et aucun courriel envoyé (É). "
                "Aucun courriel de confirmation après la réservation (É).",
            ],
            "Ce que les essais n'ont pas couvert": [
                "Modifier une seule réservation. ◆ Square : offert comme moyen de paiement en ligne (page d'aide "
                "de Square). ◆ Viator : Bookeo figure dans la liste des systèmes de réservation reliés à Viator "
                "(Viator, centre de ressources des opérateurs).",
                "◆ Square : offert pour le paiement en ligne et le terminal Square Terminal; pas l'application ni "
                "les autres appareils Square. ◆ Viator : liaison directe; les réservations Viator entrent dans "
                "Rezgo et Viator lit les places en temps réel.",
                "◆ Square : absent des moyens de paiement du fournisseur (SBPay.me); la liaison passe par un outil "
                "d'automatisation comme Zapier. ◆ Viator : aucune liaison dans la documentation du fournisseur.",
                "◆ Viator : Bókun appartient à Tripadvisor (propriétaire de Viator) depuis 2018; la liaison se fait "
                "dans l'onglet des outils de vente et met à jour les places sur Viator. Bókun ne prend pas de frais "
                "sur les réservations Viator. ◆ Square : absent des moyens de paiement offerts (Stripe, PayPal, "
                "Braintree…), ce qui confirme l'essai.",
                "Places restantes côté client (aucun produit visible dans la simulation). ◆ Viator : relié par le "
                "gestionnaire de canaux, inclus dans tous les forfaits. ◆ Square : offert pour le paiement en ligne "
                "et le lecteur Square Reader; un paiement fait au Square Terminal s'ajoute à la main à la "
                "réservation.",
            ],
            "Forfait retenu pour le calcul": [
                "Standard (Tours & Activities) : 39,95 $ US/mois, sans commission. 20 comptes d'employés, "
                "1 000 réservations par mois.",
                "Aucun abonnement : commission de 4,9 % sur chaque réservation en ligne.",
                "Premium : 66,67 $ CA/mois. Crédits de textos en plus.",
                "Start : 49 $ US/mois + 1,5 % par réservation en ligne.",
                "Accelerate : 99 $ US/mois + 3 % par réservation en ligne.",
            ],
            "Coût sur 3 ans ($ CA, hypothèses communes)": [
                "1 985 $",
                "31 752 $",
                "2 400 $ + crédits de textos",
                "12 154 $",
                "24 358 $",
            ],
            "Temps pour apprendre (mesuré)": [
                "24 min et 30 min (deux équipes)",
                "30 à 45 min",
                "25 à 30 min",
                "35 min",
                "27 min",
            ],
        },
        "calculs": [
            "Bookeo : 39,95 $ US × 36 mois × 1,38 = 1 985 $. Le forfait Standard suffit : 1 800 réservations par "
            "année, c'est moins de 1 000 par mois, même en juillet.",
            "Rezgo : 216 000 $ × 4,9 % = 10 584 $ par année × 3 = 31 752 $.",
            "SimplyBook.me : 66,67 $ × 36 mois = 2 400 $, sans les crédits de textos.",
            "Bókun : 49 $ US × 36 × 1,38 = 2 434 $ + (216 000 $ × 1,5 % = 3 240 $) × 3 = 9 720 $. Total : 12 154 $.",
            "Rezdy : 99 $ US × 36 × 1,38 = 4 918 $ + (216 000 $ × 3 % = 6 480 $) × 3 = 19 440 $. Total : 24 358 $.",
            "Les frais de traitement des cartes (Square, Stripe…) s'ajoutent pour tous les outils; ils ne sont pas comptés ici.",
        ],
        "a_verifier": [
            "Une réservation Viator qui entre d'elle-même dans l'horaire et retire les places (le problème des "
            "doubles réservations du mandat) : la liaison exige un compte Viator, qu'aucune équipe n'avait.",
            "Un paiement en ligne par Square, avec le vrai compte Square de l'entreprise.",
            "Le parcours complet du client en anglais, jusqu'au courriel de confirmation.",
            "Annuler tous les départs d'un après-midi (orage) et prévenir les clients en une seule opération.",
            "Un départ de via ferrata à 8 places, avec une liste d'attente.",
        ],
        "autres": [
            "Checkfront, FareHarbor, Xola, Zaui, Regiondo : nommés dans les sources des équipes, non essayés.",
            "◆ Wix Bookings (famille : fonction de la plateforme) est inclus dans les forfaits Wix qui acceptent "
            "les paiements, donc sans coût de plus si le site reste sur Wix.",
            "◆ FareHarbor ne facture pas l'entreprise : des frais de réservation sont ajoutés au prix que paie le "
            "client.",
        ],
    },
    {
        "titre": "Q2 — Faire signer la décharge avant l'arrivée",
        "besoin": "Chaque participant signe la décharge avant d'arriver, sur téléphone ou ordinateur, en français ou "
                  "en anglais; un parent signe pour un mineur. Les réponses de santé (allergies, épilepsie, natation) "
                  "restent liées à la bonne personne. Au quai, sans réseau, le guide voit qui a signé et qui est "
                  "allergique, sans accès au reste du dossier (Loi 25).",
        "outils": ["WaiverFile", "WaiverSign", "Smartwaiver", "Simple Waiver", "AgreeDock"],
        "cases": {
            "Famille de solution": ["Service spécialisé (SaaS)"] * 5,
            "Essayé par": ["1 équipe", "1 équipe", "2 équipes", "1 équipe", "1 équipe"],
            "Ce que les essais ont montré": [
                "Deux décharges signées sur téléphone et ordinateur, sans impression (R). Décharge parentale pour "
                "un enfant (R). Recherche d'une décharge parmi 20 : 20 s (R). Modèles de décharge offerts.",
                "Deux décharges signées sur téléphone et ordinateur (R). Mineur signé par sa mère (R). Sans réseau, "
                "liste et décharges du jour consultables avec les allergies (R). Recherche par nom : moins de 1 s "
                "(R). Choix English/Français à l'ouverture du lien; décharge remplie en anglais (R).",
                "Décharges signées sur téléphone et ordinateur, courriel de confirmation reçu (R). Recherche : "
                "moins de 1 s (R). Décharge offerte en français, anglais, espagnol et chinois (R). Export CSV par "
                "dates (R) : Mélanie peut ne garder que les colonnes utiles au guide. Drapeau rouge sur une réponse "
                "à surveiller. Période de conservation réglable. Copie PDF envoyée au participant.",
                "Signature en ligne et copie PDF envoyée par courriel. Un parent signe pour un mineur. Liste des "
                "participants affichée en 2 clics.",
                "Lien envoyé à la réservation, approbation d'un parent pour un mineur, reçu par courriel. "
                "Interface administrateur offerte en français.",
            ],
            "Échecs et limites observés": [
                "Une seule décharge pour le parent et ses enfants : recherche difficile (P). Aucun réglage trouvé "
                "pour cacher au guide les données de santé (É), même si le fournisseur annonce des permissions par "
                "rôle. Aucune consultation sans réseau (É). Questionnaire en français, page d'accueil en anglais. "
                "Export de 20 décharges lent, avec erreurs; PDF un à la fois, environ 1 min chacun (É).",
                "Deux adultes = deux décharges séparées (P). Le compte guide voit tout le dossier (naissance, "
                "contact d'urgence, santé) et peut le télécharger même si l'export est désactivé (É). Allergies "
                "visibles seulement en ouvrant chaque décharge : 1 min 48 s pour 5 participants (P). Export : un "
                "PDF à la fois (P).",
                "Plusieurs participants sur une décharge : les réponses de santé valent pour tout le groupe, pas "
                "par personne (P). Interface administrateur en anglais seulement. L'ancien outil d'export disparaît "
                "à la fin de 2026 (migration vers « Participant CSV »).",
                "Interface en anglais seulement.",
                "Le code QR s'envoie à la main par courriel. Plus de manipulations que les deux autres outils "
                "essayés par la même équipe. Les formulaires doivent être rédigés en français, sinon ils restent "
                "en anglais.",
            ],
            "Ce que les essais n'ont pas couvert": [
                "Version anglaise de la décharge. Accès réel d'un compte guide (compte fictif). ◆ Le fournisseur "
                "n'annonce aucun mode sans réseau.",
                "« Export Documents » (grisé dans l'essai).",
                "Consultation sans réseau et accès du guide (code administrateur du mode kiosque requis). Un "
                "questionnaire de santé distinct par participant dans une décharge de groupe.",
                "Consultation sans réseau, accès limité du guide, version anglaise. ◆ Le fournisseur n'annonce ni "
                "mode sans réseau, ni rôles d'employés, ni choix de langue.",
                "Consultation sans réseau, accès limité du guide. ◆ Le fournisseur n'annonce ni mode sans réseau, "
                "ni rôles d'employés.",
            ],
            "Forfait retenu pour le calcul": [
                "◆ Growth, payé à l'année : 999 $ US/an, 10 000 décharges par année. Le forfait « avec HIPAA » "
                "(1 399 $ US) n'est pas retenu : HIPAA est une loi américaine, qui ne s'applique pas ici.",
                "Growth : 19 $ US/mois, 100 décharges incluses, puis 0,15 $ US par décharge.",
                "Archivage (7 $ US/mois) hors saison; Premium (205 $ ou 280 $ US/mois) en saison. On change de "
                "forfait chaque mois.",
                "◆ Unlimited (89 $ US/mois, décharges illimitées) en saison; Archive (5 $ US/mois) hors saison. "
                "Facturé au mois. En Archive, aucune nouvelle signature n'est possible.",
                "◆ Pro : décharges et signatures illimitées. 168,48 $ CA/an (14,04 $/mois payé à l'année).",
            ],
            "Coût sur 3 ans ($ CA, hypothèses communes)": [
                "4 136 $",
                "6 222 $",
                "5 067 $",
                "1 987 $",
                "505 $",
            ],
            "Temps pour apprendre (mesuré)": [
                "Compte : 2 min. Saisie du texte et des questions : environ 1 h. Comprendre l'interface : 10 min.",
                "Première décharge prête : environ 50 min. Compte guide et permissions : 10 min.",
                "Modèle de décharge : 1 h 25. Remplir une décharge : 2 min (téléphone), 3 min (ordinateur). "
                "Principales fonctions : 25 min (autre équipe).",
                "Non mesuré par l'équipe.",
                "Non mesuré par l'équipe.",
            ],
        },
        "calculs": [
            "Volume commun : 9 000 décharges par année, réparties ainsi : juin 1 800, juillet 3 000, août 3 000, "
            "septembre 800, octobre 400. Aucune de novembre à mai (7 mois).",
            "WaiverFile : 999 $ US × 1,38 = 1 379 $ par année × 3 = 4 136 $. Les 10 000 décharges par année "
            "couvrent les 9 000.",
            "WaiverSign : décharges au-delà de 100 à 0,15 $ US. Juin 274 $, juillet 454 $, août 454 $, septembre "
            "124 $, octobre 64 $, novembre à mai 19 $ × 7 = 133 $. Total : 1 503 $ US × 1,38 = 2 074 $ par année "
            "× 3 = 6 222 $.",
            "Smartwaiver : Premium à 205 $ US en juin, septembre et octobre, à 280 $ US en juillet et en août, "
            "Archivage à 7 $ US les 7 autres mois : 615 $ + 560 $ + 49 $ = 1 224 $ US × 1,38 = 1 689 $ par année "
            "× 3 = 5 067 $. Changer de forfait chaque mois demande une action de Mélanie.",
            "Simple Waiver : 89 $ US × 5 mois + 5 $ US × 7 mois = 480 $ US × 1,38 = 662 $ par année × 3 = 1 987 $. "
            "Changer de forfait deux fois par année demande une action de Mélanie.",
            "AgreeDock : 168,48 $ × 3 = 505 $.",
        ],
        "a_verifier": [
            "Une décharge de groupe ou de famille avec un questionnaire de santé distinct par personne.",
            "Ce que voit un vrai compte guide, sur téléphone, en mode avion, au quai.",
            "Le texte juridique de l'avocat en anglais : qui le traduit, et l'outil affiche-t-il la bonne version ?",
            "Le lien avec l'outil de réservation (Q1) : la décharge part-elle d'elle-même avec la confirmation ?",
            "Où sont hébergées les données de santé et combien de temps elles sont gardées (Loi 25).",
        ],
        "autres": [
            "◆ Bookeo, Rezgo et SimplyBook.me (Q1) offrent un formulaire de décharge dans la réservation. Une seule "
            "équipe l'a vu, sans le comparer aux besoins ci-dessus.",
        ],
    },
    {
        "titre": "Q3 — La plateforme du site",
        "besoin": "Mélanie modifie seule les prix, les horaires et les textes, en peu de temps. Le site s'affiche bien "
                  "sur téléphone, se charge vite, offre le français et l'anglais, et accueille la réservation, le "
                  "paiement et les formulaires. Le site actuel est sur Wix, dans un compte au nom du neveu.",
        "outils": ["Wix", "WordPress.com", "Squarespace"],
        "cases": {
            "Famille de solution": [
                "Constructeur de site hébergé (SaaS)",
                "Système de gestion de contenu, version hébergée par WordPress.com",
                "Constructeur de site hébergé (SaaS)",
            ],
            "Essayé par": ["2 équipes", "2 équipes", "2 équipes"],
            "Ce que les essais ont montré": [
                "Ajouter un administrateur : 2 min 25 s (R). Changer un prix : 53 s (R). Publier une image : "
                "1 min 37 s (R). Changer les heures du module de réservation : 3 min 31 s (R). Affichage correct sur "
                "téléphone et tablette (R). PageSpeed bureau : 90 (R). Paiement en ligne par plusieurs moyens. "
                "Formulaires exportables en PDF. HTTPS une fois publié.",
                "Ajouter un administrateur : 36 s (R). Publier une image : 1 min, en plusieurs étapes (R). "
                "Affichage correct sur téléphone (R). HTTPS (R). Page avec images lourdes : 2,6 s.",
                "Ajouter un administrateur : 51 s (R). Changer un prix : 45 s (R). Publier une image : 1 min 02 s "
                "(R). Courriel de confirmation de réservation reçu (R). Changer les heures de réservation : "
                "environ 5 min (R). Affichage correct sur téléphone (R). PageSpeed bureau : 90 (R). Liste des "
                "réservations du jour téléchargeable.",
            ],
            "Échecs et limites observés": [
                "PageSpeed mobile : 70, sous la cible de 90 (É). Aucun courriel de confirmation de réservation (É). "
                "Nombre de formulaires limité. Données d'un formulaire perdues en actualisant la page. Viator : "
                "aucune intégration directe, seulement un code à coller. Une autre équipe (Q5) a mis 16 min 56 s à "
                "ajouter quelques mots à une phrase dans l'éditeur.",
                "Changer un prix : plus de 5 min, le tableau disparaissait (É). Deux langues : extension Polylang "
                "nécessaire, trouvée avec de l'aide (É). Le forfait gratuit bloque toutes les extensions, dont la "
                "réservation.",
                "PageSpeed mobile : 62 (É). Réservation par Acuity Scheduling, un outil de plus. Viator : "
                "intégration possible, en plusieurs étapes. Essai gratuit limité à 30 min de vidéo.",
            ],
            "Ce que les essais n'ont pas couvert": [
                "Version bilingue (application à ajouter, voir Q5).",
                "Réservation (extension). Vitesse du site publié (site non publié).",
                "Vitesse avec de vraies vidéos (publication payante).",
            ],
            "Forfait retenu pour le calcul": [
                "Le forfait le moins cher qui accepte les paiements : 44 $ CA/mois. Le forfait d'entrée lu par une "
                "équipe (22 $ CA/mois) n'accepte pas les paiements. Aucuns frais de transaction de Wix.",
                "◆ Personal : 4 $ US/mois payé à l'année. C'est le forfait le moins cher qui permet d'installer des "
                "extensions (Polylang, réservation). Les forfaits plus chers ajoutent une boutique, inutile ici.",
                "◆ Core : 32 $ CA/mois payé à l'année. C'est le forfait le moins cher sans frais sur les ventes (le "
                "forfait Basic prend 2 % sur les ventes en ligne). 5 h de vidéo.",
            ],
            "Coût sur 3 ans ($ CA, hypothèses communes)": [
                "1 584 $",
                "199 $",
                "1 152 $\n+ 1 341 $ si la réservation passe par Acuity",
            ],
            "Temps pour apprendre (mesuré)": [
                "Tâches courantes : de 53 s à 3 min 31 s.",
                "Tâches courantes : de 36 s à plus de 5 min, avec de l'aide pour les extensions.",
                "Tâches courantes : de 45 s à environ 5 min.",
            ],
        },
        "calculs": [
            "Wix : 44 $ × 12 × 3 = 1 584 $. Mélanie paie aujourd'hui environ 300 $ par année pour son forfait Wix, "
            "qui n'accepte pas les paiements.",
            "WordPress.com Personal : 4 $ US × 36 × 1,38 = 199 $. Polylang (version gratuite) suffit pour deux "
            "langues; l'outil de réservation est celui de Q1.",
            "Squarespace Core : 32 $ × 36 = 1 152 $. ◆ Si la réservation passe par Acuity Scheduling plutôt que par "
            "l'outil de Q1 : forfait Growing (6 calendriers), 27 $ US × 36 × 1,38 = 1 341 $ de plus.",
            "Le nom de domaine (déjà acheté, à récupérer du neveu) n'est compté pour aucune plateforme.",
        ],
        "a_verifier": [
            "La vitesse sur téléphone une fois le site publié, avec la vidéo de la page d'accueil.",
            "Le transfert du site et du compte Wix actuels, au nom du neveu.",
            "Mélanie, seule, change un prix et un horaire en moins de 5 minutes sur la plateforme retenue.",
            "L'outil de réservation de Q1 intégré dans la page (code à coller ou extension).",
        ],
        "autres": [
            "WordPress.org (logiciel gratuit, hébergé ailleurs) : de 550 $ à 850 $ sur 3 ans pour l'hébergement, "
            "selon une équipe. Les mises à jour, la sécurité et les sauvegardes reviennent alors à l'entreprise.",
            "Shopify et un développement sur mesure n'ont été essayés par aucune équipe; ils restent possibles si "
            "vous dites pourquoi.",
        ],
    },
    {
        "titre": "Q4 — Montrer les vidéos sans ralentir le site",
        "besoin": "Une vidéo plein écran qui démarre seule et joue en boucle à l'ouverture de la page d'accueil, sans "
                  "ralentir la page, même sur un réseau moyen, et que Mélanie peut remplacer elle-même. Patrick a "
                  "environ 60 Go de vidéos 4K. L'entreprise a déjà Google Workspace (3 comptes).",
        "outils": ["Wix Video", "Vimeo", "Google Drive"],
        "cases": {
            "Famille de solution": [
                "Fonction de la plateforme (Wix)",
                "Service spécialisé d'hébergement vidéo (SaaS)",
                "Stockage de fichiers déjà payé (Google Workspace)",
            ],
            "Essayé par": ["1 équipe"] * 3,
            "Ce que les essais ont montré": [
                "LCP mobile (PageSpeed) : 1,5 s (R). Image ni saccadée ni pixellisée (R). Démarrage : 1 s (R). "
                "Pleine largeur dès l'ouverture (R). Remplacer la vidéo : 4 ou 5 clics; téléversement de 25 s pour "
                "une vidéo 4K de 34,1 Mo (R). Image de secours possible pour les téléphones.",
                "LCP mobile : 0,8 s (R). Image ni saccadée ni pixellisée (R). Démarrage : 1,56 s, délai visible "
                "(R). Pleine largeur sur ordinateur, iPad et iPhone (R). Code d'intégration ou lien en 1 clic; "
                "lecture automatique et boucle en 1 clic.",
                "LCP mobile : 0,8 s (R). Image ni saccadée ni pixellisée (R). Pleine largeur sur les 3 appareils "
                "(R). Téléversement en moins de 1 min, lien de partage en environ 5 clics.",
            ],
            "Échecs et limites observés": [
                "Un premier essai, sur un autre ordinateur, a donné un LCP de 10,7 s; le second, 1,5 s. Recadrage "
                "au centre selon l'orientation du téléphone : les côtés de l'image sont coupés. Utilisable seulement "
                "si le site est sur Wix.",
                "Téléverser 35 Mo : 2 min et une dizaine de clics sans aide (P).",
                "Aucun démarrage automatique ni lecture en boucle : le visiteur doit cliquer (É); un code d'erreur "
                "apparaît quand on essaie de le forcer. Intégration manuelle.",
            ],
            "Ce que les essais n'ont pas couvert": [
                "◆ Wix ne publie pas de limite en heures de vidéo : les vidéos comptent dans l'espace de stockage "
                "du forfait.",
                "Intégration au site retenu (Q3). ◆ Le mode arrière-plan (lecture automatique, muette, en boucle, "
                "sans commandes) et la restriction de la vidéo au domaine du site sont réservés aux forfaits payants.",
                "◆ Google Drive n'est pas conçu pour diffuser une vidéo dans une page : aucune autre méthode de "
                "démarrage automatique n'est offerte.",
            ],
            "Forfait retenu pour le calcul": [
                "Inclus dans le forfait Wix de Q3.",
                "Abonnement : 27 $ CA/mois, 3 utilisateurs, stockage suffisant pour 60 Go selon l'équipe.",
                "◆ Inclus dans Google Workspace Business Starter, déjà payé : 30 Go par compte, mis en commun "
                "(90 Go pour les 3 comptes, courriels compris).",
            ],
            "Coût sur 3 ans ($ CA, hypothèses communes)": [
                "0 $ en plus du forfait Wix",
                "972 $",
                "0 $",
            ],
            "Temps pour apprendre (mesuré)": [
                "2 min 11 s",
                "2 min (téléversement) + 42 s (code d'intégration)",
                "Moins de 1 min 35 s (téléversement et lien)",
            ],
        },
        "calculs": [
            "Vimeo : 27 $ × 36 mois = 972 $.",
            "Google Drive : 0 $. Les vidéos du site, une fois préparées (section 9), pèsent bien moins que les "
            "90 Go partagés du forfait Business Starter. ◆ Garder les 60 Go de vidéos 4K originales dans Drive "
            "demanderait Business Standard (2 To par compte) : (18,40 $ − 9,20 $) × 3 comptes × 36 mois = 994 $ "
            "de plus.",
            "Les essais ont utilisé une vidéo de 34,1 Mo. Les 60 Go de Patrick doivent d'abord être préparés : "
            "c'est la section 9 du rapport, pas un choix d'hébergement.",
            "◆ Chrome, Safari et Firefox ne lancent automatiquement qu'une vidéo sans son : la vidéo d'accueil est "
            "muette, peu importe l'outil.",
        ],
        "a_verifier": [
            "Le LCP mobile de la page d'accueil avec la vraie vidéo, sur un réseau 4G lent, sur la plateforme "
            "retenue (Q3).",
            "Ce que voit un visiteur sur téléphone quand la lecture automatique est bloquée (image de secours).",
            "Mélanie remplace la vidéo seule, en moins de 5 minutes.",
        ],
        "autres": [
            "◆ YouTube (gratuit) n'a pas été essayé. Le lecteur intégré affiche toujours le logo YouTube et, à la "
            "fin, des suggestions de vidéos : il ne convient pas à une vidéo d'arrière-plan sans commandes.",
            "Un fichier vidéo court et compressé, téléversé directement sur la plateforme du site, est une autre "
            "façon de faire : à mesurer de la même façon.",
        ],
    },
    {
        "titre": "Q5 — Offrir le site en français et en anglais",
        "besoin": "Le visiteur choisit le français ou l'anglais sur chaque page; toutes les pages, les formulaires, la "
                  "réservation et les courriels existent dans les deux langues. Mélanie met à jour les deux versions "
                  "seule, rapidement, et les noms propres (rabaska, via ferrata, prêt-à-camper) ne sont pas traduits.",
        "outils": ["Wix Multilingual", "ConveyThis", "WebLang", "Google Traduction", "DeepL"],
        "cases": {
            "Famille de solution": [
                "Fonction de la plateforme (Wix)",
                "Service spécialisé ajouté au site",
                "Service spécialisé, extension de Wix Multilingual",
                "Service externe de traduction automatique",
                "Outil de traduction : textes copiés à la main",
            ],
            "Essayé par": ["2 équipes", "1 équipe", "1 équipe", "1 équipe", "1 équipe"],
            "Ce que les essais ont montré": [
                "Changer un prix : 1 min 30 s, l'anglais suit (R). Paragraphe avec 4 mots difficiles traduit en "
                "1 min (R). Changer de langue sur téléphone : 1 ou 2 touchers (R). Au clavier : 6 Tab, focus "
                "visible (R). Mots protégés de la traduction (R). 4 pages sur 4 ont leur adresse /en (R). Nouvelle "
                "page traduite d'elle-même en 30 s (R). Export CSV des traductions obtenu par les deux équipes, en "
                "40 s et en 30 s.",
                "Changer un prix : 1 min 52 s, l'anglais suit (R). Paragraphe traduit en 1 min (R). Changer de "
                "langue : 1 clic, 5 s (R). Au clavier : 18 s (R). Nouvelle page traduite d'elle-même en 20 s (R). "
                "PageSpeed mobile : 76 (fr), 81 (en).",
                "Changer de langue sur téléphone : 2 touchers (R). Au clavier : 1 Tab, focus visible (R). Mots "
                "protégés (R). Aucun mot resté en français sur l'accueil (R). Chargement égal dans les deux langues.",
                "Changer de langue : 1 toucher (R). Au clavier : 1 Tab, focus visible (R). Chargement égal dans les "
                "deux langues.",
                "Changer un prix : 1 min 15 s (R). Paragraphe traduit en 1 min 15 s, par copier-coller (R). Changer "
                "de langue : 1 clic (R). Au clavier : 12 s (R).",
            ],
            "Échecs et limites observés": [
                "Ajouter quelques mots à une phrase : 16 min 56 s, au moins 5 blocages, faute de savoir où cliquer "
                "dans l'éditeur (É, une équipe). 61 mots restés en français sur la page d'accueil (É). Fichier CSV "
                "jugé illisible à l'ouverture par une équipe; l'autre l'a lu (◆ le fichier est fait pour être "
                "traduit puis réimporté dans Wix). PageSpeed mobile : 59 (fr), 47 (en). Traduction automatique à "
                "relire.",
                "Le texte français s'affiche une fraction de seconde avant l'anglais (panier). Export des "
                "traductions réservé au forfait payant.",
                "Texte ajouté en français absent de la version anglaise, même après actualisation : 14 min, "
                "7 blocages (É). Aucune page n'a sa propre adresse /en (É). Export introuvable. Ne fonctionne "
                "qu'avec Wix Multilingual.",
                "Texte ajouté en français absent de la version anglaise (É); plus de 5 min pour changer un mot. "
                "67 mots restés en français sur l'accueil (É). Impossible de protéger « rabaska » (É).",
                "Nouvelle page : 5 min 30 s à la main (É). Rien à exporter : les traductions ne sont pas gardées "
                "(É). Chaque changement se refait à la main dans les deux langues.",
            ],
            "Ce que les essais n'ont pas couvert": [
                "Réservation, paiement et courriel de confirmation en anglais (forfait payant requis).",
                "Courriel de confirmation en anglais (aucun service de courriel relié au site d'essai).",
                "Réservation et paiement en anglais.",
                "Export. ◆ Google n'offre plus son module de traduction aux nouveaux sites depuis décembre 2019, "
                "sauf aux organismes publics et sans but lucratif; le code encore en circulation fonctionne, sans "
                "soutien ni garantie de durée.",
                "Courriel de confirmation en anglais.",
            ],
            "Forfait retenu pour le calcul": [
                "Application gratuite; 3 000 mots de traduction automatique offerts, puis un forfait de "
                "10 000 mots à 7,50 $, payé une seule fois. Forfait Wix requis.",
                "◆ Starter : 120 $ US/an (1 langue ajoutée, 60 000 mots). Le forfait gratuit (10 000 mots) est "
                "limité à 2 500 pages vues par mois, trop peu en été.",
                "◆ Landing : 4,16 $ US/mois payé à l'année (2 langues, 8 000 mots par mois). Wix Multilingual "
                "requis.",
                "Gratuit.",
                "◆ Version gratuite : 50 000 caractères par mois, assez pour le site d'environ 8 000 mots et ses "
                "mises à jour.",
            ],
            "Coût sur 3 ans ($ CA, hypothèses communes)": [
                "7,50 $, en plus du forfait Wix",
                "497 $",
                "207 $",
                "0 $",
                "0 $",
            ],
            "Temps pour apprendre (mesuré)": [
                "Tâches courantes : de 30 s à 1 min 30 s pour une équipe; 16 min 56 s pour ajouter quelques mots "
                "pour l'autre.",
                "Tâches courantes : de 20 s à 1 min 52 s.",
                "32 min 28 s pour comprendre l'outil.",
                "Non mesuré par l'équipe.",
                "Tâches courantes : de 1 min 15 s à 5 min 30 s.",
            ],
        },
        "calculs": [
            "Site d'environ 8 000 mots, une langue ajoutée (l'anglais).",
            "Wix Multilingual : 3 000 mots gratuits, puis un forfait de 10 000 mots à 7,50 $, payé une fois.",
            "ConveyThis : 120 $ US × 1,38 = 165,60 $ par année × 3 = 497 $.",
            "WebLang Landing : 4,16 $ US × 36 × 1,38 = 207 $. ◆ Si le site dépasse 8 000 mots par mois, le forfait "
            "suivant (Freelancer, 10 $ US/mois, 25 000 mots) coûte 497 $ sur 3 ans.",
            "DeepL : 0 $. ◆ Le premier passage du site entier (environ 50 000 caractères) atteint la limite d'un "
            "mois; il se fait sur deux mois.",
            "La traduction par une personne (la décharge, les conditions) n'est comptée pour aucun outil.",
        ],
        "a_verifier": [
            "Le parcours complet en anglais : réservation, paiement, courriel de confirmation et décharge (Q1, Q2).",
            "Ce qui se passe dans la version anglaise quand Mélanie change un texte en français.",
            "Le nombre de mots restés en français sur chaque page, avec l'outil et la plateforme retenus.",
            "Qui relit la traduction automatique, et combien de temps ça prend chaque printemps.",
        ],
        "autres": [
            "Weglot et la traduction par une personne (famille : sur mesure) n'ont été essayés par aucune équipe.",
        ],
    },
]

# ---------------------------------------------------------------------------
# Mise en forme
# ---------------------------------------------------------------------------

def vider(doc):
    corps = doc.element.body
    for enfant in list(corps):
        if enfant.tag != qn("w:sectPr"):
            corps.remove(enfant)


def paysage(doc):
    for section in doc.sections:
        largeur, hauteur = section.page_width, section.page_height
        if largeur < hauteur:
            section.orientation = WD_ORIENT.LANDSCAPE
            section.page_width, section.page_height = hauteur, largeur
        section.left_margin = section.right_margin = Cm(1.5)
        section.top_margin = section.bottom_margin = Cm(1.5)


def ombrer(cellule, couleur):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), couleur)
    cellule._tc.get_or_add_tcPr().append(shd)


def repeter_entete(rangee):
    tr_pr = rangee._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    tr_pr.append(el)


def ecrire(paragraphe, texte, taille=None, gras=False):
    """Écrit le texte; la partie qui commence par ◆ (ajout de l'enseignant) est en gris italique."""
    morceaux = texte.split("◆")
    for i, morceau in enumerate(morceaux):
        if not morceau:
            continue
        run = paragraphe.add_run(("◆" + morceau) if i > 0 else morceau)
        run.bold = gras
        if taille:
            run.font.size = taille
        if i > 0:
            run.italic = True
            run.font.color.rgb = GRIS


def consigne(doc, texte):
    run = doc.add_paragraph().add_run(texte)
    run.italic = True
    run.font.color.rgb = GRIS


def puces(doc, elements):
    for texte in elements:
        p = doc.add_paragraph(style="List Bullet")
        ecrire(p, texte)


def tableau_question(doc, q):
    outils = q["outils"]
    t = doc.add_table(rows=1 + len(LIGNES), cols=1 + len(outils))
    t.style = "Table Grid"
    t.autofit = False
    section = doc.sections[-1]
    utile = section.page_width - section.left_margin - section.right_margin
    largeur_critere = Cm(3.2)
    largeur_outil = int((utile - largeur_critere) / len(outils))
    entete = t.rows[0]
    repeter_entete(entete)
    for j, titre in enumerate(["Critère"] + outils):
        c = entete.cells[j]
        ecrire(c.paragraphs[0], titre, TAILLE_TABLEAU, gras=True)
        ombrer(c, BLEU_ENTETE)
    for i, ligne in enumerate(LIGNES, start=1):
        rangee = t.rows[i]
        ecrire(rangee.cells[0].paragraphs[0], ligne, TAILLE_TABLEAU, gras=True)
        ombrer(rangee.cells[0], GRIS_CRITERE)
        for j, texte in enumerate(q["cases"][ligne], start=1):
            parties = texte.split("\n")
            ecrire(rangee.cells[j].paragraphs[0], parties[0], TAILLE_TABLEAU)
            for suite in parties[1:]:
                ecrire(rangee.cells[j].add_paragraph(), suite, TAILLE_TABLEAU)
    for rangee in t.rows:
        rangee.cells[0].width = largeur_critere
        for c in rangee.cells[1:]:
            c.width = largeur_outil
    return t


def saut(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def generer():
    for q in QUESTIONS:
        for ligne in LIGNES:
            assert len(q["cases"][ligne]) == len(q["outils"]), (q["titre"], ligne)

    doc = Document(SOURCE)
    vider(doc)
    paysage(doc)

    doc.add_paragraph("Tableaux de comparaison communs", style="Title")
    doc.add_paragraph("Les essais de toutes les équipes, question par question")
    doc.add_paragraph("582-A05-RI — Analyse et conception Web — Base commune pour l'évaluation 2, section 8.2")

    doc.add_heading("À quoi servent ces tableaux", level=1)
    doc.add_paragraph(
        "Chaque équipe a essayé les outils d'une seule question. Ces tableaux regroupent les essais de toutes les "
        "équipes pour que chacune parte de la même base pour les cinq questions. Les coûts sur trois ans ont été "
        "recalculés avec les mêmes hypothèses, pour qu'on puisse les comparer d'un outil à l'autre.")
    puces(doc, [
        "Pour votre question, vos propres essais et votre annexe A restent votre première source. Si vos résultats "
        "diffèrent de ceux du tableau, dites-le et expliquez pourquoi.",
        "Pour les quatre autres questions, citez ces tableaux comme source : « Tableaux de comparaison communs, "
        "essais des équipes du groupe, octobre 2026 ».",
        "Vous pouvez ajouter un outil, à condition de dire pourquoi et sur quoi repose l'information.",
        "Les tableaux décrivent; ils ne choisissent rien. Le choix, c'est votre section 8.2.",
    ])

    doc.add_heading("Comment lire les tableaux", level=1)
    puces(doc, [
        "R = réussi, É = échoué, P = partiel, NV = non vérifiable : le résultat d'un essai, selon le critère "
        "« Réussi si… » de l'équipe qui l'a fait. Les critères n'étaient pas les mêmes d'une équipe à l'autre.",
        "« Essayé par » donne le nombre d'équipes qui ont essayé l'outil. Un outil essayé par une seule équipe "
        "repose sur un seul essai.",
        "◆ Le texte en gris italique qui commence par ce symbole a été ajouté par l'enseignant pour combler une "
        "information que les essais n'ont pas donnée. Il vient de la documentation du fournisseur, lue le "
        "17 novembre 2026. Ce n'est pas un résultat d'essai : citez-le comme « documentation du fournisseur ».",
        "Les autres prix ont été lus par les équipes en octobre 2026. Chaque outil a un seul forfait retenu et un "
        "seul coût : la ligne « Forfait retenu pour le calcul » dit lequel et pourquoi.",
        "Quand deux équipes ont obtenu des résultats différents pour le même outil, la case dit ce que chacune a "
        "mesuré.",
    ])

    doc.add_heading("Les hypothèses communes du coût sur trois ans", level=1)
    puces(doc, [
        "1 $ US = 1,38 $ CA (taux de l'activité 2 de la séance 4). Si vous utilisez un autre taux dans votre "
        "rapport, refaites les calculs des outils en $ US.",
        "1 800 réservations en ligne par année, à 120 $ en moyenne : 216 000 $ réservés en ligne par année "
        "(activité 2).",
        "9 000 participants par été, donc 9 000 décharges (document 3 du mandat), réparties sur la saison : "
        "juin 1 800, juillet 3 000, août 3 000, septembre 800, octobre 400. Aucune de novembre à mai.",
        "Le forfait choisi est le moins cher qui couvre ces volumes. Quand l'outil permet de changer de forfait "
        "chaque mois, le calcul suit la saison.",
        "4 utilisateurs pour les outils de réservation; 3 comptes Google Workspace (Mélanie, Patrick, info@), au "
        "forfait Business Starter, le forfait de base (le mandat ne précise pas le forfait).",
        "Un site d'environ 8 000 mots, traduit en anglais.",
        "Tous les montants sont avant taxes, sans les frais de traitement des cartes et sans le nom de domaine.",
        "Les prix et les volumes restent les mêmes pendant les trois ans; on paie à l'année quand l'outil "
        "l'offre.",
    ])

    for q in QUESTIONS:
        saut(doc)
        doc.add_heading(q["titre"], level=1)
        p = doc.add_paragraph()
        p.add_run("Le besoin : ").bold = True
        p.add_run(q["besoin"])
        tableau_question(doc, q)
        doc.add_heading("Le calcul du coût sur trois ans", level=3)
        puces(doc, q["calculs"])
        doc.add_heading("Ce qu'aucune équipe n'a pu essayer", level=3)
        puces(doc, q["a_verifier"])
        doc.add_heading("Autres outils, non essayés", level=3)
        puces(doc, q["autres"])

    doc.save(SORTIE)
    print(f"Tableaux écrits : {SORTIE}")


if __name__ == "__main__":
    generer()
