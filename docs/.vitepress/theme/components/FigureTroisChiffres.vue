<script setup lang="ts">
// Séance 8 : trois chiffres par tâche, chacun avec ce qui le justifie; l'écart entre l'optimiste
// et le pessimiste montre le risque. Aucune abréviation : les étudiants lisaient mal « O, P, Pe ».
const MAX = 12;
type Chiffre = { h: number; pourquoi: string };
const TACHES = [
  {
    nom: "Relier la réservation à Square",
    optimiste: { h: 2, pourquoi: "La documentation est claire, le premier paiement d'essai passe." },
    probable: { h: 4, pourquoi: "Deux ou trois essais ratés avant que le paiement passe." },
    pessimiste: { h: 10, pourquoi: "Les deux outils ne se parlent pas bien : on écrit au soutien et on attend." },
    note: "Grand écart entre l'optimiste et le pessimiste : c'est un risque. On l'essaie en premier.",
  },
  {
    nom: "Mettre en page la page Contact",
    optimiste: { h: 1.5, pourquoi: "Le gabarit convient tel quel." },
    probable: { h: 2, pourquoi: "Quelques retouches pour le téléphone." },
    pessimiste: { h: 3, pourquoi: "La carte intégrée s'affiche mal et il faut la remplacer." },
    note: "Petit écart : rien à craindre.",
  },
];
const COLONNES = [
  { cle: "optimiste", titre: "Optimiste", sens: "tout va bien du premier coup" },
  { cle: "probable", titre: "Probable", sens: "ce qui arrive d'habitude" },
  { cle: "pessimiste", titre: "Pessimiste", sens: "ce qui peut raisonnablement mal tourner" },
] as const;
const retenue = (t: (typeof TACHES)[number]) => (t.optimiste.h + 4 * t.probable.h + t.pessimiste.h) / 6;
const pc = (h: number) => `${(h / MAX) * 100}%`;
const fmt = (n: number) => n.toLocaleString("fr-CA", { maximumFractionDigits: 1 });
const GRAD = Array.from({ length: MAX / 2 + 1 }, (_, i) => i * 2);
const chiffre = (t: (typeof TACHES)[number], cle: (typeof COLONNES)[number]["cle"]): Chiffre => t[cle];
</script>

<template>
  <figure class="fig7 ft">
    <div v-for="t in TACHES" :key="t.nom" class="ft-tache">
      <p class="ft-nom"><strong>{{ t.nom }}</strong></p>
      <div class="ft-trois">
        <div v-for="c in COLONNES" :key="c.cle" class="ft-case" :class="'is-' + c.cle">
          <span class="ft-titre">{{ c.titre }}</span>
          <span class="ft-h">{{ fmt(chiffre(t, c.cle).h) }} h</span>
          <span class="ft-pourquoi">{{ chiffre(t, c.cle).pourquoi }}</span>
        </div>
      </div>
      <div class="ft-piste" aria-hidden="true">
        <span class="ft-bande" :style="{ left: pc(t.optimiste.h), width: pc(t.pessimiste.h - t.optimiste.h) }" />
        <span class="ft-ret" :style="{ left: pc(retenue(t)) }">{{ fmt(retenue(t)) }} h</span>
      </div>
      <div class="ft-axe" aria-hidden="true">
        <span v-for="g in GRAD" :key="g" :style="{ left: pc(g) }">{{ g }} h</span>
      </div>
      <p class="ft-calcul">
        Estimation retenue : ({{ fmt(t.optimiste.h) }} + 4 × {{ fmt(t.probable.h) }} + {{ fmt(t.pessimiste.h) }}) ÷ 6
        ≈ <strong>{{ fmt(retenue(t)) }} h</strong>. {{ t.note }}
      </p>
    </div>
    <div class="ft-formule">
      <span>Estimation retenue =</span>
      <span class="ft-frac"><span>optimiste + 4 × probable + pessimiste</span><span>6</span></span>
    </div>
    <figcaption>
      <strong>La bande jaune va de l'optimiste au pessimiste; la pastille bleue est l'estimation retenue</strong>, le chiffre
      qu'on met au devis. Le probable compte quatre fois, parce que c'est ce qui arrive le plus souvent; l'optimiste et le
      pessimiste ne font que tirer un peu le chiffre d'un côté ou de l'autre. Plus la bande est large, plus la tâche est
      risquée.
    </figcaption>
  </figure>
</template>

<style scoped>
.ft-tache { margin-bottom: 1.8rem; }
.ft-nom { margin: 0 0 0.5rem !important; font-size: 0.9rem; }
.ft-trois {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.5rem;
  margin-bottom: 2rem;
}
.ft-case {
  display: grid;
  gap: 0.15rem;
  align-content: start;
  padding: 0.5rem 0.6rem;
  border-radius: 0.5rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
}
.ft-case.is-probable { border-color: var(--vp-c-text-2); }
.ft-titre { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.03em; color: var(--vp-c-text-2); }
.ft-h { font-size: 1.1rem; font-weight: 700; }
.ft-pourquoi { font-size: 0.78rem; line-height: 1.35; color: var(--vp-c-text-2); }
.ft-piste {
  position: relative;
  height: 0.55rem;
  margin: 0 1.2rem;
  border-radius: 999px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
}
.ft-bande {
  position: absolute;
  top: -1px;
  bottom: -1px;
  border-radius: 999px;
  background: var(--vp-c-warning-soft);
  border: 1px solid var(--vp-c-warning-2);
}
.ft-ret {
  position: absolute;
  bottom: 0.95rem;
  transform: translateX(-50%);
  padding: 0.05rem 0.45rem;
  border-radius: 999px;
  background: var(--vp-c-brand-1);
  color: var(--vp-c-white);
  font-size: 0.7rem;
  font-weight: 700;
  white-space: nowrap;
}
.ft-ret::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: -0.4rem;
  border: 0.22rem solid transparent;
  border-top-color: var(--vp-c-brand-1);
  transform: translateX(-50%);
}
.ft-axe {
  position: relative;
  height: 1rem;
  margin: 0.2rem 1.2rem 0;
  font-size: 0.65rem;
  color: var(--vp-c-text-3);
}
.ft-axe span { position: absolute; top: 0; transform: translateX(-50%); white-space: nowrap; }
.ft-calcul { margin: 0.4rem 0 0 !important; font-size: 0.82rem; }
.ft-formule {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  align-items: center;
  justify-content: center;
  padding: 0.6rem;
  border-radius: 0.6rem;
  background: var(--vp-c-bg);
  font-size: 0.95rem;
}
.ft-frac { display: inline-grid; text-align: center; }
.ft-frac span:first-child { border-bottom: 1px solid currentColor; padding: 0 0.3rem; }
@media (max-width: 560px) {
  .ft-trois { grid-template-columns: 1fr; }
}
</style>
