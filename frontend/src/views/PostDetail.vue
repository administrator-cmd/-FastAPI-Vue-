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
          <el-tag type="warning" size="small">作者: {{ post.author_username || post.author_id }}</el-tag>
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
            {{ likeCount }}
          </el-tag>
        </div>
        <div class="post-content" v-html="post.content_html"></div>
        <div class="post-interactions" v-if="currentUser">
          <el-button 
            :type="isLiked ? 'danger' : 'default'" 
            @click="handleLike"
            :loading="likeLoading"
          >
            <el-icon><Star /></el-icon>
            {{ isLiked ? '已点赞' : '点赞' }}
          </el-button>
        </div>
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

    <!-- 评论区 -->
    <el-card class="comments-section" v-if="post">
      <h3 class="comments-title">评论 ({{ comments.length }})</h3>
      
      <!-- 发表评论 -->
      <div class="comment-form" v-if="currentUser">
        <el-input
          v-model="newComment"
          type="textarea"
          :rows="3"
          placeholder="写下你的评论..."
          maxlength="500"
          show-word-limit
        />
        <el-button 
          type="primary" 
          @click="submitComment"
          :loading="commentLoading"
          style="margin-top: 10px;"
        >
          发表评论
        </el-button>
      </div>
      <div v-else class="login-tip">
        <el-alert
          title="登录后即可发表评论"
          type="info"
          :closable="false"
        >
          <template #default>
            <el-button type="primary" size="small" @click="$router.push('/login')">
              去登录
            </el-button>
          </template>
        </el-alert>
      </div>

      <!-- 评论列表 -->
      <div class="comments-list" v-loading="commentsLoading">
        <div v-if="comments.length === 0 && !commentsLoading" class="no-comments">
          <el-empty description="暂无评论,快来抢沙发吧!" />
        </div>
        
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <span class="comment-author">{{ comment.author_username || '用户 ID: ' + comment.author_id }}</span>
            <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
          </div>
          <div class="comment-content">{{ comment.content }}</div>
          <div class="comment-actions">
            <el-button 
              :type="isCommentLiked(comment.id) ? 'danger' : 'default'" 
              size="small" 
              link
              @click="handleCommentLike(comment.id)"
            >
              <el-icon><Star /></el-icon>
              {{ getCommentLikeCount(comment.id) }}
            </el-button>
            <el-popconfirm 
              v-if="canDeleteComment(comment)"
              title="确定要删除这条评论吗?" 
              @confirm="handleDeleteComment(comment.id)"
            >
              <template #reference>
                <el-button type="danger" size="small" link>删除</el-button>
              </template>
            </el-popconfirm>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Star } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

export default {
  name: 'PostDetail',
  components: {
    Star
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()
    
    const loading = ref(true)
    const postId = parseInt(route.params.id)
    const newComment = ref('')
    const commentLoading = ref(false)
    const likeLoading = ref(false)
    
    const post = computed(() => store.getters['posts/currentPost'])
    const currentUser = computed(() => store.getters['auth/currentUser'])
    const comments = computed(() => store.getters['comments/comments'])
    const commentsLoading = computed(() => store.getters['comments/loading'])
    const likeCount = computed(() => store.getters['likes/getLikeCount'](postId))
    const isLiked = computed(() => store.getters['likes/isLiked'](postId))
    const getCommentLikeCount = (commentId) => store.getters['commentLikes/getCommentLikeCount'](commentId)
    const isCommentLiked = (commentId) => store.getters['commentLikes/isCommentLiked'](commentId)
    
    const canEdit = computed(() => {
      return post.value && currentUser.value && post.value.author_id === currentUser.value.id
    })
    
    const canDeleteComment = (comment) => {
      return currentUser.value && comment.author_id === currentUser.value.id
    }
    
    const loadPost = async () => {
      try {
        await store.dispatch('posts/fetchPostById', postId)
      } catch (error) {
        console.error('加载文章失败:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadComments = async () => {
      try {
        await store.dispatch('comments/fetchComments', postId)
        // 加载每条评论的点赞数和状态
        if (comments.value.length > 0) {
          for (const comment of comments.value) {
            try {
              await store.dispatch('commentLikes/fetchCommentLikeCount', comment.id)
              if (currentUser.value) {
                await store.dispatch('commentLikes/fetchUserCommentLikeStatus', comment.id)
              }
            } catch (error) {
              console.error(`加载评论 ${comment.id} 点赞信息失败:`, error)
            }
          }
        }
      } catch (error) {
        console.error('加载评论失败:', error)
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
    
    const submitComment = async () => {
      if (!newComment.value.trim()) {
        ElMessage.warning('评论内容不能为空')
        return
      }
      
      commentLoading.value = true
      try {
        await store.dispatch('comments/createComment', {
          postId,
          commentData: { content: newComment.value }
        })
        ElMessage.success('评论成功')
        newComment.value = ''
      } catch (error) {
        console.error('发表评论失败:', error)
        ElMessage.error('评论失败')
      } finally {
        commentLoading.value = false
      }
    }
    
    const handleDeleteComment = async (commentId) => {
      try {
        await store.dispatch('comments/deleteComment', commentId)
        ElMessage.success('删除成功')
      } catch (error) {
        console.error('删除评论失败:', error)
        ElMessage.error('删除失败')
      }
    }
    
    const handleLike = async () => {
      if (!currentUser.value) {
        ElMessage.warning('请先登录')
        router.push('/login')
        return
      }
      
      likeLoading.value = true
      try {
        const wasLiked = isLiked.value
        await store.dispatch('likes/toggleLike', postId)
        ElMessage.success(wasLiked ? '取消点赞成功' : '点赞成功')
      } catch (error) {
        console.error('点赞操作失败:', error)
        ElMessage.error('操作失败')
      } finally {
        likeLoading.value = false
      }
    }
    
    const handleCommentLike = async (commentId) => {
      if (!currentUser.value) {
        ElMessage.warning('请先登录')
        router.push('/login')
        return
      }
      
      try {
        await store.dispatch('commentLikes/toggleCommentLike', commentId)
      } catch (error) {
        console.error('评论点赞操作失败:', error)
        ElMessage.error('操作失败')
      }
    }
    
    onMounted(async () => {
      await loadPost()
      await loadComments()
      // 加载点赞数
      try {
        await store.dispatch('likes/fetchLikeCount', postId)
      } catch (error) {
        console.error('加载点赞数失败:', error)
      }
      // 加载用户点赞状态
      if (currentUser.value) {
        try {
          await store.dispatch('likes/fetchUserLikeStatus', postId)
        } catch (error) {
          console.error('加载点赞状态失败:', error)
        }
      }
    })
    
    return {
      post,
      loading,
      currentUser,
      canEdit,
      comments,
      commentsLoading,
      newComment,
      commentLoading,
      likeCount,
      isLiked,
      likeLoading,
      canDeleteComment,
      formatDate,
      editPost,
      deletePost,
      submitComment,
      handleDeleteComment,
      handleLike,
      getCommentLikeCount,
      isCommentLiked,
      handleCommentLike
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

.comments-section {
  margin-top: 20px;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.comments-title {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 18px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.comment-form {
  margin-bottom: 30px;
}

.login-tip {
  margin-bottom: 20px;
}

.comments-list {
  min-height: 100px;
}

.no-comments {
  padding: 20px 0;
}

.comment-item {
  padding: 15px 0;
  border-bottom: 1px solid #f0f0f0;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: bold;
  color: #409eff;
  font-size: 14px;
}

.comment-time {
  color: #999;
  font-size: 12px;
}

.comment-content {
  color: #666;
  line-height: 1.6;
  font-size: 14px;
  margin-bottom: 8px;
  word-break: break-word;
}

.comment-actions {
  text-align: right;
}

/* 平板端适配 (768px以下) */
@media (max-width: 768px) {
  .post-detail-container {
    width: 100%;
    padding: 0 16px;
  }
  
  .post-detail-card {
    padding: 16px;
  }
  
  .post-title {
    font-size: 20px;
  }
  
  .post-content {
    font-size: 16px;
    line-height: 1.7;
  }
  
  .post-content :deep(pre) {
    padding: 0.8em;
    font-size: 14px;
  }
  
  .post-content :deep(table) {
    font-size: 14px;
  }
  
  .post-actions {
    display: flex;
    gap: 10px;
    justify-content: flex-start;
  }
  
  /* 按钮点击区域至少44x44px */
  :deep(.el-button) {
    min-height: 44px;
    min-width: 44px;
    padding: 12px 20px;
  }
  
  /* 评论区优化 */
  .comments-section {
    padding: 16px;
  }
  
  .comment-form :deep(.el-textarea__inner) {
    font-size: 16px;
  }
  
  .comment-content {
    font-size: 15px;
  }
}

/* 手机端适配 (480px以下) */
@media (max-width: 480px) {
  .post-detail-container {
    padding: 0 12px;
  }
  
  .post-detail-card {
    padding: 12px;
  }
  
  .post-title {
    font-size: 18px;
  }
  
  .post-content {
    font-size: 16px;
    line-height: 1.6;
  }
  
  .post-content :deep(h1) {
    font-size: 1.6em;
  }
  
  .post-content :deep(h2) {
    font-size: 1.3em;
  }
  
  .post-content :deep(h3) {
    font-size: 1.1em;
  }
  
  .post-content :deep(pre) {
    padding: 0.6em;
    font-size: 13px;
  }
  
  .post-content :deep(table) {
    font-size: 13px;
  }
  
  .comments-section {
    padding: 12px;
  }
  
  .comments-title {
    font-size: 16px;
  }
  
  .comment-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
  
  .comment-author {
    font-size: 14px;
  }
  
  .comment-content {
    font-size: 16px;
  }
  
  .comment-actions {
    text-align: left;
  }
}
</style>