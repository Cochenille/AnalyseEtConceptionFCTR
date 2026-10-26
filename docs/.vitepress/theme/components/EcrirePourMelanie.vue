<script setup lang="ts">
import { computed, onMounted, reactive, watch } from "vue";
import BoutonCopier from "./BoutonCopier.vue";

// Dans le texte, les termes techniques sont entre [[ ]] ; chacun a son explication.
type Phrase = { texte: string; termes: Record<string, string>; reecriture: string };

const PHRASES: Phrase[] = [
  {
    texte: "Le [[CMS]] offre un [[plugin]] de réservation qui échange les réservations avec Viator par [[API]].",
    termes: {
      CMS: "Le logiciel qui sert à construire et à modifier le site (Wix, WordPress…).",
      plugin: "Un module qu'on ajoute au site pour lui donner une fonction de plus.",
      API: "Une porte d'échange entre deux logiciels, qui leur permet de se transmettre des données automatiquement.",
    },
    reecriture: "La plateforme du site offre un module de réservation qui reçoit automatiquement les réservations faites sur Viator : personne n'a à les recopier.",
  },
  {
    texte: "Avec la vidéo d'accueil, le [[LCP]] mobile monte à 4,1 s, au-delà du seuil des [[Core Web Vitals]].",
    termes: {
      LCP: "Le temps que met le contenu principal de la page à s'afficher.",
      "Core Web Vitals": "Les mesures de vitesse et de stabilité que Google utilise pour juger une page.",
    },
    reecriture: "Avec la vidéo d'accueil, la page met 4,1 secondes à afficher son contenu principal sur un téléphone. Google juge qu'une page est lente au-delà de 2,5 secondes (PageSpeed Insights, essai E5).",
  },
  {
    texte: "Les décharges contiennent des données de santé : l'outil doit offrir le [[chiffrement au repos]], et un [[hébergement]] hors Québec exige une [[EFVP]].",
    termes: {
      "chiffrement au repos": "Les fichiers sont codés là où ils sont conservés : quelqu'un qui les volerait ne pourrait pas les lire.",
      hébergement: "Les ordinateurs (serveurs) où les données sont conservées, et le pays où ils se trouvent.",
      EFVP: "L'évaluation des facteurs relatifs à la vie privée, que la Loi 25 exige avant de confier des renseignements personnels à l'extérieur du Québec.",
    },
    reecriture: "Les décharges contiennent des renseignements sur la santé des participants, dont des mineurs. L'outil doit les conserver sous une forme illisible pour quelqu'un qui volerait les fichiers. S'ils sont conservés à l'extérieur du Québec, la Loi 25 oblige l'entreprise à évaluer d'abord s'ils y seront bien protégés.",
  },
  {
    texte: "Au quai, l'application du guide lit la liste des participants en [[cache]] et fait la [[synchro]] dès que le réseau revient.",
    termes: {
      cache: "Une copie des données gardée sur le téléphone, qu'on peut consulter sans réseau.",
      synchro: "La mise à jour automatique entre le téléphone et le système central.",
    },
    reecriture: "L'application du guide enregistre la liste des participants sur son téléphone pendant qu'il a du réseau, au chalet. Au quai, il peut la consulter sans réseau. Ce qu'il y change est transmis dès que le téléphone retrouve du réseau.",
  },
  {
    texte: "Le [[DNS]] du domaine pointe encore vers Wix, et le [[registraire]] a le neveu comme [[titulaire]].",
    termes: {
      DNS: "Le système qui relie une adresse comme aventure-stmaurice.com au serveur qui affiche le site.",
      registraire: "L'entreprise auprès de qui on loue le nom de domaine (par exemple GoDaddy).",
      titulaire: "La personne qui est officiellement propriétaire du nom de domaine.",
    },
    reecriture: "L'adresse aventure-stmaurice.com mène encore au site Wix. Elle est officiellement au nom du neveu de Patrick, auprès de l'entreprise qui la loue (probablement GoDaddy) : sans son accord, on ne peut pas la relier à un nouveau site.",
  },
  {
    texte: "Traduco traduit les pages [[à la volée]] et ajoute les [[balises hreflang]] pour le [[SEO]]; le forfait de base plafonne à 10 000 mots.",
    termes: {
      "à la volée": "Automatiquement, au moment où la page est affichée.",
      "balises hreflang": "Une indication cachée dans la page qui dit à Google qu'une version dans une autre langue existe.",
      SEO: "Le référencement : ce qui aide le site à bien paraître dans les résultats de Google.",
    },
    reecriture: "Traduco traduit automatiquement chaque page en anglais. Il indique aussi à Google qu'une version anglaise existe, pour qu'elle soit proposée aux visiteurs anglophones. Le forfait de base traduit au plus 10 000 mots (page de prix consultée le 20 octobre 2026).",
  },
];

type Morceau = { texte: string; terme: boolean; espace: boolean };

// Découpe la phrase en morceaux cliquables : un terme technique entier, ou un mot.
// Un morceau garde l'espace qui le précède dans le texte d'origine.
function decouper(texte: string): Morceau[] {
  return [...texte.matchAll(/(\s*)(?:\[\[([^\]]+)\]\]|([^\s[]+))/g)].map((r) => ({
    texte: r[2] ?? r[3],
    terme: r[2] !== undefined,
    espace: r[1].length > 0,
  }));
}

const MORCEAUX = PHRASES.map((p) => decouper(p.texte));

const props = withDefaults(defineProps<{ storageKey?: string }>(), {
  storageKey: "asm-ecrire-pour-melanie",
});

const etat = reactive(PHRASES.map(() => ({ choisis: [] as number[], verifie: false, reecriture: "", voir: false })));

function basculer(n: number, i: number) {
  const e = etat[n];
  if (e.verifie) return;
  e.choisis = e.choisis.includes(i) ? e.choisis.filter((x) => x !== i) : [...e.choisis, i];
}

function bilan(n: number) {
  const choisis = new Set(etat[n].choisis);
  const termes = MORCEAUX[n].filter((m) => m.terme);
  return {
    trouves: termes.filter((m) => choisis.has(MORCEAUX[n].indexOf(m))).map((m) => m.texte),
    manques: termes.filter((m) => !choisis.has(MORCEAUX[n].indexOf(m))).map((m) => m.texte),
    enTrop: MORCEAUX[n].filter((m, i) => !m.terme && choisis.has(i)).map((m) => m.texte),
  };
}

function classe(n: number, i: number) {
  const m = MORCEAUX[n][i];
  const choisi = etat[n].choisis.includes(i);
  if (!etat[n].verifie) return { "is-choisi": choisi };
  return { "is-trouve": m.terme && choisi, "is-manque": m.terme && !choisi, "is-entrop": !m.terme && choisi };
}

const totalTermes = MORCEAUX.reduce((s, ms) => s + ms.filter((m) => m.terme).length, 0);
const trouves = computed(() => PHRASES.reduce((s, _, n) => s + (etat[n].verifie ? bilan(n).trouves.length : 0), 0));
const verifiees = computed(() => etat.filter((e) => e.verifie).length);

function texteReponses() {
  return [
    "Séance 5 — Activité 1 : écrire pour Mélanie",
    "",
    ...PHRASES.map((p, n) => {
      const e = etat[n];
      const b = bilan(n);
      const lignes = [`${n + 1}. « ${p.texte.replace(/\[\[|\]\]/g, "")} »`];
      if (e.verifie) {
        lignes.push(`   Termes trouvés : ${b.trouves.join(", ") || "—"}`);
        lignes.push(`   Termes manqués : ${b.manques.join(", ") || "—"}`);
        if (b.enTrop.length) lignes.push(`   Mots choisis qui ne sont pas du jargon : ${b.enTrop.join(", ")}`);
      } else {
        lignes.push("   (pas encore vérifiée)");
      }
      lignes.push(...Object.entries(p.termes).map(([t, def]) => `   • ${t} : ${def}`));
      lignes.push(`   Notre réécriture : ${e.reecriture.trim() || "—"}`);
      lignes.push(`   Réécriture possible : ${p.reecriture}`);
      return lignes.join("\n");
    }),
  ].join("\n\n");
}

function reinitialiser() {
  if (!confirm("Effacer toutes vos réponses ? Avez-vous copié vos réponses ?")) return;
  for (const e of etat) Object.assign(e, { choisis: [], verifie: false, reecriture: "", voir: false });
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
      e.reecriture = String(v.reecriture ?? "");
    });
  } catch {
    /* stockage indisponible : on part de réponses vides */
  }
});

watch(etat, () => {
  try {
    localStorage.setItem(props.storageKey, JSON.stringify(etat.map(({ choisis, verifie, reecriture }) => ({ choisis, verifie, reecriture }))));
  } catch {
    /* stockage indisponible : rien à faire */
  }
});
</script>

<template>
  <section class="em">
    <ol class="em-liste">
      <li v-for="(p, n) in PHRASES" :key="n" class="em-item">
        <p class="em-phrase" :class="{ 'is-verifie': etat[n].verifie }">
          <template v-for="(m, i) in MORCEAUX[n]" :key="i">
            <template v-if="m.espace">{{ " " }}</template>
            <button
              type="button"
              class="em-mot"
              :class="classe(n, i)"
              :aria-pressed="etat[n].choisis.includes(i)"
              :disabled="etat[n].verifie"
              @click="basculer(n, i)"
            >{{ m.texte }}</button>
          </template>
        </p>

        <div class="em-actions-phrase">
          <button v-if="!etat[n].verifie" type="button" class="em-action" :disabled="!etat[n].choisis.length" @click="etat[n].verifie = true">
            Vérifier
          </button>
          <button v-else type="button" class="em-lien" @click="etat[n].verifie = false">Modifier mes choix</button>
        </div>

        <template v-if="etat[n].verifie">
          <p class="em-retro">
            <strong>{{ bilan(n).trouves.length }} / {{ Object.keys(p.termes).length }}</strong> termes techniques trouvés.
            <span v-if="bilan(n).manques.length"> Manqués : <em>{{ bilan(n).manques.join(", ") }}</em>.</span>
            <span v-if="bilan(n).enTrop.length"> Mélanie connaît déjà : <em>{{ bilan(n).enTrop.join(", ") }}</em>.</span>
          </p>
          <dl class="em-termes">
            <template v-for="(def, t) in p.termes" :key="t">
              <dt>{{ t }}</dt>
              <dd>{{ def }}</dd>
            </template>
          </dl>
        </template>

        <div class="em-reecrire">
          <label class="em-label" :for="'em-r-' + n">Notre réécriture pour Mélanie (gardez les mesures et les faits)</label>
          <textarea :id="'em-r-' + n" v-model="etat[n].reecriture" class="em-zone" rows="2" />
          <button type="button" class="em-lien" :aria-expanded="etat[n].voir" @click="etat[n].voir = !etat[n].voir">
            {{ etat[n].voir ? "Cacher" : "Voir une réécriture possible" }}
          </button>
          <p v-if="etat[n].voir" class="em-modele">{{ p.reecriture }}</p>
        </div>
      </li>
    </ol>

    <p class="em-rappel">Vos réponses restent dans ce navigateur, mais elles peuvent disparaître si la cache est vidée. <strong>Copiez-les dans vos notes</strong> avant de quitter la page.</p>
    <div class="em-pied">
      <span>
        <strong>{{ trouves }} / {{ totalTermes }}</strong> termes techniques trouvés
        <span v-if="verifiees < PHRASES.length" class="em-reste">({{ PHRASES.length - verifiees }} phrases à vérifier)</span>
      </span>
      <span class="em-actions">
        <BoutonCopier :texte="texteReponses" />
        <button type="button" class="em-action" @click="reinitialiser">Recommencer</button>
      </span>
    </div>
  </section>
</template>

<style scoped>
.em {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.em-liste {
  margin: 0 !important;
  padding-left: 1.25rem !important;
}
.em-item {
  margin: 0 !important;
  padding: 0.8rem 0;
  border-top: 1px solid var(--vp-c-divider);
}
.em-item:first-child { border-top: 0; padding-top: 0; }
.em-phrase {
  margin: 0 !important;
  padding: 0.55rem 0.8rem;
  border: 1px solid var(--vp-c-divider);
  border-left: 3px solid var(--vp-c-brand-1);
  border-radius: 0.5rem;
  background: var(--vp-c-bg);
  font-size: 0.95rem;
  line-height: 1.9;
}
.em-mot {
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
.em-mot:hover:not(:disabled) { background: var(--vp-c-default-soft); }
.em-mot:disabled { cursor: default; }
.em-mot.is-choisi { background: var(--vp-c-brand-soft); color: var(--vp-c-brand-1); font-weight: 600; }
.em-mot.is-trouve { background: var(--vp-c-green-soft); color: var(--vp-c-green-1); font-weight: 600; }
.em-mot.is-manque { background: var(--vp-c-yellow-soft); color: var(--vp-c-yellow-1); font-weight: 600; text-decoration: underline wavy; }
.em-mot.is-entrop { background: var(--vp-c-red-soft); color: var(--vp-c-red-1); text-decoration: line-through; }
.em-actions-phrase { margin-top: 0.4rem; }
.em-retro {
  margin: 0.45rem 0 0 !important;
  font-size: 0.82rem;
  line-height: 1.5;
  color: var(--vp-c-text-2);
}
.em-termes {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 0.2rem 0.75rem;
  margin: 0.4rem 0 0;
  padding: 0.5rem 0.7rem;
  border-radius: 0.5rem;
  background: var(--vp-c-bg);
  font-size: 0.8rem;
  line-height: 1.45;
}
.em-termes dt { font-weight: 700; }
.em-termes dd { margin: 0; color: var(--vp-c-text-2); }
@media (max-width: 560px) {
  .em-termes { grid-template-columns: 1fr; }
  .em-termes dd { margin-bottom: 0.3rem; }
}
.em-reecrire { margin-top: 0.6rem; }
.em-label {
  display: block;
  margin-bottom: 0.2rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
.em-zone {
  width: 100%;
  padding: 0.4rem 0.55rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.5rem;
  background: var(--vp-c-bg);
  font: inherit;
  font-size: 0.85rem;
  resize: vertical;
}
.em-zone:focus { outline: none; border-color: var(--vp-c-brand-1); }
.em-lien {
  margin-top: 0.25rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--vp-c-brand-1);
}
.em-modele {
  margin: 0.3rem 0 0 !important;
  padding: 0.45rem 0.65rem;
  border-radius: 0.5rem;
  background: var(--vp-c-green-soft);
  font-size: 0.82rem;
  line-height: 1.5;
}
.em-rappel {
  margin: 0.5rem 0 0.6rem !important;
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
.em-pied {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.875rem;
}
.em-reste { color: var(--vp-c-text-2); }
.em-actions { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.em-action {
  padding: 0.3rem 0.7rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.em-action:hover:not(:disabled) { border-color: var(--vp-c-brand-1); }
.em-action:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
