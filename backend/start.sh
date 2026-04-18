#!/bin/bash

# 等待数据库启动
echo "等待数据库启动..."
sleep 5

# 初始化数据库
echo "初始化数据库..."
python init_db.py

# 启动FastAPI应用
echo "启动FastAPI应用..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload