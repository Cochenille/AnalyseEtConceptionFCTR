<script setup lang="ts">
import { computed, reactive, ref } from "vue";

// Hypothèses de l'activité
const TAUX_USD = 1.38;
const MONTANT_MOYEN = 120;
const RESERVATIONS = 1800;
const UTILISATEURS = 4;

type Outil = {
  cle: "A" | "B" | "C";
  nom: string;
  modele: string;
  lignes: string[];
  viator: boolean;
  cout: (reservations: number) => number;
  calcul: string[];
  piege: string;
};

const fmt = (n: number) =>
  n.toLocaleString("fr-CA", { minimumFractionDigits: 0, maximumFractionDigits: 0 }) + " $";

const OUTILS: Outil[] = [
  {
    cle: "A",
    nom: "Réservio",
    modele: "À la transaction",
    lignes: [
      "Aucun abonnement : « Gratuit pour toujours ! »",
      "Commission de 5 % sur chaque réservation payée en ligne",
      "Utilisateurs illimités",
      "Synchronisation avec Viator incluse",
    ],
    viator: true,
    cout: (r) => r * MONTANT_MOYEN * 0.05,
    calcul: [
      `${RESERVATIONS.toLocaleString("fr-CA")} réservations × ${MONTANT_MOYEN} $ = ${fmt(RESERVATIONS * MONTANT_MOYEN)} de ventes en ligne`,
      `${fmt(RESERVATIONS * MONTANT_MOYEN)} × 5 % = ${fmt(RESERVATIONS * MONTANT_MOYEN * 0.05)}`,
    ],
    piege: "« Gratuit » veut dire « payé par le succès ». Plus l'entreprise vend, plus la facture monte. Certains outils permettent de refiler ces frais au client, mais le prix affiché monte d'autant.",
  },
  {
    cle: "B",
    nom: "PagayePro",
    modele: "Au mois (forfait), en dollars américains",
    lignes: [
      "129 $ US par mois, facturé annuellement (159 $ US si payé au mois)",
      "Plus 1 % sur chaque réservation payée en ligne",
      "Utilisateurs illimités",
      "Module « Canaux de distribution » (Viator, etc.) : 30 $ US par mois",
    ],
    viator: true,
    cout: (r) => (129 + 30) * 12 * TAUX_USD + r * MONTANT_MOYEN * 0.01,
    calcul: [
      `(129 $ US + 30 $ US) × 12 mois = 1 908 $ US`,
      `1 908 $ US × ${TAUX_USD.toLocaleString("fr-CA")} = ${fmt(1908 * TAUX_USD)}`,
      `${fmt(RESERVATIONS * MONTANT_MOYEN)} × 1 % = ${fmt(RESERVATIONS * MONTANT_MOYEN * 0.01)}`,
      `Total : ${fmt(1908 * TAUX_USD + RESERVATIONS * MONTANT_MOYEN * 0.01)}`,
    ],
    piege: "Trois pièges en un : le prix est en dollars américains, la fonction essentielle (Viator) est un module payant, et il y a quand même une petite commission.",
  },
  {
    cle: "C",
    nom: "Quaistart",
    modele: "À l'utilisateur",
    lignes: [
      "45 $ CA par utilisateur, par mois",
      "Engagement de 12 mois",
      "Aucune commission",
      "Synchronisation avec Viator : « bientôt disponible »",
    ],
    viator: false,
    cout: () => 45 * UTILISATEURS * 12,
    calcul: [
      `45 $ × ${UTILISATEURS} utilisateurs × 12 mois = ${fmt(45 * UTILISATEURS * 12)}`,
    ],
    piege: "Le moins cher… et le seul qui ne répond pas au besoin. Sans Viator, les doubles réservations continuent. « Bientôt disponible » n'est pas une fonction : on évalue ce qui existe aujourd'hui. Et il faut payer l'hiver, quand personne ne réserve.",
  },
];

const reponses = reactive<Record<string, string>>({ A: "", B: "", C: "" });
const verifie = ref(false);
const volume = ref(RESERVATIONS);

function lireNombre(s: string) {
  const n = parseFloat(s.replace(/\s/g, "").replace("$", "").replace(",", "."));
  return Number.isFinite(n) ? n : null;
}

function proche(o: Outil) {
  const n = lireNombre(reponses[o.cle]);
  if (n === null) return null;
  const attendu = o.cout(RESERVATIONS);
  return Math.abs(n - attendu) / attendu <= 0.05;
}

const couts = computed(() => OUTILS.map((o) => ({ o, cout: o.cout(volume.value) })));
const maxCout = computed(() => Math.max(...couts.value.map((c) => c.cout), 1));

// Volume où Réservio (A) et PagayePro (B) coûtent la même chose
const pointBascule = Math.round((1908 * TAUX_USD) / (MONTANT_MOYEN * 0.04));

function reinitialiser() {
  reponses.A = reponses.B = reponses.C = "";
  verifie.value = false;
  volume.value = RESERVATIONS;
}
</script>

<template>
  <section class="gp">
    <div class="gp-hypo">
      <strong>Hypothèses</strong>
      <ul>
        <li>{{ RESERVATIONS.toLocaleString("fr-CA") }} réservations payées en ligne par année (environ 70 % des 2 600 réservations)</li>
        <li>Montant moyen d'une réservation : {{ MONTANT_MOYEN }} $</li>
        <li>1 $ US = {{ TAUX_USD.toLocaleString("fr-CA") }} $ CA</li>
        <li>{{ UTILISATEURS }} personnes gèrent les réservations : Mélanie, Patrick, Karine et le poste de l'accueil</li>
        <li>La synchronisation avec Viator est <strong>obligatoire</strong></li>
        <li>On ignore les taxes et les frais du service de paiement : ils sont les mêmes pour les trois</li>
      </ul>
    </div>

    <div class="gp-outils">
      <article v-for="o in OUTILS" :key="o.cle" class="gp-outil">
        <header>
          <span class="gp-lettre">{{ o.cle }}</span>
          <div>
            <strong>{{ o.nom }}</strong>
            <span class="gp-modele">{{ o.modele }}</span>
          </div>
        </header>
        <ul>
          <li v-for="(l, i) in o.lignes" :key="i">{{ l }}</li>
        </ul>
        <label class="gp-label" :for="'gp-' + o.cle">Notre calcul pour une année ($ CA)</label>
        <input
          :id="'gp-' + o.cle"
          v-model="reponses[o.cle]"
          class="gp-input"
          :class="verifie && proche(o) !== null ? (proche(o) ? 'is-bon' : 'is-mauvais') : ''"
          inputmode="decimal"
          placeholder="ex. 2 500"
        />
        <div v-if="verifie" class="gp-corr">
          <p class="gp-attendu">
            <strong>{{ fmt(o.cout(RESERVATIONS)) }}</strong> par année
            <span v-if="!o.viator" class="gp-tag is-mauvais">Ne répond pas au besoin</span>
          </p>
          <ul class="gp-calcul">
            <li v-for="(c, i) in o.calcul" :key="i">{{ c }}</li>
          </ul>
          <p class="gp-piege"><strong>Le piège :</strong> {{ o.piege }}</p>
        </div>
      </article>
    </div>

    <div class="gp-pied">
      <button type="button" class="gp-action is-principal" @click="verifie = true">Vérifier</button>
      <button type="button" class="gp-action" @click="reinitialiser">Recommencer</button>
    </div>

    <div v-if="verifie" class="gp-simul">
      <p class="gp-simul-titre"><strong>Et si les ventes en ligne changeaient ?</strong></p>
      <label class="gp-label" for="gp-volume">
        Réservations payées en ligne par année : <strong>{{ volume.toLocaleString("fr-CA") }}</strong>
      </label>
      <input id="gp-volume" v-model.number="volume" type="range" min="100" max="4000" step="50" class="gp-range" />
      <div class="gp-barres">
        <div v-for="c in couts" :key="c.o.cle" class="gp-barre-ligne">
          <span class="gp-barre-nom">{{ c.o.cle }} · {{ c.o.nom }}</span>
          <span class="gp-barre-piste">
            <span
              class="gp-barre"
              :class="{ 'is-hors': !c.o.viator }"
              :style="{ width: (c.cout / maxCout) * 100 + '%' }"
            />
          </span>
          <span class="gp-barre-val">{{ fmt(c.cout) }}<small> · 3 ans : {{ fmt(c.cout * 3) }}</small></span>
        </div>
      </div>
      <p class="gp-note">
        Sous environ <strong>{{ pointBascule.toLocaleString("fr-CA") }} réservations</strong> en ligne par année, Réservio coûte moins cher que PagayePro. Au-delà, c'est l'inverse.
        Le bon modèle de prix dépend du <strong>volume</strong> de l'entreprise, et ce volume va changer avec le nouveau site.
      </p>
    </div>
  </section>
</template>

<style scoped>
.gp {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
  font-size: 0.875rem;
}
.gp-hypo {
  padding: 0.65rem 0.8rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
}
.gp-hypo ul,
.gp-outil ul {
  margin: 0.3rem 0 0 !important;
  padding-left: 1.1rem !important;
  line-height: 1.5;
}
.gp-hypo li,
.gp-outil li { margin: 0.1rem 0 !important; }
.gp-outils {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.6rem;
  margin-top: 0.75rem;
}
.gp-outil {
  display: flex;
  flex-direction: column;
  padding: 0.75rem;
  border-radius: 0.75rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
}
.gp-outil header {
  display: flex;
  gap: 0.6rem;
  align-items: center;
}
.gp-outil header div {
  display: flex;
  flex-direction: column;
  line-height: 1.3;
}
.gp-lettre {
  display: grid;
  place-items: center;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-weight: 700;
  flex-shrink: 0;
}
.gp-modele {
  font-size: 0.75rem;
  color: var(--vp-c-text-2);
}
.gp-label {
  display: block;
  margin: 0.6rem 0 0.2rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
.gp-input {
  width: 100%;
  padding: 0.35rem 0.55rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.5rem;
  background: var(--vp-c-bg-soft);
  font: inherit;
}
.gp-input:focus {
  outline: none;
  border-color: var(--vp-c-brand-1);
}
.gp-input.is-bon { border-color: var(--vp-c-green-2); background: var(--vp-c-green-soft); }
.gp-input.is-mauvais { border-color: var(--vp-c-red-2); background: var(--vp-c-red-soft); }
.gp-corr {
  margin-top: 0.55rem;
  padding-top: 0.55rem;
  border-top: 1px dashed var(--vp-c-divider);
  font-size: 0.8rem;
  line-height: 1.5;
}
.gp-attendu {
  margin: 0 !important;
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  align-items: center;
}
.gp-attendu strong { font-size: 1rem; }
.gp-tag {
  padding: 0.1rem 0.45rem;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 600;
}
.gp-tag.is-mauvais { background: var(--vp-c-red-soft); color: var(--vp-c-red-1); }
.gp-calcul {
  color: var(--vp-c-text-2);
  font-family: var(--vp-font-family-mono);
  font-size: 0.72rem;
}
.gp-piege {
  margin: 0.4rem 0 0 !important;
  color: var(--vp-c-text-2);
}
.gp-pied {
  display: flex;
  gap: 0.4rem;
  margin-top: 0.75rem;
}
.gp-action {
  padding: 0.3rem 0.8rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.gp-action:hover { border-color: var(--vp-c-brand-1); }
.gp-action.is-principal {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
  font-weight: 600;
}
.gp-simul {
  margin-top: 0.9rem;
  padding-top: 0.9rem;
  border-top: 1px solid var(--vp-c-divider);
}
.gp-simul-titre { margin: 0 !important; }
.gp-range {
  width: 100%;
  accent-color: var(--vp-c-brand-1);
}
.gp-barres {
  display: grid;
  gap: 0.4rem;
  margin-top: 0.5rem;
}
.gp-barre-ligne {
  display: grid;
  grid-template-columns: 8.5rem 1fr auto;
  gap: 0.5rem;
  align-items: center;
  font-size: 0.8rem;
}
.gp-barre-piste {
  height: 0.8rem;
  border-radius: 999px;
  background: var(--vp-c-bg);
  overflow: hidden;
}
.gp-barre {
  display: block;
  height: 100%;
  border-radius: 999px;
  background: var(--vp-c-brand-1);
  transition: width 0.2s;
}
.gp-barre.is-hors {
  background: repeating-linear-gradient(45deg, var(--vp-c-red-2), var(--vp-c-red-2) 4px, transparent 4px, transparent 8px);
}
.gp-barre-val {
  font-variant-numeric: tabular-nums;
  text-align: right;
}
.gp-barre-val small { color: var(--vp-c-text-2); }
.gp-note {
  margin: 0.6rem 0 0 !important;
  font-size: 0.8rem;
  line-height: 1.5;
  color: var(--vp-c-text-2);
}
@media (max-width: 560px) {
  .gp-barre-ligne { grid-template-columns: 1fr auto; }
  .gp-barre-piste { grid-column: 1 / -1; grid-row: 2; }
}
</style>
