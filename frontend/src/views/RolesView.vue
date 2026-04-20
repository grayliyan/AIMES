<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import axios from 'axios'

const router = useRouter()
const userStore = useUserStore()
const user = ref(userStore.user)

const API_URL = 'http://localhost:8000/api/v1'

const roles = ref([])
const showModal = ref(false)
const isEditing = ref(false)
const loading = ref(false)
const error = ref('')

const formData = ref({
  id: null,
  name: '',
  description: '',
  permissions: '',
  is_active: true
})

const permissionOptions = [
  { value: 'user_manage', label: '用户管理' },
  { value: 'role_manage', label: '角色管理' },
  { value: 'document_manage', label: '文档管理' },
  { value: 'qa_access', label: '智能问答' },
  { value: 'ragflow_access', label: 'RAGFlow访问' }
]

const selectedPermissions = ref([])

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
  fetchRoles()
})

const handleLogout = () => {
  userStore.logout()
  router.push('/')
}

const openCreateModal = () => {
  isEditing.value = false
  formData.value = { id: null, name: '', description: '', permissions: '', is_active: true }
  selectedPermissions.value = []
  error.value = ''
  showModal.value = true
}

const openEditModal = (role) => {
  isEditing.value = true
  formData.value = { ...role }
  selectedPermissions.value = role.permissions ? role.permissions.split(',') : []
  error.value = ''
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  formData.value = { id: null, name: '', description: '', permissions: '', is_active: true }
  selectedPermissions.value = []
  error.value = ''
}

const submitForm = async () => {
  if (!formData.value.name) {
    error.value = '请输入角色名称'
    return
  }

  loading.value = true
  error.value = ''

  const submitData = {
    ...formData.value,
    permissions: selectedPermissions.value.join(',')
  }

  try {
    if (isEditing.value) {
      const response = await axios.put(`${API_URL}/roles/${formData.value.id}`, submitData)
      const index = roles.value.findIndex(r => r.id === formData.value.id)
      if (index !== -1) {
        roles.value[index] = response.data
      }
    } else {
      const response = await axios.post(`${API_URL}/roles/`, submitData)
      roles.value.unshift(response.data)
    }
    closeModal()
  } catch (err) {
    error.value = err.response?.data?.detail || '操作失败'
  } finally {
    loading.value = false
  }
}

const deleteRole = async (id) => {
  if (!confirm('确定要删除这个角色吗？')) return
  
  try {
    await axios.delete(`${API_URL}/roles/${id}`)
    roles.value = roles.value.filter(r => r.id !== id)
  } catch (err) {
    alert('删除角色失败')
  }
}

const getPermissionLabel = (permission) => {
  const option = permissionOptions.find(p => p.value === permission)
  return option ? option.label : permission
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
        <router-link to="/users" class="nav-link">用户管理</router-link>
        <router-link to="/roles" class="nav-link active">角色管理</router-link>
      </nav>
      <div class="user-info">
        <span class="username">{{ user?.full_name || user?.username }}</span>
        <button @click="handleLogout" class="btn-logout">退出登录</button>
      </div>
    </header>

    <main class="page-main">
      <div class="page-title">
        <h2>角色管理</h2>
        <p>管理系统角色和权限</p>
      </div>

      <div class="toolbar">
        <button @click="openCreateModal" class="btn-create">➕ 新建角色</button>
      </div>

      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>角色名称</th>
              <th>描述</th>
              <th>权限</th>
              <th>状态</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="role in roles" :key="role.id">
              <td>{{ role.id }}</td>
              <td>{{ role.name }}</td>
              <td>{{ role.description || '-' }}</td>
              <td>
                <div class="permission-tags">
                  <span 
                    v-for="perm in (role.permissions || '').split(',').filter(p => p)" 
                    :key="perm" 
                    class="permission-tag"
                  >
                    {{ getPermissionLabel(perm) }}
                  </span>
                  <span v-if="!role.permissions" class="no-permission">无权限</span>
                </div>
              </td>
              <td>
                <span :class="['status-badge', role.is_active ? 'active' : 'inactive']">
                  {{ role.is_active ? '启用' : '禁用' }}
                </span>
              </td>
              <td>{{ formatDate(role.created_at) }}</td>
              <td>
                <div class="action-buttons">
                  <button class="btn-edit" @click="openEditModal(role)">编辑</button>
                  <button class="btn-delete" @click="deleteRole(role.id)">删除</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- 角色编辑弹窗 -->
    <div class="modal-overlay" v-if="showModal" @click="closeModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>{{ isEditing ? '编辑角色' : '新建角色' }}</h3>
          <button class="btn-close" @click="closeModal">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="error" class="error-message">{{ error }}</div>
          <div class="form-group">
            <label>角色名称 <span class="required">*</span></label>
            <input v-model="formData.name" type="text" placeholder="请输入角色名称" />
          </div>
          <div class="form-group">
            <label>描述</label>
            <input v-model="formData.description" type="text" placeholder="请输入角色描述" />
          </div>
          <div class="form-group">
            <label>权限</label>
            <div class="checkbox-group">
              <label v-for="option in permissionOptions" :key="option.value" class="checkbox-label">
                <input 
                  type="checkbox" 
                  :value="option.value" 
                  v-model="selectedPermissions"
                />
                <span>{{ option.label }}</span>
              </label>
            </div>
          </div>
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.is_active" />
              <span>启用</span>
            </label>
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
  max-width: 1200px;
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
  overflow: hidden;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
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

.permission-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.permission-tag {
  background: #e6f7ff;
  color: #1890ff;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

.no-permission {
  color: #999;
  font-size: 0.85rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.status-badge.active {
  background: #f6ffed;
  color: #52c41a;
}

.status-badge.inactive {
  background: #fff2f0;
  color: #ff4d4f;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-edit, .btn-delete {
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

.btn-delete {
  background: #fff2f0;
  color: #ff4d4f;
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

.form-group input[type="text"] {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e1e5eb;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group input[type="text"]:focus {
  outline: none;
  border-color: #667eea;
}

.checkbox-group {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
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