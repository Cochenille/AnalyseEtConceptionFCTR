<script setup lang="ts">
// Séance 8 : comment les poids des critères décident (exemple de la boulangerie, outils inventés).
const ETAPES = [
  {
    poids: 3,
    nom: "Indispensable",
    effet: "l'outil qui échoue est écarté",
    critere: "La propriétaire change le menu seule",
    outils: [
      { nom: "Outil A", ok: true, note: "abonnement : 45 $ par mois" },
      { nom: "Outil B", ok: true, note: "commission de 4 % par commande" },
      { nom: "Outil C", ok: true, note: "abonnement : 30 $ par mois" },
      { nom: "Outil D", ok: false, note: "seul le fournisseur peut changer le menu" },
    ],
  },
  {
    poids: 2,
    nom: "Important",
    effet: "on garde le meilleur des outils qui restent",
    critere: "Moins de 40 $ par mois",
    outils: [
      { nom: "Outil A", ok: true },
      { nom: "Outil B", ok: false, note: "la commission revient à environ 150 $ par mois" },
      { nom: "Outil C", ok: true },
    ],
  },
  {
    poids: 1,
    nom: "Souhaitable",
    effet: "sert seulement si deux outils sont à égalité",
    critere: "Un rappel par texto la veille",
    outils: [
      { nom: "Outil A", ok: true, choix: true, note: "retenu" },
      { nom: "Outil C", ok: false, note: "pas de texto" },
    ],
  },
];
</script>

<template>
  <figure class="fig7 fp">
    <div class="fp-etapes">
      <div v-for="(e, i) in ETAPES" :key="e.poids" class="fp-etape">
        <div class="fp-tete" :class="'p' + e.poids">
          <span class="fp-poids">{{ e.poids }}</span>
          <span><strong>{{ e.nom }}</strong><br />{{ e.effet }}</span>
        </div>
        <p class="fp-critere">« {{ e.critere }} »</p>
        <ul class="fp-outils">
          <li v-for="o in e.outils" :key="o.nom" :class="{ 'is-out': !o.ok, 'is-choix': o.choix }">
            <span class="fp-marque">{{ o.choix ? "★" : o.ok ? "✓" : "✕" }}</span>
            <span><span class="fp-nom-outil">{{ o.nom }}</span><small v-if="o.note">{{ o.note }}</small></span>
          </li>
        </ul>
        <span v-if="i < ETAPES.length - 1" class="fp-fleche" aria-hidden="true">→</span>
      </div>
    </div>
    <figcaption>
      <strong>Quatre outils de commande en ligne pour la boulangerie (A à D, inventés), trois critères, un choix.</strong> Un outil qui échoue à un critère de poids 3 est écarté, même s'il est excellent ailleurs. Parmi ceux qui restent, les critères de poids 2 font le choix. Les critères de poids 1 servent seulement quand deux outils sont à égalité. Dans la section 8.2, on nomme les critères qui ont décidé.
    </figcaption>
  </figure>
</template>

<style scoped>
.fp-etapes {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.4rem;
}
.fp-etape {
  position: relative;
  display: grid;
  gap: 0.45rem;
  align-content: start;
}
.fp-tete {
  display: flex;
  gap: 0.6rem;
  align-items: center;
  padding: 0.45rem 0.6rem;
  border-radius: 0.6rem;
  font-size: 0.8rem;
  line-height: 1.25;
}
.fp-tete.p3 { background: var(--vp-c-red-soft); }
.fp-tete.p2 { background: var(--vp-c-warning-soft); }
.fp-tete.p1 { background: var(--vp-c-brand-soft); }
.fp-poids {
  display: grid;
  place-items: center;
  width: 2rem;
  height: 2rem;
  flex-shrink: 0;
  border-radius: 50%;
  background: var(--vp-c-bg);
  font-weight: 800;
  font-size: 1.1rem;
}
.fp-critere {
  margin: 0 !important;
  font-size: 0.78rem;
  font-style: italic;
  color: var(--vp-c-text-2);
}
.fp-outils {
  display: grid;
  gap: 0.3rem;
  margin: 0 !important;
  padding: 0 !important;
  list-style: none;
}
.fp-outils li {
  display: flex;
  gap: 0.45rem;
  align-items: flex-start;
  margin: 0 !important;
  padding: 0.35rem 0.55rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.5rem;
  background: var(--vp-c-bg);
  font-size: 0.8rem;
  font-weight: 600;
  line-height: 1.3;
}
.fp-outils small { display: block; font-weight: 400; color: var(--vp-c-text-2); font-size: 0.72rem; }
.fp-marque { width: 1rem; flex-shrink: 0; text-align: center; color: var(--vp-c-green-1); }
.fp-outils li.is-out { opacity: 0.75; border-style: dashed; }
.fp-outils li.is-out .fp-marque { color: var(--vp-c-red-1); }
.fp-outils li.is-out .fp-nom-outil { text-decoration: line-through; text-decoration-thickness: 1px; }
.fp-outils li.is-choix { border-color: var(--vp-c-brand-1); background: var(--vp-c-brand-soft); }
.fp-outils li.is-choix .fp-marque { color: var(--vp-c-brand-1); }
.fp-fleche {
  position: absolute;
  right: -1.15rem;
  top: 0.6rem;
  font-size: 1.1rem;
  color: var(--vp-c-text-3);
}
@media (max-width: 640px) {
  .fp-etapes { grid-template-columns: 1fr; gap: 0.9rem; }
  .fp-fleche { display: none; }
}
</style>
