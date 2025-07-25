<template>
  <div class="legal-documents">
    <h1>Terms of Service and Privacy Policy</h1>
    <div class="documents-container">
      <div class="document" v-html="termsOfService"></div>
      <div class="document" v-html="privacyPolicy"></div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { marked } from 'marked';

export default defineComponent({
  name: 'LegalDocuments',
  setup() {
    const termsOfService = ref<string | Promise<string>>('');
    const privacyPolicy = ref<string | Promise<string>>('');

    const fetchDocuments = async () => {
      try {
        const termsResponse = await fetch('/legal/terms.md');
        const termsText = await termsResponse.text();
        termsOfService.value = marked(termsText);

        const policyResponse = await fetch('/legal/privacy.md');
        const policyText = await policyResponse.text();
        privacyPolicy.value = marked(policyText);
      } catch (error) {
        console.error('Error fetching legal documents:', error);
      }
    };

    onMounted(() => {
      fetchDocuments();
    });

    return {
      termsOfService,
      privacyPolicy,
    };
  },
});
</script>

<style scoped>
.legal-documents {
  padding: 20px;
}

.documents-container {
  display: flex;
  gap: 20px;
}

.document {
  flex: 1;
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 8px;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
