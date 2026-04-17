# FastAPI Blog 系统

一个基于 FastAPI + Vue 3 的全栈博客系统，支持 Markdown 编辑、用户认证、智能问答、移动端适配。

## 技术栈

### 后端
- **FastAPI** - 高性能 Python Web 框架
- **SQLAlchemy** - ORM 数据库操作
- **JWT** - 用户认证
- **SQLite** - 数据库
- **Markdown** - 文章渲染
- **httpx** - 异步 HTTP 客户端（AI API 调用）
- **python-dotenv** - 环境变量管理

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Element Plus** - UI 组件库
- **Vuex** - 状态管理
- **Vue Router** - 路由管理
- **EasyMDE** - Markdown 编辑器
- **Axios** - HTTP 客户端
- **响应式设计** - 完整移动端适配（768px/480px 断点）

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
│   │   ├── styles/        # 全局样式（含响应式）
│   │   └── utils/         # 工具函数
│   ├── package.json
│   ├── RESPONSIVE_GUIDE.md  # 响应式适配说明
│   ├── TESTING_GUIDE.md     # 测试指南
│   └── vite.config.js
└── README.md
```


## 功能特性

- ✅ 用户注册/登录（JWT 认证）
- ✅ Markdown 文章编辑与渲染（EasyMDE 编辑器）
- ✅ 文章 CRUD 操作
- ✅ 评论系统（创建、查看、删除）
- ✅ 点赞功能（文章点赞、评论点赞）
- ✅ **智能问答**（集成云端 AI API，支持多轮对话上下文）
- ✅ 用户个人中心
- ✅ **完整移动端适配**（768px/480px 断点，触摸友好）
- ✅ RESTful API 设计
- ✅ 分层架构（Router → Service → Repository → Model）
- ✅ 统一响应格式与异常处理
- ✅ 请求拦截器自动携带 Token
- ✅ 环境变量配置管理（.env 文件）

## 快速开始

### 环境配置

#### 1. 创建 `.env` 文件

在 `backend/` 目录下创建 `.env` 文件（**不要提交到 Git**）：

```env
# 数据库配置
DATABASE_URL=sqlite+aiosqlite:///./blog_v4.db

# JWT 配置
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI API 配置（智能问答功能）
AI_API_KEY=sk-your-api-key-here
AI_API_URL=https://api.openai.com/v1/chat/completions
AI_MODEL=gpt-3.5-turbo
```

> ⚠️ **重要：** 
> - `SECRET_KEY` 生产环境必须使用强随机密钥
> - `AI_API_KEY` 需要替换为你自己的 AI API 密钥
> - `.env` 文件已加入 `.gitignore`，不会上传到 GitHub

#### 2. 安装依赖

```bash
# 后端依赖
cd backend
pip install -r requirements.txt

# 前端依赖
cd frontend
npm install
```

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

# 安装依赖（如果还没安装）
npm install

# 启动开发服务器
npm run dev
```


前端服务运行在 `http://localhost:3000`

## 功能模块

### 智能问答

项目集成了云端 AI API，提供智能问答功能：

**功能特性：**
- 🤖 向 AI 提问，获取智能回答
- 💬 支持多轮对话上下文（可选）
- 📝 自动保存问答历史记录
- 🔒 仅登录用户可使用
- 📱 完整的移动端适配

**API 接口：**
- `POST /api/v1/qa/ask` - 向 AI 提问
- `GET /api/v1/qa/history` - 获取问答历史

**使用步骤：**
1. 在 `.env` 中配置 `AI_API_KEY`、`AI_API_URL`、`AI_MODEL`
2. 启动后端和前端服务
3. 登录后访问 `/qa` 页面即可使用

> 💡 **支持的 AI 服务商：** OpenAI、Azure OpenAI、国内大模型平台等（需兼容 OpenAI 格式）

---

## 配置说明

### 环境变量配置

项目使用 `python-dotenv` 管理敏感配置信息：

**配置文件位置：** `backend/.env`

**必需配置项：**
```env
# 数据库
DATABASE_URL=sqlite+aiosqlite:///./blog_v4.db

# JWT 认证
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI API（智能问答）
AI_API_KEY=your-api-key
AI_API_URL=https://api.openai.com/v1/chat/completions
AI_MODEL=gpt-3.5-turbo
```

**配置加载流程：**
```
app/core/config.py → load_dotenv() → os.getenv()
       ↓
所有模块通过 settings 对象访问配置
```

**示例代码：**
```python
from app.core.config import settings

# 访问配置
api_key = settings.AI_API_KEY
db_url = settings.DATABASE_URL
```

> ⚠️ **安全提示：**
> - `.env` 文件包含敏感信息，**切勿提交到版本控制系统**
> - 生产环境建议使用更安全的密钥管理方案（如 Vault、AWS Secrets Manager）

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

项目已完整优化移动端体验，支持手机、平板等多种设备：

### 响应式设计
- **媒体查询断点**：768px（平板）、480px（手机）
- **移动优先**：从小屏幕开始设计，逐步增强到大屏幕
- **容器自适应**：100% 宽度，左右内边距 16px/12px

### 布局优化
- ✅ **导航栏**：平板可换行，手机垂直堆叠
- ✅ **文章列表**：移动端单列垂直排列，侧边栏下移
- ✅ **表格转换**：手机端表格自动转换为卡片式布局
- ✅ **图片自适应**：所有图片 max-width: 100%

### 交互优化
- ✅ **触摸友好**：所有按钮和链接 ≥ 44x44px
- ✅ **字体优化**：正文不小于 16px，防止 iOS 自动缩放
- ✅ **输入框**：字体固定 16px，避免 iOS 自动放大
- ✅ **代码块**：支持横向滚动，字体自适应

### 测试方法

#### 浏览器开发者工具测试
```bash
# 启动前端开发服务器
cd frontend
npm run dev
```

1. 打开 Chrome DevTools (F12)
2. 点击设备工具栏图标或按 `Ctrl+Shift+M`
3. 选择预设设备进行测试：
   - iPhone SE (375×667)
   - iPhone 12 Pro (390×844)
   - iPad (768×1024)

#### 真机测试
```bash
# 允许局域网访问
cd frontend
npm run dev -- --host
```
然后在手机浏览器访问显示的 IP 地址（如：http://192.168.1.100:5173）

### 技术实现

全局响应式样式文件：`frontend/src/styles/responsive.css`

各页面组件均包含独立的媒体查询样式：
```css
/* 平板端适配 */
@media (max-width: 768px) {
  /* 样式规则 */
}

/* 手机端适配 */
@media (max-width: 480px) {
  /* 样式规则 */
}
```

详细文档请参考：
- [RESPONSIVE_GUIDE.md](frontend/RESPONSIVE_GUIDE.md) - 响应式适配详细说明
- [TESTING_GUIDE.md](frontend/TESTING_GUIDE.md) - 完整测试指南

## 技术亮点

### 1. 分层架构设计

```
请求流程：
Client → Router (api/v1/) → Repository → Model → Database
                ↓
            Response (统一格式)
```

- **Router 层**：处理 HTTP 请求与响应，参数验证
- **Repository 层**：数据访问操作，封装数据库查询
- **Model 层**：数据库模型定义
- **Schema 层**：Pydantic 数据验证与序列化
- **Utils 层**：工具函数（JWT、AI API 调用等）

### 2. 统一响应格式

所有 API 接口返回统一的 JSON 格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {...},
  "timestamp": 1713168000000
}
```

前端请求拦截器会自动处理该格式，提取 `data` 字段。

### 3. 环境变量管理

- 使用 `python-dotenv` 加载 `.env` 文件
- 集中配置管理（`app/core/config.py`）
- 无硬编码配置，易于部署和维护

### 4. 异步编程

- 全程使用 `async/await` 异步编程
- SQLAlchemy 2.0 异步 ORM
- httpx 异步 HTTP 客户端

---

## 开发指南

### 添加新功能

1. **数据库模型**：在 `backend/app/models/` 定义 SQLAlchemy 模型
2. **数据验证**：在 `backend/app/schemas/` 定义 Pydantic Schema
3. **数据访问**：在 `backend/app/repositories/` 实现 CRUD 操作
4. **API 路由**：在 `backend/app/api/v1/` 创建路由文件
5. **注册路由**：在 `backend/app/main.py` 中 include_router
6. **前端 Store**：在 `frontend/src/store/modules/` 添加 Vuex module
7. **前端页面**：在 Vue 组件中调用 Store actions

参考智能问答功能的实现方式。

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

## 常见问题

### Q: 如何更换 AI API 服务商？

A: 修改 `.env` 文件中的 `AI_API_URL` 和 `AI_MODEL`，确保新服务商兼容 OpenAI 格式即可。

### Q: 为什么我的 `.env` 文件没有生效？

A: 检查以下几点：
1. 确认 `python-dotenv` 已安装
2. 确认 `.env` 文件在 `backend/` 目录下
3. 重启后端服务
4. 检查环境变量名是否正确

### Q: 如何部署到生产环境？

A: 
1. 设置强 `SECRET_KEY`
2. 配置真实的数据库（PostgreSQL/MySQL）
3. 使用 Gunicorn + Uvicorn 运行后端
4. 构建前端静态文件并配置 Nginx
5. 使用 HTTPS 证书

---

## License

MIT
