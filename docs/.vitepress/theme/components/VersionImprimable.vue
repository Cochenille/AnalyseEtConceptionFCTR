<script setup>
// Version PDF des pages de modules : bouton en haut de page,
// en-tête et page de notes visibles seulement à l'impression.
import { computed, ref, watch, onMounted, onBeforeUnmount } from "vue";
import { useData, useRoute } from "vitepress";

const props = defineProps({
  position: { type: String, default: "haut" }, // "haut" ou "bas"
});

const { frontmatter, page, site } = useData();
const route = useRoute();

// Actif sur les pages /modules/, ou partout où le frontmatter dit imprimable: true
const actif = computed(() => {
  if (frontmatter.value.imprimable === false) return false;
  return frontmatter.value.imprimable === true || route.path.includes("/modules/");
});

// Lue côté client seulement, pour éviter un écart d'hydratation
const adresse = ref("");
const lireAdresse = () => (adresse.value = window.location.href.split("#")[0].replace(/^https?:\/\//, ""));
watch(() => route.path, () => typeof window !== "undefined" && lireAdresse());

function imprimer() {
  window.print();
}

// Avant l'impression : thème clair et blocs <details> ouverts, puis on remet tout.
let etat = null;
function avant() {
  const html = document.documentElement;
  const details = [...document.querySelectorAll(".vp-doc details:not([open])")];
  etat = { sombre: html.classList.contains("dark"), details };
  html.classList.remove("dark");
  details.forEach((d) => (d.open = true));
}
function apres() {
  if (!etat) return;
  if (etat.sombre) document.documentElement.classList.add("dark");
  etat.details.forEach((d) => (d.open = false));
  etat = null;
}

onMounted(() => {
  lireAdresse();
  if (props.position !== "haut") return;
  window.addEventListener("beforeprint", avant);
  window.addEventListener("afterprint", apres);
});
onBeforeUnmount(() => {
  window.removeEventListener("beforeprint", avant);
  window.removeEventListener("afterprint", apres);
});
</script>

<template>
  <template v-if="actif">
    <template v-if="position === 'haut'">
      <div class="vi-barre">
        <button type="button" class="vi-bouton" @click="imprimer">
          <svg viewBox="0 0 24 24" aria-hidden="true" width="18" height="18">
            <path d="M12 3v12m0 0-4.5-4.5M12 15l4.5-4.5M5 19h14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          Télécharger en PDF
        </button>
        <span class="vi-aide">Dans la fenêtre d'impression, choisissez <strong>« Enregistrer au format PDF »</strong> comme destination. La version PDF garde une marge à droite pour vos notes.</span>
      </div>
      <header class="vi-entete">
        <span>{{ site.title }} — Analyse et conception Web</span>
        <span>{{ adresse }}</span>
      </header>
    </template>

    <section v-else class="vi-notes">
      <h2>Mes notes — {{ page.title }}</h2>
      <div class="vi-lignes" aria-hidden="true">
        <span v-for="n in 22" :key="n" />
      </div>
    </section>
  </template>
</template>

<style scoped>
.vi-barre {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem 0.9rem;
  margin-bottom: 1.5rem;
  padding: 0.6rem 0.8rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.6rem;
  background: var(--vp-c-bg-soft);
}
.vi-bouton {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.85rem;
  border-radius: 999px;
  background: var(--vp-c-brand-1);
  color: var(--vp-c-white);
  font-size: 0.875rem;
  font-weight: 600;
  white-space: nowrap;
  transition: background-color 0.15s;
}
.vi-bouton:hover { background: var(--vp-c-brand-2); }
.vi-bouton:focus-visible { outline: 2px solid var(--vp-c-brand-1); outline-offset: 2px; }
.vi-aide { flex: 1 1 18rem; font-size: 0.8rem; line-height: 1.4; color: var(--vp-c-text-2); }

.vi-entete,
.vi-notes { display: none; }

@media print {
  .vi-barre { display: none; }
  .vi-entete {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1.25rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #ccc;
    font-size: 8pt;
    color: #555;
  }
  .vi-notes {
    display: block;
    break-before: page;
  }
  .vi-notes h2 {
    margin: 0 0 0.5rem;
    padding: 0;
    border: 0;
    font-size: 14pt;
  }
  .vi-lignes span {
    display: block;
    height: 9.5mm;
    border-bottom: 1px solid #bbb;
  }
}
</style>
