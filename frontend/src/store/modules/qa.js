import request from '../../utils/request'

const state = {
  qaHistory: [],
  currentAnswer: null,
  loading: false
}

const mutations = {
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_QA_HISTORY(state, history) {
    state.qaHistory = history
  },
  ADD_QA_RECORD(state, record) {
    state.qaHistory.unshift(record)
  },
  SET_CURRENT_ANSWER(state, answer) {
    state.currentAnswer = answer
  }
}

const actions = {
  // 向 AI 提问
  askQuestion({ commit }, questionData) {
    commit('SET_LOADING', true)
    return request.post('/qa/ask', questionData)
      .then(response => {
        commit('ADD_QA_RECORD', response)
        commit('SET_CURRENT_ANSWER', response)
        commit('SET_LOADING', false)
        return response
      })
      .catch(error => {
        commit('SET_LOADING', false)
        throw error
      })
  },

  // 获取问答历史
  fetchQAHistory({ commit }) {
    commit('SET_LOADING', true)
    return request.get('/qa/history')
      .then(response => {
        commit('SET_QA_HISTORY', response)
        commit('SET_LOADING', false)
        return response
      })
      .catch(error => {
        commit('SET_LOADING', false)
        throw error
      })
  }
}

const getters = {
  qaHistory: state => state.qaHistory,
  currentAnswer: state => state.currentAnswer,
  loading: state => state.loading
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
