import request from '../../utils/request'

const state = {
  posts: [],
  currentPost: null,
  loading: false
}

const mutations = {
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_POSTS(state, posts) {
    state.posts = posts
  },
  ADD_POST(state, post) {
    state.posts.unshift(post)
  },
  UPDATE_POST(state, updatedPost) {
    const index = state.posts.findIndex(p => p.id === updatedPost.id)
    if (index !== -1) {
      state.posts.splice(index, 1, updatedPost)
    }
  },
  DELETE_POST(state, postId) {
    state.posts = state.posts.filter(p => p.id !== postId)
  },
  SET_CURRENT_POST(state, post) {
    state.currentPost = post
  }
}

const actions = {
  fetchPosts({ commit }, { page = 1, size = 10, keyword = '' } = {}) {
    commit('SET_LOADING', true)
    const params = { page, size }
    if (keyword) params.keyword = keyword
    return request.get('/posts', { params })
      .then(response => {
        commit('SET_POSTS', response)
        commit('SET_LOADING', false)
        return response
      })
      .catch(error => {
        commit('SET_LOADING', false)
        throw error
      })
  },
  createPost({ commit }, postData) {
    return request.post('/posts', postData)
      .then(response => {
        commit('ADD_POST', response)
        return response
      })
      .catch(error => {
        throw error
      })
  },
  updatePost({ commit }, { id, postData }) {
    return request.put(`/posts/${id}`, postData)
      .then(response => {
        commit('UPDATE_POST', response)
        return response
      })
      .catch(error => {
        throw error
      })
  },
  deletePost({ commit }, postId) {
    return request.delete(`/posts/${postId}`)
      .then(response => {
        commit('DELETE_POST', postId)
        return response
      })
      .catch(error => {
        throw error
      })
  },
  fetchPostById({ commit }, postId) {
    return request.get(`/posts/${postId}`)
      .then(response => {
        commit('SET_CURRENT_POST', response)
        return response
      })
      .catch(error => {
        throw error
      })
  },
  fetchUserPosts({ commit }, userId) {
    return request.get(`/users/${userId}/posts`)
      .then(response => {
        return response
      })
      .catch(error => {
        throw error
      })
  },
  fetchAllUsers({ commit }) {
    return request.get('/users')
      .then(response => {
        return response
      })
      .catch(error => {
        throw error
      })
  },
  fetchHealth({ commit }) {
    return request.get('/health')
      .then(response => {
        return response
      })
      .catch(error => {
        throw error
      })
  },
  fetchUserPosts({ commit }, userId) {
    return request.get(`/users/${userId}/posts`)
      .then(response => {
        return response
      })
      .catch(error => {
        throw error
      })
  },
  fetchAllUsers({ commit }) {
    return request.get('/users')
      .then(response => {
        return response
      })
      .catch(error => {
        throw error
      })
  },
  fetchHealth({ commit }) {
    return request.get('/health')
      .then(response => {
        return response
      })
      .catch(error => {
        throw error
      })
  }
}

const getters = {
  posts: state => state.posts,
  currentPost: state => state.currentPost,
  loading: state => state.loading
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}