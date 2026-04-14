<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="18">
        <div class="posts-container">
          <h2>最新文章</h2>
          
          <div v-if="loading" class="loading">
            <el-skeleton :rows="4" animated />
          </div>
          
          <div v-else>
            <el-card 
              v-for="post in posts" 
              :key="post.id" 
              class="post-card"
              @click="goToPost(post.id)"
            >
              <template #header>
                <div class="card-header">
                  <span class="post-title">{{ post.title }}</span>
                  <el-tag type="info" size="small">{{ formatDate(post.created_at) }}</el-tag>
                </div>
              </template>
              <div class="post-content">
                {{ truncateContent(post.content_html) }}
              </div>
              <div class="post-author">
                作者: <el-tag size="small" type="success">{{ post.author_username || post.author_id }}</el-tag>
              </div>
            </el-card>
            
            <div v-if="posts.length === 0" class="no-posts">
              <el-empty description="暂无文章" />
            </div>
          </div>
        </div>
      </el-col>
      
      <el-col :span="6">
        <div class="sidebar">
          <el-card>
            <template #header>
              <strong>博客信息</strong>
            </template>
            <p>这是一个基于 FastAPI 和 Vue 的博客系统</p>
            <el-button 
              v-if="!isLoggedIn" 
              type="primary" 
              size="small" 
              @click="$router.push('/login')"
              style="margin-top: 10px;"
            >
              登录
            </el-button>
            <el-button 
              v-if="!isLoggedIn" 
              type="success" 
              size="small" 
              @click="$router.push('/register')"
              style="margin-top: 10px;"
            >
              注册
            </el-button>
            <el-button 
              v-if="isLoggedIn" 
              type="primary" 
              size="small" 
              @click="$router.push('/posts/create')"
              style="margin-top: 10px;"
            >
              写文章
            </el-button>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'

export default {
  name: 'Home',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const posts = computed(() => store.getters['posts/posts'])
    const loading = computed(() => store.getters['posts/loading'])
    const isLoggedIn = computed(() => store.getters['auth/isLoggedIn'])
    
    const fetchPosts = async () => {
      try {
        const result = await store.dispatch('posts/fetchPosts')
        console.log('文章列表:', result)
      } catch (error) {
        console.error('获取文章列表失败:', error)
      }
    }
    
    const goToPost = (postId) => {
      router.push(`/posts/${postId}`)
    }
    
    const truncateContent = (contentHtml) => {
      if (!contentHtml) return ''
      // 从 HTML 中提取纯文本
      const div = document.createElement('div')
      div.innerHTML = contentHtml
      const plainText = div.textContent || div.innerText || ''
      return plainText.length > 150 ? plainText.substring(0, 150) + '...' : plainText
    }
    
    const formatDate = (dateString) => {
      return dayjs(dateString).format('YYYY-MM-DD HH:mm')
    }
    
    onMounted(() => {
      fetchPosts()
    })
    
    return {
      posts,
      loading,
      isLoggedIn,
      goToPost,
      truncateContent,
      formatDate
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.posts-container {
  background: white;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.sidebar {
  background: white;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.post-card {
  margin-bottom: 20px;
  cursor: pointer;
}

.post-card:hover {
  box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-title {
  font-size: 18px;
  font-weight: bold;
}

.post-content {
  margin: 15px 0;
  color: #666;
  line-height: 1.6;
}

.post-author {
  text-align: right;
  font-size: 14px;
  color: #999;
}

.no-posts {
  text-align: center;
  padding: 40px 0;
}

.loading {
  margin: 20px 0;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .home {
    width: 100%;
  }
  
  .home-row {
    flex-direction: column;
  }
  
  .posts-container,
  .sidebar {
    padding: 12px;
    width: 100%;
  }
  
  .sidebar {
    margin-top: 12px;
  }
  
  .post-title {
    font-size: 16px;
  }
  
  .post-content {
    font-size: 14px;
    line-height: 1.6;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>