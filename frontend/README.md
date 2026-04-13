# FastAPI Blog - Vue前端

这是一个基于 Vue 3 和 Element Plus 的前端项目，与 FastAPI 后端配合使用。

## 技术栈

- Vue 3
- Element Plus (UI框架)
- Vue Router (路由管理)
- Vuex (状态管理)
- Axios (HTTP客户端)
- Vite (构建工具)

## 功能特性

- 用户注册/登录
- 文章列表展示
- 创建/编辑/删除文章
- 个人资料管理
- 响应式设计

## 开发环境搭建

### 前提条件

- Node.js (>=14.0.0)
- FastAPI 后端服务正在运行 (默认端口: 8000)

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

前端将在 `http://localhost:3000` 上启动，并自动代理 `/api` 请求到后端服务。

### 构建生产版本

```bash
npm run build
```

## 目录结构

```
src/
├── assets/           # 静态资源
├── components/       # 公共组件
├── views/            # 页面组件
├── router/           # 路由配置
├── store/            # Vuex状态管理
│   └── modules/      # 状态模块
├── utils/            # 工具函数
└── App.vue          # 主应用组件
└── main.js          # 应用入口
```

## API 代理

开发环境中，所有 `/api` 请求都会被代理到 `http://127.0.0.1:8000`，这样可以避免跨域问题。

## 注意事项

1. 确保后端 FastAPI 服务正在运行
2. 用户认证使用 JWT Token，存储在 localStorage 中
3. 所有需要认证的 API 请求都会自动带上 Authorization header