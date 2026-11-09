<script setup lang="ts">
import { withBase } from "vitepress";
</script>

<template>
  <figure class="fig7 ps">
    <div class="ps-liste">
      <div class="fig7-panneau">
        <span class="fig7-titre">Sans perte : PNG réduit en couleurs · 71 Ko</span>
        <img class="pixels" :src="withBase('/images/seance7/carte-png.png')" alt="La légende de la carte en PNG : le texte vert est net." width="640" height="152" />
      </div>
      <div class="fig7-panneau">
        <span class="fig7-titre">Avec perte : JPEG très compressé · 25 Ko</span>
        <img class="pixels" :src="withBase('/images/seance7/carte-jpeg.png')" alt="La même légende en JPEG très compressé : des bavures et des taches entourent les lettres." width="640" height="152" />
      </div>
    </div>
    <figcaption>
      <strong>La légende de la carte des parcours, agrandie 2 fois.</strong> Le JPEG pèse trois fois moins, mais il fait des bavures autour des lettres et salit le blanc. Sur une photo, ces défauts passent inaperçus; sur du texte et des aplats, ils sautent aux yeux.
    </figcaption>
  </figure>
</template>

<style scoped>
.ps-liste { display: grid; gap: 1rem; }
.ps img { width: 100%; max-width: 640px !important; border: 1px solid var(--vp-c-divider); }
</style>
