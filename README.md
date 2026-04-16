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
│   │   ├── api/v1/        # API 路由层（按业务模块拆分）
│   │   ├── core/          # 核心配置与异常处理
│   │   ├── models/        # 数据库模型层
│   │   ├── repositories/  # 数据访问层
│   │   ├── schemas/       # Pydantic 数据验证层
│   │   ├── services/      # 业务逻辑层
│   │   ├── utils/         # 工具函数
│   │   ├── main.py        # FastAPI 应用入口
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
- ✅ Markdown 文章编辑与渲染（EasyMDE 编辑器）
- ✅ 文章 CRUD 操作
- ✅ 评论系统（创建、查看、删除）
- ✅ 点赞功能（文章点赞、评论点赞）
- ✅ 用户个人中心
- ✅ 响应式设计，完美支持移动端
- ✅ RESTful API 设计
- ✅ 分层架构（Router → Service → Repository → Model）
- ✅ 统一响应格式与异常处理
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

**API 文档：**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

> 💡 **提示：** 所有 API 接口的详细文档请通过 Swagger UI 查看，会自动同步最新的接口定义。

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

**前端调用示例：**
```javascript
// 前端代码
request.get('/posts')              // → 后端 /api/v1/posts
request.post('/users/login', data) // → 后端 /api/v1/users/login
```

> ⚠️ **注意：** 前端调用时不需要加 `/api/v1` 前缀，Vite 代理会自动处理。


## 移动端适配

项目已优化移动端体验：

- 响应式布局（768px 断点）
- 移动端单列显示
- 图片、代码块、表格自适应
- 触摸友好的按钮尺寸
- 表单移动端优化

## 开发指南

### 架构说明

本项目采用分层架构设计：

```
请求流程：
Client → Router (api/v1/) → Service → Repository → Model → Database
                ↓
            Response (统一格式)
```

- **Router 层**：处理 HTTP 请求与响应，参数验证
- **Service 层**：业务逻辑处理（可选，复杂业务使用）
- **Repository 层**：数据访问操作，封装数据库查询
- **Model 层**：数据库模型定义
- **Schema 层**：Pydantic 数据验证与序列化

### 添加新功能

1. **数据库模型**：在 `backend/app/models/` 定义 SQLAlchemy 模型
2. **数据验证**：在 `backend/app/schemas/` 定义 Pydantic Schema
3. **数据访问**：在 `backend/app/repositories/` 实现 CRUD 操作
4. **API 路由**：在 `backend/app/api/v1/` 创建路由文件
5. **注册路由**：在 `backend/app/main.py` 中 include_router
6. **前端 Store**：在 `frontend/src/store/modules/` 添加 Vuex module
7. **前端页面**：在 Vue 组件中调用 Store actions

### 统一响应格式

所有 API 接口返回统一的 JSON 格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {...},
  "timestamp": "2026-04-16T10:30:00"
}
```

前端请求拦截器会自动处理该格式，提取 `data` 字段。

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
