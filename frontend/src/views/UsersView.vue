<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import axios from 'axios'

const router = useRouter()
const userStore = useUserStore()
const user = ref(userStore.user)

const API_URL = 'http://localhost:8000/api/v1'

const users = ref([])
const roles = ref([])
const showModal = ref(false)
const isEditing = ref(false)
const loading = ref(false)
const error = ref('')

const formData = ref({
  id: null,
  username: '',
  email: '',
  password: '',
  full_name: '',
  is_active: true,
  is_superuser: false,
  role_id: null
})

const fetchUsers = async () => {
  try {
    const response = await axios.get(`${API_URL}/users/`)
    users.value = response.data
  } catch (err) {
    console.error('获取用户列表失败:', err)
  }
}

const fetchRoles = async () => {
  try {
    const response = await axios.get(`${API_URL}/roles/`)
    roles.value = response.data
  } catch (err) {
    console.error('获取角色列表失败:', err)
  }
}

onMounted(() => {
  if (!user.value?.is_superuser) {
    router.push('/dashboard')
    return
  }
  fetchUsers()
  fetchRoles()
})

const handleLogout = () => {
  userStore.logout()
  router.push('/')
}

const openCreateModal = () => {
  isEditing.value = false
  formData.value = {
    id: null,
    username: '',
    email: '',
    password: '',
    full_name: '',
    is_active: true,
    is_superuser: false,
    role_id: null
  }
  error.value = ''
  showModal.value = true
}

const openEditModal = (u) => {
  isEditing.value = true
  formData.value = {
    id: u.id,
    username: u.username,
    email: u.email,
    password: '',
    full_name: u.full_name || '',
    is_active: u.is_active,
    is_superuser: u.is_superuser,
    role_id: u.role_id
  }
  error.value = ''
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  formData.value = {
    id: null,
    username: '',
    email: '',
    password: '',
    full_name: '',
    is_active: true,
    is_superuser: false,
    role_id: null
  }
  error.value = ''
}

const submitForm = async () => {
  if (!formData.value.username || !formData.value.email) {
    error.value = '请填写用户名和邮箱'
    return
  }

  if (!isEditing.value && !formData.value.password) {
    error.value = '请填写密码'
    return
  }

  loading.value = true
  error.value = ''

  try {
    if (isEditing.value) {
      const updateData = {
        email: formData.value.email,
        full_name: formData.value.full_name,
        is_active: formData.value.is_active,
        is_superuser: formData.value.is_superuser,
        role_id: formData.value.role_id
      }
      if (formData.value.password) {
        updateData.password = formData.value.password
      }
      const response = await axios.put(`${API_URL}/users/${formData.value.id}`, updateData)
      const index = users.value.findIndex(u => u.id === formData.value.id)
      if (index !== -1) {
        users.value[index] = response.data
      }
    } else {
      const response = await axios.post(`${API_URL}/users/`, {
        username: formData.value.username,
        email: formData.value.email,
        password: formData.value.password,
        full_name: formData.value.full_name,
        is_active: formData.value.is_active,
        is_superuser: formData.value.is_superuser,
        role_id: formData.value.role_id
      })
      users.value.unshift(response.data)
    }
    closeModal()
  } catch (err) {
    error.value = err.response?.data?.detail || '操作失败'
  } finally {
    loading.value = false
  }
}

const deleteUser = async (id) => {
  if (!confirm('确定要删除这个用户吗？')) return
  
  try {
    await axios.delete(`${API_URL}/users/${id}`)
    users.value = users.value.filter(u => u.id !== id)
  } catch (err) {
    alert('删除用户失败')
  }
}

const toggleUserActive = async (id) => {
  try {
    const response = await axios.put(`${API_URL}/users/${id}/toggle-active`)
    const index = users.value.findIndex(u => u.id === id)
    if (index !== -1) {
      users.value[index] = response.data
    }
  } catch (err) {
    alert('操作失败')
  }
}

const getRoleName = (roleId) => {
  const role = roles.value.find(r => r.id === roleId)
  return role ? role.name : '未分配'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<template>
  <div class="management-page">
    <header class="page-header">
      <div class="logo">
        <span class="icon">📚</span>
        <h1>知识库系统</h1>
      </div>
      <nav class="nav-menu">
        <router-link to="/dashboard" class="nav-link">首页</router-link>
        <router-link to="/documents" class="nav-link">文档管理</router-link>
        <router-link to="/qa" class="nav-link">智能问答</router-link>
        <router-link to="/users" class="nav-link active">用户管理</router-link>
        <router-link to="/roles" class="nav-link">角色管理</router-link>
      </nav>
      <div class="user-info">
        <span class="username">{{ user?.full_name || user?.username }}</span>
        <button @click="handleLogout" class="btn-logout">退出登录</button>
      </div>
    </header>

    <main class="page-main">
      <div class="page-title">
        <h2>用户管理</h2>
        <p>管理系统用户账号</p>
      </div>

      <div class="toolbar">
        <button @click="openCreateModal" class="btn-create">➕ 新建用户</button>
      </div>

      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>用户名</th>
              <th>邮箱</th>
              <th>姓名</th>
              <th>角色</th>
              <th>状态</th>
              <th>管理员</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>{{ u.id }}</td>
              <td>{{ u.username }}</td>
              <td>{{ u.email }}</td>
              <td>{{ u.full_name || '-' }}</td>
              <td>{{ getRoleName(u.role_id) }}</td>
              <td>
                <span :class="['status-badge', u.is_active ? 'active' : 'inactive']">
                  {{ u.is_active ? '启用' : '禁用' }}
                </span>
              </td>
              <td>
                <span :class="['status-badge', u.is_superuser ? 'superuser' : 'normal']">
                  {{ u.is_superuser ? '是' : '否' }}
                </span>
              </td>
              <td>{{ formatDate(u.created_at) }}</td>
              <td>
                <div class="action-buttons">
                  <button class="btn-edit" @click="openEditModal(u)">编辑</button>
                  <button 
                    class="btn-toggle" 
                    :class="u.is_active ? 'deactivate' : 'activate'"
                    @click="toggleUserActive(u.id)"
                  >
                    {{ u.is_active ? '禁用' : '启用' }}
                  </button>
                  <button 
                    class="btn-delete" 
                    @click="deleteUser(u.id)"
                    :disabled="u.id === user?.id"
                  >
                    删除
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- 用户编辑弹窗 -->
    <div class="modal-overlay" v-if="showModal" @click="closeModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>{{ isEditing ? '编辑用户' : '新建用户' }}</h3>
          <button class="btn-close" @click="closeModal">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="error" class="error-message">{{ error }}</div>
          <div class="form-group">
            <label>用户名 <span class="required">*</span></label>
            <input 
              v-model="formData.username" 
              type="text" 
              placeholder="请输入用户名"
              :disabled="isEditing"
            />
          </div>
          <div class="form-group">
            <label>邮箱 <span class="required">*</span></label>
            <input v-model="formData.email" type="email" placeholder="请输入邮箱" />
          </div>
          <div class="form-group">
            <label>密码 {{ isEditing ? '' : '*' }}</label>
            <input 
              v-model="formData.password" 
              type="password" 
              :placeholder="isEditing ? '留空则不修改' : '请输入密码'" 
            />
          </div>
          <div class="form-group">
            <label>姓名</label>
            <input v-model="formData.full_name" type="text" placeholder="请输入姓名" />
          </div>
          <div class="form-group">
            <label>角色</label>
            <select v-model="formData.role_id">
              <option :value="null">未分配</option>
              <option v-for="role in roles" :key="role.id" :value="role.id">
                {{ role.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <div class="checkbox-row">
              <label class="checkbox-label">
                <input type="checkbox" v-model="formData.is_active" />
                <span>启用</span>
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="formData.is_superuser" />
                <span>管理员</span>
              </label>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeModal">取消</button>
          <button class="btn-submit" @click="submitForm" :disabled="loading">
            {{ loading ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.management-page {
  min-height: 100vh;
  background-color: #f5f7fa;
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
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-title {
  margin-bottom: 2rem;
}

.page-title h2 {
  color: #333;
  margin-bottom: 0.5rem;
}

.page-title p { color: #666; }

.toolbar {
  margin-bottom: 1.5rem;
}

.btn-create {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 900px;
}

.data-table th, .data-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

.data-table th {
  background: #fafafa;
  font-weight: 600;
  color: #333;
}

.data-table tr:hover {
  background: #fafafa;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.status-badge.active, .status-badge.activate {
  background: #f6ffed;
  color: #52c41a;
}

.status-badge.inactive, .status-badge.deactivate {
  background: #fff2f0;
  color: #ff4d4f;
}

.status-badge.superuser {
  background: #fff7e6;
  color: #fa8c16;
}

.status-badge.normal {
  background: #f5f5f5;
  color: #666;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-edit, .btn-delete, .btn-toggle {
  padding: 0.4rem 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
}

.btn-edit {
  background: #e6f7ff;
  color: #1890ff;
}

.btn-toggle.activate {
  background: #f6ffed;
  color: #52c41a;
}

.btn-toggle.deactivate {
  background: #fff7e6;
  color: #fa8c16;
}

.btn-delete {
  background: #fff2f0;
  color: #ff4d4f;
}

.btn-delete:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #f0f0f0;
}

.modal-header h3 { margin: 0; color: #333; }

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
}

.modal-body {
  padding: 1.5rem;
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

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
}

.required { color: #ff4d4f; }

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e1e5eb;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.form-group input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.checkbox-row {
  display: flex;
  gap: 2rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #f0f0f0;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  background: #f0f0f0;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-submit {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>