<script setup lang="ts">
import { computed, onMounted, reactive, watch } from "vue";
import BoutonCopier from "./BoutonCopier.vue";

// Les critères 1 à 7 de la grille de l'évaluation 1 (le français, critère 8, a son activité à part).
const CRITERES = [
  { n: 1, titre: "Organisation et clarté" },
  { n: 2, titre: "Mise en contexte" },
  { n: 3, titre: "Exigences" },
  { n: 4, titre: "Contraintes" },
  { n: 5, titre: "Risques" },
  { n: 6, titre: "Possibilités techniques" },
  { n: 7, titre: "Problèmes et questions au client" },
];

type Extrait = { ou: string; texte: string; critere: number; probleme: string; correction: string };

const EXTRAITS: Extrait[] = [
  {
    ou: "Section 3.2 — Comment il doit le faire",
    texte: "Le site doit être rapide et facile à utiliser sur tous les appareils.",
    critere: 3,
    probleme: "Rien ne permet de vérifier l'exigence : rapide comment, sur quel appareil, mesuré avec quoi ? « Tous les appareils » ne se vérifie pas non plus.",
    correction: "Sur un téléphone avec une connexion 4G, la page d'accueil affiche son contenu principal en moins de 2,5 secondes (mesure PageSpeed Insights). Le site fonctionne dans Safari sur iPhone et dans Chrome sur Android, dans leurs deux dernières versions.",
  },
  {
    ou: "Section 4.1 — Tableau des contraintes",
    texte: "Le budget du client est limité.",
    critere: 4,
    probleme: "Une contrainte générique, qu'on pourrait copier dans n'importe quel rapport : pas de chiffre, pas de source, pas d'effet sur le projet.",
    correction: "Le budget de construction est d'environ 8 000 $, ou 13 000 $ si la subvention de la MRC est accordée. Il ne prévoit rien pour les abonnements annuels des outils (mandat, notes de la rencontre).",
  },
  {
    ou: "Section 5.1 — Tableau des risques",
    texte: "R4 — Le budget est de 8 000 $. Chances : élevées. Conséquences : graves.",
    critere: 5,
    probleme: "C'est une contrainte déguisée en risque : le budget est déjà connu, il n'a rien d'incertain. Un risque est un événement qui pourrait arriver, ou pas.",
    correction: "R4 — La MRC refuse la subvention de 5 000 $, et le budget de construction reste à 8 000 $ (réponse attendue, selon le mandat).",
  },
  {
    ou: "Section 6.1 — Tableau de comparaison",
    texte: "Coût : 49 $ par mois.",
    critere: 6,
    probleme: "La page de prix de l'outil est en dollars américains. Le montant est présenté comme s'il était en dollars canadiens, au mois plutôt que sur trois ans, sans date ni source.",
    correction: "49 $ US par mois, soit environ 811 $ CA par année au taux de 1,38 $ (page de prix consultée le 20 octobre 2026). Coût sur trois ans : environ 2 434 $ CA (hypothèses sous le tableau).",
  },
  {
    ou: "Section 6.1 — Avantages, limites et points à vérifier",
    texte: "PagayePro est un outil complet, populaire et reconnu, qui offre de nombreuses fonctionnalités.",
    critere: 6,
    probleme: "Un avantage générique, qui vient du site du vendeur et ne dit rien de ce client-ci : ni Viator, ni le réseau au quai, ni Mélanie. « Populaire et reconnu » n'est appuyé par rien.",
    correction: "PagayePro gère les départs à 8 places de la via ferrata (essai E1, annexe A). En revanche, il ne reçoit pas les réservations de Viator : Karine aurait encore à les recopier, ce qui est la cause des doubles réservations de l'été 2026.",
  },
  {
    ou: "Section 7.2 — Les questions à poser au client",
    texte: "Êtes-vous d'accord pour qu'on utilise WordPress ?",
    critere: 7,
    probleme: "La question dicte une solution (et c'est une recommandation déguisée). Elle ne sert pas à mieux comprendre le besoin du client.",
    correction: "Qui, chez vous, modifiera le site pendant l'hiver, et combien d'heures par mois cette personne peut-elle y consacrer ?",
  },
  {
    ou: "Section 2.3 — La portée de ce rapport",
    texte: "Ce rapport présente les exigences, les contraintes et les risques, puis conclut sur les meilleures solutions pour votre projet.",
    critere: 2,
    probleme: "La portée promet une recommandation. Ce rapport décrit; c'est la proposition technique qui choisira.",
    correction: "Ce rapport décrit ce que le projet exige et les possibilités qui existent pour le réaliser. Il ne fait pas de choix : la proposition technique, remise en décembre, choisira les outils, estimera les coûts de construction et proposera un échéancier.",
  },
  {
    ou: "Section 4.2 — Ce qui existe déjà",
    texte: "Le CMS actuel est hébergé sur un plan SaaS et le DNS du domaine est géré par le registraire.",
    critere: 1,
    probleme: "Quatre termes techniques dans une seule phrase, aucun expliqué. Mélanie ne sait pas ce que la phrase change pour elle.",
    correction: "Le site actuel est construit sur Wix, un service payé par abonnement. L'adresse aventure-stmaurice.com est louée à une autre entreprise, au nom du neveu de Patrick : sans son accord, on ne peut pas la relier à un nouveau site.",
  },
];

const props = withDefaults(defineProps<{ storageKey?: string }>(), {
  storageKey: "asm-ou-ca-perd-des-points",
});

const etat = reactive(EXTRAITS.map(() => ({ choix: null as number | null, correction: "", voir: false })));

const score = computed(() => etat.filter((e, n) => e.choix === EXTRAITS[n].critere).length);
const repondus = computed(() => etat.filter((e) => e.choix !== null).length);

const nom = (c: number | null) => {
  const x = CRITERES.find((k) => k.n === c);
  return x ? `critère ${x.n} — ${x.titre}` : "—";
};

function texteReponses() {
  return [
    "Séance 6 — Activité 1 : où vous perdez des points ?",
    "",
    ...EXTRAITS.map((x, n) => {
      const e = etat[n];
      return [
        `${n + 1}. ${x.ou} : « ${x.texte} »`,
        `   Notre choix : ${nom(e.choix)} (attendu : ${nom(x.critere)})`,
        `   Le problème : ${x.probleme}`,
        `   Notre correction : ${e.correction.trim() || "—"}`,
        `   Correction possible : ${x.correction}`,
      ].join("\n");
    }),
  ].join("\n\n");
}

function reinitialiser() {
  if (!confirm("Effacer toutes vos réponses ? Avez-vous copié vos réponses ?")) return;
  for (const e of etat) Object.assign(e, { choix: null, correction: "", voir: false });
}

onMounted(() => {
  try {
    const data = JSON.parse(localStorage.getItem(props.storageKey) ?? "null");
    if (!Array.isArray(data)) return;
    etat.forEach((e, n) => {
      const v = data[n];
      if (!v) return;
      e.choix = CRITERES.some((c) => c.n === v.choix) ? v.choix : null;
      e.correction = String(v.correction ?? "");
    });
  } catch {
    /* stockage indisponible : on part de réponses vides */
  }
});

watch(etat, () => {
  try {
    localStorage.setItem(props.storageKey, JSON.stringify(etat.map(({ choix, correction }) => ({ choix, correction }))));
  } catch {
    /* stockage indisponible : rien à faire */
  }
});
</script>

<template>
  <section class="op">
    <ol class="op-liste">
      <li v-for="(x, n) in EXTRAITS" :key="n" class="op-item">
        <span class="op-ou">{{ x.ou }}</span>
        <blockquote class="op-phrase">« {{ x.texte }} »</blockquote>
        <div class="op-boutons" role="group" :aria-label="'Critère touché par l\'extrait ' + (n + 1)">
          <button
            v-for="c in CRITERES"
            :key="c.n"
            type="button"
            class="op-btn"
            :class="{
              'is-bon': etat[n].choix !== null && c.n === x.critere,
              'is-mauvais': etat[n].choix === c.n && c.n !== x.critere,
            }"
            :aria-pressed="etat[n].choix === c.n"
            :title="c.titre"
            @click="etat[n].choix = c.n"
          >
            <strong>{{ c.n }}</strong> {{ c.titre }}
          </button>
        </div>

        <template v-if="etat[n].choix !== null">
          <p class="op-retro" :class="etat[n].choix === x.critere ? 'is-bon' : 'is-mauvais'">
            <strong>{{ etat[n].choix === x.critere ? "Oui." : "Plutôt le " + nom(x.critere) + "." }}</strong>
            {{ x.probleme }}
          </p>
          <div class="op-corriger">
            <label class="op-label" :for="'op-c-' + n">Notre correction (inventez la mesure ou la source au besoin)</label>
            <textarea :id="'op-c-' + n" v-model="etat[n].correction" class="op-zone" rows="2" />
            <button type="button" class="op-lien" :aria-expanded="etat[n].voir" @click="etat[n].voir = !etat[n].voir">
              {{ etat[n].voir ? "Cacher" : "Voir une correction possible" }}
            </button>
            <p v-if="etat[n].voir" class="op-modele">{{ x.correction }}</p>
          </div>
        </template>
      </li>
    </ol>

    <p class="op-rappel">Vos réponses restent dans ce navigateur, mais elles peuvent disparaître si la cache est vidée. <strong>Copiez-les dans vos notes</strong> avant de quitter la page.</p>
    <div class="op-pied">
      <span>
        <strong>{{ score }} / {{ EXTRAITS.length }}</strong> critères trouvés
        <span v-if="repondus < EXTRAITS.length" class="op-reste">({{ EXTRAITS.length - repondus }} à faire)</span>
      </span>
      <span class="op-actions">
        <BoutonCopier :texte="texteReponses" />
        <button type="button" class="op-action" @click="reinitialiser">Recommencer</button>
      </span>
    </div>
  </section>
</template>

<style scoped>
.op {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.op-liste {
  margin: 0 !important;
  padding-left: 1.25rem !important;
}
.op-item {
  margin: 0 !important;
  padding: 0.8rem 0;
  border-top: 1px solid var(--vp-c-divider);
}
.op-item:first-child { border-top: 0; padding-top: 0; }
.op-ou {
  display: block;
  margin-bottom: 0.25rem;
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--vp-c-text-2);
}
.op-phrase {
  margin: 0 !important;
  padding: 0.55rem 0.8rem !important;
  border: 1px solid var(--vp-c-divider) !important;
  border-left: 3px solid var(--vp-c-brand-1) !important;
  border-radius: 0.5rem;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1) !important;
  font-size: 0.9rem !important;
  line-height: 1.5;
}
.op-boutons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin-top: 0.5rem;
}
.op-btn {
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.78rem;
  font-weight: 500;
  transition: border-color 0.15s, background-color 0.15s;
}
.op-btn:hover { border-color: var(--vp-c-brand-1); }
.op-btn[aria-pressed="true"] { border-color: var(--vp-c-brand-1); }
.op-btn.is-bon { border-color: var(--vp-c-green-2); background: var(--vp-c-green-soft); color: var(--vp-c-green-1); }
.op-btn.is-mauvais { border-color: var(--vp-c-red-2); background: var(--vp-c-red-soft); color: var(--vp-c-red-1); }
.op-retro {
  margin: 0.45rem 0 0 !important;
  font-size: 0.82rem;
  line-height: 1.5;
  color: var(--vp-c-text-2);
}
.op-retro.is-bon strong { color: var(--vp-c-green-1); }
.op-retro.is-mauvais strong { color: var(--vp-c-red-1); }
.op-corriger { margin-top: 0.5rem; }
.op-label {
  display: block;
  margin-bottom: 0.2rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
.op-zone {
  width: 100%;
  padding: 0.4rem 0.55rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.5rem;
  background: var(--vp-c-bg);
  font: inherit;
  font-size: 0.85rem;
  resize: vertical;
}
.op-zone:focus { outline: none; border-color: var(--vp-c-brand-1); }
.op-lien {
  margin-top: 0.25rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--vp-c-brand-1);
}
.op-modele {
  margin: 0.3rem 0 0 !important;
  padding: 0.45rem 0.65rem;
  border-radius: 0.5rem;
  background: var(--vp-c-green-soft);
  font-size: 0.82rem;
  line-height: 1.5;
}
.op-rappel {
  margin: 0.5rem 0 0.6rem !important;
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
.op-pied {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.875rem;
}
.op-reste { color: var(--vp-c-text-2); }
.op-actions { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.op-action {
  padding: 0.3rem 0.7rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.op-action:hover { border-color: var(--vp-c-brand-1); }
</style>
