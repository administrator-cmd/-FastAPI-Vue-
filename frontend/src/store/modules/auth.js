import request from '../../utils/request'

const state = {
  token: localStorage.getItem('token') || '',
  currentUser: {},
  isLoggedIn: !!localStorage.getItem('token')
}

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token
    state.isLoggedIn = !!token
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  },
  SET_CURRENT_USER(state, user) {
    state.currentUser = user
  },
  CLEAR_AUTH(state) {
    state.token = ''
    state.currentUser = {}
    state.isLoggedIn = false
    localStorage.removeItem('token')
  }
}

const actions = {
  login({ commit }, { account, password }) {
    return new Promise((resolve, reject) => {
      request.post('/users/login', {
        account,
        password
      })
        .then(response => {
          const { access_token } = response
          commit('SET_TOKEN', access_token)
          resolve(response)
        })
        .catch(error => {
          reject(error)
        })
    })
  },
  register({ commit }, userData) {
    return new Promise((resolve, reject) => {
      request.post('/users/register', userData)
        .then(response => {
          resolve(response)
        })
        .catch(error => {
          reject(error)
        })
    })
  },
  logout({ commit }) {
    commit('CLEAR_AUTH')
  },
  loadCurrentUser({ commit }) {
    if (!state.token) return Promise.reject('No token found')
    
    return request.get('/users/profile')
      .then(response => {
        commit('SET_CURRENT_USER', response)
        return response
      })
      .catch(error => {
        console.error('Failed to load user profile:', error)
        throw error
      })
  }
}

const getters = {
  isLoggedIn: state => state.isLoggedIn,
  currentUser: state => state.currentUser,
  token: state => state.token
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}