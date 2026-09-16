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
		logo: "./logos/logo.svg",

		nav: [
			{ text: "Plan de cours", link: "/plan-cours/plan-de-cours" },
			{ text: "Calendrier", link: "/plan-cours/calendrier" },
			/*{
				text: "Modules",
				items: [
					{ text: "Partie 1 — Faisabilité technique", link: "/modules/01-faisabilite/" },
					{ text: "Partie 2 — Conception d'un projet Web", link: "/modules/02-conception/" },
				],
			},*/
		],
		sidebar: [
			{
				text: "Documents généraux",
				items: [
					{ text: "Plan de cours", link: "/plan-cours/plan-de-cours" },
					{ text: "Calendrier", link: "/plan-cours/calendrier" },
				],
			},
			/*{
				text: "Modules du cours",
				collapsed: false,
				items: [],
			},
			{
				text: "Laboratoires",
				collapsed: true,
				items: [],
			},
			{
				text: "Évaluations",
				collapsed: true,
				items: [],
			},*/
		],

		search: {
			provider: "local",
		},
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
