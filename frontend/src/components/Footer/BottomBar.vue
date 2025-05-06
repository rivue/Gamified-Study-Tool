<template>
    <div class="app-footer">
      <div class="footer-bottom">
          <p>© 2025 Rivue.ai</p>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed } from 'vue';
  import { useThemeStore } from '@/store/themeStore';
  
  const themeStore = useThemeStore();
  
  const darkMode = computed(() => themeStore.darkMode);
  
  const themeIcon = computed(() =>
    darkMode.value
      ? require('@/assets/images/darkmode.png')
      : require('@/assets/images/lightmode.png')
  );
  
  const xIcon = computed(() =>
    darkMode.value
      ? require('@/assets/images/x-logo-black.png')
      : require('@/assets/images/x-logo-white.png')
  );
  
  const discordIcon = computed(() =>
    darkMode.value
      ? require('@/assets/images/discord-mark-black.png')
      : require('@/assets/images/discord-mark-white.png')
  );
  
  const themeIconAlt = computed(() =>
    darkMode.value ? 'Light Mode' : 'Dark Mode'
  );
  
  function toggleTheme() {
    themeStore.toggleDarkMode();
  }
  
  function donateRedirect() {
    window.open('https://donate.stripe.com/fZe8Ao9hl63qe9GeUX', '_blank');
  }
  </script>

<style scoped>
.app-footer {
    position: -webkit-sticky;
    position: sticky;
    bottom: -1px;
    /* font-family: "Garamond", sans-serif; */
    color: rgba(var(--text-color-rgb), 0.8);
    padding: 6px 0;
    text-align: center;
    font-size: 12px;
    display: flex;
    flex-direction: column;
    width: 100%;
    margin: 0 auto;
    z-index: 200;
    background-color: var(--background-color-1t);
}


.footer-bottom {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}
</style>
