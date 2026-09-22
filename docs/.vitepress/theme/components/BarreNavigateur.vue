<script setup lang="ts">
// Maquette simplifiée d'un navigateur pour montrer où cliquer.
// Les libellés varient d'un navigateur à l'autre.
withDefaults(defineProps<{ mode?: "cadenas" | "extension" }>(), { mode: "cadenas" });
</script>

<template>
  <figure class="bn">
    <svg
      viewBox="0 0 640 250"
      class="bn-svg"
      role="img"
      :aria-label="
        mode === 'cadenas'
          ? 'Maquette : cliquer sur l\'icône à gauche de l\'adresse, puis sur La connexion est sécurisée, puis Le certificat est valide'
          : 'Maquette : cliquer sur l\'icône de l\'extension Wappalyzer à droite de la barre d\'adresse'
      "
    >
      <!-- Fenêtre -->
      <rect x="1" y="1" width="638" height="248" rx="12" class="bn-fenetre" />
      <path d="M1,13 a12,12 0 0 1 12,-12 H627 a12,12 0 0 1 12,12 V42 H1 Z" class="bn-onglets" />
      <rect x="52" y="10" width="170" height="32" rx="8" class="bn-onglet" />
      <text x="70" y="31" class="bn-texte-petit">Restaurant — Accueil</text>
      <circle cx="18" cy="22" r="5" class="bn-pastille" />
      <circle cx="34" cy="22" r="5" class="bn-pastille" />

      <!-- Barre d'adresse -->
      <rect x="1" y="42" width="638" height="44" class="bn-barre" />
      <text x="16" y="70" class="bn-nav">←  →  ↻</text>
      <rect x="92" y="51" width="440" height="26" rx="13" class="bn-adresse" />
      <g :class="{ 'bn-cible': mode === 'cadenas' }">
        <circle cx="108" cy="64" r="10" class="bn-halo" />
        <!-- cadenas -->
        <rect x="103" y="62" width="10" height="8" rx="1.5" class="bn-icone-plein" />
        <path d="M105,62 v-3 a3,3 0 0 1 6,0 v3" class="bn-icone-trait" />
      </g>
      <text x="124" y="69" class="bn-url">restaurant-exemple.ca</text>

      <!-- Extensions -->
      <g :class="{ 'bn-cible': mode === 'extension' }">
        <circle cx="560" cy="64" r="12" class="bn-halo" />
        <path d="M553,58 l7,-4 l7,4 v12 l-7,4 l-7,-4 z" class="bn-icone-plein" />
      </g>
      <text x="590" y="69" class="bn-nav">⋮</text>

      <!-- Page (fond estompé) -->
      <rect x="40" y="110" width="200" height="16" rx="4" class="bn-bloc" />
      <rect x="40" y="136" width="320" height="10" rx="3" class="bn-bloc" />
      <rect x="40" y="154" width="280" height="10" rx="3" class="bn-bloc" />
      <rect x="40" y="180" width="140" height="50" rx="6" class="bn-bloc" />
      <rect x="190" y="180" width="140" height="50" rx="6" class="bn-bloc" />

      <!-- Panneau : certificat -->
      <g v-if="mode === 'cadenas'">
        <rect x="96" y="84" width="260" height="130" rx="10" class="bn-panneau" />
        <text x="112" y="108" class="bn-texte-fort">restaurant-exemple.ca</text>
        <rect x="106" y="120" width="240" height="32" rx="6" class="bn-choix bn-choix--actif" />
        <text x="118" y="141" class="bn-texte">La connexion est sécurisée</text>
        <text x="334" y="141" text-anchor="end" class="bn-texte">›</text>
        <rect x="106" y="160" width="240" height="32" rx="6" class="bn-choix bn-choix--actif" />
        <text x="118" y="181" class="bn-texte">Le certificat est valide</text>
        <text x="334" y="181" text-anchor="end" class="bn-texte">›</text>

        <g class="bn-bulle-num">
          <circle cx="86" cy="64" r="10" /><text x="86" y="68" text-anchor="middle">1</text>
          <circle cx="368" cy="136" r="10" /><text x="368" y="140" text-anchor="middle">2</text>
          <circle cx="368" cy="176" r="10" /><text x="368" y="180" text-anchor="middle">3</text>
        </g>
        <text x="390" y="140" class="bn-note">Émetteur : Let's Encrypt, Google…</text>
        <text x="390" y="180" class="bn-note">Valide jusqu'au : …</text>
      </g>

      <!-- Panneau : Wappalyzer (exemple fictif) -->
      <g v-else>
        <rect x="372" y="84" width="252" height="156" rx="10" class="bn-panneau" />
        <text x="388" y="106" class="bn-texte-fort">Technologies détectées</text>
        <text x="388" y="130" class="bn-cat">CMS</text>
        <text x="500" y="130" class="bn-texte">WordPress</text>
        <text x="388" y="152" class="bn-cat">Serveur Web</text>
        <text x="500" y="152" class="bn-texte">Nginx</text>
        <text x="388" y="174" class="bn-cat">Réservation</text>
        <text x="500" y="174" class="bn-texte">Libro</text>
        <text x="388" y="196" class="bn-cat">Analytique</text>
        <text x="500" y="196" class="bn-texte">Google Analytics</text>
        <text x="388" y="218" class="bn-cat">Bibliothèque JS</text>
        <text x="500" y="218" class="bn-texte">jQuery 3.6</text>
        <g class="bn-bulle-num">
          <circle cx="538" cy="64" r="10" /><text x="538" y="68" text-anchor="middle">1</text>
        </g>
        <text x="360" y="128" text-anchor="end" class="bn-note">Exemple fictif</text>
      </g>
    </svg>
    <figcaption class="bn-legende">
      <template v-if="mode === 'cadenas'">
        Où trouver le certificat. Les libellés varient selon le navigateur (Chrome, Edge, Firefox).
      </template>
      <template v-else>
        L'icône de Wappalyzer apparaît à droite de la barre d'adresse une fois l'extension épinglée.
      </template>
    </figcaption>
  </figure>
</template>

<style scoped>
.bn {
  margin: 1rem 0 1.5rem;
}
.bn-svg {
  display: block;
  width: 100%;
  max-width: 640px;
  height: auto;
  font-family: var(--vp-font-family-base);
}
.bn-fenetre {
  fill: var(--vp-c-bg);
  stroke: var(--vp-c-divider);
  stroke-width: 1.5;
}
.bn-onglets {
  fill: var(--vp-c-bg-alt);
}
.bn-onglet,
.bn-barre {
  fill: var(--vp-c-bg-soft);
}
.bn-pastille {
  fill: var(--vp-c-divider);
}
.bn-adresse {
  fill: var(--vp-c-bg);
  stroke: var(--vp-c-divider);
}
.bn-nav {
  font-size: 14px;
  fill: var(--vp-c-text-2);
}
.bn-url {
  font-size: 13px;
  fill: var(--vp-c-text-1);
}
.bn-icone-plein {
  fill: var(--vp-c-text-2);
}
.bn-icone-trait {
  fill: none;
  stroke: var(--vp-c-text-2);
  stroke-width: 1.6;
}
.bn-halo {
  fill: transparent;
}
.bn-cible .bn-halo {
  fill: var(--vp-c-brand-soft);
  stroke: var(--vp-c-brand-1);
  stroke-width: 2;
  animation: bn-pulse 1.8s ease-in-out infinite;
  transform-box: fill-box;
  transform-origin: center;
}
.bn-cible .bn-icone-plein {
  fill: var(--vp-c-brand-1);
}
.bn-cible .bn-icone-trait {
  stroke: var(--vp-c-brand-1);
}
.bn-bloc {
  fill: var(--vp-c-default-soft);
}
.bn-panneau {
  fill: var(--vp-c-bg);
  stroke: var(--vp-c-divider);
  filter: drop-shadow(0 6px 14px rgba(0, 0, 0, 0.14));
}
.bn-choix {
  fill: var(--vp-c-bg-soft);
}
.bn-choix--actif {
  stroke: var(--vp-c-brand-1);
  stroke-width: 1.5;
}
.bn-texte-petit {
  font-size: 11px;
  fill: var(--vp-c-text-2);
}
.bn-texte {
  font-size: 13px;
  fill: var(--vp-c-text-1);
}
.bn-texte-fort {
  font-size: 13px;
  font-weight: 600;
  fill: var(--vp-c-text-1);
}
.bn-cat {
  font-size: 12px;
  fill: var(--vp-c-text-2);
}
.bn-note {
  font-size: 12px;
  font-style: italic;
  fill: var(--vp-c-text-2);
}
.bn-bulle-num circle {
  fill: var(--vp-c-brand-1);
}
.bn-bulle-num text {
  font-size: 12px;
  font-weight: 700;
  fill: var(--vp-c-white);
}
.bn-legende {
  margin-top: 0.4rem;
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
@keyframes bn-pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.18); }
}
@media (prefers-reduced-motion: reduce) {
  .bn-cible .bn-halo { animation: none; }
}
</style>
