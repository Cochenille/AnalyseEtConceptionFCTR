<script setup lang="ts">
// Séance 9, étape 3 : le chemin d'une réponse de Mélanie, de la question jusqu'à l'évaluation 2.
const ETAPES = [
  {
    n: 1,
    titre: "Vos questions",
    quand: "Lab 08, partie 4",
    lignes: ["Cinq questions choisies dans le rapport 1", "Une question, une décision, dans ses mots à elle"],
  },
  {
    n: 2,
    titre: "La rencontre",
    quand: "Lab 09, partie 1",
    lignes: ["Les mots de Mélanie : un chiffre, une date, un nom", "Toutes les réponses, pas seulement les vôtres"],
    marques: true,
  },
  {
    n: 3,
    titre: "Le compte rendu",
    quand: "Lab 09, partie 2",
    lignes: ["Seulement ce qui change la proposition"],
    listes: true,
  },
  {
    n: 4,
    titre: "La proposition",
    quand: "Évaluation 2",
    sections: [
      ["1.3", "vos questions, ses réponses, ce qu'elles changent"],
      ["2 · 4", "un critère, un choix, une adaptation"],
      ["5.2", "les dates promises par la cliente"],
      ["7.3", "ce qui reste à éclaircir"],
    ],
  },
];
</script>

<template>
  <figure class="fig7 dq">
    <ol class="dq-chemin">
      <li v-for="e in ETAPES" :key="e.n" class="dq-etape" :class="{ 'is-fin': e.sections }">
        <header>
          <span class="dq-n">{{ e.n }}</span>
          <div>
            <strong>{{ e.titre }}</strong>
            <span class="dq-quand">{{ e.quand }}</span>
          </div>
        </header>
        <ul v-if="e.lignes" class="dq-lignes">
          <li v-for="l in e.lignes" :key="l">{{ l }}</li>
        </ul>
        <div v-if="e.marques" class="dq-marques">
          Chaque réponse marquée
          <span class="dq-pastille is-d">D</span> ou <span class="dq-pastille is-a">A</span>
        </div>
        <div v-if="e.listes" class="dq-listes">
          <div class="dq-liste is-d"><b>D</b> Décidé<span>avec ses chiffres et ses dates</span></div>
          <div class="dq-liste is-a"><b>A</b> À éclaircir<span>qui répond, avant quand, et ce qu'on suppose</span></div>
        </div>
        <dl v-if="e.sections" class="dq-sections">
          <template v-for="s in e.sections" :key="s[0]">
            <dt>{{ s[0] }}</dt>
            <dd>{{ s[1] }}</dd>
          </template>
        </dl>
      </li>
    </ol>
    <figcaption>
      <strong>« Je vous reviens d'ici vendredi » n'est pas une réponse :</strong> c'est un A, avec une personne et une date. Le compte rendu s'écrit le soir même : le lendemain, on a oublié la moitié des chiffres.
    </figcaption>
  </figure>
</template>

<style scoped>
.dq-chemin {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.1rem;
  margin: 0 !important;
  padding: 0 !important;
  list-style: none;
}
.dq-etape {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin: 0 !important;
  padding: 0.7rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.7rem;
  background: var(--vp-c-bg);
  line-height: 1.35;
}
.dq-etape:not(:last-child)::after {
  content: "→";
  position: absolute;
  right: -0.95rem;
  top: 1.1rem;
  color: var(--vp-c-brand-1);
  font-weight: 800;
}
.dq-etape.is-fin { border: 2px solid var(--vp-c-brand-1); }
.dq-etape header { display: flex; gap: 0.5rem; align-items: center; }
.dq-etape header div { display: grid; }
.dq-quand { font-size: 0.7rem; color: var(--vp-c-text-2); }
.dq-n {
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
.dq-lignes { margin: 0 !important; padding-left: 1rem !important; font-size: 0.78rem; }
.dq-lignes li { margin: 0.1rem 0 !important; }
.dq-marques { font-size: 0.78rem; }
.dq-pastille, .dq-liste b {
  display: inline-grid;
  place-items: center;
  width: 1.35rem;
  height: 1.35rem;
  border-radius: 0.3rem;
  font-weight: 800;
  font-size: 0.75rem;
}
.is-d.dq-pastille, .dq-liste.is-d b { background: var(--vp-c-green-soft); color: var(--vp-c-green-1); }
.is-a.dq-pastille, .dq-liste.is-a b { background: var(--vp-c-yellow-soft); color: var(--vp-c-yellow-1); }
.dq-listes { display: grid; gap: 0.35rem; }
.dq-liste {
  display: grid;
  grid-template-columns: auto 1fr;
  column-gap: 0.4rem;
  align-items: center;
  font-size: 0.82rem;
  font-weight: 700;
}
.dq-liste span { grid-column: 2; font-size: 0.72rem; font-weight: 400; color: var(--vp-c-text-2); }
.dq-sections {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.3rem 0.5rem;
  margin: 0;
  font-size: 0.78rem;
}
.dq-sections dt {
  padding: 0.05rem 0.4rem;
  border-radius: 0.3rem;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-weight: 700;
  text-align: center;
  white-space: nowrap;
}
.dq-sections dd { margin: 0; }
@media (max-width: 860px) {
  .dq-chemin { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .dq-etape:nth-child(2)::after { content: none; }
}
@media (max-width: 560px) {
  .dq-chemin { grid-template-columns: 1fr; }
  .dq-etape:not(:last-child)::after { content: "↓"; right: auto; left: 50%; top: auto; bottom: -1.05rem; }
}
</style>
