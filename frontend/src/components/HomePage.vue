<template>
    <div class="landing-container">
        <div class="landing-page-1">
            <div class="landing-titles-container">
                <div class="landing-title">Studying. Made. Fun.</div>
                <div class="landing-subtitle">
  Stop cramming alone the night before. Join a community where studying feels like leveling up, not burning out.
</div>
            </div>
        </div>
        <div class="landing-page-2">
            <div class="features-container1">
                <FeaturesComponent />
            </div>
            <div class="search-bar-container">
                <input type="text" class="search-input" v-model="searchQuery" @keyup.enter="handleSearch" placeholder="Search courses..." />
                <button @click="handleSearch" class="search-button">Start Learning Now</button>
            </div>
            <div class="dropdown-menus">
                <div v-for="(item, index) in items" :key="index" class="dropdown">
                    <button @click="toggleDropdown(index)" class="dropdown-button"
                        :class="{ 'active': activeDropdown === index }">
                        {{ item }}
                        <span class="dropdown-arrow">▼</span>
                    </button>
                    <div class="value-content" v-if="activeIndex === index" key="content-0">
                        <div v-html="content[index][0]" class="value-explainer"></div>
                        <div v-html="content[index][1]" class="value-text">
                        </div>
                    </div>
                </div>
            </div>

            <!-- UNCOMMENT for launch -->
            <!-- <div class="why-this-matters">
                <h2>Why Rivue</h2>
                <blockquote>
                    “When I started college, I felt alone, overwhelmed, and my grades showed it.
                    Studying felt impossible, boring, and isolating.
                    <strong>I built this tool because I believe studying doesn't have to feel like punishment—it should
                        feel like play.</strong>
                    Here, you’re not just improving your grades; you’re discovering friends, finding community, and
                    finally feeling like you belong.” - Founder
                </blockquote>
            </div> -->

            <div class="social-links-container">
                <h3>Connect With Us</h3>
                <div class="social-links">
                    <a href="https://x.com/Rivueai" target="_blank" rel="noopener noreferrer" class="social-link">
                        <img :src="require('@/assets/images/x-logo-white.png')" alt="X (Twitter)" class="social-icon" />
                        <span>Follow us on X</span>
                    </a>
                    <a href="https://discord.gg/33yAcp2qDf" target="_blank" rel="noopener noreferrer"
                        class="social-link">
                        <img :src="require('@/assets/images/discord-mark-white.png')" alt="Discord"
                            class="social-icon" />
                        <span>Join our Discord</span>
                    </a>
                </div>
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from "@/store/authStore";
import FeaturesComponent from "./Footer/LandingPageComponents/FeaturesComponent.vue";
const searchQuery = ref("");

// Component name is automatically inferred from the filename when using <script setup>

// Data properties
const items = ref(["Have Fun", "Discover", "Level Up"]);
const content = ref([
  [
    "Make learning feel like a game.",
    "Set goals, earn achievements, and compete with friends — or just with yourself. Studying doesn’t have to suck."
  ],
  [
    "Explore courses that match your curiosity.",
    "Search for anything — from ‘intro to calculus’ to ‘the mitochondria is the powerhouse’ — or join courses made by your peers."
  ],
  [
    "Track progress that actually motivates you.",
    "Visualize your streaks, XP, and personal growth over time. Every session builds momentum."
  ]
]);
const activeIndex = ref<number | null>(null);
const activeDropdown = ref<number | null>(null);

// Route and router
const router = useRouter();

// Store instances
const authStore = useAuthStore();

const handleSearch = () => {
    if (searchQuery.value.trim() !== "") {
        router.push({
            path: '/explore',
            query: { search: searchQuery.value } // Pass as state
        });
    }
};

const redirectLogin = () => {
    if (authStore.loggedIn) {
        router.push("/create");
    } else {
        router.push("/login");
    }
};

const toggleDropdown = (index: number) => {
    if (activeDropdown.value === index) {
        activeDropdown.value = null;
        activeIndex.value = null;
    } else {
        activeDropdown.value = index;
        activeIndex.value = index;
    }
};

const observeFeatures = () => {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 1,
        }
    );

    const features = document.querySelectorAll(".feature");
    features.forEach((feature) => observer.observe(feature));
};

// Mounted lifecycle hook
onMounted(() => {
    observeFeatures();
});
</script>

<style scoped>
/* Add these to your existing <style> section */

body {
    background-color: var(--background-color);
    color: var(--text-color);
}

.landing-title {
    color: var(--light-text);
    font-weight: 800;
    text-shadow: 2px 2px 4px rgba(0, 172, 193, 0.1);
}

.landing-subtitle {
    color: var(--element-color-1);
    font-weight: 600;
}

.feature-card {
    background: var(--feature-gradient);
    border: 2px solid rgba(38, 198, 218, 0.2);
    border-radius: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 172, 193, 0.1);
}

.feature-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 8px 15px rgba(0, 172, 193, 0.2);
}

.button {
    color: var(--element-color-1);
    font-weight: 600;
    transition: all 0.3s ease;
    position: relative;
    padding-bottom: 2px;
}

.button::after {
    content: '';
    position: absolute;
    width: 0;
    height: 2px;
    bottom: 0;
    left: 0;
    background-color: var(--element-color-2);
    transition: width 0.3s ease;
}

.button:hover::after {
    width: 100%;
}

.button-active {
    color: var(--highlight-color);
}

.button-active::after {
    width: 100%;
    background-color: var(--highlight-color);
}

.value-content {
    background: rgba(224, 242, 241, 0.5);
    border-radius: 12px;
    padding: 1.5em;
    border: 1px solid rgba(0, 172, 193, 0.2);
    box-shadow: 0 4px 6px rgba(0, 172, 193, 0.05);
}

.cta-button {
    background: var(--button-gradient);
    color: var(--light-text);
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 172, 193, 0.2);
}

.cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 172, 193, 0.3);
}

/* Additional styles for gamification */

.achievement-icon {
    color: var(--gold-color);
    font-size: 1.5em;
    margin-right: 0.5em;
}

.progress-bar {
    background-color: var(--background-color-2t);
    border-radius: 10px;
    height: 10px;
    overflow: hidden;
}

.progress-bar-fill {
    background-color: var(--element-color-2);
    height: 100%;
    transition: width 0.5s ease;
}

/* Animation for value content */
.fade-enter-active,
.fade-leave-active {
    transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(10px);
}

.landing-container {
    display: flex;
    flex-direction: column;
    max-width: 1024px;
    width: 100%;
}

.landing-titles-container {
    display: flex;
    flex-direction: column;
}

.landing-title {
    text-align: center;
    font-weight: 700;
    font-size: 4em;
    margin-top: 1.5em;
    color: var(--text-color);
}

.landing-subtitle {
    text-align: center;
    font-weight: 800;
    opacity: 0.9;
    font-size: 1.5em;
    margin: 0;
    margin-bottom: 3em;
    color: linear-gradient(to right, var(--text-color), var(--highlight-color));
}

.buttons {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
}

.button {
    display: inline-block;
    cursor: pointer;
    opacity: 0.4;
    margin-right: 10px;
    font-size: 1.6em;
    transition: opacity 0.3s ease;
}

.button-active {
    opacity: 1;
}

.value-content {
    height: 7em;
    font-size: 1.2em;
    padding-right: 35%;
}

.value-explainer {
    font-size: 1.2em;
    font-weight: 700;
    margin-bottom: 0.2em;
}

.value-text {
    font-size: 1em;
    opacity: 0.85;
}


.search-bar-container {
    display: flex;
    justify-content: center;
    align-items: stretch; /* Change from center to stretch */
    margin: 2em 0;
    padding: 0 1em;
    flex-wrap: wrap; /* Add this to allow wrapping on very small screens */
    gap: 10px; /* Add gap for when items wrap */
}

.search-input {
    width: 70%;
    max-width: 500px;
    padding: 15px 20px;
    font-size: 19px;
    border: 2px solid var(--element-color-1);
    border-radius: 30px 0 0 30px;
    outline: none;
    background-color: var(--background-color);
    color: var(--text-color);
    transition: border-color 0.3s ease;
    flex: 1; /* Add this to allow input to grow */
    min-width: 200px; /* Add minimum width */
}

.search-input:focus {
    border-color: var(--highlight-color);
    /* Highlight border on focus */
}

.search-button {
    padding: 15px 25px;
    font-size: 1.2em;
    background-color: var(--element-color-1);
    color: var(--background-color);
    border: 2px solid var(--element-color-1);
    border-left: none;
    border-radius: 0 30px 30px 0;
    cursor: pointer;
    transition: all 0.3s ease;
    white-space: nowrap; /* Prevent button text from wrapping */
}

.search-button:hover {
    background-color: var(--highlight-color);
    border-color: var(--highlight-color);
    color: var(--light-text);
    /* Change text color on hover for better contrast */
}


/* Responsive adjustments for search bar */
@media only screen and (max-width: 600px) {
    .search-input {
        font-size: 1em;
        /* Adjust font size for smaller screens */
        padding: 12px 15px;
    }

    .search-button {
        font-size: 1em;
        /* Adjust font size for smaller screens */
        padding: 12px 20px;
    }
}

.stat-infos {
    padding: 0.5em;
    text-align: center;
}

.shared-content {
    display: flex;
    justify-content: center;
}

.stat-info {
    font-size: 1.2em;
    font-weight: 700;
    margin-top: 1em;
    margin: 0.5em;
    opacity: 0;
    transform: translateY(20px);
}

.stat-info.visible {
    animation: fadeSlideIn 0.8s ease-out forwards;
}

.landing-page-1 {
    display: flex;
    justify-content: center;
    flex-direction: column;
}

.landing-page-2 {
    padding: 2em;
    display: flex;
    justify-content: center;
    flex-direction: column;
}

.features-container1 {
    display: flex;
    justify-content: center;
}

.openai {
    margin: 0 auto;
    padding: 64px 25%;
    max-height: 212px;
}

.small-text {
    font-weight: 700;
    font-size: 0.8em;
    opacity: 0.6;
    margin-top: 0.5em;
    margin-bottom: 1em;
}

/* media */
@media only screen and (max-width: 740px) {
    .value-content {
        height: 7em;
        padding-right: 20%;
    }


    .value-text {
        font-size: 0.7em;
    }

}

@media only screen and (max-width: 600px) {
    .landing-title {
        font-size: 3em;
    }

    .landing-subtitle {
        font-size: 1.3em;
    }

    .value-content {
        height: 8em;
        padding-right: 20%;
    }

    .value-explainer {
        font-size: 1em;
    }

    .value-text {
        font-size: 0.7em;
    }

    .openai {
        padding: 48px 20%;
    }
}

@media only screen and (max-width: 440px) {
    .landing-title {
        font-weight: 700;
        font-size: 2.5em;
    }

    .landing-page-2 {
        padding: 1em;
    }

    .value-content {
        height: 9em;
        padding: 0;
    }

    .button {
        font-size: 1.3em;
    }

    .openai {
        padding: 32px 15%;
    }
}

@media only screen and (max-width: 350px) {
    .landing-title {
        font-size: 2em;
    }

    .landing-subtitle {
        font-size: 1.1em;
    }
}
@media only screen and (max-width: 600px) {
    .search-bar-container {
        flex-direction: column; /* Stack items on very small screens */
    }
    
    .search-input {
        width: 100%; /* Full width on small screens */
        border-radius: 30px; /* Full rounded corners when stacked */
    }
    
    .search-button {
        width: 100%; /* Full width on small screens */
        border-radius: 30px; /* Full rounded corners when stacked */
        border-left: 2px solid var(--element-color-1); /* Restore left border when stacked */
    }
}

@media only screen and (max-height: 700px) {
    .landing-title {
        margin: 0;
    }

    .button {
        font-size: 1.5em;
    }
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}

@keyframes fadeSlideIn {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Add these to your existing <style> section */

.landing-title {
    background: linear-gradient(120deg, var(--text-color), var(--text-color));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 30px rgba(216, 180, 254, 0.1);
}

.landing-subtitle {
    color: var(--text-color);
    opacity: 0.9;
    text-shadow: 0 0 20px rgba(216, 180, 254, 0.1);
}

.feature-card {
    background: var(--feature-gradient);
    border: 1px solid rgba(124, 58, 237, 0.1);
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(124, 58, 237, 0.15);
}

.button {
    position: relative;
    color: var(--text-color);
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.button-active {
    opacity: 1;
    color: var(--highlight-color);
}

.button:hover {
    transform: translateX(5px);
}

.value-content {
    background: rgba(109, 40, 217, 0.05);
    border-radius: 12px;
    padding: 1.5em;
    border: 1px solid rgba(124, 58, 237, 0.1);
}

.cta-button {
    background: var(--button-gradient);
    border: none;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(124, 58, 237, 0.3);
}


.dropdown-menus {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 2rem;
}

.dropdown {
    position: relative;
}

.dropdown-button {
    width: 100%;
    padding: 1rem;
    font-size: 1.2rem;
    font-weight: 600;
    text-align: left;
    background-color: var(--background-color);
    color: var(--text-color);
    border: 1px solid var(--element-color-1);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.dropdown-button:hover,
.dropdown-button.active {
    background-color: var(--element-color-1);
    color: var(--background-color);
}

.dropdown-arrow {
    float: right;
    transition: transform 0.3s ease;
}

.dropdown-button.active .dropdown-arrow {
    transform: rotate(180deg);
}

.dropdown-content {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    padding: 1rem;
    background-color: var(--background-color);
    border: 1px solid var(--element-color-1);
    border-top: none;
    border-radius: 0 0 8px 8px;
    z-index: 1;
}

.dropdown-content h3 {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.dropdown-content p {
    font-size: 1rem;
    color: var(--text-color);
    opacity: 0.9;
}

.social-links-container {
    margin: 2rem auto;
    padding: 1.5rem;
    text-align: center;
    width: 100%;
    max-width: 800px;
}

.social-links-container h3 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    color: var(--text-color);
}

.social-links {
    display: flex;
    justify-content: center;
    gap: 2rem;
    flex-wrap: wrap;
}

.social-link {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: var(--text-color);
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    transition: all 0.3s ease;
    border: 1px solid var(--element-color-1);
}

.social-link:hover {
    background-color: var(--element-color-1);
    color: var(--background-color);
    transform: translateY(-2px);
}

.social-icon {
    width: 24px;
    height: 24px;
    margin-right: 0.75rem;
}

.social-link span {
    font-weight: 500;
}

/* Responsive adjustments */
@media only screen and (max-width: 600px) {
    .social-links {
        flex-direction: column;
        gap: 1rem;
    }

    .social-link {
        width: 100%;
        justify-content: center;
    }
}

.why-this-matters {
    background: var(--background-color-2t);
    padding: 2rem;
    margin: 2rem 0;
    border-radius: 8px;
    text-align: center;
}

.why-this-matters h2 {
    margin-bottom: 1rem;
    font-size: 1.5rem;
    font-weight: 700;
}

.why-this-matters blockquote {
    font-style: italic;
    line-height: 1.6;
    color: var(--text-color-muted);
}
</style>