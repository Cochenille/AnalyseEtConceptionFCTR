<script setup lang="ts">
import { withBase } from "vitepress";

// Les cadres sont à l'échelle : 6000 px = 100 % de la largeur.
const CADRES = [
  { largeur: 2560, texte: "2560 px · bannière, au plus" },
  { largeur: 1920, texte: "1920 px · bannière pleine largeur" },
  { largeur: 1200, texte: "1200 px · photo dans le texte" },
  { largeur: 600, texte: "600 px · vignette" },
];
const pc = (l: number) => `${(l / 6000) * 100}%`;
</script>

<template>
  <figure class="fig7 ed">
    <div class="ed-photo" :style="{ backgroundImage: `url(${withBase('/images/seance7/dossier/m1.webp')})` }">
      <span class="ed-total">6000 × 4000 px · 24 millions de pixels · 6,7 Mo<br />ce que Patrick envoie</span>
      <span
        v-for="c in CADRES"
        :key="c.largeur"
        class="ed-cadre"
        :class="{ 'is-cible': c.largeur === 1920 }"
        :style="{ width: pc(c.largeur) }"
      >
        <span class="ed-etiquette">{{ c.texte }}</span>
      </span>
    </div>
    <figcaption>
      <strong>À l'échelle.</strong> Le cadre de 1920 px, la plus grande largeur de la bannière, ne couvre qu'un dixième des pixels de la photo (2,5 millions sur 24). Sans réduction, le visiteur télécharge les neuf dixièmes restants pour rien.
    </figcaption>
  </figure>
</template>

<style scoped>
.ed-photo {
  position: relative;
  aspect-ratio: 3 / 2;
  border-radius: 0.5rem;
  background-size: cover;
  background-position: center;
  overflow: hidden;
}
.ed-total {
  position: absolute;
  right: 0.6rem;
  top: 0.5rem;
  max-width: 55%;
  text-align: right;
  font-size: 0.8rem;
  font-weight: 700;
  line-height: 1.35;
  color: #fff;
  text-shadow: 0 1px 3px rgb(0 0 0 / 0.8);
}
.ed-cadre {
  position: absolute;
  left: 0;
  bottom: 0;
  aspect-ratio: 3 / 2;
  border: 2px solid rgb(255 255 255 / 0.9);
  border-left: 0;
  border-bottom: 0;
  background: rgb(0 0 0 / 0.18);
}
.ed-cadre.is-cible { border-color: #ffd54a; border-width: 3px; }
.ed-etiquette {
  position: absolute;
  left: calc(100% + 0.35rem);
  top: -0.1rem;
  white-space: nowrap;
  font-size: 0.7rem;
  font-weight: 600;
  color: #fff;
  text-shadow: 0 1px 3px rgb(0 0 0 / 0.9);
}
.is-cible .ed-etiquette { color: #ffd54a; }
@media (max-width: 520px) {
  .ed-etiquette { font-size: 0.6rem; }
}
</style>
