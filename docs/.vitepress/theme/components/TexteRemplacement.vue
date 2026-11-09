<script setup lang="ts">
import { computed, onMounted, reactive, watch } from "vue";
import BoutonCopier from "./BoutonCopier.vue";

// Séance 7, activité 2 : choisir le meilleur texte de remplacement (attribut alt).
type Cas = { image: string; contexte: string; options: string[]; bon: number; pourquoi: string };

const VIDE = "(alt vide) — l'image est décorative";

const CAS: Cas[] = [
  {
    image: "La photo du kayak adapté, au quai : coque jaune, siège à dossier haut, deux flotteurs de chaque côté.",
    contexte: "Page « Offre adaptée », sous le titre « Des kayaks pour tout le monde ».",
    options: [
      "IMG_4540.HEIC",
      "Kayak adapté avec siège à dossier haut et deux flotteurs stabilisateurs, au quai du centre.",
      "Image d'un kayak",
    ],
    bon: 1,
    pourquoi: "La photo informe : elle montre à quoi ressemble l'équipement adapté, ce qui intéresse justement les personnes ayant une incapacité. Le nom du fichier ne dit rien, et « Image de » est inutile : le lecteur d'écran annonce déjà qu'il s'agit d'une image.",
  },
  {
    image: "Le logo d'Aventure Saint-Maurice : deux montagnes et trois vagues dans un cercle.",
    contexte: "En haut de chaque page. Un clic sur le logo ramène à l'accueil.",
    options: [
      "Aventure Saint-Maurice — accueil",
      "Logo",
      "Logo rond vert et beige avec deux montagnes enneigées et trois vagues bleues",
    ],
    bon: 0,
    pourquoi: "Quand une image sert de lien, son texte de remplacement dit où mène le lien. La description du dessin n'aide personne à naviguer, et « Logo » ne dit pas de qui ni vers où.",
  },
  {
    image: "La photo du coucher de soleil sur la rivière, en plein écran.",
    contexte: "Arrière-plan de l'accueil, sous le grand titre « Pagayez la Saint-Maurice » et le bouton « Réserver ».",
    options: [
      "Photo de la rivière",
      "kayak rivière Saint-Maurice Mauricie plein air coucher de soleil meilleur prix",
      VIDE,
    ],
    bon: 2,
    pourquoi: "Ici, la photo est un décor : le titre et le bouton portent le message. Un alt vide indique au lecteur d'écran de la sauter. L'option B est du bourrage de mots-clés : pénible à entendre, et Google ne s'y laisse plus prendre. Une courte description (« Coucher de soleil sur la rivière Saint-Maurice ») resterait défendable si l'équipe juge que l'ambiance fait partie du message.",
  },
  {
    image: "La carte des deux parcours de via ferrata, avec les distances, les durées et les âges minimums.",
    contexte: "Page Via ferrata. Sous la carte, un tableau reprend les deux parcours.",
    options: [
      "Carte montrant le parcours 1 Les Marmites en vert de 1,2 km d'environ 2 h facile dès 10 ans et le parcours 2 La Falaise en rouge de 2 km d'environ 3 h 30 difficile dès 14 ans, avec l'accueil, le stationnement, le pont suspendu et la rivière",
      "Carte",
      "Carte des deux parcours de via ferrata, à partir de l'accueil. Le détail des parcours est dans le tableau sous la carte.",
    ],
    bon: 2,
    pourquoi: "L'option A n'est pas fausse, mais le texte de remplacement n'est pas fait pour un long texte, et seules les personnes qui utilisent un lecteur d'écran en profiteraient. L'information importante (distances, durées, âges) doit être dans la page, pour tout le monde; le texte de remplacement présente l'image et renvoie au tableau.",
  },
  {
    image: "Une petite icône de vague, à côté du lien « Excursions sur l'eau » dans le menu.",
    contexte: "Menu principal.",
    options: ["Icône de vague", VIDE, "Excursions sur l'eau"],
    bon: 1,
    pourquoi: "L'icône ne fait que décorer un lien qui a déjà son texte. Avec « Excursions sur l'eau », le lecteur d'écran lirait le nom deux fois; avec « Icône de vague », il ajouterait un bruit inutile à chaque page.",
  },
  {
    image: "Un groupe de jeunes d'un camp de jour dans un rabaska, avec une guide.",
    contexte: "Page Groupes, à côté du texte sur les sorties scolaires et les camps de jour.",
    options: [
      "Un groupe de jeunes d'un camp de jour pagaie en rabaska avec une guide.",
      "Les enfants du camp de jour Les P'tits Loups de Shawinigan avec Léa, notre guide",
      "Enfants",
    ],
    bon: 0,
    pourquoi: "On décrit ce que la photo apporte : les groupes de jeunes sont bienvenus et encadrés. Les noms des enfants et de leur camp n'ont rien à faire sur le site. Et avant même d'écrire le texte de remplacement : des enfants qu'on peut reconnaître sur une photo, c'est l'autorisation écrite des parents, pour chacun.",
  },
];

const props = withDefaults(defineProps<{ storageKey?: string }>(), {
  storageKey: "asm-texte-remplacement",
});

const etat = reactive(CAS.map(() => ({ choix: null as number | null, version: "" })));

const score = computed(() => etat.filter((e, n) => e.choix === CAS[n].bon).length);
const repondus = computed(() => etat.filter((e) => e.choix !== null).length);

const lettre = (i: number | null) => (i === null ? "—" : "ABC"[i]);

function texteReponses() {
  return [
    "Séance 7 — Activité 2 : le texte de remplacement",
    "",
    ...CAS.map((x, n) => {
      const e = etat[n];
      return [
        `${n + 1}. ${x.image} (${x.contexte})`,
        `   Notre choix : ${lettre(e.choix)}${e.choix !== null ? ` — « ${x.options[e.choix]} »` : ""}`,
        `   Le meilleur : ${lettre(x.bon)} — « ${x.options[x.bon]} »`,
        `   Notre version : ${e.version.trim() || "—"}`,
        `   Pourquoi : ${x.pourquoi}`,
      ].join("\n");
    }),
  ].join("\n\n");
}

function reinitialiser() {
  if (!confirm("Effacer toutes vos réponses ? Avez-vous copié vos réponses ?")) return;
  for (const e of etat) Object.assign(e, { choix: null, version: "" });
}

onMounted(() => {
  try {
    const data = JSON.parse(localStorage.getItem(props.storageKey) ?? "null");
    if (!Array.isArray(data)) return;
    etat.forEach((e, n) => {
      const v = data[n];
      if (!v) return;
      e.choix = [0, 1, 2].includes(v.choix) ? v.choix : null;
      e.version = String(v.version ?? "");
    });
  } catch {
    /* stockage indisponible : on part de réponses vides */
  }
});

watch(etat, () => {
  try {
    localStorage.setItem(props.storageKey, JSON.stringify(etat));
  } catch {
    /* stockage indisponible : rien à faire */
  }
});
</script>

<template>
  <section class="tr">
    <ol class="tr-liste">
      <li v-for="(x, n) in CAS" :key="n" class="tr-item">
        <p class="tr-image">{{ x.image }}</p>
        <p class="tr-contexte"><span>Où :</span> {{ x.contexte }}</p>
        <div class="tr-options" role="radiogroup" :aria-label="'Texte de remplacement pour l\'image ' + (n + 1)">
          <button
            v-for="(o, i) in x.options"
            :key="i"
            type="button"
            role="radio"
            class="tr-option"
            :class="{
              'is-bon': etat[n].choix !== null && i === x.bon,
              'is-mauvais': etat[n].choix === i && i !== x.bon,
            }"
            :aria-checked="etat[n].choix === i"
            @click="etat[n].choix = i"
          >
            <span class="tr-lettre">{{ "ABC"[i] }}</span>
            <code v-if="o !== VIDE">alt="{{ o }}"</code>
            <span v-else><code>alt=""</code> — l'image est décorative</span>
          </button>
        </div>
        <template v-if="etat[n].choix !== null">
          <p class="tr-retro" :class="etat[n].choix === x.bon ? 'is-bon' : 'is-mauvais'">
            <strong>{{ etat[n].choix === x.bon ? "Oui." : "Plutôt " + "ABC"[x.bon] + "." }}</strong>
            {{ x.pourquoi }}
          </p>
          <label class="tr-label" :for="'tr-v-' + n">Votre version, si vous écririez autre chose (facultatif)</label>
          <textarea :id="'tr-v-' + n" v-model="etat[n].version" class="tr-zone" rows="1" />
        </template>
      </li>
    </ol>

    <p class="tr-rappel">Vos réponses restent dans ce navigateur, mais elles peuvent disparaître si la cache est vidée. <strong>Copiez-les dans vos notes</strong> avant de quitter la page.</p>
    <div class="tr-pied">
      <span>
        <strong>{{ score }} / {{ CAS.length }}</strong> bons choix
        <span v-if="repondus < CAS.length" class="tr-reste">({{ CAS.length - repondus }} à faire)</span>
      </span>
      <span class="tr-actions">
        <BoutonCopier :texte="texteReponses" />
        <button type="button" class="tr-action" @click="reinitialiser">Recommencer</button>
      </span>
    </div>
  </section>
</template>

<style scoped>
.tr {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.tr-liste { margin: 0 !important; padding-left: 1.25rem !important; }
.tr-item { margin: 0 !important; padding: 0.8rem 0; border-top: 1px solid var(--vp-c-divider); }
.tr-item:first-child { border-top: 0; padding-top: 0; }
.tr-image { margin: 0 !important; font-weight: 600; line-height: 1.45; }
.tr-contexte { margin: 0.15rem 0 0 !important; font-size: 0.85rem; color: var(--vp-c-text-2); }
.tr-contexte span { font-weight: 600; }
.tr-options { display: grid; gap: 0.35rem; margin-top: 0.5rem; }
.tr-option {
  display: flex;
  gap: 0.55rem;
  align-items: baseline;
  width: 100%;
  padding: 0.45rem 0.65rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.55rem;
  background: var(--vp-c-bg);
  text-align: left;
  font-size: 0.84rem;
  line-height: 1.45;
  transition: border-color 0.15s, background-color 0.15s;
}
.tr-option:hover { border-color: var(--vp-c-brand-1); }
.tr-option code { white-space: normal; word-break: break-word; }
.tr-option.is-bon { border-color: var(--vp-c-green-2); background: var(--vp-c-green-soft); }
.tr-option.is-mauvais { border-color: var(--vp-c-red-2); background: var(--vp-c-red-soft); }
.tr-lettre { flex: none; font-weight: 700; color: var(--vp-c-text-2); }
.tr-retro { margin: 0.45rem 0 0 !important; font-size: 0.82rem; line-height: 1.5; color: var(--vp-c-text-2); }
.tr-retro.is-bon strong { color: var(--vp-c-green-1); }
.tr-retro.is-mauvais strong { color: var(--vp-c-red-1); }
.tr-label { display: block; margin: 0.5rem 0 0.2rem; font-size: 0.75rem; font-weight: 600; color: var(--vp-c-text-2); }
.tr-zone {
  width: 100%;
  padding: 0.4rem 0.55rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.5rem;
  background: var(--vp-c-bg);
  font: inherit;
  font-size: 0.85rem;
  resize: vertical;
}
.tr-zone:focus { outline: none; border-color: var(--vp-c-brand-1); }
.tr-rappel { margin: 0.5rem 0 0.6rem !important; font-size: 0.78rem; color: var(--vp-c-text-2); }
.tr-pied {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.875rem;
}
.tr-reste { color: var(--vp-c-text-2); }
.tr-actions { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.tr-action {
  padding: 0.3rem 0.7rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.tr-action:hover { border-color: var(--vp-c-brand-1); }
</style>
