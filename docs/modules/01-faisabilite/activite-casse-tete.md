---
title: "Activité — Le trajet d'une page Web"
aside: false
---

# Activité — Le trajet d'une page Web

<div class="bg-blue-50 border border-blue-200 text-blue-900 rounded-lg p-4 mb-5">
<strong>Objectif de l'activité</strong><br>
Reconstruire, avec vos propres mots, tout ce qui doit exister pour qu'une personne voie le site d'un restaurant sur son téléphone.
</div>

## Mise en situation

Une cliente tape `bistro-exemple.ca` dans son téléphone pour consulter le menu et réserver une table.
En quelques secondes, la page s'affiche. **Que s'est-il passé entre les deux ?**

---

## Consignes

### Étape 1 — Le trajet (10 min)
Placez les cartes **dans l'ordre du trajet**, de la cliente qui tape l'adresse jusqu'à la page affichée.

<div class="bg-yellow-50 border border-yellow-200 text-yellow-900 rounded-lg p-4 mb-5">
<strong>Attention</strong><br>
Certaines cartes ne se placent pas directement sur le trajet. Mettez-les dans la zone <em>À côté du trajet</em> et préparez-vous à expliquer à quoi elles servent.
</div>

---

## Le casse-tête

<TrajetCartes />

<div class="bg-slate-50 border border-slate-200 text-slate-800 rounded-lg p-4 mb-5">
<strong>Votre travail est conservé dans ce navigateur.</strong><br>
Vous pouvez fermer l'onglet et y revenir : les cartes restent où vous les avez laissées. Par contre, rien n'est envoyé au professeur — notez votre trajet dans le document de votre équipe avant la mise en commun.
</div>

---

## Le corrigé

<details class="mb-5">
<summary><strong>Voir le corrigé</strong> (à ouvrir seulement une fois votre propre trajet terminé)</summary>

### Le trajet

| | Carte | Ce qui se passe |
|:-:|:--|:--|
| 1 | **Appareil** | La cliente sort son téléphone. C'est le point de départ de tout le trajet. |
| 2 | **Navigateur** | C'est lui, et non le téléphone, qui sait comment aller chercher une page Web. |
| 3 | **Nom de domaine** | L'adresse tapée, `bistro-exemple.ca`. Pour le navigateur, ce n'est encore qu'un texte. |
| 4 | **DNS** | Le navigateur demande : « à quelle adresse IP se trouve ce nom ? ». Le DNS répond. |
| 5 | **Certificat SSL/TLS** | Le navigateur ouvre une connexion **chiffrée** vers cette adresse. C'est le cadenas. |
| 6 | **Hébergement** | Le serveur où vit le site, celui qui répond à cette adresse IP. |
| 7 | **Plateforme** | Le logiciel qui tourne sur ce serveur et qui **fabrique** la page demandée. |
| 8 | **Contenus** | Ce que la plateforme assemble : les textes, les photos, le menu. C'est ce que la cliente voulait voir. |

### À côté du trajet

| Carte | Pourquoi elle n'est pas sur le trajet |
|:--|:--|
| **Registraire** | Il intervient **avant**, une fois par année : c'est chez lui qu'on loue le nom de domaine. Pendant l'affichage de la page, il ne fait rien. |
| **Courriel professionnel** | `info@bistro-exemple.ca` utilise le **même nom de domaine**, mais c'est un service complètement séparé du site. Changer d'hébergeur sans précaution peut le briser. |
| **Service externe** | La réservation, le paiement ou la livraison se déclenchent **après** l'affichage de la page, quand la cliente clique. Ce n'est pas le site qui les fait. |

<div class="bg-blue-50 border border-blue-200 text-blue-900 rounded-lg p-4 mt-5">
<strong>Ce corrigé n'est pas la seule réponse acceptable.</strong><br>
Plusieurs ordres se défendent — par exemple, on peut placer le certificat SSL/TLS plus loin sur le trajet, ou mettre le nom de domaine à côté du trajet plutôt que dessus. Ce qui compte, c'est que <strong>votre</strong> ordre s'explique. Si votre trajet diffère et que vous savez pourquoi, dites-le pendant la mise en commun.
</div>

</details>

---

### Étape 2 — Mise en commun
On compare les trajets. Là où les équipes ne sont pas d'accord, c'est souvent là que se cache une notion importante.

Suite : [Séance 1 — Ce qu'il faut pour mettre un site en ligne](./01-mettre-un-site-en-ligne#le-trajet-d-une-page-web)
