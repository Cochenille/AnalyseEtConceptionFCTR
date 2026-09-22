<script setup lang="ts">
import { computed, ref } from "vue";

type Scenario = {
  lettre: string;
  nom: string;
  construction: number;
  annuel: number;
  detailAnnuel: string;
};

// Montants fictifs, dans les ordres de grandeur de l'accroche.
const SCENARIOS: Scenario[] = [
  {
    lettre: "A",
    nom: "Café de quartier",
    construction: 300,
    annuel: 450,
    detailAnnuel: "abonnement Wix + nom de domaine",
  },
  {
    lettre: "B",
    nom: "Bistro gastronomique",
    construction: 9000,
    annuel: 2200,
    detailAnnuel: "hébergement, domaine, extensions, réservation en ligne, entretien",
  },
  {
    lettre: "C",
    nom: "Chaîne de 60 restaurants",
    construction: 180000,
    annuel: 45000,
    detailAnnuel: "serveurs, licences, sécurité, équipe d'entretien",
  },
];

const ANNEES = [1, 2, 3, 4, 5];

const choix = ref(1);
const survol = ref<number | null>(null);
const s = computed(() => SCENARIOS[choix.value]);

const donnees = computed(() =>
  ANNEES.map((a) => ({
    annee: a,
    construction: s.value.construction,
    recurrent: s.value.annuel * a,
  }))
);

// Géométrie
const L = 600;
const H = 260;
const M = { haut: 16, droite: 16, bas: 34, gauche: 64 };
const largeurTrace = L - M.gauche - M.droite;
const hauteurTrace = H - M.haut - M.bas;
const bande = largeurTrace / ANNEES.length;
const largeurBarre = Math.min(56, bande * 0.55);

function arrondiHaut(v: number) {
  const p = Math.pow(10, Math.floor(Math.log10(v)));
  const n = v / p;
  const pas = n <= 1 ? 1 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 5 ? 5 : 10;
  return pas * p;
}
const max = computed(() => arrondiHaut(s.value.construction + s.value.annuel * ANNEES.length));
const graduations = computed(() => [0, 0.25, 0.5, 0.75, 1].map((f) => f * max.value));
const y = (v: number) => M.haut + hauteurTrace - (v / max.value) * hauteurTrace;
const x = (idx: number) => M.gauche + bande * idx + (bande - largeurBarre) / 2;

const fmt = (v: number) =>
  new Intl.NumberFormat("fr-CA", { maximumFractionDigits: 0 }).format(v) + " $";
const fmtCourt = (v: number) =>
  v >= 1000
    ? new Intl.NumberFormat("fr-CA", { maximumFractionDigits: 1 }).format(v / 1000) + " k$"
    : fmt(v);

// Segment arrondi seulement en haut (extrémité de donnée)
function segment(x0: number, yHaut: number, yBas: number, w: number, arrondi: boolean) {
  const h = Math.max(0, yBas - yHaut);
  const r = arrondi ? Math.min(4, h, w / 2) : 0;
  return `M${x0},${yBas} V${yHaut + r} Q${x0},${yHaut} ${x0 + r},${yHaut} H${x0 + w - r} Q${x0 + w},${yHaut} ${x0 + w},${yHaut + r} V${yBas} Z`;
}

// Infobulle à côté de la barre survolée, à gauche pour les dernières colonnes
function styleBulle(idx: number) {
  const aGauche = idx >= ANNEES.length - 2;
  const bord = aGauche ? x(idx) - 8 : x(idx) + largeurBarre + 8;
  return {
    left: (bord / L) * 100 + "%",
    transform: aGauche ? "translateX(-100%)" : "none",
  };
}

const croisement = computed(() => {
  const n = Math.floor(s.value.construction / s.value.annuel) + 1;
  return n;
});
</script>

<template>
  <figure class="ca viz">
    <div class="ca-tete">
      <figcaption class="ca-titre">
        Coût total cumulé d'un site, année après année
        <span class="ca-sous">Montants fictifs, pour illustrer le principe</span>
      </figcaption>
      <div class="ca-choix" role="radiogroup" aria-label="Restaurant">
        <button
          v-for="(sc, n) in SCENARIOS"
          :key="sc.lettre"
          type="button"
          role="radio"
          :aria-checked="choix === n"
          class="ca-onglet"
          :class="{ 'is-on': choix === n }"
          @click="choix = n"
        >
          {{ sc.lettre }} — {{ sc.nom }}
        </button>
      </div>
    </div>

    <div class="ca-legende">
      <span><i class="ca-pastille ca-pastille--1"></i>Payé une fois : construction ({{ fmt(s.construction) }})</span>
      <span><i class="ca-pastille ca-pastille--2"></i>Payé chaque année : {{ s.detailAnnuel }} ({{ fmt(s.annuel) }}/an)</span>
    </div>

    <div class="ca-zone">
      <svg :viewBox="`0 0 ${L} ${H}`" class="ca-svg" role="img" :aria-label="`Coût cumulé sur 5 ans pour ${s.nom}`">
        <!-- Grille -->
        <g v-for="g in graduations" :key="g">
          <line :x1="M.gauche" :x2="L - M.droite" :y1="y(g)" :y2="y(g)" class="ca-grille" :class="{ 'is-base': g === 0 }" />
          <text :x="M.gauche - 8" :y="y(g) + 4" text-anchor="end" class="ca-axe">{{ fmtCourt(g) }}</text>
        </g>

        <!-- Barres empilées -->
        <g
          v-for="(d, idx) in donnees"
          :key="d.annee"
          class="ca-colonne"
          :class="{ 'is-estompe': survol !== null && survol !== idx }"
          @mouseenter="survol = idx"
          @mouseleave="survol = null"
          @focus="survol = idx"
          @blur="survol = null"
          tabindex="0"
        >
          <rect :x="M.gauche + bande * idx" :y="M.haut" :width="bande" :height="hauteurTrace" class="ca-cible" />
          <path :d="segment(x(idx), y(d.construction), y(0), largeurBarre, false)" class="ca-seg ca-seg--1" />
          <path
            :d="segment(x(idx), y(d.construction + d.recurrent), y(d.construction) - 2, largeurBarre, true)"
            class="ca-seg ca-seg--2"
          />
          <text :x="x(idx) + largeurBarre / 2" :y="H - 12" text-anchor="middle" class="ca-axe">
            Année {{ d.annee }}
          </text>
          <text
            v-if="idx === donnees.length - 1 || survol === idx"
            :x="x(idx) + largeurBarre / 2"
            :y="y(d.construction + d.recurrent) - 7"
            text-anchor="middle"
            class="ca-total"
          >
            {{ fmtCourt(d.construction + d.recurrent) }}
          </text>
        </g>
      </svg>

      <div
        v-if="survol !== null"
        class="ca-bulle"
        :style="styleBulle(survol)"
      >
        <strong>Après {{ donnees[survol].annee }} an{{ donnees[survol].annee > 1 ? "s" : "" }}</strong>
        <span><i class="ca-pastille ca-pastille--1"></i>Construction : {{ fmt(donnees[survol].construction) }}</span>
        <span><i class="ca-pastille ca-pastille--2"></i>Récurrent : {{ fmt(donnees[survol].recurrent) }}</span>
        <span class="ca-bulle-total">Total : {{ fmt(donnees[survol].construction + donnees[survol].recurrent) }}</span>
      </div>
    </div>

    <p class="ca-message">
      <template v-if="croisement <= 5">
        Dès l'année <strong>{{ croisement }}</strong>, les coûts récurrents ont dépassé le coût de construction.
      </template>
      <template v-else>
        Les coûts récurrents dépasseront le coût de construction vers l'année <strong>{{ croisement }}</strong>.
      </template>
      Un site se paie <strong>chaque année</strong>, pas seulement au lancement.
    </p>
  </figure>
</template>

<style scoped>
.viz {
  --series-1: #2a78d6;
  --series-2: #eb6834;
}
.dark .viz {
  --series-1: #3987e5;
  --series-2: #d95926;
}
.ca {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem 1rem 0.75rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.ca-tete {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 0.6rem 1rem;
}
.ca-titre {
  font-weight: 600;
  font-size: 0.95rem;
}
.ca-sous {
  display: block;
  font-weight: 400;
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
.ca-choix {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
}
.ca-onglet {
  padding: 0.3rem 0.65rem;
  border-radius: 999px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
.ca-onglet.is-on {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-text-1);
  font-weight: 600;
}
.ca-legende {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem 1.2rem;
  margin: 0.75rem 0 0.25rem;
  font-size: 0.8rem;
  color: var(--vp-c-text-2);
}
.ca-pastille {
  display: inline-block;
  width: 0.7rem;
  height: 0.7rem;
  margin-right: 0.35rem;
  border-radius: 3px;
  vertical-align: -1px;
}
.ca-pastille--1 {
  background: var(--series-1);
}
.ca-pastille--2 {
  background: var(--series-2);
}
.ca-zone {
  position: relative;
}
.ca-svg {
  display: block;
  width: 100%;
  height: auto;
  font-family: var(--vp-font-family-base);
}
.ca-grille {
  stroke: var(--vp-c-divider);
  stroke-width: 1;
  stroke-dasharray: 2 4;
}
.ca-grille.is-base {
  stroke-dasharray: none;
  stroke: var(--vp-c-text-3);
}
.ca-axe {
  font-size: 12px;
  fill: var(--vp-c-text-2);
}
.ca-total {
  font-size: 12.5px;
  font-weight: 600;
  fill: var(--vp-c-text-1);
}
.ca-cible {
  fill: transparent;
}
.ca-colonne {
  outline: none;
  cursor: default;
  transition: opacity 0.15s;
}
.ca-colonne.is-estompe {
  opacity: 0.45;
}
.ca-seg {
  transition: d 0.45s ease;
}
.ca-seg--1 {
  fill: var(--series-1);
}
.ca-seg--2 {
  fill: var(--series-2);
}
.ca-bulle {
  position: absolute;
  top: 0;
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  padding: 0.5rem 0.65rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.5rem;
  background: var(--vp-c-bg);
  box-shadow: var(--vp-shadow-2);
  font-size: 0.75rem;
  white-space: nowrap;
  pointer-events: none;
}
.ca-bulle-total {
  margin-top: 0.15rem;
  font-weight: 600;
}
.ca-message {
  margin: 0.5rem 0 0 !important;
  font-size: 0.875rem;
  line-height: 1.55;
}
@media (prefers-reduced-motion: reduce) {
  .ca-seg {
    transition: none;
  }
}
</style>
