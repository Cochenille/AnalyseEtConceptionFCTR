<script setup lang="ts">
import { computed, onMounted, reactive, watch } from "vue";
import BoutonCopier from "./BoutonCopier.vue";

// Séance 7, activité 1 : choisir le format de chaque fichier envoyé par Patrick.
const FORMATS = ["JPEG", "PNG", "WebP", "AVIF", "SVG", "MP4", "WebM", "PDF", "WOFF2", "Page Web"] as const;
type Format = (typeof FORMATS)[number];

type Cas = { quoi: string; ou: string; bons: Format[]; acceptables: Format[]; pourquoi: string };

const CAS: Cas[] = [
  {
    quoi: "Le logo. Le neveu a envoyé deux fichiers : un PNG de 3000 × 3000 px et un SVG.",
    ou: "En haut de chaque page, à environ 200 px de large.",
    bons: ["SVG"],
    acceptables: ["PNG", "WebP"],
    pourquoi: "Un logo est un dessin fait de formes et d'aplats. En SVG, il reste net à toutes les tailles et sur tous les écrans, et il pèse quelques Ko. Un PNG réduit à 400 px (deux fois la largeur affichée) reste un repli acceptable si on n'a pas de SVG.",
  },
  {
    quoi: "La photo du coucher de soleil sur la rivière, prise au reflex : 6000 × 4000 px, 6,7 Mo.",
    ou: "En haut de la page d'accueil, sur toute la largeur de l'écran.",
    bons: ["WebP", "AVIF"],
    acceptables: ["JPEG"],
    pourquoi: "Une photo se compresse avec perte. WebP est lu par tous les navigateurs actuels et pèse environ 25 à 35 % de moins qu'un JPEG de même qualité. AVIF va plus loin, mais il est plus lent à produire. JPEG fonctionne partout, en plus lourd. Dans tous les cas, on réduit d'abord la photo à 1920 px de large : c'est là que se fait le plus gros gain.",
  },
  {
    quoi: "La photo du nouveau kayak adapté, prise avec l'iPhone de Patrick : un fichier .HEIC.",
    ou: "Sur la page de l'offre adaptée, dans le texte.",
    bons: ["WebP", "AVIF"],
    acceptables: ["JPEG"],
    pourquoi: "HEIC est le format des photos d'iPhone. Presque aucun navigateur ne l'affiche, à part Safari : la photo serait invisible pour la majorité des visiteurs. On la convertit, comme n'importe quelle autre photo.",
  },
  {
    quoi: "La carte des deux parcours de via ferrata : des aplats de couleur, des lignes et du texte. Exportée de PowerPoint en PNG de 3600 × 2400 px.",
    ou: "Sur la page Via ferrata.",
    bons: ["PNG", "WebP"],
    acceptables: ["SVG", "AVIF"],
    pourquoi: "Des aplats et du texte : la compression avec perte d'un JPEG ferait des bavures autour des lettres. On garde un PNG réduit en couleurs (TinyPNG le fait) ou un WebP sans perte. Un AVIF sans perte fonctionne aussi, mais pour ce genre d'image il pèse souvent plus qu'un WebP, et il demande un repli. Un SVG serait parfait si on redessinait la carte, mais on ne reçoit qu'une image. Et le texte de la carte doit aussi se trouver dans la page.",
  },
  {
    quoi: "L'extrait de drone de Patrick : un fichier .MOV en 4K, avec le bruit du vent.",
    ou: "En arrière-plan de la page d'accueil, en boucle, sans son.",
    bons: ["MP4", "WebM"],
    acceptables: [],
    pourquoi: "Une vidéo, jamais un GIF animé. MP4 (en H.264) est lu partout; WebM est souvent plus léger. On peut offrir les deux : le navigateur prend le premier qu'il sait lire. On retire le son, on réduit à 1920 px au plus et on vise quelques Mo. Le .MOV d'origine n'est pas lu par tous les navigateurs.",
  },
  {
    quoi: "La grille des tarifs 2027, que Mélanie a numérisée : un PDF de deux pages fait d'images.",
    ou: "Sur la page Tarifs.",
    bons: ["Page Web"],
    acceptables: [],
    pourquoi: "Une information que tout le monde doit lire, et que Mélanie devra changer chaque année, va dans la page, en texte. Un PDF numérisé est une image : un lecteur d'écran ne peut pas le lire, Google l'indexe mal, et il est pénible à consulter sur un téléphone.",
  },
  {
    quoi: "Le formulaire de soumission pour les groupes, que les écoles impriment, font signer par la direction et renvoient.",
    ou: "Sur la page Groupes, en téléchargement.",
    bons: ["PDF"],
    acceptables: ["Page Web"],
    pourquoi: "Un document qu'on imprime, signe et renvoie tel quel : c'est le rôle du PDF. On le produit à partir de Word (du vrai texte, pas une numérisation), idéalement à remplir à l'écran. Un formulaire en ligne serait aussi possible, mais il ne remplace pas la signature de la direction.",
  },
  {
    quoi: "La police de caractères des titres, que Patrick a achetée en 2019 : un fichier .otf.",
    ou: "Pour tous les titres du site.",
    bons: ["WOFF2"],
    acceptables: [],
    pourquoi: "WOFF2 est le format compressé des polices pour le Web, lu par tous les navigateurs actuels. Avant de la mettre en ligne, il faut vérifier que la licence achetée en 2019 permet l'usage sur un site Web : ce n'est pas toujours le cas.",
  },
];

const props = withDefaults(defineProps<{ storageKey?: string }>(), {
  storageKey: "asm-quel-format",
});

const etat = reactive(CAS.map(() => ({ choix: null as Format | null, raison: "" })));

const verdict = (n: number): "bon" | "acceptable" | "mauvais" | null => {
  const c = etat[n].choix;
  if (!c) return null;
  if (CAS[n].bons.includes(c)) return "bon";
  if (CAS[n].acceptables.includes(c)) return "acceptable";
  return "mauvais";
};

const score = computed(() => CAS.filter((_, n) => verdict(n) === "bon").length);
const repondus = computed(() => etat.filter((e) => e.choix).length);

const liste = (f: Format[]) => (f.length ? f.join(" ou ") : "—");

function texteReponses() {
  return [
    "Séance 7 — Activité 1 : quel format pour quel fichier ?",
    "",
    ...CAS.map((x, n) => {
      const e = etat[n];
      return [
        `${n + 1}. ${x.quoi} (${x.ou})`,
        `   Notre choix : ${e.choix ?? "—"} — attendu : ${liste(x.bons)}${x.acceptables.length ? ` (acceptable : ${liste(x.acceptables)})` : ""}`,
        `   Notre raison : ${e.raison.trim() || "—"}`,
        `   Explication : ${x.pourquoi}`,
      ].join("\n");
    }),
  ].join("\n\n");
}

function reinitialiser() {
  if (!confirm("Effacer toutes vos réponses ? Avez-vous copié vos réponses ?")) return;
  for (const e of etat) Object.assign(e, { choix: null, raison: "" });
}

onMounted(() => {
  try {
    const data = JSON.parse(localStorage.getItem(props.storageKey) ?? "null");
    if (!Array.isArray(data)) return;
    etat.forEach((e, n) => {
      const v = data[n];
      if (!v) return;
      e.choix = FORMATS.includes(v.choix) ? v.choix : null;
      e.raison = String(v.raison ?? "");
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
  <section class="qf">
    <ol class="qf-liste">
      <li v-for="(x, n) in CAS" :key="n" class="qf-item">
        <p class="qf-quoi">{{ x.quoi }}</p>
        <p class="qf-ou"><span>Où :</span> {{ x.ou }}</p>
        <div class="qf-boutons" role="group" :aria-label="'Format pour le fichier ' + (n + 1)">
          <button
            v-for="f in FORMATS"
            :key="f"
            type="button"
            class="qf-btn"
            :class="etat[n].choix === f ? 'is-' + verdict(n) : etat[n].choix && x.bons.includes(f) ? 'is-attendu' : ''"
            :aria-pressed="etat[n].choix === f"
            @click="etat[n].choix = f"
          >
            {{ f }}
          </button>
        </div>
        <label class="qf-label" :for="'qf-r-' + n">Pourquoi ce format ? (en une phrase, avant de lire l'explication)</label>
        <textarea :id="'qf-r-' + n" v-model="etat[n].raison" class="qf-zone" rows="1" />
        <p v-if="verdict(n)" class="qf-retro" :class="'is-' + verdict(n)">
          <strong>{{ verdict(n) === "bon" ? "Oui." : verdict(n) === "acceptable" ? "Acceptable, mais " + liste(x.bons) + " ferait mieux." : "Plutôt " + liste(x.bons) + "." }}</strong>
          {{ x.pourquoi }}
        </p>
      </li>
    </ol>

    <p class="qf-rappel">Vos réponses restent dans ce navigateur, mais elles peuvent disparaître si la cache est vidée. <strong>Copiez-les dans vos notes</strong> avant de quitter la page.</p>
    <div class="qf-pied">
      <span>
        <strong>{{ score }} / {{ CAS.length }}</strong> meilleurs choix
        <span v-if="repondus < CAS.length" class="qf-reste">({{ CAS.length - repondus }} à faire)</span>
      </span>
      <span class="qf-actions">
        <BoutonCopier :texte="texteReponses" />
        <button type="button" class="qf-action" @click="reinitialiser">Recommencer</button>
      </span>
    </div>
  </section>
</template>

<style scoped>
.qf {
  margin: 1.25rem 0 1.75rem;
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.qf-liste { margin: 0 !important; padding-left: 1.25rem !important; }
.qf-item { margin: 0 !important; padding: 0.8rem 0; border-top: 1px solid var(--vp-c-divider); }
.qf-item:first-child { border-top: 0; padding-top: 0; }
.qf-quoi { margin: 0 !important; font-weight: 600; line-height: 1.45; }
.qf-ou { margin: 0.15rem 0 0 !important; font-size: 0.85rem; color: var(--vp-c-text-2); }
.qf-ou span { font-weight: 600; }
.qf-boutons { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.5rem; }
.qf-btn {
  padding: 0.25rem 0.7rem;
  border-radius: 999px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
  font-weight: 600;
  transition: border-color 0.15s, background-color 0.15s;
}
.qf-btn:hover { border-color: var(--vp-c-brand-1); }
.qf-btn.is-bon { border-color: var(--vp-c-green-2); background: var(--vp-c-green-soft); color: var(--vp-c-green-1); }
.qf-btn.is-acceptable { border-color: var(--vp-c-yellow-2); background: var(--vp-c-yellow-soft); color: var(--vp-c-yellow-1); }
.qf-btn.is-mauvais { border-color: var(--vp-c-red-2); background: var(--vp-c-red-soft); color: var(--vp-c-red-1); }
.qf-btn.is-attendu { border-style: dashed; border-color: var(--vp-c-green-2); }
.qf-label { display: block; margin: 0.5rem 0 0.2rem; font-size: 0.75rem; font-weight: 600; color: var(--vp-c-text-2); }
.qf-zone {
  width: 100%;
  padding: 0.4rem 0.55rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.5rem;
  background: var(--vp-c-bg);
  font: inherit;
  font-size: 0.85rem;
  resize: vertical;
}
.qf-zone:focus { outline: none; border-color: var(--vp-c-brand-1); }
.qf-retro { margin: 0.45rem 0 0 !important; font-size: 0.82rem; line-height: 1.5; color: var(--vp-c-text-2); }
.qf-retro.is-bon strong { color: var(--vp-c-green-1); }
.qf-retro.is-acceptable strong { color: var(--vp-c-yellow-1); }
.qf-retro.is-mauvais strong { color: var(--vp-c-red-1); }
.qf-rappel { margin: 0.5rem 0 0.6rem !important; font-size: 0.78rem; color: var(--vp-c-text-2); }
.qf-pied {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
  font-size: 0.875rem;
}
.qf-reste { color: var(--vp-c-text-2); }
.qf-actions { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.qf-action {
  padding: 0.3rem 0.7rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  font-size: 0.8rem;
}
.qf-action:hover { border-color: var(--vp-c-brand-1); }
</style>
