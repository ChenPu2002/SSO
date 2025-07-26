<template>
    <div id="app">
      <div v-if="!isLoggedIn" class="container">
        <div class="card">
          <div class="text-center mb-xl">
            <h1 class="app-title">SSO 登录</h1>
            <p class="app-subtitle">欢迎回来，请登录您的账户</p>
          </div>
          
          <form @submit.prevent="doLogin" class="login-form">
            <div class="form-group mb-lg">
              <div class="input-wrapper">
                <span class="input-icon">👤</span>
                <input 
                  id="username" 
                  v-model="username" 
                  type="text" 
                  class="form-input"
                  placeholder="用户名"
                  required 
                />
                <label for="username" class="form-label">用户名</label>
              </div>
            </div>
            
            <div class="form-group mb-xl">
              <div class="input-wrapper">
                <span class="input-icon">🔒</span>
                <input 
                  id="password" 
                  v-model="password" 
                  type="password" 
                  class="form-input"
                  placeholder="密码"
                  required 
                />
                <label for="password" class="form-label">密码</label>
              </div>
            </div>
            
            <button type="submit" class="btn btn-primary btn-full" :disabled="isLoading">
              <span v-if="isLoading" class="loading-spinner"></span>
              {{ isLoading ? '登录中...' : '登录' }}
            </button>
          </form>
          
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
        </div>
      </div>
      <div v-else class="container">
        <div class="card">
          <div class="user-header text-center mb-xl">
            <div class="user-avatar">
              {{ userInitials }}
            </div>
            <h2 class="welcome-title">欢迎回来</h2>
            <p class="welcome-subtitle">{{ user }}</p>
          </div>
          
          <div class="actions-section">
            <button @click="getProtectedData" class="btn btn-primary btn-full mb-lg" :disabled="isLoadingData">
              <span v-if="isLoadingData" class="loading-spinner"></span>
              {{ isLoadingData ? '加载中...' : '获取受保护数据' }}
            </button>
            
            <div v-if="protectedMessage" class="protected-data-card">
              <h3 class="data-title">受保护数据</h3>
              <p class="data-content">{{ protectedMessage }}</p>
            </div>
            
            <button @click="logout" class="btn btn-secondary btn-full">
              退出登录
            </button>
          </div>
        </div>
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
        protectedMessage: '',
        isLoading: false,
        isLoadingData: false
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
      },
      userInitials() {
        if (!this.user) return '';
        return this.user.substring(0, 2).toUpperCase();
      }
    },
    methods: {
      async doLogin() {
        this.isLoading = true;
        this.error = '';
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
        } finally {
          this.isLoading = false;
        }
      },
      async getProtectedData() {
        this.isLoadingData = true;
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
        } finally {
          this.isLoadingData = false;
        }
      },
      logout() {
        this.token = '';
        this.protectedMessage = '';
        this.username = '';
        this.password = '';
        this.error = '';
        localStorage.removeItem('token');
      }
    }
  }
  </script>
  
  <style>
  /* CSS Custom Properties (Design Tokens) */
  :root {
    --color-primary: #667eea;
    --color-secondary: #764ba2;
    --color-success: #10b981;
    --color-error: #ef4444;
    --color-warning: #f59e0b;
    --color-neutral: #6b7280;
    --color-background: #f8fafc;
    --color-surface: #ffffff;
    
    --font-family-primary: 'Inter', system-ui, sans-serif;
    --font-size-heading: 2rem;
    --font-size-subheading: 1.5rem;
    --font-size-body: 1rem;
    --font-size-small: 0.875rem;
    
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    --spacing-2xl: 3rem;
    
    --border-radius: 0.5rem;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    
    /* Performance optimized animation timing */
    --transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-normal: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow: 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* CSS Reset and Base Styles */
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: var(--font-family-primary);
    font-size: var(--font-size-body);
    line-height: 1.6;
    color: var(--color-neutral);
    background: var(--color-background);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  #app {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-md);
    /* CSS containment for performance */
    contain: layout style paint;
  }

  /* Utility Classes */
  .container {
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
  }

  .card {
    background: var(--color-surface);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-lg);
    padding: var(--spacing-2xl);
    /* CSS containment for isolated rendering */
    contain: layout style paint;
  }

  .text-center {
    text-align: center;
  }

  .mb-sm { margin-bottom: var(--spacing-sm); }
  .mb-md { margin-bottom: var(--spacing-md); }
  .mb-lg { margin-bottom: var(--spacing-lg); }
  .mb-xl { margin-bottom: var(--spacing-xl); }

  /* Responsive Design */
  @media (max-width: 768px) {
    #app {
      padding: var(--spacing-sm);
    }
    
    .container {
      max-width: 100%;
    }
    
    .card {
      padding: var(--spacing-lg);
    }
  }

  @media (min-width: 769px) and (max-width: 1024px) {
    .container {
      max-width: 500px;
    }
  }

  @media (min-width: 1025px) {
    .container {
      max-width: 400px;
    }
  }

  /* Login Form Styles */
  .app-title {
    font-size: var(--font-size-heading);
    font-weight: 600;
    color: var(--color-primary);
    margin-bottom: var(--spacing-sm);
  }

  .app-subtitle {
    font-size: var(--font-size-body);
    color: var(--color-neutral);
    opacity: 0.8;
  }

  .login-form {
    width: 100%;
  }

  .form-group {
    position: relative;
  }

  .input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
  }

  .input-icon {
    position: absolute;
    left: var(--spacing-md);
    z-index: 2;
    font-size: var(--font-size-body);
    opacity: 0.6;
  }

  .form-input {
    width: 100%;
    padding: var(--spacing-md) var(--spacing-md) var(--spacing-md) 3rem;
    border: 2px solid #e5e7eb;
    border-radius: var(--border-radius);
    font-size: var(--font-size-body);
    font-family: var(--font-family-primary);
    background: var(--color-surface);
    /* Optimized transitions using only transform and opacity */
    transition: border-color var(--transition-normal), box-shadow var(--transition-normal);
    outline: none;
    /* Performance hint for focus animations */
    will-change: border-color, box-shadow;
  }

  .form-input:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }

  .form-input:focus + .form-label,
  .form-input:not(:placeholder-shown) + .form-label {
    transform: translateY(-1.5rem) scale(0.85);
    color: var(--color-primary);
  }

  .form-label {
    position: absolute;
    left: 3rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: var(--font-size-body);
    color: var(--color-neutral);
    opacity: 0.7;
    /* Optimized transitions using only transform and opacity */
    transition: transform var(--transition-normal), color var(--transition-normal), opacity var(--transition-fast);
    pointer-events: none;
    background: var(--color-surface);
    padding: 0 var(--spacing-xs);
    /* Performance hint for label animations */
    will-change: transform, color, opacity;
  }

  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-md) var(--spacing-lg);
    border: none;
    border-radius: var(--border-radius);
    font-size: var(--font-size-body);
    font-weight: 500;
    font-family: var(--font-family-primary);
    cursor: pointer;
    /* Optimized transitions using only transform and box-shadow */
    transition: transform var(--transition-normal), box-shadow var(--transition-normal), background-color var(--transition-fast);
    text-decoration: none;
    outline: none;
    /* Performance hint for button animations */
    will-change: transform, box-shadow;
    /* CSS containment for button rendering */
    contain: layout style;
  }

  .btn-primary {
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    color: white;
    box-shadow: var(--shadow-md);
  }

  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
  }

  .btn-primary:active {
    transform: translateY(0);
  }

  .btn-full {
    width: 100%;
  }

  .btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none !important;
  }

  .loading-spinner {
    display: inline-block;
    width: 1rem;
    height: 1rem;
    border: 2px solid transparent;
    border-top: 2px solid currentColor;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-right: var(--spacing-sm);
    /* Performance hint for spinner animation */
    will-change: transform;
    /* CSS containment for spinner rendering */
    contain: layout style paint;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .error-message {
    margin-top: var(--spacing-lg);
    padding: var(--spacing-md);
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.2);
    border-radius: var(--border-radius);
    color: var(--color-error);
    font-size: var(--font-size-small);
    text-align: center;
    animation: slideIn var(--transition-normal) cubic-bezier(0.4, 0, 0.2, 1);
    /* Performance hint for slide-in animation */
    will-change: transform, opacity;
    /* CSS containment for error message rendering */
    contain: layout style paint;
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Authenticated User Interface Styles */
  .user-header {
    border-bottom: 1px solid #e5e7eb;
    padding-bottom: var(--spacing-xl);
  }

  .user-avatar {
    width: 4rem;
    height: 4rem;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: var(--font-size-subheading);
    font-weight: 600;
    margin: 0 auto var(--spacing-lg);
    box-shadow: var(--shadow-md);
    /* CSS containment for avatar rendering */
    contain: layout style paint;
  }

  .welcome-title {
    font-size: var(--font-size-subheading);
    font-weight: 600;
    color: var(--color-neutral);
    margin-bottom: var(--spacing-sm);
  }

  .welcome-subtitle {
    font-size: var(--font-size-body);
    color: var(--color-neutral);
    opacity: 0.8;
  }

  .actions-section {
    padding-top: var(--spacing-xl);
  }

  .btn-secondary {
    background: #f3f4f6;
    color: var(--color-neutral);
    border: 1px solid #d1d5db;
  }

  .btn-secondary:hover {
    background: #e5e7eb;
    transform: translateY(-1px);
    box-shadow: var(--shadow-sm);
  }

  .protected-data-card {
    background: rgba(16, 185, 129, 0.05);
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: var(--border-radius);
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
    animation: slideIn var(--transition-normal) cubic-bezier(0.4, 0, 0.2, 1);
    /* Performance hint for slide-in animation */
    will-change: transform, opacity;
    /* CSS containment for protected data card rendering */
    contain: layout style paint;
  }

  .data-title {
    font-size: var(--font-size-body);
    font-weight: 600;
    color: var(--color-success);
    margin-bottom: var(--spacing-sm);
  }

  .data-content {
    font-size: var(--font-size-body);
    color: var(--color-neutral);
    line-height: 1.5;
  }
</style>