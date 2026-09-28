<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from "vue";

type Origine = "T" | "O";
type Risque = { id: string; origine: Origine; texte: string };
type Position = { p: number; c: number } | null;

const props = withDefaults(defineProps<{ storageKey?: string }>(), {
  storageKey: "asm-matrice-risques",
});

const RISQUES: Risque[] = [
  { id: "R1", origine: "O", texte: "Le neveu tarde à transférer le nom de domaine et le compte Wix, ou ne répond plus." },
  { id: "R2", origine: "O", texte: "Les photos, les vidéos et les textes du client arrivent en retard." },
  { id: "R3", origine: "T", texte: "La synchronisation avec Viator ne fonctionne pas comme prévu : il y a encore des doubles réservations." },
  { id: "R4", origine: "O", texte: "La subvention de la MRC est refusée en janvier." },
  { id: "R5", origine: "T", texte: "Le site est trop lent sur les téléphones, surtout sur le site du centre où le réseau est faible." },
  { id: "R6", origine: "T", texte: "Les renseignements de santé des décharges sont vus par une personne non autorisée." },
  { id: "R7", origine: "O", texte: "Personne n'a le temps de mettre le site à jour pendant l'été." },
  { id: "R8", origine: "T", texte: "L'outil de réservation choisi augmente fortement ses prix ou cesse ses activités." },
  { id: "R9", origine: "O", texte: "Mélanie et Patrick ne s'entendent pas sur l'image du site et retardent les approbations." },
  { id: "R10", origine: "T", texte: "Le système de réservation tombe en panne le 1er mars, jour d'ouverture des réservations." },
];

const PROBAS = ["Faible", "Moyenne", "Élevée"];
const CONSEQ = ["Faibles", "Moyennes", "Graves"];

const positions = reactive<Record<string, Position>>(Object.fromEntries(RISQUES.map((r) => [r.id, null])));
const selection = ref<string | null>(null);

const nonPlaces = computed(() => RISQUES.filter((r) => positions[r.id] === null));
const nbPlaces = computed(() => RISQUES.length - nonPlaces.value.length);

function dans(p: number, c: number) {
  return RISQUES.filter((r) => positions[r.id]?.p === p && positions[r.id]?.c === c);
}

function zone(p: number, c: number) {
  const s = (p + 1) * (c + 1);
  if (s >= 6) return "rouge";
  if (s >= 3) return "jaune";
  return "vert";
}

function choisir(id: string) {
  selection.value = selection.value === id ? null : id;
}

function placer(p: number, c: number) {
  if (!selection.value) return;
  positions[selection.value] = { p, c };
  selection.value = null;
}

function retirer() {
  if (!selection.value) return;
  positions[selection.value] = null;
  selection.value = null;
}

function reinitialiser() {
  for (const r of RISQUES) positions[r.id] = null;
  selection.value = null;
}

const risqueChoisi = computed(() => RISQUES.find((r) => r.id === selection.value) ?? null);

onMounted(() => {
  try {
    const brut = localStorage.getItem(props.storageKey);
    if (!brut) return;
    const data = JSON.parse(brut) as Record<string, Position>;
    for (const r of RISQUES) {
      const pos = data[r.id];
      if (pos && pos.p >= 0 && pos.p <= 2 && pos.c >= 0 && pos.c <= 2) positions[r.id] = pos;
    }
  } catch {
    /* stockage indisponible : on part d'une matrice vide */
  }
});

watch(positions, () => {
  try {
    localStorage.setItem(props.storageKey, JSON.stringify(positions));
  } catch {
    /* stockage indisponible : rien à faire */
  }
});
</script>

<template>
  <section class="mr">
    <p class="mr-consigne">
      1. Cliquez sur un risque pour le sélectionner. 2. Cliquez sur la case où vous le placez.
      Pour déplacer un risque déjà placé, cliquez sur son étiquette dans la matrice.
    </p>

    <div class="mr-grille-cadre">
      <div class="mr-axe-y" aria-hidden="true">Chances que ça arrive →</div>
      <div class="mr-grille" role="group" aria-label="Matrice des risques">
        <template v-for="p in [2, 1, 0]" :key="p">
          <div class="mr-entete-ligne">{{ PROBAS[p] }}</div>
          <div
            v-for="c in [0, 1, 2]"
            :key="c"
            class="mr-case"
            :class="['is-' + zone(p, c), { 'is-cible': selection }]"
            role="group"
            :tabindex="selection ? 0 : -1"
            :aria-label="'Probabilité ' + PROBAS[p].toLowerCase() + ', conséquences ' + CONSEQ[c].toLowerCase()"
            @click="placer(p, c)"
            @keydown.enter.prevent="placer(p, c)"
          >
            <button
              v-for="r in dans(p, c)"
              :key="r.id"
              type="button"
              class="mr-puce"
              :class="['is-' + r.origine, { 'is-choisi': selection === r.id }]"
              :title="r.texte"
              @click.stop="choisir(r.id)"
              @keydown.enter.stop
            >{{ r.id }}</button>
          </div>
        </template>
        <div></div>
        <div v-for="c in [0, 1, 2]" :key="'c' + c" class="mr-entete-col">{{ CONSEQ[c] }}</div>
      </div>
      <div class="mr-axe-x" aria-hidden="true">Conséquences si ça arrive →</div>
    </div>

    <div class="mr-barre">
      <span v-if="risqueChoisi" class="mr-choisi">
        <strong>{{ risqueChoisi.id }}</strong> sélectionné : cliquez sur une case.
        <button v-if="positions[risqueChoisi.id]" type="button" class="mr-lien" @click="retirer">Retirer de la matrice</button>
      </span>
      <span v-else class="mr-etat">{{ nbPlaces }} / {{ RISQUES.length }} risques placés</span>
      <button type="button" class="mr-reset" @click="reinitialiser">Recommencer</button>
    </div>

    <ul class="mr-liste">
      <li v-for="r in RISQUES" :key="r.id">
        <button
          type="button"
          class="mr-risque"
          :class="{ 'is-choisi': selection === r.id, 'is-place': positions[r.id] }"
          :aria-pressed="selection === r.id"
          @click="choisir(r.id)"
        >
          <span class="mr-puce mr-puce--liste" :class="'is-' + r.origine">{{ r.id }}</span>
          <span class="mr-texte">{{ r.texte }}</span>
          <span class="mr-origine">{{ r.origine === "T" ? "technique" : "organisationnel" }}</span>
        </button>
      </li>
    </ul>

    <p class="mr-note">Vos placements sont conservés dans ce navigateur seulement. Reportez-les dans la fiche de votre équipe.</p>
  </section>
</template>

<style scoped>
.mr {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.mr-consigne {
  margin: 0 0 0.75rem !important;
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
}
.mr-grille-cadre {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.25rem 0.5rem;
}
.mr-axe-y {
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  align-self: center;
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
.mr-axe-x {
  grid-column: 2;
  text-align: center;
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
.mr-grille {
  display: grid;
  grid-template-columns: 4.5rem repeat(3, minmax(0, 1fr));
  gap: 0.3rem;
}
.mr-entete-ligne {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 0.3rem;
  font-size: 0.75rem;
  font-weight: 600;
}
.mr-entete-col {
  text-align: center;
  font-size: 0.75rem;
  font-weight: 600;
}
.mr-case {
  display: flex;
  flex-wrap: wrap;
  align-content: flex-start;
  gap: 0.25rem;
  min-height: 4.5rem;
  padding: 0.35rem;
  border-radius: 0.5rem;
  border: 1px solid transparent;
  text-align: left;
  cursor: default;
}
.mr-case.is-cible {
  cursor: pointer;
  border-style: dashed;
  border-color: var(--vp-c-text-3);
}
.mr-case.is-vert {
  background: var(--vp-c-green-soft);
}
.mr-case.is-jaune {
  background: var(--vp-c-warning-soft);
}
.mr-case.is-rouge {
  background: var(--vp-c-red-soft);
}
.mr-puce {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 2.2rem;
  height: 1.5rem;
  padding: 0 0.35rem;
  border-radius: 0.4rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.72rem;
  font-weight: 700;
  cursor: pointer;
  flex-shrink: 0;
}
.mr-puce--liste {
  cursor: inherit;
}
.mr-puce.is-T {
  border-left: 3px solid var(--vp-c-indigo-2, var(--vp-c-brand-2));
}
.mr-puce.is-O {
  border-left: 3px solid var(--vp-c-purple-2, var(--vp-c-text-2));
}
.mr-puce.is-choisi {
  outline: 2px solid var(--vp-c-brand-1);
  outline-offset: 1px;
}
.mr-barre {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  margin: 0.8rem 0 0.5rem;
  padding-top: 0.6rem;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.85rem;
}
.mr-etat {
  color: var(--vp-c-text-2);
}
.mr-lien {
  margin-left: 0.4rem;
  color: var(--vp-c-brand-1);
  text-decoration: underline;
  font-size: 0.8rem;
}
.mr-reset {
  padding: 0.3rem 0.7rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.mr-reset:hover {
  border-color: var(--vp-c-brand-1);
}
.mr-liste {
  list-style: none !important;
  margin: 0 !important;
  padding: 0 !important;
  display: grid;
  gap: 0.3rem;
}
.mr-liste li {
  margin: 0 !important;
}
.mr-risque {
  display: flex;
  align-items: flex-start;
  gap: 0.55rem;
  width: 100%;
  padding: 0.45rem 0.6rem;
  border-radius: 0.55rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  text-align: left;
  font-size: 0.84rem;
  line-height: 1.45;
}
.mr-risque:hover {
  border-color: var(--vp-c-brand-2);
}
.mr-risque.is-choisi {
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
}
.mr-risque.is-place .mr-texte {
  color: var(--vp-c-text-2);
}
.mr-texte {
  flex: 1;
}
.mr-origine {
  flex-shrink: 0;
  font-size: 0.7rem;
  color: var(--vp-c-text-2);
}
.mr-note {
  margin: 0.6rem 0 0 !important;
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
@media (max-width: 520px) {
  .mr-grille {
    grid-template-columns: 3.4rem repeat(3, minmax(0, 1fr));
  }
  .mr-origine {
    display: none;
  }
}
</style>
