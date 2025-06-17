<template>
<div class="section-card">
    <h2 class="section-title text-3xl">{{title}}</h2>
    <p class="section-description text-2xl pt-2 pb-4">Recall as many terms and concepts about {{title}} as you remember!</p>

    <!-- Example Structure -->
    <div class="example-card mt-8">
        <div class="example-header">Example
            <div class="example-topic pt-4">Mitosis
                <div class="example-description">
                    Mitosis is the process by which a single cell divides to produce two genetically identical diploid daughter cells. It's essential for growth, repair, and asexual reproduction in multicellular organisms.
                </div>
                <div class="example-subtopics">
                    <div class="example-child-concept">
                        <strong>Stages of Mitosis:</strong> Prophase, Prometaphase, Metaphase, Anaphase, Telophase
                    </div>
                    <div class="example-child-concept">
                        <strong>Cytokinesis:</strong> The cell divides into two identical daughter cells.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Topics List -->
    <div class="topics-list">
        <div v-for="(concept, conceptIndex) in concepts" :key="conceptIndex" class="topic-card">
            <div class="concept-header">
                <input type="text" v-model="concept.concept" placeholder="Enter title" class="concept-title-input" />
                <button class="collapse-concept-btn" @click="toggleCollapse(conceptIndex)" type="button">
                    {{ concept.collapsed ? 'Expand' : 'Collapse' }}
                </button>
                <button class="remove-concept-btn" @click="removeGroup(conceptIndex)" type="button">✕</button>
            </div>

            <div v-show="!concept.collapsed">
                <div class="concept-description-section">
                    <textarea 
                        v-model="concept.description" 
                        placeholder="Enter description..." 
                        class="concept-description-input"
                        rows="3"
                    ></textarea>
                </div>

                <div class="child-concepts-section">
                    <h4 v-if="concept.childConcepts.length > 0" class="child-concepts-header pl-4">Child Concepts:</h4>
                    
                    <div v-if="concept.childConcepts.length > 0" class="child-concepts-list">
                        <div v-for="(childConcept, childIndex) in concept.childConcepts"
                            :key="childIndex" class="child-concept-item mx-4 mb-4">
                            <div class="child-concept-header text-lg">
                                <input type="text" 
                                    v-model="childConcept.name"
                                    placeholder="Child concept title..." 
                                    class="child-concept-title-input font-bold" />
                                <button class="remove-child-concept-btn"
                                    @click="removeSection(conceptIndex, childIndex)"
                                    type="button">✕</button>
                            </div>
                            <textarea 
                                v-model="childConcept.description" 
                                placeholder="Child concept description..." 
                                class="child-concept-description-input"
                                rows="2"
                            ></textarea>
                        </div>
                    </div>

                    <button class="add-child-concept-btn" @click="addSection(conceptIndex)" type="button">
                        + Add Sub-term / Sub-concept
                    </button>
                </div>
            </div>
        </div>

        <!-- Add Topic Button -->
        <button class="add-topic-btn" @click="addConcept" type="button">
            + Add Term / Concept
        </button>
    </div>

    
</div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const title = ref<string>(''); // Define the title property

interface childConcept {
    name: string;
    description?: string;
}

interface Concept {
    concept: string;
    description: string;
    childConcepts: childConcept[];
    collapsed: boolean;
}

const concepts = ref<Concept[]>([{
    concept: "",
    description: "",
    childConcepts: [],
    collapsed: false,
}]);

const removeGroup = (groupIndex: number) => {
    concepts.value.splice(groupIndex, 1);
};

const removeSection = (groupIndex: number, sectionIndex: number) => {
    concepts.value[groupIndex].childConcepts.splice(sectionIndex, 1);
};

const addSection = (groupIndex: number) => {
    const group = concepts.value[groupIndex];
    group.childConcepts.push({ name: "", description: "" });
};

const addConcept = () => {
    concepts.value.push({
        concept: "",
        childConcepts: [],
        description: "",
        collapsed: false,
    });
};

const toggleCollapse = (groupIndex: number) => {
    concepts.value[groupIndex].collapsed = !concepts.value[groupIndex].collapsed;
};

const props = defineProps<{
    title: string;
}>();

onMounted(() => {
    if (props.title) {
        title.value = props.title;
    }
    else {
        router.back();
    }
});
</script>

<style scoped>
.section-card {
    background: rgba(26, 139, 127, 0.05);
    border-radius: 16px;
    padding: 2rem;
    border: 1px solid rgba(26, 139, 127, 0.1);
    display: flex;
    flex-direction: column;
    min-height: 500px;
    justify-content: space-between;
    width: 80%;
    max-width: 1200px;
    margin: 0 auto;
}

.section-title {
    justify-content: center;
    display: flex;
    font-weight: bold;
    margin-bottom: 0.5rem;
    color: var(--text-color);
}

.section-description {
    color: var(--text-color-secondary);
    margin: 0;
    justify-content: center;
    display: flex;
}

.example-card {
    background: rgba(26, 139, 127, 0.1);
    border: 1px solid rgba(26, 139, 127, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
}

.example-header {
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--color-primary);
}

.example-topic {
    color: var(--text-color);
    font-weight: 600;
}

.example-description {
    margin: 0.5rem 0 1rem 0;
    color: var(--text-color-secondary);
    font-size: 0.95rem;
    line-height: 1.4;
}

.example-subtopics {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.example-child-concept {
    color: var(--text-color-secondary);
    font-size: 0.9rem;
    line-height: 1.3;
    padding-left: 1rem;
    border-left: 2px solid rgba(26, 139, 127, 0.3);
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

.concept-header {
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    margin-bottom: 1rem;
}

.concept-title-input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid rgba(26, 139, 127, 0.3);
    border-radius: 8px;
    background: rgba(26, 139, 127, 0.1);
    color: var(--text-color);
    font-size: 17px;
    font-weight: 600;
}

.concept-title-input:focus {
    outline: none;
    border-color: var(--color-primary);
}

.concept-description-section {
    margin-bottom: 1.5rem;
}

.concept-description-input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid rgba(26, 139, 127, 0.3);
    border-radius: 8px;
    background: rgba(26, 139, 127, 0.1);
    color: var(--text-color);
    resize: vertical;
    min-height: 80px;
}

.concept-description-input:focus {
    outline: none;
    border-color: var(--color-primary);
}

.child-concepts-section {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.child-concepts-header {
    margin-bottom: 1rem;
    color: var(--text-color);
    font-size: 1rem;
    font-weight: 600;
}

.child-concepts-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1rem;
}

.child-concept-item {
    background: rgba(26, 139, 127, 0.05);
    border: 1px solid rgba(26, 139, 127, 0.15);
    border-radius: 8px;
    padding: 1.25rem;
}

.child-concept-header {
    display: flex;
    gap: 0.5rem;
    align-items: flex-start;
    margin-bottom: 0.75rem;
}

.child-concept-title-input {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid rgba(26, 139, 127, 0.3);
    border-radius: 6px;
    background: rgba(26, 139, 127, 0.1);
    color: var(--text-color);
    font-size: 16px;
}

.child-concept-title-input:focus {
    outline: none;
    border-color: var(--color-primary);
}

.child-concept-description-input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid rgba(26, 139, 127, 0.3);
    border-radius: 6px;
    background: rgba(26, 139, 127, 0.1);
    color: var(--text-color);
    resize: vertical;
    min-height: 60px;
    font-size: 16px;
}

.child-concept-description-input:focus {
    outline: none;
    border-color: var(--color-primary);
}

.remove-concept-btn, .remove-child-concept-btn {
    background: none;
    border: none;
    color: var(--text-color-secondary);
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 6px;
    transition: all 0.2s;
}

.remove-concept-btn:hover, .remove-child-concept-btn:hover {
    color: var(--error-color);
    background: rgba(255, 0, 0, 0.1);
}

.add-child-concept-btn {
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

.add-child-concept-btn:hover:not(:disabled) {
    background: rgba(26, 139, 127, 0.1);
    border-style: solid;
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

.collapse-concept-btn {
    background: none;
    border: none;
    color: var(--text-color-secondary);
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 6px;
    transition: all 0.2s;
}

.collapse-concept-btn:hover {
    color: var(--color-primary);
    background: rgba(26, 139, 127, 0.1);
}

</style>