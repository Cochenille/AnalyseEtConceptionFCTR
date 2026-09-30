<script setup lang="ts">
import { computed, onMounted, reactive, watch } from "vue";

type Site = { id: string; nom: string };
type Paire = { no: number; theme: string; sites: [Site, Site] };
type Saisie = { plateforme: string; score: string | number; constat: string };

const props = withDefaults(defineProps<{ storageKey?: string }>(), {
  storageKey: "retour-lab01",
});

const PAIRES: Paire[] = [
  { no: 1, theme: "Deux poutineries", sites: [{ id: "1a", nom: "La Banquise" }, { id: "1b", nom: "Casse-Croûte Courteau" }] },
  { no: 2, theme: "Deux chaînes", sites: [{ id: "2a", nom: "Thaï Express" }, { id: "2b", nom: "Ashton" }] },
  { no: 3, theme: "Deux restaurants qui vendent leurs produits", sites: [{ id: "3a", nom: "Schwartz's" }, { id: "3b", nom: "Commensal" }] },
  { no: 4, theme: "Deux tables gastronomiques", sites: [{ id: "4a", nom: "Joe Beef" }, { id: "4b", nom: "Épi, buvette de quartier" }] },
];
const SITES = PAIRES.flatMap((p) => p.sites);
const PLATEFORMES = ["WordPress", "Wix", "Squarespace", "Shopify", "Webflow", "Next.js", "Sur mesure", "Inconnue"];

const saisies = reactive<Record<string, Saisie>>(
  Object.fromEntries(SITES.map((s) => [s.id, { plateforme: "", score: "", constat: "" }]))
);
const verdicts = reactive<Record<number, string | null>>(Object.fromEntries(PAIRES.map((p) => [p.no, null])));

function valeur(id: string): number | null {
  // v-model sur un champ numérique donne un nombre, ou "" s'il est vide
  const brut = String(saisies[id].score ?? "").trim();
  if (brut === "") return null;
  const n = Number(brut);
  return Number.isFinite(n) && n >= 0 && n <= 100 ? Math.round(n) : null;
}

function niveau(n: number) {
  if (n >= 90) return "bon";
  if (n >= 50) return "moyen";
  return "faible";
}

const classement = computed(() =>
  SITES.map((s) => ({ ...s, score: valeur(s.id), plateforme: saisies[s.id].plateforme.trim() }))
    .filter((s): s is Site & { score: number; plateforme: string } => s.score !== null)
    .sort((a, b) => b.score - a.score)
);

const constats = computed(() => {
  const c = classement.value;
  if (c.length < 2) return null;
  const premier = c[0];
  const dernier = c[c.length - 1];
  const gagnants = PAIRES.map((p) => {
    const choisi = verdicts[p.no];
    if (!choisi) return null;
    const autre = p.sites.find((s) => s.id !== choisi)!;
    const a = valeur(choisi);
    const b = valeur(autre.id);
    return a !== null && b !== null ? a >= b : null;
  }).filter((v) => v !== null);
  return {
    premier,
    dernier,
    ecart: premier.score - dernier.score,
    verts: c.filter((s) => s.score >= 90).length,
    total: c.length,
    verdictsCompares: gagnants.length,
    verdictsPlusRapides: gagnants.filter(Boolean).length,
  };
});

function choisirVerdict(no: number, id: string) {
  verdicts[no] = verdicts[no] === id ? null : id;
}

function reinitialiser() {
  if (!confirm("Effacer tout le tableau ?")) return;
  for (const s of SITES) Object.assign(saisies[s.id], { plateforme: "", score: "", constat: "" });
  for (const p of PAIRES) verdicts[p.no] = null;
}

onMounted(() => {
  try {
    const brut = localStorage.getItem(props.storageKey);
    if (!brut) return;
    const data = JSON.parse(brut);
    for (const s of SITES) {
      const v = data.saisies?.[s.id];
      if (v) Object.assign(saisies[s.id], { plateforme: String(v.plateforme ?? ""), score: String(v.score ?? ""), constat: String(v.constat ?? "") });
    }
    for (const p of PAIRES) {
      const v = data.verdicts?.[p.no];
      if (p.sites.some((s) => s.id === v)) verdicts[p.no] = v;
    }
  } catch {
    /* stockage indisponible : on part d'un tableau vide */
  }
});

watch([saisies, verdicts], () => {
  try {
    localStorage.setItem(props.storageKey, JSON.stringify({ saisies, verdicts }));
  } catch {
    /* stockage indisponible : rien à faire */
  }
});
</script>

<template>
  <section class="rl">
    <datalist id="rl-plateformes">
      <option v-for="p in PLATEFORMES" :key="p" :value="p" />
    </datalist>

    <div class="rl-entetes" aria-hidden="true">
      <span>Site</span>
      <span>Plateforme</span>
      <span>Perf. mobile</span>
      <span>Un constat marquant</span>
      <span>Plus facile à faire évoluer</span>
    </div>

    <div v-for="p in PAIRES" :key="p.no" class="rl-paire">
      <p class="rl-theme"><strong>Paire {{ p.no }}</strong> · {{ p.theme }}</p>
      <div v-for="s in p.sites" :key="s.id" class="rl-ligne">
        <span class="rl-site">{{ s.nom }}</span>
        <label class="rl-champ">
          <span class="rl-etiquette">Plateforme</span>
          <input v-model="saisies[s.id].plateforme" type="text" list="rl-plateformes" placeholder="p. ex. WordPress" :aria-label="'Plateforme de ' + s.nom" />
        </label>
        <label class="rl-champ rl-champ--score">
          <span class="rl-etiquette">Perf. mobile</span>
          <input
            v-model="saisies[s.id].score"
            type="number"
            min="0"
            max="100"
            inputmode="numeric"
            placeholder="0-100"
            :class="valeur(s.id) !== null ? 'is-' + niveau(valeur(s.id)!) : ''"
            :aria-label="'Score de performance mobile de ' + s.nom"
          />
        </label>
        <label class="rl-champ">
          <span class="rl-etiquette">Un constat marquant</span>
          <input v-model="saisies[s.id].constat" type="text" placeholder="Ce qui a surpris le duo" :aria-label="'Constat marquant pour ' + s.nom" />
        </label>
        <button
          type="button"
          class="rl-verdict"
          :class="{ 'is-choisi': verdicts[p.no] === s.id }"
          :aria-pressed="verdicts[p.no] === s.id"
          @click="choisirVerdict(p.no, s.id)"
        >
          {{ verdicts[p.no] === s.id ? "✓ Celui-ci" : "Celui-ci" }}
        </button>
      </div>
    </div>

    <div class="rl-resultats">
      <p class="rl-titre">Ce que le tableau révèle</p>
      <p v-if="classement.length < 2" class="rl-vide">Entrez au moins deux scores : le classement de la classe apparaîtra ici.</p>
      <template v-else>
        <ol class="rl-barres">
          <li v-for="s in classement" :key="s.id">
            <span class="rl-nom">{{ s.nom }}<small v-if="s.plateforme"> · {{ s.plateforme }}</small></span>
            <span class="rl-piste"><span class="rl-barre" :class="'is-' + niveau(s.score)" :style="{ width: Math.max(s.score, 2) + '%' }"></span></span>
            <span class="rl-score">{{ s.score }}</span>
          </li>
        </ol>
        <ul v-if="constats" class="rl-constats">
          <li>
            <strong>{{ constats.ecart }} points</strong> séparent {{ constats.premier.nom }} ({{ constats.premier.score }}) et {{ constats.dernier.nom }} ({{ constats.dernier.score }}).
          </li>
          <li>
            <strong>{{ constats.verts }} site{{ constats.verts > 1 ? "s" : "" }} sur {{ constats.total }}</strong>
            {{ constats.verts > 1 ? "atteignent" : "atteint" }} la zone verte (90 et plus).
          </li>
          <li v-if="constats.verdictsCompares > 0">
            Dans <strong>{{ constats.verdictsPlusRapides }} paire{{ constats.verdictsPlusRapides > 1 ? "s" : "" }} sur {{ constats.verdictsCompares }}</strong>,
            le site jugé le plus facile à faire évoluer est aussi le plus rapide.
          </li>
        </ul>
      </template>
    </div>

    <div class="rl-pied">
      <span>Le tableau est conservé dans ce navigateur.</span>
      <button type="button" class="rl-reset" @click="reinitialiser">Tout effacer</button>
    </div>
  </section>
</template>

<style scoped>
.rl {
  --rl-cols: minmax(8rem, 1.1fr) minmax(7rem, 1fr) 5.5rem minmax(9rem, 1.6fr) 6.5rem;
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.rl-entetes,
.rl-ligne {
  display: grid;
  grid-template-columns: var(--rl-cols);
  gap: 0.4rem;
  align-items: center;
}
.rl-entetes {
  padding: 0 0.6rem 0.3rem;
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--vp-c-text-2);
}
.rl-paire {
  margin-top: 0.5rem;
  padding: 0.5rem 0.6rem 0.6rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.7rem;
  background: var(--vp-c-bg);
}
.rl-theme {
  margin: 0 0 0.35rem !important;
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
.rl-ligne + .rl-ligne {
  margin-top: 0.35rem;
}
.rl-site {
  font-size: 0.9rem;
  font-weight: 600;
  line-height: 1.3;
}
.rl-champ {
  display: block;
  min-width: 0;
}
.rl-etiquette {
  display: none;
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
.rl input {
  width: 100%;
  padding: 0.3rem 0.5rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.45rem;
  background: var(--vp-c-bg-soft);
  font-size: 0.85rem;
  color: var(--vp-c-text-1);
}
.rl input:focus-visible {
  outline: 2px solid var(--vp-c-brand-1);
  outline-offset: 1px;
}
.rl-champ--score input {
  font-weight: 700;
  text-align: center;
}
.rl input.is-bon {
  border-color: var(--vp-c-green-2);
  background: var(--vp-c-green-soft);
}
.rl input.is-moyen {
  border-color: var(--vp-c-yellow-2);
  background: var(--vp-c-yellow-soft);
}
.rl input.is-faible {
  border-color: var(--vp-c-red-2);
  background: var(--vp-c-red-soft);
}
.rl-verdict {
  padding: 0.3rem 0.4rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  background: var(--vp-c-bg-soft);
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
.rl-verdict:hover {
  border-color: var(--vp-c-brand-1);
}
.rl-verdict.is-choisi {
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
}
.rl-resultats {
  margin-top: 0.9rem;
  padding: 0.75rem 0.9rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.7rem;
  background: var(--vp-c-bg);
}
.rl-titre {
  margin: 0 0 0.5rem !important;
  font-size: 0.9rem;
  font-weight: 700;
}
.rl-vide {
  margin: 0 !important;
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
}
.rl-barres {
  list-style: none !important;
  margin: 0 !important;
  padding: 0 !important;
  display: grid;
  gap: 0.3rem;
}
.rl-barres li {
  display: grid;
  grid-template-columns: minmax(7rem, 14rem) 1fr 2.2rem;
  gap: 0.5rem;
  align-items: center;
  margin: 0 !important;
  font-size: 0.82rem;
}
.rl-nom {
  line-height: 1.3;
}
.rl-nom small {
  color: var(--vp-c-text-2);
}
.rl-piste {
  height: 0.9rem;
  border-radius: 999px;
  background: var(--vp-c-default-soft);
  overflow: hidden;
}
.rl-barre {
  display: block;
  height: 100%;
  border-radius: 999px;
  transition: width 0.3s;
}
.rl-barre.is-bon {
  background: var(--vp-c-green-2);
}
.rl-barre.is-moyen {
  background: var(--vp-c-yellow-2);
}
.rl-barre.is-faible {
  background: var(--vp-c-red-2);
}
.rl-score {
  font-weight: 700;
  text-align: right;
  font-variant-numeric: tabular-nums;
}
.rl-constats {
  margin: 0.7rem 0 0 !important;
  padding-left: 1.1rem !important;
  font-size: 0.85rem;
  line-height: 1.5;
}
.rl-constats li {
  margin: 0.15rem 0 !important;
}
.rl-pied {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
.rl-reset {
  padding: 0.3rem 0.7rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
  color: var(--vp-c-text-1);
}
.rl-reset:hover {
  border-color: var(--vp-c-brand-1);
}
@media (max-width: 760px) {
  .rl-entetes {
    display: none;
  }
  .rl-ligne {
    grid-template-columns: 1fr 5.5rem;
    padding-top: 0.4rem;
  }
  .rl-ligne + .rl-ligne {
    margin-top: 0.6rem;
    border-top: 1px dashed var(--vp-c-divider);
  }
  .rl-site {
    grid-column: 1 / -1;
  }
  .rl-etiquette {
    display: block;
  }
  .rl-ligne > .rl-champ:nth-of-type(3) {
    grid-column: 1 / -1;
  }
  .rl-verdict {
    grid-column: 1 / -1;
    justify-self: start;
    padding-inline: 0.8rem;
  }
  .rl-verdict::before {
    content: "Plus facile à faire évoluer : ";
    font-weight: 500;
  }
  .rl-barres li {
    grid-template-columns: minmax(5.5rem, 8rem) 1fr 2rem;
  }
}
</style>
