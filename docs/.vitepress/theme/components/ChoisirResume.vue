<script setup lang="ts">
import { computed, onMounted, reactive, watch } from "vue";
import BoutonCopier from "./BoutonCopier.vue";

type Verdict = "oui" | "defendable" | "non";
type Phrase = { texte: string; section: string; verdict: Verdict; pourquoi: string };

const MAX = 4;

const VERDICTS: Record<Verdict, string> = {
  oui: "À mettre dans le résumé",
  defendable: "Défendable",
  non: "À laisser dans le rapport",
};

const PHRASES: Phrase[] = [
  {
    texte: "Le compte Wix et le nom de domaine sont au nom du neveu de Patrick, qui habite à Vancouver. Sans ses accès, le site actuel ne peut être ni gardé ni déplacé.",
    section: "Section 4",
    verdict: "oui",
    pourquoi: "Bloquant : tout le projet en dépend, quelle que soit la solution choisie. C'est aussi la première chose que Mélanie doit régler.",
  },
  {
    texte: "Lors de l'essai E2, la réservation de 5 places sur téléphone a pris 2 min 40 s avec Réservio et 4 min 10 s avec PagayePro.",
    section: "Section 6",
    verdict: "non",
    pourquoi: "Un bon constat, mais une mesure de détail. Sa place est dans la section 6 et dans l'annexe A.",
  },
  {
    texte: "Le budget de 8 000 $ couvre la construction du site, mais pas les abonnements. Selon les outils, ceux-ci coûteraient de 1 400 $ à 3 900 $ par année, en plus.",
    section: "Sections 4 et 6",
    verdict: "oui",
    pourquoi: "Mélanie croit que son site lui coûte 300 $ par année. Ce constat change sa façon de voir le budget, quelle que soit la solution.",
  },
  {
    texte: "Réservio est la solution à privilégier pour les réservations.",
    section: "Section 6",
    verdict: "non",
    pourquoi: "« À privilégier » : c'est une recommandation. Elle n'a sa place nulle part dans l'évaluation 1, et surtout pas dans le résumé.",
  },
  {
    texte: "Des deux outils de réservation essayés, un seul reçoit les réservations de Viator sans qu'on les recopie. Les doubles réservations de l'été 2026 venaient de cette recopie.",
    section: "Section 6",
    verdict: "oui",
    pourquoi: "Le résultat principal des essais de l'équipe, relié à un problème que Mélanie a vécu. Remarquez qu'il ne nomme pas de gagnant.",
  },
  {
    texte: "La page Facebook de l'entreprise compte environ 8 000 abonnés.",
    section: "Section 2",
    verdict: "non",
    pourquoi: "Vrai, mais ça ne change rien à la suite du projet. C'est du contexte.",
  },
  {
    texte: "Les deux outils offrent un widget en iframe compatible avec Wix et WordPress.",
    section: "Section 6",
    verdict: "non",
    pourquoi: "Technique, et sans conséquence claire pour Mélanie. Si c'est important, dites ce que ça veut dire : « les deux outils peuvent s'ajouter à un site Wix ou WordPress ».",
  },
  {
    texte: "L'ouverture des réservations le 1er mars 2027 laisse environ quatre mois pour choisir, mettre en place et essayer les outils. Pour vendre des cartes-cadeaux à Noël, il en reste moins de deux.",
    section: "Section 4",
    verdict: "oui",
    pourquoi: "Le délai est la contrainte la plus ferme du mandat. Il pèse sur tous les choix de la proposition technique.",
  },
  {
    texte: "Les décharges contiennent des renseignements de santé, dont ceux de mineurs : la Loi 25 impose des obligations de protection, quel que soit l'outil choisi.",
    section: "Sections 3 et 5",
    verdict: "defendable",
    pourquoi: "Un bon candidat : il touche tout le projet. S'il entre, un autre doit sortir. Lequel pèse le moins pour Mélanie ? On peut aussi le joindre à un autre constat en une phrase.",
  },
  {
    texte: "Le prix de Réservio est de 49 $ US par mois (page de prix consultée le 20 octobre 2026).",
    section: "Section 6",
    verdict: "non",
    pourquoi: "Un prix au mois, en dollars américains, pour un seul outil : un détail. Le résumé parle du coût par année, en dollars canadiens, pour l'ensemble.",
  },
];

const RESUME = [
  {
    role: "Ce que le projet demande",
    texte: "Aventure Saint-Maurice veut un nouveau site qui permette de réserver et de payer en ligne, de signer la décharge avant l'arrivée et de consulter le contenu en français et en anglais. Il doit être prêt pour l'ouverture des réservations, le 1er mars 2027.",
  },
  {
    role: "Les constats, du plus bloquant au moins bloquant",
    texte: "Quatre constats pèsent sur la suite du projet. D'abord, le compte Wix et le nom de domaine appartiennent au neveu de Patrick : sans ses accès, le site actuel ne peut être ni gardé ni déplacé. Ensuite, le délai est court : environ quatre mois avant le 1er mars, et moins de deux avant Noël pour les cartes-cadeaux. Le budget de 8 000 $ couvre la construction, mais pas les abonnements, qui coûteraient de 1 400 $ à 3 900 $ par année selon les outils. Enfin, des deux outils de réservation essayés, un seul reçoit les réservations de Viator sans qu'on les recopie, ce qui touche directement les doubles réservations de l'été 2026.",
  },
  {
    role: "Ce qui suivra",
    texte: "La proposition technique présentera ensuite les choix recommandés, les coûts et l'échéancier. Avant de la préparer, quelques points doivent être vérifiés avec l'entreprise (section 7).",
  },
];

const props = withDefaults(defineProps<{ storageKey?: string }>(), {
  storageKey: "asm-choisir-resume",
});

const etat = reactive({ choisis: [] as number[], verifie: false });

const pleins = computed(() => etat.choisis.length >= MAX);

function basculer(n: number) {
  if (etat.verifie) return;
  if (etat.choisis.includes(n)) etat.choisis = etat.choisis.filter((x) => x !== n);
  else if (!pleins.value) etat.choisis = [...etat.choisis, n];
}

const bons = computed(() => etat.choisis.filter((n) => PHRASES[n].verdict !== "non").length);

function texteReponses() {
  const choisies = [...etat.choisis].sort((a, b) => a - b);
  return [
    "Séance 5 — Activité 2 : ce qui va dans le résumé",
    "",
    "Nos choix :",
    ...(choisies.length ? choisies.map((n) => `   ${n + 1}. ${PHRASES[n].texte}`) : ["   —"]),
    "",
    "Le verdict pour chaque phrase :",
    ...PHRASES.map(
      (p, n) => `   ${n + 1}. ${etat.choisis.includes(n) ? "[choisie] " : ""}${VERDICTS[p.verdict]} — ${p.pourquoi}`,
    ),
    "",
    "Un résumé possible :",
    ...RESUME.map((r) => `   [${r.role}] ${r.texte}`),
  ].join("\n");
}

function reinitialiser() {
  if (!confirm("Effacer vos choix ? Avez-vous copié vos réponses ?")) return;
  Object.assign(etat, { choisis: [], verifie: false });
}

onMounted(() => {
  try {
    const data = JSON.parse(localStorage.getItem(props.storageKey) ?? "null");
    if (!data || !Array.isArray(data.choisis)) return;
    etat.choisis = data.choisis.filter((n: unknown) => Number.isInteger(n) && (n as number) < PHRASES.length).slice(0, MAX);
    etat.verifie = Boolean(data.verifie) && etat.choisis.length > 0;
  } catch {
    /* stockage indisponible : on part de choix vides */
  }
});

watch(etat, () => {
  try {
    localStorage.setItem(props.storageKey, JSON.stringify(etat));
  } catch {
    /* stockage indisponible : rien à faire */
  }
});
</script>

<template>
  <section class="rs">
    <p class="rs-compte">
      <strong>{{ etat.choisis.length }} / {{ MAX }}</strong> phrases choisies
      <span v-if="pleins && !etat.verifie" class="rs-aide">— retirez-en une pour en choisir une autre</span>
    </p>

    <ol class="rs-liste">
      <li v-for="(p, n) in PHRASES" :key="n" class="rs-item">
        <button
          type="button"
          class="rs-carte"
          :class="{
            'is-choisi': etat.choisis.includes(n),
            ['is-' + p.verdict]: etat.verifie,
          }"
          :aria-pressed="etat.choisis.includes(n)"
          :disabled="etat.verifie || (pleins && !etat.choisis.includes(n))"
          @click="basculer(n)"
        >
          <span class="rs-case" aria-hidden="true">{{ etat.choisis.includes(n) ? "✓" : "" }}</span>
          <span class="rs-texte">{{ p.texte }}</span>
          <span class="rs-section">{{ p.section }}</span>
        </button>
        <p v-if="etat.verifie" class="rs-retro" :class="'is-' + p.verdict">
          <strong>{{ VERDICTS[p.verdict] }}.</strong> {{ p.pourquoi }}
        </p>
      </li>
    </ol>

    <div class="rs-verifier">
      <button v-if="!etat.verifie" type="button" class="rs-action is-principal" :disabled="!etat.choisis.length" @click="etat.verifie = true">
        Vérifier
      </button>
      <template v-else>
        <span><strong>{{ bons }} / {{ etat.choisis.length }}</strong> de vos choix ont leur place dans le résumé.</span>
        <button type="button" class="rs-lien" @click="etat.verifie = false">Modifier mes choix</button>
      </template>
    </div>

    <div v-if="etat.verifie" class="rs-resume">
      <p class="rs-titre">Un résumé possible (environ 180 mots)</p>
      <div v-for="r in RESUME" :key="r.role" class="rs-bloc">
        <span class="rs-role">{{ r.role }}</span>
        <p>{{ r.texte }}</p>
      </div>
    </div>

    <p class="rs-rappel">Vos choix restent dans ce navigateur, mais ils peuvent disparaître si la cache est vidée. <strong>Copiez-les dans vos notes</strong> avant de quitter la page.</p>
    <div class="rs-pied">
      <span />
      <span class="rs-actions">
        <BoutonCopier :texte="texteReponses" />
        <button type="button" class="rs-action" @click="reinitialiser">Recommencer</button>
      </span>
    </div>
  </section>
</template>

<style scoped>
.rs {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.rs-compte { margin: 0 0 0.6rem !important; font-size: 0.875rem; }
.rs-aide { color: var(--vp-c-text-2); }
.rs-liste {
  display: grid;
  gap: 0.5rem;
  margin: 0 !important;
  padding: 0 !important;
  list-style: none !important;
}
.rs-item { margin: 0 !important; }
.rs-carte {
  display: grid;
  grid-template-columns: 1.4rem 1fr auto;
  align-items: start;
  gap: 0.6rem;
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 1px solid var(--vp-c-divider);
  border-left-width: 4px;
  border-radius: 0.6rem;
  background: var(--vp-c-bg);
  text-align: left;
  font-size: 0.88rem;
  line-height: 1.5;
  transition: border-color 0.15s, background-color 0.15s;
}
.rs-carte:hover:not(:disabled) { border-color: var(--vp-c-brand-1); }
.rs-carte:disabled { cursor: default; }
.rs-carte:disabled:not(.is-choisi):not(.is-oui):not(.is-defendable):not(.is-non) { opacity: 0.55; }
.rs-carte.is-choisi { border-color: var(--vp-c-brand-1); background: var(--vp-c-brand-soft); }
.rs-carte.is-oui { border-left-color: var(--vp-c-green-2); }
.rs-carte.is-defendable { border-left-color: var(--vp-c-yellow-2); }
.rs-carte.is-non { border-left-color: var(--vp-c-red-2); }
.rs-case {
  display: grid;
  place-items: center;
  width: 1.2rem;
  height: 1.2rem;
  margin-top: 0.1rem;
  border: 1.5px solid var(--vp-c-divider);
  border-radius: 0.3rem;
  background: var(--vp-c-bg);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--vp-c-brand-1);
}
.is-choisi .rs-case { border-color: var(--vp-c-brand-1); }
.rs-section {
  font-size: 0.72rem;
  white-space: nowrap;
  color: var(--vp-c-text-2);
}
@media (max-width: 560px) {
  .rs-carte { grid-template-columns: 1.4rem 1fr; }
  .rs-section { grid-column: 2; }
}
.rs-retro {
  margin: 0.3rem 0 0 1.25rem !important;
  font-size: 0.8rem;
  line-height: 1.5;
  color: var(--vp-c-text-2);
}
.rs-retro.is-oui strong { color: var(--vp-c-green-1); }
.rs-retro.is-defendable strong { color: var(--vp-c-yellow-1); }
.rs-retro.is-non strong { color: var(--vp-c-red-1); }
.rs-verifier {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.6rem;
  margin-top: 0.75rem;
  font-size: 0.875rem;
}
.rs-resume {
  margin-top: 0.9rem;
  padding: 0.8rem 0.9rem;
  border-radius: 0.6rem;
  background: var(--vp-c-green-soft);
}
.rs-titre { margin: 0 0 0.5rem !important; font-weight: 700; font-size: 0.9rem; }
.rs-bloc + .rs-bloc { margin-top: 0.55rem; }
.rs-role {
  display: block;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--vp-c-green-1);
}
.rs-bloc p { margin: 0.1rem 0 0 !important; font-size: 0.86rem; line-height: 1.55; }
.rs-lien { font-size: 0.78rem; font-weight: 600; color: var(--vp-c-brand-1); }
.rs-rappel {
  margin: 0.75rem 0 0.6rem !important;
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
.rs-pied {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
}
.rs-actions { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.rs-action {
  padding: 0.3rem 0.7rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.rs-action:hover:not(:disabled) { border-color: var(--vp-c-brand-1); }
.rs-action:disabled { opacity: 0.5; cursor: not-allowed; }
.rs-action.is-principal { border-color: var(--vp-c-brand-1); color: var(--vp-c-brand-1); font-weight: 600; }
</style>
