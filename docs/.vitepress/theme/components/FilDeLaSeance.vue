<script setup lang="ts">
// Séance 8 : le plan de la soirée en quatre étapes. Chaque étape produit ce dont la suivante a besoin.
const ETAPES = [
  {
    n: 1,
    ancre: "#choisir-avec-des-criteres",
    titre: "Choisir",
    question: "Quel outil prendre, et pourquoi ?",
    produit: "Des critères avec un poids",
    rapport: "Sections 2.1 et 2.2",
  },
  {
    n: 2,
    ancre: "#estimer-le-travail",
    titre: "Estimer",
    question: "Combien d'heures de travail ?",
    produit: "Une liste de tâches, chacune en heures",
    rapport: "Section 5.1 · Lab 08, partie 1",
  },
  {
    n: 3,
    ancre: "#echeancier",
    titre: "Planifier",
    question: "Est-ce prêt à temps ?",
    produit: "Des étapes datées, avec un coussin",
    rapport: "Section 5.2 · Lab 08, partie 2",
  },
  {
    n: 4,
    ancre: "#devis",
    titre: "Chiffrer",
    question: "Est-ce que ça entre dans le budget ?",
    produit: "Un devis et trois options",
    rapport: "Section 6 · Lab 08, parties 3 et 4",
  },
];
</script>

<template>
  <figure class="fig7 fs">
    <ol class="fs-etapes">
      <li v-for="(e, i) in ETAPES" :key="e.n" class="fs-etape">
        <a :href="e.ancre" class="fs-carte">
          <span class="fs-n">{{ e.n }}</span>
          <strong class="fs-titre">{{ e.titre }}</strong>
          <span class="fs-question">{{ e.question }}</span>
          <span class="fs-produit"><span class="fs-etiq">On obtient</span>{{ e.produit }}</span>
          <span class="fs-rapport"><span class="fs-etiq">Ça va dans</span>{{ e.rapport }}</span>
        </a>
        <span v-if="i < ETAPES.length - 1" class="fs-fleche" aria-hidden="true">→</span>
      </li>
    </ol>
    <figcaption>
      <strong>Les quatre étapes de ce soir, dans l'ordre.</strong> Chaque étape se sert de ce que la précédente a
      produit : les heures viennent des tâches, l'échéancier vient des heures, le devis vient des heures et des outils
      choisis. On les fait d'abord pour la boulangerie, puis vous les refaites pour Aventure Saint-Maurice dans le Lab 08.
    </figcaption>
  </figure>
</template>

<style scoped>
.fs-etapes {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.2rem;
  list-style: none;
  margin: 0 !important;
  padding: 0 !important;
}
.fs-etape { position: relative; margin: 0 !important; }
.fs-carte {
  display: grid;
  gap: 0.35rem;
  align-content: start;
  height: 100%;
  padding: 0.7rem 0.75rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.6rem;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1) !important;
  text-decoration: none !important;
  transition: border-color 0.15s;
}
.fs-carte:hover, .fs-carte:focus-visible { border-color: var(--vp-c-brand-1); }
.fs-n {
  display: inline-grid;
  place-items: center;
  width: 1.7rem;
  height: 1.7rem;
  border-radius: 999px;
  background: var(--vp-c-brand-1);
  color: var(--vp-c-white);
  font-weight: 700;
  font-size: 0.9rem;
}
.fs-titre { font-size: 1rem; }
.fs-question { font-size: 0.85rem; font-style: italic; color: var(--vp-c-text-2); }
.fs-produit, .fs-rapport { display: grid; font-size: 0.8rem; line-height: 1.35; }
.fs-etiq {
  font-size: 0.66rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--vp-c-text-3);
}
.fs-fleche {
  position: absolute;
  top: 50%;
  right: -1.05rem;
  transform: translateY(-50%);
  color: var(--vp-c-text-3);
  font-size: 1rem;
}
@media (max-width: 760px) {
  .fs-etapes { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .fs-fleche { display: none; }
}
@media (max-width: 420px) {
  .fs-etapes { grid-template-columns: 1fr; }
}
</style>
