<template>
  <div class="login-container">
    <el-card class="login-form" style="width: 400px;">
      <h2 style="text-align: center; margin-bottom: 20px;">用户登录</h2>
      <el-form :model="form" :rules="rules" ref="loginFormRef">
        <el-form-item prop="account">
          <el-input 
            v-model="form.account" 
            placeholder="用户名或邮箱" 
            prefix-icon="el-icon-user"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="密码" 
            prefix-icon="el-icon-lock"
            @keyup.enter="submitForm"
          />
        </el-form-item>
        <el-form-item>
          <el-button 
            type="primary" 
            @click="submitForm" 
            :loading="loading"
            style="width: 100%;"
          >
            登录
          </el-button>
        </el-form-item>
        <p style="text-align: center;">
          还没有账号？<router-link to="/register">立即注册</router-link>
        </p>
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
  name: 'Login',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const loginFormRef = ref(null)
    
    const state = reactive({
      form: {
        account: '',
        password: ''
      },
      loading: false,
      rules: {
        account: [
          { required: true, message: '请输入用户名或邮箱', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
        ]
      }
    })
    
    const submitForm = async () => {
      try {
        await loginFormRef.value.validate()
        
        state.loading = true
        
        await store.dispatch('auth/login', {
          account: state.form.account,
          password: state.form.password
        })
        
        ElMessage.success('登录成功')
        
        // 获取用户信息
        try {
          await store.dispatch('auth/loadCurrentUser')
        } catch (error) {
          console.error('加载用户信息失败:', error)
        }
        
        router.push('/')
      } catch (error) {
        console.error('登录失败:', error)
        const errorData = error.response?.data?.detail || error.response?.data?.details || error.detail || error.details
        if (Array.isArray(errorData)) {
          ElMessage.error(errorData.map(e => (e.msg || e || '')).join('; '))
        } else {
          ElMessage.error(errorData || '登录失败，请重试')
        }
      } finally {
        state.loading = false
      }
    }
    
    return {
      ...toRefs(state),
      loginFormRef,
      submitForm
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.login-form {
  padding: 20px;
}

/* 平板端适配 (768px以下) */
@media (max-width: 768px) {
  .login-form {
    width: 100% !important;
    margin: 0 16px;
    padding: 16px;
  }
  
  /* 输入框字体不小于16px，防止iOS自动缩放 */
  :deep(.el-input__inner) {
    font-size: 16px;
    min-height: 44px;
  }
  
  /* 按钮点击区域至少44x44px */
  :deep(.el-button) {
    min-height: 44px;
    font-size: 16px;
  }
}

/* 手机端适配 (480px以下) */
@media (max-width: 480px) {
  .login-form {
    margin: 0 12px;
    padding: 12px;
  }
  
  :deep(.el-card__body) {
    padding: 12px;
  }
  
  h2 {
    font-size: 20px;
  }
}
</style>