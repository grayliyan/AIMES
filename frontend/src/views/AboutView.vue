<script setup>
import { ref } from 'vue'

const message = ref('关于我们')
</script>

<template>
  <div class="about">
    <h1>{{ message }}</h1>
    <p>知识库系统是一个企业内部知识管理与智能问答平台。</p>
    <p>我们致力于帮助企业高效管理和利用内部知识资源。</p>
  </div>
</template>

<style scoped>
.about {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

h1 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

p {
  color: #666;
  margin-bottom: 0.5rem;
}
</style>
