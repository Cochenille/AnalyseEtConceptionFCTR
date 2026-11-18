<script setup lang="ts">
// Séance 8 : échéancier à rebours de la boulangerie (mise en ligne le 1er décembre 2026).
const DEBUT = new Date(2026, 8, 4); // 4 sept.
const FIN = new Date(2026, 11, 4); // 4 déc.
const jours = (d: Date) => (d.getTime() - DEBUT.getTime()) / 86400000;
const TOTAL = jours(FIN);
const pc = (d: Date) => `${(jours(d) / TOTAL) * 100}%`;
const larg = (a: Date, b: Date) => `${((jours(b) - jours(a)) / TOTAL) * 100}%`;

const ETAPES = [
  { nom: "Démarrage", de: new Date(2026, 8, 4), a: new Date(2026, 8, 18) },
  { nom: "Maquettes", de: new Date(2026, 8, 18), a: new Date(2026, 9, 2) },
  { nom: "Construction", de: new Date(2026, 9, 2), a: new Date(2026, 9, 30) },
  { nom: "Tests et formation", de: new Date(2026, 9, 30), a: new Date(2026, 10, 13) },
  { nom: "Coussin", de: new Date(2026, 10, 13), a: new Date(2026, 10, 27), coussin: true },
];
const CLIENT = [
  { date: new Date(2026, 8, 18), texte: "accès au domaine" },
  { date: new Date(2026, 8, 25), texte: "commentaires sur les maquettes" },
  { date: new Date(2026, 9, 9), texte: "textes et photos" },
  { date: new Date(2026, 10, 10), texte: "1 h de formation" },
];
const LANCEMENT = new Date(2026, 11, 1);
const MOIS = [
  { nom: "sept.", d: new Date(2026, 8, 4) },
  { nom: "oct.", d: new Date(2026, 9, 1) },
  { nom: "nov.", d: new Date(2026, 10, 1) },
  { nom: "déc.", d: new Date(2026, 11, 1) },
];
const jour = (d: Date) => d.toLocaleDateString("fr-CA", { day: "numeric", month: "short" });
const SEMAINES = 7;
</script>

<template>
  <figure class="fig7 fe">
    <ol class="fe-raison">
      <li>
        <strong>Les heures.</strong> L'estimation de la boulangerie (étape 2) donne 96 heures, arrondies à
        <strong>100 h</strong>.
      </li>
      <li>
        <strong>Les heures par semaine.</strong> Le studio a d'autres clients : il peut donner <strong>15 h par
        semaine</strong> à ce projet. 100 h ÷ 15 h ≈ <strong>7 semaines de travail</strong>. À temps plein (40 h par
        semaine), ce serait 2 ½ semaines, mais personne ne travaille sur un seul projet à la fois.
        <span class="fe-semaines">
          <span class="fe-blocs">
            <span v-for="s in SEMAINES" :key="s" class="fe-bloc">s{{ s }}</span>
          </span>
          <span class="fe-calc">7 semaines de travail</span>
        </span>
      </li>
      <li>
        <strong>Le calendrier.</strong> Les quatre étapes s'étalent sur <strong>10 semaines</strong>, pas 7, parce qu'on
        attend la cliente entre les étapes (ses commentaires, ses textes). On ajoute un <strong>coussin</strong> de
        20 % : 20 % de 10 semaines = <strong>2 semaines</strong>. Total : 12 semaines, à placer avant le 1<sup>er</sup>
        décembre.
      </li>
    </ol>

    <div class="fe-gantt">
      <div class="fe-mois">
        <span v-for="m in MOIS" :key="m.nom" :style="{ left: pc(m.d) }">{{ m.nom }}</span>
      </div>
      <div v-for="e in ETAPES" :key="e.nom" class="fe-ligne">
        <span class="fe-nom">{{ e.nom }}</span>
        <span class="fe-piste">
          <span class="fe-barre" :class="{ 'is-coussin': e.coussin }" :style="{ left: pc(e.de), width: larg(e.de, e.a) }">
            <template v-if="e.coussin">2 sem.</template>
          </span>
        </span>
      </div>
      <div class="fe-ligne fe-ligne-client">
        <span class="fe-nom">La cliente fournit</span>
        <span class="fe-piste">
          <span v-for="c in CLIENT" :key="c.texte" class="fe-losange" :style="{ left: pc(c.date) }" :title="jour(c.date) + ' : ' + c.texte" />
        </span>
      </div>
      <span class="fe-lancement" :style="{ left: `calc(var(--fe-nom) + (100% - var(--fe-nom)) * ${jours(LANCEMENT) / TOTAL})` }">
        <span>Mise en ligne<br />1<sup>er</sup> déc.</span>
      </span>
    </div>

    <ul class="fe-legende">
      <li v-for="c in CLIENT" :key="c.texte"><i class="fe-losange-mini" /><strong>{{ jour(c.date) }}</strong> {{ c.texte }}</li>
    </ul>

    <figcaption>
      <strong>On part de la date qu'on ne peut pas déplacer, et on remonte.</strong> Ici, la mise en ligne du 1<sup>er</sup> décembre : en reculant de 12 semaines, le projet commence début septembre. Le coussin est une étape à part, à la fin (15 à 20 % de la durée des étapes), pas un peu de marge cachée dans chaque tâche. Les losanges sont ce que la cliente doit fournir, chacun avec sa date : un texte en retard est la première cause de retard d'un petit projet.
    </figcaption>
  </figure>
</template>

<style scoped>
.fe { --fe-nom: 9.5rem; }
.fe-raison {
  margin: 0 0 1.4rem !important;
  padding-left: 1.3rem !important;
  font-size: 0.88rem;
  line-height: 1.5;
}
.fe-raison li { margin: 0.35rem 0 !important; }
.fe-semaines {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
  margin-top: 0.4rem;
  font-size: 0.8rem;
  color: var(--vp-c-text-2);
}
.fe-blocs { display: inline-flex; gap: 3px; }
.fe-bloc {
  display: grid;
  place-items: center;
  width: 1.7rem;
  height: 1.5rem;
  border-radius: 0.3rem;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-size: 0.65rem;
  font-weight: 700;
}
.fe-gantt { position: relative; padding-top: 1.2rem; }
.fe-mois {
  position: absolute;
  top: 0;
  left: var(--fe-nom);
  right: 0;
  height: 1rem;
  font-size: 0.7rem;
  color: var(--vp-c-text-3);
}
.fe-mois span { position: absolute; padding-left: 0.2rem; border-left: 1px solid var(--vp-c-divider); }
.fe-ligne {
  display: grid;
  grid-template-columns: var(--fe-nom) 1fr;
  align-items: center;
  min-height: 1.9rem;
}
.fe-nom { font-size: 0.8rem; font-weight: 600; padding-right: 0.5rem; }
.fe-piste {
  position: relative;
  height: 1.3rem;
  border-bottom: 1px dashed var(--vp-c-divider);
}
.fe-barre {
  position: absolute;
  top: 0;
  bottom: 0;
  border-radius: 0.35rem;
  background: var(--vp-c-brand-1);
  color: var(--vp-c-text-1);
  font-size: 0.68rem;
  font-weight: 700;
  display: grid;
  place-items: center;
  white-space: nowrap;
  overflow: hidden;
}
.fe-barre.is-coussin {
  background: repeating-linear-gradient(135deg, var(--vp-c-warning-soft) 0 6px, transparent 6px 12px);
  border: 1.5px dashed var(--vp-c-warning-1);
}
.fe-ligne-client { margin-top: 0.3rem; }
.fe-losange {
  position: absolute;
  top: 50%;
  width: 0.8rem;
  height: 0.8rem;
  background: var(--vp-c-warning-1);
  transform: translate(-50%, -50%) rotate(45deg);
  border-radius: 2px;
}
.fe-lancement {
  position: absolute;
  top: 1rem;
  bottom: -2.2rem;
  border-left: 2px solid var(--vp-c-green-1);
}
.fe-lancement span {
  position: absolute;
  bottom: 0;
  right: 0.3rem;
  font-size: 0.68rem;
  font-weight: 700;
  line-height: 1.2;
  text-align: right;
  white-space: nowrap;
  color: var(--vp-c-green-1);
}
.fe-legende {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem 1rem;
  margin: 2.6rem 0 0 !important;
  padding: 0 !important;
  list-style: none;
  font-size: 0.75rem;
  color: var(--vp-c-text-2);
}
.fe-legende li { margin: 0 !important; display: inline-flex; gap: 0.35rem; align-items: center; }
.fe-losange-mini {
  display: inline-block;
  width: 0.55rem;
  height: 0.55rem;
  background: var(--vp-c-warning-1);
  transform: rotate(45deg);
  border-radius: 1px;
}
@media (max-width: 560px) {
  .fe { --fe-nom: 6.5rem; }
  .fe-nom { font-size: 0.7rem; }
  .fe-barre.is-coussin { font-size: 0; }
}
</style>
