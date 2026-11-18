<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from "vue";
import BoutonCopier from "./BoutonCopier.vue";

// Séance 8, activité 1 : l'estimation en trois chiffres d'un site de boulangerie (outils inventés).
// La collègue n'a donné qu'un chiffre (le probable); les étudiants ajoutent l'optimiste et le pessimiste.

type Tache = { cle: string; nom: string; probable: number; reel: number };

const TACHES: Tache[] = [
  { cle: "t1", nom: "Rencontre de départ et plan du site", probable: 3, reel: 4 },
  { cle: "t2", nom: "Maquettes de l'accueil et de la page de commande", probable: 8, reel: 11 },
  { cle: "t3", nom: "Intégration des pages : accueil, menu, à propos, contact", probable: 12, reel: 16 },
  { cle: "t4", nom: "Configuration de l'outil de commande : produits, plages de cueillette", probable: 6, reel: 9 },
  { cle: "t5", nom: "Liaison avec le terminal de paiement", probable: 3, reel: 9 },
  { cle: "t6", nom: "Rappel par texto la veille de la cueillette", probable: 4, reel: 5 },
];

type Oubli = { cle: string; nom: string; oublie: boolean; reel?: number; pourquoi: string };

const OUBLIS: Oubli[] = [
  { cle: "o1", nom: "Gestion de projet : courriels, appels, rencontres de suivi", oublie: true, reel: 9, pourquoi: "Toujours là, jamais dans la liste. Comptez de 10 à 15 % du projet." },
  { cle: "o2", nom: "Écrire les textes et photographier les produits", oublie: false, pourquoi: "C'est la cliente qui les fournit. Ça va dans l'échéancier (avec une date), pas dans les heures du studio." },
  { cle: "o3", nom: "Intégrer les textes et les photos fournis par la cliente", oublie: true, reel: 5, pourquoi: "Le contenu arrive rarement prêt : photos trop lourdes, textes à couper, menus à mettre en forme." },
  { cle: "o4", nom: "Concevoir un nouveau logo", oublie: false, pourquoi: "Personne ne l'a demandé. Ce n'est pas dans le mandat." },
  { cle: "o5", nom: "Tests sur téléphone et corrections", oublie: true, reel: 7, pourquoi: "La plupart des commandes viendront d'un téléphone. Chaque test trouve quelque chose à corriger." },
  { cle: "o6", nom: "Formation de la propriétaire, pour changer le menu seule", oublie: true, reel: 3, pourquoi: "C'est le critère de poids 3 de l'énoncé : sans formation, il n'est pas atteint." },
  { cle: "o7", nom: "Développer une application mobile", oublie: false, pourquoi: "Personne ne l'a demandée, et le site sur téléphone suffit." },
  { cle: "o8", nom: "Mise en ligne : nom de domaine, redirections, vérifications", oublie: true, reel: 4, pourquoi: "Le jour de la mise en ligne n'est jamais gratuit, surtout si l'accès au domaine est chez quelqu'un d'autre." },
];

const props = withDefaults(defineProps<{ storageKey?: string }>(), {
  storageKey: "asm-estimation-trois-chiffres",
});

const saisies = reactive<Record<string, { o: string; pe: string }>>(
  Object.fromEntries(TACHES.map((t) => [t.cle, { o: "", pe: "" }])),
);
const coches = reactive<Record<string, boolean>>(Object.fromEntries(OUBLIS.map((o) => [o.cle, false])));
const revele = ref(false);

const fmtH = (n: number) => n.toLocaleString("fr-CA", { maximumFractionDigits: 1 }) + " h";

function nombre(s: string) {
  const n = parseFloat(String(s).replace(/\s/g, "").replace(",", "."));
  return Number.isFinite(n) && n >= 0 ? n : null;
}

const lignes = computed(() =>
  TACHES.map((t) => {
    const o = nombre(saisies[t.cle].o);
    const pe = nombre(saisies[t.cle].pe);
    const complet = o !== null && pe !== null;
    const retenue = complet ? (o! + 4 * t.probable + pe!) / 6 : null;
    const incoherent = complet && (o! > t.probable || pe! < t.probable);
    const grandEcart = complet && !incoherent && o! > 0 && pe! / o! >= 3;
    return { t, o, pe, retenue, incoherent, grandEcart };
  }),
);

const totalProbable = TACHES.reduce((s, t) => s + t.probable, 0);
const totalReelTaches = TACHES.reduce((s, t) => s + t.reel, 0);
const totalReelOublis = OUBLIS.reduce((s, o) => s + (o.reel ?? 0), 0);
const totalReel = totalReelTaches + totalReelOublis;

const toutesCompletes = computed(() => lignes.value.every((l) => l.retenue !== null));
const totalRetenu = computed(() => lignes.value.reduce((s, l) => s + (l.retenue ?? l.t.probable), 0));

const bonsOublis = computed(() => OUBLIS.filter((o) => o.oublie && coches[o.cle]).length);
const nbOublis = OUBLIS.filter((o) => o.oublie).length;
const fauxOublis = computed(() => OUBLIS.filter((o) => !o.oublie && coches[o.cle]).length);

function texteReponses() {
  const l = [
    "Séance 8 — Activité 1 : l'estimation de la boulangerie",
    "Estimation retenue = (optimiste + 4 × probable + pessimiste) ÷ 6",
    "",
    ...lignes.value.map(
      (x) =>
        `${x.t.nom}\n   optimiste : ${saisies[x.t.cle].o || "—"} · probable : ${x.t.probable} · pessimiste : ${saisies[x.t.cle].pe || "—"} · retenue : ${x.retenue !== null ? fmtH(x.retenue) : "—"}${x.grandEcart ? " (grand écart)" : ""}`,
    ),
    "",
    `Total à un chiffre (la collègue) : ${fmtH(totalProbable)}`,
    `Notre total retenu : ${toutesCompletes.value ? fmtH(totalRetenu.value) : "incomplet"}`,
    "",
    "Les tâches que nous avons cochées comme oubliées :",
    ...OUBLIS.filter((o) => coches[o.cle]).map((o) => `   - ${o.nom}`),
  ];
  if (revele.value) {
    l.push(
      "",
      `Le projet semblable (le fleuriste) : ${fmtH(totalReelTaches)} pour les six tâches, ${fmtH(totalReel)} au total avec les tâches oubliées.`,
      ...OUBLIS.map((o) => `   ${o.oublie ? "Oubliée" : "Pas une tâche du studio"} — ${o.nom} : ${o.pourquoi}`),
    );
  }
  return l.join("\n");
}

function reinitialiser() {
  if (!confirm("Effacer vos réponses ?")) return;
  for (const t of TACHES) Object.assign(saisies[t.cle], { o: "", pe: "" });
  for (const o of OUBLIS) coches[o.cle] = false;
  revele.value = false;
}

onMounted(() => {
  try {
    const data = JSON.parse(localStorage.getItem(props.storageKey) ?? "null");
    if (!data) return;
    for (const t of TACHES) {
      saisies[t.cle].o = String(data.saisies?.[t.cle]?.o ?? "");
      saisies[t.cle].pe = String(data.saisies?.[t.cle]?.pe ?? "");
    }
    for (const o of OUBLIS) coches[o.cle] = data.coches?.[o.cle] === true;
    revele.value = data.revele === true;
  } catch {
    /* stockage indisponible : on part de réponses vides */
  }
});

watch([saisies, coches, revele], () => {
  try {
    localStorage.setItem(props.storageKey, JSON.stringify({ saisies, coches, revele: revele.value }));
  } catch {
    /* stockage indisponible : rien à faire */
  }
});
</script>

<template>
  <section class="et">
    <p class="et-titre"><strong>1. Les six tâches de la collègue</strong> <span>(heures)</span></p>
    <div class="et-table-wrap">
      <table class="et-table">
        <thead>
          <tr>
            <th scope="col">Tâche</th>
            <th scope="col">Optimiste</th>
            <th scope="col">Probable</th>
            <th scope="col">Pessimiste</th>
            <th scope="col">Retenue</th>
            <th v-if="revele" scope="col">Le fleuriste, réel</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="l in lignes" :key="l.t.cle">
            <th scope="row">
              {{ l.t.nom }}
              <span v-if="l.incoherent" class="et-alerte">L'optimiste doit être sous le probable, le pessimiste au-dessus.</span>
              <span v-else-if="l.grandEcart" class="et-ecart">Grand écart : un risque à essayer en premier.</span>
            </th>
            <td><input v-model="saisies[l.t.cle].o" class="et-input" inputmode="decimal" :aria-label="'Optimiste : ' + l.t.nom" /></td>
            <td class="et-fixe">{{ l.t.probable }}</td>
            <td><input v-model="saisies[l.t.cle].pe" class="et-input" inputmode="decimal" :aria-label="'Pessimiste : ' + l.t.nom" /></td>
            <td class="et-retenue">{{ l.retenue !== null ? fmtH(l.retenue) : "—" }}</td>
            <td v-if="revele" class="et-reel">{{ fmtH(l.t.reel) }}</td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <th scope="row">Total</th>
            <td></td>
            <td class="et-fixe">{{ totalProbable }}</td>
            <td></td>
            <td class="et-retenue">{{ toutesCompletes ? fmtH(totalRetenu) : "—" }}</td>
            <td v-if="revele" class="et-reel">{{ fmtH(totalReelTaches) }}</td>
          </tr>
        </tfoot>
      </table>
    </div>
    <p class="et-note">À 75 $ de l'heure, les {{ totalProbable }} heures de la collègue donnent {{ (totalProbable * 75).toLocaleString("fr-CA") }} $.</p>

    <p class="et-titre"><strong>2. Qu'est-ce qui manque à la liste ?</strong> Cochez les tâches que le studio devra faire et qui ne sont pas là.</p>
    <ul class="et-oublis">
      <li v-for="o in OUBLIS" :key="o.cle" :class="revele ? (o.oublie ? 'is-oubli' : 'is-faux') : ''">
        <label>
          <input v-model="coches[o.cle]" type="checkbox" />
          <span>{{ o.nom }}<template v-if="revele && o.reel"> · <strong>{{ o.reel }} h</strong> chez le fleuriste</template></span>
        </label>
        <p v-if="revele" class="et-pourquoi">{{ o.oublie ? "Oubliée." : "Pas une tâche du studio." }} {{ o.pourquoi }}</p>
      </li>
    </ul>

    <div class="et-boutons">
      <button type="button" class="et-action is-principal" @click="revele = true">Comparer avec le projet semblable</button>
    </div>

    <div v-if="revele" class="et-bilan">
      <p><strong>Le projet semblable : le site d'un fleuriste, fait l'an dernier.</strong> Même taille, même genre d'outil de commande.</p>
      <div class="et-barres">
        <div class="et-barre-ligne">
          <span>La collègue (un chiffre)</span>
          <span class="et-piste"><span class="et-seg is-un" :style="{ width: (totalProbable / totalReel) * 100 + '%' }" /></span>
          <span class="et-val">{{ fmtH(totalProbable) }}</span>
        </div>
        <div class="et-barre-ligne">
          <span>Votre estimation retenue</span>
          <span class="et-piste"><span class="et-seg is-vous" :style="{ width: Math.min(100, (totalRetenu / totalReel) * 100) + '%' }" /></span>
          <span class="et-val">{{ toutesCompletes ? fmtH(totalRetenu) : "—" }}</span>
        </div>
        <div class="et-barre-ligne">
          <span>Le fleuriste, réel</span>
          <span class="et-piste">
            <span class="et-seg is-reel" :style="{ width: (totalReelTaches / totalReel) * 100 + '%' }" />
            <span class="et-seg is-oubli" :style="{ width: (totalReelOublis / totalReel) * 100 + '%' }" />
          </span>
          <span class="et-val">{{ fmtH(totalReel) }}</span>
        </div>
      </div>
      <p class="et-legende"><i class="is-reel" />les six mêmes tâches · <i class="is-oubli" />les tâches oubliées</p>
      <p>
        Vous avez trouvé <strong>{{ bonsOublis }} des {{ nbOublis }}</strong> tâches oubliées<template v-if="fauxOublis > 0">, et coché {{ fauxOublis }} tâche{{ fauxOublis > 1 ? "s" : "" }} qui n'est pas au studio</template>.
        Les tâches oubliées représentent {{ totalReelOublis }} heures, soit le tiers du projet réel.
        Et la liaison avec le terminal, estimée à 3 heures, en a pris 9 : la documentation n'était pas à jour.
      </p>
      <p class="et-note">Rien ici ne dit que votre estimation est fausse. Le projet semblable sert à <strong>vérifier</strong> : un écart de cette taille veut dire qu'il manque des tâches, ou qu'un chiffre est trop optimiste.</p>
    </div>

    <p class="et-rappel">Vos réponses restent dans ce navigateur, mais elles peuvent disparaître si la cache est vidée. <strong>Copiez-les dans vos notes</strong> avant de quitter la page.</p>
    <div class="et-pied">
      <BoutonCopier :texte="texteReponses" />
      <button type="button" class="et-action" @click="reinitialiser">Recommencer</button>
    </div>
  </section>
</template>

<style scoped>
.et {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
  font-size: 0.875rem;
}
.et-titre { margin: 0.2rem 0 0.5rem !important; }
.et-titre span { color: var(--vp-c-text-2); font-weight: 400; }
.et-table-wrap { overflow-x: auto; }
.et-table {
  display: table !important;
  width: 100%;
  margin: 0 !important;
  border-collapse: collapse;
  font-size: 0.82rem;
}
.et-table th,
.et-table td {
  padding: 0.35rem 0.5rem !important;
  border: 1px solid var(--vp-c-divider) !important;
  background: var(--vp-c-bg);
  vertical-align: middle;
}
.et-table thead th { font-size: 0.75rem; color: var(--vp-c-text-2); text-align: center; }
.et-table tbody th { font-weight: 500; text-align: left; min-width: 14rem; }
.et-table tfoot th, .et-table tfoot td { font-weight: 700; }
.et-fixe, .et-retenue, .et-reel { text-align: center; font-variant-numeric: tabular-nums; white-space: nowrap; }
.et-retenue { color: var(--vp-c-brand-1); font-weight: 600; }
.et-reel { background: var(--vp-c-bg-soft) !important; }
.et-input {
  width: 4rem;
  padding: 0.25rem 0.4rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.4rem;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font: inherit;
  text-align: center;
}
.et-input:focus { outline: none; border-color: var(--vp-c-brand-1); }
.et-alerte, .et-ecart {
  display: block;
  margin-top: 0.15rem;
  font-size: 0.72rem;
  font-weight: 400;
}
.et-alerte { color: var(--vp-c-red-1); }
.et-ecart { color: var(--vp-c-warning-1); }
.et-note {
  margin: 0.5rem 0 0.9rem !important;
  font-size: 0.8rem;
  color: var(--vp-c-text-2);
}
.et-oublis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 0.4rem;
  margin: 0 !important;
  padding: 0 !important;
  list-style: none;
}
.et-oublis li {
  margin: 0 !important;
  padding: 0.45rem 0.6rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.6rem;
  background: var(--vp-c-bg);
}
.et-oublis li.is-oubli { border-color: var(--vp-c-green-2); }
.et-oublis li.is-faux { opacity: 0.8; }
.et-oublis label { display: flex; gap: 0.5rem; align-items: flex-start; cursor: pointer; line-height: 1.4; }
.et-oublis input { margin-top: 0.2rem; accent-color: var(--vp-c-brand-1); }
.et-pourquoi {
  margin: 0.3rem 0 0 1.5rem !important;
  font-size: 0.78rem;
  line-height: 1.45;
  color: var(--vp-c-text-2);
}
.et-boutons { margin-top: 0.75rem; }
.et-action {
  padding: 0.3rem 0.8rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.et-action:hover { border-color: var(--vp-c-brand-1); }
.et-action.is-principal { border-color: var(--vp-c-brand-1); color: var(--vp-c-brand-1); font-weight: 600; }
.et-bilan {
  margin-top: 0.9rem;
  padding-top: 0.9rem;
  border-top: 1px solid var(--vp-c-divider);
  line-height: 1.55;
}
.et-bilan p { margin: 0.4rem 0 !important; }
.et-barres { display: grid; gap: 0.4rem; margin: 0.6rem 0 0.3rem; }
.et-barre-ligne {
  display: grid;
  grid-template-columns: 11rem 1fr 4.5rem;
  gap: 0.5rem;
  align-items: center;
  font-size: 0.8rem;
}
.et-piste {
  display: flex;
  gap: 2px;
  height: 0.9rem;
  border-radius: 0.25rem;
  background: var(--vp-c-bg);
  overflow: hidden;
}
.et-seg { display: block; height: 100%; transition: width 0.2s; }
.et-seg.is-un { background: var(--vp-c-text-3); }
.et-seg.is-vous { background: var(--vp-c-brand-1); }
.is-reel { background: var(--vp-c-brand-3); }
.is-oubli { background: var(--vp-c-warning-1); }
.et-val { text-align: right; font-variant-numeric: tabular-nums; }
.et-legende { display: flex; flex-wrap: wrap; gap: 0.3rem 0.8rem; align-items: center; font-size: 0.75rem; color: var(--vp-c-text-2); }
.et-legende i { display: inline-block; width: 0.8rem; height: 0.8rem; border-radius: 0.2rem; margin-right: 0.2rem; vertical-align: -0.1rem; }
.et-rappel { margin: 0.75rem 0 0.6rem !important; font-size: 0.78rem; color: var(--vp-c-text-2); }
.et-pied {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
}
@media (max-width: 560px) {
  .et-barre-ligne { grid-template-columns: 1fr auto; }
  .et-piste { grid-column: 1 / -1; grid-row: 2; }
}
</style>
