<template>
    <div class="not-found-container">
      <div class="content">
        <h1 class="title">404</h1>
        <h2 class="subtitle">Oops! This library doesn't exist yet</h2>
        <p class="message">Even the stars get lost in the Rivue cosmos sometimes!</p>
        <p class="hint">Perhaps this knowledge hasn't reached the Rivue library yet?</p>
        <router-link to="/" class="home-button">Return to Library</router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NotFound'
  }
  </script>
  
  <style scoped>
  .not-found-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    text-align: center;
    padding: 1rem;
    font-family: 'Arial', sans-serif;
    color: #e0e0e0;
  }
  
  .content {
    max-width: 600px;
    padding: 2rem;
    background-color: rgba(40, 40, 60, 0.9);
    border-radius: 12px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
  }
  
  .title {
    font-size: 8rem;
    color: #00a8cc;
    margin-bottom: 0;
    text-shadow: 3px 3px 0 rgba(0, 0, 0, 0.2);
  }
  
  .subtitle {
    font-size: 2rem;
    color: #f5f5f5;
    margin-top: 0;
  }
  
  .message {
    font-size: 1.5rem;
    color: #b0b0b0;
    margin: 1.5rem 0;
  }
  
  .hint {
    font-style: italic;
    color: #999;
    margin: 2rem 0;
  }
  
  .home-button {
    display: inline-block;
    background-color: #007acc;
    color: white;
    padding: 0.8rem 1.5rem;
    border-radius: 50px;
    text-decoration: none;
    font-weight: bold;
    transition: transform 0.2s, background-color 0.2s;
  }
  
  .home-button:hover {
    background-color: #005f99;
    transform: scale(1.05);
  }
  
  </style>
