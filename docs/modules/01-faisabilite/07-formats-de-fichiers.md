---
title: "Séance 7 — Les formats de fichiers du Web"
aside: false
---

# Séance 7 — Les formats de fichiers du Web

## Objectifs
- Choisir le **format** d'un fichier selon ce qu'il contient et l'endroit où il sera affiché.
- Appliquer les **règles de qualité** de la mise en ligne : poids, dimensions, texte de remplacement, sous-titres, contraste.
- Comprendre ce que demande l'**évaluation 2 : la proposition technique**.

## Déroulement de la séance

La séance se fait en deux temps : **la remise, toute la matière et la présentation de l'évaluation 2 d'abord**, en grand groupe, puis **le reste de la soirée pour le Lab 07**, en équipe.

| Heure | Activité |
|:--|:--|
| 18 h 30 | Remise de l'évaluation 1 et retour sur le Lab 06 |
| 18 h 45 | Un fichier, trois questions · les formats d'image, de vidéo et de document |
| 19 h 05 | Activité 1 — Quel format pour quel fichier ? |
| 19 h 25 | Les règles de qualité pour la mise en ligne |
| 19 h 35 | Activité 2 — Le texte de remplacement |
| 19 h 50 | L'évaluation 2 : la proposition technique |
| 20 h 10 | Les consignes du Lab 07 et ce qu'il y a à faire à la maison |
| 20 h 15 | Marge pour les questions |
| 20 h 25 | Pause |
| 20 h 40 | [Lab 07 — Alléger les médias de Patrick](./../../labs/lab07-alleger-les-medias), en équipe, jusqu'à la fin de la soirée |

Le **retour en grand groupe** sur le Lab 07 aura lieu **au début de la séance 8**.

---

## Remise de l'évaluation 1 et retour sur le Lab 06 {#retour-lab-06}

<div class="bg-yellow-50 border border-yellow-200 text-yellow-900 rounded-lg p-4 mb-5">
<strong>Avant de commencer : votre rapport est-il bien sur LÉA ?</strong><br>
Ouvrez LÉA et vérifiez que le fichier déposé est le bon : <code>eval1-equipeN-nom1-nom2-nom3.docx</code>, avec les annexes A, B et C. Un fichier vide ou une ancienne version, ça arrive : c'est maintenant qu'on le voit, pas dans deux semaines.
</div>

Avez-vous des **questions de dernière minute** sur l'évaluation 1 ? Posez-les dans le chat.

Écrivez ensuite dans le chat **le défaut que vous avez corrigé le plus souvent** dans votre rapport, en quelques mots. On regarde ensemble ceux qui reviennent : ce sont les mêmes pièges qui vous attendent dans la proposition technique, où il faudra cette fois **choisir**, chiffrer et justifier.

---

## Un fichier, trois questions

Patrick a envoyé ses photos, son logo, un extrait de drone et la grille des tarifs :

<DossierPatrick />

Avant de choisir un format, posez trois questions sur chaque fichier :

1. **Qu'est-ce que c'est ?** Une photo, un dessin (logo, icône, carte), une vidéo, un document, une police de caractères.
2. **Où va-t-il, et à quelle taille ?** Une bannière sur toute la largeur de l'écran, une photo dans le texte, une petite icône dans le menu.
3. **Qui le regarde, et comment ?** Sur un téléphone, au quai, avec un réseau faible. Avec un lecteur d'écran. En anglais.

### Deux familles d'images

| | Une **image matricielle** | Une **image vectorielle** |
|:--|:--|:--|
| **Ce que c'est** | Une grille de pixels, chacun avec sa couleur | Des formes décrites par des calculs : un cercle, une ligne, un texte |
| **Pour quoi** | Les photos | Les logos, les icônes, les pictogrammes |
| **Si on l'agrandit** | Elle devient floue, puis pixelisée | Elle reste nette à toutes les tailles |
| **Formats** | JPEG, PNG, WebP, AVIF | SVG |

<MatricielVectoriel />

Une image matricielle se compresse **avec perte** (on retire des détails que l'œil ne voit presque pas : idéal pour une photo) ou **sans perte** (on ne retire rien : nécessaire pour du texte et des aplats, où la moindre bavure se voit).

<PerteSansPerte />

### Les formats d'image

| Format | Pour quoi | Transparence | Ce qu'il faut savoir |
|:--|:--|:-:|:--|
| **JPEG** | Les photos | Non | Lu partout, depuis toujours. Avec perte. Le repli quand rien d'autre ne fonctionne. |
| **PNG** | Les captures d'écran, les dessins avec du texte, les logos sans SVG | Oui | Sans perte. **Énorme pour une photo** : 5 à 10 fois le poids d'un JPEG. |
| **WebP** | Les photos et les dessins | Oui | Avec ou sans perte. Environ 25 à 35 % plus léger qu'un JPEG de même qualité. Lu par tous les navigateurs actuels. |
| **AVIF** | Les photos | Oui | Encore plus léger que WebP, mais plus lent à produire. Lu par les navigateurs à jour depuis 2024 : on prévoit un repli en WebP ou en JPEG. |
| **SVG** | Les logos, les icônes, les cartes simples | Oui | Vectoriel : quelques Ko, net à toutes les tailles. Inutile pour une photo. |

Deux formats qu'on reçoit souvent, et qu'on ne met **jamais** en ligne tels quels :
- **HEIC** : le format des photos d'iPhone. À part Safari, les navigateurs ne l'affichent pas. On le convertit.
- **GIF animé** : lourd, limité à 256 couleurs. Une courte vidéo MP4 fait la même chose pour une fraction du poids.

### Les vidéos

| Format | Ce qu'il faut savoir |
|:--|:--|
| **MP4** (codec H.264) | Lu par tous les navigateurs et tous les appareils. Le choix par défaut. |
| **WebM** (codecs VP9 ou AV1) | Souvent plus léger à qualité égale. Certains appareils Apple plus anciens ne le lisent pas : on l'offre **avec** un MP4 en repli. |

Ce que Patrick envoie, un fichier **.MOV en 4K**, est fait pour le montage, pas pour le Web : une minute de vidéo 4K de drone pèse facilement plusieurs centaines de Mo. Pour une vidéo d'arrière-plan, on retire le son, on réduit à 1920 px de large (souvent 1280 suffisent), on garde 10 à 20 secondes en boucle, et on prévoit une **image d'affiche** (*poster*) qui s'affiche pendant le chargement.

Les longues vidéos (une visite guidée de 4 minutes, par exemple) ne s'hébergent généralement pas sur le site lui-même. C'est justement la question Q4 du rapport : vous en avez fait le tour à l'évaluation 1.

### Les documents et les polices

- **PDF** : pour ce qu'on **imprime, signe ou conserve** tel quel (un formulaire de groupe, une décharge à imprimer). Pas pour l'information que tout le monde doit lire : les horaires et les tarifs vont dans la page, en texte. Un PDF **numérisé** est une image : un lecteur d'écran ne peut pas le lire.
- **WOFF2** : le format des polices de caractères pour le Web, compressé et lu par tous les navigateurs actuels. Avant de mettre une police en ligne, on vérifie que sa **licence** permet l'usage sur un site. On se limite à deux familles, et à peu de graisses (normal, gras).

---

### Activité 1 — Quel format pour quel fichier ? {#activite-1}

<div class="bg-blue-50 border border-blue-200 text-blue-900 rounded-lg p-4 mb-5">
<strong>Consigne (10 min, en équipe, puis retour en grand groupe)</strong><br>
Huit fichiers, tirés de l'envoi de Patrick et des besoins du mandat.
<ol class="list-decimal pl-5">
  <li>Pour chaque fichier, écrivez en une phrase <strong>pourquoi</strong> vous choisiriez tel format.</li>
  <li>Cliquez ensuite sur le format. Un contour pointillé vert indique le meilleur choix, s'il est différent du vôtre.</li>
</ol>
</div>

<QuelFormat />

**Ce qu'il faut retenir :** le format découle de **ce que contient le fichier**, pas de ce qu'on a reçu. Une photo reste une photo, qu'elle arrive en PNG, en HEIC ou en JPEG; un tableau de prix reste du texte, même numérisé. Et le meilleur format ne sert à rien si le fichier est **six fois trop grand** pour l'endroit où il s'affiche.

---

## Les règles de qualité pour la mise en ligne

### Le poids et les dimensions

Le plus gros gain ne vient pas du format : il vient des **dimensions**. La photo du coucher de soleil fait 6000 px de large; la bannière de l'accueil en affiche au plus 1920. Les 24 millions de pixels de la photo, contre 2,5 millions affichés : le visiteur télécharge **dix fois trop d'image**.

<EchelleDimensions />

**La règle du double :** une image n'a pas besoin de faire plus de **deux fois la largeur à laquelle elle s'affiche** (les écrans haute densité affichent deux pixels pour un). Un logo affiché à 200 px : 400 px au plus.

| Où va le fichier | Largeur visée | Poids visé |
|:--|:-:|:-:|
| Bannière ou photo sur toute la largeur | 1920 px (2560 au plus) | moins de 300 Ko |
| Photo dans le texte | 1200 px | moins de 150 Ko |
| Vignette (une carte d'activité, par exemple) | 600 px | moins de 60 Ko |
| Logo, icônes | SVG (sinon 2 × la taille affichée) | moins de 10 Ko |
| Vidéo d'arrière-plan, sans son, 10 à 20 s | 1280 à 1920 px | moins de 4 Mo |
| Toutes les images de la page d'accueil, ensemble | | moins de 1,5 Mo |

Ces repères ne sont pas des normes officielles. Ce sont des cibles raisonnables, qui aident à respecter l'exigence du rapport : **la page d'accueil s'affiche en moins de 2,5 secondes sur un téléphone**. Avec l'extrait de drone de Patrick tel quel (16 Mo pour 8 secondes), c'est impossible au quai, et difficile même à Trois-Rivières.

### Jusqu'où compresser ?

Une fois la photo à la bonne largeur, le réglage de **qualité** décide du reste. Comparez :

<ComparerQualite />

### L'accessibilité des médias

Le programme d'aide qui a financé les kayaks adaptés exige que l'information sur l'offre adaptée soit « accessible à tous ». La référence, pour le Web, ce sont les règles **WCAG** (*Web Content Accessibility Guidelines*). Quatre d'entre elles touchent directement les médias :

| La règle | Ce qu'elle demande | Pour Aventure Saint-Maurice |
|:--|:--|:--|
| **Texte de remplacement** (WCAG 1.1.1) | Chaque image qui informe a un texte qui dit ce qu'elle apporte (l'attribut `alt`). Une image décorative a un `alt` vide. | La photo du kayak adapté décrit l'équipement. La photo de décor derrière un titre est sautée. |
| **Sous-titres** (WCAG 1.2.2) | Une vidéo où l'on parle a des sous-titres (un fichier `.vtt`, à côté de la vidéo). | La vidéo de sécurité où Patrick explique comment pagayer, en français et en anglais. |
| **Pause** (WCAG 2.2.2) | Ce qui bouge seul plus de 5 secondes peut être mis en pause. | La vidéo de drone en boucle a un bouton pause visible. |
| **Contraste** (WCAG 1.4.3) | Le texte se détache du fond : un rapport d'au moins 4,5 pour 1 (3 pour 1 pour un grand titre). | Le titre blanc posé sur la vidéo de drone a besoin d'un voile sombre derrière lui. |

<VoileContraste />

### Ce qu'on vérifie aussi avant de mettre une photo en ligne

- **Le nom du fichier** : en minuscules, sans espace ni accent, et qui dit ce qu'il contient. `via-ferrata-falaise.webp`, pas `via ferrata FALAISE final(2).png`.
- **Les personnes sur la photo** : une personne qu'on peut reconnaître doit avoir donné son autorisation (c'est le droit à l'image, au Code civil du Québec). Pour un enfant, c'est le parent qui signe. Rappel : le quart des participants de l'été 2026 étaient mineurs.
- **Les métadonnées** : une photo de téléphone peut contenir l'endroit exact où elle a été prise. Squoosh les retire au moment de la compression.

### Activité 2 — Le texte de remplacement {#activite-2}

<div class="bg-blue-50 border border-blue-200 text-blue-900 rounded-lg p-4 mb-5">
<strong>Consigne (10 min, en équipe, puis retour en grand groupe)</strong><br>
Six images du futur site, chacune à un endroit précis.
<ol class="list-decimal pl-5">
  <li>Choisissez le meilleur texte de remplacement parmi les trois proposés. Une des options peut être un <code>alt</code> vide.</li>
  <li>Si aucun ne vous convient tout à fait, écrivez votre version.</li>
</ol>
</div>

<TexteRemplacement />

**Ce qu'il faut retenir :** le texte de remplacement ne décrit pas l'image : il dit **ce qu'elle apporte à cet endroit de la page**. La même photo peut mériter une description sur une page et un `alt` vide sur une autre.

---

## L'évaluation 2 : la proposition technique {#evaluation-2}

Le rapport que vous venez de remettre décrivait la situation, sans rien recommander. La **proposition technique** tranche : elle complète le même document.

<div class="bg-yellow-50 border border-yellow-200 text-yellow-900 rounded-lg p-4 mb-5">
<strong>En bref</strong><br>
<ul class="list-disc pl-5">
  <li><strong>Remise :</strong> mercredi <strong>9 décembre, 18 h 30</strong>, sur LÉA (séance 11). 20 %, dont 10 % pour le français.</li>
  <li><strong>Ce qui s'ajoute :</strong> les choix techniques, les formats et les règles de mise en ligne, les adaptations aux contraintes, le temps, l'argent et la recommandation finale.</li>
  <li><strong>Ce qui change dans la partie 1 :</strong> le résumé et la portée sont réécrits, et les commentaires reçus pour l'évaluation 1 sont appliqués.</li>
</ul>
<a href="./../../evaluations/evaluation-2"><strong>Lire l'énoncé complet de l'évaluation 2</strong></a>
</div>

Ce que chaque séance vous apporte pour la proposition :

| Séance | Pour la proposition |
|:-:|:--|
| 7 (ce soir) | Lab 07 : les **formats** et les règles de mise en ligne (section 9) |
| 8 (18 nov.) | Estimer le **temps** et monter le **devis** (sections 11 et 12). Votre rapport de l'évaluation 1 vous est rendu corrigé |
| 9 (25 nov.) | La **rencontre avec le client** : les réponses à vos questions de la section 7 |
| 10 (2 déc.) | Période de questions sur l'évaluation 2 |
| 11 (9 déc.) | **Remise** avant 18 h 30 |

Votre rapport de l'évaluation 1 vous sera rendu corrigé **au plus tard le 18 novembre**, avec les commentaires à appliquer. D'ici là, commencez par ce qui n'en dépend pas : le choix des outils, à partir de vos essais et de vos tableaux de l'évaluation 1.

---

## À faire maintenant

[Lab 07 — Alléger les médias de Patrick](./../../labs/lab07-alleger-les-medias), en équipe, jusqu'à la fin de la soirée. Téléchargez le dossier de Patrick et la fiche avant la pause : le dossier fait 36 Mo.

---

## À faire à la maison {#a-faire-a-la-maison}

- **Lire l'[énoncé de l'évaluation 2](./../../evaluations/evaluation-2)** en équipe et noter vos questions : on y répond au début de la séance 8.
- **Terminer le Lab 07** si vous n'avez pas eu le temps d'alléger tous les fichiers. La fiche sert directement à la section 9 de la proposition.
- **Rassembler vos tableaux de comparaison** de l'évaluation 1, pour votre question et les quatre autres : la section 8 de la proposition part de là.

---

## Avant la séance 8 (18 novembre)

<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text">Copier vos réponses des activités 1 et 2 dans vos notes</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Déposer la fiche du Lab 07 et vos fichiers allégés dans l'équipe Teams du cours</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Lire l'énoncé de l'évaluation 2 et écrire vos questions</span></label></li>
</ul>
