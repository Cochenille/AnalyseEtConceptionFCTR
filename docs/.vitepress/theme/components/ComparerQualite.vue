<script setup lang="ts">
import { computed, ref } from "vue";
import { withBase } from "vitepress";

// Poids mesurés sur la photo entière réduite à 1920 px (outils/medias/generer_visuels_seance7.py).
const NIVEAUX = [
  { q: 90, poids: 104, avis: "Impossible à distinguer de l'original." },
  { q: 60, poids: 28, avis: "Toujours impeccable à 100 %, pour quatre fois moins lourd." },
  { q: 30, poids: 21, avis: "De légères marches apparaissent dans le dégradé du ciel." },
  { q: 8, poids: 16, avis: "Des blocs et des marches partout : trop loin." },
];

const choix = ref(1);
const niveau = computed(() => NIVEAUX[choix.value]);
</script>

<template>
  <figure class="fig7 cq">
    <div class="cq-boutons" role="group" aria-label="Qualité JPEG">
      <button
        v-for="(n, i) in NIVEAUX"
        :key="n.q"
        type="button"
        class="cq-btn"
        :aria-pressed="choix === i"
        @click="choix = i"
      >
        Qualité {{ n.q }}
      </button>
    </div>
    <div class="cq-image">
      <img
        v-for="(n, i) in NIVEAUX"
        v-show="choix === i"
        :key="n.q"
        :src="withBase(`/images/seance7/qualite-${n.q}.png`)"
        :alt="`Portion du coucher de soleil en JPEG, qualité ${n.q}`"
        width="720"
        height="405"
      />
      <span class="cq-etiquette">JPEG {{ niveau.q }} · <strong>{{ niveau.poids }} Ko</strong> pour toute la photo</span>
    </div>
    <p class="cq-avis">{{ niveau.avis }}</p>
    <figcaption>
      <strong>Une portion du coucher de soleil, réduit à 1920 px, à 100 % de zoom.</strong> Le poids baisse vite au début, puis presque plus : passé un certain point, on perd de la qualité sans rien gagner. Les outils proposent souvent 75 par défaut; c'est un bon départ, à vérifier à l'œil.
    </figcaption>
  </figure>
</template>

<style scoped>
.cq-boutons { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 0.6rem; }
.cq-btn {
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
  font-weight: 600;
}
.cq-btn:hover { border-color: var(--vp-c-brand-1); }
.cq-btn[aria-pressed="true"] { border-color: var(--vp-c-brand-1); background: var(--vp-c-brand-soft); color: var(--vp-c-brand-1); }
.cq-image { position: relative; max-width: 720px; }
.cq-image img { width: 100%; }
.cq-etiquette {
  position: absolute;
  left: 0.5rem;
  bottom: 0.5rem;
  padding: 0.2rem 0.55rem;
  border-radius: 0.4rem;
  background: rgb(0 0 0 / 0.65);
  color: #fff;
  font-size: 0.78rem;
}
.cq-avis { margin: 0.5rem 0 0 !important; font-size: 0.9rem; font-weight: 600; }
</style>
