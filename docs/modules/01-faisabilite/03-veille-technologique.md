---
title: "Séance 3 — La veille technologique"
aside: false
---

# Séance 3 — La veille technologique

## Objectifs
- Trouver de l'information fiable sur le Web et reconnaître une **publicité déguisée en comparatif**.
- Lire une **grille de prix** : ce qui se paie au mois, à l'utilisateur ou à la transaction.
- Préparer l'**essai rigoureux** d'un outil : les mêmes manipulations, dans les mêmes conditions, sur chaque solution.
- Comprendre ce qu'on attend dans l'**évaluation 1**.

## Déroulement de la séance

| Heure | Activité |
|:--|:--|
| 18 h 30 | Retour sur le Lab 02 : ce qu'on garde pour l'évaluation 1 |
| 18 h 40 | [L'énoncé de l'évaluation 1](./../../evaluations/evaluation-1) |
| 19 h 05 | La veille technologique : où chercher, à qui se fier |
| 19 h 20 | Activité 1 — Dix sources à classer (en équipe) |
| 19 h 45 | Retour en grand groupe |
| 20 h 00 | Pause |
| 20 h 15 | Lire une grille de prix · Activité 2 — Trois outils, trois factures |
| 20 h 45 | Essayer un outil de façon rigoureuse |
| 21 h 00 | Tirage des questions · [Lab 03 — Le plan d'essai](./../../labs/lab03-plan-essai) (en équipe) |
| 21 h 50 | Ce qu'il faut avoir fait avant la séance 4 |

---

## Retour sur le Lab 02

La radiographie du mandat est terminée : vous savez **ce que le projet exige**, **ce qui le limite** et **ce qui pourrait mal tourner**. Ce soir, on ouvre la deuxième moitié du travail d'analyste : **quelles technologies existent** pour répondre à ces besoins ?

<div class="bg-blue-50 border border-blue-200 text-blue-900 rounded-lg p-4 mb-5">
<strong>Les trois constats de la correction commentée</strong><br>
<ul class="list-disc pl-5">
  <li><strong>Les coûts annuels sont partout et personne ne les a chiffrés.</strong> Ce soir, on apprend à les lire dans une grille de prix.</li>
  <li><strong>Viator, Square, Google Workspace et le nom de domaine existent déjà.</strong> Tout outil qu'on regarde doit composer avec eux.</li>
  <li><strong>Le réseau est faible au quai.</strong> Un outil qui fonctionne parfaitement au bureau peut échouer là où on en a besoin. Seul un essai peut le révéler.</li>
</ul>
</div>

---

## L'évaluation 1

L'énoncé complet est sur sa propre page : **[Évaluation 1 — Rapport de faisabilité technique : évaluation technique](./../../evaluations/evaluation-1)**.

<div class="bg-yellow-50 border border-yellow-200 text-yellow-900 rounded-lg p-4 mb-5">
<strong>En bref</strong><br>
<ul class="list-disc pl-5">
  <li>Un rapport qui <strong>décrit la situation</strong> du projet Aventure Saint-Maurice : exigences, contraintes, risques et <strong>technologies possibles</strong>. Il ne recommande encore rien.</li>
  <li>En équipe, remise le <strong>11 novembre</strong> sur LÉA. 20 % de la note finale, dont 10 % pour le français.</li>
  <li>Le Lab 02 vous a donné les trois premières parties. Les séances 3 et 4 vous donnent la quatrième : les technologies.</li>
</ul>
</div>

---

## La veille technologique

Faire de la veille, c'est **suivre ce qui existe et ce qui change** dans son domaine. Dans un projet, c'est plus précis : on cherche les outils qui pourraient répondre à un besoin, puis on vérifie ce qu'ils valent vraiment.

Le problème : sur le Web, une bonne partie de l'information sur les outils est écrite par **ceux qui les vendent**, ou par des gens **payés quand vous les achetez**.

### Où chercher

| Type de source | Exemples | À quoi elle sert |
|:--|:--|:--|
| **Documentation de référence** | MDN Web Docs, W3C, Can I use | Comprendre une technologie, vérifier ce qu'un navigateur supporte |
| **Organismes officiels** | Commission d'accès à l'information, Office québécois de la langue française | Connaître les obligations légales |
| **Documentation de l'outil** | Centre d'aide, page des prix, conditions d'utilisation | Savoir ce que l'outil **prétend** faire, et à quel prix |
| **Témoignages d'utilisateurs** | Forums, Reddit, groupes d'entrepreneurs, sites d'avis | Découvrir les problèmes que le vendeur ne mentionne pas |
| **Comparatifs** | Articles « les 10 meilleurs… », vidéos « j'ai testé… » | Trouver des noms d'outils… et c'est tout, tant qu'on n'a pas vérifié qui paie |
| **Assistants d'IA** | ChatGPT, Copilot, Claude | Trouver des pistes et du vocabulaire. Jamais une source en soi : tout est à vérifier |

#### Exemples réels : des sources fiables

Ouvrez chaque lien et cherchez **qui parle**, **la date** et **l'absence de produit à vendre**.

| Source | Ce qu'il faut remarquer |
|:--|:--|
| [MDN — Formats d'image](https://developer.mozilla.org/fr/docs/Web/Media/Guides/Formats/Image_types) | En bas de page : la date de modification et l'historique des contributions. On sait qui a écrit quoi, et quand. |
| [Can I use — AVIF](https://caniuse.com/avif) | Une case par navigateur et par version, le pourcentage d'utilisateurs couverts, les sources dans l'onglet « Resources ». |
| [CAI — Principaux changements de la Loi 25](https://www.cai.gouv.qc.ca/protection-renseignements-personnels/sujets-et-domaines-dinteret/principaux-changements-loi-25) | L'organisme qui applique la loi explique chaque obligation et sa date d'entrée en vigueur. |
| [W3C — Introduction à l'accessibilité](https://www.w3.org/WAI/fundamentals/accessibility-intro/fr) | Publié par l'organisme qui écrit les normes. En bas : date, auteurs, traducteurs. |
| [OQLF — Une entreprise condamnée pour son site](https://www.oqlf.gouv.qc.ca/office/communiques/2021/20210709_infraction-cible-jeu.aspx) | Un vrai cas : une amende parce que le site n'était pas en français. Utile pour la Q5. |

Un piège vécu en préparant ce cours : la page de l'OQLF sur les sites Web sort encore dans Google, mais elle a été retirée. Une source officielle peut disparaître : notez toujours **la date de consultation**, et repartez de la [page Entreprises de l'OQLF](https://www.oqlf.gouv.qc.ca/francisation/entreprises/).

### Les cinq questions à poser à une source

1. **Qui parle ?** Un organisme, un expert identifié, un vendeur, un anonyme ?
2. **Quand ?** Une page de 2021 sur les prix ou les lois est probablement périmée.
3. **Qui paie ?** Y a-t-il une commandite, des liens d'affiliation, un bouton « Essai gratuit » à chaque paragraphe ?
4. **Sur quoi s'appuie-t-elle ?** Des essais décrits, des chiffres, des sources citées… ou des impressions ?
5. **Est-ce confirmé ailleurs ?** Une information qu'on ne retrouve dans aucune autre source indépendante reste à vérifier.

### Reconnaître une publicité déguisée en comparatif

<div class="bg-red-50 border border-red-300 text-red-900 rounded-lg p-4 mb-5">
<strong>Les indices qui doivent allumer une lumière</strong><br>
<ul class="list-disc pl-5">
  <li>Le comparatif est publié <strong>par l'un des outils comparés</strong>… qui arrive premier.</li>
  <li>Les liens vers les outils contiennent <code>?ref=</code>, <code>?aff=</code>, <code>?via=</code> ou <code>partner</code> : l'auteur touche une commission.</li>
  <li>Une phrase en petits caractères : « Nous pouvons recevoir une rémunération… », « Cette vidéo est commanditée par… ».</li>
  <li>Aucun défaut n'est mentionné pour le gagnant, et aucun essai n'est décrit.</li>
  <li>Le texte est le même, à quelques mots près, sur plusieurs sites.</li>
</ul>
Un comparatif publicitaire n'est pas inutile : il donne des <strong>noms d'outils</strong> à explorer. Mais il ne peut jamais servir de preuve dans un rapport.
</div>

#### Exemples réels : trois publicités déguisées

Trois vraies pages sur des outils qui pourraient servir à Aventure Saint-Maurice. Retrouvez les indices de l'encadré rouge.

| Page | Ce qu'il faut remarquer |
|:--|:--|
| [« Best booking software for tour operators »](https://www.peekpro.com/blog/best-booking-software-for-tour-operators) — blogue de Peek Pro | Regardez l'adresse : qui arrive premier ? Comptez les boutons « Request Demo ». Les autres outils nommés restent de bonnes pistes. |
| [« FareHarbor pricing guide »](https://www.trekksoft.com/en/blog/fareharbor-pricing-guidewhat-to-know-before-you-buy) — blogue de TrekkSoft | Un guide des prix de FareHarbor écrit par un concurrent. Devinez qui est le moins cher dans son tableau. |
| [« Best website builders for small business »](https://tech.co/website-builders/best-website-builders-for-small-business) — tech.co | Auteur nommé et page datée, mais avis de commission. Survolez un lien vers Wix : il passe par `tech.co/go/…`, ce qui permet au site d'enregistrer votre clic et de toucher une commission si vous vous abonnez. |

**Essayez-le :** cherchez *FareHarbor pricing* dans Google. Parmi les dix premiers résultats, combien viennent de FareHarbor ? Combien de concurrents ? Combien de sites de comparaison (Capterra, G2, GetApp) ?

**Pour trouver de vrais témoignages :** `site:reddit.com FareHarbor problems` ne montre que les discussions Reddit. Vérifiez la date de chaque message et si quelqu'un dans le fil travaille pour l'outil.

---

## Activité 1 — Dix sources à classer

<div class="bg-blue-50 border border-blue-200 text-blue-900 rounded-lg p-4 mb-5">
<strong>Consigne (25 min, en équipe)</strong><br>
Votre équipe cherche de l'information pour le projet Aventure Saint-Maurice et tombe sur les dix sources ci-dessous.
<ol class="list-decimal pl-5">
  <li>Pour chacune, écrivez votre <strong>justification</strong> en une phrase : quel indice vous a fait trancher ?</li>
  <li>Classez-la : <strong>fiable</strong>, <strong>à vérifier</strong> ou <strong>publicitaire</strong>. La réponse s'affiche après votre choix.</li>
  <li>À la fin, cliquez sur « Copier nos réponses » et collez-les dans le document de votre équipe.</li>
</ol>
</div>

<TriSources />

**Ce qu'il faut retenir :** « fiable » ne veut pas dire « vrai pour toujours », et « publicitaire » ne veut pas dire « faux ». Ça veut dire : **quel poids** cette source peut avoir dans un rapport remis à un client. Dans l'évaluation 1, chaque information importante doit pouvoir s'appuyer sur une source fiable ou sur **votre propre essai**.

---

## Lire une grille de prix

Les outils Web se paient rarement « une fois ». Presque tous sont des **abonnements** (on parle de SaaS : *Software as a Service*), et chacun calcule son prix à sa façon.

| Modèle | Comment ça marche | Ce qui fait monter la facture |
|:--|:--|:--|
| **Au mois (forfait)** | Un montant fixe chaque mois, peu importe l'usage | Le forfait supérieur, quand on dépasse une limite (nombre de réservations, de pages, d'espace) |
| **À l'utilisateur** | Un montant par personne qui a un accès | Chaque employé ajouté : l'accueil, les guides, le comptable |
| **À la transaction (commission)** | Un pourcentage ou un montant sur chaque vente | Le succès : plus l'entreprise vend, plus elle paie |
| **Gratuit… avec limites** | Un forfait de départ gratuit | Les fonctions essentielles réservées aux forfaits payants, le logo de l'outil affiché |

### Les pièges d'une grille de prix

<div class="bg-red-50 border border-red-300 text-red-900 rounded-lg p-4 mb-5">
<ul class="list-disc pl-5">
  <li><strong>Le prix en dollars américains.</strong> 100 $ US, ce n'est pas 100 $ CA.</li>
  <li><strong>« Facturé annuellement ».</strong> Le prix affiché au mois suppose souvent un engagement de 12 mois payé d'avance. Au mois, c'est plus cher.</li>
  <li><strong>Les modules payants.</strong> La fonction dont vous avez besoin (synchronisation avec Viator, deuxième langue, décharge) est souvent un supplément.</li>
  <li><strong>Les frais de paiement.</strong> Le service de paiement prend sa part (souvent autour de 3 % par transaction) en plus de l'outil.</li>
  <li><strong>Les taxes.</strong> TPS et TVQ s'ajoutent presque toujours au prix affiché.</li>
  <li><strong>La saison.</strong> Une entreprise saisonnière paie-t-elle 12 mois pour en utiliser 8 ? Peut-on suspendre l'abonnement l'hiver ?</li>
</ul>
</div>

#### Exemples réels : des grilles de prix

Les prix changent souvent : ceux-ci ont été vérifiés le **6 octobre 2026**. Dans votre rapport, notez toujours la date à laquelle vous avez lu un prix.

| Outil | Le piège à repérer |
|:--|:--|
| [Square — Nos frais (Canada)](https://squareup.com/ca/fr/payments/our-fees) | Déjà utilisé par le client. En ligne : 2,8 % + 0,30 $. Cherchez le supplément pour les cartes émises hors du Canada. |
| [Checkfront](https://www.checkfront.com/pricing) (Q1) | Abonnement mensuel **et** commission par réservation en ligne, en dollars américains. |
| [Weglot](https://www.weglot.com/pricing) (Q5) | Prix en euros, limite de mots traduits et de langues. Comparez « Monthly » et « Yearly ». |
| [Wix — Forfaits](https://www.wix.com/plans) (Q3) | Le prix au mois suppose un paiement annuel. Que manque-t-il au forfait gratuit ? |
| FareHarbor (Q1) | Pas d'abonnement : les frais de réservation sont ajoutés à la facture **du client**. Le modèle de prix touche aussi l'expérience client. |

**Calcul rapide :** une réservation en ligne de 400 $ avec Checkfront, frais de paiement compris. Et si la carte vient des États-Unis ?

## Activité 2 — Trois outils, trois factures

<div class="bg-blue-50 border border-blue-200 text-blue-900 rounded-lg p-4 mb-5">
<strong>Consigne (25 min, en équipe)</strong><br>
Trois outils de réservation <strong>fictifs</strong>, trois façons de calculer le prix. Avec les hypothèses fournies, calculez ce que chacun coûterait à Aventure Saint-Maurice <strong>pour une année</strong>. Écrivez vos réponses, puis cliquez sur « Vérifier ».
</div>

<GrillePrix />

---

## Essayer un outil de façon rigoureuse

Lire la documentation d'un outil, c'est savoir ce qu'il **prétend** faire. L'essayer, c'est savoir ce qu'il **fait**, et combien d'efforts ça demande. À la séance 4, chaque équipe essaiera deux ou trois outils. Pour que la comparaison soit juste, l'essai se prépare **ce soir**.

### Les règles d'un essai rigoureux

| Règle | Pourquoi |
|:--|:--|
| **Les mêmes manipulations sur chaque outil**, dans le même ordre | Sinon, on compare des pommes et des oranges. |
| **Des scénarios tirés du mandat**, pas de la démonstration du vendeur | « Une famille de 4 réserve la via ferrata pour samedi 10 h », pas « créer un produit test ». |
| **On note le temps** que prend chaque manipulation | « Facile » ne veut rien dire. « 4 minutes, sans aide » veut dire quelque chose. |
| **On prend des captures d'écran** | Elles serviront de preuves dans le rapport. |
| **On note ce qui ne fonctionne pas** ou ce qui est bloqué dans la version d'essai | Un échec est un résultat aussi important qu'un succès. |
| **On essaie des deux côtés** : le client qui réserve, et Mélanie qui gère | Un outil peut être agréable pour l'un et pénible pour l'autre. |
| **On essaie sur téléphone**, et avec un réseau lent | La majorité des clients réserveront sur leur téléphone. Le guide sera au quai. |
| **On vérifie comment on en sort** : exporter les données, fermer le compte | Un outil facile à adopter et impossible à quitter est un risque. |

### Ouvrir un compte d'essai sans se faire piéger

<div class="bg-yellow-50 border border-yellow-200 text-yellow-900 rounded-lg p-4 mb-5">
<ul class="list-disc pl-5">
  <li><strong>Vérifiez la durée de l'essai avant de l'ouvrir.</strong> Il n'y a pas de cours le 14 octobre : un essai de 14 jours ouvert ce soir sera expiré le 21. Si l'essai est court, notez-le et ouvrez le compte <strong>la veille de la séance 4</strong>.</li>
  <li><strong>Utilisez une adresse courriel d'équipe</strong> que tous les membres peuvent consulter, et notez les accès dans votre dossier partagé.</li>
  <li><strong>N'entrez aucune carte de crédit.</strong> Si un outil l'exige pour l'essai, notez-le comme constat et passez au suivant, ou demandez à l'enseignant.</li>
  <li><strong>N'entrez aucun vrai renseignement personnel</strong>, ni le vôtre ni celui d'un client. Utilisez des données inventées (Loi 25).</li>
  <li><strong>Lisez ce que l'essai ne comprend pas.</strong> Certaines fonctions sont bloquées pendant l'essai : c'est un constat à noter.</li>
</ul>
</div>

---

## Les cinq questions techniques

Chaque équipe reçoit, par tirage, **une** des cinq questions. Elle l'explore en profondeur aux séances 3 et 4, avec des essais. Dans l'évaluation 1, elle traite aussi les quatre autres questions, en survol, à partir de sa propre recherche documentaire.

| # | La question | Ce qui la rend difficile dans le mandat |
|:-:|:--|:--|
| **Q1** | **Comment réserver et payer en ligne ?** | Places limitées par départ, groupes avec dépôt de 30 %, Viator qui vend les mêmes places, Square à garder, cartes-cadeaux, annulations pour la météo |
| **Q2** | **Comment faire signer la décharge avant l'arrivée ?** | Parents qui signent pour les mineurs, questions de santé (Loi 25), texte de l'avocat en français seulement, consultation au quai sans réseau |
| **Q3** | **Sur quelle plateforme construire le site ?** | Mélanie doit le modifier seule, compte Wix au nom du neveu, nom de domaine et courriels à ne pas briser, intégration de la réservation |
| **Q4** | **Comment montrer les vidéos sans ralentir le site ?** | 60 Go de vidéos 4K, vidéo plein écran souhaitée, visiteurs sur téléphone, sous-titres et accessibilité |
| **Q5** | **Comment offrir le site en français et en anglais ?** | Charte de la langue française, traduction automatique ou humaine, décharge juridique, outil de réservation à traduire aussi |

## À faire maintenant

[Lab 03 — Le plan d'essai](./../../labs/lab03-plan-essai)

---

## Avant la séance 4 (21 octobre)

<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text">Déposer la fiche du Lab 03 dans l'équipe Teams du cours</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Ouvrir les comptes d'essai <strong>au bon moment</strong> : ils doivent être actifs le 21 octobre</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Préparer les données inventées dont vous aurez besoin pour vos scénarios (noms, départs, tarifs)</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Lire l'énoncé de l'évaluation 1 et noter vos questions</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Commencer la mise au propre des parties 1 à 3 du rapport à partir du Lab 02</span></label></li>
</ul>
