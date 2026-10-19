---
title: "Séance 4 — Essayer et comparer des outils"
aside: false
---

# Séance 4 — Essayer et comparer des outils

## Objectifs
- Faire les essais prévus au Lab 03 et en **documenter les résultats** : réussi, échoué ou non vérifiable, avec une mesure et une preuve.
- Écrire un **constat appuyé**, sans jugement vague et sans recommandation.
- Comparer des outils sur les critères de l'évaluation 1 : ce qu'ils font, le **coût sur trois ans**, le **temps pour apprendre**, la **facilité d'en sortir** et les **signes de pérennité** (ces trois derniers se complètent à la maison).
- Profiter du travail des autres équipes pour préparer le survol des quatre autres questions.

## Déroulement de la séance

| Heure | Activité |
|:--|:--|
| 18 h 30 | Retour sur les plans d'essai du Lab 03 et correction des critères |
| 18 h 45 | Documenter un essai |
| 18 h 55 | Activité 1 — Constat, affirmation non appuyée ou recommandation ? |
| 19 h 20 | [Lab 04 — Les essais](./../../labs/lab04-essais) (en équipe) |
| 20 h 00 | Pause |
| 20 h 15 | Lab 04 — suite des essais |
| 21 h 00 | Comparer sans recommander : les familles de solutions et les critères du tableau |
| 21 h 10 | Lab 04 — le tableau de comparaison et les trois constats |
| 21 h 30 | Retour en grand groupe : les cinq questions |
| 21 h 45 | À faire à la maison et avant la séance 5 |

---

## Retour sur le Lab 03

Ce soir, vous passez de la lecture à l'essai. Un plan d'essai faible se voit tout de suite : on improvise, chaque outil est essayé différemment, et à la fin on ne peut rien comparer.

<div class="bg-blue-50 border border-blue-200 text-blue-900 rounded-lg p-4 mb-5">
<strong>Ce qui revient le plus souvent dans les plans</strong><br>
<ul class="list-disc pl-5">
  <li><strong>Des critères qui ne se mesurent pas.</strong> « Réussi si c'est facile » ou « si ça marche bien ». Remplacez l'adjectif par un chiffre ou par un fait observable : un temps, un nombre de clics, oui ou non.</li>
  <li><strong>Des scénarios sans données.</strong> « Tester la réservation » ne dit pas quoi réserver, pour combien de personnes, sur quel appareil.</li>
  <li><strong>Des essais différents d'un outil à l'autre.</strong> La règle ne change pas : les mêmes essais, dans le même ordre, sur chaque outil.</li>
</ul>
</div>

**Le test des deux observateurs :** deux personnes regardent le même essai, chacune de son côté. Si elles peuvent arriver à un verdict différent, le critère n'est pas assez précis. Prenez cinq minutes pour corriger vos critères **avant** de commencer.

| Critère faible | Critère mesurable |
|:--|:--|
| Réussi si la réservation est rapide | Réussi si la réservation de 5 places prend moins de 3 minutes sur téléphone, sans aide |
| Réussi si l'outil fonctionne hors ligne | Réussi si, en mode avion, la liste des participants du jour et leurs allergies s'affichent |
| Réussi si Mélanie peut s'en servir | Réussi si le membre qui n'a jamais vu l'outil change un prix en moins de 5 minutes, sans ouvrir l'aide |
| Réussi si la vidéo ne ralentit pas le site | Réussi si le LCP mobile de la page reste sous 2,5 secondes dans PageSpeed Insights |

---

## Documenter un essai

Un essai qui n'est pas noté n'a pas eu lieu. Dans le rapport, chaque résultat doit pouvoir être **retrouvé** : quel outil, quel jour, quelle mesure, quelle capture.

### Trois résultats possibles

| Résultat | Quand l'utiliser | Exemple |
|:--|:--|:--|
| **Réussi** ✓ | Le critère décidé d'avance est atteint. | La réservation de 5 places a pris 2 min 40 s. Il reste bien 3 places. |
| **Échoué** ✗ | L'outil permet la manipulation, mais le critère n'est pas atteint. Ou l'outil ne le permet pas du tout. | En mode avion, l'application affiche « Aucune connexion » et aucune liste. |
| **Non vérifiable** ? | L'essai ne permet pas de savoir : fonction bloquée pendant l'essai, besoin d'un vrai compte Viator, d'un vrai paiement… | La connexion à Viator exige un compte Viator d'entreprise. |

<div class="bg-yellow-50 border border-yellow-200 text-yellow-900 rounded-lg p-4 mb-5">
<strong>« Non vérifiable » n'est pas un échec de votre part</strong><br>
C'est un résultat honnête, à condition d'écrire <strong>pourquoi</strong> et <strong>ce qui permettrait de vérifier</strong> (une démonstration du vendeur, une question au support, un compte réel). Ces points deviennent les problèmes à prévoir et les questions de la section 7 du rapport. Ne transformez jamais un « non vérifiable » en « réussi » parce que la documentation le promet.
</div>

### Ce qu'on note pour chaque essai

- **La mesure brute :** « 2 min 40 s », « 14 clics », « 3,8 Mo », « score de 62 ». Pas « assez vite ».
- **Le résultat :** réussi, échoué ou non vérifiable.
- **Ce qu'on a observé :** un message d'erreur, une étape inattendue, une fonction introuvable, une aide demandée.
- **La preuve :** au moins une capture d'écran, nommée pour qu'on la retrouve : `Q1-Checkfront-E3-01.png` (question, outil, essai, numéro).
- **Le contexte, une seule fois par outil :** la date, le forfait d'essai utilisé, l'appareil et le navigateur.

### Les règles pendant l'essai

| Règle | Pourquoi |
|:--|:--|
| **On ne change pas le critère après coup.** | Sinon, tous les outils finissent par réussir. |
| **Si le scénario doit changer, on le note.** | « Fonction introuvable : on a fait E4 avec 3 places au lieu de 5. » Le lecteur doit le savoir. |
| **Le chronomètre part** quand la personne touche à l'écran, **et s'arrête** quand le résultat est visible. | Mêmes règles pour chaque outil. |
| **La personne qui joue Mélanie n'est pas aidée.** | Si elle demande de l'aide, on note « aide demandée » et on continue. C'est une mesure, pas un échec de l'équipe. |
| **Données inventées seulement.** | Aucun vrai nom, aucune vraie carte, aucune vraie information de santé (Loi 25). |

---

## Activité 1 — Constat, affirmation non appuyée ou recommandation ? {#activite-1}

Dans l'évaluation 1, la section 6 décrit les possibilités techniques. Chaque phrase doit être un **constat appuyé** : sur le mandat, sur une source datée ou sur **vos essais**. Deux sortes de phrases s'y glissent sans qu'on s'en rende compte.

| Sorte de phrase | Ce qui la trahit | Ce qu'on en fait |
|:--|:--|:--|
| **Constat appuyé** | Une mesure, une date, une source, un renvoi à un essai | On la garde |
| **Affirmation non appuyée** | *facile*, *rapide*, *complet*, *performant*, *tout le monde*, *risque de*… sans preuve | On la remplace par ce qu'on a mesuré ou lu |
| **Recommandation** | *nous recommandons*, *il faudrait*, *devrait*, *le meilleur choix*, *à privilégier*, *idéalement* | On la retire de l'évaluation 1 et on garde le fait qui se cache derrière |

<div class="bg-blue-50 border border-blue-200 text-blue-900 rounded-lg p-4 mb-5">
<strong>Consigne (15 min, en équipe, puis retour en grand groupe)</strong><br>
Les onze phrases ci-dessous viennent du brouillon d'une équipe fictive. Les outils sont inventés.
<ol class="list-decimal pl-5">
  <li>Classez chaque phrase. La réponse s'affiche après votre choix.</li>
  <li>Pour chaque phrase qui n'est pas un constat, écrivez votre réécriture <strong>avant</strong> de regarder celle qu'on propose. Inventez la mesure ou la source au besoin.</li>
  <li>À la fin, cliquez sur « Copier nos réponses » et collez-les dans vos notes ou le document de l'équipe.</li>
</ol>
</div>

<ConstatOuRecommandation />

**Ce qu'il faut retenir :** derrière presque chaque recommandation, il y a un fait utile. Le travail de l'évaluation 1, c'est de **trouver ce fait et de le montrer**, pour que Mélanie puisse décider. L'évaluation 2 dira ce que vous lui conseillez.

## À faire maintenant

[Lab 04 — Les essais](./../../labs/lab04-essais) : partie 1, les essais, jusqu'à la pause et après.

---

## Comparer sans recommander

À la fin des essais, vous avez des résultats pour deux ou trois outils. L'évaluation 1 demande de les présenter dans un **tableau de comparaison**, sur les mêmes critères, sans désigner de gagnant.

### Les familles de solutions

Avant de comparer des outils, situez-les. Pour presque toutes les questions, il existe trois grandes façons de répondre au besoin.

| Famille | Exemple pour Q1 (réservation) | Ce qu'on gagne | Ce qu'on risque |
|:--|:--|:--|:--|
| **Un service spécialisé**, payé par abonnement | Un logiciel de réservation pour les entreprises d'activités | Des fonctions pensées pour le métier, mises à jour par le fournisseur | Un outil de plus à payer, à apprendre et à relier au site |
| **Une fonction de la plateforme du site** (module, extension) | Le module de réservation du constructeur de site | Tout au même endroit, une seule facture | Des fonctions souvent plus simples : capacité par départ, synchronisation avec Viator… |
| **Un développement sur mesure** | Un système de réservation programmé pour le client | Exactement ce que le client veut | Le coût, le délai, et la dépendance envers celui qui l'a programmé |

Dans le rapport, nommez la famille de chaque outil. Une équipe qui n'a essayé que des outils de la même famille doit au moins **décrire** les autres familles.

### Les critères du tableau de comparaison

Ce sont les lignes du tableau demandé dans l'évaluation 1. Chaque case se remplit avec un **constat** : une mesure de vos essais ou une information d'une source citée.

| Critère | La question à se poser | Où trouver la réponse |
|:--|:--|:--|
| **Ce que l'outil fait** | Quels besoins essentiels du Lab 03 sont couverts ? Lesquels ne le sont pas ? | Vos essais d'abord, la documentation ensuite |
| **Le modèle de prix et le coût sur trois ans** | Combien, au total, pour les trois premières années, en dollars canadiens ? | La page de prix (datée), et votre calcul avec ses hypothèses |
| **Le temps pour apprendre** | Combien de temps avant que Mélanie puisse faire seule une tâche courante ? | L'essai joué par le membre qui ne connaît pas l'outil; l'aide offerte en français |
| **La facilité d'en changer** | Si l'entreprise veut quitter l'outil dans trois ans, que peut-elle emporter ? | L'essai de sortie : export, format, fermeture du compte; les conditions d'utilisation |
| **Les signes de pérennité** | Qu'est-ce qui indique que l'outil existera encore dans cinq ans ? | Le journal des modifications, l'historique de l'entreprise, les témoignages récents |

## À faire maintenant

[Lab 04 — Les essais](./../../labs/lab04-essais) : parties 2 et 3, le tableau de comparaison et les trois constats. Remplissez ce que vos essais permettent; les lignes du coût sur trois ans, de la facilité d'en changer et de la pérennité se complètent à la maison.

---

## Retour en grand groupe : les cinq questions

**Une équipe par question** présente ses essais en **2 minutes**, sans diapositive :

1. Les outils essayés, avec leur famille.
2. **Deux constats**, dont au moins une limite.
3. Ce qui est resté **non vérifiable**.

Si deux équipes ont la même question, la deuxième ajoute seulement ce qui diffère de la première, en 30 secondes.

Pendant ce temps, les autres prennent des notes. Elles serviront au **survol des quatre autres questions** dans l'évaluation 1.

<div class="bg-red-50 border border-red-300 text-red-900 rounded-lg p-4 mb-5">
<strong>Les notes d'une autre équipe ne sont pas une source</strong><br>
Elles vous donnent des <strong>pistes</strong> : des noms d'outils, des pièges, des pages à aller lire. Dans votre rapport, chaque information sur un outil doit venir de <strong>votre propre recherche</strong> : la page de prix, la documentation, un témoignage, avec la date de consultation.
</div>

<NotesCinqQuestions />

---

## À faire à la maison {#a-faire-a-la-maison}

<div class="bg-yellow-50 border border-yellow-200 text-yellow-900 rounded-lg p-4 mb-5">
<strong>Pour compléter votre tableau de comparaison</strong><br>
Trois lignes du tableau demandent plus que vos essais : la <strong>facilité d'en changer</strong>, les <strong>signes de pérennité</strong> et le <strong>coût sur trois ans</strong>. Lisez les trois sections ci-dessous, faites l'activité 2, puis complétez ces lignes dans la fiche du Lab 04 avant de la déposer.
</div>

### Lire : le verrouillage, ou la facilité d'en changer

On parle de **verrouillage** (en anglais, *lock-in*) quand il coûte si cher de quitter un outil qu'on reste, même s'il ne convient plus. Le client en vit déjà un : le site actuel est sur Wix, au nom du neveu, et personne ne sait le modifier.

Ce qui verrouille le plus souvent :
- **Les données qu'on ne peut pas exporter**, ou seulement dans un format que personne d'autre ne lit. Une liste de réservations en CSV ou en Excel se réutilise; un PDF par client, beaucoup moins.
- **Le contenu qui ne sort pas de la plateforme.** Un site fait sur un constructeur ne se transporte généralement pas tel quel chez un autre : il faut le refaire. Le [centre d'aide de Wix](https://support.wix.com/en/article/exporting-or-embedding-your-wix-site-elsewhere) l'indique clairement : un site Wix ne peut pas être hébergé ailleurs. Le nom de domaine, lui, peut changer de fournisseur.
- **Les comptes au nom d'une personne** plutôt que de l'entreprise.
- **Les contrats** : engagement de 12 mois, frais de résiliation, renouvellement automatique.

### Lire : les signes de pérennité

Personne ne peut prédire qu'un outil existera dans cinq ans. On peut toutefois **observer des signes** et les rapporter, avec leur source. Aucun signe ne suffit seul.

| Plutôt rassurant | Plutôt inquiétant |
|:--|:--|
| Un journal des modifications avec des nouveautés récentes | Aucune nouveauté depuis plus d'un an |
| Une application mobile mise à jour régulièrement | Une application mal notée et pas mise à jour depuis longtemps |
| Une entreprise qui existe depuis plusieurs années, des clients nommés | Aucun nom, aucune adresse, aucune date sur le site |
| Une page d'état du service, qui montre l'historique des pannes | Des témoignages récents de pannes sans réponse du support |
| Des prix publics et des conditions claires | L'annonce de la fin d'une fonction ou d'un forfait |

<div class="bg-slate-50 border border-slate-200 text-slate-800 rounded-lg p-4 mb-5">
<strong>Un rachat : bon ou mauvais signe ?</strong><br>
Quand une grande entreprise achète un outil, il a plus de moyens… mais ses prix et ses priorités peuvent changer. Exemple : le logiciel de réservation Bókun appartient à Tripadvisor, qui possède aussi Viator. Pour Aventure Saint-Maurice, est-ce un avantage ou un risque ? Les deux : c'est exactement le genre de nuance à <strong>décrire</strong> dans le rapport, sans trancher.
</div>

### Le coût sur trois ans

Le prix affiché d'un outil, c'est rarement ce qu'il coûte vraiment. L'évaluation 1 demande une **estimation sur trois ans**, parce que la première année est souvent trompeuse.

| Ce qui change d'une année à l'autre | Exemple |
|:--|:--|
| **Les frais payés une seule fois** | Mise en place, configuration, importation des données, formation |
| **Les prix de lancement** | « 25 $ par mois la première année », puis le prix régulier |
| **Les frais qui suivent l'usage** | Commission par réservation, prix par décharge signée, prix au visionnement d'une vidéo, nombre de mots traduits |
| **La devise** | Un prix en dollars américains ou en euros, converti avec un taux qu'on indique |

Montrez toujours le calcul et **les hypothèses** : nombre de réservations, de participants, d'utilisateurs, taux de change, date de lecture des prix. Le lecteur doit pouvoir refaire votre calcul.

### Activité 2 — Le coût sur trois ans {#activite-2}

<div class="bg-blue-50 border border-blue-200 text-blue-900 rounded-lg p-4 mb-5">
<strong>Consigne (environ 20 min, seul ou en équipe)</strong><br>
Trois outils de décharge électronique <strong>fictifs</strong> pour la question Q2. Avec les hypothèses fournies, calculez pour chacun le coût de la <strong>première année</strong> et le coût <strong>total sur trois ans</strong>, en dollars canadiens. Cliquez sur « Vérifier », puis <strong>copiez vos réponses dans vos notes</strong> : on en fera un court retour au début de la séance 5.
</div>

<CoutTroisAns />

**Ce qu'il faut retenir :** le classement de la première année n'est pas celui de trois ans. Et le moins cher n'est pas un choix : dans l'évaluation 1, on présente les trois coûts côte à côte, avec ce que chaque outil fait et ne fait pas.

---

## Avant la séance 5 (28 octobre)

<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text">Faire l'<a href="#activite-2">activité 2 — Le coût sur trois ans</a> et copier vos réponses dans vos notes</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Compléter les lignes « coût sur trois ans », « facilité d'en changer » et « signes de pérennité » du tableau de comparaison</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Déposer la fiche du Lab 04 dans l'équipe Teams du cours</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Terminer les essais qui n'ont pas pu être faits en classe, avec les mêmes règles</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Ranger les captures dans le dossier partagé, bien nommées : elles iront dans l'annexe A</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Rédiger le premier jet de votre question dans la section 6 du rapport, avec le tableau de comparaison</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Commencer la recherche pour les quatre autres questions : deux outils chacune, page de prix datée et coût sur trois ans</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Fermer les comptes d'essai dont vous n'avez plus besoin, ou noter leur date d'expiration</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Apporter le brouillon du rapport à la séance 5 : on travaillera l'organisation et l'écriture pour un client</span></label></li>
</ul>
