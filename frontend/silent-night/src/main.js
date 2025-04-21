import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { Quasar } from 'quasar'
import quasarIconSet from 'quasar/icon-set/fontawesome-v6'
// Import icon libraries
import '@quasar/extras/fontawesome-v6/fontawesome-v6.css'

// Import Quasar css
import 'quasar/src/css/index.sass'

const app = createApp(App)

app.use(router)

app.use(Quasar, {
    plugins: {}, // import Quasar plugins and add here
    iconSet: quasarIconSet,
    
    config: {
      dark: true
      /*
      brand: {
        // primary: '#e46262',
        // ... or all other brand colors
      },
      notify: {...}, // default set of options for Notify Quasar plugin
      loading: {...}, // default set of options for Loading Quasar plugin
      loadingBar: { ... }, // settings for LoadingBar Quasar plugin
      // ..and many more (check Installation card on each Quasar component/directive/plugin)*/
    }
    
  })

app.mount('#app')
