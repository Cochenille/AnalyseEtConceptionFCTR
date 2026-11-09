<script setup lang="ts">
import { ref } from "vue";
import { withBase } from "vitepress";

const voile = ref(false);
</script>

<template>
  <figure class="fig7 vc">
    <label class="vc-choix">
      <input v-model="voile" type="checkbox" />
      Ajouter un voile sombre derrière le texte
    </label>
    <div class="vc-banniere" :style="{ backgroundImage: `url(${withBase('/images/seance7/banniere.webp')})` }">
      <div class="vc-texte" :class="{ 'is-voile': voile }">
        <span class="vc-titre">Pagayez la Saint-Maurice</span>
        <span class="vc-sous">Kayak, rabaska, via ferrata et prêt-à-camper, à 45 minutes de Trois-Rivières</span>
        <span class="vc-bouton">Réserver</span>
      </div>
    </div>
    <figcaption>
      <strong>Le même titre, sur une image de la vidéo de drone.</strong> Sans voile, le texte blanc se perd dans le ciel clair : le contraste descend jusqu'à 2,4 pour 1, loin des 4,5 pour 1 exigés. Avec le voile, il dépasse 11 pour 1 partout, quelle que soit l'image qui passe dans la vidéo.
    </figcaption>
  </figure>
</template>

<style scoped>
.vc-choix { display: inline-flex; gap: 0.45rem; align-items: center; margin-bottom: 0.6rem; font-size: 0.875rem; font-weight: 600; cursor: pointer; }
.vc-banniere {
  aspect-ratio: 16 / 9;
  border-radius: 0.5rem;
  background-size: cover;
  background-position: center;
  overflow: hidden;
  display: flex;
}
.vc-texte {
  display: grid;
  align-content: start;
  justify-items: start;
  gap: 0.4rem;
  width: 100%;
  padding: 7% 1.25rem 1rem 45%;
  color: #fff;
  transition: background-color 0.25s;
}
.vc-texte.is-voile { background: linear-gradient(90deg, rgb(10 12 30 / 0.15), rgb(10 12 30 / 0.72) 45%); }
.vc-titre { font-size: clamp(1.2rem, 3.5vw, 1.9rem); font-weight: 800; line-height: 1.1; }
.vc-sous { font-size: 0.85rem; max-width: 34ch; }
.vc-bouton {
  margin-top: 0.3rem;
  padding: 0.3rem 0.9rem;
  border-radius: 999px;
  background: #fff;
  color: #1f2937;
  font-size: 0.8rem;
  font-weight: 700;
}
@media (max-width: 520px) {
  .vc-texte { padding-left: 1rem; }
}
</style>
