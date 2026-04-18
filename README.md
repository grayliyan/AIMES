# 知识库系统

一个具有RAG智能问答功能的企业内部知识库系统。

## 功能特性

- 用户注册与登录（JWT认证）
- 文档管理（增删改查）
- 分类和标签组织
- 全文搜索
- RAG智能问答（RAGFlow集成）
- 版本历史（待实现）

## 技术栈

### 前端
- Vue 3 + Vite
- Vue Router
- Pinia（状态管理）
- Axios（HTTP客户端）

### 后端
- FastAPI
- SQLAlchemy（ORM）
- PostgreSQL（数据库）
- RAGFlow（RAG引擎）
- JWT（用户认证）

### 基础设施
- Docker & Docker Compose
- PostgreSQL 15
- RAGFlow

## 快速开始

1. **克隆仓库**
   ```bash
   git clone <repository-url>
   cd knowledge-base
   ```

2. **使用Docker Compose启动服务**
   ```bash
   docker-compose up -d
   ```

3. **访问应用**
   - 前端: http://localhost:5173
   - 后端API: http://localhost:8000
   - API文档: http://localhost:8000/docs
   - RAGFlow: http://localhost:9380

## 开发

### 前端开发
```bash
cd frontend
npm install
npm run dev
```

### 后端开发
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 项目结构

```
├── frontend/              # Vue.js前端
│   ├── src/
│   │   ├── assets/       # 静态资源
│   │   ├── router/       # Vue Router配置
│   │   ├── stores/       # Pinia状态管理
│   │   ├── views/        # 页面组件
│   │   └── main.js       # 入口文件
│   ├── package.json
│   └── vite.config.js
├── backend/               # FastAPI后端
│   ├── app/
│   │   ├── api/          # API端点
│   │   ├── core/         # 配置
│   │   ├── crud/         # 数据库操作
│   │   ├── db/           # 数据库设置
│   │   ├── models/       # SQLAlchemy模型
│   │   └── schemas/      # Pydantic模式
│   ├── main.py
│   └── requirements.txt
├── docs/                  # 文档
├── docker-compose.yml     # Docker服务
└── README.md
```

## API端点

### 认证
- `POST /api/v1/login/login` - 用户登录
- `POST /api/v1/login/register` - 用户注册
- `GET /api/v1/login/me` - 获取当前用户信息

### 文档
- `GET /api/v1/documents/` - 获取文档列表
- `POST /api/v1/documents/` - 创建文档
- `GET /api/v1/documents/{id}` - 获取文档详情
- `PUT /api/v1/documents/{id}` - 更新文档
- `DELETE /api/v1/documents/{id}` - 删除文档

### 问答
- `POST /api/v1/qa/ask` - 提问

## 配置

在backend目录下创建`.env`文件：

```env
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=knowledge_base
SECRET_KEY=your_secret_key_here
```

## 贡献

1. Fork仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

本项目采用MIT许可证。