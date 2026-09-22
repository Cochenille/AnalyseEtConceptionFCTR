<script setup lang="ts">
import { computed, reactive } from "vue";

type Sorte = "technique" | "organisationnelle" | "ressources";
type Situation = { texte: string; reponse: Sorte; pourquoi: string };

const SORTES: { cle: Sorte; titre: string; question: string; }[] = [
  { cle: "technique", titre: "Technique", question: "Que permet ou impose la technologie ?" },
  { cle: "organisationnelle", titre: "Organisationnelle", question: "Comment le client fonctionne-t-il ?" },
  { cle: "ressources", titre: "De ressources", question: "De quoi dispose-t-on ?" },
];

const SITUATIONS: Situation[] = [
  {
    texte: "Le site doit être en ligne avant l'ouverture de la terrasse, dans 5 semaines.",
    reponse: "ressources",
    pourquoi: "Le temps disponible est une ressource, au même titre que l'argent et les compétences.",
  },
  {
    texte: "Le forfait Wix actuel ne permet pas de vendre des cartes-cadeaux.",
    reponse: "technique",
    pourquoi: "C'est la plateforme elle-même qui limite ce qui est possible.",
  },
  {
    texte: "C'est la gérante qui mettra le menu à jour, et elle n'a jamais utilisé WordPress.",
    reponse: "organisationnelle",
    pourquoi: "On parle de qui fait quoi chez le client et de sa façon de fonctionner.",
  },
  {
    texte: "Le système de réservation utilisé en salle n'offre aucun moyen de se connecter au site.",
    reponse: "technique",
    pourquoi: "Deux systèmes qui ne communiquent pas : c'est une limite de la technologie.",
  },
  {
    texte: "Le budget total pour la première année est de 4 000 $.",
    reponse: "ressources",
    pourquoi: "Le budget est la ressource la plus évidente d'un projet.",
  },
  {
    texte: "Le site doit être offert en français, conformément à la Charte de la langue française.",
    reponse: "organisationnelle",
    pourquoi: "Les lois et règles que le client doit respecter font partie de son contexte organisationnel.",
  },
];

const choix = reactive<(Sorte | null)[]>(SITUATIONS.map(() => null));
const score = computed(() => choix.filter((c, n) => c === SITUATIONS[n].reponse).length);
const repondues = computed(() => choix.filter((c) => c !== null).length);

function reinitialiser() {
  choix.fill(null);
}
</script>

<template>
  <section class="tq">
    <div class="tq-sortes">
      <div v-for="s in SORTES" :key="s.cle" class="tq-sorte" :class="'tq-sorte--' + s.cle">
        <strong>{{ s.titre }}</strong>
        <span>{{ s.question }}</span>
      </div>
    </div>

    <p class="tq-consigne">Pour chaque situation, choisissez la sorte de contrainte <strong>principale</strong>.</p>

    <ol class="tq-liste">
      <li v-for="(sit, n) in SITUATIONS" :key="n" class="tq-item">
        <p class="tq-texte">{{ sit.texte }}</p>
        <div class="tq-boutons" role="group" :aria-label="'Sorte de contrainte pour la situation ' + (n + 1)">
          <button
            v-for="s in SORTES"
            :key="s.cle"
            type="button"
            class="tq-btn"
            :class="{
              'is-bon': choix[n] !== null && s.cle === sit.reponse,
              'is-mauvais': choix[n] === s.cle && s.cle !== sit.reponse,
            }"
            :aria-pressed="choix[n] === s.cle"
            @click="choix[n] = s.cle"
          >
            {{ s.titre }}
          </button>
        </div>
        <p v-if="choix[n] !== null" class="tq-retro" :class="choix[n] === sit.reponse ? 'is-bon' : 'is-mauvais'">
          <strong>{{ choix[n] === sit.reponse ? "Oui." : "Pas tout à fait." }}</strong>
          {{ sit.pourquoi }}
        </p>
      </li>
    </ol>

    <div class="tq-pied">
      <span>
        <strong>{{ score }}</strong> / {{ SITUATIONS.length }} bonnes réponses
        <span v-if="repondues < SITUATIONS.length" class="tq-reste">({{ SITUATIONS.length - repondues }} à faire)</span>
      </span>
      <button type="button" class="tq-reset" @click="reinitialiser">Recommencer</button>
    </div>
  </section>
</template>

<style scoped>
.tq {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.tq-sortes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.5rem;
}
.tq-sorte {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  padding: 0.6rem 0.75rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
  line-height: 1.4;
}
.tq-sorte strong {
  display: block;
  font-size: 0.875rem;
}
.tq-sorte span {
  color: var(--vp-c-text-2);
}
.tq-consigne {
  margin: 0.9rem 0 0.5rem !important;
  font-size: 0.875rem;
}
.tq-liste {
  margin: 0 !important;
  padding-left: 1.25rem !important;
}
.tq-item {
  margin: 0 !important;
  padding: 0.6rem 0;
  border-top: 1px solid var(--vp-c-divider);
}
.tq-texte {
  margin: 0 0 0.4rem !important;
  font-size: 0.9rem;
  line-height: 1.5;
}
.tq-boutons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}
.tq-btn {
  padding: 0.25rem 0.7rem;
  border-radius: 999px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
  font-weight: 500;
  transition: border-color 0.15s, background-color 0.15s;
}
.tq-btn:hover {
  border-color: var(--vp-c-brand-1);
}
.tq-btn.is-bon {
  border-color: var(--vp-c-green-2);
  background: var(--vp-c-green-soft);
  color: var(--vp-c-green-1);
}
.tq-btn.is-mauvais {
  border-color: var(--vp-c-red-2);
  background: var(--vp-c-red-soft);
  color: var(--vp-c-red-1);
}
.tq-retro {
  margin: 0.4rem 0 0 !important;
  font-size: 0.8rem;
  line-height: 1.5;
  color: var(--vp-c-text-2);
}
.tq-retro.is-bon strong {
  color: var(--vp-c-green-1);
}
.tq-retro.is-mauvais strong {
  color: var(--vp-c-red-1);
}
.tq-pied {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.875rem;
}
.tq-reste {
  color: var(--vp-c-text-2);
}
.tq-reset {
  padding: 0.3rem 0.7rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.tq-reset:hover {
  border-color: var(--vp-c-brand-1);
}
</style>
