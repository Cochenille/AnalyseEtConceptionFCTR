# Générateur de fiches de lab

La fiche Word **est** le lab : l'étudiant n'a pas besoin de suivre la page Web en parallèle. La page Web du lab se limite aux objectifs, au téléchargement de la fiche, à l'horaire et à la remise; elle ne répète aucune consigne.

## Utilisation

```bash
pip install python-docx pyyaml
python outils/fiches/generer_fiche.py outils/fiches/labs/lab06.yaml
```

La fiche est écrite dans `docs/public/fiches/`. Pour un essai, ajoutez `--sortie chemin/essai.docx`.

Pour un nouveau lab : copier [`modele.yaml`](modele.yaml) dans `outils/fiches/labs/labNN.yaml`, le remplir, générer. On modifie le YAML, jamais le `.docx` à la main.

## Structure d'une partie (toujours la même)

1. **Titre et durée**
2. **À faire :** une phrase, avec le nombre attendu (« 6 essais »)
3. **Vous aurez besoin de :** ce qui vient d'une autre partie ou d'un lab précédent, nommé précisément (facultatif)
4. **Les blocs :**
   - `liste` : une rangée par élément (B1, E1…). Les en-têtes sont des questions, avec une précision dessous. Une rangée d'exemple grisée, puis exactement le nombre de rangées attendues.
   - `grille` : une rangée par critère, une colonne par objet comparé (Outil 1, Outil 2…). Colonne d'exemple grisée si un critère a un `exemple`.
   - `texte` : une case libre pour un court paragraphe.
5. **Avant de passer à la suite, cochez :** 2 à 4 cases au plus. Elles remplacent la liste de remise.

Les conseils (outils, mots-clés, cas particuliers) vont dans la section `aide`, à la fin de la fiche, jamais entre les consignes.

## Conventions pour toute la session

| Quoi | Convention |
|:--|:--|
| Fichier remis | `labNN-equipeN.docx`, déposé dans l'équipe Teams du cours |
| Captures | `labNN-equipeN-E3-01.png` (lab, équipe, élément, numéro) |
| Numérotation | B (besoins), S (sources), E (essais), C (constats), R (risques) : les mêmes d'un lab à l'autre |
| Enchaînement | Une fiche ne contient jamais un tableau à remplir dans un lab suivant |
