<script setup lang="ts">
import { computed, reactive, ref } from "vue";

type Categorie = "fiable" | "verifier" | "pub";
type Source = {
  titre: string;
  ou: string;
  date: string;
  apercu: string;
  reponse: Categorie;
  pourquoi: string;
};

const CATEGORIES: { cle: Categorie; titre: string; aide: string }[] = [
  { cle: "fiable", titre: "Fiable", aide: "Peut appuyer une affirmation dans le rapport" },
  { cle: "verifier", titre: "À vérifier", aide: "Utile, mais à confirmer ailleurs ou par un essai" },
  { cle: "pub", titre: "Publicitaire", aide: "Écrite pour vendre : donne des noms, pas des preuves" },
];

const SOURCES: Source[] = [
  {
    titre: "Formats de fichiers image et types",
    ou: "MDN Web Docs (developer.mozilla.org), Mozilla et sa communauté",
    date: "Mise à jour il y a 3 semaines",
    apercu: "Tableau des formats (JPEG, PNG, WebP, AVIF, SVG), de leur prise en charge par les navigateurs et de leurs usages recommandés. Liens vers les spécifications.",
    reponse: "fiable",
    pourquoi: "Documentation de référence, maintenue, datée et sans produit à vendre. Elle cite les spécifications.",
  },
  {
    titre: "Les 7 meilleurs logiciels de réservation pour activités de plein air en 2026",
    ou: "Blogue d'un éditeur de logiciel de réservation",
    date: "Janvier 2026",
    apercu: "Le logiciel de l'éditeur arrive premier, « le seul qui offre tout ». Un bouton « Commencer l'essai gratuit » après chaque section. Les six autres outils ont chacun un paragraphe et un défaut.",
    reponse: "pub",
    pourquoi: "L'auteur est l'un des outils comparés, et il se classe premier. C'est une page de vente déguisée en comparatif. Elle donne au mieux des noms de concurrents à explorer.",
  },
  {
    titre: "Loi 25 : les nouvelles obligations des entreprises",
    ou: "Commission d'accès à l'information du Québec (cai.gouv.qc.ca)",
    date: "Révisée en 2025",
    apercu: "Liste des obligations (personne responsable, politique de confidentialité, consentement, incidents), avec des guides et des modèles pour les PME.",
    reponse: "fiable",
    pourquoi: "C'est l'organisme public chargé d'appliquer la loi. Pour connaître une obligation légale, c'est la source à citer.",
  },
  {
    titre: "Wix ou WordPress ? Notre verdict après 5 ans de tests",
    ou: "comparatif-outils-web.example — auteur : « L'équipe »",
    date: "Non datée",
    apercu: "Tableau de notes sur 10, verdict clair pour un des deux. Les liens « Voir l'offre » se terminent par ?ref=cow2026. En bas de page : « Nous pouvons recevoir une commission sur les achats effectués via nos liens. »",
    reponse: "pub",
    pourquoi: "Liens d'affiliation, avis de commission, auteur anonyme, aucune date et aucun essai décrit. L'auteur gagne de l'argent selon l'outil que vous choisissez.",
  },
  {
    titre: "« Quelqu'un utilise un logiciel de réservation pour une entreprise de kayak ? »",
    ou: "Fil de discussion sur Reddit, 42 réponses",
    date: "Il y a 3 ans",
    apercu: "Des propriétaires d'entreprises de plein air racontent leur expérience. Deux se plaignent de la synchronisation avec les plateformes touristiques. Un répondant travaille pour un des outils mentionnés.",
    reponse: "verifier",
    pourquoi: "De vrais témoignages, précieux pour découvrir des problèmes que le vendeur ne mentionne pas. Mais ils sont anecdotiques, vieux de trois ans, et pas tous neutres. À confirmer par un essai.",
  },
  {
    titre: "J'ai testé 5 constructeurs de sites pour vous !",
    ou: "Vidéo YouTube, 410 000 vues",
    date: "Il y a 4 mois",
    apercu: "À 0:45 : « Cette vidéo est commanditée par [un des cinq outils]. » Le lien dans la description donne 20 % de rabais. L'outil commanditaire gagne le comparatif.",
    reponse: "pub",
    pourquoi: "Commandite déclarée, lien promotionnel, et le commanditaire gagne. Même si les démonstrations sont réelles, la conclusion n'est pas indépendante.",
  },
  {
    titre: "Réponse d'un assistant d'IA à « Combien coûte un logiciel de réservation ? »",
    ou: "Assistant conversationnel, sans source citée",
    date: "Ce soir",
    apercu: "« Un logiciel comme X coûte environ 49 $ par mois et se synchronise avec Viator. » Le ton est sûr. Aucun lien vers la page de prix.",
    reponse: "verifier",
    pourquoi: "Un bon point de départ pour trouver des noms et du vocabulaire, mais l'IA peut se tromper ou s'appuyer sur des prix périmés. Toujours vérifier sur la page de prix officielle, et ne jamais la citer comme source.",
  },
  {
    titre: "AVIF image format — Browser support tables",
    ou: "Can I use (caniuse.com)",
    date: "Données mises à jour chaque semaine",
    apercu: "Pour chaque navigateur et chaque version, indique si le format est supporté. Pourcentage d'utilisateurs couverts. Notes et liens vers les sources.",
    reponse: "fiable",
    pourquoi: "Données de compatibilité mises à jour en continu, avec leurs sources. C'est la référence pour savoir si une technologie fonctionne sur les navigateurs à supporter.",
  },
  {
    titre: "Les PME québécoises mal préparées à la Loi 25",
    ou: "Article d'un grand média québécois, section Économie",
    date: "Septembre 2022",
    apercu: "Entrevues avec des propriétaires et un avocat. Explique les obligations « qui entreront en vigueur au cours des prochaines années ».",
    reponse: "verifier",
    pourquoi: "Source sérieuse, mais datée : en 2022, la loi s'appliquait par étapes, jusqu'en 2024. Bonne pour comprendre le contexte; pour les obligations actuelles, il faut vérifier auprès de la CAI.",
  },
  {
    titre: "Introduction à l'accessibilité du Web",
    ou: "W3C — Web Accessibility Initiative (w3.org/WAI)",
    date: "Mise à jour en 2024",
    apercu: "Explique ce qu'est l'accessibilité, qui est concerné et comment les WCAG s'appliquent. Disponible en français.",
    reponse: "fiable",
    pourquoi: "Le W3C est l'organisme qui publie les normes du Web, dont les WCAG. C'est la source à citer pour l'accessibilité.",
  },
];

const choix = reactive<(Categorie | null)[]>(SOURCES.map(() => null));
const justifs = reactive<string[]>(SOURCES.map(() => ""));
const copie = ref(false);

const score = computed(() => choix.filter((c, n) => c === SOURCES[n].reponse).length);
const repondues = computed(() => choix.filter((c) => c !== null).length);

function nomCategorie(c: Categorie | null) {
  return CATEGORIES.find((x) => x.cle === c)?.titre ?? "—";
}

function texteReponses() {
  return SOURCES.map((s, n) =>
    [
      `${n + 1}. ${s.titre} (${s.ou})`,
      `   Notre classement : ${nomCategorie(choix[n])}`,
      `   Notre justification : ${justifs[n].trim() || "—"}`,
    ].join("\n"),
  ).join("\n\n");
}

async function copier() {
  try {
    await navigator.clipboard.writeText(texteReponses());
    copie.value = true;
    setTimeout(() => (copie.value = false), 2000);
  } catch {
    copie.value = false;
  }
}

function reinitialiser() {
  choix.fill(null);
  justifs.fill("");
}
</script>

<template>
  <section class="ts">
    <div class="ts-cats">
      <div v-for="c in CATEGORIES" :key="c.cle" class="ts-cat" :class="'is-' + c.cle">
        <strong>{{ c.titre }}</strong>
        <span>{{ c.aide }}</span>
      </div>
    </div>

    <ol class="ts-liste">
      <li v-for="(s, n) in SOURCES" :key="n" class="ts-item">
        <div class="ts-fiche">
          <p class="ts-titre">{{ s.titre }}</p>
          <p class="ts-meta">{{ s.ou }} · {{ s.date }}</p>
          <p class="ts-apercu">{{ s.apercu }}</p>
        </div>

        <label class="ts-label" :for="'ts-j-' + n">Notre justification (l'indice qui nous a fait trancher)</label>
        <textarea :id="'ts-j-' + n" v-model="justifs[n]" class="ts-justif" rows="2" />

        <div class="ts-boutons" role="group" :aria-label="'Classement de la source ' + (n + 1)">
          <button
            v-for="c in CATEGORIES"
            :key="c.cle"
            type="button"
            class="ts-btn"
            :class="{
              'is-bon': choix[n] !== null && c.cle === s.reponse,
              'is-mauvais': choix[n] === c.cle && c.cle !== s.reponse,
            }"
            :aria-pressed="choix[n] === c.cle"
            @click="choix[n] = c.cle"
          >
            {{ c.titre }}
          </button>
        </div>
        <p v-if="choix[n] !== null" class="ts-retro" :class="choix[n] === s.reponse ? 'is-bon' : 'is-mauvais'">
          <strong>{{ choix[n] === s.reponse ? "Oui." : "Plutôt « " + nomCategorie(s.reponse) + " »." }}</strong>
          {{ s.pourquoi }}
        </p>
      </li>
    </ol>

    <div class="ts-pied">
      <span>
        <strong>{{ score }} / {{ SOURCES.length }}</strong> classements attendus
        <span v-if="repondues < SOURCES.length" class="ts-reste">({{ SOURCES.length - repondues }} à faire)</span>
      </span>
      <span class="ts-actions">
        <button type="button" class="ts-action is-principal" @click="copier">{{ copie ? "Copié ✓" : "Copier nos réponses" }}</button>
        <button type="button" class="ts-action" @click="reinitialiser">Recommencer</button>
      </span>
    </div>
  </section>
</template>

<style scoped>
.ts {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.ts-cats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}
.ts-cat {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  padding: 0.6rem 0.75rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  border-left-width: 4px;
  background: var(--vp-c-bg);
  font-size: 0.8rem;
  line-height: 1.4;
}
.ts-cat.is-fiable { border-left-color: var(--vp-c-green-2); }
.ts-cat.is-verifier { border-left-color: var(--vp-c-yellow-2); }
.ts-cat.is-pub { border-left-color: var(--vp-c-red-2); }
.ts-cat strong { font-size: 0.875rem; }
.ts-cat span { color: var(--vp-c-text-2); }
.ts-liste {
  margin: 0 !important;
  padding-left: 1.25rem !important;
}
.ts-item {
  margin: 0 !important;
  padding: 0.8rem 0;
  border-top: 1px solid var(--vp-c-divider);
}
.ts-fiche {
  padding: 0.65rem 0.8rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.6rem;
  background: var(--vp-c-bg);
}
.ts-titre {
  margin: 0 !important;
  font-weight: 600;
  font-size: 0.92rem;
  line-height: 1.4;
}
.ts-meta {
  margin: 0.15rem 0 0.35rem !important;
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
.ts-apercu {
  margin: 0 !important;
  font-size: 0.85rem;
  line-height: 1.5;
}
.ts-label {
  display: block;
  margin: 0.55rem 0 0.2rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
.ts-justif {
  width: 100%;
  padding: 0.4rem 0.55rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.5rem;
  background: var(--vp-c-bg);
  font: inherit;
  font-size: 0.85rem;
  resize: vertical;
}
.ts-justif:focus {
  outline: none;
  border-color: var(--vp-c-brand-1);
}
.ts-boutons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin-top: 0.45rem;
}
.ts-btn {
  padding: 0.25rem 0.7rem;
  border-radius: 999px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
  font-weight: 500;
  transition: border-color 0.15s, background-color 0.15s;
}
.ts-btn:hover { border-color: var(--vp-c-brand-1); }
.ts-btn.is-bon {
  border-color: var(--vp-c-green-2);
  background: var(--vp-c-green-soft);
  color: var(--vp-c-green-1);
}
.ts-btn.is-mauvais {
  border-color: var(--vp-c-red-2);
  background: var(--vp-c-red-soft);
  color: var(--vp-c-red-1);
}
.ts-retro {
  margin: 0.4rem 0 0 !important;
  font-size: 0.8rem;
  line-height: 1.5;
  color: var(--vp-c-text-2);
}
.ts-retro.is-bon strong { color: var(--vp-c-green-1); }
.ts-retro.is-mauvais strong { color: var(--vp-c-red-1); }
.ts-pied {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.875rem;
}
.ts-reste { color: var(--vp-c-text-2); }
.ts-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}
.ts-action {
  padding: 0.3rem 0.7rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.ts-action:hover { border-color: var(--vp-c-brand-1); }
.ts-action.is-principal {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
  font-weight: 600;
}
</style>
