---
title: "Lab 01 — Enquête technique : comparer deux sites"
aside: false
---

# 🔎 Lab 01 — Enquête technique : comparer deux sites

<div class="bg-blue-50 border border-blue-200 text-blue-900 rounded-lg p-4 mb-5">
<strong>Objectifs du laboratoire</strong><br>
<ul class="list-disc pl-5">
  <li>Utiliser des outils gratuits pour découvrir comment un site Web est construit.</li>
  <li>Relever les ressources techniques d'un site : plateforme, hébergement, domaine, sécurité, services externes.</li>
  <li>Évaluer la performance et l'affichage mobile d'un site.</li>
  <li>Comparer deux sites et <strong>justifier un jugement</strong> à partir d'observations.</li>
</ul>
</div>

<div class="bg-yellow-50 border border-yellow-200 text-yellow-900 rounded-lg p-4 mb-5">
<strong>Modalités</strong><br>
<ul class="list-disc pl-5">
  <li>En <strong>duo</strong> (salle de sous-groupe).</li>
  <li>Durée : environ 1 h 30, puis mise en commun en grand groupe.</li>
  <li>Remise : la fiche d'observation remplie, déposée dans le <strong>forum du cours</strong>. Ce travail est <strong>formatif</strong> (non noté).</li>
</ul>
</div>

---

## Contexte

Deux restaurants peuvent offrir le même service, mais avec des sites construits de façons complètement différentes.
Votre travail : **enquêter** sur deux sites, comme le ferait un analyste avant de conseiller un client.

À la fin, vous devrez répondre à une question de jugement :

> **Lequel de ces deux sites serait le plus facile à faire évoluer ? Pourquoi ?**

Il n'y a pas de réponse évidente. Ce qui compte, c'est la qualité de vos **observations** et de votre **justification**.

---

## Les paires de sites

L'enseignant attribue une paire à chaque duo.

| Paire | Thème | Site A | Site B |
|:-:|:--|:--|:--|
| **1** | Deux poutineries | [La Banquise](https://labanquise.com) | [Casse-Croûte Courteau](https://lecourteau.com) |
| **2** | Deux chaînes | [Thaï Express](https://thaiexpress.ca) | [Ashton](https://ashtonrestaurants.ca) |
| **3** | Deux restaurants qui vendent leurs produits | [Schwartz's](https://schwartzsdeli.com) | [Commensal](https://commensal.com) |
| **4** | Deux tables gastronomiques | [Joe Beef](https://joebeef.com) | [Épi, buvette de quartier](https://epibuvette.ca) |

---

## Préparation (10 min)

### 1. Télécharger la fiche
<a href="./../fiches/lab01-fiche-observation.docx" download>📄 Télécharger la fiche d'observation (Word)</a>

Une seule fiche par duo. Travaillez dans un document partagé (OneDrive, Google Docs…) pour la remplir à deux.

### 2. Se répartir les rôles

| Personne 1 — **Ordinateur** | Personne 2 — **Mobile** |
|:--|:--|
| Wappalyzer, code source, domaine, certificat | PageSpeed Insights, mode appareil, test sur un vrai téléphone |

Les deux personnes **installent quand même tous les outils** : vous inversez les rôles pour le site B.

### 3. Installer les outils

<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text">Installer l'extension <a href="https://www.wappalyzer.com/apps/" target="_blank">Wappalyzer</a> dans Chrome, Edge ou Firefox, puis l'épingler à la barre d'outils</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Ouvrir <a href="https://pagespeed.web.dev/" target="_blank">PageSpeed Insights</a> dans un onglet</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Ouvrir <a href="https://lookup.icann.org/" target="_blank">ICANN Lookup</a> (recherche WHOIS) dans un onglet</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Vérifier que les outils de développement s'ouvrent avec <kbd>F12</kbd></span></label></li>
</ul>

---

## Partie 1 — Première impression (10 min)

Parcourez les deux sites **sans outil**, comme un client ordinaire.

<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text">À qui s'adresse le site ? Qu'est-ce qu'on peut y faire (consulter le menu, réserver, commander, acheter, créer un compte…) ?</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Quels liens mènent vers un autre site (réservation, livraison, paiement, réseaux sociaux) ?</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Votre impression générale en trois mots</span></label></li>
</ul>

---

## Partie 2 — Les technologies (15 min)

Sur la page d'accueil de chaque site, cliquez sur l'icône **Wappalyzer**.

<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text">La plateforme ou le CMS (WordPress, Shopify, Squarespace, Next.js…)</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">L'hébergement, le CDN et le serveur Web</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Les services externes : réservation, paiement, commerce en ligne</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Les outils d'analyse et de publicité (Google Analytics, Meta Pixel…)</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Les bibliothèques JavaScript et leurs versions (p. ex. jQuery)</span></label></li>
</ul>

<div class="bg-red-50 border border-red-300 text-red-900 rounded-lg p-4 mb-5">
<strong>Wappalyzer peut se tromper</strong><br>
Il devine les technologies à partir d'indices. Il en rate parfois, ou en voit qui n'y sont pas. Si un résultat vous surprend, cherchez une preuve dans le code source (partie 5).
</div>

---

## Partie 3 — Domaine et sécurité (15 min)

### Le nom de domaine
Dans **ICANN Lookup**, entrez le nom de domaine (sans `https://` ni `www`).

<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text">La date de création du domaine (depuis combien d'années existe-t-il ?)</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Le registraire (chez qui le domaine est loué)</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">La date d'expiration</span></label></li>
</ul>

### Le certificat
Cliquez sur l'icône à gauche de l'adresse, puis sur **La connexion est sécurisée → Le certificat est valide** (les libellés varient selon le navigateur).

<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text">L'émetteur du certificat (Let's Encrypt, Google, Sectigo…)</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Sa date d'expiration</span></label></li>
</ul>

### Témoins et langue
Ouvrez le site dans une **fenêtre de navigation privée**.

<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text">Une bannière de témoins (cookies) apparaît-elle ? Permet-elle de <strong>refuser</strong> ?</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Dans quelle langue le site s'affiche-t-il par défaut ?</span></label></li>
</ul>

---

## Partie 4 — Performance et mobile (20 min)

### PageSpeed Insights
Analysez l'**adresse de la page d'accueil** de chaque site.

<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text">Onglet <strong>Mobile</strong> : score de performance, score d'accessibilité, Largest Contentful Paint (LCP)</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Onglet <strong>Ordinateur</strong> : score de performance</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Dans les diagnostics : un problème principal qui ralentit le site</span></label></li>
</ul>

<div class="bg-yellow-50 border border-yellow-200 text-yellow-900 rounded-lg p-4 mb-5">
<strong>Les scores varient</strong><br>
Deux analyses du même site peuvent donner des scores différents. Lancez l'analyse <strong>deux fois</strong> et notez les deux résultats.
</div>

### L'affichage sur téléphone
Dans le navigateur, ouvrez les outils de développement (<kbd>F12</kbd>), puis le **mode appareil** (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>M</kbd>). Choisissez un téléphone dans la liste. Si possible, ouvrez aussi le site sur **votre vrai téléphone**.

<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text">Le texte est-il lisible sans zoomer ?</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Le menu est-il facile à ouvrir et à utiliser ?</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Les boutons importants (réserver, commander, appeler) sont-ils faciles à toucher ?</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Y a-t-il un défilement horizontal ou des éléments coupés ?</span></label></li>
</ul>

---

## Partie 5 — Le code source (10 min)

Affichez le code source de la page d'accueil (<kbd>Ctrl</kbd> + <kbd>U</kbd>), puis cherchez (<kbd>Ctrl</kbd> + <kbd>F</kbd>) :

<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text"><code>&lt;title&gt;</code> : le titre est-il clair et descriptif ?</span></label></li>
  <li><label><input type="checkbox"><span class="check-text"><code>description</code> : y a-t-il une description pour les moteurs de recherche ?</span></label></li>
  <li><label><input type="checkbox"><span class="check-text"><code>lang=</code> : quelle langue est déclarée ?</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Un indice qui confirme la plateforme trouvée par Wappalyzer (p. ex. <code>wp-content</code>, <code>cdn.shopify.com</code>, <code>squarespace</code>, <code>_next</code>)</span></label></li>
</ul>

---

## Partie 6 — Les contraintes probables (10 min)

Pour chaque site, imaginez une contrainte probable de chaque sorte. Appuyez-vous sur vos observations.

| Sorte | Question |
|:--|:--|
| **Technique** | Qu'est-ce que la technologie de ce site rendrait difficile ? |
| **Organisationnelle** | Qui doit probablement mettre ce site à jour ? Est-ce simple pour cette personne ? |
| **De ressources** | Qu'est-ce que ce site coûte probablement à entretenir : argent, temps, compétences ? |

---

## Partie 7 — Le verdict (10 min)

> **Lequel de ces deux sites serait le plus facile à faire évoluer ? Pourquoi ?**

Par exemple : le restaurant veut ajouter la commande en ligne, traduire le site ou changer complètement son image.

Rédigez une justification de **5 à 8 lignes** qui s'appuie sur **au moins trois observations** de votre fiche.

---

## 🏆 Défi bonus

Trouvez un site de restaurant québécois dont le **score de performance mobile** dans PageSpeed Insights est **plus bas** que ceux de votre paire.
Notez l'adresse, le score et **deux causes** probables de sa lenteur.

---

## Remise

<ul class="checklist">
  <li><label><input type="checkbox"><span class="check-text">La fiche est complète pour les <strong>deux</strong> sites</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Le verdict est justifié par au moins trois observations</span></label></li>
  <li><label><input type="checkbox"><span class="check-text">Le fichier est nommé <code>lab01-paireN-nom1-nom2.docx</code></span></label></li>
  <li><label><input type="checkbox"><span class="check-text">La fiche est déposée dans le forum du cours</span></label></li>
</ul>

---

## Mise en commun

En grand groupe, chaque duo présente en une minute :
- la plateforme de chacun de ses deux sites ;
- les scores de performance mobile ;
- son verdict et **la** meilleure raison qui l'appuie.

On remplit ensemble un tableau des quatre paires pour comparer les approches.
