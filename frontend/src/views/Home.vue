<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="18">
        <div class="posts-container">
          <!-- 搜索框 -->
          <div class="search-box">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索文章标题或内容..."
              prefix-icon="Search"
              clearable
              @keyup.enter="handleSearch"
              @clear="handleClearSearch"
            >
              <template #append>
                <el-button @click="handleSearch">搜索</el-button>
              </template>
            </el-input>
          </div>
          
          <h2>{{ searchKeyword ? `搜索结果: "${searchKeyword}"` : '最新文章' }}</h2>
          
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
                  <div class="card-tags">
                    <el-tag type="info" size="small">{{ formatDate(post.created_at) }}</el-tag>
                    <!-- 显示文章标签 -->
                    <el-tag 
                      v-for="tag in post.tags" 
                      :key="tag.id" 
                      size="small" 
                      type="success"
                      style="margin-left: 4px;"
                    >
                      {{ tag.name }}
                    </el-tag>
                    <el-tag type="danger" size="small">
                      <el-icon><Star /></el-icon>
                      {{ getLikeCount(post.id) }}
                    </el-tag>
                  </div>
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
import { computed, onMounted, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { Star, Search } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

export default {
  name: 'Home',
  components: {
    Star,
    Search
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const searchKeyword = ref('')
    
    const posts = computed(() => store.getters['posts/posts'])
    const loading = computed(() => store.getters['posts/loading'])
    const isLoggedIn = computed(() => store.getters['auth/isLoggedIn'])
    
    const getLikeCount = (postId) => {
      return store.getters['likes/getLikeCount'](postId)
    }
    
    const fetchPosts = async (keyword = '') => {
      try {
        const result = await store.dispatch('posts/fetchPosts', { keyword })
        console.log('文章列表:', result)
        // 加载每篇文章的点赞数
        for (const post of result) {
          try {
            await store.dispatch('likes/fetchLikeCount', post.id)
          } catch (error) {
            console.error(`加载文章 ${post.id} 的点赞数失败:`, error)
          }
        }
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
    
    const handleSearch = () => {
      if (searchKeyword.value.trim()) {
        fetchPosts(searchKeyword.value.trim())
      } else {
        handleClearSearch()
      }
    }
    
    const handleClearSearch = () => {
      searchKeyword.value = ''
      fetchPosts()
    }
    
    onMounted(() => {
      fetchPosts()
    })
    
    return {
      posts,
      loading,
      isLoggedIn,
      searchKeyword,
      goToPost,
      truncateContent,
      formatDate,
      getLikeCount,
      handleSearch,
      handleClearSearch
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
  min-height: 44px;
}

.post-card:hover {
  box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-tags {
  display: flex;
  gap: 8px;
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
  font-size: 16px;
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

/* 平板端适配 (768px以下) */
@media (max-width: 768px) {
  .home {
    width: 100%;
    padding: 0 16px;
  }
  
  /* 文章列表改为单列布局 */
  :deep(.el-col-18),
  :deep(.el-col-6) {
    width: 100%;
    max-width: 100%;
    flex: 0 0 100%;
  }
  
  .posts-container,
  .sidebar {
    padding: 16px;
    width: 100%;
  }
  
  .sidebar {
    margin-top: 16px;
  }
  
  .post-title {
    font-size: 17px;
  }
  
  .post-content {
    font-size: 15px;
    line-height: 1.6;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .card-tags {
    width: 100%;
    justify-content: flex-start;
  }
  
  /* 按钮点击区域至少44x44px */
  :deep(.el-button) {
    min-height: 44px;
    min-width: 44px;
    padding: 12px 20px;
  }
}

/* 手机端适配 (480px以下) */
@media (max-width: 480px) {
  .home {
    padding: 0 12px;
  }
  
  .posts-container,
  .sidebar {
    padding: 12px;
  }
  
  .post-title {
    font-size: 16px;
  }
  
  .post-content {
    font-size: 16px;
  }
  
  .post-author {
    font-size: 13px;
  }
  
  /* 侧边栏按钮垂直排列 */
  :deep(.sidebar .el-button) {
    display: block;
    width: 100%;
    margin-top: 8px !important;
    margin-left: 0 !important;
  }
}
</style>