<template>
  <div class="page-container">
    <header class="page-header">
      <button @click="goBack" class="back-button">
        <ArrowLeftIcon class="w-6 h-6" />
        <span>Back to Course</span>
      </button>
      <h1 class="page-title">Course Materials</h1>
    </header>

    <main class="content-area">
      <!-- Upload Section -->
      <div v-if="isOwner" class="upload-section">
        <div class="upload-box" @dragover.prevent @drop.prevent="handleDrop">
          <input type="file" ref="fileInput" @change="handleFileSelect" multiple class="hidden-input" />
          <div class="upload-content">
            <CloudArrowUpIcon class="upload-icon" />
            <p class="upload-text">Drag & drop your lecture slides here</p>
            <p class="upload-subtext">or</p>
            <button @click="triggerFileInput" class="browse-button">Browse Files</button>
            <p class="supported-files">Supported: PDF, PPTX, DOCX (max 25MB)</p>
          </div>
        </div>
      </div>

      <!-- Uploading Files Section -->
      <div v-if="uploadingFiles.length > 0" class="materials-list-section">
        <h2 class="section-title">Currently Uploading</h2>
        <ul class="materials-list">
          <li v-for="file in uploadingFiles" :key="file.name" class="material-item uploading">
            <div class="file-info">
              <DocumentIcon class="file-icon" />
              <div class="file-details">
                <span class="file-name">{{ file.name }}</span>
                <span class="file-size">{{ formatSize(file.size) }}</span>
              </div>
            </div>
            <div class="file-status">
              <div class="progress-bar">
                <div class="progress" :style="{ width: file.progress + '%' }"></div>
              </div>
              <span class="status-text">{{ file.progress }}%</span>
            </div>
          </li>
        </ul>
      </div>

      <!-- Processed Files Section -->
      <div class="materials-list-section">
        <h2 class="section-title">Uploaded Materials</h2>
        <ul v-if="materials.length > 0" class="materials-list">
          <li v-for="material in materials" :key="material.id" class="material-item">
            <div class="file-info">
              <component :is="getIconForFileType(material.type)" class="file-icon" />
              <div class="file-details">
                <span class="file-name">{{ material.name }}</span>
                <span class="file-size">{{ formatSize(material.size) }} - Uploaded on {{ material.uploadedDate }}</span>
              </div>
            </div>
            <div class="file-status">
              <span :class="['status-badge', getStatusClass(material.status)]">{{ material.status }}</span>
            </div>
            <div class="file-actions">
              <button @click="showSummary(material)" class="action-button" :disabled="material.status !== 'Ready' || !material.summary">
                <DocumentTextIcon class="w-5 h-5" />
                <span>View Summary</span>
              </button>
              <button @click="showQuiz(material)" class="action-button" :disabled="material.status !== 'Ready'">
                <QuestionMarkCircleIcon class="w-5 h-5" />
                <span>Generate Quiz</span>
              </button>
              <button class="action-button delete-button">
                <TrashIcon class="w-5 h-5" />
              </button>
            </div>
          </li>
        </ul>
        <div v-else class="empty-state">
          <p>No materials uploaded yet. Start by dropping a file above.</p>
        </div>
      </div>
    </main>
    <SummaryModal
      v-if="summaryIsShowing"
      :material-name="selectedMaterial.name"
      :summary="selectedMaterial.summary"
      @close="closeSummaryModal"
    />
    <QuizModal
      v-if="quizIsShowing"
      :material-name="selectedMaterial.name"
      @close="closeQuizModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import {
  ArrowLeftIcon,
  CloudArrowUpIcon,
  DocumentIcon,
  DocumentTextIcon,
  QuestionMarkCircleIcon,
  TrashIcon,
  PhotoIcon, // for pptx
  ClipboardDocumentIcon // for docx
} from '@heroicons/vue/24/outline';
import SummaryModal from '@/components/Graphs/Materials/SummaryModal.vue';
import QuizModal from '@/components/Graphs/Materials/QuizModal.vue';

const route = useRoute();
const router = useRouter();
const fileInput = ref<HTMLInputElement | null>(null);
const summaryIsShowing = ref(false);
const quizIsShowing = ref(false);
const selectedMaterial = ref(null as Material | null);
const isOwner = ref(false);

type UploadingFile = {
  id: number; // Use a unique ID for the list key
  name: string;
  size: number;
  progress: number;
  error?: string;
};
const uploadingFiles = ref<UploadingFile[]>([]);
let nextUploadId = 0;

type Material = {
    id: number;
    name: string;
    type: 'pdf' | 'pptx' | 'docx';
    size: number;
    uploadedDate: string;
    status: 'Ready' | 'Summarizing' | 'Error';
    summary: string;
};
const materials = ref<Material[]>([]);

const checkOwnership = async () => {
  const courseId = route.params.id as string;
  if (!courseId) return;
  try {
    const response = await axios.get(`/api/courses/${courseId}/is-owner`);
    isOwner.value = response.data.is_owner;
    console.log(isOwner.value ? "User is the owner of the course." : "User is NOT the owner of the course.");
  } catch (error) {
    console.error("Failed to check course ownership:", error);
    isOwner.value = false;
  }
};

const fetchMaterials = async () => {
  const courseId = route.params.id as string;
  if (!courseId) {
    console.error("Course ID is missing, cannot fetch materials.");
    return;
  }
  try {
    const response = await axios.get(`/api/materials/course/${courseId}`);

    if (!Array.isArray(response.data)) {
      console.error("Data received from backend is not an array as expected.");
      materials.value = [];
      return;
    }

    const statusMap: { [key: string]: 'Ready' | 'Summarizing' | 'Error' } = {
      processing: 'Summarizing',
      ready: 'Ready',
      error: 'Error',
    };

    materials.value = response.data.map((material: any) => ({
      id: material.id,
      name: material.name,
      type: material.type,
      size: material.size,
      uploadedDate: new Date(material.uploaded_at || new Date()).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
      status: statusMap[material.status] || 'Error',
      summary: material.summary || ''
    }));
  } catch (error) {
    console.error("Failed to fetch materials:", error);
  }
};

onMounted(() => {
  fetchMaterials();
  checkOwnership();
});

const goBack = () => {
  router.back();
};

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files) {
    uploadFiles(target.files);
  }
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

const handleDrop = (event: DragEvent) => {
  if (event.dataTransfer?.files) {
    uploadFiles(event.dataTransfer.files);
  }
};

async function uploadFiles(files: FileList) {
  if (!isOwner.value) {
    console.error("You are not the owner of this course and cannot upload materials.");
    // Optionally, show a user-facing error message here.
    return;
  }

  const courseId = route.params.id as string; // Assuming course ID is in route.params.id
  if (!courseId) {
    console.error("Course ID is missing from the route.");
    return;
  }

  for (const file of Array.from(files)) {
    const uploadId = nextUploadId++;
    const uploader: UploadingFile = {
      id: uploadId,
      name: file.name,
      size: file.size,
      progress: 0,
    };
    uploadingFiles.value.push(uploader);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('course_id', courseId);

    try {
      const response = await axios.post('/api/materials/upload', formData, {
        onUploadProgress: (progressEvent) => {
          const total = progressEvent.total || 0;
          const percent = Math.round((progressEvent.loaded * 100) / total);
          const uploadItem = uploadingFiles.value.find(f => f.id === uploadId);
          if (uploadItem) {
            uploadItem.progress = percent;
          }
        },
      });

      const newMaterial = response.data;

      // On successful upload, remove from uploading list
      uploadingFiles.value = uploadingFiles.value.filter(f => f.id !== uploadId);
      
      // Add to the main materials list to be shown in the UI
      const newMaterialForList: Material = {
        id: newMaterial.id,
        name: newMaterial.name,
        type: newMaterial.type,
        size: newMaterial.size,
        uploadedDate: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
        status: 'Summarizing', // Backend job will now process it
        summary: ''
      };
      materials.value.unshift(newMaterialForList);

    } catch (error: any) {
      const errorMsg = error.response?.data?.error || error.message || 'An unknown error occurred';
      console.error(`[Upload] Failed for ${file.name}:`, errorMsg);
      
      const uploadItem = uploadingFiles.value.find(f => f.id === uploadId);
      if (uploadItem) {
        uploadItem.error = errorMsg;
        uploadItem.progress = 100; // Mark as finished but with an error
      }
    }
  }
}

const formatSize = (bytes: number) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const getStatusClass = (status: string) => {
  switch (status) {
    case 'Ready': return 'status-ready';
    case 'Summarizing': return 'status-summarizing';
    case 'Error': return 'status-error';
    default: return '';
  }
};

const getIconForFileType = (type: string) => {
    if (type === 'pdf') return DocumentTextIcon;
    if (type === 'pptx') return PhotoIcon;
    if (type === 'docx') return ClipboardDocumentIcon;
    return DocumentIcon;
}

function showSummary(file: Material) {
    summaryIsShowing.value = true;
    selectedMaterial.value = file;
}

function closeSummaryModal() {
    summaryIsShowing.value = false;
    selectedMaterial.value = null;
}

function showQuiz(file: Material) {
    quizIsShowing.value = true;
    selectedMaterial.value = file;
}

function closeQuizModal() {
    quizIsShowing.value = false;
    selectedMaterial.value = null;
}
</script>

<style scoped>
/* Using CSS variables from the project */
.page-container {
  padding: 2rem 4rem;
  color: var(--light-text);
  height: 100vh;
  overflow-y: auto;
  background-color: var(--background-color);
}

@media (max-width: 768px) {
    .page-container {
        padding: 1rem;
    }
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  background-color: var(--background-color-1t);
  border: 1px solid var(--color-primary-dark);
  color: var(--highlight-color);
  transition: all 0.2s ease;
}
.back-button:hover {
  background-color: var(--element-color-1);
  transform: translateY(-2px);
}

.page-title {
  font-size: 2.25rem;
  font-weight: bold;
  margin-left: 1.5rem;
}

.content-area {
  max-width: 1200px;
  margin: 0 auto;
}

/* Upload Section */
.upload-section {
  background-color: var(--background-color-1t);
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 3rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.upload-box {
  border: 2px dashed var(--color-primary-dark);
  border-radius: 0.75rem;
  padding: 3rem;
  text-align: center;
  transition: background-color 0.2s ease;
}
.upload-box:hover {
  background-color: rgba(var(--highlight-color-rgb), 0.05);
  border-color: var(--highlight-color);
}

.upload-icon {
  width: 4rem;
  height: 4rem;
  margin: 0 auto 1rem;
  color: var(--highlight-color);
}

.upload-text {
  font-size: 1.25rem;
  font-weight: 500;
}

.upload-subtext {
  margin: 0.5rem 0;
  color: var(--text-color-secondary);
}

.browse-button {
  padding: 0.75rem 1.5rem;
  background-color: var(--highlight-color);
  color: var(--element-color-1);
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
}
.browse-button:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.supported-files {
  margin-top: 1rem;
  font-size: 0.875rem;
  color: var(--text-color-secondary);
}

.hidden-input {
  display: none;
}

/* Materials List */
.materials-list-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--color-primary-dark);
}

.materials-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.material-item {
  display: grid;
  grid-template-columns: 2fr 1fr 2fr;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem 1.5rem;
  background-color: var(--background-color-1t);
  border-radius: 0.75rem;
  border: 1px solid transparent;
  transition: all 0.2s ease;
}
.material-item:hover {
  border-color: var(--color-primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.file-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  min-width: 0;
}

.file-icon {
  width: 2.5rem;
  height: 2.5rem;
  color: var(--highlight-color);
  flex-shrink: 0;
}

.file-details {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.file-name {
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-size {
  font-size: 0.875rem;
  color: var(--text-color-secondary);
}

/* Status */
.file-status {
    display: flex;
    align-items: center;
}
.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
  white-space: nowrap;
}
.status-ready { background-color: #2ecc71; color: white; }
.status-summarizing { background-color: #3498db; color: white; }
.status-error { background-color: #e74c3c; color: white; }

/* Actions */
.file-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  background-color: var(--element-color-1);
  border: 1px solid var(--color-primary-dark);
  color: var(--light-text);
  transition: all 0.2s ease;
  cursor: pointer;
}
.action-button:hover:not(:disabled) {
  background-color: var(--element-color-2);
  transform: scale(1.05);
}
.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.delete-button:hover:not(:disabled) {
  background-color: #e74c3c;
  color: white;
}

/* Uploading item */
.material-item.uploading {
  grid-template-columns: 1fr 1fr;
}
.progress-bar {
  width: 100%;
  height: 8px;
  background-color: var(--element-color-1);
  border-radius: 4px;
  overflow: hidden;
}
.progress {
  height: 100%;
  background-color: var(--highlight-color);
  transition: width 0.3s ease;
}
.status-text {
  font-size: 0.875rem;
  margin-left: 1rem;
  white-space: nowrap;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem;
  background-color: var(--background-color-1t);
  border-radius: 0.75rem;
  color: var(--text-color-secondary);
}

@media (max-width: 1024px) {
    .material-item {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    .file-actions {
        justify-content: flex-start;
    }
}
</style>
