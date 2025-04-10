<template>
    <div class="changelog-container">
        <h1 class="changelog-title">Changelog</h1>
        <p class="changelog-subtitle">See what's new, improved, or fixed in Rivue!</p>

        <div class="changelog-entry" v-for="(entry, index) in changelog" :key="index">
            <div class="changelog-date">{{ entry.date }}</div>
            <div class="changelog-content">
                <ul>
                    <li v-for="(item, i) in entry.items" :key="i">• {{ item }}</li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "ChangelogPage",
    data() {
        return {
            changelog: [
                {
                    date: "April 10, 2025",
                    items: [
                        "Added password reset ability",
                    ],
                },
                {
                    date: "April 5, 2025",
                    items: [
                        "Fixed mobile viewing on Course Selection page and Learning Path page"
                    ],
                },
                {
                    date: "April 2, 2025",
                    items: [
                        "Added ability to add multiple new rooms with \"Add New Stepping Stones\" button"
                    ],
                },
                {

                    date: "March 26, 2025",
                    items: [
                        "Added a database",
                        "Added this changelog"
                    ],
                },
                {
                    date: "March 24, 2025",
                    items: [
                        "Deployment now live",
                    ],
                },
            ],
        };
    },
};
</script>

<style scoped>
.changelog-container {
    max-width: 700px;
    margin: 3rem auto;
    padding: 1.5rem;
    background: var(--background-color, #fff);
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.changelog-title {
    font-size: 2rem;
    font-weight: bold;
    color: var(--text-color, #222);
    margin-bottom: 0.5rem;
    text-align: center;
}

.changelog-subtitle {
    font-size: 1rem;
    color: #888;
    text-align: center;
    margin-bottom: 2rem;
}

.changelog-entry {
    margin-bottom: 2rem;
}

.changelog-date {
    font-weight: 600;
    font-size: 1.1rem;
    color: var(--highlight-color, #4a90e2);
    margin-bottom: 0.5rem;
}

.changelog-content ul {
    list-style: none;
    padding-left: 0;
    color: var(--text-color, #333);
    line-height: 1.6;
}
</style>