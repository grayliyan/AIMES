<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const formData = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  full_name: ''
})
const error = ref('')
const success = ref('')
const loading = ref(false)

const handleRegister = async () => {
  error.value = ''
  success.value = ''

  if (!formData.value.username || !formData.value.email || !formData.value.password) {
    error.value = '请填写所有必填字段'
    return
  }

  if (formData.value.password !== formData.value.confirmPassword) {
    error.value = '两次输入的密码不一致'
    return
  }

  if (formData.value.password.length < 6) {
    error.value = '密码长度至少为6位'
    return
  }

  loading.value = true

  const result = await userStore.register({
    username: formData.value.username,
    email: formData.value.email,
    password: formData.value.password,
    full_name: formData.value.full_name || null
  })

  if (result.success) {
    success.value = '注册成功！即将跳转到登录页面...'
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } else {
    error.value = result.message
  }

  loading.value = false
}

const goToLogin = () => {
  router.push('/login')
}

const goHome = () => {
  router.push('/')
}
</script>

<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h1>用户注册</h1>
        <p>创建您的知识库账号</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="username">用户名 <span class="required">*</span></label>
          <input
            id="username"
            v-model="formData.username"
            type="text"
            placeholder="请输入用户名"
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="email">邮箱 <span class="required">*</span></label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            placeholder="请输入邮箱地址"
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="full_name">姓名</label>
          <input
            id="full_name"
            v-model="formData.full_name"
            type="text"
            placeholder="请输入姓名（选填）"
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="password">密码 <span class="required">*</span></label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            placeholder="请输入密码（至少6位）"
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="confirmPassword">确认密码 <span class="required">*</span></label>
          <input
            id="confirmPassword"
            v-model="formData.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            :disabled="loading"
          />
        </div>

        <div v-if="success" class="success-message">
          {{ success }}
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" class="btn-register" :disabled="loading || success">
          {{ loading ? '注册中...' : '注 册' }}
        </button>
      </form>

      <div class="register-footer">
        <p>已有账号？<a href="#" @click.prevent="goToLogin">立即登录</a></p>
        <p><a href="#" @click.prevent="goHome">返回首页</a></p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.register-card {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.register-header h1 {
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 1.75rem;
}

.register-header p {
  color: #666;
  font-size: 0.95rem;
}

.register-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
  font-size: 0.95rem;
}

.required {
  color: #ff4d4f;
}

.form-group input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e1e5eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.form-group input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.success-message {
  background-color: #f6ffed;
  border: 1px solid #b7eb8f;
  color: #52c41a;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.error-message {
  background-color: #fff2f0;
  border: 1px solid #ffccc7;
  color: #ff4d4f;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.btn-register {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-register:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-register:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-footer {
  text-align: center;
  color: #666;
  font-size: 0.9rem;
}

.register-footer p {
  margin: 0.5rem 0;
}

.register-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.register-footer a:hover {
  text-decoration: underline;
}
</style>
