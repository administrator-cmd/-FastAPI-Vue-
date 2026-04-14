<template>
  <div class="post-detail-container">
    <el-card class="post-detail-card">
      <div v-if="loading" class="loading">
        <el-skeleton :rows="6" animated />
      </div>
      <div v-else-if="post">
        <h1 class="post-title">{{ post.title }}</h1>
        <div class="post-meta">
          <el-tag type="info" size="small">{{ formatDate(post.created_at) }}</el-tag>
          <el-tag type="warning" size="small">作者 ID: {{ post.author_id }}</el-tag>
        </div>
        <div class="post-content" v-html="post.content_html"></div>
        <div class="post-actions" v-if="canEdit">
          <el-button type="primary" @click="editPost">编辑</el-button>
          <el-popconfirm 
            title="确定要删除这篇文章吗？" 
            @confirm="deletePost"
          >
            <template #reference>
              <el-button type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </div>
      </div>
      <div v-else class="no-post">
        <el-empty description="文章不存在" />
        <el-button @click="$router.push('/')">返回首页</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'

export default {
  name: 'PostDetail',
  setup() {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()
    
    const loading = ref(true)
    const postId = parseInt(route.params.id)
    
    const post = computed(() => store.getters['posts/currentPost'])
    const currentUser = computed(() => store.getters['auth/currentUser'])
    
    const canEdit = computed(() => {
      return post.value && currentUser.value && post.value.author_id === currentUser.value.id
    })
    
    const loadPost = async () => {
      try {
        await store.dispatch('posts/fetchPostById', postId)
      } catch (error) {
        console.error('加载文章失败:', error)
      } finally {
        loading.value = false
      }
    }
    
    const formatDate = (dateString) => {
      return dayjs(dateString).format('YYYY-MM-DD HH:mm')
    }
    
    const editPost = () => {
      router.push(`/posts/${postId}/edit`)
    }
    
    const deletePost = async () => {
      try {
        await store.dispatch('posts/deletePost', postId)
        ElMessage.success('删除成功')
        router.push('/')
      } catch (error) {
        console.error('删除文章失败:', error)
        ElMessage.error('删除失败')
      }
    }
    
    onMounted(() => {
      loadPost()
    })
    
    return {
      post,
      loading,
      currentUser,
      canEdit,
      formatDate,
      editPost,
      deletePost
    }
  }
}
</script>

<style scoped>
.post-detail-container {
  max-width: 800px;
  margin: 0 auto;
}

.post-detail-card {
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.post-title {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 24px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.post-meta {
  margin-bottom: 20px;
}

.post-content {
  line-height: 1.8;
  color: #444;
  font-size: 16px;
  margin-bottom: 30px;
}

.post-content :deep(h1) {
  font-size: 2em;
  margin: 0.67em 0;
  font-weight: bold;
}

.post-content :deep(h2) {
  font-size: 1.5em;
  margin: 0.75em 0;
  font-weight: bold;
}

.post-content :deep(h3) {
  font-size: 1.17em;
  margin: 0.83em 0;
  font-weight: bold;
}

.post-content :deep(p) {
  margin: 1em 0;
}

.post-content :deep(ul), .post-content :deep(ol) {
  margin: 1em 0;
  padding-left: 2em;
}

.post-content :deep(li) {
  margin: 0.5em 0;
}

.post-content :deep(code) {
  background-color: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}

.post-content :deep(pre) {
  background-color: #f5f5f5;
  padding: 1em;
  border-radius: 4px;
  overflow-x: auto;
  max-width: 100%;
}

.post-content :deep(pre code) {
  background-color: transparent;
  padding: 0;
}

.post-content :deep(blockquote) {
  border-left: 4px solid #ddd;
  padding-left: 1em;
  margin: 1em 0;
  color: #666;
}

.post-content :deep(a) {
  color: #409eff;
  text-decoration: none;
}

.post-content :deep(a:hover) {
  text-decoration: underline;
}

.post-content :deep(img) {
  max-width: 100%;
  height: auto;
}

.post-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  display: block;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.post-content :deep(th),
.post-content :deep(td) {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.post-actions {
  border-top: 1px solid #eee;
  padding-top: 20px;
  text-align: right;
}

.loading {
  padding: 20px 0;
}

.no-post {
  text-align: center;
  padding: 40px 0;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .post-detail-container {
    width: 100%;
  }
  
  .post-detail-card {
    padding: 12px;
  }
  
  .post-title {
    font-size: 20px;
  }
  
  .post-content {
    font-size: 15px;
    line-height: 1.6;
  }
  
  .post-content :deep(pre) {
    padding: 0.8em;
    font-size: 13px;
  }
  
  .post-content :deep(table) {
    font-size: 13px;
  }
  
  .post-actions {
    display: flex;
    gap: 10px;
    justify-content: flex-start;
  }
}
</style>