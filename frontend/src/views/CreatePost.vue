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
        
        <el-form-item label="标签">
          <div class="tag-input-container">
            <el-tag
              v-for="tag in inputTags"
              :key="tag"
              closable
              @close="removeTag(tag)"
              style="margin-right: 8px; margin-bottom: 8px;"
            >
              {{ tag }}
            </el-tag>
            <el-input
              v-if="tagInputVisible"
              ref="tagInputRef"
              v-model="tagInputValue"
              size="small"
              style="width: 150px;"
              @keyup.enter="handleTagInputConfirm"
              @blur="handleTagInputConfirm"
            />
            <el-button 
              v-else 
              size="small" 
              @click="showTagInput"
            >
              + 添加标签
            </el-button>
          </div>
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
import { reactive, ref, toRefs, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import EasyMDE from 'easymde'
import 'easymde/dist/easymde.min.css'

export default {
  name: 'CreatePost',
  setup() {
    const store = useStore()
    const router = useRouter()
    const postFormRef = ref(null)
    const tagInputRef = ref(null)
    let easyMDE = null
    
    // 标签相关状态
    const inputTags = ref([])
    const tagInputVisible = ref(false)
    const tagInputValue = ref('')
    
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
    
    const submitForm = async () => {
      try {
        // 从编辑器获取最新内容
        state.form.content = easyMDE.value()
        
        await postFormRef.value.validate()
        
        state.submitting = true
        
        await store.dispatch('posts/createPost', {
          title: state.form.title,
          content: state.form.content,
          tag_names: inputTags.value
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
    
    // 显示标签输入框
    const showTagInput = () => {
      tagInputVisible.value = true
      nextTick(() => {
        tagInputRef.value?.focus()
      })
    }
    
    // 处理标签输入确认
    const handleTagInputConfirm = () => {
      const tagName = tagInputValue.value.trim()
      if (tagName && !inputTags.value.includes(tagName)) {
        inputTags.value.push(tagName)
      }
      tagInputVisible.value = false
      tagInputValue.value = ''
    }
    
    // 移除已选标签
    const removeTag = (tagName) => {
      inputTags.value = inputTags.value.filter(tag => tag !== tagName)
    }
    
    onMounted(async () => {
      initEditor()
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
      tagInputRef,
      submitForm,
      inputTags,
      tagInputVisible,
      tagInputValue,
      showTagInput,
      handleTagInputConfirm,
      removeTag
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

.tag-input-container {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
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

/* 平板端适配 (768px以下) */
@media (max-width: 768px) {
  .create-post-container {
    width: 100%;
    padding: 0 16px;
  }
  
  .create-post-card {
    padding: 16px;
  }
  
  :deep(.CodeMirror) {
    min-height: 300px;
    font-size: 16px;
  }
  
  :deep(.editor-toolbar) {
    font-size: 14px;
  }
  
  :deep(.el-form-item__label) {
    font-size: 14px;
  }
  
  /* 输入框字体不小于16px，防止iOS自动缩放 */
  :deep(.el-input__inner) {
    font-size: 16px;
    min-height: 44px;
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
  .create-post-container {
    padding: 0 12px;
  }
  
  .create-post-card {
    padding: 12px;
  }
  
  h2 {
    font-size: 18px;
  }
  
  :deep(.CodeMirror) {
    min-height: 250px;
    font-size: 15px;
  }
  
  :deep(.editor-toolbar) {
    font-size: 13px;
  }
  
  /* 表单标签垂直排列 */
  :deep(.el-form-item__label) {
    width: 100% !important;
    text-align: left !important;
    margin-bottom: 8px;
  }
  
  :deep(.el-form-item__content) {
    margin-left: 0 !important;
  }
}
</style>