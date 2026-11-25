<script setup lang="ts">
// Séance 9, étape 2 : l'anatomie d'un récit utilisateur, deux exemples et un contre-exemple.
const PARTIES = [
  { cle: "qui", mot: "En tant que", role: "Qui ?", regle: "Une personne précise, pas « l'utilisateur »" },
  { cle: "quoi", mot: "je veux", role: "Quoi ?", regle: "Une action, sans nommer d'outil" },
  { cle: "pourquoi", mot: "afin de", role: "Pourquoi ?", regle: "Le besoin : la partie la plus importante" },
];
const EXEMPLES = [
  ["cliente pressée", "commander mon pain du samedi depuis mon téléphone", "ne pas faire la file"],
  ["guide", "voir les allergies de mon groupe avant de quitter le chalet", "réagir vite au quai, même sans réseau"],
];
const MANQUES = ["Personne", "Aucune raison", "Impose déjà un outil"];
</script>

<template>
  <figure class="fig7 rc">
    <div class="rc-anatomie">
      <div v-for="p in PARTIES" :key="p.cle" class="rc-partie" :class="'is-' + p.cle">
        <span class="rc-mot">{{ p.mot }} …</span>
        <span class="rc-role">{{ p.role }}</span>
        <span class="rc-regle">{{ p.regle }}</span>
      </div>
    </div>

    <div class="rc-exemples">
      <p v-for="(e, i) in EXEMPLES" :key="i" class="rc-phrase">
        <span class="is-qui"><b>En tant que</b> {{ e[0] }},</span>
        <span class="is-quoi"><b>je veux</b> {{ e[1] }},</span>
        <span class="is-pourquoi"><b>afin de</b> {{ e[2] }}.</span>
      </p>
    </div>

    <div class="rc-contre">
      <span class="rc-barre">« Le site utilise Bookeo. »</span>
      <span class="rc-verdict">Ce n'est pas un récit :</span>
      <span v-for="m in MANQUES" :key="m" class="rc-manque">✕ {{ m }}</span>
    </div>

    <figcaption>
      <strong>Ce soir, on apprend à reconnaître un récit.</strong> On les écrira à la séance 10, à partir des réponses de Mélanie.
    </figcaption>
  </figure>
</template>

<style scoped>
.rc { --c-qui: var(--vp-c-brand-1); --s-qui: var(--vp-c-brand-soft);
      --c-quoi: var(--vp-c-purple-1); --s-quoi: var(--vp-c-purple-soft);
      --c-pourquoi: var(--vp-c-green-1); --s-pourquoi: var(--vp-c-green-soft); }
.is-qui { --c: var(--c-qui); --s: var(--s-qui); }
.is-quoi { --c: var(--c-quoi); --s: var(--s-quoi); }
.is-pourquoi { --c: var(--c-pourquoi); --s: var(--s-pourquoi); }

.rc-anatomie { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.3rem; }
.rc-partie {
  display: grid;
  gap: 0.15rem;
  padding: 0.65rem 0.75rem;
  background: var(--s);
  line-height: 1.3;
}
.rc-partie:first-child { border-radius: 0.7rem 0 0 0.7rem; }
.rc-partie:last-child { border-radius: 0 0.7rem 0.7rem 0; outline: 2px solid var(--c); outline-offset: -2px; }
.rc-mot { font-weight: 800; font-size: 1.05rem; color: var(--c); }
.rc-role { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; color: var(--vp-c-text-2); }
.rc-regle { font-size: 0.8rem; }

.rc-exemples { display: grid; gap: 0.45rem; margin-top: 0.8rem; }
.rc-phrase {
  margin: 0 !important;
  padding: 0.55rem 0.7rem;
  border-radius: 0.6rem;
  background: var(--vp-c-bg);
  line-height: 1.9;
  font-size: 0.9rem;
}
.rc-phrase span {
  padding: 0.1rem 0.3rem;
  border-radius: 0.3rem;
  background: var(--s);
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
}
.rc-phrase b { color: var(--c); }

.rc-contre {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  align-items: center;
  margin-top: 0.8rem;
  padding: 0.55rem 0.7rem;
  border-radius: 0.6rem;
  background: var(--vp-c-red-soft);
  font-size: 0.82rem;
}
.rc-barre { font-weight: 700; text-decoration: line-through; text-decoration-color: var(--vp-c-red-1); text-decoration-thickness: 2px; }
.rc-verdict { margin-left: 0.3rem; font-weight: 600; }
.rc-manque {
  padding: 0.12rem 0.55rem;
  border-radius: 999px;
  background: var(--vp-c-bg);
  color: var(--vp-c-red-1);
  font-weight: 600;
}
@media (max-width: 640px) {
  .rc-anatomie { grid-template-columns: 1fr; }
  .rc-partie:first-child { border-radius: 0.7rem 0.7rem 0 0; }
  .rc-partie:last-child { border-radius: 0 0 0.7rem 0.7rem; }
}
</style>
