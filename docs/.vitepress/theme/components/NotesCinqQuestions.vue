<script setup lang="ts">
import { onMounted, reactive, watch } from "vue";
import BoutonCopier from "./BoutonCopier.vue";

const QUESTIONS = [
  { cle: "Q1", titre: "Comment réserver et payer en ligne ?" },
  { cle: "Q2", titre: "Comment faire signer la décharge avant l'arrivée ?" },
  { cle: "Q3", titre: "Sur quelle plateforme construire le site ?" },
  { cle: "Q4", titre: "Comment montrer les vidéos sans ralentir le site ?" },
  { cle: "Q5", titre: "Comment offrir le site en français et en anglais ?" },
];

const CHAMPS = [
  { cle: "outils", titre: "Outils essayés par l'équipe", aide: "Noms, et la famille de solution de chacun" },
  { cle: "constats", titre: "Leurs constats", aide: "Ce qui a réussi, échoué, ce qui était non vérifiable" },
  { cle: "verifier", titre: "À vérifier nous-mêmes pour notre survol", aide: "Page de prix, documentation, témoignages à aller lire" },
] as const;

type Cle = (typeof CHAMPS)[number]["cle"];

const props = withDefaults(defineProps<{ storageKey?: string }>(), {
  storageKey: "asm-notes-cinq-questions",
});

const notes = reactive(
  Object.fromEntries(QUESTIONS.map((q) => [q.cle, { outils: "", constats: "", verifier: "" }])) as Record<string, Record<Cle, string>>,
);

function texteNotes() {
  return [
    "Séance 4 — Retour en grand groupe : notes sur les cinq questions",
    ...QUESTIONS.map((q) =>
      [`${q.cle} — ${q.titre}`, ...CHAMPS.map((c) => `   ${c.titre} : ${notes[q.cle][c.cle].trim() || "—"}`)].join("\n"),
    ),
  ].join("\n\n");
}

function reinitialiser() {
  if (!confirm("Effacer toutes vos notes ? Avez-vous copié vos notes ?")) return;
  for (const q of QUESTIONS) Object.assign(notes[q.cle], { outils: "", constats: "", verifier: "" });
}

onMounted(() => {
  try {
    const data = JSON.parse(localStorage.getItem(props.storageKey) ?? "null");
    if (!data) return;
    for (const q of QUESTIONS) for (const c of CHAMPS) notes[q.cle][c.cle] = String(data[q.cle]?.[c.cle] ?? "");
  } catch {
    /* stockage indisponible : on part de notes vides */
  }
});

watch(notes, () => {
  try {
    localStorage.setItem(props.storageKey, JSON.stringify(notes));
  } catch {
    /* stockage indisponible : rien à faire */
  }
});
</script>

<template>
  <section class="nq">
    <article v-for="q in QUESTIONS" :key="q.cle" class="nq-carte">
      <p class="nq-titre"><span class="nq-q">{{ q.cle }}</span> {{ q.titre }}</p>
      <div class="nq-champs">
        <label v-for="c in CHAMPS" :key="c.cle" class="nq-champ">
          <span>{{ c.titre }}</span>
          <textarea v-model="notes[q.cle][c.cle]" rows="3" :placeholder="c.aide" />
        </label>
      </div>
    </article>

    <p class="nq-rappel">Vos notes restent dans ce navigateur, mais elles peuvent disparaître si la cache est vidée. <strong>Copiez-les dans vos notes de cours</strong> à la fin du retour.</p>
    <div class="nq-pied">
      <BoutonCopier :texte="texteNotes" libelle="Copier mes notes" />
      <button type="button" class="nq-action" @click="reinitialiser">Tout effacer</button>
    </div>
  </section>
</template>

<style scoped>
.nq {
  display: grid;
  gap: 0.6rem;
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.nq-carte {
  padding: 0.7rem 0.8rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.7rem;
  background: var(--vp-c-bg);
}
.nq-titre {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 0 0.5rem !important;
  font-weight: 600;
  line-height: 1.35;
}
.nq-q {
  flex-shrink: 0;
  padding: 0.1rem 0.45rem;
  border-radius: 0.4rem;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-size: 0.8rem;
  font-weight: 700;
}
.nq-champs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.5rem;
}
.nq-champ {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
.nq-champ textarea {
  width: 100%;
  padding: 0.4rem 0.55rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.5rem;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font: inherit;
  font-size: 0.85rem;
  font-weight: 400;
  resize: vertical;
}
.nq-champ textarea:focus { outline: none; border-color: var(--vp-c-brand-1); }
.nq-rappel {
  margin: 0.2rem 0 0 !important;
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
.nq-pied {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
}
.nq-action {
  padding: 0.3rem 0.7rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.nq-action:hover { border-color: var(--vp-c-brand-1); }
</style>
