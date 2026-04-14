# FastAPI Blog 系统

一个基于 FastAPI + Vue 3 的全栈博客系统，支持 Markdown 编辑、用户认证、移动端适配。

## 技术栈

### 后端
- **FastAPI** - 高性能 Python Web 框架
- **SQLAlchemy** - ORM 数据库操作
- **JWT** - 用户认证
- **SQLite** - 数据库
- **Markdown** - 文章渲染

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Element Plus** - UI 组件库
- **Vuex** - 状态管理
- **Vue Router** - 路由管理
- **EasyMDE** - Markdown 编辑器
- **Axios** - HTTP 客户端
- **响应式设计** - 支持移动端

## 项目结构

```
Fastapi-blog/
├── backend/
│   ├── main.py          # FastAPI 应用入口
│   ├── models.py        # 数据库模型
│   ├── schemas.py       # Pydantic 数据验证
│   ├── crud.py          # 数据库操作
│   ├── auth.py          # JWT 认证
│   ├── database.py      # 数据库连接
│   ├── dependencies.py  # 依赖注入
│   ├── utils.py         # 工具函数
│   └── requirements.txt # Python 依赖
├── frontend/
│   ├── src/
│   │   ├── views/       # 页面组件
│   │   ├── store/       # Vuex 状态管理
│   │   ├── router/      # 路由配置
│   │   └── utils/       # 工具函数
│   ├── package.json
│   └── vite.config.js
└── alembic.ini          # 数据库迁移配置
```


## 功能特性

- ✅ 用户注册/登录（JWT 认证）
- ✅ Markdown 文章编辑（EasyMDE 编辑器）
- ✅ 文章 CRUD 操作
- ✅ 文章内容自动转换为 HTML
- ✅ 用户个人中心
- ✅ 响应式设计，支持移动端
- ✅ RESTful API 设计
- ✅ 请求拦截器自动携带 Token

## 快速开始

### 后端启动

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```


后端服务运行在 `http://localhost:8000`

API 文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```


前端服务运行在 `http://localhost:5173`

## API 接口

### 认证接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/auth/register` | 用户注册 |
| POST | `/auth/login` | 用户登录 |
| GET | `/auth/me` | 获取当前用户信息 |

### 文章接口

| 方法 | 路径 | 说明 | 需要认证 |
|------|------|------|----------|
| GET | `/posts` | 获取文章列表 | 否 |
| GET | `/posts/{post_id}` | 获取文章详情 | 否 |
| POST | `/posts` | 创建文章 | 是 |
| PUT | `/posts/{post_id}` | 更新文章 | 是 |
| DELETE | `/posts/{post_id}` | 删除文章 | 是 |

### 用户接口

| 方法 | 路径 | 说明 | 需要认证 |
|------|------|------|----------|
| GET | `/users/{user_id}` | 获取用户信息 | 是 |
| GET | `/users/{user_id}/posts` | 获取用户文章列表 | 是 |

## 配置说明

### 前端代理配置

`frontend/vite.config.js` 已配置反向代理，将 `/api` 请求转发到后端：

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```


### 请求拦截器

前端使用 Axios 拦截器自动携带 JWT Token：

```javascript
// 请求拦截器
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```


## 移动端适配

项目已优化移动端体验：

- 响应式布局（768px 断点）
- 移动端单列显示
- 图片、代码块、表格自适应
- 触摸友好的按钮尺寸
- 表单移动端优化

## 开发说明

### 添加新接口

1. 在 `backend/models.py` 定义数据库模型
2. 在 `backend/schemas.py` 定义 Pydantic 模型
3. 在 `backend/crud.py` 实现数据库操作
4. 在 `backend/main.py` 注册路由
5. 在 `frontend/src/store/modules/` 添加 Vuex actions
6. 在 Vue 组件中调用

### 数据库迁移

```bash
# 生成迁移文件
alembic revision --autogenerate -m "description"

# 执行迁移
alembic upgrade head
```


## 依赖版本

- Python 3.8+
- Node.js 16+
- FastAPI 0.104+
- Vue 3.2+
- Element Plus 2.2+

## License

MIT
