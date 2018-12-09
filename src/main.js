// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import bCarousel from 'bootstrap-vue/es/components/carousel/carousel';

import ECharts from 'vue-echarts/components/ECharts'

// import ECharts modules manually to reduce bundle size
// for each plot category (line, bar, etc), it must be imported here manually otherwise cannot be used
import 'echarts/lib/chart/bar'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/polar'
import 'echarts/lib/chart/line'

import App from './App'
import router from './router'
import 'firebase/auth';
import {
  store
} from './store/store'

const fb = require('@/components/firebaseConfiguration.js')
const VueAvatar = require('@lossendae/vue-avatar')

Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.component('b-carousel', bCarousel);
Vue.use(BootstrapVue)
Vue.component('vue-avatar', VueAvatar)
Vue.component('chart', ECharts)
// Vue.use(ECharts)

//Handle page reloads, ensures that firebase initialises before loading the app when a user refreshes a page
let app;
fb.auth.onAuthStateChanged(function (user) {
  if (!app) {
    app = new Vue({
      store,
      el: '#app',
      components: {
        App
      },
      router,
      template: '<App/>',
    })
  }
});
