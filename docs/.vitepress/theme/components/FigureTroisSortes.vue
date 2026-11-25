<script setup lang="ts">
// Séance 9, étape 2 : trier chaque réponse de la cliente en trois sortes, et savoir où chacune va.
const SORTES = [
  {
    cle: "quoi",
    symbole: "1",
    titre: "Ce que le site doit faire",
    signe: "Une personne fait une action",
    exemple: "« Les clients commandent leur pain du samedi en ligne. »",
    devient: "Un récit utilisateur",
    ou: "Séance 10",
  },
  {
    cle: "comment",
    symbole: "2",
    titre: "Comment il doit le faire",
    signe: "Une qualité qu'on peut mesurer",
    exemple: "« La page s'ouvre en moins de 3 secondes sur un téléphone. »",
    devient: "Un critère ou une règle de qualité",
    ou: "Évaluation 2 : 2.1, 3.1",
  },
  {
    cle: "decision",
    symbole: "3",
    titre: "Une décision de la cliente",
    signe: "Une règle d'affaires qu'aucun outil ne choisit",
    exemple: "« Une commande non ramassée n'est pas remboursée. »",
    devient: "D (décidé) ou A (à éclaircir) au compte rendu",
    ou: "Évaluation 2 : 1.3, 7.3",
  },
];
</script>

<template>
  <figure class="fig7 ts">
    <div class="ts-source">
      <span class="ts-bulle">Une réponse de la cliente</span>
      <span class="ts-q">De quelle sorte est-elle ?</span>
    </div>
    <div class="ts-branches" aria-hidden="true">↓</div>
    <div class="ts-colonnes">
      <article v-for="s in SORTES" :key="s.cle" class="ts-col" :class="'is-' + s.cle">
        <header>
          <span class="ts-symbole">{{ s.symbole }}</span>
          <strong>{{ s.titre }}</strong>
        </header>
        <p class="ts-ligne"><span>Le signe</span>{{ s.signe }}</p>
        <p class="ts-exemple">{{ s.exemple }}</p>
        <p class="ts-devient"><span>Devient</span><strong>{{ s.devient }}</strong></p>
        <p class="ts-ou">{{ s.ou }}</p>
      </article>
    </div>
    <figcaption>
      <strong>Les exemples viennent de la boulangerie.</strong> Une même réponse peut contenir deux sortes : « on prend les commandes jusqu'à 14 h la veille » est une décision de la propriétaire, et « le site ferme les commandes tout seul » est ce que le site doit faire pour l'appliquer.
    </figcaption>
  </figure>
</template>

<style scoped>
.ts { --c-quoi: var(--vp-c-brand-1); --s-quoi: var(--vp-c-brand-soft);
      --c-comment: var(--vp-c-green-1); --s-comment: var(--vp-c-green-soft);
      --c-decision: var(--vp-c-yellow-1); --s-decision: var(--vp-c-yellow-soft); }
.ts-source { display: grid; justify-items: center; gap: 0.25rem; }
.ts-bulle {
  padding: 0.45rem 1rem;
  border-radius: 999px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  font-weight: 700;
}
.ts-q { font-size: 0.75rem; color: var(--vp-c-text-2); }
.ts-branches {
  margin: 0.1rem 0 0.3rem;
  text-align: center;
  color: var(--vp-c-text-2);
  font-size: 1.4rem;
  font-weight: 800;
  line-height: 1;
}
.ts-colonnes { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.6rem; }
.ts-col {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  padding: 0.75rem;
  border-radius: 0.7rem;
  border-top: 5px solid var(--c);
  background: var(--vp-c-bg);
  line-height: 1.35;
}
.ts-col.is-quoi { --c: var(--c-quoi); --s: var(--s-quoi); }
.ts-col.is-comment { --c: var(--c-comment); --s: var(--s-comment); }
.ts-col.is-decision { --c: var(--c-decision); --s: var(--s-decision); }
.ts-col header { display: flex; gap: 0.5rem; align-items: center; }
.ts-symbole {
  display: grid;
  place-items: center;
  flex-shrink: 0;
  width: 1.9rem;
  height: 1.9rem;
  border-radius: 50%;
  background: var(--s);
  color: var(--c);
  font-size: 0.95rem;
  font-weight: 800;
}
.ts-col p { margin: 0 !important; }
.ts-ligne, .ts-devient { display: grid; gap: 0.05rem; font-size: 0.82rem; }
.ts-ligne span, .ts-devient span {
  font-size: 0.66rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--vp-c-text-2);
}
.ts-exemple {
  padding: 0.45rem 0.55rem;
  border-radius: 0.5rem;
  background: var(--s);
  font-size: 0.8rem;
  font-style: italic;
}
.ts-devient strong { color: var(--c); }
.ts-ou {
  margin-top: auto !important;
  padding-top: 0.4rem;
  border-top: 1px dashed var(--vp-c-divider);
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
@media (max-width: 640px) {
  .ts-colonnes { grid-template-columns: 1fr; margin-top: 0.6rem; }
}
</style>
