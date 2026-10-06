import { defineConfig } from "vitepress";
import { withMermaid } from "vitepress-plugin-mermaid";

// https://vitepress.dev/reference/site-config
export default withMermaid(defineConfig({
	base: "/AnalyseEtConceptionFCTR/",
	lang: "fr-CA",
	cleanUrls: true,
	title: "582-A05-RI",
	description:
		"Analyse et conception Web — Plan de cours, calendrier et ressources",
	themeConfig: {
		logo: {
			light: "/logos/logo-ctr.png",
			dark: "/logos/logo-ctr-blanc.png",
			alt: "Cégep de Trois-Rivières",
		},

		nav: [
			{ text: "Plan de cours", link: "/plan-cours/plan-de-cours" },
			{ text: "Calendrier", link: "/plan-cours/calendrier" },
			{ text: "Mandat", link: "/mandat/" },
			{ text: "Évaluation 1", link: "/evaluations/evaluation-1" },
			{
				text: "Modules",
				items: [
					{ text: "Partie 1 — Faisabilité technique", link: "/modules/01-faisabilite/" },
					//{ text: "Partie 2 — Conception d'un projet Web", link: "/modules/02-conception/" },
				],
			},
		],
		sidebar: [
			{
				text: "Documents généraux",
				items: [
					{ text: "Plan de cours", link: "/plan-cours/plan-de-cours" },
					{ text: "Calendrier", link: "/plan-cours/calendrier" },
					{ text: "Mandat — Aventure Saint-Maurice", link: "/mandat/" },
				],
			},
			{
				text: "Modules du cours",
				collapsed: false,
				items: [
					{
						text: "Partie 1 — Faisabilité technique",
						collapsed: false,
						items: [
							{ text: "Présentation", link: "/modules/01-faisabilite/" },
							{
								text: "Séance 1 — Mettre un site en ligne",
								link: "/modules/01-faisabilite/01-mettre-un-site-en-ligne",
							},
							{
								text: "Activité — Le trajet d'une page Web",
								link: "/modules/01-faisabilite/activite-casse-tete",
							},
							{
								text: "Séance 2 — Contraintes et risques",
								link: "/modules/01-faisabilite/02-contraintes-et-risques",
							},
							{
								text: "Séance 3 — La veille technologique",
								link: "/modules/01-faisabilite/03-veille-technologique",
							},
						],
					},
				],
			},
			{
				text: "Laboratoires",
				collapsed: false,
				items: [
					{ text: "Lab 01 — Enquête technique", link: "/labs/lab01-enquete-technique" },
					{ text: "Lab 02 — Radiographie du mandat", link: "/labs/lab02-radiographie-mandat" },
					{ text: "Lab 03 — Le plan d'essai", link: "/labs/lab03-plan-essai" },
				],
			},
			{
				text: "Évaluations",
				collapsed: false,
				items: [
					{ text: "Évaluation 1 — Évaluation technique", link: "/evaluations/evaluation-1" },
				],
			},
		],

		search: {
			provider: "local",
		},
	},
	mermaid: {
		flowchart: { wrappingWidth: 400 },
	},
	vite: {
		optimizeDeps: {
			include: [
				"fastdom",
				"fastdom/extensions/fastdom-promised.js",
			],
		},
	},
}));
