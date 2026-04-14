import { createStore } from 'vuex'
import auth from './modules/auth'
import posts from './modules/posts'
import comments from './modules/comments'

export default createStore({
  modules: {
    auth,
    posts,
    comments
  }
})