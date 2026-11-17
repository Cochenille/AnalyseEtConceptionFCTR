<script setup lang="ts">
// Séance 8 : trois chiffres par tâche; l'écart entre O et Pe montre le risque.
const MAX = 12;
const TACHES = [
  { nom: "Relier la réservation à Square", o: 2, p: 4, pe: 10, note: "Grand écart : un risque. À essayer en premier." },
  { nom: "Mettre en page la page Contact", o: 1.5, p: 2, pe: 3, note: "Petit écart : rien à craindre." },
];
const retenue = (t: { o: number; p: number; pe: number }) => (t.o + 4 * t.p + t.pe) / 6;
const pc = (h: number) => `${(h / MAX) * 100}%`;
const fmt = (n: number) => n.toLocaleString("fr-CA", { maximumFractionDigits: 1 });
const GRAD = Array.from({ length: MAX / 2 + 1 }, (_, i) => i * 2);
</script>

<template>
  <figure class="fig7 ft">
    <div v-for="t in TACHES" :key="t.nom" class="ft-ligne">
      <p class="ft-nom">
        <strong>{{ t.nom }}</strong>
        <span class="ft-vals">O {{ fmt(t.o) }} h · P {{ fmt(t.p) }} h · Pe {{ fmt(t.pe) }} h</span>
        <span>{{ t.note }}</span>
      </p>
      <div class="ft-piste">
        <span class="ft-bande" :style="{ left: pc(t.o), width: pc(t.pe - t.o) }" />
        <span class="ft-pt" :style="{ left: pc(t.o) }">O</span>
        <span class="ft-pt is-p" :style="{ left: pc(t.p) }">P</span>
        <span class="ft-pt" :style="{ left: pc(t.pe) }">Pe</span>
        <span class="ft-ret" :style="{ left: pc(retenue(t)) }">retenue {{ fmt(retenue(t)) }} h</span>
      </div>
    </div>
    <div class="ft-axe">
      <span v-for="g in GRAD" :key="g" :style="{ left: pc(g) }">{{ g }} h</span>
    </div>
    <div class="ft-formule">
      <span>Retenue =</span>
      <span class="ft-frac"><span>O + 4 × P + Pe</span><span>6</span></span>
      <span class="ft-ex">(2 + 16 + 10) ÷ 6 ≈ <strong>4,7 h</strong></span>
    </div>
    <figcaption>
      <strong>Optimiste</strong> : tout va bien du premier coup. <strong>Probable</strong> : ce qui arrive d'habitude. <strong>Pessimiste</strong> : ce qui peut raisonnablement mal tourner. La retenue penche vers le probable, mais la largeur de la bande dit où est le risque.
    </figcaption>
  </figure>
</template>

<style scoped>
.ft-ligne { margin-bottom: 2.4rem; }
.ft-nom { display: flex; flex-wrap: wrap; gap: 0.2rem 0.6rem; align-items: baseline; margin: 0 0 1.2rem !important; font-size: 0.85rem; }
.ft-nom span { color: var(--vp-c-text-2); font-size: 0.78rem; }
.ft-nom .ft-vals { font-family: var(--vp-font-family-mono); font-size: 0.72rem; color: var(--vp-c-text-1); }
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
.ft-pt {
  position: absolute;
  bottom: -0.2rem;
  height: 1.5rem;
  transform: translateX(-1px);
  padding-left: 3px;
  border-left: 2px solid var(--vp-c-text-3);
  font-size: 0.7rem;
  font-weight: 700;
  line-height: 0.9rem;
  color: var(--vp-c-text-2);
}
.ft-pt.is-p { border-left-color: var(--vp-c-text-1); color: var(--vp-c-text-1); }
.ft-ret {
  position: absolute;
  top: 0.85rem;
  transform: translateX(-50%);
  padding: 0.1rem 0.45rem;
  border-radius: 999px;
  background: var(--vp-c-brand-1);
  color: var(--vp-c-white);
  font-size: 0.7rem;
  font-weight: 700;
  white-space: nowrap;
}
.ft-ret::before {
  content: "";
  position: absolute;
  left: 50%;
  top: -0.4rem;
  border: 0.22rem solid transparent;
  border-bottom-color: var(--vp-c-brand-1);
  transform: translateX(-50%);
}
.ft-axe {
  position: relative;
  height: 1rem;
  margin: -0.6rem 1.2rem 0;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.65rem;
  color: var(--vp-c-text-3);
}
.ft-axe span { position: absolute; top: 0.15rem; transform: translateX(-50%); white-space: nowrap; }
.ft-formule {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  align-items: center;
  justify-content: center;
  margin-top: 1rem;
  padding: 0.6rem;
  border-radius: 0.6rem;
  background: var(--vp-c-bg);
  font-size: 0.95rem;
}
.ft-frac { display: inline-grid; text-align: center; }
.ft-frac span:first-child { border-bottom: 1px solid currentColor; padding: 0 0.3rem; }
.ft-ex { color: var(--vp-c-text-2); font-size: 0.85rem; }
</style>
