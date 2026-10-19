<script setup lang="ts">
import { computed, onMounted, reactive, watch } from "vue";
import BoutonCopier from "./BoutonCopier.vue";

type Sorte = "constat" | "nonappuye" | "reco";
type Phrase = { texte: string; reponse: Sorte; pourquoi: string; reecriture?: string };

const SORTES: { cle: Sorte; titre: string; aide: string }[] = [
  { cle: "constat", titre: "Constat appuyé", aide: "Appuyé sur le mandat, une source datée ou un essai. Il a sa place dans le rapport." },
  { cle: "nonappuye", titre: "Affirmation non appuyée", aide: "Un jugement vague ou une affirmation sans preuve. À réécrire avec une mesure ou une source." },
  { cle: "reco", titre: "Recommandation", aide: "Elle choisit à la place du client. Interdite dans l'évaluation 1 : elle ira dans l'évaluation 2." },
];

const PHRASES: Phrase[] = [
  {
    texte: "Lors de notre essai du 21 octobre, la réservation de 5 places sur téléphone a pris 2 min 40 s avec Réservio, sans aide (essai E2, annexe A).",
    reponse: "constat",
    pourquoi: "Une date, une mesure, un renvoi à l'essai. N'importe qui peut vérifier d'où vient l'information.",
  },
  {
    texte: "PagayePro est très facile à utiliser.",
    reponse: "nonappuye",
    pourquoi: "« Facile » pour qui, et mesuré comment ? Mélanie n'est pas l'équipe Web. Remplacez l'adjectif par ce que vous avez observé.",
    reecriture: "Le membre de l'équipe qui jouait Mélanie, sans avoir vu l'outil, a créé un départ de via ferrata en 6 minutes, sans ouvrir l'aide (essai E4).",
  },
  {
    texte: "Nous recommandons Wix, puisque le client l'utilise déjà.",
    reponse: "reco",
    pourquoi: "« Nous recommandons » : le mot est dans la phrase. Le fait derrière (le client utilise déjà Wix) est utile, mais il faut le décrire, avec ses avantages et ses limites.",
    reecriture: "Le client utilise déjà Wix. Le conserver éviterait de refaire le site sur une autre plateforme, mais le compte est au nom d'une personne qui ne travaille pas pour l'entreprise (mandat, notes de la rencontre).",
  },
  {
    texte: "Selon sa page de prix consultée le 20 octobre 2026, Quaistart coûte 45 $ CA par utilisateur, par mois, avec un engagement de 12 mois.",
    reponse: "constat",
    pourquoi: "La source est nommée et datée. On rapporte ce que le vendeur affiche, sans dire que c'est un bon prix.",
  },
  {
    texte: "Le meilleur choix pour les vidéos serait clairement une plateforme payante.",
    reponse: "reco",
    pourquoi: "« Le meilleur choix » tranche à la place du client. Décrivez plutôt la différence que vous avez observée entre les plateformes.",
    reecriture: "Les deux plateformes payantes essayées n'affichent ni publicité ni suggestion de vidéos à la fin de la lecture; la plateforme gratuite affiche des vidéos d'autres chaînes (essai E5, captures en annexe A).",
  },
  {
    texte: "Réservio est l'outil le plus rapide.",
    reponse: "nonappuye",
    pourquoi: "Le plus rapide pour faire quoi, et mesuré comment ? Sans la mesure, le lecteur doit vous croire sur parole. Donnez les temps, et l'essai d'où ils viennent.",
    reecriture: "Sur téléphone, la réservation de 5 places a pris 2 min 40 s avec Réservio, contre 4 min 10 s avec PagayePro (essai E2, annexe A).",
  },
  {
    texte: "En mode avion, la liste des participants du jour ne s'est pas affichée dans l'application de Signéo (essai E3, capture Q2-Signeo-E3-01).",
    reponse: "constat",
    pourquoi: "Un échec est un constat aussi solide qu'un succès, à condition d'être documenté. C'est même souvent l'information la plus utile pour le client.",
  },
  {
    texte: "Il faudrait que Mélanie suive une formation avant d'utiliser Réservio.",
    reponse: "reco",
    pourquoi: "« Il faudrait » est une recommandation déguisée, comme « devrait », « idéalement » ou « à privilégier ». Le fait observé derrière est intéressant : écrivez-le.",
    reecriture: "Les tutoriels de Réservio sont en anglais seulement. Le membre qui jouait Mélanie a dû les consulter deux fois pour modifier un tarif, ce qui lui a pris 9 minutes (essai E4).",
  },
  {
    texte: "La synchronisation avec Viator n'a pas pu être vérifiée : la version d'essai de PagayePro ne permet pas de connecter une plateforme de distribution.",
    reponse: "constat",
    pourquoi: "« Non vérifiable », avec la raison. C'est honnête, et ça devient un point à vérifier dans la section 7 du rapport.",
  },
  {
    texte: "Tout le monde s'entend pour dire que Quaistart est l'outil le plus complet du marché.",
    reponse: "nonappuye",
    pourquoi: "« Tout le monde » n'est pas une source, et « le plus complet du marché » ne se mesure pas. Ramenez la phrase aux besoins du client.",
    reecriture: "Quaistart couvre 5 des 7 besoins essentiels de notre plan d'essai; la synchronisation avec Viator est annoncée comme « bientôt disponible » sur sa page des fonctions (consultée le 20 octobre 2026).",
  },
  {
    texte: "Quaistart est le moins cher; c'est donc la solution à privilégier pour une petite entreprise.",
    reponse: "reco",
    pourquoi: "La première moitié est un constat (si le calcul est montré). « À privilégier » est une recommandation, et elle ignore un besoin essentiel.",
    reecriture: "Sur trois ans, Quaistart coûterait environ 6 480 $, contre 14 379 $ pour PagayePro (hypothèses en annexe), mais il ne se synchronise pas avec Viator.",
  },
];

const props = withDefaults(defineProps<{ storageKey?: string }>(), {
  storageKey: "asm-constat-ou-reco",
});

const etat = reactive(PHRASES.map(() => ({ choix: null as Sorte | null, reecriture: "", voir: false })));

const score = computed(() => etat.filter((e, n) => e.choix === PHRASES[n].reponse).length);
const repondues = computed(() => etat.filter((e) => e.choix !== null).length);

const nom = (s: Sorte | null) => SORTES.find((x) => x.cle === s)?.titre ?? "—";

function texteReponses() {
  return [
    "Séance 4 — Activité 1 : constat, affirmation non appuyée ou recommandation ?",
    "",
    ...PHRASES.map((p, n) => {
      const e = etat[n];
      const lignes = [`${n + 1}. « ${p.texte} »`, `   Notre classement : ${nom(e.choix)} (attendu : ${nom(p.reponse)})`];
      if (p.reponse !== "constat") {
        lignes.push(`   Notre réécriture : ${e.reecriture.trim() || "—"}`);
        lignes.push(`   Réécriture possible : ${p.reecriture}`);
      }
      return lignes.join("\n");
    }),
  ].join("\n\n");
}

function reinitialiser() {
  if (!confirm("Effacer toutes vos réponses ?")) return;
  for (const e of etat) Object.assign(e, { choix: null, reecriture: "", voir: false });
}

onMounted(() => {
  try {
    const data = JSON.parse(localStorage.getItem(props.storageKey) ?? "null");
    if (!Array.isArray(data)) return;
    etat.forEach((e, n) => {
      const v = data[n];
      if (!v) return;
      e.choix = SORTES.some((s) => s.cle === v.choix) ? v.choix : null;
      e.reecriture = String(v.reecriture ?? "");
    });
  } catch {
    /* stockage indisponible : on part de réponses vides */
  }
});

watch(etat, () => {
  try {
    localStorage.setItem(props.storageKey, JSON.stringify(etat.map(({ choix, reecriture }) => ({ choix, reecriture }))));
  } catch {
    /* stockage indisponible : rien à faire */
  }
});
</script>

<template>
  <section class="cr">
    <div class="cr-sortes">
      <div v-for="s in SORTES" :key="s.cle" class="cr-sorte" :class="'is-' + s.cle">
        <strong>{{ s.titre }}</strong>
        <span>{{ s.aide }}</span>
      </div>
    </div>

    <ol class="cr-liste">
      <li v-for="(p, n) in PHRASES" :key="n" class="cr-item">
        <blockquote class="cr-phrase">« {{ p.texte }} »</blockquote>
        <div class="cr-boutons" role="group" :aria-label="'Classement de la phrase ' + (n + 1)">
          <button
            v-for="s in SORTES"
            :key="s.cle"
            type="button"
            class="cr-btn"
            :class="{
              'is-bon': etat[n].choix !== null && s.cle === p.reponse,
              'is-mauvais': etat[n].choix === s.cle && s.cle !== p.reponse,
            }"
            :aria-pressed="etat[n].choix === s.cle"
            @click="etat[n].choix = s.cle"
          >
            {{ s.titre }}
          </button>
        </div>

        <template v-if="etat[n].choix !== null">
          <p class="cr-retro" :class="etat[n].choix === p.reponse ? 'is-bon' : 'is-mauvais'">
            <strong>{{ etat[n].choix === p.reponse ? "Oui." : "Plutôt : " + nom(p.reponse) + "." }}</strong>
            {{ p.pourquoi }}
          </p>
          <div v-if="p.reecriture" class="cr-reecrire">
            <label class="cr-label" :for="'cr-r-' + n">Notre réécriture, en constat appuyé (inventez la mesure ou la source au besoin)</label>
            <textarea :id="'cr-r-' + n" v-model="etat[n].reecriture" class="cr-zone" rows="2" />
            <button type="button" class="cr-voir" :aria-expanded="etat[n].voir" @click="etat[n].voir = !etat[n].voir">
              {{ etat[n].voir ? "Cacher" : "Voir une réécriture possible" }}
            </button>
            <p v-if="etat[n].voir" class="cr-modele">{{ p.reecriture }}</p>
          </div>
        </template>
      </li>
    </ol>

    <p class="cr-rappel">Vos réponses restent dans ce navigateur, mais elles peuvent disparaître si la cache est vidée. <strong>Copiez-les dans vos notes</strong> avant de quitter la page.</p>
    <div class="cr-pied">
      <span>
        <strong>{{ score }} / {{ PHRASES.length }}</strong> classements attendus
        <span v-if="repondues < PHRASES.length" class="cr-reste">({{ PHRASES.length - repondues }} à faire)</span>
      </span>
      <span class="cr-actions">
        <BoutonCopier :texte="texteReponses" />
        <button type="button" class="cr-action" @click="reinitialiser">Recommencer</button>
      </span>
    </div>
  </section>
</template>

<style scoped>
.cr {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.cr-sortes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}
.cr-sorte {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  padding: 0.6rem 0.75rem;
  border: 1px solid var(--vp-c-divider);
  border-left-width: 4px;
  border-radius: 0.65rem;
  background: var(--vp-c-bg);
  font-size: 0.8rem;
  line-height: 1.4;
}
.cr-sorte.is-constat { border-left-color: var(--vp-c-green-2); }
.cr-sorte.is-nonappuye { border-left-color: var(--vp-c-yellow-2); }
.cr-sorte.is-reco { border-left-color: var(--vp-c-red-2); }
.cr-sorte strong { font-size: 0.875rem; }
.cr-sorte span { color: var(--vp-c-text-2); }
.cr-liste {
  margin: 0 !important;
  padding-left: 1.25rem !important;
}
.cr-item {
  margin: 0 !important;
  padding: 0.8rem 0;
  border-top: 1px solid var(--vp-c-divider);
}
.cr-phrase {
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
.cr-boutons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin-top: 0.5rem;
}
.cr-btn {
  padding: 0.25rem 0.7rem;
  border-radius: 999px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
  font-weight: 500;
  transition: border-color 0.15s, background-color 0.15s;
}
.cr-btn:hover { border-color: var(--vp-c-brand-1); }
.cr-btn.is-bon { border-color: var(--vp-c-green-2); background: var(--vp-c-green-soft); color: var(--vp-c-green-1); }
.cr-btn.is-mauvais { border-color: var(--vp-c-red-2); background: var(--vp-c-red-soft); color: var(--vp-c-red-1); }
.cr-retro {
  margin: 0.45rem 0 0 !important;
  font-size: 0.82rem;
  line-height: 1.5;
  color: var(--vp-c-text-2);
}
.cr-retro.is-bon strong { color: var(--vp-c-green-1); }
.cr-retro.is-mauvais strong { color: var(--vp-c-red-1); }
.cr-reecrire { margin-top: 0.5rem; }
.cr-label {
  display: block;
  margin-bottom: 0.2rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
.cr-zone {
  width: 100%;
  padding: 0.4rem 0.55rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.5rem;
  background: var(--vp-c-bg);
  font: inherit;
  font-size: 0.85rem;
  resize: vertical;
}
.cr-zone:focus { outline: none; border-color: var(--vp-c-brand-1); }
.cr-voir {
  margin-top: 0.25rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--vp-c-brand-1);
}
.cr-modele {
  margin: 0.3rem 0 0 !important;
  padding: 0.45rem 0.65rem;
  border-radius: 0.5rem;
  background: var(--vp-c-green-soft);
  font-size: 0.82rem;
  line-height: 1.5;
}
.cr-rappel {
  margin: 0.5rem 0 0.6rem !important;
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
.cr-pied {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.875rem;
}
.cr-reste { color: var(--vp-c-text-2); }
.cr-actions { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.cr-action {
  padding: 0.3rem 0.7rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.cr-action:hover { border-color: var(--vp-c-brand-1); }
</style>
