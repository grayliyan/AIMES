#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建数据库表
"""

from sqlalchemy import create_engine
from app.core.config import settings
from app.db.base_class import Base
from app.models.user import User  # 导入所有模型以确保它们被注册到Base中

def init_db():
    """初始化数据库，创建所有表"""
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功！")

if __name__ == "__main__":
    init_db()