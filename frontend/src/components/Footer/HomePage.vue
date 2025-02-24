<template>
  <div class="landing-container">
    <div class="landing-page-1">
      <div class="landing-titles-container">
        <div class="landing-title">Learn Anything!</div>
        <div class="landing-subtitle">Where Curious Minds Play to Learn.</div>
      </div>
    </div>
    <div class="landing-page-2">
      <div class="features-container">
        <FeaturesComponent />
    </div>
    <FeatureGrid />
      <div class="cta-container" @click="redirectLogin">
        <CtaButton />
      </div>
      <div class="buttons">
        <div
          v-for="(item, index) in items"
          :key="index"
          :class="{ 'button-active': activeIndex === index }"
          class="button"
          @click="setActiveIndex(index)"
        >
          {{ item }}
        </div>
      </div>
      <transition name="fade" mode="out-in">
        <div v-if="4===2+2">
        <div class="value-content" v-if="activeIndex === 0" key="content-0">
          <div class="value-explainer">Your personal learning journey.</div>
          <div class="value-text">
            <b>You</b> decide what to learn. Choose any topic you can describe in a few words.
            Or let our tutor suggest based on your goals and interests.
          </div>
        </div>
        <div class="value-content" v-if="activeIndex === 1" key="content-1">
          <div class="value-explainer">Learn anything, challenge yourself.</div>
          <div class="value-text">
            Embark on a personalized learning adventure with interactive lessons
            and fun quizzes.
          </div>
        </div>
        <div class="value-content" v-if="activeIndex === 2" key="content-2">
          <div class="value-explainer">Stats, graphs, streaks...</div>
          <div class="value-text">
            Seeing progress gives us the rewarding feeling hard work deserves.
            Track your gains with graphs and stats.
          </div>
        </div>
        </div>
      </transition>
      <img :src="openaiPath" alt="Powered by OpenAI" class="openai" />
      <div class="faq-container">
        <FaqComponent />
      </div>
    </div>
  </div>
</template>

<script>
import { usePopupStore } from "@/store/popupStore";
import { useThemeStore } from "@/store/themeStore";
import { useAuthStore } from "@/store/authStore";
import CtaButton from "./LandingPageComponents/CtaButton.vue";
import FaqComponent from "./LandingPageComponents/FaqComponent.vue";
import FeatureGrid from "./LandingPageComponents/FeatureGrid.vue";
// import SharedContent from "./LandingPageComponents/SharedContent.vue";
import FeaturesComponent from "./LandingPageComponents/FeaturesComponent.vue";

export default {
  name: "HomePage",
  components: {
    CtaButton,
    FaqComponent,
    // SharedContent,
    FeatureGrid,
    FeaturesComponent,
  },
  data() {
    return {
      items: ["Have Fun", "Discover", "Level Up"],
      activeIndex: 0,
      popupMessage: "",
    };
  },
  created() {
    const messageCode = this.$route.query.message;
    this.handleMessageCode(messageCode);
    this.interval = setInterval(this.rotateActiveIndex, 6000);
  },
  computed: {
    openaiPath() {
      const themeStore = useThemeStore();
      return themeStore.darkMode
        ? require("@/assets/images/powered-by-openai-badge-outlined-on-light.svg")
        : require("@/assets/images/powered-by-openai-badge-outlined-on-dark.svg");
    },
  },
  methods: {
    handleMessageCode(code) {
      const messages = {
        expired_registration_token:
          "This registration token was expired. A new one has been sent to your email.",
        invalid_registration_token:
          "The registration token you provided is invalid. Please check your email for the correct link or contact support.",
      };
      this.popupMessage = messages[code] || "";
      if (this.popupMessage != "") {
        const popupStore = usePopupStore();
        popupStore.showPopup(this.popupMessage);
      }
    },
    redirectLogin() {
      const authStore = useAuthStore();
      if (authStore.loggedIn) {
        this.$router.push("/library");
      }
      else{
        this.$router.push("/login");
      }
    },
    setActiveIndex(index) {
      this.activeIndex = index;
    },
    rotateActiveIndex() {
      this.activeIndex = (this.activeIndex + 1) % this.items.length;
    },
    observeFeatures() {
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
    },
    // observeStatInfos() {
    //   const observer = new IntersectionObserver(
    //     (entries, observer) => {
    //       entries.forEach((entry) => {
    //         if (entry.isIntersecting) {
    //           entry.target.classList.add("visible");
    //           observer.unobserve(entry.target);
    //         }
    //       });
    //     },
    //     {
    //       threshold: 1,
    //     }
    //   );

    //   const stats = document.querySelectorAll(".stat-info");
    //   stats.forEach((stat) => {
    //     observer.observe(stat);
    //   });
    // },
  },
  mounted() {
    // this.observeStatInfos();
    this.observeFeatures();
  },
  beforeUnmount() {
    clearInterval(this.interval);
  },
};
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

.cta-container {
  margin-top: 2em;
  margin-bottom: 2em;

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

.features-container {
  display: flex;
  justify-content: center;
}

.faq-container {
  z-index: 1;
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
    font-size: 0.8em;
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
</style>
