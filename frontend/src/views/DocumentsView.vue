<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import axios from 'axios'

const router = useRouter()
const userStore = useUserStore()
const user = ref(userStore.user)

const API_URL = 'http://localhost:8000/api/v1'

const documents = ref([])
const searchQuery = ref('')
const showCreateModal = ref(false)
const showUploadModal = ref(false)
const loading = ref(false)
const error = ref('')

const newDoc = ref({
  title: '',
  content: '',
  category: '',
  tags: ''
})

const uploadForm = ref({
  title: '',
  category: '',
  tags: '',
  file: null
})
const selectedFileName = ref('')

const showEditModal = ref(false)
const editingDoc = ref({
  id: null,
  title: '',
  content: '',
  category: '',
  tags: ''
})

// 获取文档列表
const fetchDocuments = async () => {
  try {
    const response = await axios.get(`${API_URL}/documents/`)
    documents.value = response.data
  } catch (err) {
    console.error('获取文档列表失败:', err)
  }
}

onMounted(() => {
  fetchDocuments()
})

const handleLogout = () => {
  userStore.logout()
  router.push('/')
}

const handleSearch = () => {
  console.log('搜索:', searchQuery.value)
}

const handleCreateDoc = () => {
  showCreateModal.value = true
}

const handleUploadDoc = () => {
  showUploadModal.value = true
}

const closeModal = () => {
  showCreateModal.value = false
  newDoc.value = { title: '', content: '', category: '', tags: '' }
}

const closeUploadModal = () => {
  showUploadModal.value = false
  uploadForm.value = { title: '', category: '', tags: '', file: null }
  selectedFileName.value = ''
  error.value = ''
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    uploadForm.value.file = file
    selectedFileName.value = file.name
    // 如果没有填写标题，使用文件名作为标题
    if (!uploadForm.value.title) {
      uploadForm.value.title = file.name.replace(/\.[^/.]+$/, '')
    }
  }
}

const submitDoc = async () => {
  if (!newDoc.value.title || !newDoc.value.content) {
    error.value = '请填写标题和内容'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const response = await axios.post(`${API_URL}/documents/`, {
      title: newDoc.value.title,
      content: newDoc.value.content,
      category: newDoc.value.category || null,
      tags: newDoc.value.tags || null
    })
    documents.value.unshift(response.data)
    closeModal()
  } catch (err) {
    error.value = err.response?.data?.detail || '创建文档失败'
  } finally {
    loading.value = false
  }
}

const submitUpload = async () => {
  if (!uploadForm.value.file) {
    error.value = '请选择文件'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const formData = new FormData()
    formData.append('file', uploadForm.value.file)
    if (uploadForm.value.title) {
      formData.append('title', uploadForm.value.title)
    }
    if (uploadForm.value.category) {
      formData.append('category', uploadForm.value.category)
    }
    if (uploadForm.value.tags) {
      formData.append('tags', uploadForm.value.tags)
    }

    const response = await axios.post(`${API_URL}/documents/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    documents.value.unshift(response.data)
    closeUploadModal()
  } catch (err) {
    error.value = err.response?.data?.detail || '上传文档失败'
  } finally {
    loading.value = false
  }
}

const deleteDocument = async (id) => {
  if (!confirm('确定要删除这个文档吗？')) return
  
  try {
    await axios.delete(`${API_URL}/documents/${id}`)
    documents.value = documents.value.filter(doc => doc.id !== id)
  } catch (err) {
    alert('删除文档失败')
  }
}

const openEditModal = (doc) => {
  editingDoc.value = {
    id: doc.id,
    title: doc.title,
    content: doc.content || '',
    category: doc.category || '',
    tags: doc.tags || ''
  }
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  editingDoc.value = { id: null, title: '', content: '', category: '', tags: '' }
  error.value = ''
}

const submitEdit = async () => {
  if (!editingDoc.value.title) {
    error.value = '请填写标题'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const response = await axios.put(`${API_URL}/documents/${editingDoc.value.id}`, {
      title: editingDoc.value.title,
      content: editingDoc.value.content,
      category: editingDoc.value.category || null,
      tags: editingDoc.value.tags || null
    })
    const index = documents.value.findIndex(doc => doc.id === editingDoc.value.id)
    if (index !== -1) {
      documents.value[index] = response.data
    }
    closeEditModal()
  } catch (err) {
    error.value = err.response?.data?.detail || '更新文档失败'
  } finally {
    loading.value = false
  }
}

const formatFileSize = (bytes) => {
  if (!bytes) return ''
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
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

const getFileIcon = (fileType) => {
  const icons = {
    'txt': '📄',
    'md': '📝',
    'pdf': '📕',
    'doc': '📘',
    'docx': '📘'
  }
  return icons[fileType] || '📄'
}

const getParseStatusText = (status) => {
  const statusMap = {
    'pending': '待解析',
    'parsing': '解析中',
    'completed': '已解析',
    'failed': '解析失败'
  }
  return statusMap[status] || status
}

const getParseStatusClass = (status) => {
  const classMap = {
    'pending': 'status-pending',
    'parsing': 'status-parsing',
    'completed': 'status-completed',
    'failed': 'status-failed'
  }
  return classMap[status] || ''
}

const reparseDocument = async (id) => {
  try {
    const response = await axios.post(`${API_URL}/documents/${id}/reparse`)
    const index = documents.value.findIndex(doc => doc.id === id)
    if (index !== -1) {
      documents.value[index] = response.data
    }
  } catch (err) {
    alert('重新解析失败')
  }
}

// 轮询检查解析状态
const checkParseStatus = async () => {
  const parsingDocs = documents.value.filter(doc => doc.parse_status === 'parsing' || doc.parse_status === 'pending')
  for (const doc of parsingDocs) {
    try {
      const response = await axios.get(`${API_URL}/documents/${doc.id}/parse-status`)
      const index = documents.value.findIndex(d => d.id === doc.id)
      if (index !== -1 && documents.value[index].parse_status !== response.data.parse_status) {
        documents.value[index].parse_status = response.data.parse_status
        documents.value[index].ragflow_dataset_id = response.data.ragflow_dataset_id
        documents.value[index].ragflow_document_id = response.data.ragflow_document_id
      }
    } catch (err) {
      console.error('检查解析状态失败:', err)
    }
  }
}

onMounted(() => {
  fetchDocuments()
  // 每5秒检查一次解析状态
  setInterval(checkParseStatus, 5000)
})
</script>

<template>
  <div class="documents-page">
    <header class="page-header">
      <div class="logo">
        <span class="icon">📚</span>
        <h1>知识库系统</h1>
      </div>
      <nav class="nav-menu">
        <router-link to="/dashboard" class="nav-link">首页</router-link>
        <router-link to="/documents" class="nav-link active">文档管理</router-link>
        <router-link to="/qa" class="nav-link">智能问答</router-link>
        <template v-if="user?.is_superuser">
          <router-link to="/users" class="nav-link">用户管理</router-link>
          <router-link to="/roles" class="nav-link">角色管理</router-link>
        </template>
      </nav>
      <div class="user-info">
        <span class="username">{{ user?.full_name || user?.username }}</span>
        <button @click="handleLogout" class="btn-logout">退出登录</button>
      </div>
    </header>

    <main class="page-main">
      <div class="page-title">
        <h2>文档管理</h2>
        <p>管理和组织您的知识文档</p>
      </div>

      <div class="toolbar">
        <div class="search-box">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="搜索文档..." 
            @keyup.enter="handleSearch"
          />
          <button @click="handleSearch" class="btn-search">🔍 搜索</button>
        </div>
        <div class="action-buttons">
          <a v-if="user?.is_superuser" href="http://localhost:9380" target="_blank" class="btn-ragflow">🔧 RAGFlow管理</a>
          <button @click="handleUploadDoc" class="btn-upload">📤 上传文档</button>
          <button @click="handleCreateDoc" class="btn-create">➕ 新建文档</button>
        </div>
      </div>

      <div class="documents-list">
        <div class="doc-card" v-for="doc in documents" :key="doc.id">
          <div class="doc-header">
            <div class="doc-title-wrapper">
              <span v-if="doc.file_type" class="file-icon">{{ getFileIcon(doc.file_type) }}</span>
              <h3>{{ doc.title }}</h3>
            </div>
            <span class="doc-category">{{ doc.category || '未分类' }}</span>
          </div>
          <div class="doc-info" v-if="doc.file_name">
            <span class="file-info">{{ doc.file_name }} ({{ formatFileSize(doc.file_size) }})</span>
            <span v-if="doc.parse_status" :class="['parse-status', getParseStatusClass(doc.parse_status)]">
              {{ getParseStatusText(doc.parse_status) }}
              <button 
                v-if="doc.parse_status === 'failed'" 
                class="btn-reparse" 
                @click.stop="reparseDocument(doc.id)"
              >
                重试
              </button>
            </span>
          </div>
          <div class="doc-tags" v-if="doc.tags">
            <span class="tag" v-for="tag in doc.tags.split(',')" :key="tag">{{ tag }}</span>
          </div>
          <div class="doc-footer">
            <span class="doc-date">{{ formatDate(doc.created_at) }}</span>
            <div class="doc-actions">
              <button class="btn-parse" v-if="doc.file_name" @click="reparseDocument(doc.id)" :disabled="doc.parse_status === 'parsing'">
                {{ doc.parse_status === 'parsing' ? '解析中...' : '解析' }}
              </button>
              <button class="btn-edit" @click="openEditModal(doc)">编辑</button>
              <button class="btn-delete" @click="deleteDocument(doc.id)">删除</button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 创建文档弹窗 -->
    <div class="modal-overlay" v-if="showCreateModal" @click="closeModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>新建文档</h3>
          <button class="btn-close" @click="closeModal">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="error" class="error-message">{{ error }}</div>
          <div class="form-group">
            <label>标题 <span class="required">*</span></label>
            <input v-model="newDoc.title" type="text" placeholder="请输入文档标题" />
          </div>
          <div class="form-group">
            <label>分类</label>
            <input v-model="newDoc.category" type="text" placeholder="请输入分类" />
          </div>
          <div class="form-group">
            <label>标签</label>
            <input v-model="newDoc.tags" type="text" placeholder="多个标签用逗号分隔" />
          </div>
          <div class="form-group">
            <label>内容 <span class="required">*</span></label>
            <textarea v-model="newDoc.content" rows="6" placeholder="请输入文档内容"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeModal">取消</button>
          <button class="btn-submit" @click="submitDoc" :disabled="loading">
            {{ loading ? '创建中...' : '创建' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 上传文档弹窗 -->
    <div class="modal-overlay" v-if="showUploadModal" @click="closeUploadModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>上传文档</h3>
          <button class="btn-close" @click="closeUploadModal">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="error" class="error-message">{{ error }}</div>
          <div class="form-group">
            <label>选择文件 <span class="required">*</span></label>
            <div class="file-upload-area">
              <input 
                type="file" 
                id="file-input"
                accept=".txt,.md,.pdf,.doc,.docx"
                @change="handleFileSelect"
                hidden
              />
              <label for="file-input" class="file-upload-label">
                <span class="upload-icon">📁</span>
                <span v-if="!selectedFileName">点击选择文件</span>
                <span v-else class="selected-file">{{ selectedFileName }}</span>
              </label>
            </div>
            <p class="file-hint">支持的格式: TXT, MD, PDF, DOC, DOCX</p>
          </div>
          <div class="form-group">
            <label>标题</label>
            <input v-model="uploadForm.title" type="text" placeholder="默认使用文件名" />
          </div>
          <div class="form-group">
            <label>分类</label>
            <input v-model="uploadForm.category" type="text" placeholder="请输入分类" />
          </div>
          <div class="form-group">
            <label>标签</label>
            <input v-model="uploadForm.tags" type="text" placeholder="多个标签用逗号分隔" />
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeUploadModal">取消</button>
          <button class="btn-submit" @click="submitUpload" :disabled="loading || !uploadForm.file">
            {{ loading ? '上传中...' : '上传' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 编辑文档弹窗 -->
    <div class="modal-overlay" v-if="showEditModal" @click="closeEditModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>编辑文档</h3>
          <button class="btn-close" @click="closeEditModal">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="error" class="error-message">{{ error }}</div>
          <div class="form-group">
            <label>标题 <span class="required">*</span></label>
            <input v-model="editingDoc.title" type="text" placeholder="请输入文档标题" />
          </div>
          <div class="form-group">
            <label>分类</label>
            <input v-model="editingDoc.category" type="text" placeholder="请输入分类" />
          </div>
          <div class="form-group">
            <label>标签</label>
            <input v-model="editingDoc.tags" type="text" placeholder="多个标签用逗号分隔" />
          </div>
          <div class="form-group">
            <label>内容</label>
            <textarea v-model="editingDoc.content" rows="6" placeholder="请输入文档内容"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeEditModal">取消</button>
          <button class="btn-submit" @click="submitEdit" :disabled="loading">
            {{ loading ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.documents-page {
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.search-box {
  display: flex;
  gap: 0.5rem;
  flex: 1;
  max-width: 500px;
}

.search-box input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e1e5eb;
  border-radius: 8px;
  font-size: 1rem;
}

.search-box input:focus {
  outline: none;
  border-color: #667eea;
}

.btn-search {
  padding: 0.75rem 1.5rem;
  background: #f0f0f0;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
}

.btn-upload {
  padding: 0.75rem 1.5rem;
  background: #52c41a;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.btn-upload:hover {
  background: #389e05;
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

.btn-ragflow {
  padding: 0.75rem 1.5rem;
  background: #722ed1;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
}

.btn-ragflow:hover {
  background: #531dab;
}

.documents-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.doc-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
}

.doc-card:hover {
  transform: translateY(-4px);
}

.doc-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.doc-title-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.file-icon {
  font-size: 1.25rem;
}

.doc-header h3 {
  color: #333;
  font-size: 1.1rem;
  margin: 0;
}

.doc-category {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.doc-info {
  margin-bottom: 0.75rem;
}

.file-info {
  color: #999;
  font-size: 0.85rem;
}

.parse-status {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  margin-left: 0.5rem;
}

.status-pending {
  background: #fff7e6;
  color: #fa8c16;
}

.status-parsing {
  background: #e6f7ff;
  color: #1890ff;
}

.status-completed {
  background: #f6ffed;
  color: #52c41a;
}

.status-failed {
  background: #fff2f0;
  color: #ff4d4f;
}

.btn-reparse {
  padding: 0.1rem 0.3rem;
  background: transparent;
  border: 1px solid currentColor;
  border-radius: 3px;
  color: inherit;
  cursor: pointer;
  font-size: 0.7rem;
}

.btn-reparse:hover {
  background: rgba(0, 0, 0, 0.1);
}

.doc-tags {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.tag {
  background: #f5f5f5;
  color: #666;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.doc-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #f0f0f0;
}

.doc-date {
  color: #999;
  font-size: 0.85rem;
}

.doc-actions {
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

.btn-parse {
  padding: 0.4rem 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  background: #1890ff;
  color: white;
}

.btn-parse:hover:not(:disabled) {
  background: #096dd9;
}

.btn-parse:disabled {
  background: #91d5ff;
  cursor: not-allowed;
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

.form-group input, .form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e1e5eb;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group input:focus, .form-group textarea:focus {
  outline: none;
  border-color: #667eea;
}

.file-upload-area {
  margin-bottom: 0.5rem;
}

.file-upload-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  border: 2px dashed #e1e5eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.file-upload-label:hover {
  border-color: #667eea;
  background-color: rgba(102, 126, 234, 0.05);
}

.upload-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.selected-file {
  color: #667eea;
  font-weight: 500;
}

.file-hint {
  color: #999;
  font-size: 0.85rem;
  margin: 0;
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