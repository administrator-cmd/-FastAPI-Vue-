<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <h2>个人资料</h2>
        </div>
      </template>
      
      <div class="profile-info">
        <el-descriptions :column="1" border>
          <el-descriptions-item width="150px" label="用户ID">
            {{ currentUser.id }}
          </el-descriptions-item>
          <el-descriptions-item width="150px" label="用户名">
            {{ currentUser.username }}
          </el-descriptions-item>
          <el-descriptions-item width="150px" label="邮箱">
            {{ currentUser.email }}
          </el-descriptions-item>
          <el-descriptions-item width="150px" label="注册时间">
            {{ formatDate(currentUser.created_at) }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>
    
    <el-card class="my-posts" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <h2>我的文章</h2>
        </div>
      </template>
      
      <div v-if="loading" class="loading">
        <el-skeleton :rows="4" animated />
      </div>
      
      <div v-else>
        <el-table 
          :data="userPosts" 
          stripe 
          style="width: 100%"
          @row-click="goToPost"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="标题" />
          <el-table-column prop="created_at" label="创建时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <el-button size="small" @click.stop="editPost(row.id)">编辑</el-button>
              <el-popconfirm 
                title="确定要删除这篇文章吗？" 
                @confirm="deletePost(row.id)"
              >
                <template #reference>
                  <el-button size="small" type="danger">删除</el-button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
        
        <div class="no-posts" v-if="userPosts.length === 0">
          <el-empty description="暂无文章" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'

export default {
  name: 'Profile',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const loading = ref(false)
    const userPosts = ref([])
    
    const currentUser = computed(() => store.getters['auth/currentUser'])
    
    const formatDate = (dateString) => {
      return dayjs(dateString).format('YYYY-MM-DD HH:mm')
    }
    
    const loadUserPosts = async () => {
      try {
        loading.value = true
        const response = await store.dispatch('posts/fetchUserPosts', currentUser.value.id)
        userPosts.value = response
      } catch (error) {
        console.error('加载用户文章失败:', error)
      } finally {
        loading.value = false
      }
    }
    
    const goToPost = (row) => {
      router.push(`/posts/${row.id}`)
    }
    
    const editPost = (postId) => {
      router.push(`/posts/${postId}/edit`)
    }
    
    const deletePost = async (postId) => {
      try {
        await store.dispatch('posts/deletePost', postId)
        ElMessage.success('删除成功')
        // 重新加载文章列表
        loadUserPosts()
      } catch (error) {
        console.error('删除文章失败:', error)
        ElMessage.error('删除失败')
      }
    }
    
    onMounted(async () => {
      try {
        // 加载用户信息
        await store.dispatch('auth/loadCurrentUser')
        // 加载用户的文章
        loadUserPosts()
      } catch (error) {
        console.error('加载用户信息失败:', error)
      }
    })
    
    return {
      currentUser,
      userPosts,
      loading,
      formatDate,
      goToPost,
      editPost,
      deletePost
    }
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
}

.profile-card {
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.my-posts {
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-info {
  padding: 20px 0;
}

.loading {
  margin: 20px 0;
}

.no-posts {
  text-align: center;
  padding: 40px 0;
}

/* 平板端适配 (768px以下) */
@media (max-width: 768px) {
  .profile-container {
    width: 100%;
    padding: 0 16px;
  }
  
  .profile-card,
  .my-posts {
    padding: 16px;
  }
  
  /* 表格字体优化 */
  :deep(.el-table) {
    font-size: 14px;
  }
  
  :deep(.el-descriptions__label),
  :deep(.el-descriptions__content) {
    font-size: 14px;
  }
  
  /* 按钮点击区域至少44x44px */
  :deep(.el-button) {
    min-height: 44px;
    min-width: 44px;
    padding: 12px 16px;
  }
  
  /* 表格操作列按钮垂直排列 */
  :deep(.el-table .cell) {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }
}

/* 手机端适配 (480px以下) */
@media (max-width: 480px) {
  .profile-container {
    padding: 0 12px;
  }
  
  .profile-card,
  .my-posts {
    padding: 12px;
  }
  
  h2 {
    font-size: 18px;
  }
  
  :deep(.el-table) {
    font-size: 13px;
  }
  
  :deep(.el-descriptions__label),
  :deep(.el-descriptions__content) {
    font-size: 13px;
  }
  
  /* 表格改为卡片式布局 */
  :deep(.el-table__header) {
    display: none;
  }
  
  :deep(.el-table__body tr) {
    display: block;
    margin-bottom: 12px;
    border: 1px solid #ebeef5;
    border-radius: 4px;
    padding: 12px;
  }
  
  :deep(.el-table__body td) {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #f0f0f0;
  }
  
  :deep(.el-table__body td:last-child) {
    border-bottom: none;
  }
  
  :deep(.el-table__body td::before) {
    content: attr(data-label);
    font-weight: bold;
    margin-right: 10px;
  }
}
</style>