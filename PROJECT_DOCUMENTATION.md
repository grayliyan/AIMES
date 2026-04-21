# AIMES 项目开发文档

## 项目概述

AIMES 是一个基于 RAG（检索增强生成）技术的企业知识库系统，支持文档管理、智能问答、用户权限管理等功能。

**技术栈：**
- 后端：FastAPI + SQLAlchemy + PostgreSQL
- 前端：Vue 3 + Vite
- AI：RAGFlow
- 部署：Docker Compose

---

## 开发过程

### 1. 项目初始化

项目使用 Docker Compose 进行容器化部署，包含以下服务：
- PostgreSQL（数据库）
- MySQL（RAGFlow 数据库）
- Redis（缓存）
- Elasticsearch（搜索引擎）
- MinIO（对象存储）
- FastAPI 后端
- Vue 3 前端
- RAGFlow（AI 服务）

### 2. 用户认证功能

#### 2.1 注册功能
实现了用户注册功能，包括用户名、邮箱、密码验证。

#### 2.2 登录功能
实现了 JWT Token 认证机制。

---

## 遇到的问题及解决方案

### 问题 1：bcrypt 版本不兼容

**错误现象：**
```
AttributeError: module 'bcrypt' has no attribute '__about__'
```

**原因分析：**
bcrypt 5.0.0 与 passlib 1.7.4 不兼容，passlib 依赖 bcrypt 的 `__about__` 属性，但新版本的 bcrypt 已移除该属性。

**解决方案：**
在 `requirements.txt` 中指定 bcrypt 版本为 4.0.1：
```txt
passlib==1.7.4
bcrypt==4.0.1
```

---

### 问题 2：数据库表未创建

**错误现象：**
注册时返回内部服务器错误，日志显示表不存在。

**原因分析：**
项目启动时没有自动创建数据库表结构。

**解决方案：**
1. 创建数据库初始化脚本 `backend/init_db.py`
2. 创建启动脚本 `backend/start.sh`，在启动前自动执行数据库初始化
3. 修改 Dockerfile 使用启动脚本

**代码：**
```python
# init_db.py
from sqlalchemy import create_engine
from app.core.config import settings
from app.db.base_class import Base
from app.models.user import User

def init_db():
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功！")
```

```bash
#!/bin/bash
# start.sh
echo "等待数据库启动..."
sleep 5

echo "初始化数据库..."
python init_db.py

echo "启动FastAPI应用..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

### 问题 3：注册按钮一直是灰色

**错误现象：**
注册页面的注册按钮一直处于禁用状态，无法点击。

**原因分析：**
在 Vue 3 中，`success` 变量初始化为空字符串 `''`，在绑定到 `disabled` 属性时：
```html
<button :disabled="loading || success">
```
空字符串 `''` 在 JavaScript 中是 falsy 值，但在 Vue 的属性绑定中，空字符串会被解释为 `true`。

**解决方案：**
使用 `!!` 操作符将字符串转换为布尔值：
```html
<button :disabled="loading || !!success">
```

---

### 问题 4：编辑按钮无响应

**错误现象：**
文档管理页面点击编辑按钮没有任何反应。

**原因分析：**
编辑按钮没有绑定点击事件处理函数。

**解决方案：**
1. 添加编辑弹窗状态变量
2. 添加编辑函数（openEditModal、closeEditModal、submitEdit）
3. 绑定点击事件

```vue
<button class="btn-edit" @click="openEditModal(doc)">编辑</button>
```

---

### 问题 5：SQLAlchemy 映射错误

**错误现象：**
```
sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize
When initializing mapper Mapper[User(user)], expression 'Role' failed to locate a name
```

**原因分析：**
User 模型中定义了与 Role 的关系，但 Role 模型在 User 之后加载，导致 SQLAlchemy 无法找到 Role 类。

**解决方案：**
在 `models/__init__.py` 中确保 Role 在 User 之前导入：
```python
from .role import Role
from .document import Document
from .user import User
```

---

### 问题 6：PowerShell 语法问题

**错误现象：**
使用 `&&` 连接命令时报错。

**原因分析：**
PowerShell 5.1 不支持 `&&` 语法（这是 Bash 的语法）。

**解决方案：**
1. 使用分号 `;` 分隔命令
2. 或者分别执行多个命令

```powershell
# 错误
docker-compose down && docker-compose up --build -d

# 正确
docker-compose down
docker-compose up --build -d
```

---

### 问题 7：文件上传测试困难

**错误现象：**
PowerShell 的 `Invoke-RestMethod` 不支持 `-Form` 参数进行文件上传。

**解决方案：**
使用 .NET 的 HttpClient 类进行文件上传：
```powershell
Add-Type -AssemblyName System.Net.Http
$handler = New-Object System.Net.Http.HttpClientHandler
$client = New-Object System.Net.Http.HttpClient($handler)
$form = New-Object System.Net.Http.MultipartFormDataContent
$fileContent = [System.IO.File]::ReadAllBytes("文件路径")
$fileByteArray = New-Object System.Net.Http.ByteArrayContent -ArgumentList @(,$fileContent)
$form.Add($fileByteArray, "file", "文件名")
$response = $client.PostAsync("URL", $form).Result
```

---

## 功能模块

### 1. 用户认证模块
- 用户注册
- 用户登录
- JWT Token 认证
- 路由守卫

### 2. 文档管理模块
- 文档列表展示
- 新建文档（手动输入）
- 上传文档（支持 TXT、MD、PDF、DOC、DOCX）
- 编辑文档
- 删除文档
- RAGFlow 自动解析

### 3. 智能问答模块
- 基于 RAG 技术的问答
- 与 RAGFlow 集成

### 4. 用户管理模块（管理员）
- 用户列表
- 创建用户
- 编辑用户
- 删除用户
- 启用/禁用用户
- 分配角色

### 5. 角色管理模块（管理员）
- 角色列表
- 创建角色
- 编辑角色
- 删除角色
- 权限配置

---

## 权限系统

### 权限类型
- `user_manage` - 用户管理
- `role_manage` - 角色管理
- `document_manage` - 文档管理
- `qa_access` - 智能问答
- `ragflow_access` - RAGFlow 访问

### 管理员权限
- `is_superuser` 字段标识是否为超级管理员
- 管理员可以访问用户管理和角色管理页面
- 管理员可以看到 RAGFlow 管理入口

---

## 数据库表结构

### user 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| username | String(50) | 用户名（唯一） |
| email | String(100) | 邮箱（唯一） |
| hashed_password | String(255) | 密码哈希 |
| full_name | String(100) | 姓名 |
| is_active | Boolean | 是否启用 |
| is_superuser | Boolean | 是否超级管理员 |
| role_id | Integer | 角色ID（外键） |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### role 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| name | String(50) | 角色名称（唯一） |
| description | String(200) | 角色描述 |
| permissions | Text | 权限列表（逗号分隔） |
| is_active | Boolean | 是否启用 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### document 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| title | String(255) | 文档标题 |
| content | Text | 文档内容 |
| category | String(100) | 分类 |
| tags | String(500) | 标签（逗号分隔） |
| file_name | String(255) | 原始文件名 |
| file_path | String(500) | 文件存储路径 |
| file_type | String(50) | 文件类型 |
| file_size | BigInteger | 文件大小 |
| ragflow_dataset_id | String(100) | RAGFlow 数据集ID |
| ragflow_document_id | String(100) | RAGFlow 文档ID |
| parse_status | String(50) | 解析状态 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

---

## API 接口

### 认证接口
- `POST /api/v1/login/register` - 用户注册
- `POST /api/v1/login/login` - 用户登录

### 文档接口
- `GET /api/v1/documents/` - 获取文档列表
- `POST /api/v1/documents/` - 创建文档
- `POST /api/v1/documents/upload` - 上传文档
- `GET /api/v1/documents/{id}` - 获取文档详情
- `PUT /api/v1/documents/{id}` - 更新文档
- `DELETE /api/v1/documents/{id}` - 删除文档
- `POST /api/v1/documents/{id}/reparse` - 重新解析文档
- `GET /api/v1/documents/{id}/parse-status` - 获取解析状态

### 用户管理接口（管理员）
- `GET /api/v1/users/` - 获取用户列表
- `POST /api/v1/users/` - 创建用户
- `GET /api/v1/users/{id}` - 获取用户详情
- `PUT /api/v1/users/{id}` - 更新用户
- `DELETE /api/v1/users/{id}` - 删除用户
- `PUT /api/v1/users/{id}/toggle-active` - 切换用户状态
- `PUT /api/v1/users/{id}/assign-role` - 分配角色

### 角色管理接口（管理员）
- `GET /api/v1/roles/` - 获取角色列表
- `POST /api/v1/roles/` - 创建角色
- `GET /api/v1/roles/{id}` - 获取角色详情
- `PUT /api/v1/roles/{id}` - 更新角色
- `DELETE /api/v1/roles/{id}` - 删除角色

---

## 部署说明

### 环境要求
- Docker
- Docker Compose

### 启动命令
```bash
docker-compose up --build -d
```

### 访问地址
- 前端：http://localhost:5173
- 后端 API：http://localhost:8000
- RAGFlow：http://localhost:9380

### 默认管理员账号
- 用户名：admin
- 密码：admin123

---

## 总结

本项目在开发过程中遇到了多个技术问题，主要包括：

1. **依赖版本兼容性问题** - bcrypt 版本与 passlib 不兼容
2. **数据库初始化问题** - 需要手动创建初始化脚本
3. **前端绑定问题** - Vue 中布尔值绑定的陷阱
4. **ORM 映射问题** - SQLAlchemy 模型加载顺序
5. **Shell 语法差异** - PowerShell 与 Bash 的语法差异

通过这些问题的解决，项目的稳定性和可用性得到了提升。