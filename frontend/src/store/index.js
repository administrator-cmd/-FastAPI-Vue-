import { createStore } from 'vuex'
import auth from './modules/auth'
import posts from './modules/posts'
import comments from './modules/comments'
import likes from './modules/likes'
import commentLikes from './modules/commentLikes'

export default createStore({
  modules: {
    auth,
    posts,
    comments,
    likes,
    commentLikes
  }
})
