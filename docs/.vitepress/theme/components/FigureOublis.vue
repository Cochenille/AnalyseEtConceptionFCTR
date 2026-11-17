<script setup lang="ts">
// Séance 8 : les cinq tâches qu'on oublie presque toujours dans une estimation.
const OUBLIS = [
  { cle: "gestion", titre: "Gestion de projet", sous: "courriels, appels, rencontres de suivi" },
  { cle: "contenu", titre: "Intégrer le contenu", sous: "textes, photos, traductions du client" },
  { cle: "tests", titre: "Tests et corrections", sous: "téléphone, clavier, deux langues" },
  { cle: "formation", titre: "Formation", sous: "Mélanie modifie les prix seule" },
  { cle: "enligne", titre: "Mise en ligne", sous: "domaine, redirections, vérifications" },
];
</script>

<template>
  <figure class="fig7 fo">
    <ul class="fo-liste">
      <li v-for="o in OUBLIS" :key="o.cle">
        <svg viewBox="0 0 32 32" aria-hidden="true" class="fo-icone">
          <g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <template v-if="o.cle === 'gestion'">
              <path d="M5 7h16v11H11l-5 4v-4H5z" />
              <path d="M24 12h3v10h-2v3l-4-3h-8" />
            </template>
            <template v-else-if="o.cle === 'contenu'">
              <rect x="5" y="5" width="22" height="22" rx="2" />
              <circle cx="12" cy="12" r="2.5" />
              <path d="M5 23l7-7 5 5 3-3 7 7" />
            </template>
            <template v-else-if="o.cle === 'tests'">
              <rect x="9" y="3" width="14" height="26" rx="2.5" />
              <path d="M12.5 16l3 3 5-6" />
            </template>
            <template v-else-if="o.cle === 'formation'">
              <circle cx="11" cy="9" r="3.5" />
              <path d="M4 27v-5a7 7 0 0 1 14 0v5" />
              <rect x="20" y="6" width="9" height="7" rx="1" />
              <path d="M17 17l4-4" />
            </template>
            <template v-else>
              <circle cx="16" cy="16" r="11" />
              <path d="M5 16h22M16 5c3.5 3.2 3.5 18.8 0 22M16 5c-3.5 3.2-3.5 18.8 0 22" />
            </template>
          </g>
        </svg>
        <strong>{{ o.titre }}</strong>
        <span>{{ o.sous }}</span>
      </li>
    </ul>
    <figcaption>
      <strong>Les cinq tâches qu'on oublie.</strong> Aucune n'est une page du site, et pourtant elles prennent souvent le tiers du projet. Relisez cette liste avant de chiffrer.
    </figcaption>
  </figure>
</template>

<style scoped>
.fo-liste {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 0.6rem;
  margin: 0 !important;
  padding: 0 !important;
  list-style: none;
}
.fo-liste li {
  display: grid;
  justify-items: center;
  gap: 0.25rem;
  margin: 0 !important;
  padding: 0.8rem 0.6rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.7rem;
  background: var(--vp-c-bg);
  text-align: center;
  line-height: 1.3;
}
.fo-icone {
  width: 2.2rem;
  height: 2.2rem;
  margin-bottom: 0.2rem;
  color: var(--vp-c-warning-1);
}
.fo-liste strong { font-size: 0.85rem; }
.fo-liste span { font-size: 0.74rem; color: var(--vp-c-text-2); }
</style>
