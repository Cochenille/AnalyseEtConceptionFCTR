<script setup lang="ts">
// Séance 8 : un devis se lit en trois comparaisons (boulangerie de l'activité 2, montants avant taxes).
const UNIQUES = 7290;
const BUDGET = 6000;
const ANNUELS = 860;
const AUJOURDHUI = 300;
const TROIS_ANS = UNIQUES + 3 * ANNUELS;
const fmt = (n: number) => n.toLocaleString("fr-CA") + " $";
const pcU = (n: number) => `${(n / (UNIQUES * 1.08)) * 100}%`;
const pcA = (n: number) => `${(n / (ANNUELS * 1.25)) * 100}%`;
const pcT = (n: number) => `${(n / TROIS_ANS) * 100}%`;
</script>

<template>
  <figure class="fig7 fd">
    <div class="fd-bloc">
      <p class="fd-titre"><strong>Coûts uniques</strong> <span>construction (heures × 75 $) et achats</span></p>
      <div class="fd-piste">
        <span class="fd-barre is-u" :style="{ width: pcU(BUDGET) }">{{ fmt(UNIQUES) }}</span>
        <span class="fd-barre is-trop" :style="{ left: pcU(BUDGET), width: pcU(UNIQUES - BUDGET) }" />
        <span class="fd-repere" :style="{ left: pcU(BUDGET) }"><span>budget {{ fmt(BUDGET) }}</span></span>
      </div>
      <p class="fd-verdict is-mal">{{ fmt(UNIQUES - BUDGET) }} au-dessus du budget</p>
    </div>

    <div class="fd-bloc">
      <p class="fd-titre"><strong>Coûts annuels</strong> <span>abonnements, domaine, commissions, entretien</span></p>
      <div class="fd-piste">
        <span class="fd-barre is-a" :style="{ width: pcA(ANNUELS) }">{{ fmt(ANNUELS) }} par année</span>
        <span class="fd-repere" :style="{ left: pcA(AUJOURDHUI) }"><span>aujourd'hui {{ fmt(AUJOURDHUI) }}</span></span>
      </div>
      <p class="fd-verdict">La cliente n'avait rien prévu : on lui dit combien mettre de côté chaque année.</p>
    </div>

    <div class="fd-bloc">
      <p class="fd-titre"><strong>Total sur trois ans</strong> <span>pour information : ce que le projet coûte vraiment</span></p>
      <div class="fd-piste fd-empile">
        <span class="fd-seg is-u" :style="{ width: pcT(UNIQUES) }">uniques</span>
        <span v-for="a in 3" :key="a" class="fd-seg is-a" :style="{ width: pcT(ANNUELS) }">an {{ a }}</span>
      </div>
      <p class="fd-verdict"><strong>{{ fmt(TROIS_ANS) }}</strong></p>
    </div>

    <figcaption>
      <strong>Trois chiffres, trois comparaisons.</strong> Les coûts uniques se comparent au budget de construction (pour Mélanie : 8 000 $, ou 13 000 $ avec la subvention). Les coûts annuels se comparent à ce que l'entreprise paie aujourd'hui (environ 300 $ pour Wix). Le total sur trois ans ne se compare à rien : il informe.
    </figcaption>
  </figure>
</template>

<style scoped>
.fd { display: grid; gap: 1.3rem; }
.fd-bloc { display: grid; gap: 0.35rem; }
.fd-titre { margin: 0 !important; font-size: 0.85rem; }
.fd-titre span { color: var(--vp-c-text-2); font-size: 0.75rem; }
.fd-piste {
  position: relative;
  height: 1.6rem;
  margin-top: 1.1rem;
  border-radius: 0.35rem;
  background: var(--vp-c-bg);
}
.fd-barre {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  display: flex;
  align-items: center;
  padding-left: 0.5rem;
  border-radius: 0.35rem;
  font-size: 0.75rem;
  font-weight: 700;
  white-space: nowrap;
  color: var(--vp-c-white);
}
.is-u { background: var(--vp-c-brand-1); }
.is-a { background: var(--vp-c-brand-3); }
.fd-barre.is-u { border-radius: 0.35rem 0 0 0.35rem; }
.fd-barre.is-trop {
  border-radius: 0 0.35rem 0.35rem 0;
  background: repeating-linear-gradient(135deg, var(--vp-c-red-2) 0 5px, var(--vp-c-red-soft) 5px 10px);
}
.fd-repere {
  position: absolute;
  top: -1.1rem;
  bottom: -0.25rem;
  border-left: 2px solid var(--vp-c-text-1);
}
.fd-repere span {
  position: absolute;
  top: 0;
  left: 0.3rem;
  font-size: 0.7rem;
  font-weight: 600;
  line-height: 1;
  white-space: nowrap;
}
.fd-empile { display: flex; gap: 2px; margin-top: 0.2rem; overflow: hidden; }
.fd-seg {
  display: grid;
  place-items: center;
  height: 100%;
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--vp-c-white);
  white-space: nowrap;
  overflow: hidden;
}
.fd-verdict { margin: 0 !important; font-size: 0.78rem; color: var(--vp-c-text-2); }
.fd-verdict.is-mal { color: var(--vp-c-red-1); font-weight: 600; }
</style>
