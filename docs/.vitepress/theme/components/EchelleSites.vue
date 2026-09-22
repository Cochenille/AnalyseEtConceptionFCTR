<script setup lang="ts">
import { ref } from "vue";

type Niveau = { niveau: number; texte: string };
type Site = {
  lettre: string;
  nom: string;
  fait: string;
  construction: Niveau;
  delai: Niveau;
  equipe: Niveau;
  annuel: Niveau;
};

const SITES: Site[] = [
  {
    lettre: "A",
    nom: "Café de quartier",
    fait: "Une page : photos, heures, adresse, lien Facebook",
    construction: { niveau: 1, texte: "0 $ à quelques centaines de $" },
    delai: { niveau: 1, texte: "Une fin de semaine" },
    equipe: { niveau: 1, texte: "1 personne" },
    annuel: { niveau: 1, texte: "Quelques centaines de $" },
  },
  {
    lettre: "B",
    nom: "Bistro gastronomique",
    fait: "Plusieurs pages, menu saisonnier, réservation, bilingue",
    construction: { niveau: 3, texte: "Quelques milliers à ~15 000 $" },
    delai: { niveau: 3, texte: "Quelques semaines" },
    equipe: { niveau: 2, texte: "1 à 3 personnes" },
    annuel: { niveau: 3, texte: "Centaines à milliers de $" },
  },
  {
    lettre: "C",
    nom: "Chaîne de 60 restaurants",
    fait: "Commande en ligne, fidélité, compte client, appli mobile",
    construction: { niveau: 5, texte: "Dizaines à centaines de milliers de $" },
    delai: { niveau: 5, texte: "Plusieurs mois" },
    equipe: { niveau: 5, texte: "Une équipe complète" },
    annuel: { niveau: 5, texte: "Dizaines de milliers de $" },
  },
];

const DIMENSIONS: { cle: "construction" | "delai" | "equipe" | "annuel"; titre: string }[] = [
  { cle: "construction", titre: "Construction" },
  { cle: "delai", titre: "Délai" },
  { cle: "equipe", titre: "Équipe" },
  { cle: "annuel", titre: "Chaque année" },
];

const revele = ref(false);
</script>

<template>
  <section class="es">
    <div class="es-grille">
      <article v-for="s in SITES" :key="s.lettre" class="es-carte">
        <header class="es-tete">
          <span class="es-lettre">{{ s.lettre }}</span>
          <div>
            <h4 class="es-nom">{{ s.nom }}</h4>
            <p class="es-fait">{{ s.fait }}</p>
          </div>
        </header>

        <!-- Petite maquette : la « taille » du site grossit de A à C -->
        <div class="es-maquette" aria-hidden="true">
          <span
            v-for="n in s.construction.niveau * 2 - 1"
            :key="n"
            class="es-page"
          ></span>
        </div>

        <dl class="es-dims">
          <div v-for="d in DIMENSIONS" :key="d.cle" class="es-dim">
            <dt>{{ d.titre }}</dt>
            <dd>
              <span class="es-barre">
                <span
                  class="es-rempli"
                  :style="{ width: revele ? s[d.cle].niveau * 20 + '%' : '0%' }"
                ></span>
              </span>
              <span class="es-valeur" :class="{ 'is-cache': !revele }">
                {{ revele ? s[d.cle].texte : "?" }}
              </span>
            </dd>
          </div>
        </dl>
      </article>
    </div>

    <div class="es-actions">
      <button type="button" class="es-btn" @click="revele = !revele">
        {{ revele ? "Masquer les ordres de grandeur" : "Révéler les ordres de grandeur" }}
      </button>
      <span class="es-note">À ouvrir après la discussion. Ce sont des ordres de grandeur, pas des prix à citer.</span>
    </div>
  </section>
</template>

<style scoped>
.es {
  margin: 1.25rem 0 1.75rem;
}
.es-grille {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 0.75rem;
}
.es-carte {
  padding: 0.9rem 1rem 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.9rem;
  background: var(--vp-c-bg-soft);
}
.es-tete {
  display: flex;
  gap: 0.65rem;
  align-items: flex-start;
}
.es-lettre {
  flex-shrink: 0;
  display: grid;
  place-items: center;
  width: 2rem;
  height: 2rem;
  border-radius: 0.6rem;
  background: var(--vp-c-brand-1);
  color: var(--vp-c-white);
  font-weight: 700;
}
.es-nom {
  margin: 0 !important;
  font-size: 0.95rem;
  font-weight: 600;
  line-height: 1.3;
}
.es-fait {
  margin: 0.2rem 0 0 !important;
  font-size: 0.78rem;
  line-height: 1.4;
  color: var(--vp-c-text-2);
}
.es-maquette {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  min-height: 42px;
  margin: 0.75rem 0 0.5rem;
  align-content: flex-start;
}
.es-page {
  width: 16px;
  height: 19px;
  border-radius: 3px;
  border: 1px solid var(--vp-c-brand-2);
  background: linear-gradient(
    var(--vp-c-brand-soft) 0 5px,
    var(--vp-c-bg) 5px
  );
}
.es-dims {
  margin: 0;
}
.es-dim + .es-dim {
  margin-top: 0.5rem;
}
.es-dim dt {
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--vp-c-text-2);
}
.es-dim dd {
  margin: 0.15rem 0 0;
}
.es-barre {
  display: block;
  height: 6px;
  border-radius: 999px;
  background: var(--vp-c-default-soft);
  overflow: hidden;
}
.es-rempli {
  display: block;
  height: 100%;
  border-radius: 999px;
  background: var(--vp-c-brand-1);
  transition: width 0.7s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.es-valeur {
  display: block;
  margin-top: 0.15rem;
  font-size: 0.8rem;
  line-height: 1.35;
  color: var(--vp-c-text-1);
}
.es-valeur.is-cache {
  color: var(--vp-c-text-3);
}
.es-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem 0.9rem;
  margin-top: 0.8rem;
}
.es-btn {
  padding: 0.45rem 0.9rem;
  border-radius: 0.65rem;
  border: 1px solid var(--vp-c-brand-1);
  background: var(--vp-c-brand-1);
  color: var(--vp-c-white);
  font-size: 0.85rem;
  font-weight: 600;
}
.es-btn:hover {
  background: var(--vp-c-brand-2);
}
.es-note {
  font-size: 0.78rem;
  color: var(--vp-c-text-2);
}
@media (prefers-reduced-motion: reduce) {
  .es-rempli {
    transition: none;
  }
}
</style>
