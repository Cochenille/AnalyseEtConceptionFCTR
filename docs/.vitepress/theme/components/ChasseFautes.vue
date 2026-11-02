<script setup lang="ts">
import { computed, onMounted, reactive, watch } from "vue";
import BoutonCopier from "./BoutonCopier.vue";

// Dans le texte, les fautes sont entre [[ ]] ; chacune a sa correction, sa sorte et sa règle.
type Faute = { correction: string; sorte: string; regle: string };
type Passage = { ou: string; texte: string; fautes: Record<string, Faute> };

const PASSAGES: Passage[] = [
  {
    ou: "Section 2.1 — Le client et sa situation actuelle",
    texte:
      "L'été dernier, l'entreprise a reçu environ [[2600]] réservations, dont [[55%]] par téléphone. Les réservations de Viator arrivent par courriel, et Karine les [[recopies]] dans un fichier Excel. Quand une journée est [[cancellée]] à cause de la météo, elle doit appeler les clients un par un. [[À date,]] aucun outil ne les prévient automatiquement.",
    fautes: {
      "2600": { correction: "2 600", sorte: "Typographie", regle: "On sépare les milliers par une espace, sans point ni virgule." },
      "55%": { correction: "55 %", sorte: "Typographie", regle: "Une espace (insécable) entre le nombre et le symbole %." },
      recopies: { correction: "recopie", sorte: "Conjugaison", regle: "Le sujet est « Karine » (3e personne du singulier) : elle recopie. « Recopies » est la 2e personne (tu recopies)." },
      cancellée: { correction: "annulée", sorte: "Anglicisme", regle: "« Canceller » vient de l'anglais to cancel. On écrit « annuler »." },
      "À date,": { correction: "Jusqu'à maintenant,", sorte: "Anglicisme", regle: "« À date » est calqué sur l'anglais to date. On écrit « jusqu'à maintenant » ou « jusqu'ici »." },
    },
  },
  {
    ou: "Section 6.1 — Avantages, limites et points à vérifier",
    texte:
      "Les deux outils [[qu'on a essayé]] gèrent les départs à places limitées. Avec PagayePro, la réservation de 5 places sur téléphone a pris [[2min40]] (essai E2, annexe A). Réservio [[supporte]] la synchronisation avec Viator, mais cette fonction n'était pas offerte dans la version d'essai : elle reste [[a]] vérifier. Les deux outils offrent des tutoriels, mais [[leur]] tutoriels sont en anglais seulement.",
    fautes: {
      "qu'on a essayé": { correction: "que nous avons essayés", sorte: "Accord et registre", regle: "Avec avoir, le participe passé s'accorde avec le complément placé avant (« que », mis pour « les outils ») : essayés. Dans un rapport, « nous » plutôt que « on »." },
      "2min40": { correction: "2 min 40 s", sorte: "Typographie", regle: "Les symboles d'unités s'écrivent après une espace, sans point et sans s au pluriel." },
      supporte: { correction: "prend en charge", sorte: "Anglicisme", regle: "Calqué sur to support. Un logiciel « prend en charge » une fonction, ou « permet » de faire quelque chose. « Supporter » veut dire endurer ou soutenir." },
      a: { correction: "à", sorte: "Homophone", regle: "« a » est le verbe avoir : on peut le remplacer par « avait ». Ici, c'est la préposition « à »." },
      leur: { correction: "leurs", sorte: "Accord", regle: "Devant un nom au pluriel (les tutoriels des deux outils), le déterminant « leur » prend un s." },
    },
  },
  {
    ou: "Section 6.1 — Comparaison (texte sous le tableau)",
    texte:
      "Sur trois ans, Réservio coûterait environ [[5 730$]], en comptant [[tout les]] frais annuels, au taux de 1,38 $ CA pour 1 $ US. Les essais de [[l'équipe,]] ont montré que la liste des participants ne s'affiche pas sans réseau. [[Ça]] pose un problème au quai, où le guide n'a pas de signal. La synchronisation avec Viator n'a pas pu être [[vérifié]] pendant l'essai; c'est un point à régler avant le [[1 mars]], date où le site doit être en ligne.",
    fautes: {
      "5 730$": { correction: "5 730 $", sorte: "Typographie", regle: "En français, le symbole $ se place après le nombre, séparé par une espace." },
      "tout les": { correction: "tous les", sorte: "Accord", regle: "Devant un nom masculin pluriel (les frais), « tout » s'écrit « tous »." },
      "l'équipe,": { correction: "l'équipe", sorte: "Ponctuation", regle: "Pas de virgule entre le sujet (les essais de l'équipe) et son verbe (ont montré)." },
      Ça: { correction: "Cela", sorte: "Registre", regle: "« Ça » appartient à la langue familière. Dans un rapport, on écrit « cela »." },
      vérifié: { correction: "vérifiée", sorte: "Accord", regle: "Avec être, le participe passé s'accorde avec le sujet : la synchronisation… n'a pas pu être vérifiée." },
      "1 mars": { correction: "1er mars", sorte: "Typographie", regle: "Le premier jour du mois s'écrit avec l'ordinal : 1er. Les autres jours, en chiffres simples (le 2 mars)." },
    },
  },
];

type Morceau = { texte: string; faute: boolean; espace: boolean };

// Découpe le passage en morceaux cliquables : une faute entière, ou un mot.
// Un morceau garde l'espace qui le précède dans le texte d'origine.
function decouper(texte: string): Morceau[] {
  return [...texte.matchAll(/(\s*)(?:\[\[([^\]]+)\]\]|([^\s[]+))/g)].map((r) => ({
    texte: r[2] ?? r[3],
    faute: r[2] !== undefined,
    espace: r[1].length > 0,
  }));
}

const MORCEAUX = PASSAGES.map((p) => decouper(p.texte));

const props = withDefaults(defineProps<{ storageKey?: string }>(), {
  storageKey: "asm-chasse-fautes",
});

const etat = reactive(PASSAGES.map(() => ({ choisis: [] as number[], verifie: false })));

function basculer(n: number, i: number) {
  const e = etat[n];
  if (e.verifie) return;
  e.choisis = e.choisis.includes(i) ? e.choisis.filter((x) => x !== i) : [...e.choisis, i];
}

function bilan(n: number) {
  const choisis = new Set(etat[n].choisis);
  const fautes = MORCEAUX[n].filter((m) => m.faute);
  return {
    trouvees: fautes.filter((m) => choisis.has(MORCEAUX[n].indexOf(m))).map((m) => m.texte),
    manquees: fautes.filter((m) => !choisis.has(MORCEAUX[n].indexOf(m))).map((m) => m.texte),
    enTrop: MORCEAUX[n].filter((m, i) => !m.faute && choisis.has(i)).map((m) => m.texte),
  };
}

function classe(n: number, i: number) {
  const m = MORCEAUX[n][i];
  const choisi = etat[n].choisis.includes(i);
  if (!etat[n].verifie) return { "is-choisi": choisi };
  return { "is-trouve": m.faute && choisi, "is-manque": m.faute && !choisi, "is-entrop": !m.faute && choisi };
}

const totalFautes = MORCEAUX.reduce((s, ms) => s + ms.filter((m) => m.faute).length, 0);
const trouvees = computed(() => PASSAGES.reduce((s, _, n) => s + (etat[n].verifie ? bilan(n).trouvees.length : 0), 0));
const verifies = computed(() => etat.filter((e) => e.verifie).length);

function texteReponses() {
  return [
    "Séance 6 — Activité 2 : la chasse aux fautes",
    "",
    ...PASSAGES.map((p, n) => {
      const e = etat[n];
      const b = bilan(n);
      const lignes = [`${n + 1}. ${p.ou}`, `   « ${p.texte.replace(/\[\[|\]\]/g, "")} »`];
      if (e.verifie) {
        lignes.push(`   Fautes trouvées : ${b.trouvees.join(" · ") || "—"}`);
        lignes.push(`   Fautes manquées : ${b.manquees.join(" · ") || "—"}`);
        if (b.enTrop.length) lignes.push(`   Mots corrects choisis : ${b.enTrop.join(" · ")}`);
      } else {
        lignes.push("   (pas encore vérifié)");
      }
      lignes.push(...Object.entries(p.fautes).map(([f, x]) => `   • ${f} → ${x.correction} (${x.sorte}) : ${x.regle}`));
      return lignes.join("\n");
    }),
  ].join("\n\n");
}

function reinitialiser() {
  if (!confirm("Effacer toutes vos réponses ? Avez-vous copié vos réponses ?")) return;
  for (const e of etat) Object.assign(e, { choisis: [], verifie: false });
}

onMounted(() => {
  try {
    const data = JSON.parse(localStorage.getItem(props.storageKey) ?? "null");
    if (!Array.isArray(data)) return;
    etat.forEach((e, n) => {
      const v = data[n];
      if (!v) return;
      e.choisis = Array.isArray(v.choisis) ? v.choisis.filter((i: unknown) => Number.isInteger(i) && (i as number) < MORCEAUX[n].length) : [];
      e.verifie = Boolean(v.verifie);
    });
  } catch {
    /* stockage indisponible : on part de réponses vides */
  }
});

watch(etat, () => {
  try {
    localStorage.setItem(props.storageKey, JSON.stringify(etat.map(({ choisis, verifie }) => ({ choisis, verifie }))));
  } catch {
    /* stockage indisponible : rien à faire */
  }
});
</script>

<template>
  <section class="cf">
    <ol class="cf-liste">
      <li v-for="(p, n) in PASSAGES" :key="n" class="cf-item">
        <span class="cf-ou">{{ p.ou }}</span>
        <p class="cf-passage" :class="{ 'is-verifie': etat[n].verifie }">
          <template v-for="(m, i) in MORCEAUX[n]" :key="i">
            <template v-if="m.espace">{{ " " }}</template>
            <button
              type="button"
              class="cf-mot"
              :class="classe(n, i)"
              :aria-pressed="etat[n].choisis.includes(i)"
              :disabled="etat[n].verifie"
              @click="basculer(n, i)"
            >{{ m.texte }}</button>
          </template>
        </p>

        <div class="cf-actions-passage">
          <button v-if="!etat[n].verifie" type="button" class="cf-action" :disabled="!etat[n].choisis.length" @click="etat[n].verifie = true">
            Vérifier
          </button>
          <button v-else type="button" class="cf-lien" @click="etat[n].verifie = false">Modifier mes choix</button>
        </div>

        <template v-if="etat[n].verifie">
          <p class="cf-retro">
            <strong>{{ bilan(n).trouvees.length }} / {{ Object.keys(p.fautes).length }}</strong> fautes trouvées.
            <span v-if="bilan(n).manquees.length"> Manquées : <em>{{ bilan(n).manquees.join(" · ") }}</em>.</span>
            <span v-if="bilan(n).enTrop.length"> Ces mots étaient corrects : <em>{{ bilan(n).enTrop.join(" · ") }}</em>.</span>
          </p>
          <table class="cf-fautes">
            <thead>
              <tr><th>Écrit</th><th>Corrigé</th><th>La règle</th></tr>
            </thead>
            <tbody>
              <tr v-for="(x, f) in p.fautes" :key="f">
                <td class="cf-non">{{ f }}</td>
                <td class="cf-oui">{{ x.correction }}</td>
                <td><strong>{{ x.sorte }}.</strong> {{ x.regle }}</td>
              </tr>
            </tbody>
          </table>
        </template>
      </li>
    </ol>

    <p class="cf-rappel">Vos réponses restent dans ce navigateur, mais elles peuvent disparaître si la cache est vidée. <strong>Copiez-les dans vos notes</strong> avant de quitter la page.</p>
    <div class="cf-pied">
      <span>
        <strong>{{ trouvees }} / {{ totalFautes }}</strong> fautes trouvées
        <span v-if="verifies < PASSAGES.length" class="cf-reste">({{ PASSAGES.length - verifies }} passages à vérifier)</span>
      </span>
      <span class="cf-actions">
        <BoutonCopier :texte="texteReponses" />
        <button type="button" class="cf-action" @click="reinitialiser">Recommencer</button>
      </span>
    </div>
  </section>
</template>

<style scoped>
.cf {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.cf-liste {
  margin: 0 !important;
  padding-left: 1.25rem !important;
}
.cf-item {
  margin: 0 !important;
  padding: 0.8rem 0;
  border-top: 1px solid var(--vp-c-divider);
}
.cf-item:first-child { border-top: 0; padding-top: 0; }
.cf-ou {
  display: block;
  margin-bottom: 0.25rem;
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--vp-c-text-2);
}
.cf-passage {
  margin: 0 !important;
  padding: 0.55rem 0.8rem;
  border: 1px solid var(--vp-c-divider);
  border-left: 3px solid var(--vp-c-brand-1);
  border-radius: 0.5rem;
  background: var(--vp-c-bg);
  font-size: 0.95rem;
  line-height: 1.9;
}
.cf-mot {
  display: inline;
  padding: 0.05rem 0.15rem;
  margin: 0 -0.15rem;
  border-radius: 0.3rem;
  font: inherit;
  line-height: inherit;
  color: inherit;
  cursor: pointer;
  transition: background-color 0.15s;
}
.cf-mot:hover:not(:disabled) { background: var(--vp-c-default-soft); }
.cf-mot:disabled { cursor: default; }
.cf-mot.is-choisi { background: var(--vp-c-brand-soft); color: var(--vp-c-brand-1); font-weight: 600; }
.cf-mot.is-trouve { background: var(--vp-c-green-soft); color: var(--vp-c-green-1); font-weight: 600; }
.cf-mot.is-manque { background: var(--vp-c-yellow-soft); color: var(--vp-c-yellow-1); font-weight: 600; text-decoration: underline wavy; }
.cf-mot.is-entrop { background: var(--vp-c-red-soft); color: var(--vp-c-red-1); text-decoration: line-through; }
.cf-actions-passage { margin-top: 0.4rem; }
.cf-retro {
  margin: 0.45rem 0 0 !important;
  font-size: 0.82rem;
  line-height: 1.5;
  color: var(--vp-c-text-2);
}
.cf-fautes {
  display: table;
  width: 100%;
  margin: 0.4rem 0 0 !important;
  border-collapse: collapse;
  font-size: 0.8rem;
  line-height: 1.45;
}
.cf-fautes th,
.cf-fautes td {
  padding: 0.35rem 0.55rem !important;
  border: 1px solid var(--vp-c-divider) !important;
  vertical-align: top;
}
.cf-fautes th { background: var(--vp-c-bg); font-size: 0.75rem; }
.cf-fautes tr { background: var(--vp-c-bg) !important; }
.cf-non { color: var(--vp-c-red-1); text-decoration: line-through; white-space: nowrap; }
.cf-oui { color: var(--vp-c-green-1); font-weight: 600; white-space: nowrap; }
.cf-lien {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--vp-c-brand-1);
}
.cf-rappel {
  margin: 0.5rem 0 0.6rem !important;
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
.cf-pied {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.875rem;
}
.cf-reste { color: var(--vp-c-text-2); }
.cf-actions { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.cf-action {
  padding: 0.3rem 0.7rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.cf-action:hover:not(:disabled) { border-color: var(--vp-c-brand-1); }
.cf-action:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
