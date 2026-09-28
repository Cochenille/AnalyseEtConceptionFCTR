---
title: "Séance 2 — Le mandat, les contraintes et les risques"
aside: false
---

# Séance 2 — Le mandat, les contraintes et les risques

## Objectifs
- Relever les contraintes d'un mandat réel et les classer.
- Préciser les contraintes de budget, de délai, de personnel et de technologie.
- Distinguer ce que le site doit **faire** de la façon dont il doit le **faire** : vitesse, sécurité, accessibilité, Loi 25, navigateurs.
- Distinguer une **contrainte** d'un **risque**, et évaluer un risque selon ses chances d'arriver et ses conséquences.
- Dresser la liste des problèmes techniques à prévoir.

## Déroulement de la séance

| Heure | Activité |
|:--|:--|
| 18 h 30 | Retour sur le Lab 01 : le tableau des quatre paires |
| 18 h 45 | Formation des équipes |
| 18 h 55 | [Le mandat du client](./../../mandat/) : lecture en équipe |
| 19 h 15 | Les contraintes de ressources, en détail |
| 19 h 30 | Ce que le site doit faire, et comment il doit le faire |
| 19 h 50 | Activité — Les cinq phrases du client |
| 20 h 10 | Pause |
| 20 h 25 | Contrainte ou risque ? La matrice des risques |
| 20 h 40 | [Lab 02 — Radiographie du mandat](./../../labs/lab02-radiographie-mandat) (en équipe) |
| 21 h 35 | Correction commentée en grand groupe |
| 21 h 55 | L'évaluation 1 : ce qui s'en vient |

---

## Retour sur le Lab 01

Chaque duo donne ses résultats : plateforme, score de performance mobile, verdict. On remplit ensemble le tableau.

| Paire | Site | Plateforme | Performance mobile | Plus facile à faire évoluer ? |
|:-:|:--|:--|:-:|:-:|
| 1 | La Banquise | | | |
| 1 | Casse-Croûte Courteau | | | |
| 2 | Thaï Express | | | |
| 2 | Ashton | | | |
| 3 | Schwartz's | | | |
| 3 | Commensal | | | |
| 4 | Joe Beef | | | |
| 4 | Épi, buvette de quartier | | | |

**La question à retenir :** un site peut être beau, rapide et difficile à faire évoluer. C'est ce genre de nuance qu'on attend dans un rapport de faisabilité.

---

## Formation des équipes

- Équipes de **2 ou 3 personnes**, qui restent **les mêmes toute la session** (évaluations 1, 2 et 3).
- Votre équipe est une petite agence Web : **Studio Web FC**. Donnez-lui un nom d'équipe si vous voulez.
- Créez tout de suite un **dossier partagé** (OneDrive ou Teams) où vous rangerez tous les documents du mandat.

<div class="bg-yellow-50 border border-yellow-200 text-yellow-900 rounded-lg p-4 mb-5">
<strong>Avant de partir ce soir</strong><br>
Écrivez-vous une <strong>entente d'équipe</strong> de cinq lignes : comment vous communiquez, à quel moment vous travaillez ensemble, qui remet les travaux, et ce que vous faites si quelqu'un ne livre pas sa part.
</div>

---

## Le mandat du client

Le mandat qui servira toute la session : **[Aventure Saint-Maurice](./../../mandat/)**, un centre de plein air qui veut refaire son site Web.

Lisez-le en équipe : le courriel du client, les notes de la première rencontre et les chiffres. Pendant la lecture, **surlignez** avec trois couleurs :

| Couleur | Ce que vous surlignez |
|:--|:--|
| **Jaune** | Ce que le client **veut** que le site fasse |
| **Rose** | Ce qui **limite** les choix : argent, temps, personnes, technologie, lois |
| **Vert** | Ce qui est **flou** ou qu'il faudra **vérifier** |

---

## Les contraintes de ressources, en détail

À la séance 1, on a vu trois sortes de contraintes : techniques, organisationnelles et de ressources. Dans un rapport de faisabilité, on regarde de plus près quatre éléments.

| Élément | La question à se poser | Dans le mandat |
|:--|:--|:--|
| **Budget** | Combien pour construire ? Et combien **chaque année** ensuite ? | 8 000 $ pour construire, peut-être 13 000 $. Aucun montant prévu pour les coûts annuels. |
| **Délai** | La date est-elle **ferme** ou **souhaitée** ? De quoi dépend-elle ? | Le 1<sup>er</sup> mars est ferme. Les cartes-cadeaux « pour Noël » sont souhaitées. |
| **Personnel** | Qui fera le travail, **avant** et **après** le lancement ? Avec quelles compétences ? Quand est-il disponible ? | Mélanie seule l'hiver, débordée l'été. Des guides différents chaque année. |
| **Technologie** | Qu'est-ce qui **existe déjà** et qu'il faut garder, remplacer ou relier ? | Wix, Square, Viator, Google Workspace, le nom de domaine, l'Excel. |

<div class="bg-red-50 border border-red-300 text-red-900 rounded-lg p-4 mb-5">
<strong>Pièges fréquents</strong><br>
<ul class="list-disc pl-5">
  <li><strong>Prendre le budget annoncé pour le budget réel.</strong> Le client a donné un chiffre pour la construction. Il n'a pas pensé aux abonnements, aux frais par transaction ni à l'entretien.</li>
  <li><strong>Oublier que le délai dépend du client.</strong> Si les photos et les textes arrivent en février, le site ne sera pas prêt le 1<sup>er</sup> mars, peu importe la vitesse de l'équipe.</li>
  <li><strong>Compter seulement ceux qui construisent.</strong> Il faut aussi savoir qui fera vivre le site pendant cinq ans.</li>
  <li><strong>Oublier ce qui existe déjà.</strong> Le nom de domaine et les adresses courriel fonctionnent aujourd'hui. Le projet ne doit pas les briser.</li>
</ul>
</div>

---

## Ce que le site doit faire, et comment il doit le faire

Un client décrit surtout ce que le site doit **faire** : réserver, payer, signer une décharge. On appelle ça les **exigences fonctionnelles**.

Mais il y a aussi la **façon** dont il doit le faire : assez vite, de façon sécuritaire, pour tout le monde, dans le respect de la loi. On appelle ça les **exigences non fonctionnelles**. Le client en parle rarement, mais c'est souvent là que se cachent les problèmes techniques.

### À vous de classer

<TriExigences />

### Les cinq exigences non fonctionnelles à vérifier dans tout projet

#### 1. La vitesse
- Plus de la moitié des visites se font sur téléphone, souvent avec un réseau moyen.
- Les repères de Google (Core Web Vitals) : l'élément principal de la page devrait s'afficher en **moins de 2,5 secondes** (le LCP, vu au Lab 01).
- Ce qui ralentit le plus : les images et les vidéos trop lourdes, les scripts de services externes (publicité, clavardage, suivi).

#### 2. La sécurité
- Le cadenas (HTTPS) est un minimum, pas une garantie.
- **Ne jamais garder les numéros de carte de crédit** sur le site. On confie le paiement à un service spécialisé (Square, Stripe, PayPal…) qui respecte les normes de l'industrie.
- Qui a accès à quoi ? Un guide n'a pas besoin de voir les revenus. L'employée d'accueil n'a pas besoin de pouvoir supprimer le site.
- Les mises à jour, les sauvegardes et les mots de passe : qui s'en occupe, et à quelle fréquence ?

#### 3. L'accessibilité
- Un site accessible peut être utilisé par une personne aveugle, malvoyante, sourde, qui ne peut pas se servir d'une souris, ou qui a une incapacité cognitive.
- La référence internationale : les **WCAG** (Web Content Accessibility Guidelines), niveau **AA**.
- Au Québec, les organismes publics doivent respecter un standard gouvernemental. Pour une entreprise privée, c'est une bonne pratique… et parfois une **condition d'une subvention**, comme dans notre mandat.
- Exemples concrets : texte de remplacement des images, contraste suffisant, navigation au clavier, sous-titres des vidéos, formulaires bien identifiés.

#### 4. La Loi 25 et les renseignements personnels

La **Loi 25** modernise les règles québécoises de protection des renseignements personnels. Elle s'applique à toute entreprise qui recueille des renseignements sur des Québécois, **petite ou grande**.

| Ce que la loi demande | Ce que ça veut dire pour un site Web |
|:--|:--|
| Une **personne responsable** de la protection des renseignements personnels | Par défaut, c'est la personne la plus haut placée de l'entreprise : ici, Mélanie. Son titre et ses coordonnées doivent être publiés sur le site. |
| Une **politique de confidentialité** en termes simples et clairs | Une page qui explique ce qu'on recueille, pourquoi, combien de temps on le garde et qui y a accès. |
| Un **consentement** clair | Les témoins (cookies) de suivi et de publicité doivent être **désactivés par défaut**. La bannière doit permettre de refuser aussi facilement que d'accepter. |
| Un consentement **exprès** pour les renseignements **sensibles** | Les renseignements de santé de la décharge sont sensibles : le client doit les fournir en sachant clairement pourquoi. |
| Une **évaluation** avant d'envoyer des renseignements **hors du Québec** | Si le système de réservation garde ses données aux États-Unis, il faut évaluer les risques avant de l'adopter. |
| Déclarer les **incidents** de confidentialité | Une fuite qui présente un risque sérieux doit être déclarée à la Commission d'accès à l'information et aux personnes touchées. |
| Détruire ou anonymiser les renseignements quand on n'en a plus besoin | Les boîtes de décharges « depuis 2014 » posent déjà problème. |

<div class="bg-slate-50 border border-slate-200 text-slate-800 rounded-lg p-4 mb-5">
<strong>Ce n'est pas un avis juridique</strong><br>
Dans un rapport de faisabilité, on <strong>signale</strong> les enjeux de la Loi 25 et on recommande au client de valider avec un conseiller juridique. On ne s'improvise pas avocat. Pour en savoir plus : le site de la <a href="https://www.cai.gouv.qc.ca/" target="_blank">Commission d'accès à l'information du Québec</a>.
</div>

La **Charte de la langue française** s'ajoute : un site offert au Québec doit être disponible en français, et la version française doit être au moins aussi complète que les autres versions.

#### 5. Les navigateurs et les appareils à supporter
- On ne peut pas tester sur tous les appareils : il faut **choisir** une liste et l'écrire dans le rapport.
- Une liste raisonnable en 2026 : les deux dernières versions de **Chrome, Safari, Edge et Firefox**, sur ordinateur, et **Safari sur iPhone** et **Chrome sur Android**, sur téléphone.
- Pour choisir, on regarde les statistiques du site actuel. Ici, il n'y en a pas : c'est une information à obtenir.
- Attention à **Safari sur iPhone** : au Québec, il représente une grande part des visites sur téléphone, et c'est souvent là que des problèmes apparaissent.

---

## Activité — Les cinq phrases du client

<div class="bg-blue-50 border border-blue-200 text-blue-900 rounded-lg p-4 mb-5">
<strong>Consigne (20 min, en équipe)</strong><br>
Chacune des phrases ci-dessous a été prononcée pendant la rencontre. Elles ont l'air banales, mais chacune cache un problème technique.
<ol class="list-decimal pl-5">
  <li>Pour chaque phrase, trouvez le problème caché et notez une question à poser au client.</li>
  <li>Estimez ce que ça pourrait coûter : <strong>$</strong>, <strong>$$</strong> ou <strong>$$$</strong>. Est-ce un coût unique ou annuel ?</li>
  <li>Ne cliquez sur « Révéler » qu'une fois votre réponse écrite. On compare en grand groupe.</li>
</ol>
</div>

<PhrasesCachees />

**Ce qu'il faut retenir :** le client ne ment pas et il n'est pas naïf. Il ne sait simplement pas ce que sa demande implique. C'est le rôle de l'analyste de le lui expliquer **avant** que le projet commence, pas après.

---

## Contrainte ou risque ?

Les deux mots se ressemblent, mais ils ne veulent pas dire la même chose.

| | Contrainte | Risque |
|:--|:--|:--|
| **Définition** | Une limite **certaine**, connue dès le départ | Un événement **incertain** qui pourrait nuire au projet |
| **Question** | Qu'est-ce qui limite nos choix ? | Qu'est-ce qui pourrait mal tourner ? |
| **Exemple** | Le site doit être en ligne le 1<sup>er</sup> mars. | Les photos arrivent en retard et le site n'est pas prêt le 1<sup>er</sup> mars. |
| **Ce qu'on en fait** | On en tient compte dans les choix | On l'évalue, puis on prévoit une mesure pour le réduire |

### D'où viennent les risques ?

| Origine | Exemples |
|:--|:--|
| **Techniques** | Deux systèmes qui ne se parlent pas comme prévu; des données perdues pendant le transfert; un outil qui ferme ses portes; un site trop lent. |
| **Organisationnels** | Le client livre ses contenus en retard; personne ne met le site à jour; les décideurs changent d'avis; un accès essentiel est au nom de quelqu'un d'autre. |

### Évaluer un risque

On évalue chaque risque selon deux questions :
1. **Quelles sont les chances que ça arrive ?** Faible, moyenne ou élevée.
2. **Si ça arrive, quelles sont les conséquences ?** Faibles, moyennes ou graves.

On place ensuite le risque dans une **matrice**. Plus il est en haut à droite, plus il faut s'en occuper.

| Chances ↓ · Conséquences → | Faibles | Moyennes | Graves |
|:--|:-:|:-:|:-:|
| **Élevées** | 🟨 À surveiller | 🟥 À traiter | 🟥 À traiter en priorité |
| **Moyennes** | 🟩 À accepter | 🟨 À surveiller | 🟥 À traiter |
| **Faibles** | 🟩 À accepter | 🟩 À accepter | 🟨 Prévoir un plan B |

Pour chaque risque placé dans la zone rouge, on propose une **mesure** : ce qu'on fera pour qu'il arrive moins souvent, ou pour que ses conséquences soient moins graves.

> *Exemple :* « Les photos arrivent en retard. » → **Mesure :** fixer au 15 janvier la date limite de remise des contenus et prévoir des photos temporaires.

---

## La liste des problèmes techniques à prévoir

C'est la synthèse de tout le travail de ce soir. Pour chaque problème, on écrit :

| Problème | Pourquoi c'est un problème | Ce qu'il faut vérifier ou demander |
|:--|:--|:--|
| *Ex. :* Les réservations Viator doivent partager les places avec le nouveau site. | Sinon, les doubles réservations continuent. | Quels outils de réservation sont connectés à Viator ? Combien coûtent-ils ? |

Cette liste servira directement à l'**évaluation 1**, puis à la rencontre avec le client à la **séance 9**.

---

## L'évaluation 1 : ce qui s'en vient

<div class="bg-yellow-50 border border-yellow-200 text-yellow-900 rounded-lg p-4 mb-5">
<strong>Rapport de faisabilité technique — Évaluation technique (20 %)</strong><br>
<ul class="list-disc pl-5">
  <li>En équipe, sur le mandat Aventure Saint-Maurice.</li>
  <li>Remise à la <strong>séance 7 (11 novembre)</strong> sur LÉA. Le français compte pour 10 %.</li>
  <li>Le rapport <strong>décrit la situation</strong> : ce que le projet exige, ce qui le contraint, les risques et les technologies qui existent pour le réaliser. Il ne recommande <strong>encore rien</strong> : les choix viendront à l'évaluation 2.</li>
  <li>Le travail de ce soir (contraintes, exigences, risques, problèmes à prévoir) en est le point de départ.</li>
</ul>
</div>

---

## À faire maintenant

[Lab 02 — Radiographie du mandat](./../../labs/lab02-radiographie-mandat)
