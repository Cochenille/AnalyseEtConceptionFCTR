<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from "vue";
import BoutonCopier from "./BoutonCopier.vue";

// Séance 9, activité 1 : six phrases de la propriétaire de la boulangerie (mise en situation de la séance 8).
// Pour chaque phrase : le vrai besoin (un choix sur trois), puis la sorte de réponse
// (ce que le site doit faire, comment il doit le faire, ou une décision de la cliente).

type Sorte = "quoi" | "comment" | "decision";

const SORTES: Record<Sorte, string> = {
  quoi: "Ce que le site doit faire",
  comment: "Comment il doit le faire",
  decision: "Une décision de la cliente",
};

type Phrase = {
  cle: string;
  phrase: string;
  besoins: string[]; // trois propositions
  bonBesoin: number; // indice de la bonne
  sorte: Sorte;
  relance: string; // la question à poser pour en être sûr
  explication: string;
};

const PHRASES: Phrase[] = [
  {
    cle: "p1",
    phrase: "« Il me faudrait une application, comme les grosses chaînes. »",
    besoins: [
      "Une application à télécharger dans l'App Store et Google Play.",
      "Que les clients commandent depuis leur téléphone, sans appeler.",
      "Que la boulangerie ait l'air aussi moderne qu'une grande chaîne.",
    ],
    bonBesoin: 1,
    sorte: "quoi",
    relance: "« Qu'est-ce que vos clients feraient avec l'application ? »",
    explication:
      "« Une application » est une solution, pas un besoin. Derrière, il y a une action : commander depuis son téléphone. Un site qui marche bien sur téléphone le permet, pour bien moins cher.",
  },
  {
    cle: "p2",
    phrase: "« Il faut que ce soit rapide. »",
    besoins: [
      "Que le site soit construit en moins d'un mois.",
      "Que les commandes soient prêtes plus vite le samedi.",
      "Que la page de commande s'ouvre vite sur un téléphone, même en file d'attente.",
    ],
    bonBesoin: 2,
    sorte: "comment",
    relance: "« Rapide pour qui, et à quel moment ? »",
    explication:
      "« Rapide » peut vouloir dire trois choses différentes : le chantier, la préparation ou le site. Il faut relancer. Ici, c'est une qualité du site (sa vitesse), pas une fonction : on la vérifie avec un chiffre, par exemple moins de 3 secondes sur un téléphone.",
  },
  {
    cle: "p3",
    phrase: "« Je ne veux plus de commandes qui ne sont jamais ramassées. »",
    besoins: [
      "Une règle claire : par exemple, la commande est payée d'avance, ou on garde un dépôt.",
      "Un bouton pour annuler une commande en ligne.",
      "Un rappel automatique la veille, par texto.",
    ],
    bonBesoin: 0,
    sorte: "decision",
    relance: "« Que voulez-vous qu'il arrive quand une commande n'est pas ramassée ? »",
    explication:
      "Aucun outil ne règle ça tant que la propriétaire n'a pas choisi sa règle. C'est une décision d'affaires : elle va au compte rendu, avec une date pour la prendre. Le rappel par texto peut aider, mais il ne décide rien.",
  },
  {
    cle: "p4",
    phrase: "« Mes clients sont âgés : il faut que ce soit gros. »",
    besoins: [
      "Une police de 24 points partout sur le site.",
      "Que des personnes qui voient moins bien puissent lire et commander sans aide.",
      "Une version spéciale du site pour les personnes âgées.",
    ],
    bonBesoin: 1,
    sorte: "comment",
    relance: "« Qu'est-ce qui leur donne du mal aujourd'hui ? »",
    explication:
      "« Gros » est sa façon de dire « lisible ». C'est une qualité du site : contraste, texte qu'on peut agrandir, gros boutons. Ce sont des règles d'accessibilité, pas une fonction de plus.",
  },
  {
    cle: "p5",
    phrase: "« Mettez-moi un clavardage sur le site. »",
    besoins: [
      "Que les clients trouvent seuls les réponses à leurs questions (allergènes, sans gluten), sans appeler.",
      "Une fenêtre de clavardage, ouverte de 6 h à 18 h.",
      "Un robot conversationnel qui répond à sa place.",
    ],
    bonBesoin: 0,
    sorte: "quoi",
    relance: "« Quelles questions vos clients vous posent-ils le plus souvent ? »",
    explication:
      "Encore une solution. Le vrai problème : toujours les mêmes questions au comptoir. Si ce sont les allergènes, une fiche par produit y répond, sans que personne ait à surveiller une fenêtre de clavardage toute la journée.",
  },
  {
    cle: "p6",
    phrase: "« Je ne sais pas encore jusqu'à quelle heure on prend les commandes. »",
    besoins: [
      "Un compte à rebours sur la page d'accueil.",
      "Que le site ferme les commandes tout seul.",
      "Une heure limite à choisir, selon le temps de préparation.",
    ],
    bonBesoin: 2,
    sorte: "decision",
    relance: "« Jusqu'à quelle heure pouvez-vous préparer une commande pour le lendemain ? »",
    explication:
      "L'outil saura fermer les commandes, mais à quelle heure ? Ça dépend de la boulangère et de son four. Tant qu'elle n'a pas choisi, c'est un point « à éclaircir », avec une date.",
  },
];

const props = withDefaults(defineProps<{ storageKey?: string }>(), {
  storageKey: "boulangerie-ce-quelle-veut",
});

const besoin = reactive<Record<string, number | null>>(Object.fromEntries(PHRASES.map((p) => [p.cle, null])));
const sorte = reactive<Record<string, Sorte | "">>(Object.fromEntries(PHRASES.map((p) => [p.cle, ""])));
const verifie = ref(false);

const nbBons = computed(
  () => PHRASES.filter((p) => besoin[p.cle] === p.bonBesoin).length + PHRASES.filter((p) => sorte[p.cle] === p.sorte).length,
);

function texteReponses() {
  const l = ["Séance 9 — Activité 1 : ce qu'elle dit, ce qu'elle veut (la boulangerie)", ""];
  PHRASES.forEach((p, i) => {
    const b = besoin[p.cle];
    l.push(`${i + 1}. ${p.phrase}`);
    l.push(`   Le vrai besoin : ${b === null ? "—" : p.besoins[b]}`);
    l.push(`   La sorte : ${sorte[p.cle] ? SORTES[sorte[p.cle] as Sorte] : "—"}`);
    if (verifie.value) {
      l.push(`   Correction : ${p.besoins[p.bonBesoin]} · ${SORTES[p.sorte]}`);
      l.push(`   La question à poser : ${p.relance}`);
      l.push(`   ${p.explication}`);
    }
    l.push("");
  });
  return l.join("\n");
}

function reinitialiser() {
  if (!confirm("Effacer vos réponses ?")) return;
  for (const p of PHRASES) {
    besoin[p.cle] = null;
    sorte[p.cle] = "";
  }
  verifie.value = false;
}

onMounted(() => {
  try {
    const data = JSON.parse(localStorage.getItem(props.storageKey) ?? "null");
    if (!data) return;
    for (const p of PHRASES) {
      const b = data.besoin?.[p.cle];
      besoin[p.cle] = typeof b === "number" && b >= 0 && b < p.besoins.length ? b : null;
      const s = data.sorte?.[p.cle];
      sorte[p.cle] = s in SORTES ? s : "";
    }
    verifie.value = data.verifie === true;
  } catch {
    /* stockage indisponible : on part de réponses vides */
  }
});

watch([besoin, sorte, verifie], () => {
  try {
    localStorage.setItem(props.storageKey, JSON.stringify({ besoin, sorte, verifie: verifie.value }));
  } catch {
    /* stockage indisponible : rien à faire */
  }
});
</script>

<template>
  <section class="cq">
    <ol class="cq-liste">
      <li v-for="(p, i) in PHRASES" :key="p.cle" class="cq-carte">
        <p class="cq-phrase"><span class="cq-num">{{ i + 1 }}</span>{{ p.phrase }}</p>

        <p class="cq-q">Que veut-elle vraiment ?</p>
        <div class="cq-choix cq-col" role="radiogroup" :aria-label="'Le vrai besoin, phrase ' + (i + 1)">
          <label
            v-for="(b, j) in p.besoins"
            :key="j"
            :class="verifie && besoin[p.cle] === j ? (j === p.bonBesoin ? 'is-bon' : 'is-mauvais') : verifie && j === p.bonBesoin ? 'is-attendu' : ''"
          >
            <input v-model="besoin[p.cle]" type="radio" :value="j" :name="'cq-b-' + p.cle" /> {{ b }}
          </label>
        </div>

        <p class="cq-q">Qu'est-ce que c'est ?</p>
        <div class="cq-choix" role="radiogroup" :aria-label="'La sorte de réponse, phrase ' + (i + 1)">
          <label
            v-for="(nom, s) in SORTES"
            :key="s"
            :class="verifie && sorte[p.cle] === s ? (s === p.sorte ? 'is-bon' : 'is-mauvais') : verifie && s === p.sorte ? 'is-attendu' : ''"
          >
            <input v-model="sorte[p.cle]" type="radio" :value="s" :name="'cq-s-' + p.cle" /> {{ nom }}
          </label>
        </div>

        <div v-if="verifie" class="cq-corr">
          <p><strong>La question à poser :</strong> {{ p.relance }}</p>
          <p class="cq-expl">{{ p.explication }}</p>
        </div>
      </li>
    </ol>

    <div class="cq-boutons">
      <button type="button" class="cq-action is-principal" @click="verifie = true">Vérifier</button>
      <span v-if="verifie" class="cq-score">Bonnes réponses : {{ nbBons }} sur {{ PHRASES.length * 2 }}.</span>
    </div>

    <p class="cq-rappel">Vos réponses restent dans ce navigateur, mais elles peuvent disparaître si la cache est vidée. <strong>Copiez-les dans vos notes</strong> avant de quitter la page.</p>
    <div class="cq-pied">
      <BoutonCopier :texte="texteReponses" />
      <button type="button" class="cq-action" @click="reinitialiser">Recommencer</button>
    </div>
  </section>
</template>

<style scoped>
.cq {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
  font-size: 0.875rem;
}
.cq-liste {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 0.6rem;
  margin: 0 !important;
  padding: 0 !important;
  list-style: none;
}
.cq-carte {
  margin: 0 !important;
  padding: 0.75rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.75rem;
  background: var(--vp-c-bg);
}
.cq-phrase {
  display: flex;
  gap: 0.5rem;
  align-items: flex-start;
  margin: 0 0 0.4rem !important;
  font-weight: 600;
  line-height: 1.4;
}
.cq-num {
  display: grid;
  place-items: center;
  flex-shrink: 0;
  width: 1.6rem;
  height: 1.6rem;
  border-radius: 50%;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-size: 0.8rem;
}
.cq-q { margin: 0.45rem 0 0.15rem !important; font-size: 0.75rem; font-weight: 600; color: var(--vp-c-text-2); }
.cq-choix { display: flex; flex-wrap: wrap; gap: 0.25rem 0.9rem; font-size: 0.8rem; }
.cq-col { flex-direction: column; }
.cq-choix label {
  display: inline-flex;
  gap: 0.35rem;
  align-items: flex-start;
  padding: 0.1rem 0.3rem;
  border-radius: 0.35rem;
  line-height: 1.4;
  cursor: pointer;
}
.cq-choix input { margin-top: 0.2rem; accent-color: var(--vp-c-brand-1); }
.cq-choix .is-bon { background: var(--vp-c-green-soft); }
.cq-choix .is-mauvais { background: var(--vp-c-red-soft); }
.cq-choix .is-attendu { outline: 1px dashed var(--vp-c-green-2); }
.cq-corr {
  margin-top: 0.55rem;
  padding-top: 0.55rem;
  border-top: 1px dashed var(--vp-c-divider);
  font-size: 0.8rem;
  line-height: 1.5;
}
.cq-corr p { margin: 0 !important; }
.cq-expl { margin-top: 0.3rem !important; color: var(--vp-c-text-2); }
.cq-boutons { display: flex; flex-wrap: wrap; gap: 0.6rem; align-items: center; margin-top: 0.75rem; }
.cq-score { font-size: 0.8rem; color: var(--vp-c-text-2); }
.cq-action {
  padding: 0.3rem 0.8rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.cq-action:hover { border-color: var(--vp-c-brand-1); }
.cq-action.is-principal { border-color: var(--vp-c-brand-1); color: var(--vp-c-brand-1); font-weight: 600; }
.cq-rappel { margin: 0.75rem 0 0.6rem !important; font-size: 0.78rem; color: var(--vp-c-text-2); }
.cq-pied {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
}
</style>
