// https://vitepress.dev/guide/custom-theme
import { h } from 'vue'
import Theme from 'vitepress/theme'
import './style.css'
import './custom.css'
import WeeklyTodo from "./components/WeeklyTodo.vue"
import TrajetCartes from "./components/TrajetCartes.vue"
import TrajetAnime from "./components/TrajetAnime.vue"
import EchelleSites from "./components/EchelleSites.vue"
import CoutsAnnees from "./components/CoutsAnnees.vue"
import TriContraintes from "./components/TriContraintes.vue"
import ParcoursLab from "./components/ParcoursLab.vue"
import JaugesPageSpeed from "./components/JaugesPageSpeed.vue"
import BarreNavigateur from "./components/BarreNavigateur.vue"
import TriExigences from "./components/TriExigences.vue"
import PhrasesCachees from "./components/PhrasesCachees.vue"
import MatriceRisques from "./components/MatriceRisques.vue"
import RetourLab01 from "./components/RetourLab01.vue"
import TriSources from "./components/TriSources.vue"
import GrillePrix from "./components/GrillePrix.vue"
import VersionImprimable from "./components/VersionImprimable.vue"


export default {
  extends: Theme,
  Layout: () => {
    return h(Theme.Layout, null, {
      // https://vitepress.dev/guide/extending-default-theme#layout-slots
      "doc-before": () => h(VersionImprimable, { position: "haut" }),
      "doc-after": () => h(VersionImprimable, { position: "bas" }),
    })
  },
  enhanceApp({ app, router, siteData }) {
    app.component("WeeklyTodo", WeeklyTodo);
    app.component("TrajetCartes", TrajetCartes);
    app.component("TrajetAnime", TrajetAnime);
    app.component("EchelleSites", EchelleSites);
    app.component("CoutsAnnees", CoutsAnnees);
    app.component("TriContraintes", TriContraintes);
    app.component("ParcoursLab", ParcoursLab);
    app.component("JaugesPageSpeed", JaugesPageSpeed);
    app.component("BarreNavigateur", BarreNavigateur);
    app.component("TriExigences", TriExigences);
    app.component("PhrasesCachees", PhrasesCachees);
    app.component("MatriceRisques", MatriceRisques);
    app.component("RetourLab01", RetourLab01);
    app.component("TriSources", TriSources);
    app.component("GrillePrix", GrillePrix);
  }
}

