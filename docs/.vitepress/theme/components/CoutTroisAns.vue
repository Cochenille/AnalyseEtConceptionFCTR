<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from "vue";
import BoutonCopier from "./BoutonCopier.vue";

// Hypothèses de l'activité
const TAUX_USD = 1.38;
const PARTICIPANTS = 9000;
const RESERVATIONS = 2600;

type Outil = {
  cle: "A" | "B" | "C";
  nom: string;
  modele: string;
  lignes: string[];
  annees: (participants: number) => [number, number, number];
  calcul: string[];
  piege: string;
};

const fmt = (n: number) =>
  n.toLocaleString("fr-CA", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " $";
const fmt0 = (n: number) =>
  n.toLocaleString("fr-CA", { maximumFractionDigits: 0 }) + " $";

const signeo = (p: number) => {
  const usd = 49 * 12 + Math.max(0, p - 5000) * 0.1;
  const an = usd * TAUX_USD;
  return [an, an, an] as [number, number, number];
};

const OUTILS: Outil[] = [
  {
    cle: "A",
    nom: "Signéo",
    modele: "Au mois, en dollars américains, avec un plafond",
    lignes: [
      "49 $ US par mois, facturé annuellement",
      "5 000 décharges signées par année incluses",
      "0,10 $ US par décharge au-delà du plafond",
      "Application kiosque hors ligne incluse",
    ],
    annees: signeo,
    calcul: [
      "49 $ US × 12 mois = 588 $ US",
      `${PARTICIPANTS.toLocaleString("fr-CA")} décharges − 5 000 incluses = 4 000 × 0,10 $ US = 400 $ US`,
      `(588 + 400) $ US = 988 $ US × ${TAUX_USD.toLocaleString("fr-CA")} = 1 363,44 $ par année`,
      "1 363,44 $ × 3 ans = 4 090,32 $",
    ],
    piege: "Une décharge par participant, pas par réservation : 9 000, pas 2 600. Avec 2 600, on reste sous le plafond et on sous-estime la facture de 40 %. Et le prix est en dollars américains.",
  },
  {
    cle: "B",
    nom: "Quai-Signe",
    modele: "Au mois, en dollars canadiens, avec frais de mise en place",
    lignes: [
      "65 $ CA par mois, décharges illimitées",
      "Frais de mise en place de 1 200 $ CA, payés une seule fois : configuration, mise en forme de la décharge, formation d'une heure",
      "Mode hors ligne inclus",
    ],
    annees: () => [1200 + 780, 780, 780],
    calcul: [
      "65 $ × 12 mois = 780 $ par année",
      "Année 1 : 1 200 $ + 780 $ = 1 980 $",
      "Années 2 et 3 : 780 $ chacune",
      "Total : 1 980 $ + 780 $ + 780 $ = 3 540 $",
    ],
    piege: "Le plus cher la première année, mais pas sur trois ans. Les frais de mise en place ne se paient qu'une fois : ne les comptez ni zéro fois ni trois fois.",
  },
  {
    cle: "C",
    nom: "FormuPro",
    modele: "Au mois, en dollars américains, prix de lancement",
    lignes: [
      "Prix de lancement : 25 $ US par mois, garanti pendant 12 mois",
      "Ensuite : 59 $ US par mois",
      "Facturé annuellement, décharges illimitées",
      "Mode hors ligne inclus",
    ],
    annees: () => [25 * 12 * TAUX_USD, 59 * 12 * TAUX_USD, 59 * 12 * TAUX_USD],
    calcul: [
      `Année 1 : 25 $ US × 12 = 300 $ US × ${TAUX_USD.toLocaleString("fr-CA")} = 414,00 $`,
      `Années 2 et 3 : 59 $ US × 12 = 708 $ US × ${TAUX_USD.toLocaleString("fr-CA")} = 977,04 $ chacune`,
      "Total : 414,00 $ + 977,04 $ + 977,04 $ = 2 368,08 $",
    ],
    piege: "Le prix affiché en gros caractères ne dure qu'un an. Sur trois ans, la facture est presque six fois celle de la première année (414 $ × 3 = 1 242 $ serait une grave erreur).",
  },
];

const props = withDefaults(defineProps<{ storageKey?: string }>(), {
  storageKey: "asm-cout-trois-ans",
});

const reponses = reactive<Record<string, { an1: string; total: string }>>({
  A: { an1: "", total: "" },
  B: { an1: "", total: "" },
  C: { an1: "", total: "" },
});
const verifie = ref(false);
const participants = ref(PARTICIPANTS);

function lireNombre(s: string) {
  const n = parseFloat(s.replace(/\s/g, "").replace("$", "").replace(",", "."));
  return Number.isFinite(n) ? n : null;
}

function proche(saisie: string, attendu: number) {
  const n = lireNombre(saisie);
  if (n === null) return null;
  return Math.abs(n - attendu) / attendu <= 0.02;
}

const attendus = computed(() =>
  Object.fromEntries(
    OUTILS.map((o) => {
      const a = o.annees(PARTICIPANTS);
      return [o.cle, { an1: a[0], total: a[0] + a[1] + a[2] }];
    }),
  ) as Record<string, { an1: number; total: number }>,
);

const classe = (saisie: string, attendu: number) => {
  if (!verifie.value) return "";
  const p = proche(saisie, attendu);
  return p === null ? "" : p ? "is-bon" : "is-mauvais";
};

const simul = computed(() =>
  OUTILS.map((o) => {
    const a = o.annees(participants.value);
    return { o, a, total: a[0] + a[1] + a[2] };
  }),
);
const maxSimul = computed(() => Math.max(...simul.value.map((s) => s.total), 1));

function texteReponses() {
  return [
    "Séance 4 — Activité 2 : le coût sur trois ans",
    `Hypothèses : ${PARTICIPANTS.toLocaleString("fr-CA")} participants par année, une décharge chacun; 1 $ US = ${TAUX_USD.toLocaleString("fr-CA")} $ CA; taxes exclues.`,
    "",
    ...OUTILS.map((o) => {
      const r = reponses[o.cle];
      const lignes = [
        `${o.cle} · ${o.nom} (${o.modele})`,
        `   Notre année 1 : ${r.an1.trim() || "—"} · Notre total sur 3 ans : ${r.total.trim() || "—"}`,
      ];
      if (verifie.value) {
        lignes.push(`   Attendu : année 1 = ${fmt(attendus.value[o.cle].an1)} · 3 ans = ${fmt(attendus.value[o.cle].total)}`);
        lignes.push(...o.calcul.map((c) => `   ${c}`));
        lignes.push(`   Le piège : ${o.piege}`);
      }
      return lignes.join("\n");
    }),
  ].join("\n\n");
}

function reinitialiser() {
  if (!confirm("Effacer vos réponses ?")) return;
  for (const o of OUTILS) Object.assign(reponses[o.cle], { an1: "", total: "" });
  verifie.value = false;
  participants.value = PARTICIPANTS;
}

onMounted(() => {
  try {
    const data = JSON.parse(localStorage.getItem(props.storageKey) ?? "null");
    if (!data) return;
    for (const o of OUTILS) {
      reponses[o.cle].an1 = String(data.reponses?.[o.cle]?.an1 ?? "");
      reponses[o.cle].total = String(data.reponses?.[o.cle]?.total ?? "");
    }
    verifie.value = data.verifie === true;
  } catch {
    /* stockage indisponible : on part de réponses vides */
  }
});

watch([reponses, verifie], () => {
  try {
    localStorage.setItem(props.storageKey, JSON.stringify({ reponses, verifie: verifie.value }));
  } catch {
    /* stockage indisponible : rien à faire */
  }
});
</script>

<template>
  <section class="ct">
    <div class="ct-hypo">
      <strong>Hypothèses</strong>
      <ul>
        <li>{{ PARTICIPANTS.toLocaleString("fr-CA") }} participants par année ({{ RESERVATIONS.toLocaleString("fr-CA") }} réservations). <strong>Chaque participant</strong> a sa décharge; pour un mineur, c'est un parent qui la signe.</li>
        <li>1 $ US = {{ TAUX_USD.toLocaleString("fr-CA") }} $ CA, pendant les trois ans</li>
        <li>Le nombre de participants ne change pas pendant les trois ans</li>
        <li>Les trois outils offrent le mode hors ligne dont les guides ont besoin au quai</li>
        <li>Taxes exclues</li>
      </ul>
    </div>

    <div class="ct-outils">
      <article v-for="o in OUTILS" :key="o.cle" class="ct-outil">
        <header>
          <span class="ct-lettre">{{ o.cle }}</span>
          <div>
            <strong>{{ o.nom }}</strong>
            <span class="ct-modele">{{ o.modele }}</span>
          </div>
        </header>
        <ul>
          <li v-for="(l, i) in o.lignes" :key="i">{{ l }}</li>
        </ul>
        <div class="ct-champs">
          <label class="ct-label">
            Année 1 ($ CA)
            <input
              v-model="reponses[o.cle].an1"
              class="ct-input"
              :class="classe(reponses[o.cle].an1, attendus[o.cle].an1)"
              inputmode="decimal"
              placeholder="ex. 1 000"
            />
          </label>
          <label class="ct-label">
            Total sur 3 ans ($ CA)
            <input
              v-model="reponses[o.cle].total"
              class="ct-input"
              :class="classe(reponses[o.cle].total, attendus[o.cle].total)"
              inputmode="decimal"
              placeholder="ex. 3 000"
            />
          </label>
        </div>
        <div v-if="verifie" class="ct-corr">
          <p class="ct-attendu">
            Année 1 : <strong>{{ fmt(attendus[o.cle].an1) }}</strong> · 3 ans : <strong>{{ fmt(attendus[o.cle].total) }}</strong>
          </p>
          <ul class="ct-calcul">
            <li v-for="(c, i) in o.calcul" :key="i">{{ c }}</li>
          </ul>
          <p class="ct-piege"><strong>Le piège :</strong> {{ o.piege }}</p>
        </div>
      </article>
    </div>

    <div class="ct-boutons">
      <button type="button" class="ct-action is-principal" @click="verifie = true">Vérifier</button>
    </div>

    <div v-if="verifie" class="ct-simul">
      <p class="ct-simul-titre"><strong>Ce que montre le calcul sur trois ans</strong></p>
      <label class="ct-label" for="ct-volume">
        Participants par année : <strong>{{ participants.toLocaleString("fr-CA") }}</strong>
      </label>
      <input id="ct-volume" v-model.number="participants" type="range" min="2000" max="15000" step="250" class="ct-range" />
      <div class="ct-legende">
        <span><i class="ct-an1" />Année 1</span>
        <span><i class="ct-an2" />Année 2</span>
        <span><i class="ct-an3" />Année 3</span>
      </div>
      <div class="ct-barres">
        <div v-for="s in simul" :key="s.o.cle" class="ct-barre-ligne">
          <span class="ct-barre-nom">{{ s.o.cle }} · {{ s.o.nom }}</span>
          <span class="ct-barre-piste">
            <span
              v-for="(an, i) in s.a"
              :key="i"
              class="ct-seg"
              :class="'ct-an' + (i + 1)"
              :style="{ width: (an / maxSimul) * 100 + '%' }"
              :title="'Année ' + (i + 1) + ' : ' + fmt(an)"
            />
          </span>
          <span class="ct-barre-val">{{ fmt0(s.total) }}<small> · an 1 : {{ fmt0(s.a[0]) }}</small></span>
        </div>
      </div>
      <p class="ct-note">
        La première année, l'ordre est C, A, B. Sur trois ans, c'est C, B, A : <strong>le classement change</strong>.
        Faites glisser le nombre de participants : seul Signéo réagit, parce qu'il est le seul à compter les décharges.
        Rien ici ne dit lequel choisir. Le coût n'est qu'une ligne du tableau de comparaison.
      </p>
    </div>

    <p class="ct-rappel">Vos réponses restent dans ce navigateur, mais elles peuvent disparaître si la cache est vidée. <strong>Copiez-les dans vos notes</strong> avant de quitter la page.</p>
    <div class="ct-pied">
      <BoutonCopier :texte="texteReponses" />
      <button type="button" class="ct-action" @click="reinitialiser">Recommencer</button>
    </div>
  </section>
</template>

<style scoped>
.ct {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
  font-size: 0.875rem;
}
.ct-hypo {
  padding: 0.65rem 0.8rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.65rem;
  background: var(--vp-c-bg);
}
.ct-hypo ul,
.ct-outil ul {
  margin: 0.3rem 0 0 !important;
  padding-left: 1.1rem !important;
  line-height: 1.5;
}
.ct-hypo li,
.ct-outil li { margin: 0.1rem 0 !important; }
.ct-outils {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.6rem;
  margin-top: 0.75rem;
}
.ct-outil {
  display: flex;
  flex-direction: column;
  padding: 0.75rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.75rem;
  background: var(--vp-c-bg);
}
.ct-outil header {
  display: flex;
  gap: 0.6rem;
  align-items: center;
}
.ct-outil header div {
  display: flex;
  flex-direction: column;
  line-height: 1.3;
}
.ct-lettre {
  display: grid;
  place-items: center;
  flex-shrink: 0;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-weight: 700;
}
.ct-modele {
  font-size: 0.75rem;
  color: var(--vp-c-text-2);
}
.ct-champs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.4rem;
  margin-top: auto;
  padding-top: 0.6rem;
}
.ct-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
.ct-input {
  width: 100%;
  margin-top: 0.2rem;
  padding: 0.35rem 0.55rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.5rem;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font: inherit;
  font-weight: 400;
}
.ct-input:focus { outline: none; border-color: var(--vp-c-brand-1); }
.ct-input.is-bon { border-color: var(--vp-c-green-2); background: var(--vp-c-green-soft); }
.ct-input.is-mauvais { border-color: var(--vp-c-red-2); background: var(--vp-c-red-soft); }
.ct-corr {
  margin-top: 0.55rem;
  padding-top: 0.55rem;
  border-top: 1px dashed var(--vp-c-divider);
  font-size: 0.8rem;
  line-height: 1.5;
}
.ct-attendu { margin: 0 !important; }
.ct-calcul {
  color: var(--vp-c-text-2);
  font-family: var(--vp-font-family-mono);
  font-size: 0.72rem;
}
.ct-piege {
  margin: 0.4rem 0 0 !important;
  color: var(--vp-c-text-2);
}
.ct-boutons { margin-top: 0.75rem; }
.ct-action {
  padding: 0.3rem 0.8rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.ct-action:hover { border-color: var(--vp-c-brand-1); }
.ct-action.is-principal {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
  font-weight: 600;
}
.ct-simul {
  margin-top: 0.9rem;
  padding-top: 0.9rem;
  border-top: 1px solid var(--vp-c-divider);
}
.ct-simul-titre { margin: 0 0 0.3rem !important; }
.ct-range {
  width: 100%;
  accent-color: var(--vp-c-brand-1);
}
.ct-legende {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  margin: 0.3rem 0 0.4rem;
  font-size: 0.75rem;
  color: var(--vp-c-text-2);
}
.ct-legende span { display: inline-flex; align-items: center; gap: 0.3rem; }
.ct-legende i {
  display: inline-block;
  width: 0.8rem;
  height: 0.8rem;
  border-radius: 0.2rem;
}
.ct-an1 { background: var(--vp-c-brand-1); }
.ct-an2 { background: var(--vp-c-brand-3); }
.ct-an3 { background: var(--vp-c-brand-soft); outline: 1px solid var(--vp-c-brand-3); outline-offset: -1px; }
.ct-barres {
  display: grid;
  gap: 0.4rem;
}
.ct-barre-ligne {
  display: grid;
  grid-template-columns: 8rem 1fr auto;
  gap: 0.5rem;
  align-items: center;
  font-size: 0.8rem;
}
.ct-barre-piste {
  display: flex;
  gap: 2px;
  height: 0.9rem;
  border-radius: 0.25rem;
  background: var(--vp-c-bg);
  overflow: hidden;
}
.ct-seg {
  display: block;
  height: 100%;
  transition: width 0.2s;
}
.ct-barre-val {
  font-variant-numeric: tabular-nums;
  text-align: right;
}
.ct-barre-val small { color: var(--vp-c-text-2); }
.ct-note {
  margin: 0.6rem 0 0 !important;
  font-size: 0.8rem;
  line-height: 1.5;
  color: var(--vp-c-text-2);
}
.ct-rappel {
  margin: 0.75rem 0 0.6rem !important;
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
.ct-pied {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
}
@media (max-width: 560px) {
  .ct-barre-ligne { grid-template-columns: 1fr auto; }
  .ct-barre-piste { grid-column: 1 / -1; grid-row: 2; }
}
</style>
