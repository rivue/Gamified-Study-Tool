<template>
  <div class="birthday-overlay" role="dialog" aria-modal="true">
    <div class="background-glow"></div>
    <div class="starlit-sky">
      <span
        v-for="star in starfield"
        :key="`star-${star.id}`"
        class="sky-star"
        :style="{
          left: `${star.left}%`,
          top: `${star.top}%`,
          animationDelay: `${star.delay}s`,
          animationDuration: `${star.duration}s`,
          opacity: star.opacity
        }"
      ></span>
    </div>

    <div class="floating-confetti">
      <div
        v-for="piece in confettiPieces"
        :key="`confetti-${piece.id}`"
        class="confetti-piece"
        :style="{
          left: `${piece.left}%`,
          animationDelay: `${piece.delay}s`,
          animationDuration: `${piece.duration}s`,
          transform: `rotate(${piece.rotation}deg)`,
          background: piece.gradient
        }"
      ></div>
    </div>

    <div class="floating-balloons">
      <div
        v-for="balloon in balloons"
        :key="`balloon-${balloon.id}`"
        class="balloon"
        :style="{
          left: `${balloon.left}%`,
          animationDelay: `${balloon.delay}s`,
          animationDuration: `${balloon.duration}s`,
          background: balloon.background,
          boxShadow: balloon.shadow
        }"
      >
        <span>{{ balloon.emoji }}</span>
      </div>
    </div>

    <div class="content-card">

      <h1 class="headline">Happy Birthday favorite cousin</h1>
      <p class="side-note">PS: sorry I forgot the past 3 years :(</p>

      <section class="truck-parade">
        <h2>Truck</h2>
        <p class="truck-caption">I know you love your massive truck so that is what I put here</p>
        <div class="truck-highway">
          <div class="truck-asphalt"></div>
          <div class="truck-center-line"></div>
          <div
            v-for="light in truckLights"
            :key="`light-${light.id}`"
            class="truck-light"
            :style="{
              left: `${light.left}%`,
              animationDelay: `${light.delay}s`,
              background: light.color
            }"
          ></div>
          <div class="truck-rig">
            <div class="truck-cab">
              <div class="truck-window"></div>
              <div class="truck-flag">16</div>
            </div>
            <div class="truck-bed">
              <div class="truck-decal">KB</div>
            </div>
            <div class="truck-wheel front"></div>
            <div class="truck-wheel rear"></div>
            <div class="truck-headlight"></div>
            <div class="truck-tailglow"></div>
          </div>
        </div>
      </section>

      <section class="gratitude-notes">
        <h2>Love Letters From Your Study Crew</h2>
        <div class="note-row">
          <article
            v-for="note in appreciationNotes"
            :key="note.text"
            class="gratitude-note"
            :style="{ borderColor: note.accent }"
          >
            <span class="note-accent" :style="{ background: note.accent }"></span>
            <p>{{ note.text }}</p>
          </article>
        </div>
      </section>

      <footer class="closing">
        <button class="close-secondary" @click="closeSurprise">✨ Take Me To My Dashboard</button>
      </footer>
    </div>

    <div v-if="showFireworks" class="firework-field" aria-hidden="true">
      <div
        v-for="burst in fireworkBursts"
        :key="`firework-${burst.id}`"
        class="firework-burst"
        :style="{
          left: `${burst.left}%`,
          top: `${burst.top}%`,
          animationDelay: `${burst.delay}s`,
          background: `radial-gradient(circle, hsla(${burst.hue}, 95%, 75%, 1) 0%, transparent 60%)`
        }"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

const emit = defineEmits<{ (e: 'close'): void }>();

const confettiSeed = ref(0);
const balloonSeed = ref(0);
const starSeed = ref(0);
const truckLightSeed = ref(0);
const showFireworks = ref(false);
const fireworkBursts = ref<Array<{ id: number; left: number; top: number; delay: number; hue: number }>>([]);

const pseudoRandom = (seed: number, offset: number) => {
  const x = Math.sin(seed * 999 + offset * 13.37) * 43758.5453;
  return x - Math.floor(x);
};

const accentPalette = ['#ff4d6d', '#ff9f1c', '#ffd23f', '#59d9a3', '#845ef7', '#f77fbe', '#70d6ff'];

const confettiPieces = computed(() => {
  const seed = confettiSeed.value + 1;
  return Array.from({ length: 160 }, (_, index) => {
    const hueShift = pseudoRandom(seed, index) * 360;
    const secondaryHue = (hueShift + 60 + pseudoRandom(seed, index + 40) * 120) % 360;
    return {
      id: index,
      left: pseudoRandom(seed, index + 10) * 100,
      delay: pseudoRandom(seed, index + 20) * 4,
      duration: 6 + pseudoRandom(seed, index + 30) * 6,
      rotation: pseudoRandom(seed, index + 50) * 360,
      gradient: `linear-gradient(135deg, hsla(${hueShift}, 90%, 65%, 0.95), hsla(${secondaryHue}, 90%, 70%, 0.9))`
    };
  });
});

const balloons = computed(() => {
  const seed = balloonSeed.value + 7;
  const balloonEmojis = ['🎈', '🎉', '💖', '🌟', '🎂', '🪩'];
  return Array.from({ length: 12 }, (_, index) => {
    const emoji = balloonEmojis[Math.floor(pseudoRandom(seed, index) * balloonEmojis.length)];
    const hue = pseudoRandom(seed, index + 15) * 360;
    const saturation = 70 + pseudoRandom(seed, index + 25) * 20;
    const lightness = 65 + pseudoRandom(seed, index + 35) * 20;
    const highlight = (lightness + 20) % 100;
    return {
      id: index,
      left: 5 + pseudoRandom(seed, index + 5) * 90,
      delay: pseudoRandom(seed, index + 60) * 3,
      duration: 12 + pseudoRandom(seed, index + 70) * 8,
      background: `radial-gradient(circle at 30% 30%, hsla(${hue}, ${saturation}%, ${highlight}%, 0.95) 0%, hsla(${hue}, ${saturation}%, ${lightness}%, 0.9) 60%, hsla(${hue}, ${saturation}%, ${lightness - 10}%, 0.8) 100%)`,
      shadow: `0 0 20px hsla(${hue}, ${saturation}%, ${lightness + 5}%, 0.6)`,
      emoji
    };
  });
});

const starfield = computed(() => {
  const seed = starSeed.value + 3;
  return Array.from({ length: 80 }, (_, index) => ({
    id: index,
    left: pseudoRandom(seed, index) * 100,
    top: pseudoRandom(seed, index + 40) * 100,
    delay: pseudoRandom(seed, index + 60) * 5,
    duration: 5 + pseudoRandom(seed, index + 80) * 6,
    opacity: 0.4 + pseudoRandom(seed, index + 100) * 0.5
  }));
});

const truckLights = computed(() => {
  const seed = 42 + truckLightSeed.value;
  return Array.from({ length: 10 }, (_, index) => {
    const hue = (pseudoRandom(seed, index + 10) * 360 + 200) % 360;
    return {
      id: index,
      left: pseudoRandom(seed, index) * 100,
      delay: pseudoRandom(seed, index + 20) * 4,
      color: `radial-gradient(circle, hsla(${hue}, 85%, 65%, 0.9) 0%, rgba(0,0,0,0) 70%)`
    };
  });
});

const appreciationNotes = [
  {
    text: '“the sweetest birthday girl” - isabel.marryyy',
    accent: accentPalette[0]
  },
  {
    text: '“happy 16th pretty girl!!” - isabella_mw_',
    accent: accentPalette[5]
  },
  {
    text: '“Love this and you🩷🩷.” - its.anya27',
    accent: accentPalette[1]
  },
  {
    text: '“so pretty angel!!!.” - eabruner (aka not the favorite cousin)',
    accent: accentPalette[2]
  },
  {
    text: '“so cuteee” - samantha.kennedy1',
    accent: accentPalette[3]
  },
  {
    text: '“happy 16th gorgeous!!” - blakely_gracegomez',
    accent: accentPalette[4]
  },
  {
    text: '"“happiest 16th!"” - lauren.patterson27',
    accent: accentPalette[5]
  },
  {
    text: '“aw this is adorable” - also lauren.patterson27',
    accent: accentPalette[2]
  }
];

const milestoneAge = 16;
const birthdayChapter = milestoneAge;

const closeSurprise = () => {
  showFireworks.value = false;
  emit('close');
};

</script>

<style scoped>
.birthday-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: radial-gradient(circle at top, rgba(26, 20, 63, 0.95) 0%, rgba(10, 7, 26, 0.92) 50%, rgba(5, 4, 16, 0.96) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  color: #fff;
  font-family: 'Poppins', 'Avenir', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.background-glow {
  position: absolute;
  inset: -50vh;
  background: radial-gradient(circle at 30% 20%, rgba(255, 123, 182, 0.35) 0%, transparent 55%),
    radial-gradient(circle at 70% 30%, rgba(104, 221, 255, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 50% 80%, rgba(255, 214, 126, 0.28) 0%, transparent 60%);
  filter: blur(40px);
  animation: glowPulse 12s ease-in-out infinite;
}

@keyframes glowPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.7;
  }
  50% {
    transform: scale(1.05);
    opacity: 1;
  }
}

.starlit-sky {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.sky-star {
  position: absolute;
  width: 3px;
  height: 3px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  animation: starTwinkle linear infinite;
}

@keyframes starTwinkle {
  0%, 100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.8);
    opacity: 1;
  }
}

.floating-confetti {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.confetti-piece {
  position: absolute;
  top: -10vh;
  width: 14px;
  height: 28px;
  border-radius: 4px;
  animation-name: confettiRain;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

@keyframes confettiRain {
  0% {
    transform: translateY(-10vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  100% {
    transform: translateY(110vh) rotate(720deg);
    opacity: 0;
  }
}

.floating-balloons {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.balloon {
  position: absolute;
  bottom: -20vh;
  width: 70px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.9);
  animation-name: balloonFloat;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
}

.balloon::after {
  content: '';
  position: absolute;
  bottom: -35px;
  width: 2px;
  height: 40px;
  background: rgba(255, 255, 255, 0.6);
}

@keyframes balloonFloat {
  0% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-60vh) scale(1.05);
  }
  100% {
    transform: translateY(-120vh) scale(1.1);
  }
}

.content-card {
  position: relative;
  z-index: 2;
  max-width: 860px;
  width: 92vw;
  background: rgba(19, 16, 46, 0.82);
  backdrop-filter: blur(18px);
  border-radius: 32px;
  padding: 3.5rem 3rem 3rem;
  border: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.55);
  overflow-y: auto;
  max-height: calc(100vh - 6rem);
}

.headline {
  font-size: clamp(2.4rem, 3vw, 3.4rem);
  text-align: center;
  margin: 1rem auto 0.75rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  background: linear-gradient(120deg, #ffe066 0%, #ffa8d4 40%, #9be7ff 70%, #fff 100%);
  -webkit-background-clip: text;
  color: transparent;
  filter: drop-shadow(0 10px 25px rgba(255, 255, 255, 0.18));
}

.intro {
  text-align: center;
  font-size: 1.15rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.85);
  max-width: 650px;
}

.side-note {
  text-align: center;
  font-size: 1rem;
  color: rgba(255, 200, 220, 0.9);
  margin: 2rem auto 2.5rem;
  font-style: italic;
}

.gratitude-notes h2 {
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 1.6rem;
  text-align: center;
}

.truck-parade {
  margin: 3rem auto 2.5rem;
  max-width: 840px;
  text-align: center;
}

.truck-caption {
  max-width: 620px;
  margin: 0.5rem auto 2.2rem;
  color: rgba(255, 255, 255, 0.82);
  line-height: 1.7;
}

.truck-highway {
  position: relative;
  width: 100%;
  height: 220px;
  border-radius: 28px;
  overflow: hidden;
  background: linear-gradient(180deg, rgba(30, 28, 56, 0.8) 0%, rgba(10, 8, 28, 0.9) 65%, rgba(8, 6, 20, 0.95) 100%);
  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.45), 0 35px 80px rgba(0, 0, 0, 0.35);
  margin-bottom: 2.3rem;
}

.truck-asphalt {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 52%;
  background: linear-gradient(180deg, rgba(20, 18, 36, 0.95) 0%, rgba(12, 10, 26, 0.98) 100%);
}

.truck-center-line {
  position: absolute;
  left: -100%;
  right: 0;
  bottom: 40%;
  height: 6px;
  background: repeating-linear-gradient(90deg, rgba(255, 223, 128, 0.9) 0, rgba(255, 223, 128, 0.9) 18px, transparent 18px, transparent 40px);
  animation: laneDrift 3s linear infinite;
}

.truck-light {
  position: absolute;
  top: 18%;
  width: 90px;
  height: 90px;
  border-radius: 50%;
  filter: blur(8px);
  animation: lightPulse 3.2s ease-in-out infinite;
}

.truck-rig {
  position: absolute;
  bottom: 18%;
  left: -35%;
  width: 260px;
  height: 120px;
  animation: driveAcross 9s linear infinite;
  transform-origin: center;
}

.truck-cab {
  position: absolute;
  left: 0;
  top: 28px;
  width: 110px;
  height: 76px;
  background: linear-gradient(135deg, #f9416d, #ffb347);
  border-radius: 12px 8px 18px 8px;
  box-shadow: inset 0 -8px 12px rgba(0, 0, 0, 0.3);
}

.truck-window {
  position: absolute;
  top: 14px;
  left: 18px;
  width: 60px;
  height: 26px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.8), rgba(162, 217, 255, 0.65));
  border-radius: 6px;
}

.truck-flag {
  position: absolute;
  top: -26px;
  left: 58px;
  padding: 0.25rem 0.65rem;
  background: linear-gradient(135deg, #ffd43b, #ff70a6);
  color: #281f3f;
  font-weight: 800;
  border-radius: 6px 6px 6px 0;
  box-shadow: 0 4px 10px rgba(255, 108, 165, 0.65);
  letter-spacing: 0.08em;
}

.truck-bed {
  position: absolute;
  left: 82px;
  top: 10px;
  width: 158px;
  height: 94px;
  background: linear-gradient(135deg, #353358, #23203f);
  border-radius: 12px 18px 18px 12px;
  box-shadow: inset 0 -6px 12px rgba(0, 0, 0, 0.35);
}

.truck-decal {
  position: absolute;
  right: 14px;
  top: 22px;
  padding: 0.3rem 0.9rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.35);
  letter-spacing: 0.15em;
  font-weight: 700;
}

.truck-wheel {
  position: absolute;
  bottom: -22px;
  width: 58px;
  height: 58px;
  background: radial-gradient(circle, rgba(80, 80, 80, 1) 0%, rgba(22, 22, 22, 1) 60%);
  border-radius: 50%;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.6);
  animation: wheelSpin 1s linear infinite;
}

.truck-wheel::after {
  content: '';
  position: absolute;
  inset: 12px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.45) 0%, rgba(120, 120, 120, 0.4) 60%, transparent 85%);
}

.truck-wheel.front {
  left: 38px;
}

.truck-wheel.rear {
  right: 34px;
}

.truck-headlight {
  position: absolute;
  left: -18px;
  top: 58px;
  width: 60px;
  height: 26px;
  background: radial-gradient(circle, rgba(255, 255, 190, 0.85) 0%, rgba(255, 243, 160, 0.7) 45%, rgba(255, 255, 255, 0) 75%);
  filter: blur(2px);
  transform: rotate(-5deg);
  animation: headlightGlow 2s ease-in-out infinite;
}

.truck-tailglow {
  position: absolute;
  right: -12px;
  top: 78px;
  width: 44px;
  height: 18px;
  background: radial-gradient(circle, rgba(255, 92, 120, 0.85) 0%, rgba(255, 0, 68, 0) 70%);
  filter: blur(3px);
}

.gratitude-notes {
  margin-top: 1.5rem;
}

.note-row {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.gratitude-note {
  position: relative;
  background: rgba(24, 21, 52, 0.85);
  border-radius: 18px;
  padding: 1.4rem 1.6rem 1.4rem 3.8rem;
  border: 2px solid;
  color: rgba(255, 255, 255, 0.92);
  font-style: italic;
  line-height: 1.7;
  box-shadow: 0 14px 32px rgba(0, 0, 0, 0.45);
}

.note-accent {
  position: absolute;
  left: 1.2rem;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 70%;
  border-radius: 999px;
}

.closing {
  text-align: center;
  margin-top: 3rem;
  font-size: 1.05rem;
  color: rgba(255, 255, 255, 0.88);
}

.close-secondary {
  margin-top: 1.8rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.35);
  color: rgba(255, 255, 255, 0.9);
  padding: 0.85rem 1.6rem;
  border-radius: 999px;
  font-weight: 600;
  letter-spacing: 0.05em;
  transition: background 0.3s ease, color 0.3s ease;
}

.close-secondary:hover {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
}

.firework-field {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.firework-burst {
  position: absolute;
  width: 240px;
  height: 240px;
  transform: translate(-50%, -50%) scale(0.4);
  opacity: 0;
  animation: fireworkBurst 2.2s ease-out forwards;
  filter: blur(0.3px);
}

@keyframes fireworkBurst {
  0% {
    transform: translate(-50%, -50%) scale(0.1);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  55% {
    transform: translate(-50%, -50%) scale(1);
  }
  100% {
    transform: translate(-50%, -60%) scale(0.2);
    opacity: 0;
  }
}

@media (max-width: 768px) {
  .content-card {
    padding: 2.6rem 1.6rem 2.2rem;
    max-height: calc(100vh - 3rem);
  }

  .truck-highway {
    height: 190px;
  }

  .truck-rig {
    width: 210px;
    height: 100px;
  }

}

@keyframes driveAcross {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(160%);
  }
}

@keyframes wheelSpin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes headlightGlow {
  0%, 100% {
    opacity: 0.7;
    transform: rotate(-5deg) scale(1);
  }
  50% {
    opacity: 1;
    transform: rotate(-4deg) scale(1.08);
  }
}

@keyframes laneDrift {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(100%);
  }
}

@keyframes lightPulse {
  0%, 100% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.15);
  }
}
</style>
