<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const user = computed(() => userStore.user)

const handleLogout = () => {
  userStore.logout()
  router.push('/')
}
</script>

<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <div class="logo">
        <span class="icon">📚</span>
        <h1>知识库系统</h1>
      </div>
      <nav class="nav-menu">
        <router-link to="/dashboard" class="nav-link active">首页</router-link>
        <router-link to="/documents" class="nav-link">文档管理</router-link>
        <router-link to="/qa" class="nav-link">智能问答</router-link>
      </nav>
      <div class="user-info">
        <span class="username">{{ user?.full_name || user?.username }}</span>
        <button @click="handleLogout" class="btn-logout">退出登录</button>
      </div>
    </header>

    <main class="dashboard-main">
      <div class="welcome-section">
        <h2>欢迎回来，{{ user?.full_name || user?.username }}！</h2>
        <p>这是您的知识库管理面板</p>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">📄</div>
          <div class="stat-info">
            <h3>文档总数</h3>
            <p class="stat-number">0</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📁</div>
          <div class="stat-info">
            <h3>分类数量</h3>
            <p class="stat-number">0</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">💬</div>
          <div class="stat-info">
            <h3>问答次数</h3>
            <p class="stat-number">0</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">👥</div>
          <div class="stat-info">
            <h3>用户数量</h3>
            <p class="stat-number">1</p>
          </div>
        </div>
      </div>

      <div class="quick-actions">
        <h3>快速操作</h3>
        <div class="actions-grid">
          <router-link to="/documents" class="action-card">
            <span class="action-icon">➕</span>
            <span>新建文档</span>
          </router-link>
          <router-link to="/qa" class="action-card">
            <span class="action-icon">❓</span>
            <span>提问问题</span>
          </router-link>
          <router-link to="/documents" class="action-card">
            <span class="action-icon">🔍</span>
            <span>搜索文档</span>
          </router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.dashboard-header {
  background: white;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo .icon {
  font-size: 1.75rem;
}

.logo h1 {
  font-size: 1.25rem;
  color: #333;
  margin: 0;
}

.nav-menu {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  color: #666;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.nav-link:hover,
.nav-link.active {
  color: #667eea;
  background-color: rgba(102, 126, 234, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.username {
  color: #333;
  font-weight: 500;
}

.btn-logout {
  padding: 0.5rem 1rem;
  background: #ff4d4f;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-logout:hover {
  background: #ff7875;
}

.dashboard-main {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  margin-bottom: 2rem;
}

.welcome-section h2 {
  color: #333;
  margin-bottom: 0.5rem;
}

.welcome-section p {
  color: #666;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-icon {
  font-size: 2.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-info h3 {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.quick-actions h3 {
  color: #333;
  margin-bottom: 1rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: #333;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
}

.action-icon {
  font-size: 2rem;
}

.action-card span:last-child {
  font-weight: 500;
}
</style>
