<script setup lang="ts">
// Séance 9, étape 1 : une phrase du client, une question pour creuser, deux besoins possibles.
const BRANCHES = [
  {
    qui: "Si c'est pour les clients",
    dit: "« Réserver sans appeler, sur mon téléphone. »",
    besoin: "Un site qui fonctionne bien sur téléphone",
  },
  {
    qui: "Si c'est pour les guides",
    dit: "« Voir la liste au quai, même sans réseau. »",
    besoin: "Une liste qu'on ouvre au chalet, avant de partir",
  },
];
const GESTES = [
  { n: 1, titre: "Repérer la solution déguisée", ex: "« une application », « un clavardage », « comme le site de… »" },
  { n: 2, titre: "Demander à quoi ça sert", ex: "« Qu'est-ce que vos clients feraient avec ? »" },
  { n: 3, titre: "Reformuler et faire confirmer", ex: "« Si je comprends bien, vous voulez que… C'est bien ça ? »" },
];
</script>

<template>
  <figure class="fig7 up">
    <div class="up-schema">
      <div class="up-col">
        <span class="up-etiquette">Ce qu'on entend</span>
        <div class="up-bulle">« Il faudrait une application. »</div>
        <span class="up-source">Le beau-frère de Patrick (mandat)</span>
      </div>

      <div class="up-fleche" aria-hidden="true"><span>on creuse</span></div>

      <div class="up-col">
        <span class="up-etiquette">Ce qu'on demande</span>
        <div class="up-relance">« Qu'est-ce que les gens feraient avec l'application ? »</div>
      </div>

      <div class="up-fleche" aria-hidden="true"><span>la réponse</span></div>

      <div class="up-col up-branches">
        <span class="up-etiquette">Ce qu'elle veut vraiment</span>
        <div v-for="b in BRANCHES" :key="b.qui" class="up-branche">
          <span class="up-qui">{{ b.qui }}</span>
          <span class="up-dit">{{ b.dit }}</span>
          <strong class="up-besoin">{{ b.besoin }}</strong>
        </div>
      </div>
    </div>

    <ol class="up-gestes">
      <li v-for="g in GESTES" :key="g.n">
        <span class="up-n">{{ g.n }}</span>
        <div>
          <strong>{{ g.titre }}</strong>
          <span>{{ g.ex }}</span>
        </div>
      </li>
    </ol>

    <figcaption>
      <strong>Une phrase, deux projets différents.</strong> Sans cette question, on construit une application que personne n'a demandée. Tant que la cliente n'a pas dit « oui, c'est ça », le besoin est une hypothèse.
    </figcaption>
  </figure>
</template>

<style scoped>
.up-schema {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr) auto minmax(0, 1.3fr);
  gap: 0.5rem;
  align-items: center;
}
.up-col { display: grid; gap: 0.35rem; align-content: center; }
.up-etiquette {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--vp-c-text-2);
}
.up-bulle {
  position: relative;
  padding: 0.7rem 0.8rem;
  border-radius: 0.9rem 0.9rem 0.9rem 0.2rem;
  background: var(--vp-c-yellow-soft);
  font-weight: 700;
  line-height: 1.35;
}
.up-source { font-size: 0.72rem; color: var(--vp-c-text-2); }
.up-relance {
  padding: 0.7rem 0.8rem;
  border: 2px dashed var(--vp-c-brand-1);
  border-radius: 0.7rem;
  background: var(--vp-c-bg);
  font-size: 0.85rem;
  font-style: italic;
  line-height: 1.4;
}
.up-fleche {
  display: grid;
  justify-items: center;
  gap: 0.1rem;
  min-width: 3.2rem;
  font-size: 0.65rem;
  color: var(--vp-c-text-2);
}
.up-fleche::after {
  content: "→";
  color: var(--vp-c-brand-1);
  font-size: 1.8rem;
  font-weight: 800;
  line-height: 1;
}
.up-branches { gap: 0.45rem; }
.up-branche {
  display: grid;
  gap: 0.15rem;
  padding: 0.55rem 0.7rem;
  border-left: 4px solid var(--vp-c-green-2);
  border-radius: 0.4rem;
  background: var(--vp-c-bg);
  line-height: 1.35;
}
.up-qui { font-size: 0.72rem; font-weight: 700; color: var(--vp-c-text-2); }
.up-dit { font-size: 0.8rem; font-style: italic; }
.up-besoin { font-size: 0.88rem; color: var(--vp-c-green-1); }

.up-gestes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 0.5rem;
  margin: 1rem 0 0 !important;
  padding: 0.8rem 0 0 !important;
  border-top: 1px solid var(--vp-c-divider);
  list-style: none;
}
.up-gestes li { display: flex; gap: 0.55rem; align-items: flex-start; margin: 0 !important; }
.up-gestes li div { display: grid; gap: 0.1rem; line-height: 1.35; }
.up-gestes li strong { font-size: 0.85rem; }
.up-gestes li span:not(.up-n) { font-size: 0.75rem; color: var(--vp-c-text-2); }
.up-n {
  display: grid;
  place-items: center;
  flex-shrink: 0;
  width: 1.7rem;
  height: 1.7rem;
  border-radius: 50%;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-weight: 800;
}

@media (max-width: 720px) {
  .up-schema { grid-template-columns: 1fr; }
  .up-fleche { min-width: 0; }
  .up-fleche::after { content: "↓"; font-size: 1.4rem; }
}
</style>
