<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()
const user = ref(userStore.user)

const documents = ref([
  { id: 1, title: '公司规章制度', category: '管理制度', tags: '人事,行政', created_at: '2024-01-15' },
  { id: 2, title: '新员工入职指南', category: '培训资料', tags: '入职,培训', created_at: '2024-01-20' },
  { id: 3, title: '项目开发流程', category: '技术文档', tags: '开发,流程', created_at: '2024-02-01' },
  { id: 4, title: 'API接口文档', category: '技术文档', tags: 'API,接口', created_at: '2024-02-10' },
])

const searchQuery = ref('')
const showCreateModal = ref(false)

const newDoc = ref({
  title: '',
  content: '',
  category: '',
  tags: ''
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

const closeModal = () => {
  showCreateModal.value = false
  newDoc.value = { title: '', content: '', category: '', tags: '' }
}

const submitDoc = () => {
  if (newDoc.value.title && newDoc.value.content) {
    documents.value.unshift({
      id: documents.value.length + 1,
      title: newDoc.value.title,
      category: newDoc.value.category || '未分类',
      tags: newDoc.value.tags || '',
      created_at: new Date().toISOString().split('T')[0]
    })
    closeModal()
  }
}
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
        <button @click="handleCreateDoc" class="btn-create">➕ 新建文档</button>
      </div>

      <div class="documents-list">
        <div class="doc-card" v-for="doc in documents" :key="doc.id">
          <div class="doc-header">
            <h3>{{ doc.title }}</h3>
            <span class="doc-category">{{ doc.category }}</span>
          </div>
          <div class="doc-tags" v-if="doc.tags">
            <span class="tag" v-for="tag in doc.tags.split(',')" :key="tag">{{ tag }}</span>
          </div>
          <div class="doc-footer">
            <span class="doc-date">{{ doc.created_at }}</span>
            <div class="doc-actions">
              <button class="btn-edit">编辑</button>
              <button class="btn-delete">删除</button>
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
          <button class="btn-submit" @click="submitDoc">创建</button>
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

.btn-create {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
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
  margin-bottom: 1rem;
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
  max-width: 600px;
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
</style>
