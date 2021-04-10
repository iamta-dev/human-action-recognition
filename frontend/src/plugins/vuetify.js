import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import '@fortawesome/fontawesome-free/css/all.css';
import VueSession from 'vue-session';

Vue.use(VueSession);
Vue.use(Vuetify);

export default new Vuetify({
    icons: {
      iconfont: 'fa',
    },
  })
  