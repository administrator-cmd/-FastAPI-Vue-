import request from '@/utils/request'

const state = {
  likeCounts: {}, // 存储每篇文章的点赞数 { postId: count }
  userLikes: {}   // 存储用户点赞状态 { postId: boolean }
}

const getters = {
  getLikeCount: (state) => (postId) => {
    return state.likeCounts[postId] || 0
  },
  isLiked: (state) => (postId) => {
    return !!state.userLikes[postId]
  }
}

const mutations = {
  SET_LIKE_COUNT(state, { postId, count }) {
    state.likeCounts[postId] = count
  },
  SET_USER_LIKE(state, { postId, liked }) {
    state.userLikes[postId] = liked
  },
  INCREMENT_LIKE_COUNT(state, postId) {
    if (state.likeCounts[postId] !== undefined) {
      state.likeCounts[postId]++
    }
  },
  DECREMENT_LIKE_COUNT(state, postId) {
    if (state.likeCounts[postId] !== undefined && state.likeCounts[postId] > 0) {
      state.likeCounts[postId]--
    }
  }
}

const actions = {
  // 获取文章点赞数
  async fetchLikeCount({ commit }, postId) {
    try {
      const response = await request.get(`/likes/${postId}`)
      commit('SET_LIKE_COUNT', { postId, count: response.like_count })
      return response
    } catch (error) {
      console.error('获取点赞数失败:', error)
      throw error
    }
  },

  // 获取用户点赞状态
  async fetchUserLikeStatus({ commit }, postId) {
    try {
      const response = await request.get(`/likes/user/${postId}`)
      commit('SET_USER_LIKE', { postId, liked: response.is_liked })
      return response
    } catch (error) {
      console.error('获取点赞状态失败:', error)
      throw error
    }
  },

  // 点赞
  async createLike({ commit, state }, postId) {
    try {
      const response = await request.post('/likes', { post_id: postId })
      commit('SET_USER_LIKE', { postId, liked: true })
      commit('INCREMENT_LIKE_COUNT', postId)
      return response
    } catch (error) {
      console.error('点赞失败:', error)
      throw error
    }
  },

  // 取消点赞
  async deleteLike({ commit, state }, postId) {
    try {
      const response = await request.delete(`/likes/${postId}`)
      commit('SET_USER_LIKE', { postId, liked: false })
      commit('DECREMENT_LIKE_COUNT', postId)
      return response
    } catch (error) {
      console.error('取消点赞失败:', error)
      throw error
    }
  },

  // 切换点赞状态
  async toggleLike({ dispatch, state }, postId) {
    const isLiked = state.userLikes[postId]
    if (isLiked) {
      return await dispatch('deleteLike', postId)
    } else {
      return await dispatch('createLike', postId)
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
