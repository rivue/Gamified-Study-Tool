<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <div class="tabs">
          <button :class="{ active: activeTab === 'terms' }" @click="activeTab = 'terms'">Terms of Service</button>
          <button :class="{ active: activeTab === 'privacy' }" @click="activeTab = 'privacy'">Privacy Policy</button>
        </div>
        <button class="close-btn" @click="$emit('close')">Close</button>
      </div>
      <div class="modal-body">
        <div v-if="activeTab === 'terms'" v-html="termsContent" class="legal-text"></div>
        <div v-if="activeTab === 'privacy'" v-html="privacyContent" class="legal-text"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { marked } from 'marked';

defineEmits(['close']);

const activeTab = ref('terms');
const termsContent = ref<string | Promise<string>>('');
const privacyContent = ref<string | Promise<string>>('');

const fetchDocuments = async () => {
  try {
    const termsResponse = await fetch('/legal/terms.md');
    const termsText = await termsResponse.text();
    termsContent.value = marked(termsText);

    const policyResponse = await fetch('/legal/privacy.md');
    const policyText = await policyResponse.text();
    privacyContent.value = marked(policyText);
  } catch (error) {
    console.error('Error fetching legal documents:', error);
    termsContent.value = '<p>Could not load Terms of Service.</p>';
    privacyContent.value = '<p>Could not load Privacy Policy.</p>';
  }
};

onMounted(() => {
  fetchDocuments();
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 1);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
  box-sizing: border-box;
}

.modal-content {
  background-color: var(--background-color-1);
  width: 80%;
  max-width: 900px;
  height: 80vh;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  border-bottom: 1px solid var(--background-color-2);
  flex-wrap: wrap;
  gap: 10px;
}

.tabs {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.tabs button {
  padding: 10px 15px;
  border: none;
  background-color: transparent;
  color: var(--text-color-secondary);
  cursor: pointer;
  font-size: 16px;
  border-bottom: 2px solid transparent;
  min-height: 44px;
}

.tabs button.active {
  color: var(--accent-color-1);
  border-bottom-color: var(--accent-color-1);
}

.close-btn {
  background: none;
  border: none;
  font-size: 16px;
  color: var(--text-color-secondary);
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 4px;
  background-color: var(--background-color-2);
  min-height: 44px;
  min-width: 44px;
}

.close-btn:hover {
  background-color: var(--background-color-3, var(--background-color-2));
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.legal-text {
  color: var(--text-color);
  line-height: 1.6;
}

/* Mobile optimizations */
@media (max-width: 768px) {
  .modal-overlay {
    padding: 10px;
  }
  
  .modal-content {
    width: 95%;
    height: 90vh;
    max-height: 90vh;
  }
  
  .modal-header {
    padding: 15px;
    flex-direction: column;
    align-items: stretch;
  }
  
  .tabs {
    justify-content: center;
    margin-bottom: 10px;
  }
  
  .tabs button {
    flex: 1;
    text-align: center;
    font-size: 14px;
    padding: 12px 8px;
  }
  
  .close-btn {
    align-self: center;
    padding: 12px 24px;
  }
  
  .modal-body {
    padding: 15px;
  }
  
  .legal-text {
    font-size: 14px;
    line-height: 1.7;
  }
}

@media (max-width: 480px) {
  .modal-overlay {
    padding: 5px;
  }
  
  .modal-content {
    width: 98%;
    height: 95vh;
    border-radius: 4px;
  }
  
  .tabs button {
    font-size: 13px;
    padding: 10px 6px;
  }
  
  .modal-body {
    padding: 12px;
  }
  
  .legal-text {
    font-size: 13px;
  }
}
</style>
