<template>
  <div class="create-post-container">
    <el-card class="create-post-card">
      <template #header>
        <div class="card-header">
          <h2>撰写新文章</h2>
        </div>
      </template>
      
      <el-form :model="form" :rules="rules" ref="postFormRef" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input 
            v-model="form.title" 
            placeholder="请输入文章标题"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="内容" prop="content">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="15"
            placeholder="请输入文章内容"
            maxlength="5000"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            @click="submitForm" 
            :loading="submitting"
            style="margin-right: 10px;"
          >
            发布文章
          </el-button>
          <el-button @click="$router.go(-1)">
            取消
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { reactive, ref, toRefs } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

export default {
  name: 'CreatePost',
  setup() {
    const store = useStore()
    const router = useRouter()
    const postFormRef = ref(null)
    
    const state = reactive({
      form: {
        title: '',
        content: ''
      },
      submitting: false,
      rules: {
        title: [
          { required: true, message: '请输入文章标题', trigger: 'blur' },
          { min: 3, max: 100, message: '标题长度应在3-100之间', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入文章内容', trigger: 'blur' },
          { min: 10, message: '内容长度不能少于10个字符', trigger: 'blur' }
        ]
      }
    })
    
    const submitForm = async () => {
      try {
        await postFormRef.value.validate()
        
        state.submitting = true
        
        await store.dispatch('posts/createPost', {
          title: state.form.title,
          content: state.form.content
        })
        
        ElMessage.success('文章发布成功')
        router.push('/')
      } catch (error) {
        console.error('发布文章失败:', error)
        const errorData = error.response?.data?.detail || error.response?.data?.details || error.detail || error.details
        if (Array.isArray(errorData)) {
          ElMessage.error(errorData.map(e => (e.msg || e || '')).join('; '))
        } else {
          ElMessage.error(errorData || '发布失败，请重试')
        }
      } finally {
        state.submitting = false
      }
    }
    
    return {
      ...toRefs(state),
      postFormRef,
      submitForm
    }
  }
}
</script>

<style scoped>
.create-post-container {
  max-width: 1000px;
  margin: 0 auto;
}

.create-post-card {
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>