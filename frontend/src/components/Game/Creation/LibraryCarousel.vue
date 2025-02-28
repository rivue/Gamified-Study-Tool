<template>
    <div class="library-list">
      <div class="list-header">
        <h1>My Courses</h1>
        <p class="subtitle">Browse your courses and track your progress.</p>
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
          v-for="library in paginatedLibraries" 
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
      
      <div class="pagination" v-if="totalItems > 0">
        <div class="pagination-info">
          Showing {{ startIndex + 1 }}-{{ endIndex }} of {{ totalItems }} courses
        </div>
        <div class="pagination-controls">
          <button 
            class="pagination-btn" 
            :disabled="currentPage === 1"
            @click="prevPage"
          >
            <span class="pagination-icon">←</span> Prev
          </button>
          <div class="page-numbers">
            <button 
              v-for="page in displayedPages" 
              :key="page" 
              class="page-btn"
              :class="{ 'active': currentPage === page }"
              @click="goToPage(page)"
            >
              {{ page }}
            </button>
          </div>
          <button 
            class="pagination-btn" 
            :disabled="currentPage === totalPages"
            @click="nextPage"
          >
            Next <span class="pagination-icon">→</span>
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
    data() {
      return {
        currentPage: 1,
        itemsPerPage: 5
      };
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
      },
      displayedPages() {
        const range = [];
        const maxVisiblePages = 5;
        
        if (this.totalPages <= maxVisiblePages) {
          // Show all pages if there are few pages
          for (let i = 1; i <= this.totalPages; i++) {
            range.push(i);
          }
        } else {
          // Complex pagination for many pages
          let start = Math.max(1, this.currentPage - 2);
          let end = Math.min(this.totalPages, start + maxVisiblePages - 1);
          
          // Adjust start if needed to show maxVisiblePages
          if (end - start + 1 < maxVisiblePages) {
            start = Math.max(1, end - maxVisiblePages + 1);
          }
          
          for (let i = start; i <= end; i++) {
            range.push(i);
          }
        }
        
        return range;
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
      },
      goToPage(page) {
        this.currentPage = page;
      }
    }
  };
  </script>
  
  <style scoped>
  .library-list {
    padding: 24px;
    background: var(--background-color-1);
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  }
  
  .list-header {
    margin-bottom: 24px;
  }
  
  .list-header h1 {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 8px;
    color: var(--text-color);
  }
  
  .subtitle {
    color: var(--text-color-secondary);
    font-size: 16px;
  }
  
  .list-table {
    width: 100%;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid var(--border-color);
    margin-bottom: 16px;
  }
  
  .table-header {
    display: grid;
    grid-template-columns: 80px 2fr 1fr 1fr 1fr 48px;
    padding: 14px 16px;
    background-color: var(--background-color-2);
    border-bottom: 1px solid var(--border-color);
    color: var(--text-color-secondary);
    font-size: 14px;
    font-weight: 600;
  }
  
  .library-item {
    display: grid;
    grid-template-columns: 80px 2fr 1fr 1fr 1fr 48px;
    padding: 16px;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .library-item:last-child {
    border-bottom: none;
  }
  
  .library-item:hover {
    background-color: var(--element-color-1);
    transform: translateY(-2px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }
  
  .thumbnail {
    width: 56px;
    height: 56px;
    border-radius: 8px;
    background-size: cover;
    background-position: center;
    background-color: var(--element-color-1);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .col-name h3 {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-color);
    margin: 0;
  }
  
  .status-badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 16px;
    background-color: var(--success-color-bg);
    color: var(--success-color);
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.3px;
  }
  
  .col-stats {
    display: flex;
    gap: 16px;
  }
  
  .stat {
    font-size: 14px;
    color: var(--text-color-secondary);
    display: flex;
    align-items: center;
    font-weight: 500;
  }
  
  .col-date {
    font-size: 14px;
    color: var(--text-color-secondary);
  }
  
  .action-btn {
    width: 32px;
    height: 32px;
    border: none;
    background: transparent;
    color: var(--text-color-secondary);
    cursor: pointer;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    transition: all 0.2s ease;
  }
  
  .action-btn:hover {
    background-color: var(--background-color-3);
    color: var(--text-color);
  }
  
  .pagination {
    padding: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
  }
  
  .pagination-info {
    color: var(--text-color-secondary);
    font-size: 14px;
    font-weight: 500;
  }
  
  .pagination-controls {
    display: flex;
    gap: 8px;
    align-items: center;
  }
  
  .pagination-btn {
    padding: 8px 14px;
    border: 1px solid var(--border-color);
    background: var(--background-color-1);
    color: var(--text-color);
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  
  .pagination-btn:hover:not(:disabled) {
    background: var(--background-color-2);
    border-color: var(--text-color-secondary);
  }
  
  .pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .pagination-icon {
    font-size: 12px;
  }
  
  .page-numbers {
    display: flex;
    gap: 4px;
  }
  
  .page-btn {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    border: 1px solid var(--border-color);
    background: var(--background-color-1);
    color: var(--text-color);
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
  }
  
  .page-btn:hover {
    background: var(--background-color-2);
    border-color: var(--text-color-secondary);
  }
  
  .page-btn.active {
    background: var(--primary-color, #4361ee);
    color: white;
    border-color: var(--primary-color, #4361ee);
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(67, 97, 238, 0.3);
    transform: scale(1.05);
  }
  
  /* Fallback styles if CSS variables are not defined */
  :root {
    --background-color-1: #ffffff;
    --background-color-2: #f8f9fa;
    --background-color-3: #e9ecef;
    --text-color: #212529;
    --text-color-secondary: #6c757d;
    --border-color: #dee2e6;
    --success-color: #198754;
    --success-color-bg: rgba(25, 135, 84, 0.1);
    --primary-color: #4361ee;
  }
  </style>