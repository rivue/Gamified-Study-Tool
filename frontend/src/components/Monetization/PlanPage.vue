<template>
    <div class="plan-page">
      <!-- Header -->
      <div class="header-container">
        <h1 class="page-title">Choose Your Plan and Start Learning Today!</h1>
        <p class="page-description">
          Whether you're just starting or ready to level up, we have a plan to fit your needs.
        </p>
      </div>
  
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
            <button
              :style="{ backgroundColor: plan.buttonColor }"
              :disabled="userTierMapping[plan.title] === userTier"
              @click="updateUserPlan(plan.title)"
            >
              {{ planButtonLabels[index] }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import { useAuthStore } from '@/store/authStore';
  
  export default {
    name: "PlanPage",
    data() {
      return {
        plans: [
          {
            title: "Aspirant",
            price: "Free",
            features: [
              "25☁️ Free Every Day",
              "Custom Libraries",
              "Knowledge Map",
              "Personal Tutor",
            ],
            color: "#1D7F74", // Dark teal
            buttonColor: "#33B2A5", // Light teal
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
            color: "#33B2A5", // Light teal
            buttonColor: "#33B2A5", // Light teal
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
            color: "#66C5BC", // Very light teal
            buttonColor: "#66C5BC", // Very light teal
          },
        ],
        userTierMapping: {
          Aspirant: "free",
          Awakened: "paid",
          Ascendant: "pro",
        },
        planUrls: {
          Aspirant: "https://buy.stripe.com/bIY6sg5154ZmaXu4gi",
          Awakened: "https://buy.stripe.com/cN2aIw79ddvSghOaEI",
          Ascendant: "https://buy.stripe.com/9AQ5ocbptfE0fdK005",
        },
      };
    },
    computed: {
      isPlanPage() {
        return this.$route.path === "/plan";
      },
      authStore(){
        return useAuthStore();
      },
      loggedIn(){
        return this.authStore.loggedIn;
      },
      userTier() {
        return this.authStore.userTier;
      },
      planButtonLabels() {
        return this.plans.map((plan) => {
          if (this.userTierMapping[plan.title] === this.userTier) {
            return "Active";
          } else if (this.isUpgrade(plan.title)) {
            return "Upgrade";
          }
          return "Subscribe";
        });
      },
    },
    methods: {
      updateUserPlan(planTitle) {
        const paymentUrl = this.planUrls[planTitle];
        window.open(paymentUrl, "_blank");
      },
      isUpgrade(planTitle) {
        const tierOrder = ["Aspirant", "Awakened", "Ascendant"];
        const currentUserTierIndex = tierOrder.indexOf(
          Object.keys(this.userTierMapping).find(
            (key) => this.userTierMapping[key] === this.userTier
          )
        );
        const planTierIndex = tierOrder.indexOf(planTitle);
        return planTierIndex > currentUserTierIndex;
      },
    },
  };
  </script>
  
  <style scoped>
  .plan-page {
    color: var(--text-color);
    background-color: var(--background-color);
    padding: 40px 20px;
  }
  
  .header-container {
    text-align: center;
    margin-bottom: 40px;
  }
  
  .page-title {
    font-size: 2rem;
    font-weight: bold;
    color: #fff;
  }
  
  .page-description {
    font-size: 1rem;
    color: #94a3b8;
    line-height: 1.5;
  }
  
  .plans-container {
    display: flex;
    justify-content: center;
    gap: 30px;
    flex-wrap: wrap;
  }
  
  .plan {
    border: 2px solid transparent;
    border-radius: 8px;
    width: 300px;
    background-color: #00000000;
    transition: background-color opacity 0.3s;
    margin-bottom: 20px;
  }
  
  .plan-header {
    padding: 20px;
    text-align: center;
    color: var(--text-color);
    background-color: var(--background-color-1t);
  }
  
  .plan-header h1 {
    font-size: 1.5rem;
  }
  
  .plan-header .price {
    font-size: 1.25rem;
    font-weight: bold;
    color: var(--text-color);
  }
  
  .plan-body {
    background-color: var(--background-color-1t);
    padding: 15px;
    height: 220px;
  }
  
  .plan-footer {
    padding: 20px;
    text-align: center;
    background-color: var(--background-color-2t);
  }
  
  .plan-footer button {
    padding: 12px 20px;
    border-radius: 5px;
    cursor: pointer;
    border: 2px solid transparent;
    color: var(--text-color);
    transition: background-color 0.3s ease;
    font-weight: bold;
  }
  
  .plan-footer button:hover {
    background-color: var(--element-color-1);
    border-color: var(--element-color-1);
  }
  
  .plan:hover {
    background-color: var(--element-color-2);
    opacity: 0.9;
  }
  
  li {
    padding: 10px 0;
    color: #94a3b8;
  }
  
  @media (max-width: 768px) {
    .plans-container {
      flex-direction: column;
      align-items: center;
    }
    .plan {
      width: 100%;
    }
  }
  </style>
  