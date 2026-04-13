import { createStore } from 'vuex'
import auth from './modules/auth'
import posts from './modules/posts'

export default createStore({
  modules: {
    auth,
    posts
  }
})