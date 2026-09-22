<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from "vue";

type NoeudId = "appareil" | "dns" | "registraire" | "hebergement" | "plateforme" | "contenus" | "externe";

type Etape = {
  titre: string;
  texte: string;
  fleche?: string; // id du chemin animé
  actifs: NoeudId[];
};

const ETAPES: Etape[] = [
  {
    titre: "Vue d'ensemble",
    texte:
      "Une cliente tape bistro-exemple.ca dans son téléphone. En quelques secondes, plusieurs acteurs travaillent pour afficher la page. Avancez étape par étape.",
    actifs: ["appareil", "dns", "registraire", "hebergement", "plateforme", "contenus", "externe"],
  },
  {
    titre: "① Où est ce site ?",
    texte:
      "Le navigateur ne sait pas où se trouve bistro-exemple.ca. Il pose la question au DNS, l'annuaire d'Internet. Le nom de domaine, lui, a été loué chez un registraire.",
    fleche: "p1",
    actifs: ["appareil", "dns", "registraire"],
  },
  {
    titre: "② Voici l'adresse IP",
    texte:
      "Le DNS répond avec l'adresse IP du serveur, une série de chiffres comme 203.0.113.42. Les humains retiennent des noms ; les machines utilisent des numéros.",
    fleche: "p2",
    actifs: ["appareil", "dns"],
  },
  {
    titre: "③ Demande sécurisée de la page",
    texte:
      "Le navigateur contacte le serveur. Grâce au certificat SSL/TLS, la connexion est chiffrée : c'est le cadenas à côté de l'adresse (https://).",
    fleche: "p3",
    actifs: ["appareil", "hebergement"],
  },
  {
    titre: "④ La page revient",
    texte:
      "L'hébergement fait fonctionner la plateforme (WordPress, Shopify, code maison…). Elle assemble les contenus — textes, photos, menu — et renvoie le HTML, le CSS, le JavaScript et les images.",
    fleche: "p4",
    actifs: ["appareil", "hebergement", "plateforme", "contenus"],
  },
  {
    titre: "⑤ Réserver une table",
    texte:
      "Certaines fonctions ne sont pas dans le site lui-même. La réservation ou le paiement passent souvent par un service externe (Libro, OpenTable, Stripe…).",
    fleche: "p5",
    actifs: ["appareil", "externe"],
  },
];

const CHEMINS: Record<string, string> = {
  p1: "M172,138 C225,95 245,62 288,56",
  p2: "M288,76 C240,90 220,132 172,156",
  p3: "M172,178 L518,178",
  p4: "M518,210 L172,210",
  p5: "M172,222 C220,285 245,318 288,322",
};

const i = ref(0);
const lecture = ref(false);
let minuterie: ReturnType<typeof setInterval> | undefined;

const etape = computed(() => ETAPES[i.value]);
const actif = (id: NoeudId) => etape.value.actifs.includes(id);
const flecheActive = (id: string) => i.value === 0 || etape.value.fleche === id;

function aller(n: number) {
  i.value = (n + ETAPES.length) % ETAPES.length;
}
function arreter() {
  lecture.value = false;
  clearInterval(minuterie);
}
function basculerLecture() {
  if (lecture.value) return arreter();
  lecture.value = true;
  if (i.value === ETAPES.length - 1) i.value = 0;
  minuterie = setInterval(() => {
    if (i.value >= ETAPES.length - 1) return arreter();
    i.value++;
  }, 4500);
}
function manuel(n: number) {
  arreter();
  aller(n);
}

onBeforeUnmount(arreter);
</script>

<template>
  <section class="ta">
    <svg
      class="ta-svg"
      viewBox="0 0 720 370"
      role="img"
      aria-label="Schéma du trajet d'une page Web : appareil, DNS, hébergement, plateforme, contenus et service externe"
    >
      <defs>
        <marker id="ta-pointe" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 z" class="ta-pointe" />
        </marker>
        <marker id="ta-pointe-off" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 z" class="ta-pointe-off" />
        </marker>
      </defs>

      <!-- Registraire → DNS (contexte) -->
      <line x1="478" y1="52" x2="444" y2="52" class="ta-lien-pointille" />

      <!-- Flèches du trajet -->
      <g v-for="(d, id) in CHEMINS" :key="id">
        <path
          :d="d"
          class="ta-fleche"
          :class="{ 'is-on': flecheActive(id), 'is-courante': etape.fleche === id }"
          :marker-end="flecheActive(id) ? 'url(#ta-pointe)' : 'url(#ta-pointe-off)'"
        />
      </g>

      <!-- Paquet animé -->
      <circle v-if="etape.fleche" :key="'paquet-' + i" r="7" class="ta-paquet">
        <animateMotion :path="CHEMINS[etape.fleche]" dur="1.6s" repeatCount="indefinite" />
      </circle>

      <!-- Étiquettes des flèches -->
      <g class="ta-etiquettes">
        <text x="200" y="88" :class="{ 'is-on': flecheActive('p1') }">① Où est ce site ?</text>
        <text x="190" y="128" :class="{ 'is-on': flecheActive('p2') }">② Adresse IP</text>
        <text x="345" y="170" text-anchor="middle" :class="{ 'is-on': flecheActive('p3') }">③ Demande la page (HTTPS)</text>
        <text x="345" y="228" text-anchor="middle" :class="{ 'is-on': flecheActive('p4') }">④ HTML, CSS, JS, images</text>
        <text x="186" y="300" :class="{ 'is-on': flecheActive('p5') }">⑤ Réserver</text>
      </g>

      <!-- Appareil -->
      <g class="ta-noeud" :class="{ 'is-on': actif('appareil') }">
        <rect x="62" y="112" width="110" height="130" rx="18" class="ta-boite" />
        <rect x="74" y="128" width="86" height="80" rx="4" class="ta-ecran" />
        <rect x="80" y="136" width="74" height="10" rx="5" class="ta-url" />
        <text x="117" y="144" text-anchor="middle" class="ta-mini">bistro-exemple.ca</text>
        <circle cx="117" cy="225" r="6" class="ta-bouton" />
        <text x="117" y="266" text-anchor="middle" class="ta-titre">Appareil + navigateur</text>
      </g>

      <!-- DNS -->
      <g class="ta-noeud" :class="{ 'is-on': actif('dns') }">
        <rect x="290" y="22" width="152" height="62" rx="12" class="ta-boite" />
        <text x="366" y="48" text-anchor="middle" class="ta-titre">DNS</text>
        <text x="366" y="68" text-anchor="middle" class="ta-sous">nom → adresse IP</text>
      </g>

      <!-- Registraire -->
      <g class="ta-noeud ta-noeud--annexe" :class="{ 'is-on': actif('registraire') }">
        <rect x="480" y="28" width="130" height="48" rx="12" class="ta-boite ta-boite--pointille" />
        <text x="545" y="50" text-anchor="middle" class="ta-titre ta-titre--petit">Registraire</text>
        <text x="545" y="66" text-anchor="middle" class="ta-sous">loue le nom</text>
      </g>

      <!-- Hébergement -->
      <g class="ta-noeud" :class="{ 'is-on': actif('hebergement') }">
        <rect x="520" y="112" width="178" height="208" rx="14" class="ta-boite" />
        <text x="609" y="138" text-anchor="middle" class="ta-titre">Hébergement</text>
        <text x="609" y="154" text-anchor="middle" class="ta-sous">le serveur</text>
      </g>
      <g class="ta-noeud ta-noeud--interne" :class="{ 'is-on': actif('plateforme') }">
        <rect x="536" y="170" width="146" height="58" rx="10" class="ta-boite" />
        <text x="609" y="195" text-anchor="middle" class="ta-titre ta-titre--petit">Plateforme</text>
        <text x="609" y="213" text-anchor="middle" class="ta-sous">WordPress, Shopify…</text>
      </g>
      <g class="ta-noeud ta-noeud--interne" :class="{ 'is-on': actif('contenus') }">
        <rect x="536" y="244" width="146" height="58" rx="10" class="ta-boite" />
        <text x="609" y="269" text-anchor="middle" class="ta-titre ta-titre--petit">Contenus</text>
        <text x="609" y="287" text-anchor="middle" class="ta-sous">textes, photos, menu</text>
      </g>
      <line x1="609" y1="228" x2="609" y2="244" class="ta-lien" />

      <!-- Service externe -->
      <g class="ta-noeud" :class="{ 'is-on': actif('externe') }">
        <rect x="290" y="292" width="152" height="62" rx="12" class="ta-boite" />
        <text x="366" y="318" text-anchor="middle" class="ta-titre">Service externe</text>
        <text x="366" y="338" text-anchor="middle" class="ta-sous">réservation, paiement</text>
      </g>
    </svg>

    <div class="ta-panneau" aria-live="polite">
      <p class="ta-panneau-titre">{{ etape.titre }}</p>
      <p class="ta-panneau-texte">{{ etape.texte }}</p>
    </div>

    <div class="ta-controles">
      <button type="button" class="ta-btn" aria-label="Étape précédente" @click="manuel(i - 1)">←</button>
      <div class="ta-points" role="tablist" aria-label="Étapes">
        <button
          v-for="(e, n) in ETAPES"
          :key="n"
          type="button"
          role="tab"
          class="ta-point"
          :class="{ 'is-on': n === i }"
          :aria-selected="n === i"
          :aria-label="e.titre"
          @click="manuel(n)"
        ></button>
      </div>
      <button type="button" class="ta-btn" aria-label="Étape suivante" @click="manuel(i + 1)">→</button>
      <button type="button" class="ta-btn ta-btn--lecture" @click="basculerLecture">
        {{ lecture ? "Pause" : "Lecture" }}
      </button>
    </div>
  </section>
</template>

<style scoped>
.ta {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.ta-svg {
  display: block;
  width: 100%;
  height: auto;
  font-family: var(--vp-font-family-base);
}

/* Nœuds */
.ta-boite {
  fill: var(--vp-c-bg);
  stroke: var(--vp-c-divider);
  stroke-width: 1.5;
  transition: stroke 0.3s, fill 0.3s;
}
.ta-boite--pointille {
  stroke-dasharray: 5 4;
}
.ta-noeud {
  opacity: 0.35;
  transition: opacity 0.35s;
}
.ta-noeud.is-on {
  opacity: 1;
}
.ta-noeud.is-on > .ta-boite {
  stroke: var(--vp-c-brand-1);
  stroke-width: 2;
}
.ta-noeud--interne.is-on > .ta-boite {
  fill: var(--vp-c-brand-soft);
}
.ta-titre {
  font-size: 15px;
  font-weight: 600;
  fill: var(--vp-c-text-1);
}
.ta-titre--petit {
  font-size: 14px;
}
.ta-sous {
  font-size: 12px;
  fill: var(--vp-c-text-2);
}
.ta-mini {
  font-size: 7px;
  fill: var(--vp-c-text-2);
}
.ta-ecran {
  fill: var(--vp-c-bg-soft);
  stroke: var(--vp-c-divider);
}
.ta-url {
  fill: var(--vp-c-bg);
}
.ta-bouton {
  fill: none;
  stroke: var(--vp-c-divider);
}

/* Liens et flèches */
.ta-lien,
.ta-lien-pointille {
  stroke: var(--vp-c-text-3);
  stroke-width: 1.5;
}
.ta-lien-pointille {
  stroke-dasharray: 4 4;
}
.ta-fleche {
  fill: none;
  stroke: var(--vp-c-divider);
  stroke-width: 2;
  transition: stroke 0.3s;
}
.ta-fleche.is-on {
  stroke: var(--vp-c-text-3);
}
.ta-fleche.is-courante {
  stroke: var(--vp-c-brand-1);
  stroke-width: 3;
}
.ta-pointe {
  fill: var(--vp-c-brand-1);
}
.ta-pointe-off {
  fill: var(--vp-c-divider);
}
.ta-paquet {
  fill: var(--vp-c-brand-1);
  stroke: var(--vp-c-bg);
  stroke-width: 2;
}
.ta-etiquettes text {
  font-size: 12.5px;
  font-weight: 500;
  fill: var(--vp-c-text-3);
  opacity: 0.45;
  transition: opacity 0.3s;
}
.ta-etiquettes text.is-on {
  fill: var(--vp-c-text-1);
  opacity: 1;
}

/* Panneau d'explication */
.ta-panneau {
  min-height: 5.5rem;
  margin-top: 0.75rem;
  padding: 0.75rem 0.9rem;
  border-left: 3px solid var(--vp-c-brand-1);
  border-radius: 0.4rem;
  background: var(--vp-c-bg);
}
.ta-panneau-titre {
  margin: 0 !important;
  font-weight: 600;
}
.ta-panneau-texte {
  margin: 0.25rem 0 0 !important;
  font-size: 0.9rem;
  line-height: 1.55;
  color: var(--vp-c-text-2);
}

/* Contrôles */
.ta-controles {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
}
.ta-btn {
  padding: 0.35rem 0.75rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.85rem;
  font-weight: 500;
  transition: border-color 0.15s;
}
.ta-btn:hover {
  border-color: var(--vp-c-brand-1);
}
.ta-btn--lecture {
  margin-left: auto;
}
.ta-points {
  display: flex;
  gap: 0.35rem;
}
.ta-point {
  width: 0.7rem;
  height: 0.7rem;
  border-radius: 999px;
  background: var(--vp-c-divider);
  transition: background-color 0.2s, transform 0.2s;
}
.ta-point.is-on {
  background: var(--vp-c-brand-1);
  transform: scale(1.25);
}

@media (prefers-reduced-motion: reduce) {
  .ta-paquet {
    display: none;
  }
}
</style>
