<template>
    <div class="page-main-container">
        <h1 class="page-title">Knowledge Map🗺️{{ titleName }}</h1>

        <knowledge-graph/>
    </div>
</template>
    
<script>
import KnowledgeGraph from "../Graphs/KnowledgeGraph.vue";
import { practiceStore } from "@/store/practiceStore";

export default {
    name: "KnowledgePage",
    components: { KnowledgeGraph },
    data() {
        return {
            titleName: ''
        };
    },
    mounted() {
        this.titleName = practiceStore.state.titleName;
    }
};
</script>
    
<style scoped>

</style>