<template>

<div class="section-card">
    <div class="card-header">
        <h2 class="section-title">Course Structure</h2>
        <p class="section-description text-lg">Organize your course into topics and subtopics</p>
    </div>

    <!-- Example Structure -->
    <div class="example-card">
        <div class="example-header">Example Structure</div>
        <div class="example-content">
            <div class="example-topic">
                <strong>Topic:</strong> "Cell Biology"
                <div class="example-subtopics">
                    <strong>Subtopics:</strong> "Cell Membrane", "Mitochondria", "Nucleus"
                </div>
            </div>
        </div>
    </div>

    <!-- Topics List -->
    <div class="topics-list">
        <div v-for="(group, groupIndex) in groups" :key="groupIndex" class="topic-card">
            <div class="topic-header">
                <input type="text" v-model="group.concept" placeholder="Enter a concept" />
                <button class="remove-topic-btn" @click="removeGroup(groupIndex)"
                    type="button">✕</button>
            </div>


            <div class="subtopics-section">
                <div v-if="group.childConcepts.length > 0" class="subtopics-list">
                    <div v-for="(section, sectionIndex) in group.childConcepts"
                        :key="sectionIndex" class="subtopic-item">
                        <input type="text" v-model="group.childConcepts[sectionIndex]"
                            placeholder="Enter subtopic name..." maxlength="40"
                            class="subtopic-input" />
                        <button class="remove-subtopic-btn"
                            @click="removeSection(groupIndex, sectionIndex)"
                            type="button">✕</button>
                    </div>
                </div>

                <button class="add-subtopic-btn" @click="addSection(groupIndex)" type="button">
                    + Add Subtopic
                </button>

            </div>
        </div>

        <!-- Add Topic Button -->
        <button class="add-topic-btn" @click="addGroup" type="button">
            + Add Topic
        </button>
    </div>

</div>
</template>

<script setup lang="ts">

import { ref } from 'vue';

interface childConcept {
    name: string;
    description?: string;
}

interface Concept {
    concept: string;
    description: string;
    childConcepts: childConcept[];
}


const groups = ref<Concept[]>(
    [{
        concept: "",
        description: "",
        childConcepts: [],
    }]
);

const removeGroup = (groupIndex: number) => {
    groups.value.splice(groupIndex, 1);
};

const removeSection = (groupIndex: number, sectionIndex: number) => {
    groups.value[groupIndex].childConcepts.splice(sectionIndex, 1);
};

const addSection = (groupIndex: number) => {
    const group = groups.value[groupIndex];
        group.childConcepts.push({ name: "", description: "" });
};

const addGroup = () => {
        groups.value.push({
            concept: "",
            childConcepts: [],
            description: "",
        });
};

</script>


<style scoped>
.section-card {
    flex: 1;
    background: rgba(26, 139, 127, 0.05);
    border-radius: 16px;
    padding: 2rem;
    border: 1px solid rgba(26, 139, 127, 0.1);
    display: flex;
    flex-direction: column;
    min-height: 500px;
    justify-content: space-between;
    width: 100%;
    /* Ensure full width */
}
.section-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: var(--text-color);
}
.section-description {
    color: var(--text-color-secondary);
    margin: 0;
}
.example-card {
    background: rgba(26, 139, 127, 0.1);
    border: 1px solid rgba(26, 139, 127, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    flex-shrink: 0;
}
.example-header {
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--color-primary);
}
.example-topic {
    color: var(--text-color);
}

.example-subtopics {
    margin-left: 1rem;
    margin-top: 0.5rem;
    color: var(--text-color-secondary);
}
.topics-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    flex: 1;
}
.topic-card {
    background: var(--background-color-1);
    border: 1px solid rgba(26, 139, 127, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    flex: 1;
}
.topic-header {
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    margin-bottom: 1rem;
}
.remove-topic-btn {
    background: none;
    border: none;
    color: var(--text-color-secondary);
    cursor: pointer;
    padding: 0.75rem;
    border-radius: 6px;
    transition: all 0.2s;
}

.remove-topic-btn:hover {
    color: var(--error-color);
    background: rgba(255, 0, 0, 0.1);
}

.subtopics-section {
    flex: 1;
    display: flex;
    flex-direction: column;
}
.subtopics-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 1rem;
    flex: 1;
}
.subtopic-item {
    display: flex;
    gap: 0.5rem;
    align-items: center;
}

.subtopic-input {
    flex: 1;
    padding: 0.625rem;
    border: 1px solid rgba(26, 139, 127, 0.3);
    border-radius: 6px;
    background: rgba(26, 139, 127, 0.1);
    color: var(--text-color);
}

.subtopic-input:focus {
    outline: none;
    border-color: var(--color-primary);
}
.add-subtopic-btn {
    width: 100%;
    padding: 0.75rem;
    border: 1px dashed rgba(26, 139, 127, 0.5);
    border-radius: 8px;
    background: transparent;
    color: var(--color-primary);
    cursor: pointer;
    transition: all 0.2s;
    margin-top: auto;
}

.add-subtopic-btn:hover:not(:disabled) {
    background: rgba(26, 139, 127, 0.1);
    border-style: solid;
}

.add-subtopic-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
.add-topic-btn {
    width: 100%;
    padding: 2rem;
    border: 2px dashed rgba(26, 139, 127, 0.3);
    border-radius: 12px;
    background: transparent;
    color: var(--text-color-secondary);
    cursor: pointer;
    font-size: 1.1rem;
    transition: all 0.2s;
    margin-top: auto;
}

.add-topic-btn:hover:not(:disabled) {
    color: var(--color-primary);
    border-color: var(--color-primary);
    background: rgba(26, 139, 127, 0.05);
}

.add-topic-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}

</style>