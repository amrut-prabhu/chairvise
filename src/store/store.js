import Vue from 'vue';
import Vuex from 'vuex'

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null,
  },
  getters: {
    isLoggedIn: state => {
      return !!state.user;
    },
    getUser: state => {
      return state.user;
    },
  },
  mutations: {
    setUser: (state, payload) => {
      state.user = payload;
      localStorage.setItem('user', JSON.stringify(payload));
    },
    clearUser: (state) => {
      state.user = null;
      localStorage.setItem('user', null);
    }
  }
});
