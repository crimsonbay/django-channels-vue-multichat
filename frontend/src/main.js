import Vue from 'vue'
import VueRouter from 'vue-router'
import BootstrapVue from 'bootstrap-vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import store from './store'
import Home from './components/Home.vue'
import ChatTabs from './components/ChatTabs.vue'
import Registration from './components/Registration.vue'
import About from './components/About.vue'
import ChatList from './components/ChatList.vue'
Vue.use(BootstrapVue)
Vue.use(VueRouter)
// Vue.config.productionTip = false

// routes which component display( маршруты, какой компонент отображать)
const routes = [
  { path: '/', component: Home },
  { path: '/chat-list', component: ChatList },
  { path: '/chat', component: ChatTabs },
  { path: '/registration', component: Registration },
  { path: '/about', component: About }
]

const router = new VueRouter({
  mode: 'history',
  routes // shorthand notation for `routes: routes`( сокращённая запись для `routes: routes`)
})

let vm = new Vue({
  el: '#app',
  store,
  router,
  // template: '<App/>',
  // components: { App }
  render: h => h(App)
})
Vue.use(vm)
// sdf
// alpha
