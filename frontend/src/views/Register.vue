<template>
  <div class="register-container">
    <el-card class="register-form" style="width: 400px;">
      <h2 style="text-align: center; margin-bottom: 20px;">用户注册</h2>
      <el-form :model="form" :rules="rules" ref="registerFormRef">
        <el-form-item prop="username">
          <el-input 
            v-model="form.username" 
            placeholder="用户名" 
            prefix-icon="el-icon-user"
          />
        </el-form-item>
        <el-form-item prop="email">
          <el-input 
            v-model="form.email" 
            type="email" 
            placeholder="邮箱" 
            prefix-icon="el-icon-message"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="密码" 
            prefix-icon="el-icon-lock"
          />
        </el-form-item>
        <el-form-item prop="nickname">
          <el-input 
            v-model="form.nickname" 
            placeholder="昵称（选填）" 
            prefix-icon="el-icon-star-on"
          />
        </el-form-item>
        <el-form-item prop="bio">
          <el-input 
            v-model="form.bio" 
            type="textarea" 
            :rows="3"
            placeholder="个人简介（选填）" 
          />
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input 
            v-model="form.confirmPassword" 
            type="password" 
            placeholder="确认密码" 
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
            注册
          </el-button>
        </el-form-item>
        <p style="text-align: center;">
          已有账号？<router-link to="/login">立即登录</router-link>
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
  name: 'Register',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const registerFormRef = ref(null)
    
    const state = reactive({
      form: {
        username: '',
        email: '',
        password: '',
        nickname: '',
        bio: '',
        confirmPassword: ''
      },
      loading: false,
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '用户名长度应在3-20之间', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 8, message: '密码长度不能少于8位', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请确认密码', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (value !== state.form.password) {
                callback(new Error('两次输入密码不一致'))
              } else {
                callback()
              }
            },
            trigger: 'blur'
          }
        ]
      }
    })
    
    const submitForm = async () => {
      try {
        await registerFormRef.value.validate()
        
        state.loading = true
        
        await store.dispatch('auth/register', {
          username: state.form.username,
          email: state.form.email,
          password: state.form.password
        })
        
        ElMessage.success('注册成功，请登录')
        router.push('/login')
      } catch (error) {
        console.error('注册失败:', error)
        console.log('完整错误响应:', error.response?.data)
        const errorData = error.response?.data?.detail || error.response?.data?.details || error.detail || error.details
        if (Array.isArray(errorData)) {
          ElMessage.error(errorData.map(e => e.msg).join('; '))
        } else {
          ElMessage.error(errorData || '注册失败，请重试')
        }
      } finally {
        state.loading = false
      }
    }
    
    return {
      ...toRefs(state),
      registerFormRef,
      submitForm
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.register-form {
  padding: 20px;
}
</style>