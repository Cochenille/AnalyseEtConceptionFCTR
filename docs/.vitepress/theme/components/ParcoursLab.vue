<script setup lang="ts">
const ETAPES = [
  { ancre: "preparation", court: "Prép.", titre: "Préparation", min: 10, outil: "Fiche + outils" },
  { ancre: "partie-1", court: "1", titre: "Première impression", min: 10, outil: "Vos yeux" },
  { ancre: "partie-2", court: "2", titre: "Technologies", min: 15, outil: "Wappalyzer" },
  { ancre: "partie-3", court: "3", titre: "Domaine et sécurité", min: 15, outil: "ICANN Lookup, cadenas" },
  { ancre: "partie-4", court: "4", titre: "Performance et mobile", min: 20, outil: "PageSpeed, F12" },
  { ancre: "partie-5", court: "5", titre: "Code source", min: 10, outil: "Ctrl + U" },
  { ancre: "partie-6", court: "6", titre: "Contraintes", min: 10, outil: "Vos observations" },
  { ancre: "partie-7", court: "7", titre: "Verdict", min: 10, outil: "Justification" },
];
const total = ETAPES.reduce((t, e) => t + e.min, 0);

// Les trois grandes phases de l'enquête
const PHASES = [
  { titre: "Observer", de: 0, a: 1 },
  { titre: "Mesurer", de: 2, a: 5 },
  { titre: "Juger", de: 6, a: 7 },
];
const largeur = (de: number, a: number) =>
  (ETAPES.slice(de, a + 1).reduce((t, e) => t + e.min, 0) / total) * 100 + "%";
</script>

<template>
  <nav class="pl" aria-label="Parcours du laboratoire">
    <div class="pl-phases" aria-hidden="true">
      <span v-for="p in PHASES" :key="p.titre" :style="{ width: largeur(p.de, p.a) }">{{ p.titre }}</span>
    </div>
    <ol class="pl-barre">
      <li v-for="(e, n) in ETAPES" :key="e.ancre" :style="{ flexGrow: e.min }">
        <a :href="'#' + e.ancre" class="pl-seg" :class="'pl-seg--' + (n < 2 ? 0 : n < 6 ? 1 : 2)">
          <span class="pl-num">{{ e.court }}</span>
          <span class="pl-titre">{{ e.titre }}</span>
          <span class="pl-meta">{{ e.min }} min · {{ e.outil }}</span>
        </a>
      </li>
    </ol>
    <p class="pl-total"> Cliquez sur une étape pour y aller.</p>
  </nav>
</template>

<style scoped>
.pl {
  margin: 1.25rem 0 1.75rem;
}
.pl-phases {
  display: flex;
  margin-bottom: 0.3rem;
}
.pl-phases span {
  padding-left: 0.2rem;
  border-left: 2px solid var(--vp-c-divider);
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--vp-c-text-2);
}
.pl-barre {
  display: flex;
  gap: 3px;
  margin: 0 !important;
  padding: 0 !important;
  list-style: none !important;
}
.pl-barre li {
  flex-basis: 0;
  min-width: 0;
  margin: 0 !important;
}
.pl-seg {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 0.5rem 0.45rem;
  border-radius: 0.5rem;
  text-decoration: none !important;
  color: var(--vp-c-text-1) !important;
  transition: transform 0.15s, box-shadow 0.15s;
}
.pl-seg:hover {
  transform: translateY(-2px);
  box-shadow: var(--vp-shadow-2);
}
.pl-seg--0 {
  background: var(--vp-c-default-soft);
}
.pl-seg--1 {
  background: var(--vp-c-brand-soft);
}
.pl-seg--2 {
  background: color-mix(in srgb, var(--vp-c-brand-1) 28%, transparent);
}
.pl-num {
  font-size: 1rem;
  font-weight: 700;
  line-height: 1.2;
}
.pl-titre {
  margin-top: 0.15rem;
  font-size: 0.75rem;
  font-weight: 600;
  line-height: 1.25;
}
.pl-meta {
  margin-top: auto;
  padding-top: 0.25rem;
  font-size: 0.68rem;
  line-height: 1.3;
  color: var(--vp-c-text-2);
}
.pl-total {
  margin: 0.5rem 0 0 !important;
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
@media (max-width: 640px) {
  .pl-phases {
    display: none;
  }
  .pl-barre {
    flex-direction: column;
  }
  .pl-seg {
    flex-direction: row;
    align-items: baseline;
    gap: 0.5rem;
  }
  .pl-titre {
    margin: 0;
  }
  .pl-meta {
    margin: 0 0 0 auto;
    padding: 0;
  }
}
</style>
