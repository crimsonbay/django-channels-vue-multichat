import Vue from 'vue'
import Vuex from 'vuex'
import {
  SET_NOTES,
  SET_FIRST_NAME,
  CLEAR_FIRST_NAME,
  SET_TOKEN,
  CLEAR_TOKEN,
  SET_PAGE_NAME
} from './mutation-types.js'
import { serverAddr } from '../config'
import { fetchCheckToken, fetchAPITokenAuth } from '../api'

Vue.use(Vuex)

const state = {
  notes: [],
  token: '', // user token (токен пользователя)
  firstName: 'Anonymous', // user first_name( first_name пользователя)
  pageName: '' // the name of the opened page( имя открытой страницы)
}

const getters = {
  NOTES: state => state.notes,
  TOKEN: state => state.token,
  FIRST_NAME: state => state.firstName,
  PAGE_NAME: state => state.pageName
}

const mutations = {
  [SET_PAGE_NAME] (state, pageName) {
    state.pageName = pageName
  },
  [SET_TOKEN] (state, token) {
    state.token = token
  },
  [CLEAR_TOKEN] (state) {
    state.token = ''
    window.location.reload(true)
  },
  [CLEAR_FIRST_NAME] (state) {
    state.firstName = 'Anonymous'
  },
  [SET_FIRST_NAME] (state, firstName) {
    state.firstName = firstName
  },
  [SET_NOTES] (state, { notes }) {
    state.notes = notes
  }
}

const actions = {
  // set the name of the opened page( уcтановить имя открытой страницы)
  setPageName: ({ commit }, { pageName }) => {
    commit(SET_PAGE_NAME, pageName)
    return 0
  },

  // clear token( очистить токен)
  clearToken: ({ commit }) => {
    commit(CLEAR_TOKEN)
    commit(CLEAR_FIRST_NAME)
    sessionStorage.setItem('firstName', 'Anonymous')
    sessionStorage.setItem('token', '')
    return 0
  },

  // check token, if ok, set the firstName for the token that came,
  // otherwise, erase the token and set the name Anonymous
  // (проверка токена, если ок, устанавливаем пришедший firstName для токена,
  // иначе стираем токен и устанавливаем имя Anonymous)
  checkToken: ({ dispatch, commit }) => {
    let token = sessionStorage.getItem('token')
    if (!token) {
      if (token == null) {
        dispatch('clearToken')
      }
      return 0
    }
    fetchCheckToken(token)
      .then(function (obj) {
        console.log(obj.status)
        if (obj.status === 200) {
          // commit(SET_TOKEN, obj.body.first_name);
          sessionStorage.setItem('firstName', obj.body.firstName)
          commit(SET_FIRST_NAME, obj.body.firstName)
        } else {
          commit(SET_TOKEN, '')
          commit(SET_FIRST_NAME, 'Anonymous')
          sessionStorage.setItem('firstName', 'Anonymous')
        }
        return obj
      }).catch(console.error.bind(console))
  },

  // set the token by name and password, if the name and password are incorrect,
  // then the token is empty and the name is Anonymous
  // (установить токен по имени и паролю, если имя и пароль неверные, то токен пустой и имя Anonymous)
  setToken: ({ dispatch, commit }, { name, password }) => {
    fetchAPITokenAuth(name, password)
      .then(function (obj) {
        if (obj.status === 200) {
          commit(SET_TOKEN, obj.body.token)
          // document.cookie = "token=" + obj.body.token
          sessionStorage.setItem('token', obj.body.token)
        } else {
          commit(SET_TOKEN, '')
          commit(SET_FIRST_NAME, 'Anonymous')
        }
        return obj
      }).then(function (obj) {
        dispatch('checkToken')
        window.location.reload(true)
        return obj
      }).catch(console.error.bind(console))
  }
}

export default new Vuex.Store({
  state,
  getters,
  mutations,
  actions
})
