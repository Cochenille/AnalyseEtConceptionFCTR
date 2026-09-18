<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from "vue";

type ZoneKey = "pool" | "trajet" | "hors";
type Carte = { id: string; label: string; detail: string };

const CARTES: Carte[] = [
  { id: "contenus", label: "Contenus", detail: "textes, photos, menu, heures d'ouverture" },
  { id: "navigateur", label: "Navigateur", detail: "Chrome, Safari, Firefox…" },
  { id: "ssl", label: "Certificat SSL/TLS", detail: "le cadenas" },
  { id: "domaine", label: "Nom de domaine", detail: "bistro-exemple.ca" },
  { id: "service-externe", label: "Service externe", detail: "réservation, paiement, livraison" },
  { id: "hebergement", label: "Hébergement", detail: "le serveur où vit le site" },
  { id: "appareil", label: "Appareil", detail: "téléphone, tablette, ordinateur" },
  { id: "dns", label: "DNS", detail: "l'annuaire qui traduit le nom en adresse" },
  { id: "plateforme", label: "Plateforme", detail: "WordPress, Shopify, Wix, code maison…" },
  { id: "registraire", label: "Registraire", detail: "l'entreprise où on loue le nom de domaine" },
  { id: "courriel", label: "Courriel professionnel", detail: "info@bistro-exemple.ca" },
];

const props = withDefaults(
  defineProps<{
    cartes?: Carte[];
    storageKey?: string;
  }>(),
  { storageKey: "trajet-cartes-v1" }
);

const cartes = computed<Carte[]>(() => props.cartes ?? CARTES);
const parId = computed(() => Object.fromEntries(cartes.value.map((c) => [c.id, c])));

const ZONES: { key: ZoneKey; titre: string; aide: string }[] = [
  {
    key: "pool",
    titre: "Cartes à placer",
    aide: "Glissez chaque carte dans une des deux zones ci-dessous.",
  },
  {
    key: "trajet",
    titre: "Le trajet",
    aide: "De la cliente qui tape l'adresse jusqu'à la page affichée.",
  },
  {
    key: "hors",
    titre: "À côté du trajet",
    aide: "Les cartes qui ne se placent pas directement sur le trajet.",
  },
];

/* ---------------------------------------------- état */

const zones = reactive<Record<ZoneKey, string[]>>({
  pool: cartes.value.map((c) => c.id),
  trajet: [],
  hors: [],
});

const pret = ref(false);
const message = ref("");
const selection = ref<string | null>(null);

/* ---------------------------------------------- persistance */

function sauvegarder() {
  if (!pret.value) return;
  try {
    localStorage.setItem(
      props.storageKey,
      JSON.stringify({ zones: { ...zones } })
    );
  } catch {
    /* navigation privée, quota plein : on continue sans sauvegarde */
  }
}

function charger(): boolean {
  try {
    const brut = localStorage.getItem(props.storageKey);
    if (!brut) return false;
    const data = JSON.parse(brut);
    const connus = new Set(cartes.value.map((c) => c.id));
    const vus = new Set<string>();
    for (const k of ["pool", "trajet", "hors"] as ZoneKey[]) {
      const liste = Array.isArray(data?.zones?.[k]) ? data.zones[k] : [];
      zones[k] = liste.filter((id: string) => {
        if (!connus.has(id) || vus.has(id)) return false;
        vus.add(id);
        return true;
      });
    }
    // Une carte ajoutée depuis la dernière sauvegarde retombe dans la banque.
    zones.pool.push(...cartes.value.map((c) => c.id).filter((id) => !vus.has(id)));
    return true;
  } catch {
    return false;
  }
}

function melanger() {
  const ids = cartes.value.map((c) => c.id);
  for (let i = ids.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [ids[i], ids[j]] = [ids[j], ids[i]];
  }
  zones.pool = ids;
  zones.trajet = [];
  zones.hors = [];
}

onMounted(() => {
  // Le mélange se fait après le montage : le rendu serveur et le premier rendu
  // client partent du même ordre, donc pas d'erreur d'hydratation.
  if (!charger()) melanger();
  pret.value = true;
});

watch(zones, sauvegarder, { deep: true });

/* ---------------------------------------------- déplacements */

function deplacer(id: string, vers: ZoneKey, index?: number) {
  for (const k of ["pool", "trajet", "hors"] as ZoneKey[]) {
    const i = zones[k].indexOf(id);
    if (i !== -1) zones[k].splice(i, 1);
  }
  const cibleListe = zones[vers];
  const pos = index === undefined ? cibleListe.length : Math.max(0, Math.min(index, cibleListe.length));
  cibleListe.splice(pos, 0, id);
}

function zoneDe(id: string): ZoneKey {
  for (const k of ["pool", "trajet", "hors"] as ZoneKey[]) if (zones[k].includes(id)) return k;
  return "pool";
}

/* ---------------------------------------------- glisser-déposer (souris + tactile) */

const SEUIL = 6;
const racine = ref<HTMLElement | null>(null);
const drag = ref<{ id: string; x: number; y: number; label: string } | null>(null);
const cible = ref<{ zone: ZoneKey; index: number } | null>(null);
const repere = ref<{ zone: ZoneKey; left: number; top: number; height: number } | null>(null);

let depart: { id: string; x: number; y: number; pointerId: number } | null = null;
let glissementRecent = false;

/* Défilement automatique quand le pointeur approche le haut ou le bas de
   l'écran : sans ça, une zone hors de l'écran est inatteignable. */
const MARGE = 90;
let raf = 0;
let vitesse = 0;

function boucleDefilement() {
  if (!drag.value) {
    raf = 0;
    return;
  }
  if (vitesse !== 0) {
    window.scrollBy(0, vitesse);
    calculerCible(drag.value.x, drag.value.y);
  }
  raf = requestAnimationFrame(boucleDefilement);
}

function surPointerDown(e: PointerEvent, id: string) {
  const el = e.target as HTMLElement;
  if (el.closest("input, select, textarea, button, a")) return;
  // Sur écran tactile, seule la poignée démarre un glissement : le reste de la
  // carte doit continuer à faire défiler la page.
  if (e.pointerType !== "mouse" && !el.closest("[data-poignee]")) return;
  if (e.pointerType === "mouse" && e.button !== 0) return;
  depart = { id, x: e.clientX, y: e.clientY, pointerId: e.pointerId };
  window.addEventListener("pointermove", surPointerMove, { passive: false });
  window.addEventListener("pointerup", surPointerUp);
  window.addEventListener("pointercancel", surPointerUp);
}

function surPointerMove(e: PointerEvent) {
  if (!depart || e.pointerId !== depart.pointerId) return;
  if (!drag.value) {
    if (Math.hypot(e.clientX - depart.x, e.clientY - depart.y) < SEUIL) return;
    drag.value = { id: depart.id, x: e.clientX, y: e.clientY, label: parId.value[depart.id].label };
    if (!raf) raf = requestAnimationFrame(boucleDefilement);
  }
  e.preventDefault();
  drag.value.x = e.clientX;
  drag.value.y = e.clientY;
  const h = window.innerHeight;
  vitesse =
    e.clientY < MARGE
      ? -Math.ceil((MARGE - e.clientY) / 5)
      : e.clientY > h - MARGE
        ? Math.ceil((e.clientY - (h - MARGE)) / 5)
        : 0;
  calculerCible(e.clientX, e.clientY);
}

function surPointerUp() {
  window.removeEventListener("pointermove", surPointerMove);
  window.removeEventListener("pointerup", surPointerUp);
  window.removeEventListener("pointercancel", surPointerUp);
  if (drag.value) {
    if (cible.value) deplacer(drag.value.id, cible.value.zone, cible.value.index);
    // Le « click » qui suit le glissement ne doit pas changer la sélection.
    glissementRecent = true;
    setTimeout(() => (glissementRecent = false), 0);
  }
  if (raf) cancelAnimationFrame(raf);
  raf = 0;
  vitesse = 0;
  drag.value = null;
  cible.value = null;
  repere.value = null;
  depart = null;
}

/* ---------------------------------------------- sélection au clic (surtout tactile) */

function surClic(id: string) {
  if (glissementRecent) return;
  selection.value = selection.value === id ? null : id;
}

function envoyer(vers: ZoneKey) {
  if (!selection.value) return;
  deplacer(selection.value, vers);
  annoncer(`« ${parId.value[selection.value].label} » déplacée vers « ${titreZone(vers)} ».`);
}

function decaler(pas: -1 | 1) {
  const id = selection.value;
  if (!id) return;
  const z = zoneDe(id);
  const i = zones[z].indexOf(id);
  deplacer(id, z, Math.max(0, Math.min(zones[z].length - 1, i + pas)));
}

function titreZone(k: ZoneKey): string {
  return ZONES.find((z) => z.key === k)!.titre;
}

function calculerCible(x: number, y: number) {
  const sous = document.elementFromPoint(x, y) as HTMLElement | null;
  const zoneEl = sous?.closest("[data-zone]") as HTMLElement | null;
  if (!zoneEl || !racine.value?.contains(zoneEl)) {
    cible.value = null;
    repere.value = null;
    return;
  }
  const zone = zoneEl.dataset.zone as ZoneKey;
  const cartesEl = Array.from(zoneEl.querySelectorAll<HTMLElement>("[data-carte-id]")).filter(
    (el) => el.dataset.carteId !== drag.value?.id
  );

  let index = cartesEl.length;
  for (let i = 0; i < cartesEl.length; i++) {
    const r = cartesEl[i].getBoundingClientRect();
    if (y < r.bottom && x < r.left + r.width / 2) {
      index = i;
      break;
    }
  }

  cible.value = { zone, index };

  const rz = zoneEl.getBoundingClientRect();
  if (cartesEl.length === 0) {
    repere.value = null;
  } else if (index < cartesEl.length) {
    const r = cartesEl[index].getBoundingClientRect();
    repere.value = { zone, left: r.left - rz.left - 5, top: r.top - rz.top, height: r.height };
  } else {
    const r = cartesEl[cartesEl.length - 1].getBoundingClientRect();
    repere.value = { zone, left: r.right - rz.left + 2, top: r.top - rz.top, height: r.height };
  }
}

onBeforeUnmount(surPointerUp);

/* ---------------------------------------------- clavier */

const ORDRE: ZoneKey[] = ["pool", "trajet", "hors"];

function surClavier(e: KeyboardEvent, id: string) {
  const z = zoneDe(id);
  const i = zones[z].indexOf(id);
  let bouge = true;

  if (e.key === "ArrowLeft") deplacer(id, z, Math.max(0, i - 1));
  else if (e.key === "ArrowRight") deplacer(id, z, Math.min(zones[z].length - 1, i + 1));
  else if (e.key === "ArrowDown") deplacer(id, ORDRE[Math.min(ORDRE.length - 1, ORDRE.indexOf(z) + 1)]);
  else if (e.key === "ArrowUp") deplacer(id, ORDRE[Math.max(0, ORDRE.indexOf(z) - 1)]);
  else bouge = false;

  if (!bouge) return;
  e.preventDefault();
  nextTick(() => {
    racine.value?.querySelector<HTMLElement>('[data-carte-id="' + id + '"]')?.focus();
  });
}

let minuterie: ReturnType<typeof setTimeout> | undefined;
function annoncer(t: string) {
  message.value = t;
  clearTimeout(minuterie);
  minuterie = setTimeout(() => (message.value = ""), 4000);
}
onBeforeUnmount(() => clearTimeout(minuterie));
</script>

<template>
  <section ref="racine" class="tc" :class="{ 'tc--drag': !!drag }">
    <p class="tc-message" :class="{ 'is-vide': !message }" role="status" aria-live="polite">
      {{ message || "&nbsp;" }}
    </p>

    <p class="tc-aide">
      <strong>Deux façons de déplacer une carte.</strong> La glisser jusqu'à la zone voulue (à la souris,
      ou par la poignée <span aria-hidden="true">⠿</span> sur téléphone), ou la
      <strong>toucher pour la sélectionner</strong> puis choisir sa destination dans la barre qui apparaît en bas.
      Au clavier : <kbd>Tab</kbd> pour atteindre une carte, <kbd>←</kbd> <kbd>→</kbd> pour la déplacer dans sa zone,
      <kbd>↑</kbd> <kbd>↓</kbd> pour changer de zone.
    </p>

    <div
      v-for="z in ZONES"
      :key="z.key"
      class="tc-zone"
      :class="['tc-zone--' + z.key, { 'is-cible': cible?.zone === z.key }]"
    >
      <div class="tc-zone-tete">
        <h3 class="tc-zone-titre">
          {{ z.titre }}
          <span class="tc-compte">{{ zones[z.key].length }}</span>
        </h3>
        <p class="tc-zone-aide">{{ z.aide }}</p>
      </div>

      <div class="tc-piste" :data-zone="z.key">
        <p v-if="zones[z.key].length === 0" class="tc-vide">Déposez des cartes ici.</p>

        <template v-for="(id, i) in zones[z.key]" :key="id">
          <span v-if="z.key === 'trajet' && i > 0" class="tc-fleche" aria-hidden="true">→</span>

          <div
            class="tc-carte"
            :class="{ 'is-prise': drag?.id === id, 'is-choisie': selection === id }"
            :data-carte-id="id"
            tabindex="0"
            role="button"
            :aria-pressed="selection === id"
            :aria-label="
              parId[id].label + '. Zone : ' + z.titre + ', position ' + (i + 1) + ' sur ' + zones[z.key].length + '.'
            "
            @pointerdown="surPointerDown($event, id)"
            @click="surClic(id)"
            @keydown="surClavier($event, id)"
          >
            <span v-if="z.key === 'trajet'" class="tc-rang">{{ i + 1 }}</span>
            <span class="tc-poignee" data-poignee aria-hidden="true">⠿</span>
            <span class="tc-texte">
              <strong>{{ parId[id].label }}</strong>
              <em>{{ parId[id].detail }}</em>
            </span>
          </div>
        </template>

        <span
          v-if="repere && repere.zone === z.key"
          class="tc-repere"
          :style="{ left: repere.left + 'px', top: repere.top + 'px', height: repere.height + 'px' }"
          aria-hidden="true"
        />
      </div>
    </div>

    <!-- Barre de déplacement, visible quand une carte est sélectionnée -->
    <div v-if="selection" class="tc-selection">
      <span class="tc-selection-nom">
        <span class="tc-selection-etiquette">Carte choisie</span>
        <strong>{{ parId[selection].label }}</strong>
      </span>

      <span class="tc-selection-boutons">
        <button
          v-for="z in ZONES"
          :key="z.key"
          type="button"
          class="tc-btn tc-btn--sel"
          :class="{ 'is-actif': zoneDe(selection) === z.key }"
          :disabled="zoneDe(selection) === z.key"
          @click="envoyer(z.key)"
        >
          {{ z.titre }}
        </button>

        <span class="tc-selection-sep" aria-hidden="true"></span>

        <button type="button" class="tc-btn tc-btn--icone" aria-label="Reculer la carte" @click="decaler(-1)">
          ←
        </button>
        <button type="button" class="tc-btn tc-btn--icone" aria-label="Avancer la carte" @click="decaler(1)">
          →
        </button>
        <button
          type="button"
          class="tc-btn tc-btn--icone"
          aria-label="Désélectionner la carte"
          @click="selection = null"
        >
          ✕
        </button>
      </span>
    </div>

    <!-- Carte fantôme suivant le pointeur -->
    <Teleport to="body">
      <div
        v-if="drag"
        class="tc-fantome"
        :style="{ transform: 'translate(' + drag.x + 'px, ' + drag.y + 'px)' }"
        aria-hidden="true"
      >
        {{ drag.label }}
      </div>
    </Teleport>
  </section>
</template>

<style scoped>
.tc {
  margin: 1.5rem 0 2rem;
}
.tc--drag,
.tc--drag * {
  cursor: grabbing !important;
  user-select: none;
}

/* Barre d'outils */
.tc-btn {
  padding: 0.4rem 0.8rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 0.8125rem;
  font-weight: 500;
  transition: border-color 0.15s, background-color 0.15s;
}
.tc-btn:hover {
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-bg-soft);
}

.tc-message {
  min-height: 1.25rem;
  margin: 0.5rem 0 0;
  font-size: 0.8125rem;
  color: var(--vp-c-brand-1);
}
.tc-message.is-vide {
  visibility: hidden;
}

.tc-aide {
  margin: 0.5rem 0 1rem;
  font-size: 0.8125rem;
  line-height: 1.6;
  color: var(--vp-c-text-2);
}
.tc-aide kbd {
  padding: 0.05rem 0.3rem;
  border: 1px solid var(--vp-c-divider);
  border-bottom-width: 2px;
  border-radius: 0.3rem;
  background: var(--vp-c-bg-soft);
  font-size: 0.75rem;
}

/* Zones */
.tc-zone {
  margin-bottom: 1rem;
  padding: 0.875rem 1rem 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
  transition: border-color 0.15s, box-shadow 0.15s;
}
.tc-zone.is-cible {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--vp-c-brand-1) 18%, transparent);
}
.tc-zone-tete {
  margin-bottom: 0.75rem;
}
.tc-zone-titre {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}
.tc-compte {
  padding: 0.05rem 0.45rem;
  border-radius: 999px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--vp-c-text-2);
}
.tc-zone-aide {
  margin: 0.15rem 0 0;
  font-size: 0.8125rem;
  color: var(--vp-c-text-2);
}

.tc-piste {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;
  gap: 0.5rem;
  min-height: 3.75rem;
  padding: 0.5rem;
  border-radius: 0.65rem;
  border: 1px dashed var(--vp-c-divider);
  background: var(--vp-c-bg);
}
.tc-vide {
  margin: auto;
  font-size: 0.8125rem;
  color: var(--vp-c-text-3);
}

/* Cartes */
.tc-carte {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  max-width: 100%;
  padding: 0.5rem 0.7rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.65rem;
  background: var(--vp-c-bg-soft);
  cursor: grab;
  transition: border-color 0.15s, transform 0.15s, box-shadow 0.15s;
}
.tc-carte:hover {
  border-color: var(--vp-c-brand-1);
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgb(0 0 0 / 8%);
}
.tc-carte:focus-visible {
  outline: 2px solid var(--vp-c-brand-1);
  outline-offset: 2px;
}
.tc-carte.is-prise {
  opacity: 0.35;
}
.tc-carte.is-choisie {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--vp-c-brand-1) 30%, transparent);
}
.tc-rang {
  display: grid;
  place-items: center;
  flex: none;
  width: 1.35rem;
  height: 1.35rem;
  border-radius: 999px;
  background: var(--vp-c-brand-1);
  color: var(--vp-c-bg);
  font-size: 0.75rem;
  font-weight: 600;
}
.tc-poignee {
  flex: none;
  padding: 0.35rem 0.1rem;
  color: var(--vp-c-text-3);
  font-size: 0.95rem;
  line-height: 1;
  touch-action: none;
  cursor: grab;
}
.tc-texte {
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.tc-texte strong {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}
.tc-texte em {
  font-style: normal;
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
}
.tc-fleche {
  align-self: center;
  color: var(--vp-c-text-3);
  font-size: 1rem;
}

.tc-repere {
  position: absolute;
  width: 3px;
  border-radius: 2px;
  background: var(--vp-c-brand-1);
  pointer-events: none;
}

.tc-fantome {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 999;
  margin: -1.1rem 0 0 -3rem;
  padding: 0.45rem 0.75rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-brand-1);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 0.875rem;
  font-weight: 600;
  box-shadow: 0 6px 18px rgb(0 0 0 / 18%);
  pointer-events: none;
}

/* Barre de sélection */
.tc-selection {
  position: sticky;
  bottom: 0.5rem;
  z-index: 10;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 0.75rem;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.75rem;
  padding: 0.6rem 0.75rem;
  border: 1px solid var(--vp-c-brand-1);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-elv, var(--vp-c-bg));
  box-shadow: 0 6px 20px rgb(0 0 0 / 15%);
}
.tc-selection-nom {
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.tc-selection-etiquette {
  font-size: 0.6875rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--vp-c-text-3);
}
.tc-selection-nom strong {
  font-size: 0.875rem;
  color: var(--vp-c-text-1);
}
.tc-selection-boutons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
  align-items: center;
}
.tc-btn--sel.is-actif,
.tc-btn--sel:disabled {
  opacity: 0.45;
  cursor: default;
}
.tc-btn--sel:disabled:hover {
  border-color: var(--vp-c-divider);
  background: var(--vp-c-bg);
}
.tc-btn--icone {
  min-width: 2rem;
  padding: 0.35rem 0.5rem;
  text-align: center;
}
.tc-selection-sep {
  width: 1px;
  height: 1.25rem;
  background: var(--vp-c-divider);
}

/* Étape 2 */

@media (max-width: 640px) {
  .tc-carte {
    flex: 1 1 100%;
  }
}

@media print {
  .tc-aide,
  .tc-message,
  .tc-selection {
    display: none;
  }
}
</style>
