<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()
const user = ref(userStore.user)

const question = ref('')
const answer = ref('')
const loading = ref(false)
const chatHistory = ref([])

const handleLogout = () => {
  userStore.logout()
  router.push('/')
}

const handleAsk = async () => {
  if (!question.value.trim()) return

  const currentQuestion = question.value
  question.value = ''
  loading.value = true

  chatHistory.value.push({
    type: 'question',
    content: currentQuestion
  })

  // 模拟问答响应
  setTimeout(() => {
    chatHistory.value.push({
      type: 'answer',
      content: '这是智能问答的示例回复。RAGFlow集成后，将根据知识库内容提供精准回答。'
    })
    loading.value = false
  }, 1500)
}
</script>

<template>
  <div class="qa-page">
    <header class="page-header">
      <div class="logo">
        <span class="icon">📚</span>
        <h1>知识库系统</h1>
      </div>
      <nav class="nav-menu">
        <router-link to="/dashboard" class="nav-link">首页</router-link>
        <router-link to="/documents" class="nav-link">文档管理</router-link>
        <router-link to="/qa" class="nav-link active">智能问答</router-link>
      </nav>
      <div class="user-info">
        <span class="username">{{ user?.full_name || user?.username }}</span>
        <button @click="handleLogout" class="btn-logout">退出登录</button>
      </div>
    </header>

    <main class="page-main">
      <div class="page-title">
        <h2>智能问答</h2>
        <p>基于RAG技术的智能问答，精准回答您的问题</p>
      </div>

      <div class="chat-container">
        <div class="chat-messages">
          <div class="welcome-message" v-if="chatHistory.length === 0">
            <span class="welcome-icon">🤖</span>
            <h3>您好！我是知识库智能助手</h3>
            <p>请向我提问，我会根据知识库内容为您解答</p>
          </div>

          <div 
            v-for="(msg, index) in chatHistory" 
            :key="index"
            :class="['message', msg.type]"
          >
            <div class="message-avatar">
              {{ msg.type === 'question' ? '👤' : '🤖' }}
            </div>
            <div class="message-content">
              {{ msg.content }}
            </div>
          </div>

          <div class="message answer" v-if="loading">
            <div class="message-avatar">🤖</div>
            <div class="message-content typing">
              <span class="dot"></span>
              <span class="dot"></span>
              <span class="dot"></span>
            </div>
          </div>
        </div>

        <div class="chat-input">
          <input 
            v-model="question"
            type="text" 
            placeholder="请输入您的问题..."
            @keyup.enter="handleAsk"
            :disabled="loading"
          />
          <button @click="handleAsk" :disabled="loading || !question.trim()">
            {{ loading ? '思考中...' : '发送' }}
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.qa-page {
  min-height: 100vh;
  background-color: #f5f7fa;
  display: flex;
  flex-direction: column;
}

.page-header {
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

.logo .icon { font-size: 1.75rem; }
.logo h1 { font-size: 1.25rem; color: #333; margin: 0; }

.nav-menu { display: flex; gap: 1.5rem; }

.nav-link {
  color: #666;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.nav-link:hover, .nav-link.active {
  color: #667eea;
  background-color: rgba(102, 126, 234, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.username { color: #333; font-weight: 500; }

.btn-logout {
  padding: 0.5rem 1rem;
  background: #ff4d4f;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.page-main {
  flex: 1;
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.page-title {
  margin-bottom: 1.5rem;
  text-align: center;
}

.page-title h2 {
  color: #333;
  margin-bottom: 0.5rem;
}

.page-title p { color: #666; }

.chat-container {
  flex: 1;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  min-height: 400px;
}

.welcome-message {
  text-align: center;
  padding: 3rem 1rem;
  color: #666;
}

.welcome-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: 1rem;
}

.welcome-message h3 {
  color: #333;
  margin-bottom: 0.5rem;
}

.message {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.message.question {
  flex-direction: row-reverse;
}

.message-avatar {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 50%;
  flex-shrink: 0;
}

.message-content {
  max-width: 70%;
  padding: 1rem 1.25rem;
  border-radius: 12px;
  line-height: 1.6;
}

.message.question .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.answer .message-content {
  background: #f5f5f5;
  color: #333;
  border-bottom-left-radius: 4px;
}

.typing {
  display: flex;
  gap: 4px;
  padding: 1rem 1.5rem;
}

.dot {
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.dot:nth-child(1) { animation-delay: 0s; }
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); }
  40% { transform: scale(1); }
}

.chat-input {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #f0f0f0;
  background: white;
}

.chat-input input {
  flex: 1;
  padding: 1rem 1.25rem;
  border: 2px solid #e1e5eb;
  border-radius: 12px;
  font-size: 1rem;
}

.chat-input input:focus {
  outline: none;
  border-color: #667eea;
}

.chat-input button {
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 500;
}

.chat-input button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
