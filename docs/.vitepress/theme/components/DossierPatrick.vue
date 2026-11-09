<script setup lang="ts">
import { withBase } from "vitepress";

// Séance 7 : ce que Patrick a envoyé, tel quel (poids mesurés sur le dossier du Lab 07).
const FICHIERS = [
  { img: "m1", nom: "IMG_4521.JPG", sorte: "Photo · JPEG", dims: "6000 × 4000", poids: "6,7 Mo", ou: "Bannière de l'accueil" },
  { img: "m2", nom: "IMG_4540.HEIC", sorte: "Photo · HEIC", dims: "4032 × 3024", poids: "1,7 Mo", ou: "Page de l'offre adaptée" },
  { img: "m3", nom: "via ferrata FALAISE final(2).png", sorte: "Photo · PNG", dims: "2400 × 1800", poids: "7,5 Mo", ou: "Page Via ferrata" },
  { img: "m4", nom: "logo-ASM-final.png + logo-ASM.svg", sorte: "Dessin · PNG et SVG", dims: "3000 × 3000", poids: "111 Ko + 58 Ko", ou: "En-tête de chaque page", contenir: true },
  { img: "m5", nom: "carte-parcours.png", sorte: "Dessin avec texte · PNG", dims: "3600 × 2400", poids: "487 Ko", ou: "Page Via ferrata" },
  { img: "m6", nom: "DJI_0042.MOV", sorte: "Vidéo 4K · 8 s · avec son", dims: "3840 × 2160", poids: "16 Mo", ou: "Arrière-plan de l'accueil", video: true },
  { img: "m7", nom: "Tarifs 2027 SCAN.pdf", sorte: "Document numérisé · PDF", dims: "2 pages", poids: "3,1 Mo", ou: "Page Tarifs", contenir: true },
];
</script>

<template>
  <figure class="fig7 dp">
    <ul class="dp-grille">
      <li v-for="f in FICHIERS" :key="f.img" class="dp-carte">
        <div class="dp-apercu" :class="{ 'is-contenu': f.contenir }">
          <img :src="withBase(`/images/seance7/dossier/${f.img}.webp`)" alt="" loading="lazy" />
          <span v-if="f.video" class="dp-lecture" aria-hidden="true">▶</span>
        </div>
        <span class="dp-nom">{{ f.nom }}</span>
        <span class="dp-poids">{{ f.poids }}</span>
        <span class="dp-meta">{{ f.sorte }} · {{ f.dims }}</span>
        <span class="dp-ou">→ {{ f.ou }}</span>
      </li>
    </ul>
    <figcaption>
      <strong>L'envoi de Patrick, tel qu'il arrive : environ 36 Mo pour 7 fichiers.</strong>
      Les mêmes fichiers que dans le dossier du Lab 07. Les images sont des paysages générés pour le cours.
    </figcaption>
  </figure>
</template>

<style scoped>
.dp-grille {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.75rem;
  margin: 0 !important;
  padding: 0 !important;
  list-style: none;
}
.dp-carte {
  display: grid;
  gap: 0.2rem;
  align-content: start;
  margin: 0 !important;
  padding: 0.5rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.65rem;
  background: var(--vp-c-bg);
}
.dp-apercu {
  position: relative;
  aspect-ratio: 3 / 2;
  overflow: hidden;
  border-radius: 0.4rem;
  background: var(--vp-c-bg-soft);
}
.dp-apercu img { width: 100%; height: 100% !important; object-fit: cover; border-radius: 0 !important; }
.dp-apercu.is-contenu { background: #fff; }
.dp-apercu.is-contenu img { object-fit: contain; padding: 0.3rem; }
.dp-lecture {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  font-size: 1.4rem;
  color: #fff;
  text-shadow: 0 1px 4px rgb(0 0 0 / 0.6);
}
.dp-nom {
  font-family: var(--vp-font-family-mono);
  font-size: 0.72rem;
  line-height: 1.35;
  word-break: break-word;
}
.dp-poids { font-weight: 700; font-size: 1rem; color: var(--vp-c-red-1); }
.dp-meta, .dp-ou { font-size: 0.75rem; line-height: 1.35; color: var(--vp-c-text-2); }
</style>
