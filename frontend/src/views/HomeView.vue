<script setup>
import { ref } from 'vue'

const message = ref('Welcome to Knowledge Base System')
</script>

<template>
  <div class="home">
    <h1>{{ message }}</h1>
    <p>This is the home page of your knowledge base system.</p>
  </div>
</template>

<style scoped>
.home {
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
}
</style>