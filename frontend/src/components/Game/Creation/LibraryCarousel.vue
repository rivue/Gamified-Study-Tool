<template>
  <div class="library-list">
    <div class="list-header">
      <h1>Libraries</h1>
      <p class="subtitle">Browse your learning libraries and track your progress.</p>
    </div>
    
    <div class="list-table">
      <div class="table-header">
        <div class="col-thumbnail">Preview</div>
        <div class="col-name">Name</div>
        <div class="col-status">Status</div>
        <div class="col-stats">Statistics</div>
        <div class="col-date">Created at</div>
        <div class="col-actions"></div>
      </div>

      <div 
        v-for="library in libraries" 
        :key="library.id" 
        class="library-item"
        @click="goToLibrary(library.id)"
      >
        <div class="col-thumbnail">
          <div 
            class="thumbnail" 
            :style="{ backgroundImage: `url(${library.image_url})` }"
          ></div>
        </div>
        <div class="col-name">
          <h3>{{ library.library_topic }}</h3>
        </div>
        <div class="col-status">
          <span class="status-badge">Active</span>
        </div>
        <div class="col-stats">
          <span class="stat">👥 {{ library.clicks || 0 }}</span>
          <span class="stat">❤️ {{ library.likes || 0 }}</span>
        </div>
        <div class="col-date">
          {{ new Date(library.created_at).toLocaleDateString() }}
        </div>
        <div class="col-actions">
          <button class="action-btn">⋮</button>
        </div>
      </div>
    </div>
  <div class="pagination">
      <div class="pagination-info">
        Showing {{ startIndex + 1 }}-{{ endIndex }} of {{ totalItems }} products
      </div>
      <div class="pagination-controls">
        <button 
          class="pagination-btn" 
          :disabled="currentPage === 1"
          @click="prevPage"
        >
          Prev
        </button>
        <button 
          class="pagination-btn" 
          :disabled="currentPage === totalPages"
          @click="nextPage"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LibraryList",
  props: {
    libraries: {
      type: Array,
      required: true,
      default: () => []
    }
  },
  computed: {
    totalItems() {
      return this.libraries.length;
    },
    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage);
    },
    startIndex() {
      return (this.currentPage - 1) * this.itemsPerPage;
    },
    endIndex() {
      return Math.min(this.startIndex + this.itemsPerPage, this.totalItems);
    },
    paginatedLibraries() {
      return this.libraries.slice(this.startIndex, this.endIndex);
    }
  },
  methods: {
    goToLibrary(id) {
      this.$router.push(`/lessons/${id}`);
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    }
  }
};
</script>

<style scoped>
.library-list {
  padding: 24px;
  background: var(--background-color-1);
  border-radius: 8px;
}

.list-header {
  margin-bottom: 24px;
}

.list-header h1 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
}

.subtitle {
  color: var(--text-color-secondary);
  font-size: 14px;
}

.list-table {
  width: 100%;
}

.table-header {
  display: grid;
  grid-template-columns: 80px 2fr 1fr 1fr 1fr 48px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-color-secondary);
  font-size: 14px;
}

.library-item {
  display: grid;
  grid-template-columns: 80px 2fr 1fr 1fr 1fr 48px;
  padding: 12px 16px;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.library-item:hover {
  background-color: var(--background-color-2);
}

.thumbnail {
  width: 48px;
  height: 48px;
  border-radius: 6px;
  background-size: cover;
  background-position: center;
  background-color: var(--background-color-2);
}

.col-name h3 {
  font-size: 14px;
  font-weight: 500;
}

.status-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  background-color: var(--success-color-bg);
  color: var(--success-color);
  font-size: 12px;
  font-weight: 500;
}

.col-stats {
  display: flex;
  gap: 12px;
}

.stat {
  font-size: 14px;
  color: var(--text-color-secondary);
}

.col-date {
  font-size: 14px;
  color: var(--text-color-secondary);
}

.action-btn {
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  color: var(--text-color-secondary);
  cursor: pointer;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background-color: var(--background-color-3);
}.pagination {
  margin-top: 20px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--border-color);
}

.pagination-info {
  color: var(--text-color-secondary);
  font-size: 14px;
}

.pagination-controls {
  display: flex;
  gap: 8px;
}

.pagination-btn {
  padding: 6px 12px;
  border: 1px solid var(--border-color);
  background: var(--background-color-1);
  color: var(--text-color);
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: var(--background-color-2);
  border-color: var(--text-color-secondary);
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}


</style>