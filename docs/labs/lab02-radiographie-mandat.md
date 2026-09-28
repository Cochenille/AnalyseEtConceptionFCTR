---
title: "Lab 02 — Radiographie du mandat"
aside: false
---

# Lab 02 — Radiographie du mandat

<div class="bg-blue-50 border border-blue-200 text-blue-900 rounded-lg p-4 mb-5">
<strong>Objectifs du laboratoire</strong><br>
<ul class="list-disc pl-5">
  <li>Relever <strong>toutes</strong> les contraintes d'un mandat réel et les classer.</li>
  <li>Traduire les demandes du client en exigences fonctionnelles et non fonctionnelles.</li>
  <li>Évaluer des risques selon leurs chances d'arriver et leurs conséquences, et proposer des mesures.</li>
  <li>Dresser la liste des problèmes techniques à prévoir.</li>
</ul>
</div>

<div class="bg-yellow-50 border border-yellow-200 text-yellow-900 rounded-lg p-4 mb-5">
<strong>Modalités</strong><br>
<ul class="list-disc pl-5">
  <li>Avec <strong>votre équipe de la session</strong> (2 ou 3 personnes).</li>
  <li>Durée : environ 55 minutes, puis correction commentée en grand groupe.</li>
  <li>Remise : la fiche remplie, déposée dans l'<strong>équipe Teams du cours</strong>. Ce travail est <strong>formatif</strong> (non noté)… mais c'est la base de votre <strong>évaluation 1</strong>. Gardez-le précieusement.</li>
</ul>
</div>

---

## Contexte

Studio Web FC, c'est vous. Aventure Saint-Maurice vous a confié son projet et vous devez produire un rapport de faisabilité.
Avant de penser à une seule solution, un analyste fait la **radiographie** du mandat : il relève tout ce qui limite le projet, tout ce qu'il doit faire et tout ce qui pourrait mal tourner.

> **Règle d'or du lab :** on ne propose **aucune solution** aujourd'hui. Pas de « on prendrait WordPress », pas de « il faudrait Shopify ». On décrit la situation. Les choix viendront plus tard.

---

## Préparation (5 min) {#preparation}

<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text">Ouvrir le <a href="./../mandat/" target="_blank">mandat Aventure Saint-Maurice</a> dans un onglet</span></label></li>
  <li><label><input type="checkbox"><span class="check-text"><a href="./../fiches/lab02-fiche-radiographie.docx" download>Télécharger la fiche de radiographie (Word)</a> et la placer dans le dossier partagé de l'équipe</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Se répartir la lecture : une personne par document (courriel, notes, chiffres), puis chacun résume le sien aux autres en deux minutes</span></label></li>
</ul>

---

## Partie 1 — Les contraintes (20 min) {#partie-1}

Relevez **au moins 15 contraintes** dans le mandat. Pour chacune, remplissez une ligne du tableau de la fiche.

| Colonne | Ce qu'on y écrit |
|:--|:--|
| **Contrainte** | La contrainte, dans vos mots, en une phrase |
| **Source** | Le document et un court extrait qui la prouve |
| **Sorte** | **T** (technique), **O** (organisationnelle) ou **R** (ressources) |
| **Élément** | Budget, délai, personnel, technologie ou loi |

<div class="bg-slate-50 border border-slate-200 text-slate-800 rounded-lg p-4 mb-5">
<strong>Pour ne rien oublier, cherchez dans chaque catégorie</strong><br>
<ul class="list-disc pl-5">
  <li><strong>Budget :</strong> construction, coûts annuels, commissions, subvention.</li>
  <li><strong>Délai :</strong> dates fermes, dates souhaitées, saisons.</li>
  <li><strong>Personnel :</strong> qui construit, qui entretient, compétences, disponibilité selon la saison.</li>
  <li><strong>Technologie :</strong> les outils qui existent déjà, les comptes, les accès, le réseau sur place.</li>
  <li><strong>Lois et règles :</strong> renseignements personnels, langue, accessibilité, assurance.</li>
</ul>
</div>

<div class="bg-red-50 border border-red-300 text-red-900 rounded-lg p-4 mb-5">
<strong>Une contrainte n'est pas un souhait</strong><br>
« Le client veut une vidéo plein écran » est un souhait. « Le site doit bien s'afficher avec un réseau cellulaire faible » est une contrainte. Si vous hésitez, demandez-vous : <em>est-ce que ça limite nos choix ?</em>
</div>

---

## Partie 2 — Les exigences (10 min) {#partie-2}

### Ce que le site doit faire
Dressez la liste d'au moins **8 exigences fonctionnelles**. Écrivez-les sous la forme : **« [Qui] peut [faire quoi]. »**

> *Exemple :* Un client peut voir les places qui restent pour un départ de via ferrata.

Pensez à tous les utilisateurs : le client, le parent, le responsable d'un groupe, Karine à l'accueil, les guides, Mélanie.

### Comment il doit le faire
Pour **chacune des cinq catégories** vues en classe, écrivez **une exigence précise** tirée du mandat.

| Catégorie | Votre exigence |
|:--|:--|
| Vitesse | |
| Sécurité | |
| Accessibilité | |
| Loi 25 et langue | |
| Navigateurs et appareils | |

---

## Partie 3 — Les risques (15 min) {#partie-3}

### 1. Placer les risques
Voici dix risques du projet. Placez chacun dans la matrice selon **ses chances d'arriver** et **ses conséquences**. Discutez en équipe : vous devez être capables de justifier chaque placement.

<MatriceRisques />

### 2. Compléter
Dans la fiche :
<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text">Reportez la position de chaque risque (p. ex. R3 : moyenne / graves)</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Ajoutez <strong>deux risques</strong> que la liste a oubliés : un technique et un organisationnel</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Pour chaque risque de la <strong>zone rouge</strong>, proposez une <strong>mesure</strong> qui le réduit</span></label></li>
</ul>

<div class="bg-slate-50 border border-slate-200 text-slate-800 rounded-lg p-4 mb-5">
<strong>Une mesure n'est pas une solution technique</strong><br>
« Fixer une date limite pour la remise des photos » est une mesure. « Prendre FareHarbor » est une solution : gardez-la pour l'évaluation 2.
</div>

---

## Partie 4 — Les problèmes techniques à prévoir (10 min) {#partie-4}

Choisissez les **cinq problèmes techniques** qui vous inquiètent le plus. Pour chacun :

| Problème | Pourquoi c'est un problème | Ce qu'il faut vérifier ou demander |
|:--|:--|:--|
| | | |

Vous pouvez vous inspirer de l'activité des cinq phrases, mais trouvez-en **au moins deux autres**.

---

## Défi bonus

Mélanie a écrit : « Est-ce que c'est faisable ? »
Rédigez la réponse que vous lui enverriez **ce soir**, en **cinq lignes maximum**, sans aucun mot technique. Vous ne pouvez pas encore dire oui ou non : que lui dites-vous ?

---

## Remise

<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text">Au moins 15 contraintes, chacune avec sa source, sa sorte et son élément</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Au moins 8 exigences fonctionnelles et une exigence par catégorie non fonctionnelle</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Les 10 risques placés, 2 risques ajoutés, une mesure pour chaque risque de la zone rouge</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Cinq problèmes techniques à prévoir</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Le fichier est nommé <code>lab02-equipeN-nom1-nom2.docx</code> et déposé dans l'équipe Teams du cours</span></label></li>
</ul>

---

## Correction commentée

En grand groupe, on bâtit ensemble :
- la liste complète des contraintes, chaque équipe ajoutant celles que les autres n'ont pas trouvées ;
- la matrice des risques de la classe : on compare les placements et on discute des désaccords ;
- les trois problèmes techniques qui reviennent le plus souvent.

Corrigez votre fiche au fil de la discussion, **dans une autre couleur**. Elle vous servira pour l'évaluation 1.
