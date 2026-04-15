import request from '../../utils/request'

const state = {
  comments: [],
  loading: false
}

const mutations = {
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_COMMENTS(state, comments) {
    state.comments = comments
  },
  ADD_COMMENT(state, comment) {
    state.comments.unshift(comment)
  },
  DELETE_COMMENT(state, commentId) {
    state.comments = state.comments.filter(c => c.id !== commentId)
  }
}

const actions = {
  fetchComments({ commit }, postId) {
    commit('SET_LOADING', true)
    return request.get(`/comments/posts/${postId}/comments`)
      .then(response => {
        commit('SET_COMMENTS', response)
        commit('SET_LOADING', false)
        return response
      })
      .catch(error => {
        commit('SET_LOADING', false)
        throw error
      })
  },
  
  createComment({ commit }, { postId, commentData }) {
    return request.post(`/comments/posts/${postId}/comments`, commentData)
      .then(response => {
        commit('ADD_COMMENT', response)
        return response
      })
      .catch(error => {
        throw error
      })
  },
  
  deleteComment({ commit }, commentId) {
    return request.delete(`/comments/${commentId}`)
      .then(response => {
        commit('DELETE_COMMENT', commentId)
        return response
      })
      .catch(error => {
        throw error
      })
  }
}

const getters = {
  comments: state => state.comments,
  loading: state => state.loading
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
