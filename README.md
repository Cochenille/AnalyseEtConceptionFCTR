# AnalyseEtConceptionFCTR
Site du cours Analyse et Conception pour la formation continue du Cégep de Trois-rivières

Site VitePress publié sur GitHub Pages : https://cochenille.github.io/AnalyseEtConceptionFCTR/

## Développement

```bash
npm install
npm run docs:dev
```

## Déploiement

Chaque push sur `main` déclenche `.github/workflows/deploy.yml`, qui construit le site et le publie
sur la branche `gh-pages`.
