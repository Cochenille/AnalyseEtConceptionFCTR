<script setup lang="ts">
// Séance 8 : trois façons d'entrer dans le budget, et ce qu'on ne coupe jamais.
const FACONS = [
  { l: "A", titre: "Enlever", sous: "une fonctionnalité de poids 1", question: "Que perd le client ?" },
  { l: "B", titre: "Changer d'outil", sous: "moins d'heures à configurer", question: "Moins cher sur trois ans, ou seulement l'an 1 ?" },
  { l: "C", titre: "Livrer en étapes", sous: "l'essentiel pour la date ferme", question: "Qu'est-ce qui doit être prêt le 1er mars ?" },
];
const JAMAIS = ["les tests", "la formation", "l'accessibilité"];
</script>

<template>
  <figure class="fig7 f3">
    <div class="f3-cartes">
      <div v-for="f in FACONS" :key="f.l" class="f3-carte">
        <span class="f3-lettre">{{ f.l }}</span>
        <strong>{{ f.titre }}</strong>
        <span class="f3-sous">{{ f.sous }}</span>
        <span class="f3-q">{{ f.question }}</span>
      </div>
    </div>
    <div class="f3-jamais">
      <span class="f3-jamais-titre">On ne coupe jamais</span>
      <span v-for="j in JAMAIS" :key="j" class="f3-pastille">✕ {{ j }}</span>
    </div>
    <figcaption>
      <strong>On ne baisse pas les heures pour que « ça rentre ».</strong> On présente au client une option par famille, avec ce qu'elle fait économiser et ce qu'elle lui coûte. C'est lui qui choisit.
    </figcaption>
  </figure>
</template>

<style scoped>
.f3-cartes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 0.6rem;
}
.f3-carte {
  display: grid;
  justify-items: center;
  gap: 0.2rem;
  padding: 0.8rem 0.6rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.7rem;
  background: var(--vp-c-bg);
  text-align: center;
  line-height: 1.3;
}
.f3-lettre {
  display: grid;
  place-items: center;
  width: 2.2rem;
  height: 2.2rem;
  margin-bottom: 0.2rem;
  border-radius: 50%;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-weight: 800;
  font-size: 1.1rem;
}
.f3-sous { font-size: 0.75rem; color: var(--vp-c-text-2); }
.f3-q {
  margin-top: 0.4rem;
  padding-top: 0.4rem;
  border-top: 1px dashed var(--vp-c-divider);
  font-size: 0.78rem;
  font-style: italic;
}
.f3-jamais {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  align-items: center;
  margin-top: 0.8rem;
  padding: 0.55rem 0.7rem;
  border-radius: 0.6rem;
  background: var(--vp-c-red-soft);
  font-size: 0.8rem;
}
.f3-jamais-titre { font-weight: 700; margin-right: 0.3rem; }
.f3-pastille {
  padding: 0.15rem 0.55rem;
  border-radius: 999px;
  background: var(--vp-c-bg);
  color: var(--vp-c-red-1);
  font-weight: 600;
}
</style>
