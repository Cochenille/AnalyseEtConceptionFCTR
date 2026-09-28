<script setup lang="ts">
import { computed, reactive } from "vue";

type Sorte = "fonctionnelle" | "non-fonctionnelle";
type Enonce = { texte: string; reponse: Sorte; pourquoi: string };

const SORTES: { cle: Sorte; titre: string; question: string }[] = [
  { cle: "fonctionnelle", titre: "Ce que le site fait", question: "Une action ou un service offert à quelqu'un" },
  { cle: "non-fonctionnelle", titre: "Comment il le fait", question: "Une qualité : vitesse, sécurité, accessibilité, compatibilité…" },
];

const ENONCES: Enonce[] = [
  {
    texte: "Un client peut acheter une carte-cadeau et la recevoir par courriel.",
    reponse: "fonctionnelle",
    pourquoi: "C'est un service offert au visiteur : acheter quelque chose.",
  },
  {
    texte: "Sur un téléphone, la page d'accueil s'affiche en moins de 3 secondes.",
    reponse: "non-fonctionnelle",
    pourquoi: "On ne décrit pas une action, mais la vitesse à laquelle le site répond.",
  },
  {
    texte: "Le guide voit la liste des participants d'un départ.",
    reponse: "fonctionnelle",
    pourquoi: "C'est une action que le site permet à un utilisateur précis : le guide.",
  },
  {
    texte: "Les réponses aux questions de santé ne sont visibles que par le personnel autorisé.",
    reponse: "non-fonctionnelle",
    pourquoi: "C'est une exigence de sécurité et de confidentialité (Loi 25) sur une fonction qui existe déjà.",
  },
  {
    texte: "Le site fonctionne sur Safari pour iPhone et sur Chrome pour Android.",
    reponse: "non-fonctionnelle",
    pourquoi: "C'est une exigence de compatibilité : sur quels navigateurs tout doit fonctionner.",
  },
  {
    texte: "Un client peut s'inscrire à la liste d'attente d'un départ complet.",
    reponse: "fonctionnelle",
    pourquoi: "C'est une action offerte au visiteur.",
  },
  {
    texte: "Toutes les fonctions peuvent être utilisées au clavier, sans souris.",
    reponse: "non-fonctionnelle",
    pourquoi: "C'est une exigence d'accessibilité : elle s'applique à toutes les fonctions du site.",
  },
  {
    texte: "Mélanie peut changer le prix d'une activité.",
    reponse: "fonctionnelle",
    pourquoi: "C'est une action offerte à un utilisateur : l'administratrice du site.",
  },
];

const choix = reactive<(Sorte | null)[]>(ENONCES.map(() => null));
const score = computed(() => choix.filter((c, n) => c === ENONCES[n].reponse).length);
const repondues = computed(() => choix.filter((c) => c !== null).length);

function reinitialiser() {
  choix.fill(null);
}
</script>

<template>
  <section class="te">
    <div class="te-sortes">
      <div v-for="s in SORTES" :key="s.cle" class="te-sorte">
        <strong>{{ s.titre }}</strong>
        <span>{{ s.question }}</span>
      </div>
    </div>

    <p class="te-consigne">Pour chaque énoncé, dites s'il décrit <strong>ce que le site fait</strong> ou <strong>comment il le fait</strong>.</p>

    <ol class="te-liste">
      <li v-for="(en, n) in ENONCES" :key="n" class="te-item">
        <p class="te-texte">{{ en.texte }}</p>
        <div class="te-boutons" role="group" :aria-label="'Sorte d\'exigence pour l\'énoncé ' + (n + 1)">
          <button
            v-for="s in SORTES"
            :key="s.cle"
            type="button"
            class="te-btn"
            :class="{
              'is-bon': choix[n] !== null && s.cle === en.reponse,
              'is-mauvais': choix[n] === s.cle && s.cle !== en.reponse,
            }"
            :aria-pressed="choix[n] === s.cle"
            @click="choix[n] = s.cle"
          >
            {{ s.titre }}
          </button>
        </div>
        <p v-if="choix[n] !== null" class="te-retro" :class="choix[n] === en.reponse ? 'is-bon' : 'is-mauvais'">
          <strong>{{ choix[n] === en.reponse ? "Oui." : "Pas tout à fait." }}</strong>
          {{ en.pourquoi }}
        </p>
      </li>
    </ol>

    <div class="te-pied">
      <span>
        <strong>{{ score }} / {{ ENONCES.length }}</strong> bonnes réponses
        <span v-if="repondues < ENONCES.length" class="te-reste">({{ ENONCES.length - repondues }} à faire)</span>
      </span>
      <button type="button" class="te-reset" @click="reinitialiser">Recommencer</button>
    </div>
  </section>
</template>

<style scoped>
.te {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.te-sortes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.5rem;
}
.te-sorte {
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
.te-sorte strong {
  font-size: 0.875rem;
}
.te-sorte span {
  color: var(--vp-c-text-2);
}
.te-consigne {
  margin: 0.9rem 0 0.5rem !important;
  font-size: 0.875rem;
}
.te-liste {
  margin: 0 !important;
  padding-left: 1.25rem !important;
}
.te-item {
  margin: 0 !important;
  padding: 0.6rem 0;
  border-top: 1px solid var(--vp-c-divider);
}
.te-texte {
  margin: 0 0 0.4rem !important;
  font-size: 0.9rem;
  line-height: 1.5;
}
.te-boutons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}
.te-btn {
  padding: 0.25rem 0.7rem;
  border-radius: 999px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
  font-weight: 500;
  transition: border-color 0.15s, background-color 0.15s;
}
.te-btn:hover {
  border-color: var(--vp-c-brand-1);
}
.te-btn.is-bon {
  border-color: var(--vp-c-green-2);
  background: var(--vp-c-green-soft);
  color: var(--vp-c-green-1);
}
.te-btn.is-mauvais {
  border-color: var(--vp-c-red-2);
  background: var(--vp-c-red-soft);
  color: var(--vp-c-red-1);
}
.te-retro {
  margin: 0.4rem 0 0 !important;
  font-size: 0.8rem;
  line-height: 1.5;
  color: var(--vp-c-text-2);
}
.te-retro.is-bon strong {
  color: var(--vp-c-green-1);
}
.te-retro.is-mauvais strong {
  color: var(--vp-c-red-1);
}
.te-pied {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.875rem;
}
.te-reste {
  color: var(--vp-c-text-2);
}
.te-reset {
  padding: 0.3rem 0.7rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.te-reset:hover {
  border-color: var(--vp-c-brand-1);
}
</style>
