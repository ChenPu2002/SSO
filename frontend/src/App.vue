<template>
    <div id="app">
      <div v-if="!isLoggedIn">
        <h2>登录</h2>
        <form @submit.prevent="doLogin">
          <div>
            <label for="username">用户名:</label>
            <input id="username" v-model="username" type="text" required />
          </div>
          <div>
            <label for="password">密码:</label>
            <input id="password" v-model="password" type="password" required />
          </div>
          <button type="submit">登录</button>
        </form>
        <p v-if="error" style="color:red;">{{ error }}</p>
      </div>
      <div v-else>
        <h2>欢迎, {{ user }}</h2>
        <button @click="getProtectedData">获取受保护数据</button>
        <p>{{ protectedMessage }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'App',
    data() {
      return {
        username: '',
        password: '',
        token: localStorage.getItem('token') || '',
        error: '',
        protectedMessage: ''
      };
    },
    computed: {
      isLoggedIn() {
        return !!this.token;
      },
      user() {
        if (!this.token) return '';
        try {
          const payloadBase64 = this.token.split('.')[1];
          const payload = JSON.parse(atob(payloadBase64));
          return payload.sub;
        } catch (err) {
          return '';
        }
      }
    },
    methods: {
      async doLogin() {
        try {
          // OAuth2PasswordRequestForm 格式需要将参数放在 URLSearchParams 中
          const params = new URLSearchParams();
          params.append('username', this.username);
          params.append('password', this.password);
          const response = await axios.post('http://localhost:8000/login', params);
          this.token = response.data.access_token;
          localStorage.setItem('token', this.token);
          this.error = '';
        } catch (err) {
          console.error(err);
          this.error = '登录失败，请检查用户名和密码';
        }
      },
      async getProtectedData() {
        try {
          const response = await axios.get('http://localhost:8000/protected', {
            headers: {
              Authorization: `Bearer ${this.token}`
            }
          });
          this.protectedMessage = response.data.message;
        } catch (err) {
          console.error(err);
          this.protectedMessage = '无法获取受保护数据';
        }
      }
    }
  }
  </script>
  
  <style>
  #app {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  form div {
    margin-bottom: 10px;
  }
</style>