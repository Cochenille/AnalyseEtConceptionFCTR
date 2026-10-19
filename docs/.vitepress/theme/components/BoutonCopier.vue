<script setup lang="ts">
// Bouton « Copier nos réponses » commun aux activités.
// Les étudiants perdent parfois ce qu'ils ont saisi (cache vidée) :
// on copie en texte brut et, si fourni, en HTML pour que les tableaux
// se collent proprement dans Word. Si le presse-papiers refuse,
// le texte s'affiche sélectionné dans une fenêtre pour un Ctrl+C manuel.
import { nextTick, ref } from "vue";

const props = withDefaults(
  defineProps<{
    texte: () => string;
    html?: () => string;
    libelle?: string;
    principal?: boolean;
  }>(),
  { libelle: "Copier nos réponses", principal: true },
);

const copie = ref(false);
const secours = ref("");
const zone = ref<HTMLTextAreaElement | null>(null);

async function copier() {
  const texte = props.texte();
  try {
    if (props.html && typeof ClipboardItem !== "undefined" && navigator.clipboard?.write) {
      await navigator.clipboard.write([
        new ClipboardItem({
          "text/plain": new Blob([texte], { type: "text/plain" }),
          "text/html": new Blob([props.html()], { type: "text/html" }),
        }),
      ]);
    } else {
      await navigator.clipboard.writeText(texte);
    }
    copie.value = true;
    setTimeout(() => (copie.value = false), 2500);
  } catch {
    secours.value = texte;
    await nextTick();
    zone.value?.focus();
    zone.value?.select();
  }
}
</script>

<template>
  <button type="button" class="bc-btn" :class="{ 'is-principal': principal }" @click="copier">
    {{ copie ? "Copié ✓ — collez dans vos notes" : libelle }}
  </button>
  <Teleport to="body">
    <div v-if="secours" class="bc-fond" @click.self="secours = ''">
      <div class="bc-boite" role="dialog" aria-modal="true" aria-labelledby="bc-titre">
        <p id="bc-titre" class="bc-titre">La copie automatique n'a pas fonctionné</p>
        <p class="bc-aide">Le texte est sélectionné : faites <kbd>Ctrl</kbd>+<kbd>C</kbd> (<kbd>Cmd</kbd>+<kbd>C</kbd> sur Mac), puis collez-le dans vos notes.</p>
        <textarea ref="zone" class="bc-zone" readonly :value="secours" rows="12" />
        <button type="button" class="bc-btn is-principal" @click="secours = ''">Fermer</button>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.bc-btn {
  padding: 0.3rem 0.75rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
  transition: border-color 0.15s;
}
.bc-btn:hover { border-color: var(--vp-c-brand-1); }
.bc-btn.is-principal {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
  font-weight: 600;
}
.bc-fond {
  position: fixed;
  inset: 0;
  z-index: 200;
  display: grid;
  place-items: center;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.5);
}
.bc-boite {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  width: min(640px, 100%);
  padding: 1rem;
  border-radius: 0.9rem;
  background: var(--vp-c-bg);
  box-shadow: var(--vp-shadow-4);
}
.bc-titre { margin: 0; font-weight: 700; }
.bc-aide { margin: 0; font-size: 0.85rem; color: var(--vp-c-text-2); }
.bc-zone {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.5rem;
  background: var(--vp-c-bg-soft);
  font-family: var(--vp-font-family-mono);
  font-size: 0.75rem;
}
.bc-boite .bc-btn { align-self: flex-end; }
</style>
