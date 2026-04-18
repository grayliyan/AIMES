<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const message = ref('知识库系统')

const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<template>
  <div class="home">
    <div class="hero">
      <h1>{{ message }}</h1>
      <p class="subtitle">企业内部知识管理与智能问答平台</p>
      <div class="features">
        <div class="feature">
          <span class="icon">📚</span>
          <h3>文档管理</h3>
          <p>轻松创建、编辑和组织您的知识文档</p>
        </div>
        <div class="feature">
          <span class="icon">🔍</span>
          <h3>全文搜索</h3>
          <p>快速查找所需信息，提高工作效率</p>
        </div>
        <div class="feature">
          <span class="icon">🤖</span>
          <h3>智能问答</h3>
          <p>基于RAG技术的智能问答，精准回答您的问题</p>
        </div>
      </div>
      <div class="actions">
        <button class="btn-primary" @click="goToLogin">登录</button>
        <button class="btn-secondary" @click="goToRegister">注册</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.hero {
  max-width: 900px;
  text-align: center;
  color: white;
}

h1 {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 3rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.feature {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 1.5rem;
  transition: transform 0.3s ease;
}

.feature:hover {
  transform: translateY(-5px);
}

.feature .icon {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 1rem;
}

.feature h3 {
  margin-bottom: 0.5rem;
  font-size: 1.25rem;
}

.feature p {
  opacity: 0.9;
  font-size: 0.95rem;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn-primary,
.btn-secondary {
  padding: 0.875rem 2rem;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  border: none;
}

.btn-primary {
  background: white;
  color: #667eea;
}

.btn-primary:hover {
  background: #f0f0f0;
  transform: scale(1.05);
}

.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: scale(1.05);
}
</style>
