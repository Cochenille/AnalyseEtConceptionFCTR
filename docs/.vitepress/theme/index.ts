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


export default {
  extends: Theme,
  Layout: () => {
    return h(Theme.Layout, null, {
      // https://vitepress.dev/guide/extending-default-theme#layout-slots
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
  }
}

