<template>
  <div class="edit-post-container">
    <el-card class="edit-post-card">
      <template #header>
        <div class="card-header">
          <h2>编辑文章</h2>
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
          <textarea id="post-content-editor"></textarea>
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            @click="submitForm" 
            :loading="submitting"
            style="margin-right: 10px;"
          >
            更新文章
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
import { reactive, ref, toRefs, onMounted, onBeforeUnmount } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import EasyMDE from 'easymde'
import 'easymde/dist/easymde.min.css'

export default {
  name: 'EditPost',
  setup() {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()
    const postFormRef = ref(null)
    let easyMDE = null
    
    const state = reactive({
      form: {
        title: '',
        content: ''
      },
      submitting: false,
      postId: route.params.id,
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
    
    // 初始化 Markdown 编辑器
    const initEditor = () => {
      easyMDE = new EasyMDE({
        element: document.getElementById('post-content-editor'),
        spellChecker: false,
        autosave: {
          enabled: false
        },
        toolbar: [
          'bold', 'italic', 'heading', '|',
          'quote', 'unordered-list', 'ordered-list', '|',
          'link', 'image', '|',
          'preview', 'side-by-side', 'fullscreen', '|',
          'guide'
        ],
        placeholder: '请输入文章内容（支持 Markdown）',
        status: false
      })
      
      // 监听编辑器内容变化，同步到表单
      easyMDE.codemirror.on('change', () => {
        state.form.content = easyMDE.value()
      })
    }
    
    // 加载文章详情
    const loadPost = async () => {
      try {
        await store.dispatch('posts/fetchPostById', state.postId)
        const post = store.getters['posts/currentPost']
        
        // 检查是否有编辑权限
        const currentUser = store.getters['auth/currentUser']
        if (post.author_id !== currentUser.id) {
          ElMessage.error('没有权限编辑此文章')
          router.push('/')
          return
        }
        
        state.form.title = post.title
        state.form.content = post.content
        
        // 填充编辑器内容
        if (easyMDE) {
          easyMDE.value(post.content)
        }
      } catch (error) {
        console.error('加载文章失败:', error)
        ElMessage.error('加载文章失败')
        router.push('/')
      }
    }
    
    const submitForm = async () => {
      try {
        // 从编辑器获取最新内容
        state.form.content = easyMDE.value()
        
        await postFormRef.value.validate()
        
        state.submitting = true
        
        await store.dispatch('posts/updatePost', {
          id: parseInt(state.postId),
          postData: {
            title: state.form.title,
            content: state.form.content
          }
        })
        
        ElMessage.success('文章更新成功')
        router.push(`/posts/${state.postId}`)
      } catch (error) {
        console.error('更新文章失败:', error)
        const errorData = error.response?.data?.detail || error.response?.data?.details || error.detail || error.details
        if (Array.isArray(errorData)) {
          ElMessage.error(errorData.map(e => (e.msg || e || '')).join('; '))
        } else {
          ElMessage.error(errorData || '更新失败，请重试')
        }
      } finally {
        state.submitting = false
      }
    }
    
    onMounted(() => {
      initEditor()
      loadPost()
    })
    
    onBeforeUnmount(() => {
      // 清理编辑器实例
      if (easyMDE) {
        easyMDE.toTextArea()
        easyMDE = null
      }
    })
    
    return {
      ...toRefs(state),
      postFormRef,
      submitForm
    }
  }
}
</script>

<style scoped>
.edit-post-container {
  max-width: 1000px;
  margin: 0 auto;
}

.edit-post-card {
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* EasyMDE 样式调整 */
:deep(.EasyMDEContainer) {
  margin-top: 10px;
}

:deep(.editor-toolbar) {
  border-color: #dcdfe6;
}

:deep(.CodeMirror) {
  border-color: #dcdfe6;
  min-height: 400px;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .edit-post-container {
    width: 100%;
  }
  
  .edit-post-card {
    padding: 12px;
  }
  
  :deep(.CodeMirror) {
    min-height: 300px;
    font-size: 14px;
  }
  
  :deep(.editor-toolbar) {
    font-size: 13px;
  }
  
  :deep(.el-form-item__label) {
    font-size: 14px;
  }
}
</style>