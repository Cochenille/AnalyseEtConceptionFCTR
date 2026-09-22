<script setup lang="ts">
import { computed, reactive } from "vue";

type Etat = { cle: "bon" | "moyen" | "faible"; libelle: string; icone: string };

const ETATS: Record<Etat["cle"], Etat> = {
  bon: { cle: "bon", libelle: "Bon", icone: "●" },
  moyen: { cle: "moyen", libelle: "À améliorer", icone: "■" },
  faible: { cle: "faible", libelle: "Faible", icone: "▲" },
};

// Seuils utilisés par PageSpeed Insights / Lighthouse
const etatScore = (s: number): Etat => (s >= 90 ? ETATS.bon : s >= 50 ? ETATS.moyen : ETATS.faible);
const etatLcp = (l: number): Etat => (l <= 2.5 ? ETATS.bon : l <= 4 ? ETATS.moyen : ETATS.faible);

const sites = reactive([
  { nom: "Site A", score: null as number | string | null, lcp: null as number | string | null },
  { nom: "Site B", score: null as number | string | null, lcp: null as number | string | null },
]);

// Jauge circulaire
const R = 42;
const C = 2 * Math.PI * R;
const arc = (score: number | string | null) => {
  const v = typeof score === "number" ? Math.max(0, Math.min(100, score)) : 0;
  return `${(v / 100) * C} ${C}`;
};

// Échelle LCP : 0 à 8 s
const LCP_MAX = 8;
const posLcp = (l: number) => Math.min(100, (l / LCP_MAX) * 100);

const comparaison = computed(() => {
  const [a, b] = sites;
  if (typeof a.score !== "number" || typeof b.score !== "number") return "";
  if (a.score === b.score) return "Les deux sites ont le même score mobile.";
  const meilleur = a.score > b.score ? a : b;
  return `${meilleur.nom} est plus rapide sur mobile, de ${Math.abs(a.score - b.score)} points.`;
});
</script>

<template>
  <section class="jp">
    <p class="jp-intro">
      Entrez les résultats <strong>mobiles</strong> de vos deux sites pour les situer sur l'échelle de PageSpeed Insights.
    </p>

    <div class="jp-grille">
      <div v-for="site in sites" :key="site.nom" class="jp-site">
        <h4 class="jp-nom">{{ site.nom }}</h4>

        <div class="jp-jauge-zone">
          <svg viewBox="0 0 100 100" class="jp-jauge" :class="typeof site.score === 'number' ? 'is-' + etatScore(site.score).cle : ''">
            <circle cx="50" cy="50" :r="R" class="jp-fond" />
            <circle
              cx="50"
              cy="50"
              :r="R"
              class="jp-arc"
              :stroke-dasharray="arc(site.score)"
              transform="rotate(-90 50 50)"
            />
            <text x="50" y="57" text-anchor="middle" class="jp-valeur">{{ typeof site.score === 'number' ? site.score : "–" }}</text>
          </svg>
          <label class="jp-champ">
            <span>Score de performance</span>
            <input v-model.number="site.score" type="number" min="0" max="100" placeholder="0 à 100" />
            <span v-if="typeof site.score === 'number'" class="jp-etat" :class="'is-' + etatScore(site.score).cle">
              {{ etatScore(site.score).icone }} {{ etatScore(site.score).libelle }}
            </span>
          </label>
        </div>

        <label class="jp-champ">
          <span>Largest Contentful Paint (secondes)</span>
          <input v-model.number="site.lcp" type="number" min="0" step="0.1" placeholder="p. ex. 3,2" />
        </label>
        <div class="jp-lcp" aria-hidden="true">
          <span class="jp-lcp-bande is-bon" :style="{ width: (2.5 / LCP_MAX) * 100 + '%' }"></span>
          <span class="jp-lcp-bande is-moyen" :style="{ width: (1.5 / LCP_MAX) * 100 + '%' }"></span>
          <span class="jp-lcp-bande is-faible" :style="{ width: (4 / LCP_MAX) * 100 + '%' }"></span>
          <span v-if="typeof site.lcp === 'number'" class="jp-lcp-curseur" :style="{ left: posLcp(site.lcp) + '%' }"></span>
        </div>
        <div class="jp-lcp-axe" aria-hidden="true">
          <span>0 s</span><span style="left: 31.25%">2,5 s</span><span style="left: 50%">4 s</span><span style="left: 100%">8 s +</span>
        </div>
        <p v-if="typeof site.lcp === 'number'" class="jp-etat jp-etat--ligne" :class="'is-' + etatLcp(site.lcp).cle">
          {{ etatLcp(site.lcp).icone }} LCP {{ etatLcp(site.lcp).libelle.toLowerCase() }}
        </p>
      </div>
    </div>

    <p v-if="comparaison" class="jp-comparaison">{{ comparaison }}</p>

    <dl class="jp-legende">
      <div><dt class="is-bon">● 90 à 100</dt><dd>Bon</dd></div>
      <div><dt class="is-moyen">■ 50 à 89</dt><dd>À améliorer</dd></div>
      <div><dt class="is-faible">▲ 0 à 49</dt><dd>Faible</dd></div>
      <div><dt>LCP</dt><dd>Temps d'affichage du plus gros élément visible (image, titre…). Bon : 2,5 s ou moins.</dd></div>
    </dl>
  </section>
</template>

<style scoped>
.jp {
  --bon: var(--vp-c-green-1);
  --moyen: var(--vp-c-yellow-1);
  --faible: var(--vp-c-red-1);
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.jp-intro {
  margin: 0 0 0.75rem !important;
  font-size: 0.875rem;
}
.jp-grille {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 0.75rem;
}
.jp-site {
  padding: 0.75rem 0.9rem 0.9rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.75rem;
  background: var(--vp-c-bg);
}
.jp-nom {
  margin: 0 0 0.5rem !important;
  font-size: 0.95rem;
}
.jp-jauge-zone {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  margin-bottom: 0.75rem;
}
.jp-jauge {
  width: 84px;
  height: 84px;
  flex-shrink: 0;
  --c: var(--vp-c-text-3);
}
.jp-jauge.is-bon { --c: var(--bon); }
.jp-jauge.is-moyen { --c: var(--moyen); }
.jp-jauge.is-faible { --c: var(--faible); }
.jp-fond {
  fill: color-mix(in srgb, var(--c) 10%, transparent);
  stroke: var(--vp-c-divider);
  stroke-width: 7;
}
.jp-arc {
  fill: none;
  stroke: var(--c);
  stroke-width: 7;
  stroke-linecap: round;
  transition: stroke-dasharray 0.6s ease, stroke 0.3s;
}
.jp-valeur {
  font-size: 24px;
  font-weight: 700;
  fill: var(--c);
  font-family: var(--vp-font-family-base);
}
.jp-champ {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  font-size: 0.75rem;
  color: var(--vp-c-text-2);
}
.jp-champ input {
  width: 100%;
  max-width: 9rem;
  padding: 0.3rem 0.5rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.45rem;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font-size: 0.875rem;
}
.jp-champ input:focus {
  border-color: var(--vp-c-brand-1);
  outline: none;
}
.jp-etat {
  font-size: 0.78rem;
  font-weight: 600;
}
.jp-etat.is-bon { color: var(--bon); }
.jp-etat.is-moyen { color: var(--moyen); }
.jp-etat.is-faible { color: var(--faible); }
.jp-etat--ligne {
  margin: 0.35rem 0 0 !important;
}
.jp-lcp {
  position: relative;
  display: flex;
  gap: 2px;
  height: 8px;
  margin-top: 0.6rem;
}
.jp-lcp-bande {
  height: 100%;
  border-radius: 2px;
  opacity: 0.75;
}
.jp-lcp-bande.is-bon { background: var(--bon); }
.jp-lcp-bande.is-moyen { background: var(--moyen); }
.jp-lcp-bande.is-faible { background: var(--faible); }
.jp-lcp-curseur {
  position: absolute;
  top: -4px;
  width: 4px;
  height: 16px;
  margin-left: -2px;
  border-radius: 2px;
  background: var(--vp-c-text-1);
  box-shadow: 0 0 0 2px var(--vp-c-bg);
  transition: left 0.4s ease;
}
.jp-lcp-axe {
  position: relative;
  height: 1rem;
  margin-top: 0.2rem;
  font-size: 0.68rem;
  color: var(--vp-c-text-2);
}
.jp-lcp-axe span {
  position: absolute;
  transform: translateX(-50%);
  white-space: nowrap;
}
.jp-lcp-axe span:first-child {
  transform: none;
}
.jp-lcp-axe span:last-child {
  transform: translateX(-100%);
}
.jp-comparaison {
  margin: 0.75rem 0 0 !important;
  font-weight: 600;
  font-size: 0.9rem;
}
.jp-legende {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem 1.25rem;
  margin: 0.9rem 0 0;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.78rem;
}
.jp-legende div {
  display: flex;
  gap: 0.35rem;
}
.jp-legende dt {
  font-weight: 600;
}
.jp-legende dt.is-bon { color: var(--bon); }
.jp-legende dt.is-moyen { color: var(--moyen); }
.jp-legende dt.is-faible { color: var(--faible); }
.jp-legende dd {
  margin: 0;
  color: var(--vp-c-text-2);
}
@media (prefers-reduced-motion: reduce) {
  .jp-arc, .jp-lcp-curseur { transition: none; }
}
</style>
