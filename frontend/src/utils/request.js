import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const service = axios.create({
  baseURL: '/api', // 代理到后端API
  timeout: 10000 // 请求超时时间
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 在发送请求之前添加token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    // 请求错误处理
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理统一响应格式
service.interceptors.response.use(
  response => {
    // 后端返回统一格式: { code, message, data, timestamp }
    const res = response.data
    
    // 如果响应已经是统一格式（包含code字段）
    if (res.code !== undefined) {
      // 成功响应 (2xx)
      if (res.code >= 200 && res.code < 300) {
        return res.data || res  // 返回data字段，如果没有则返回整个响应
      } else {
        // 业务错误
        ElMessage.error(res.message || '请求失败')
        return Promise.reject(new Error(res.message || '请求失败'))
      }
    }
    
    // 兼容旧格式，直接返回数据
    return res
  },
  error => {
    // HTTP 错误处理
    console.error('响应错误:', error)
    
    if (error.response) {
      const status = error.response.status
      const res = error.response.data
      
      // 处理统一格式的错误响应
      if (res && res.code !== undefined) {
        ElMessage.error(res.message || '请求失败')
      } else {
        // 根据HTTP状态码显示错误信息
        switch (status) {
          case 400:
            ElMessage.error('请求参数错误')
            break
          case 401:
            ElMessage.error('未授权，请重新登录')
            localStorage.removeItem('token')
            window.location.href = '/login'
            break
          case 403:
            ElMessage.error('拒绝访问')
            break
          case 404:
            ElMessage.error('请求资源不存在')
            break
          case 500:
            ElMessage.error('服务器内部错误')
            break
          default:
            ElMessage.error(res?.detail || res?.message || '请求失败')
        }
      }
    } else {
      ElMessage.error('网络连接失败')
    }
    
    return Promise.reject(error)
  }
)

export default service