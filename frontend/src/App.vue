<template>
  <div>
    <div id="nav">
      <el-menu
        :default-active="$route.path"
        mode="horizontal"
        router
        @select="handleMenuSelect"
      >
        <el-menu-item index="/">首页</el-menu-item>
        <div class="flex-grow" />
        <template v-if="!isLoggedIn">
          <el-menu-item index="/login">登录</el-menu-item>
          <el-menu-item index="/register">注册</el-menu-item>
        </template>
        <template v-else>
          <el-menu-item index="/profile">个人资料</el-menu-item>
          <el-sub-menu index="2">
            <template #title>{{ currentUser.username }}</template>
            <el-menu-item index="/logout" @click="logout">退出登录</el-menu-item>
          </el-sub-menu>
        </template>
      </el-menu>
    </div>
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const store = useStore()
    const router = useRouter()

    const isLoggedIn = computed(() => store.state.auth.isLoggedIn)
    const currentUser = computed(() => store.state.auth.currentUser)

    const handleMenuSelect = (key) => {
      // 处理菜单选择
    }

    const logout = () => {
      store.dispatch('auth/logout')
      router.push('/login')
    }

    onMounted(() => {
      // 检查是否已有登录状态
      const token = localStorage.getItem('token')
      if (token) {
        store.commit('auth/SET_TOKEN', token)
        // 可以在这里获取用户信息
      }
    })

    return {
      isLoggedIn,
      currentUser,
      handleMenuSelect,
      logout
    }
  }
}
</script>

<style>
/* 全局基础样式 */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.main-content {
  min-height: calc(100vh - 60px);
  padding: 20px;
}

.flex-grow {
  flex-grow: 1;
}

.el-menu {
  border-radius: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 平板端适配 (768px以下) */
@media (max-width: 768px) {
  .main-content {
    padding: 16px;
  }
  
  /* 导航栏改为垂直堆叠 */
  .el-menu--horizontal {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
  }
  
  .el-menu--horizontal > .el-menu-item {
    padding: 0 12px;
    font-size: 14px;
    height: 48px;
    line-height: 48px;
    min-width: 44px;
    min-height: 44px;
  }
  
  /* 确保点击区域足够大 */
  .el-menu-item,
  .el-sub-menu__title {
    min-height: 44px;
    min-width: 44px;
  }
}

/* 手机端适配 (480px以下) */
@media (max-width: 480px) {
  .main-content {
    padding: 12px;
  }
  
  /* 导航栏进一步简化 */
  .el-menu--horizontal {
    flex-direction: column;
  }
  
  .el-menu--horizontal > .el-menu-item {
    width: 100%;
    text-align: center;
    padding: 0 16px;
    font-size: 15px;
  }
  
  .flex-grow {
    display: none;
  }
}
</style>