import request from '@/utils/request'

const state = {
  commentLikeCounts: {}, // { commentId: count }
  userCommentLikes: {}   // { commentId: boolean }
}

const getters = {
  getCommentLikeCount: (state) => (commentId) => {
    return state.commentLikeCounts[commentId] || 0
  },
  isCommentLiked: (state) => (commentId) => {
    return !!state.userCommentLikes[commentId]
  }
}

const mutations = {
  SET_COMMENT_LIKE_COUNT(state, { commentId, count }) {
    state.commentLikeCounts[commentId] = count
  },
  SET_USER_COMMENT_LIKE(state, { commentId, liked }) {
    state.userCommentLikes[commentId] = liked
  },
  INCREMENT_COMMENT_LIKE_COUNT(state, commentId) {
    if (state.commentLikeCounts[commentId] !== undefined) {
      state.commentLikeCounts[commentId]++
    }
  },
  DECREMENT_COMMENT_LIKE_COUNT(state, commentId) {
    if (state.commentLikeCounts[commentId] !== undefined && state.commentLikeCounts[commentId] > 0) {
      state.commentLikeCounts[commentId]--
    }
  }
}

const actions = {
  // 获取评论点赞数
  async fetchCommentLikeCount({ commit }, commentId) {
    try {
      const response = await request.get(`/comment-likes/${commentId}`)
      commit('SET_COMMENT_LIKE_COUNT', { commentId, count: response.like_count })
      return response
    } catch (error) {
      console.error('获取评论点赞数失败:', error)
      throw error
    }
  },

  // 获取用户评论点赞状态
  async fetchUserCommentLikeStatus({ commit }, commentId) {
    try {
      const response = await request.get(`/comment-likes/user/${commentId}`)
      commit('SET_USER_COMMENT_LIKE', { commentId, liked: response.is_liked })
      return response
    } catch (error) {
      console.error('获取评论点赞状态失败:', error)
      throw error
    }
  },

  async createCommentLike({ commit }, commentId) {
    try {
      await request.post('/comment-likes', { comment_id: commentId })
      commit('SET_USER_COMMENT_LIKE', { commentId, liked: true })
      commit('INCREMENT_COMMENT_LIKE_COUNT', commentId)
    } catch (error) {
      console.error('评论点赞失败:', error)
      // 如果是重复点赞错误，说明数据库已有记录，同步本地状态
      const errorMsg = error.response?.data?.message || error.message || ''
      if (errorMsg.includes('UNIQUE constraint') || errorMsg.includes('已经点赞过')) {
        console.warn('检测到重复点赞，同步本地状态为已点赞')
        commit('SET_USER_COMMENT_LIKE', { commentId, liked: true })
        // 不抛出错误，让调用方认为操作成功
        return
      }
      throw error
    }
  },

  async deleteCommentLike({ commit }, commentId) {
    try {
      await request.delete(`/comment-likes/${commentId}`)
      commit('SET_USER_COMMENT_LIKE', { commentId, liked: false })
      commit('DECREMENT_COMMENT_LIKE_COUNT', commentId)
    } catch (error) {
      console.error('取消评论点赞失败:', error)
      throw error
    }
  },

  async toggleCommentLike({ dispatch, state }, commentId) {
    try {
      const isLiked = state.userCommentLikes[commentId]
      if (isLiked) {
        // 已点赞 → 取消点赞
        await dispatch('deleteCommentLike', commentId)
        return { success: true, action: 'unliked' }
      } else {
        // 未点赞 → 点赞
        await dispatch('createCommentLike', commentId)
        return { success: true, action: 'liked' }
      }
    } catch (error) {
      // 如果创建点赞时遇到重复错误，说明状态不同步，重新获取状态
      const errorMsg = error.response?.data?.message || error.message || ''
      if (errorMsg.includes('UNIQUE constraint') || errorMsg.includes('已经点赞过')) {
        console.warn('检测到状态不同步，重新获取点赞状态')
        await dispatch('fetchUserCommentLikeStatus', commentId)
        await dispatch('fetchCommentLikeCount', commentId)
        return { success: true, action: 'synced' }
      }
      throw error
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
