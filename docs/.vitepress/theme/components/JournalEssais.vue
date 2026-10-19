<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from "vue";
import BoutonCopier from "./BoutonCopier.vue";

type Statut = "" | "reussi" | "echoue" | "nv";
type Resultat = { statut: Statut; mesure: string; note: string };
type Essai = { besoin: string; critere: string };

const STATUTS: { cle: Exclude<Statut, "">; titre: string; symbole: string }[] = [
  { cle: "reussi", titre: "Réussi", symbole: "✓" },
  { cle: "echoue", titre: "Échoué", symbole: "✗" },
  { cle: "nv", titre: "Non vérifiable", symbole: "?" },
];
const QUESTIONS = ["Q1", "Q2", "Q3", "Q4", "Q5"];
const MIN_ESSAIS = 1;
const MAX_ESSAIS = 10;
const NB_OUTILS = 3;

const props = withDefaults(defineProps<{ storageKey?: string }>(), {
  storageKey: "asm-journal-essais",
});

const resultatVide = (): Resultat => ({ statut: "", mesure: "", note: "" });
const ligneVide = () => Array.from({ length: NB_OUTILS }, resultatVide);

const etat = reactive({
  equipe: "",
  question: "",
  outils: ["", "", ""] as string[],
  essais: Array.from({ length: 6 }, () => ({ besoin: "", critere: "" })) as Essai[],
  resultats: Array.from({ length: 6 }, ligneVide) as Resultat[][],
  actif: 0,
});

const nomOutil = (o: number) => etat.outils[o].trim() || `Outil ${o + 1}`;
const titreStatut = (s: Statut) => STATUTS.find((x) => x.cle === s)?.titre ?? "À faire";
const symbole = (s: Statut) => STATUTS.find((x) => x.cle === s)?.symbole ?? "·";

function slug(s: string) {
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^A-Za-z0-9]+/g, "");
}
const nomCapture = (e: number, o: number) =>
  `${etat.question || "QX"}-${slug(etat.outils[o]) || "Outil" + (o + 1)}-E${e + 1}-01.png`;

function ajouterEssai() {
  if (etat.essais.length >= MAX_ESSAIS) return;
  etat.essais.push({ besoin: "", critere: "" });
  etat.resultats.push(ligneVide());
}
function retirerEssai() {
  if (etat.essais.length <= MIN_ESSAIS) return;
  const n = etat.essais.length - 1;
  const rempli = etat.resultats[n].some((r) => r.statut || r.mesure || r.note) || etat.essais[n].besoin || etat.essais[n].critere;
  if (rempli && !confirm(`Retirer l'essai E${n + 1} et ses résultats ?`)) return;
  etat.essais.pop();
  etat.resultats.pop();
}

// Bilan par outil
const bilan = computed(() =>
  Array.from({ length: NB_OUTILS }, (_, o) => {
    const r = etat.resultats.map((ligne) => ligne[o].statut);
    return {
      reussi: r.filter((s) => s === "reussi").length,
      echoue: r.filter((s) => s === "echoue").length,
      nv: r.filter((s) => s === "nv").length,
      faits: r.filter((s) => s !== "").length,
    };
  }),
);
const texteBilan = (o: number) => {
  const b = bilan.value[o];
  return `${b.reussi} réussi(s), ${b.echoue} échoué(s), ${b.nv} non vérifiable(s) sur ${etat.essais.length}`;
};

// Chronomètre : un seul à la fois
const chrono = reactive({ cle: "", debut: 0 });
const maintenant = ref(Date.now());
let minuterie: ReturnType<typeof setInterval> | undefined;

const cle = (e: number, o: number) => `${e}-${o}`;
const ecoule = computed(() => (chrono.cle ? Math.max(0, maintenant.value - chrono.debut) : 0));
function formatDuree(ms: number) {
  const s = Math.round(ms / 1000);
  const m = Math.floor(s / 60);
  return m > 0 ? `${m} min ${String(s % 60).padStart(2, "0")} s` : `${s} s`;
}
function demarrer(e: number, o: number) {
  chrono.cle = cle(e, o);
  chrono.debut = Date.now();
  maintenant.value = chrono.debut;
  clearInterval(minuterie);
  minuterie = setInterval(() => (maintenant.value = Date.now()), 250);
}
function arreter(e: number, o: number) {
  const duree = formatDuree(Date.now() - chrono.debut);
  const r = etat.resultats[e][o];
  r.mesure = r.mesure.trim() ? `${r.mesure.trim()}; ${duree}` : duree;
  chrono.cle = "";
  clearInterval(minuterie);
}
function annulerChrono() {
  chrono.cle = "";
  clearInterval(minuterie);
}

// Copie : texte brut et tableau HTML (se colle comme un tableau dans Word)
const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const entete = () =>
  `Lab 04 — Résultats des essais${etat.equipe.trim() ? " — Équipe " + etat.equipe.trim() : ""}${etat.question ? " — " + etat.question : ""}`;

function texteReponses() {
  const outils = Array.from({ length: NB_OUTILS }, (_, o) => nomOutil(o));
  return [
    entete(),
    `Outils : ${outils.join(" · ")}`,
    ...etat.essais.map((es, e) =>
      [
        `E${e + 1} — Besoin vérifié : ${es.besoin.trim() || "—"}`,
        `     Réussi si : ${es.critere.trim() || "—"}`,
        ...outils.map((nom, o) => {
          const r = etat.resultats[e][o];
          const morceaux = [titreStatut(r.statut), r.mesure.trim(), r.note.trim()].filter(Boolean);
          return `     ${nom} : ${morceaux.join(" — ")}`;
        }),
      ].join("\n"),
    ),
    "Bilan :\n" + outils.map((nom, o) => `     ${nom} : ${texteBilan(o)}`).join("\n"),
  ].join("\n\n");
}

function htmlReponses() {
  const outils = Array.from({ length: NB_OUTILS }, (_, o) => nomOutil(o));
  const th = (t: string) => `<th style="background:#E0E7FF;text-align:left">${esc(t)}</th>`;
  const lignes = etat.essais.map((es, e) => {
    const cellules = outils.map((_, o) => {
      const r = etat.resultats[e][o];
      const morceaux = [`<b>${esc(titreStatut(r.statut))}</b>`];
      if (r.mesure.trim()) morceaux.push(esc(r.mesure.trim()));
      if (r.note.trim()) morceaux.push(`<i>${esc(r.note.trim())}</i>`);
      return `<td>${morceaux.join("<br>")}</td>`;
    });
    return `<tr><td>E${e + 1}</td><td>${esc(es.besoin.trim())}</td><td>${esc(es.critere.trim())}</td>${cellules.join("")}</tr>`;
  });
  const bilanLigne = `<tr><td colspan="3"><b>Bilan</b></td>${outils.map((_, o) => `<td>${esc(texteBilan(o))}</td>`).join("")}</tr>`;
  return [
    `<p><b>${esc(entete())}</b></p>`,
    `<table border="1" cellpadding="5" style="border-collapse:collapse">`,
    `<tr>${th("#")}${th("Besoin vérifié")}${th("Réussi si…")}${outils.map(th).join("")}</tr>`,
    ...lignes,
    bilanLigne,
    `</table>`,
  ].join("");
}

function reinitialiser() {
  if (!confirm("Effacer tout le journal (plan et résultats) ? Avez-vous copié vos résultats ?")) return;
  annulerChrono();
  etat.equipe = "";
  etat.question = "";
  etat.outils.splice(0, NB_OUTILS, "", "", "");
  etat.essais.splice(0, etat.essais.length, ...Array.from({ length: 6 }, () => ({ besoin: "", critere: "" })));
  etat.resultats.splice(0, etat.resultats.length, ...Array.from({ length: 6 }, ligneVide));
  etat.actif = 0;
}

onMounted(() => {
  try {
    const data = JSON.parse(localStorage.getItem(props.storageKey) ?? "null");
    if (!data || !Array.isArray(data.essais) || data.essais.length < MIN_ESSAIS) return;
    etat.equipe = String(data.equipe ?? "");
    etat.question = QUESTIONS.includes(data.question) ? data.question : "";
    etat.outils.splice(0, NB_OUTILS, ...Array.from({ length: NB_OUTILS }, (_, o) => String(data.outils?.[o] ?? "")));
    const essais = data.essais.slice(0, MAX_ESSAIS);
    etat.essais.splice(0, etat.essais.length, ...essais.map((x: any) => ({ besoin: String(x?.besoin ?? ""), critere: String(x?.critere ?? "") })));
    etat.resultats.splice(
      0,
      etat.resultats.length,
      ...essais.map((_: unknown, e: number) =>
        Array.from({ length: NB_OUTILS }, (_, o) => {
          const r = data.resultats?.[e]?.[o] ?? {};
          return {
            statut: STATUTS.some((s) => s.cle === r.statut) ? r.statut : "",
            mesure: String(r.mesure ?? ""),
            note: String(r.note ?? ""),
          } as Resultat;
        }),
      ),
    );
    etat.actif = Number.isInteger(data.actif) && data.actif >= 0 && data.actif < NB_OUTILS ? data.actif : 0;
  } catch {
    /* stockage indisponible : on part d'un journal vide */
  }
});

watch(etat, () => {
  try {
    localStorage.setItem(props.storageKey, JSON.stringify(etat));
  } catch {
    /* stockage indisponible : rien à faire */
  }
});

onBeforeUnmount(() => clearInterval(minuterie));
</script>

<template>
  <section class="je">
    <!-- 1. Le plan -->
    <h4 class="je-etape"><span>1</span> Votre plan (repris du Lab 03)</h4>
    <div class="je-ident">
      <label class="je-label">
        Équipe n°
        <input v-model="etat.equipe" class="je-input je-court" inputmode="numeric" />
      </label>
      <label class="je-label">
        Question
        <select v-model="etat.question" class="je-input je-court">
          <option value="">—</option>
          <option v-for="q in QUESTIONS" :key="q" :value="q">{{ q }}</option>
        </select>
      </label>
      <label v-for="(_, o) in etat.outils" :key="o" class="je-label je-outil-nom">
        Outil {{ o + 1 }}
        <input v-model="etat.outils[o]" class="je-input" :placeholder="o === 2 ? 'facultatif' : 'nom de l’outil'" />
      </label>
    </div>

    <div class="je-plan">
      <div class="je-plan-tete" aria-hidden="true">
        <span>#</span><span>Besoin vérifié / scénario (court)</span><span>Réussi si…</span>
      </div>
      <div v-for="(es, e) in etat.essais" :key="e" class="je-plan-ligne">
        <span class="je-num">E{{ e + 1 }}</span>
        <input v-model="es.besoin" class="je-input" placeholder="Besoin vérifié" :aria-label="'Besoin vérifié, essai ' + (e + 1)" />
        <input v-model="es.critere" class="je-input" placeholder="Réussi si…" :aria-label="'Critère de réussite, essai ' + (e + 1)" />
      </div>
      <div class="je-plan-actions">
        <button type="button" class="je-petit" :disabled="etat.essais.length >= MAX_ESSAIS" @click="ajouterEssai">+ Ajouter un essai</button>
        <button type="button" class="je-petit" :disabled="etat.essais.length <= MIN_ESSAIS" @click="retirerEssai">− Retirer le dernier</button>
      </div>
    </div>

    <!-- 2. Les essais -->
    <h4 class="je-etape"><span>2</span> Les essais, outil par outil</h4>
    <div class="je-onglets" role="tablist" aria-label="Outil essayé">
      <button
        v-for="(_, o) in etat.outils"
        :key="o"
        type="button"
        role="tab"
        class="je-onglet"
        :aria-selected="etat.actif === o"
        @click="etat.actif = o"
      >
        {{ nomOutil(o) }}
        <small>{{ bilan[o].faits }}/{{ etat.essais.length }}</small>
      </button>
    </div>

    <ol class="je-cartes">
      <li v-for="(es, e) in etat.essais" :key="e" class="je-carte" :class="'is-' + (etat.resultats[e][etat.actif].statut || 'vide')">
        <p class="je-carte-titre"><strong>E{{ e + 1 }}</strong> · {{ es.besoin.trim() || "Besoin à préciser dans le plan" }}</p>
        <p class="je-critere"><strong>Réussi si :</strong> {{ es.critere.trim() || "—" }}</p>

        <div class="je-ligne">
          <div class="je-statuts" role="group" :aria-label="'Résultat de l’essai E' + (e + 1)">
            <button
              v-for="s in STATUTS"
              :key="s.cle"
              type="button"
              class="je-statut"
              :class="'is-' + s.cle"
              :aria-pressed="etat.resultats[e][etat.actif].statut === s.cle"
              @click="etat.resultats[e][etat.actif].statut = etat.resultats[e][etat.actif].statut === s.cle ? '' : s.cle"
            >
              {{ s.symbole }} {{ s.titre }}
            </button>
          </div>
          <div class="je-chrono">
            <template v-if="chrono.cle === cle(e, etat.actif)">
              <span class="je-temps" aria-live="off">{{ formatDuree(ecoule) }}</span>
              <button type="button" class="je-petit is-principal" @click="arreter(e, etat.actif)">Arrêter et noter</button>
              <button type="button" class="je-petit" @click="annulerChrono">Annuler</button>
            </template>
            <button v-else type="button" class="je-petit" @click="demarrer(e, etat.actif)">⏱ Chronomètre</button>
          </div>
        </div>

        <div class="je-saisies">
          <label class="je-label">
            Mesure (temps, clics, poids, score…)
            <input v-model="etat.resultats[e][etat.actif].mesure" class="je-input" />
          </label>
          <label class="je-label">
            Ce qu'on a observé (imprévu, aide demandée, ou pourquoi non vérifiable)
            <textarea v-model="etat.resultats[e][etat.actif].note" class="je-input" rows="2" />
          </label>
        </div>
        <p class="je-capture">Capture : <code>{{ nomCapture(e, etat.actif) }}</code></p>
      </li>
    </ol>

    <!-- 3. Le tableau -->
    <h4 class="je-etape"><span>3</span> Le tableau des résultats</h4>
    <div class="je-tableau">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Réussi si…</th>
            <th v-for="(_, o) in etat.outils" :key="o">{{ nomOutil(o) }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(es, e) in etat.essais" :key="e">
            <td>E{{ e + 1 }}</td>
            <td class="je-td-critere">{{ es.critere.trim() || "—" }}</td>
            <td v-for="(_, o) in etat.outils" :key="o" :class="'is-' + (etat.resultats[e][o].statut || 'vide')">
              <span class="je-symbole">{{ symbole(etat.resultats[e][o].statut) }}</span>
              {{ etat.resultats[e][o].mesure }}
            </td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="2">Réussis / échoués / non vérifiables</td>
            <td v-for="(b, o) in bilan" :key="o">{{ b.reussi }} / {{ b.echoue }} / {{ b.nv }}</td>
          </tr>
        </tfoot>
      </table>
    </div>

    <p class="je-rappel">
      Le journal reste dans ce navigateur, mais il peut disparaître si la cache est vidée. <strong>Copiez-le souvent</strong> :
      collé dans Word, il devient un tableau, prêt pour la fiche et l'annexe A du rapport.
    </p>
    <div class="je-pied">
      <BoutonCopier :texte="texteReponses" :html="htmlReponses" libelle="Copier le tableau des résultats" />
      <button type="button" class="je-petit" @click="reinitialiser">Tout effacer</button>
    </div>
  </section>
</template>

<style scoped>
.je {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
  font-size: 0.875rem;
}
.je-etape {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 1.2rem 0 0.6rem !important;
  font-size: 0.95rem;
}
.je-etape:first-child { margin-top: 0 !important; }
.je-etape span {
  display: grid;
  place-items: center;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: var(--vp-c-brand-1);
  color: var(--vp-c-white);
  font-size: 0.8rem;
}
.je-label {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
.je-input {
  width: 100%;
  padding: 0.35rem 0.55rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.5rem;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font: inherit;
  font-size: 0.85rem;
  font-weight: 400;
}
textarea.je-input { resize: vertical; }
.je-input:focus { outline: none; border-color: var(--vp-c-brand-1); }
.je-ident {
  display: grid;
  grid-template-columns: 5.5rem 5.5rem repeat(3, minmax(0, 1fr));
  gap: 0.5rem;
}
.je-plan {
  display: grid;
  gap: 0.35rem;
  margin-top: 0.75rem;
}
.je-plan-tete,
.je-plan-ligne {
  display: grid;
  grid-template-columns: 2.2rem 1fr 1fr;
  gap: 0.4rem;
  align-items: center;
}
.je-plan-tete {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
.je-num { font-weight: 700; color: var(--vp-c-brand-1); }
.je-plan-actions { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.2rem; }
.je-petit {
  padding: 0.25rem 0.65rem;
  border-radius: 0.6rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.78rem;
}
.je-petit:hover:not(:disabled) { border-color: var(--vp-c-brand-1); }
.je-petit:disabled { opacity: 0.45; cursor: not-allowed; }
.je-petit.is-principal { border-color: var(--vp-c-brand-1); color: var(--vp-c-brand-1); font-weight: 600; }
.je-onglets {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}
.je-onglet {
  display: inline-flex;
  align-items: baseline;
  gap: 0.4rem;
  padding: 0.35rem 0.8rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.6rem 0.6rem 0 0;
  background: var(--vp-c-bg);
  font-weight: 600;
}
.je-onglet small { font-weight: 400; color: var(--vp-c-text-2); }
.je-onglet[aria-selected="true"] {
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
}
.je-cartes {
  list-style: none !important;
  margin: 0 !important;
  padding: 0.6rem !important;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0 0.65rem 0.65rem 0.65rem;
  background: var(--vp-c-bg);
  display: grid;
  gap: 0.5rem;
}
.je-carte {
  margin: 0 !important;
  padding: 0.65rem 0.75rem;
  border: 1px solid var(--vp-c-divider);
  border-left: 4px solid var(--vp-c-divider);
  border-radius: 0.6rem;
  background: var(--vp-c-bg-soft);
}
.je-carte.is-reussi { border-left-color: var(--vp-c-green-2); }
.je-carte.is-echoue { border-left-color: var(--vp-c-red-2); }
.je-carte.is-nv { border-left-color: var(--vp-c-yellow-2); }
.je-carte-titre { margin: 0 !important; line-height: 1.4; }
.je-critere { margin: 0.15rem 0 0 !important; font-size: 0.8rem; color: var(--vp-c-text-2); }
.je-ligne {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 0.4rem;
  margin-top: 0.45rem;
}
.je-statuts, .je-chrono { display: flex; flex-wrap: wrap; align-items: center; gap: 0.35rem; }
.je-statut {
  padding: 0.22rem 0.65rem;
  border-radius: 999px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.78rem;
  font-weight: 500;
}
.je-statut:hover { border-color: var(--vp-c-brand-1); }
.je-statut.is-reussi[aria-pressed="true"] { border-color: var(--vp-c-green-2); background: var(--vp-c-green-soft); color: var(--vp-c-green-1); }
.je-statut.is-echoue[aria-pressed="true"] { border-color: var(--vp-c-red-2); background: var(--vp-c-red-soft); color: var(--vp-c-red-1); }
.je-statut.is-nv[aria-pressed="true"] { border-color: var(--vp-c-yellow-2); background: var(--vp-c-yellow-soft); color: var(--vp-c-yellow-1); }
.je-temps {
  font-family: var(--vp-font-family-mono);
  font-variant-numeric: tabular-nums;
  font-weight: 600;
  color: var(--vp-c-brand-1);
}
.je-saisies {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 2fr);
  gap: 0.5rem;
  margin-top: 0.5rem;
}
.je-capture {
  margin: 0.35rem 0 0 !important;
  font-size: 0.72rem;
  color: var(--vp-c-text-2);
}
.je-tableau { overflow-x: auto; }
.je-tableau table {
  display: table;
  width: 100%;
  margin: 0 !important;
  font-size: 0.8rem;
}
.je-tableau th, .je-tableau td { padding: 0.35rem 0.5rem !important; vertical-align: top; }
.je-td-critere { color: var(--vp-c-text-2); }
.je-symbole { display: inline-block; width: 1.1rem; font-weight: 700; }
.je-tableau td.is-reussi .je-symbole { color: var(--vp-c-green-1); }
.je-tableau td.is-echoue .je-symbole { color: var(--vp-c-red-1); }
.je-tableau td.is-nv .je-symbole { color: var(--vp-c-yellow-1); }
.je-tableau td.is-vide .je-symbole { color: var(--vp-c-text-3); }
.je-tableau tfoot td { font-weight: 600; }
.je-rappel {
  margin: 0.75rem 0 0.6rem !important;
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
.je-pied {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
}
@media (max-width: 720px) {
  .je-ident { grid-template-columns: 1fr 1fr; }
  .je-outil-nom { grid-column: 1 / -1; }
  .je-plan-tete { display: none; }
  .je-plan-ligne { grid-template-columns: 2.2rem 1fr; }
  .je-plan-ligne input:last-child { grid-column: 2; }
  .je-saisies { grid-template-columns: 1fr; }
}
</style>
