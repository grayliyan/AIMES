# AIMES 项目 Docker 部署全记录

> 日期：2026-04-18
> 项目路径：E:\AIMES
> 技术栈：Vue3 + Vite (前端) · FastAPI (后端) · PostgreSQL 15 · RAGFlow
> 部署方式：Docker Compose

---

## 一、项目概述

AIMES 是一个 RAG 知识库系统，前后端分离架构：

| 组件 | 技术栈 | 容器端口 | 宿主机端口 |
|------|--------|---------|-----------|
| Frontend | Vue3 + Vite | 5173 | 5173 |
| Backend | FastAPI + Uvicorn | 8000 | 8000 |
| PostgreSQL | 15 | 5432 | 5432 |
| MySQL | 8.0 | 3306 | 3306 |
| Redis | 7 | 6379 | 6379 |
| Elasticsearch | 8.11.3 | 9200 | 9200 |
| MinIO | Latest | 9000/9001 | 9000/9001 |
| RAGFlow | v0.24.0 | 80 (nginx) → 9380 (API) | 9380 |

---

## 二、部署步骤

### 2.1 前置条件

- Docker Desktop 已安装（需手动启动，否则 `docker compose up` 报 pipe 错误）
- OpenCode v1.4.11（用于执行编码任务）

### 2.2 构建前端镜像（首次失败 → 修复）

**问题**：Dockerfile 使用 `npm ci`，但 `E:\AIMES\frontend` 目录缺少 `package-lock.json`。

**解决**：

```bash
cd E:\AIMES\frontend
npm install
```

生成 `package-lock.json` 后重新 `docker compose build`，前端镜像 `aimes-frontend` 构建成功。

### 2.3 构建后端镜像

```bash
docker compose build backend
```

后端镜像 `aimes-backend` 构建成功。

### 2.4 首次启动

```bash
docker compose up -d
```

**问题**：Docker Hub 限速（`请求过于频繁，请稍后再试`）。

**解决**：等待后重试，PostgreSQL 镜像（~1.3GB）下载耗时较长。

---

## 三、遇到的问题与解决方案

### 3.1 前端无法从宿主机访问（ERR_EMPTY_RESPONSE）

**现象**：`localhost:5173` 无法访问，`curl.exe` 返回空响应。

**根因**：Vite dev server 默认只监听容器内 `localhost`（127.0.0.1），Docker 端口映射需要容器监听 `0.0.0.0`。

**解决**：修改 `E:\AIMES\frontend\vite.config.js`：

```diff
  server: {
+   host: true,   // 监听 0.0.0.0
    port: 5173,
    proxy: {
      '/api': 'http://backend:8000'
    }
  }
```

修复后 `curl.exe localhost:5173` 返回 200 OK。

### 3.2 PowerShell 的 `curl` 是 `Invoke-WebRequest` 的别名

**现象**：`curl localhost:5173` 返回的对象格式与 `curl.exe` 不同，容易混淆。

**解决**：使用完整路径 `C:\Windows\System32\curl.exe` 或通过 `.bat` 脚本调用。

### 3.3 RAGFlow 数据库连接失败

**现象**：RAGFlow 日志报错 `Access denied for user 'ragflow'@'%' to database 'rag_flow'`。

**根因**：`docker-compose.yml` 中 MySQL 的 `MYSQL_DATABASE` 配置为 `ragflow`，但 RAGFlow 要求数据库名为 `rag_flow`（下划线）。

**解决**：

```diff
  mysql:
    environment:
-     MYSQL_DATABASE: ragflow
+     MYSQL_DATABASE: rag_flow
```

同时需要清除旧的 MySQL volume（`docker compose down -v`），否则旧数据库不会被重建。

### 3.4 RAGFlow 依赖缺失（Redis / ES / MinIO）

**现象**：RAGFlow 启动后日志持续报错缺少依赖服务。

**排查过程**：
1. 首次启动 → 缺少 Redis → 添加 Redis 服务
2. 重启 → 缺少 Elasticsearch → 添加 ES 服务
3. 重启 → 缺少 MinIO → 添加 MinIO 服务

**最终 `docker-compose.yml` 中的 RAGFlow 完整依赖栈**：

```yaml
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: infini_rag_flow
      MYSQL_DATABASE: rag_flow
      MYSQL_USER: ragflow
      MYSQL_PASSWORD: infini_rag_flow

  redis:
    image: redis:7
    command: redis-server --requirepass infini_rag_flow

  es01:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.3
    environment:
      - discovery.type=single-node
      - ELASTIC_PASSWORD=infini_rag_flow
      - xpack.security.enabled=true
      - xpack.security.http.ssl.enabled=false

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: rag_flow
      MINIO_ROOT_PASSWORD: infini_rag_flow

  ragflow:
    image: infiniflow/ragflow:latest
    depends_on:
      mysql: { condition: service_healthy }
      redis: { condition: service_healthy }
      es01: { condition: service_healthy }
      minio: { condition: service_healthy }
    ports:
      - "9380:80"   # 注意：容器内是 nginx:80，不是 9380
```

### 3.5 RAGFlow 端口映射错误（核心问题）

**现象**：所有容器运行正常，RAGFlow 日志无报错，但 `localhost:9380` 返回 `ERR_EMPTY_RESPONSE`。

**排查过程**：
1. `docker top` 确认所有进程在跑（nginx、ragflow_server.py、sync_data_source.py、task_executor.py）
2. 容器内 `curl localhost:9380` → Connection refused
3. 检查 nginx 配置 `/etc/nginx/conf.d/ragflow.conf`：

```nginx
server {
    listen 80;                    # ← nginx 监听的是 80，不是 9380！
    server_name _;
    root /ragflow/web/dist;

    location ~ ^/(v1|api) {
        proxy_pass http://localhost:9380;   # ← 代理到 RAGFlow server
    }
    location / {
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

**根因**：RAGFlow 容器内的 nginx 监听 **80 端口**（提供前端静态文件 + API 反向代理），而 `docker-compose.yml` 端口映射写的是 `9380:9380`，导致宿主机 9380 端口映射到了容器内无人监听的 9380 端口。

**解决**：

```diff
  ragflow:
    ports:
-     - "9380:9380"
+     - "9380:80"
```

修改后重启容器，`curl localhost:9380` 返回 200 OK，RAGFlow 页面正常访问。

### 3.6 Redis 连接警告

**现象**：RAGFlow 日志中有 `Realtime synonym is disabled, since no redis connection.`

**状态**：Redis 服务本身正常运行（`Ready to accept connections`），RAGFlow 的 `service_conf.yaml` 中 Redis 配置为 `host: redis:6379`。此警告可能是因为 ragflow_server.py 在完全初始化前尝试连接 Redis 失败，属于启动时序问题，不影响核心功能。

---

## 四、最终运行状态

```
容器名称              状态          端口映射
aimes-frontend-1      Running       5173:5173
aimes-backend-1       Running       8000:8000
aimes-postgres-1      Healthy       5432:5432
aimes-mysql-1         Healthy       3306:3306
aimes-redis-1         Healthy       6379:6379
es01                  Healthy       9200:9200
minio                 Healthy       9000:9000, 9001:9001
aimes-ragflow-1       Running       9380:80
```

访问地址：
- 前端：http://localhost:5173
- 后端 API：http://localhost:8000
- RAGFlow：http://localhost:9380
- MinIO 控制台：http://localhost:9001

---

## 五、经验总结

| 问题 | 教训 |
|------|------|
| `npm ci` 需要 lock 文件 | Docker 构建前确保 `package-lock.json` 存在 |
| Docker Hub 限速 | 遇到 `请求过于频繁` 等待后重试 |
| Vite 只监听 localhost | 容器内服务必须监听 `0.0.0.0` 才能被宿主机访问 |
| PowerShell `curl` 是别名 | 始终用 `curl.exe` 完整路径或 `.bat` 脚本 |
| MySQL 数据库名写错 | RAGFlow 要求 `rag_flow`（下划线），不是 `ragflow` |
| MySQL volume 脏数据 | 修改数据库配置后需 `docker compose down -v` 清除旧 volume |
| RAGFlow 依赖多 | 需要完整依赖栈：MySQL + Redis + ES + MinIO |
| **RAGFlow 端口映射** | **nginx 监听 80，映射必须是 `9380:80` 而非 `9380:9380`** |
| docker-compose.yml `version` 属性 | 已过时，会产生 warning 但不影响运行 |
