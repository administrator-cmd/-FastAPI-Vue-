import request from '../../utils/request'

const state = {
  tags: [],
  loading: false
}

const mutations = {
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_TAGS(state, tags) {
    state.tags = tags
  }
}

const actions = {
  // 获取所有标签
  fetchTags({ commit }) {
    commit('SET_LOADING', true)
    return request.get('/tags')
      .then(response => {
        commit('SET_TAGS', response)
        commit('SET_LOADING', false)
        return response
      })
      .catch(error => {
        commit('SET_LOADING', false)
        throw error
      })
  },
  
  // 创建标签
  createTag({ dispatch }, tagName) {
    return request.post('/tags', { name: tagName })
      .then(response => {
        // 创建成功后刷新标签列表
        dispatch('fetchTags')
        return response
      })
      .catch(error => {
        throw error
      })
  }
}

const getters = {
  tags: state => state.tags,
  loading: state => state.loading
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
