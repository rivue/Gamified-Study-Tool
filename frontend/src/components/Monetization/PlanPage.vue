<template>
    <div class="plan-page">
        <h1 class="page-title" v-if="isPlanPage">Choose Your Subscription Plan</h1>
        <div class="header-container">
            <h1 class="page-title">Choose Your Plan and Start Learning Today!</h1>
            <p class="page-description">
                Whether you're just starting or ready to level up, we have a plan to fit your needs.
            </p>
        </div>
        <!-- <h1 class="page-title" v-else>Subscription Plans</h1> -->
        <div class="plans-container">
            <div class="plan" v-for="(plan, index) in plans" :key="index">
                <div class="plan-header" :style="{ backgroundColor: plan.color }">
                    <h1 v-if="loggedIn">{{ plan.title }}</h1>
                    <p class="price">{{ plan.price }}</p>
                </div>
                <div class="plan-body">
                    <ul>
                        <li v-for="(feature, index) in plan.features" :key="index">
                            {{ feature }}
                        </li>
                    </ul>
                </div>
                <div class="plan-footer">
                    <button :style="{ backgroundColor: plan.buttonColor }"
                        :disabled="userTierMapping[plan.title] === userTier" @click="updateUserPlan(plan.title)">
                        {{ planButtonLabels[index] }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">

import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { useAuthStore } from "@/store/authStore";


interface Plan {
    title: string;
    price: string;
    features: string[];
    color: string;
    buttonColor: string;
}

const route = useRoute();
const authStore = useAuthStore();

const plans = ref<Plan[]>([
    {
        title: "Aspirant",
        price: "Free",
        features: [
            "25☁️ Free Every Day",
            "Custom Libraries",
            "Knowledge Map",
            "Personal Tutor",
        ],
        color: "var(--background-color-1t)",
        buttonColor: "var(--background-color-2t)",
    },
    {
        title: "Awakened",
        price: "$4/month",
        features: [
            "250☁️ Every Day",
            "All features in Aspirant",
            "Unlimited Knowledge Map",
            "Priority Support",
        ],
        color: "var(--element-color-1)",
        buttonColor: "var(--element-color-1)",
    },
    {
        title: "Ascendant",
        price: "$8/month",
        features: [
            '2500☁️ Every Day',
            "All Features in Awakened",
            "Use Frontier AI Models",
            "Early Access to New Features",
        ],
        color: "var(--element-color-2)",
        buttonColor: "var(--element-color-2)",
    },
]);

const userTier = ref<string>("free");

const userTierMapping: Record<string, string> = {
    Aspirant: "free",
    Awakened: "paid",
    Ascendant: "pro",
};

const planUrls: Record<string, string> = {
  Aspirant: "https://buy.stripe.com/bIY6sg5154ZmaXu4gi",
  Awakened: "https://buy.stripe.com/cN2aIw79ddvSghOaEI",
  Ascendant: "https://buy.stripe.com/9AQ5ocbptfE0fdK005",
};


const isPlanPage = computed(() => route.path === "/plan");
const loggedIn = computed(() => authStore.loggedIn);
const currentUserTier = computed(() => authStore.userTier || userTier.value);

const isUpgrade = (planTitle: string): boolean => {
  const tierOrder = ["Aspirant", "Awakened", "Ascendant"];
  const currentTier = Object.keys(userTierMapping).find(
    (key) => userTierMapping[key] === currentUserTier.value
  );
  const currentIndex = tierOrder.indexOf(currentTier ?? "Aspirant");
  const planIndex = tierOrder.indexOf(planTitle);
  return planIndex > currentIndex;
};

const planButtonLabels = computed(() =>
  plans.value.map((plan) => {
    if (userTierMapping[plan.title] === currentUserTier.value) return "Active";
    else if (isUpgrade(plan.title)) return "Upgrade";
    return "Subscribe";
  })
);

const updateUserPlan = (planTitle: string) => {
  const paymentUrl = planUrls[planTitle];
  window.open(paymentUrl, "_blank");
  axios
    .post("/api/plan", { tier: userTierMapping[planTitle] })
    .then((response) => {
      if (response.data.status === "success") {
        userTier.value = userTierMapping[planTitle];
      }
    })
    .catch((error) => {
      console.error("Error updating user plan:", error);
    });
};

const fetchUserPlan = () => {
  axios
    .get("/api/plan")
    .then((response) => {
      userTier.value = response.data.tier;
    })
    .catch((error) => {
      console.error("Error fetching user plan:", error);
    });
};

onMounted(fetchUserPlan);
</script>

<style scoped>
.plan-page {
    color: var(--text-color);
    background-color: var(--background-color);
    padding: 20px;
}

.page-title {
    text-align: center;
    margin-bottom: 40px;
}

.plans-container {
    display: flex;
    justify-content: center;
    gap: 20px;
}

.plan-header h1 {
    border-bottom: 2px solid var(--background-color);
}

.plan {
    border: 2px solid var(--element-color-1);
    border-radius: 8px;
    overflow: hidden;
    width: 300px;
    opacity: 1;
    background-color: #00000000;
    transition: background-color opacity 0.3s;
}

.plan-header {
    padding: 20px;
    color: var(--text-color);
    text-align: center;
}

.plan:hover {
    background-color: var(--element-color-1);
    opacity: 0.8;
}

.plan-body {
    background-color: var(--background-color-1t);
    padding: 12px;
    height: 200px;
}

.plan-footer {
    padding: 20px;
    text-align: center;
    background-color: var(--background-color-2t);
}

.price {
    font-size: 1.5em;
}

button {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    color: var(--text-color);
    cursor: pointer;
    border: 2px solid var(--background-color-1t);
    transition: background-color 0.3s;
}

button:hover {
    background-color: var(--background-color-2t);
}

li {
    padding: 0px;
}

@media (max-width: 768px) {
    .plans-container {
        flex-direction: column;
        align-items: center;
    }

    .plan {
        width: 100%;
        margin-bottom: 20px;
    }
}
</style>
