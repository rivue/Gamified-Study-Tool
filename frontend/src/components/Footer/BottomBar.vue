<template>
    <div class="app-footer">
      <div class="footer-bottom">
        <div class="footer-top">
          <router-link to="/changelog" class="text-link">Changelog</router-link>
          <span class="separator">·</span>
          <router-link to="/terms" class="text-link">Terms and Policies</router-link>
          <span class="separator">·</span>
          <p>© 2025 Rivue.ai</p>
        </div>
        <div>
          <p class="sincere-msg">Made with ❤️ for thinking and doing.</p>
        </div>
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
    padding: 12px 0;
    text-align: center;
    font-size: 14px;
    display: flex;
    flex-direction: column;
    width: 100%;
    margin: 0 auto;
    z-index: 200;
    background-color: var(--background-color-1t);
    backdrop-filter: blur(8px);
    box-shadow: 0 0 2px 2px var(--background-color-1t);
}

.footer-top,
.footer-bottom {
    display: flex;
    justify-content: center;
    align-items: center;
}

.footer-bottom {
    flex-direction: column;
}

.link-icon:hover {
    opacity: 0.6;
}

.separator {
    margin: 0 5px;
}

.text-link {
    cursor: pointer;
    color: var(--text-color);
    text-decoration: none;
}

.text-link:hover {
    opacity: 0.6;
}
</style>
