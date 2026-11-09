<script setup lang="ts">
import { withBase } from "vitepress";
</script>

<template>
  <figure class="fig7 mv">
    <div class="mv-logo">
      <div class="mv-cadre">
        <img :src="withBase('/images/seance7/logo.svg')" alt="Le logo d'Aventure Saint-Maurice" width="120" height="120" />
        <span class="mv-zone" aria-hidden="true" />
      </div>
      <span class="fig7-sous">Le logo affiché à 120 px. On agrandit la zone encadrée.</span>
    </div>
    <div class="fig7-duo">
      <div class="fig7-panneau">
        <span class="fig7-titre">Image matricielle (PNG)</span>
        <img class="pixels mv-zoom" :src="withBase('/images/seance7/logo-pixels.png')" alt="Le sommet de la montagne du logo en PNG, agrandi : on voit les carrés des pixels." width="36" height="36" />
        <span class="fig7-sous">36 × 36 pixels, agrandis 8 fois : chaque carré est un pixel. Les bords deviennent des marches.</span>
      </div>
      <div class="fig7-panneau">
        <span class="fig7-titre">Image vectorielle (SVG)</span>
        <img class="mv-zoom" :src="withBase('/images/seance7/logo-zoom.svg')" alt="Le même sommet en SVG, agrandi : les bords restent nets." width="288" height="288" />
        <span class="fig7-sous">Le même fichier de 3 Ko, agrandi autant qu'on veut : le navigateur redessine les formes à chaque taille.</span>
      </div>
    </div>
    <figcaption>
      <strong>Même logo, même agrandissement.</strong> Un écran de téléphone affiche deux ou trois pixels pour un : un logo matriciel trop petit y paraît flou, un SVG reste net.
    </figcaption>
  </figure>
</template>

<style scoped>
.mv-logo { display: flex; align-items: center; gap: 0.9rem; margin-bottom: 1rem; }
.mv-cadre { position: relative; flex: none; width: 120px; height: 120px; border-radius: 0.4rem; background: #fff; }
.mv-zone {
  position: absolute;
  left: 40px;
  top: 20px;
  width: 36px;
  height: 36px;
  border: 2px solid var(--vp-c-red-1);
  border-radius: 2px;
}
.mv-zoom {
  width: 100%;
  max-width: 288px !important;
  aspect-ratio: 1;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
}
</style>
