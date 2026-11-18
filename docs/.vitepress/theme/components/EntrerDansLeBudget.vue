<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from "vue";
import BoutonCopier from "./BoutonCopier.vue";

// Séance 8, activité 2 : six mesures pour faire entrer le devis de la boulangerie dans son budget.
// Outils inventés. Montants avant taxes, en dollars canadiens.

const TAUX = 75;
const BUDGET = 6000;
const HEURES = 96;
const THEME = 90;
const UNIQUES = HEURES * TAUX + THEME; // 7 290 $
const ANNUELS = 860; // outil A 540 $ + hébergement et domaine 220 $ + textos 100 $

type Mesure = {
  cle: string;
  famille: "A" | "B" | "C";
  titre: string;
  detail: string;
  uniques: number; // effet sur les coûts uniques (négatif = économie)
  annuels: number; // effet par année sur les coûts annuels
  plusTard?: number; // coût reporté à une étape suivante, payé dans les 3 ans
  attendu: "proposer" | "ecarter";
  explication: string;
};

const FAMILLES = { A: "Enlever une fonctionnalité", B: "Changer d'outil", C: "Livrer en étapes" };

// Chaque mesure est une économie possible. « Oui » : on la présente à la cliente comme option.
// « Non » : on ne la lui présente pas, et le devis reste tel quel sur ce point.
const LIBELLES = { proposer: "Oui, on la propose", ecarter: "Non, on garde le devis tel quel" };

const MESURES: Mesure[] = [
  {
    cle: "m1",
    famille: "A",
    titre: "Retirer le rappel par texto",
    detail: "6 heures de moins, et plus de frais de textos (100 $ par année).",
    uniques: -450,
    annuels: -100,
    attendu: "proposer",
    explication: "Le rappel répond à un critère de poids 1 : c'est exactement ce qu'on peut retirer. La cliente perd les rappels la veille, donc quelques commandes oubliées de plus. On peut l'ajouter l'an prochain.",
  },
  {
    cle: "m2",
    famille: "A",
    titre: "Ne pas tester le site sur téléphone",
    detail: "7 heures de tests et de corrections en moins.",
    uniques: -525,
    annuels: 0,
    attendu: "ecarter",
    explication: "Les tests ne sont pas une fonctionnalité : c'est la condition pour que le site fonctionne. La plupart des commandes viendront d'un téléphone. Un bogue dans la commande coûtera plus cher que 525 $.",
  },
  {
    cle: "m3",
    famille: "B",
    titre: "Prendre les commandes par Messenger au lieu de l'outil A",
    detail: "Plus d'outil de commande : les clients écrivent à la boulangerie sur Messenger, et la propriétaire répond et note chaque commande. 20 heures de configuration en moins, et plus d'abonnement (540 $ par année).",
    uniques: -1500,
    annuels: -540,
    attendu: "ecarter",
    explication: "Le piège classique : c'est gratuit pour le studio, mais pas pour la cliente. Le travail ne disparaît pas, il passe chez elle. Environ 2 000 commandes par année, à 3 minutes chacune pour lire, répondre, noter et confirmer : 100 heures de plus par année, souvent le vendredi soir. Sans paiement à l'avance, certaines commandes ne seront jamais ramassées. Et une commande oubliée dans les messages, c'est un client perdu.",
  },
  {
    cle: "m4",
    famille: "B",
    titre: "Utiliser la page de commande toute faite de l'outil A",
    detail: "Au lieu d'une page de commande faite sur mesure : 12 heures de moins. Même outil, même abonnement.",
    uniques: -900,
    annuels: 0,
    attendu: "proposer",
    explication: "Une vraie économie, sans coût caché : l'abonnement ne change pas. La cliente perd une page de commande aux couleurs exactes de la boulangerie; celle de l'outil A est plus générique, mais elle fonctionne.",
  },
  {
    cle: "m5",
    famille: "C",
    titre: "Reporter les paniers-cadeaux au printemps",
    detail: "Les commandes en ligne ouvrent comme prévu; la boutique de paniers-cadeaux (18 heures) vient dans une deuxième étape, payée sur le budget de l'an prochain.",
    uniques: -1350,
    annuels: 0,
    plusTard: 1500, // 18 h + 2 h de reprise, à 75 $
    attendu: "proposer",
    explication: "La cliente garde l'essentiel pour la date ferme et étale la dépense. Elle perd les paniers-cadeaux de Noël, et la deuxième étape coûtera un peu plus (2 heures pour reprendre le projet) : 150 $ de plus sur trois ans.",
  },
  {
    cle: "m6",
    famille: "C",
    titre: "Mettre en ligne d'abord un site vitrine, sans commandes",
    detail: "Le menu et les heures d'ouverture d'abord; la commande en ligne dans une deuxième étape. 40 heures de moins maintenant.",
    uniques: -3000,
    annuels: 0,
    plusTard: 3150,
    attendu: "ecarter",
    explication: "La commande en ligne est la raison du projet. Sans elle, le site ne répond pas à la demande de départ : on rentre dans le budget en livrant autre chose. Une étape doit livrer l'essentiel, pas le reporter.",
  },
];

const props = withDefaults(defineProps<{ storageKey?: string }>(), {
  storageKey: "asm-entrer-dans-le-budget",
});

const choix = reactive<Record<string, "" | "proposer" | "ecarter">>(Object.fromEntries(MESURES.map((m) => [m.cle, ""])));
const pertes = reactive<Record<string, string>>(Object.fromEntries(MESURES.map((m) => [m.cle, ""])));
const verifie = ref(false);

const fmt = (n: number) => n.toLocaleString("fr-CA", { maximumFractionDigits: 0 }) + " $";
const fmtSigne = (n: number) => (n > 0 ? "+" : n < 0 ? "−" : "") + fmt(Math.abs(n));
const effetTroisAns = (m: Mesure) => m.uniques + 3 * m.annuels + (m.plusTard ?? 0);

const proposees = computed(() => MESURES.filter((m) => choix[m.cle] === "proposer"));
const uniquesApres = computed(() => UNIQUES + proposees.value.reduce((s, m) => s + m.uniques, 0));
const annuelsApres = computed(() => ANNUELS + proposees.value.reduce((s, m) => s + m.annuels, 0));
const plusTardApres = computed(() => proposees.value.reduce((s, m) => s + (m.plusTard ?? 0), 0));
const troisAnsAvant = UNIQUES + 3 * ANNUELS;
const troisAnsApres = computed(() => uniquesApres.value + 3 * annuelsApres.value + plusTardApres.value);
const dansBudget = computed(() => uniquesApres.value <= BUDGET);
const echelle = UNIQUES * 1.05;

const nbBons = computed(() => MESURES.filter((m) => choix[m.cle] === m.attendu).length);

function texteReponses() {
  const l = [
    "Séance 8 — Activité 2 : faire entrer la boulangerie dans le budget",
    `Devis de départ : coûts uniques ${fmt(UNIQUES)} (budget ${fmt(BUDGET)}), coûts annuels ${fmt(ANNUELS)}, ${fmt(troisAnsAvant)} sur trois ans.`,
    "",
    ...MESURES.map((m) => {
      const lignes = [
        `${m.famille}. ${m.titre} (coûts uniques : ${fmtSigne(m.uniques)})`,
        `   Ce que la cliente perd ou reporte : ${pertes[m.cle].trim() || "—"}`,
        `   Propose-t-on cette économie à la cliente ? ${choix[m.cle] ? LIBELLES[choix[m.cle] as "proposer" | "ecarter"] : "—"}`,
      ];
      if (verifie.value) {
        lignes.push(`   Effet sur trois ans : ${fmtSigne(effetTroisAns(m))} · réponse attendue : ${LIBELLES[m.attendu]}`);
        lignes.push(`   ${m.explication}`);
      }
      return lignes.join("\n");
    }),
    "",
    `Avec les économies proposées : coûts uniques ${fmt(uniquesApres.value)} (${dansBudget.value ? "dans le budget" : "hors budget"}), ${fmt(troisAnsApres.value)} sur trois ans.`,
  ];
  return l.join("\n");
}

function reinitialiser() {
  if (!confirm("Effacer vos réponses ?")) return;
  for (const m of MESURES) {
    choix[m.cle] = "";
    pertes[m.cle] = "";
  }
  verifie.value = false;
}

onMounted(() => {
  try {
    const data = JSON.parse(localStorage.getItem(props.storageKey) ?? "null");
    if (!data) return;
    for (const m of MESURES) {
      const c = data.choix?.[m.cle];
      choix[m.cle] = c === "proposer" || c === "ecarter" ? c : "";
      pertes[m.cle] = String(data.pertes?.[m.cle] ?? "");
    }
    verifie.value = data.verifie === true;
  } catch {
    /* stockage indisponible : on part de réponses vides */
  }
});

watch([choix, pertes, verifie], () => {
  try {
    localStorage.setItem(props.storageKey, JSON.stringify({ choix, pertes, verifie: verifie.value }));
  } catch {
    /* stockage indisponible : rien à faire */
  }
});
</script>

<template>
  <section class="eb">
    <div class="eb-devis">
      <strong>Le devis de départ</strong>
      <ul>
        <li>Construction : {{ HEURES }} heures × {{ TAUX }} $ = {{ fmt(HEURES * TAUX) }}, dont la boutique de paniers-cadeaux (18 h). Thème payant : {{ THEME }} $. <strong>Coûts uniques : {{ fmt(UNIQUES) }}</strong>, pour un budget de <strong>{{ fmt(BUDGET) }}</strong>.</li>
        <li>Coûts annuels : {{ fmt(ANNUELS) }} (abonnement à l'outil de commande A, retenu à la séance : 540 $, hébergement et domaine 220 $, textos 100 $).</li>
        <li>Total sur trois ans : {{ fmt(troisAnsAvant) }}. Tous les montants sont avant taxes.</li>
      </ul>
    </div>

    <div class="eb-jauge" :class="dansBudget ? 'is-ok' : 'is-depasse'">
      <div class="eb-jauge-tete">
        <span>Coûts uniques, avec les économies proposées</span>
        <strong>{{ fmt(uniquesApres) }}</strong>
      </div>
      <div class="eb-piste">
        <span class="eb-rempli" :style="{ width: (uniquesApres / echelle) * 100 + '%' }" />
        <span class="eb-budget" :style="{ left: (BUDGET / echelle) * 100 + '%' }" title="Budget" />
      </div>
      <p class="eb-jauge-pied">
        {{ dansBudget ? "Dans le budget de " + fmt(BUDGET) + "." : "Encore " + fmt(uniquesApres - BUDGET) + " au-dessus du budget." }}
        <template v-if="verifie"> Sur trois ans : <strong>{{ fmt(troisAnsApres) }}</strong> (au départ : {{ fmt(troisAnsAvant) }}).</template>
      </p>
    </div>

    <div class="eb-mesures">
      <article v-for="m in MESURES" :key="m.cle" class="eb-mesure" :class="verifie && choix[m.cle] ? (choix[m.cle] === m.attendu ? 'is-bon' : 'is-mauvais') : ''">
        <header>
          <span class="eb-famille">{{ m.famille }}</span>
          <div>
            <span class="eb-fam-nom">{{ FAMILLES[m.famille] }}</span>
            <strong>{{ m.titre }}</strong>
          </div>
        </header>
        <p class="eb-detail">{{ m.detail }}</p>
        <p class="eb-eco">Coûts uniques : <strong>{{ fmtSigne(m.uniques) }}</strong></p>
        <label class="eb-label">
          Ce que la cliente perd ou reporte
          <textarea v-model="pertes[m.cle]" class="eb-texte" rows="2" />
        </label>
        <p class="eb-question">Propose-t-on cette économie à la cliente ?</p>
        <div class="eb-choix" role="radiogroup" :aria-label="'Propose-t-on cette économie à la cliente ? ' + m.titre">
          <label><input v-model="choix[m.cle]" type="radio" value="proposer" :name="'eb-' + m.cle" /> {{ LIBELLES.proposer }}</label>
          <label><input v-model="choix[m.cle]" type="radio" value="ecarter" :name="'eb-' + m.cle" /> {{ LIBELLES.ecarter }}</label>
        </div>
        <div v-if="verifie" class="eb-corr">
          <p>
            Effet sur trois ans : <strong>{{ fmtSigne(effetTroisAns(m)) }}</strong> ·
            Réponse attendue : {{ LIBELLES[m.attendu] }}
          </p>
          <p class="eb-expl">{{ m.explication }}</p>
        </div>
      </article>
    </div>

    <div class="eb-boutons">
      <button type="button" class="eb-action is-principal" @click="verifie = true">Vérifier</button>
      <span v-if="verifie" class="eb-score">Décisions qui correspondent à la correction : {{ nbBons }} sur {{ MESURES.length }}.</span>
    </div>

    <p v-if="verifie" class="eb-note">
      Trois économies peuvent se proposer : une par famille. Aucune ne suffit seule sauf le report des paniers-cadeaux; ensemble, deux d'entre elles suffisent.
      C'est ce que demande la section 6.4 : <strong>trois options</strong>, chacune avec son économie et ce que le client perd, pour qu'il choisisse.
    </p>

    <p class="eb-rappel">Vos réponses restent dans ce navigateur, mais elles peuvent disparaître si la cache est vidée. <strong>Copiez-les dans vos notes</strong> avant de quitter la page.</p>
    <div class="eb-pied">
      <BoutonCopier :texte="texteReponses" />
      <button type="button" class="eb-action" @click="reinitialiser">Recommencer</button>
    </div>
  </section>
</template>

<style scoped>
.eb {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
  font-size: 0.875rem;
}
.eb-devis {
  padding: 0.65rem 0.8rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.65rem;
  background: var(--vp-c-bg);
}
.eb-devis ul { margin: 0.3rem 0 0 !important; padding-left: 1.1rem !important; line-height: 1.5; }
.eb-devis li { margin: 0.1rem 0 !important; }
.eb-jauge {
  position: sticky;
  /* sous la barre du site et la barre « On this page » (les pages n'ont pas d'aside) */
  top: calc(var(--vp-nav-height, 64px) + 3.5rem);
  z-index: 2;
  margin-top: 0.75rem;
  padding: 0.6rem 0.8rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.65rem;
  background: var(--vp-c-bg);
}
.eb-jauge-tete { display: flex; justify-content: space-between; gap: 0.5rem; font-size: 0.8rem; }
.eb-piste {
  position: relative;
  height: 0.9rem;
  margin: 0.35rem 0;
  border-radius: 0.25rem;
  background: var(--vp-c-bg-soft);
}
.eb-rempli {
  display: block;
  height: 100%;
  border-radius: 0.25rem;
  transition: width 0.2s;
}
.is-ok .eb-rempli { background: var(--vp-c-green-2); }
.is-depasse .eb-rempli { background: var(--vp-c-red-2); }
.eb-budget {
  position: absolute;
  top: -0.25rem;
  bottom: -0.25rem;
  width: 2px;
  background: var(--vp-c-text-1);
}
.eb-jauge-pied { margin: 0 !important; font-size: 0.78rem; color: var(--vp-c-text-2); }
.eb-mesures {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 0.6rem;
  margin-top: 0.75rem;
}
.eb-mesure {
  display: flex;
  flex-direction: column;
  padding: 0.75rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.75rem;
  background: var(--vp-c-bg);
}
.eb-mesure.is-bon { border-color: var(--vp-c-green-2); }
.eb-mesure.is-mauvais { border-color: var(--vp-c-red-2); }
.eb-mesure header { display: flex; gap: 0.6rem; align-items: center; }
.eb-mesure header div { display: flex; flex-direction: column; line-height: 1.3; }
.eb-famille {
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
.eb-fam-nom { font-size: 0.72rem; color: var(--vp-c-text-2); }
.eb-detail { margin: 0.5rem 0 0.3rem !important; font-size: 0.8rem; line-height: 1.45; }
.eb-eco { margin: 0 0 0.4rem !important; font-size: 0.8rem; }
.eb-label {
  display: block;
  margin-top: auto;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
.eb-texte {
  width: 100%;
  margin-top: 0.2rem;
  padding: 0.35rem 0.55rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.5rem;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font: inherit;
  font-weight: 400;
  resize: vertical;
}
.eb-texte:focus { outline: none; border-color: var(--vp-c-brand-1); }
.eb-question { margin: 0.45rem 0 0 !important; font-size: 0.75rem; font-weight: 600; color: var(--vp-c-text-2); }
.eb-choix { display: flex; flex-wrap: wrap; gap: 0.3rem 1rem; margin-top: 0.2rem; font-size: 0.8rem; }
.eb-choix label { display: inline-flex; gap: 0.3rem; align-items: center; cursor: pointer; }
.eb-choix input { accent-color: var(--vp-c-brand-1); }
.eb-corr {
  margin-top: 0.55rem;
  padding-top: 0.55rem;
  border-top: 1px dashed var(--vp-c-divider);
  font-size: 0.8rem;
  line-height: 1.5;
}
.eb-corr p { margin: 0 !important; }
.eb-expl { margin-top: 0.3rem !important; color: var(--vp-c-text-2); }
.eb-boutons { display: flex; flex-wrap: wrap; gap: 0.6rem; align-items: center; margin-top: 0.75rem; }
.eb-score { font-size: 0.8rem; color: var(--vp-c-text-2); }
.eb-action {
  padding: 0.3rem 0.8rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.eb-action:hover { border-color: var(--vp-c-brand-1); }
.eb-action.is-principal { border-color: var(--vp-c-brand-1); color: var(--vp-c-brand-1); font-weight: 600; }
.eb-note { margin: 0.6rem 0 0 !important; font-size: 0.8rem; line-height: 1.5; color: var(--vp-c-text-2); }
.eb-rappel { margin: 0.75rem 0 0.6rem !important; font-size: 0.78rem; color: var(--vp-c-text-2); }
.eb-pied {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
}
</style>
