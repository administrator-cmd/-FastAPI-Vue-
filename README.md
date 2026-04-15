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
│   ├── app/
│   │   ├── api/v1/        # API 路由（按业务模块拆分）
│   │   │   ├── users.py   # 用户相关接口
│   │   │   ├── posts.py   # 文章相关接口
│   │   │   └── comments.py # 评论相关接口
│   │   ├── crud/          # 数据库操作层
│   │   ├── models/        # 数据库模型
│   │   ├── schemas/       # Pydantic 数据验证
│   │   ├── utils/         # 工具函数
│   │   ├── main.py        # FastAPI 应用入口
│   │   ├── database.py    # 数据库连接
│   │   └── dependencies.py # 依赖注入
│   └── requirements.txt   # Python 依赖
├── frontend/
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   ├── store/modules/ # Vuex 状态管理
│   │   ├── router/        # 路由配置
│   │   └── utils/         # 工具函数
│   ├── package.json
│   └── vite.config.js
└── README.md
```


## 功能特性

- ✅ 用户注册/登录（JWT 认证）
- ✅ Markdown 文章编辑（EasyMDE 编辑器）
- ✅ 文章 CRUD 操作
- ✅ 文章内容自动转换为 HTML
- ✅ 评论系统（创建、查看、删除）
- ✅ 用户个人中心
- ✅ 响应式设计，支持移动端
- ✅ RESTful API 设计
- ✅ 模块化架构（按业务垂直拆分）
- ✅ 请求拦截器自动携带 Token

## 快速开始

### 后端启动

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
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


前端服务运行在 `http://localhost:3000`

## API 接口

### 用户接口

| 方法 | 路径 | 说明 | 需要认证 |
|------|------|------|----------|
| POST | `/api/v1/users/register` | 用户注册 | 否 |
| POST | `/api/v1/users/login` | 用户登录（参数：account, password） | 否 |
| GET | `/api/v1/users/profile` | 获取当前用户信息 | 是 |
| GET | `/api/v1/users` | 获取用户列表 | 否 |

### 文章接口

| 方法 | 路径 | 说明 | 需要认证 |
|------|------|------|----------|
| GET | `/api/v1/posts` | 获取文章列表（支持分页和搜索） | 否 |
| GET | `/api/v1/posts/{post_id}` | 获取文章详情 | 否 |
| POST | `/api/v1/posts` | 创建文章 | 是 |
| PUT | `/api/v1/posts/{post_id}` | 更新文章 | 是 |
| DELETE | `/api/v1/posts/{post_id}` | 删除文章 | 是 |
| GET | `/api/v1/posts/user/{user_id}/posts` | 获取指定用户的文章 | 否 |

### 评论接口

| 方法 | 路径 | 说明 | 需要认证 |
|------|------|------|----------|
| GET | `/api/v1/comments/posts/{post_id}/comments` | 获取文章评论列表 | 否 |
| POST | `/api/v1/comments/posts/{post_id}/comments` | 创建评论 | 是 |
| DELETE | `/api/v1/comments/{comment_id}` | 删除评论 | 是 |

**注意：** 评论接口路径为 `/comments/posts/{id}/comments`，不是 `/posts/{id}/comments`

## 配置说明

### 前端代理配置

`frontend/vite.config.js` 已配置反向代理，将 `/api` 请求转发到后端并添加版本前缀：

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '/api/v1')
    }
  }
}
```

前端调用示例：
- `request.get('/posts')` → 后端 `/api/v1/posts`
- `request.get('/comments/posts/1/comments')` → 后端 `/api/v1/comments/posts/1/comments`


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

1. 在 `backend/app/models/` 定义数据库模型
2. 在 `backend/app/schemas/` 定义 Pydantic 模型
3. 在 `backend/app/crud/` 实现数据库操作
4. 在 `backend/app/api/v1/` 创建或修改路由文件
5. 在 `backend/app/main.py` 注册路由
6. 在 `frontend/src/store/modules/` 添加 Vuex actions
7. 在 Vue 组件中调用

**注意：** 前端调用时不需要加 `/api/v1` 前缀，Vite 代理会自动处理。

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
