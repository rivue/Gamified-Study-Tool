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
      <div class="upload-section">
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
    <!-- <QuizModal
      v-if="quizIsShowing"
      :material-name="selectedMaterial.name"
      @close="closeQuizModal"
    /> -->
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import {
  ArrowLeftIcon,
  CloudArrowUpIcon,
  DocumentIcon,
  DocumentTextIcon,
  QuestionMarkCircleIcon,
  TrashIcon,
  PhotoIcon, // for pptx
  ClipboardDocumentIcon // for docx
} from '@heroicons/vue/24/outline'; // Using outline for a lighter feel
import SummaryModal from '@/components/Graphs/Materials/SummaryModal.vue';
// import QuizModal from '@/components/QuizModal.vue';

const router = useRouter();
const fileInput = ref<HTMLInputElement | null>(null);
const summaryIsShowing = ref(false);
// const quizIsShowing = ref(false);
const selectedMaterial = ref(null as Material | null);

// Mock data
const uploadingFiles = ref([
  { name: 'Introduction to AI.pptx', size: 5242880, progress: 45 }
]);

type Material = {
    id: number;
    name: string;
    type: 'pdf' | 'pptx' | 'docx';
    size: number;
    uploadedDate: string;
    status: 'Ready' | 'Summarizing' | 'Error';
    summary: string;
};
const summary = `Line 1: Artificial Intelligence (AI) studies systems that perceive, reason, learn, and act.
Line 2: Narrow AI focuses on specific tasks like classification or translation.
Line 3: General AI (AGI) would perform any intellectual task humans can, but remains hypothetical.
Line 4: Key historical milestone: Dartmouth workshop (1956) coined the term AI.
Line 5: Symbolic AI emphasized logic, rules, and explicit knowledge representation.
Line 6: Machine Learning (ML) shifted focus to data-driven pattern learning.
Line 7: ML paradigm: algorithms improve performance P on task T given experience E.
Line 8: Supervised learning uses labeled examples (input, desired output).
Line 9: Unsupervised learning discovers structure in unlabeled data.
Line 10: Reinforcement learning optimizes sequential decisions via reward signals.
Line 11: Common supervised tasks: classification (categorical output) and regression (continuous output).
Line 12: Features are measurable properties fed into models.
Line 13: Labels are ground-truth outcomes used for training in supervised learning.
Line 14: Dataset split: training, validation, test for honest performance estimation.
Line 15: Overfitting occurs when a model memorizes noise instead of general patterns.
Line 16: Underfitting happens when the model is too simple to capture relationships.
Line 17: Bias refers to systematic error from erroneous assumptions.
Line 18: Variance refers to sensitivity to fluctuations in the training set.
Line 19: Goal: find bias–variance balance for generalization.
Line 20: Evaluation metrics must align with business or scientific objectives.
Line 21: Accuracy can mislead on imbalanced datasets.
Line 22: Precision measures correctness of positive predictions.
Line 23: Recall measures coverage of actual positives.
Line 24: F1 score harmonizes precision and recall.
Line 25: ROC curve plots true positive rate vs false positive rate.
Line 26: AUC summarizes overall separability.
Line 27: Confusion matrix tabulates prediction outcomes (TP, FP, TN, FN).
Line 28: Loss functions quantify prediction error during training.
Line 29: Mean Squared Error penalizes large regression deviations.
Line 30: Cross-entropy loss suits probabilistic classification.
Line 31: Gradient descent iteratively updates parameters to minimize loss.
Line 32: Learning rate controls step size; too large diverges, too small stagnates.
Line 33: Stochastic Gradient Descent (SGD) uses mini-batches for efficiency and noise benefits.
Line 34: Regularization discourages overly complex models.
Line 35: L2 regularization shrinks weights smoothly.
Line 36: L1 regularization encourages sparsity (feature selection).
Line 37: Early stopping halts training when validation loss stops improving.
Line 38: Data preprocessing includes normalization and encoding categorical variables.
Line 39: One-hot encoding converts categories to binary indicator vectors.
Line 40: Feature scaling helps gradient-based methods converge.
Line 41: Principal Component Analysis (PCA) reduces dimensionality via variance maximization.
Line 42: K-Nearest Neighbors classifies by majority vote among closest points.
Line 43: Decision trees split features to maximize purity.
Line 44: Entropy measures uncertainty; information gain measures reduction.
Line 45: Random forests aggregate many decorrelated trees to reduce variance.
Line 46: Gradient boosting sequentially fits models to residual errors.
Line 47: Support Vector Machines seek maximal margin hyperplanes.
Line 48: Kernel trick enables implicit high-dimensional mapping.
Line 49: Logistic regression outputs class probabilities via sigmoid.
Line 50: Probabilistic calibration matters for downstream risk decisions.
Line 51: Neural networks compose layers of linear transforms and nonlinear activations.
Line 52: Activation functions introduce nonlinearity (ReLU, sigmoid, tanh, GELU).
Line 53: Backpropagation applies chain rule to compute gradients efficiently.
Line 54: Deep learning leverages large data and compute to learn hierarchical features.
Line 55: Convolutional Neural Networks (CNNs) exploit spatial locality in images.
Line 56: Recurrent Neural Networks (RNNs) handle sequential dependencies.
Line 57: Long Short-Term Memory (LSTM) units mitigate vanishing gradients.
Line 58: Transformers use self-attention to model global token interactions.
Line 59: Attention weights reallocate focus dynamically across sequence positions.
Line 60: Pretraining followed by fine-tuning enables transfer learning efficiency.
Line 61: Embeddings map discrete tokens to dense vector spaces capturing semantics.
Line 62: Data augmentation improves robustness by synthetically diversifying samples.
Line 63: Class imbalance strategies: resampling, synthetic generation, cost-sensitive losses.
Line 64: Explainability tools (SHAP, LIME) elucidate model predictions.
Line 65: Model interpretability influences trust and regulatory compliance.
Line 66: Fairness concerns address disparate impact across demographic groups.
Line 67: Ethical AI includes transparency, accountability, inclusiveness, reliability.
Line 68: Robustness assesses performance under distributional shift or adversarial noise.
Line 69: Adversarial examples reveal vulnerabilities in learned decision boundaries.
Line 70: MLOps operationalizes ML through reproducibility, monitoring, and automation.
Line 71: Version control of data and models aids traceability.
Line 72: Deployment patterns: batch inference, real-time APIs, streaming.
Line 73: Concept drift occurs when statistical properties of targets change over time.
Line 74: Monitoring metrics post-deployment detects performance degradation.
Line 75: Feature stores centralize and standardize engineered features.
Line 76: Data lineage tracks origin, transformations, and usage.
Line 77: Privacy-preserving ML techniques include differential privacy and federated learning.
Line 78: Differential privacy adds calibrated noise to protect individual records.
Line 79: Federated learning keeps raw data local while sharing model updates.
Line 80: Reinforcement learning formalizes environment interaction via Markov Decision Processes.
Line 81: Policy defines action selection strategy given a state.
Line 82: Value function estimates expected cumulative reward.
Line 83: Exploration–exploitation tradeoff balances learning vs using knowledge.
Line 84: Q-learning learns action-value estimates iteratively.
Line 85: Policy gradients optimize expected reward directly.
Line 86: Model-based RL learns environment dynamics explicitly.
Line 87: Scaling laws observe predictable performance gains with data/model size.
Line 88: Energy efficiency and carbon footprint are emerging AI concerns.
Line 89: Curriculum learning orders examples from easy to hard.
Line 90: Active learning queries labels for most informative samples.
Line 91: Semi-supervised learning leverages unlabeled data with limited labels.
Line 92: Self-supervised learning creates proxy tasks from raw structure.
Line 93: Transfer learning adapts pretrained representations to new domains.
Line 94: Domain adaptation mitigates shift between source and target distributions.
Line 95: Zero-shot learning generalizes to unseen classes via semantic descriptors.
Line 96: Few-shot learning performs with extremely limited labeled examples.
Line 97: Benchmark suites (ImageNet, GLUE) drive comparative progress.
Line 98: Open research challenges include reasoning, grounding, and alignment.
Line 99: Responsible deployment demands iterative auditing and stakeholder engagement.
Line 100: Foundational understanding of these concepts enables deeper AI specialization.`
const materials = ref<Material[]>([
    {
        id: 1,
        name: 'Machine Learning Basics.pdf',
        type: 'pdf',
        size: 1258291,
        uploadedDate: 'Aug 28, 2025',
        status: 'Ready',
        summary: summary
    },
    {
        id: 2,
        name: 'Neural Networks Deep Dive.pptx',
        type: 'pptx',
        size: 8388608,
        uploadedDate: 'Aug 27, 2025',
        status: 'Summarizing',
        summary: summary
    },
    {
        id: 3,
        name: 'Course_Syllabus.docx',
        type: 'docx',
        size: 450560,
        uploadedDate: 'Aug 26, 2025',
        status: 'Error',
        summary: summary
    },
]);

const goBack = () => {
  router.back();
};

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files) {
    // handle files
  }
};

const handleDrop = (event: DragEvent) => {
  if (event.dataTransfer?.files) {
    // handle files
  }
};

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

// function showQuiz(file: Material) {
//     quizIsShowing.value = true;
//     selectedMaterial.value = file;
// }

// function closeQuizModal() {
//     quizIsShowing.value = false;
//     selectedMaterial.value = null;
// }

// Simulate upload progress for mock
setInterval(() => {
  if (uploadingFiles.value.length > 0) {
    const progress = uploadingFiles.value[0].progress + 5;
    if (progress >= 100) {
      uploadingFiles.value = [];
    } else {
      uploadingFiles.value[0].progress = progress;
    }
  }
}, 500);
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
