---
layout: home
title: 582-A05-RI — Analyse et conception Web
hero:
  name: 582-A05-RI — Analyse et conception Web
  text: Automne 2026 — Bloc 1
  tagline: AEC Techniques de conception Web — Cégep de Trois-Rivières
  image:
    light: /logos/logo-ctr-fc.png
    dark: /logos/logo-ctr-fc-blanc.png
    alt: Cégep de Trois-Rivières — Direction de la formation continue et des services aux entreprises
  actions:
    - theme: brand
      text: Plan de cours
      link: /plan-cours/plan-de-cours
    - theme: alt
      text: Calendrier
      link: /plan-cours/calendrier
---
<section id="seance-1">
<div class="relative flex py-5 items-center mt-10">
   <div class="grow border-t border-gray-400"></div>
   <span class="shrink mx-4 text-gray-400">Séance 1 — mercredi 23 septembre</span>
  <div class="grow border-t border-gray-400"></div>
</div>
<div class="grid grid-cols-1 gap-5 lg:grid-cols-2">
  <WeeklyTodo
    title="À faire cette semaine — En classe"
    subtitle="Activités réalisées pendant la séance."
    :steps="[
      {
        title: 'Ce qu’il faut pour mettre un site en ligne',
        links: [
          { text: 'Séance 1', href: '/modules/01-faisabilite/01-mettre-un-site-en-ligne', variant: 'primary' },
          { text: 'Activité — casse-tête', href: '/modules/01-faisabilite/activite-casse-tete', variant: 'secondary' }
        ]
      },
      {
        title: 'Lab 01 — Enquête technique',
        badge: 'En duo',
        links: [
          { text: 'Lab 01', href: '/labs/lab01-enquete-technique', variant: 'primary' }
        ]
      }
    ]"
  />

  <WeeklyTodo
    title="À préparer / compléter"
    subtitle="À compléter de votre côté."
    :steps="[
      {
        title: 'Déposer la fiche du Lab 01 dans le forum',
        description: 'Travail formatif, une fiche par duo.',
        links: [
          { text: 'Consignes de remise', href: '/labs/lab01-enquete-technique#remise', variant: 'primary' }
        ]
      },
      {
        title: 'Lire le plan de cours',
        links: [
          { text: 'Plan de cours', href: '/plan-cours/plan-de-cours', variant: 'secondary' }
        ]
      }
    ]"
  />
</div>
</section>
