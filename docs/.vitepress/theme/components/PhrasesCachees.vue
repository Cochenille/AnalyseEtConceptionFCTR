<script setup lang="ts">
import { reactive } from "vue";

type Cout = 1 | 2 | 3;
type Phrase = {
  qui: string;
  phrase: string;
  probleme: string;
  details: string[];
  questions: string[];
  cout: Cout;
  recurrent: boolean;
  justification: string;
};

const COUTS: { valeur: Cout; symbole: string; sens: string }[] = [
  { valeur: 1, symbole: "$", sens: "Quelques heures, moins de 500 $" },
  { valeur: 2, symbole: "$$", sens: "De 500 $ à 3 000 $" },
  { valeur: 3, symbole: "$$$", sens: "Plus de 3 000 $" },
];

const PHRASES: Phrase[] = [
  {
    qui: "Mélanie",
    phrase: "Ah, et les gens devraient pouvoir réserver pour toute leur famille d'un coup.",
    probleme: "Une réservation, ce n'est plus une personne : c'est un payeur et plusieurs participants.",
    details: [
      "Chaque participant doit avoir sa propre décharge. Pour un enfant, c'est un parent qui signe.",
      "Il faut peut-être l'âge, la taille ou le poids de chacun (via ferrata, veste de flottaison).",
      "Que se passe-t-il si un membre de la famille n'a pas signé en arrivant au quai ?",
    ],
    questions: [
      "Un parent peut-il signer pour trois enfants en une seule fois ?",
      "Un adulte peut-il signer pour un autre adulte ? (Réponse probable : non.)",
    ],
    cout: 2,
    recurrent: false,
    justification: "Peu coûteux si l'outil de réservation choisi gère les participants et les décharges. Très coûteux s'il faut le programmer.",
  },
  {
    qui: "Mélanie",
    phrase: "Pour l'anglais, on pourrait juste utiliser Google Traduction.",
    probleme: "La décharge est un document juridique. Une traduction automatique peut changer son sens.",
    details: [
      "Il n'y a pas que les pages : les courriels de confirmation, les rappels, la politique de confidentialité et les conditions d'annulation doivent aussi être traduits.",
      "Chaque modification devra être faite deux fois, pour toujours.",
      "Au Québec, la version française doit rester au moins aussi complète que la version anglaise.",
    ],
    questions: [
      "L'avocat de l'assurance acceptera-t-il une décharge traduite ? Par qui ?",
      "Qui fera les mises à jour en anglais pendant l'été ?",
    ],
    cout: 2,
    recurrent: true,
    justification: "Traduction professionnelle au départ, puis du temps chaque fois qu'un texte change.",
  },
  {
    qui: "Patrick",
    phrase: "Quand il y a un orage, le site pourrait juste avertir les gens.",
    probleme: "Avertir, c'est facile. Mais ensuite : on rembourse, on reporte ou on donne un crédit ?",
    details: [
      "Il faut pouvoir joindre d'un coup tous les participants d'un départ, idéalement par texto. Les textos coûtent quelques sous chacun et demandent le consentement du client.",
      "Le remboursement doit passer par le même outil de paiement que l'achat.",
      "L'entreprise n'a encore aucune politique d'annulation : c'est un problème organisationnel avant d'être technique.",
    ],
    questions: [
      "Qui décide d'annuler, et à partir de quel moment ?",
      "Quelle sera la politique d'annulation, pour la météo et pour le client qui change d'idée ?",
    ],
    cout: 2,
    recurrent: true,
    justification: "Inclus dans plusieurs outils de réservation, mais chaque texto est facturé. Très coûteux si c'est fait sur mesure.",
  },
  {
    qui: "Karine",
    phrase: "Viator, ça continue comme avant.",
    probleme: "Deux systèmes vendent les mêmes places. Sans synchronisation, les doubles réservations vont continuer.",
    details: [
      "Il faut que le nouveau système et Viator partagent en temps réel les places restantes.",
      "Seuls certains outils de réservation sont connectés à Viator. Cette phrase élimine donc une partie des choix possibles.",
      "Recopier à la main, c'est exactement ce qui cause le problème aujourd'hui.",
    ],
    questions: [
      "Combien de places Viator a-t-il le droit de vendre sur chaque départ ?",
      "L'entreprise veut-elle aussi vendre sur d'autres plateformes (Expedia, GetYourGuide) ?",
    ],
    cout: 2,
    recurrent: true,
    justification: "Les outils connectés à Viator coûtent souvent plus cher par mois ou par réservation. Faire le lien soi-même serait bien plus cher.",
  },
  {
    qui: "Patrick",
    phrase: "Je vais mettre ma vidéo de drone en plein écran sur la page d'accueil.",
    probleme: "Une vidéo 4K brute pèse des centaines de mégaoctets. Sur un téléphone avec un réseau faible, la page ne s'affichera pas.",
    details: [
      "Il faut compresser la vidéo, la raccourcir et prévoir une image fixe pendant le chargement.",
      "La vidéo doit être hébergée à un endroit capable de la servir rapidement.",
      "Accessibilité : la vidéo doit pouvoir être mise en pause, sans son au départ, et l'information importante ne doit pas se trouver seulement dans la vidéo.",
    ],
    questions: [
      "Quelle durée maximale ? 15 secondes suffisent souvent.",
      "La vidéo doit-elle aussi jouer sur les téléphones, ou seulement sur ordinateur ?",
    ],
    cout: 1,
    recurrent: false,
    justification: "Peu coûteux si c'est prévu dès le départ. Le vrai coût, c'est un site lent qui fait fuir les clients.",
  },
];

const etat = reactive(PHRASES.map(() => ({ estimation: null as Cout | null, revele: false })));

function symbole(c: Cout) {
  return COUTS[c - 1].symbole;
}
</script>

<template>
  <section class="pc">
    <div class="pc-echelle" aria-label="Échelle de coût">
      <div v-for="c in COUTS" :key="c.valeur" class="pc-niveau">
        <strong>{{ c.symbole }}</strong>
        <span>{{ c.sens }}</span>
      </div>
    </div>

    <ol class="pc-liste">
      <li v-for="(p, n) in PHRASES" :key="n" class="pc-carte" :class="{ 'is-revele': etat[n].revele }">
        <p class="pc-qui">Phrase {{ n + 1 }} · {{ p.qui }}</p>
        <blockquote class="pc-phrase">« {{ p.phrase }} »</blockquote>

        <div class="pc-estimer">
          <span>Votre estimation :</span>
          <div class="pc-boutons" role="group" :aria-label="'Coût estimé pour la phrase ' + (n + 1)">
            <button
              v-for="c in COUTS"
              :key="c.valeur"
              type="button"
              class="pc-btn"
              :aria-pressed="etat[n].estimation === c.valeur"
              @click="etat[n].estimation = c.valeur"
            >
              {{ c.symbole }}
            </button>
          </div>
          <button type="button" class="pc-reveler" :aria-expanded="etat[n].revele" @click="etat[n].revele = !etat[n].revele">
            {{ etat[n].revele ? "Cacher" : "Révéler le problème caché" }}
          </button>
        </div>

        <div v-if="etat[n].revele" class="pc-reponse">
          <p class="pc-probleme"><strong>Le problème caché :</strong> {{ p.probleme }}</p>
          <ul>
            <li v-for="(d, i) in p.details" :key="i">{{ d }}</li>
          </ul>
          <p class="pc-sous">Questions à poser au client</p>
          <ul>
            <li v-for="(q, i) in p.questions" :key="i">{{ q }}</li>
          </ul>
          <p class="pc-cout">
            <span class="pc-pastille">{{ symbole(p.cout) }}</span>
            <span v-if="p.recurrent" class="pc-pastille is-recurrent">coût annuel</span>
            {{ p.justification }}
          </p>
          <p v-if="etat[n].estimation !== null" class="pc-compare">
            Vous aviez estimé <strong>{{ symbole(etat[n].estimation!) }}</strong>.
            <template v-if="etat[n].estimation === p.cout">Même ordre de grandeur.</template>
            <template v-else>Qu'est-ce qui explique l'écart ?</template>
          </p>
        </div>
      </li>
    </ol>
  </section>
</template>

<style scoped>
.pc {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.pc-echelle {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 0.5rem;
}
.pc-niveau {
  display: flex;
  flex-direction: column;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.65rem;
  background: var(--vp-c-bg);
  font-size: 0.8rem;
  line-height: 1.4;
}
.pc-niveau strong {
  font-size: 0.95rem;
}
.pc-niveau span {
  color: var(--vp-c-text-2);
}
.pc-liste {
  list-style: none !important;
  margin: 0.75rem 0 0 !important;
  padding: 0 !important;
  display: grid;
  gap: 0.75rem;
}
.pc-carte {
  margin: 0 !important;
  padding: 0.8rem 0.9rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.75rem;
  background: var(--vp-c-bg);
}
.pc-carte.is-revele {
  border-color: var(--vp-c-brand-2);
}
.pc-qui {
  margin: 0 !important;
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--vp-c-text-2);
}
.pc-phrase {
  margin: 0.3rem 0 0.6rem !important;
  padding: 0 !important;
  border: 0 !important;
  font-size: 1.02rem;
  font-weight: 600;
  line-height: 1.45;
  color: var(--vp-c-text-1) !important;
}
.pc-estimer {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
  color: var(--vp-c-text-2);
}
.pc-boutons {
  display: flex;
  gap: 0.3rem;
}
.pc-btn {
  min-width: 2.6rem;
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
  font-size: 0.8rem;
  font-weight: 600;
}
.pc-btn:hover {
  border-color: var(--vp-c-brand-1);
}
.pc-btn[aria-pressed="true"] {
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
}
.pc-reveler {
  margin-left: auto;
  padding: 0.3rem 0.75rem;
  border-radius: 0.6rem;
  border: 1px solid var(--vp-c-brand-2);
  color: var(--vp-c-brand-1);
  font-size: 0.8rem;
  font-weight: 600;
}
.pc-reveler:hover {
  background: var(--vp-c-brand-soft);
}
.pc-reponse {
  margin-top: 0.75rem;
  padding-top: 0.6rem;
  border-top: 1px dashed var(--vp-c-divider);
  font-size: 0.86rem;
  line-height: 1.55;
}
.pc-reponse p {
  margin: 0.4rem 0 !important;
}
.pc-reponse ul {
  margin: 0.2rem 0 0.4rem !important;
  padding-left: 1.2rem !important;
}
.pc-reponse li {
  margin: 0.15rem 0 !important;
}
.pc-sous {
  font-weight: 600;
  font-size: 0.8rem;
  color: var(--vp-c-text-2);
}
.pc-pastille {
  display: inline-block;
  margin-right: 0.3rem;
  padding: 0.05rem 0.45rem;
  border-radius: 999px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-size: 0.75rem;
  font-weight: 700;
}
.pc-pastille.is-recurrent {
  background: var(--vp-c-warning-soft);
  color: var(--vp-c-warning-1);
}
.pc-compare {
  font-size: 0.8rem;
  color: var(--vp-c-text-2);
}
</style>
