<template>
    <div class="page-main-container">
        <h1 class="page-title">Settings</h1>

        <div class="profile-section">
            <h2 class="section-title">Email</h2>
            <p class="profile-info">{{ profile.email }}</p>
            <div class="settings-buttons half-n-half">
                <!-- <MenuButton label="Reset" @click="resetConversation" class="red" /> -->
                <MenuButton label="Logout" @click="logout" />
            </div>
        </div>

        <!-- TODO: maybe add later, but also maybe not -->
        <!-- <div class="profile-section">
            <h2 class="section-title">Current Theme</h2>
            <div class="half-n-half">
                <p v-if="currentTheme" class="profile-info">Note: Dark Mode is recommended</p>
                <p class="profile-info"> {{ currentTheme ? 'Light Mode' : 'Dark Mode'}} </p>
                <MenuButton label="Change Theme" @click="changeTheme" />
            </div>
        </div> -->

        <!-- Commented sections omitted for brevity -->
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from "axios";
import MenuButton from "@/components/Menus/MenuButton.vue";
// import TierButton from "@/components/Menus/TierButton.vue";
import { useMentorStore } from "@/store/mentorStore";
import { useAuthStore } from "@/store/authStore";
import { usePopupStore } from "@/store/popupStore";
import { useThemeStore } from "@/store/themeStore";

const router = useRouter();
const popupStore = usePopupStore();
const mentorStore = useMentorStore();
const authStore = useAuthStore();
const themeStore = useThemeStore();

interface Profile {
    user: string;
    tutor: string;
    email: string;
    tier: string;
}

const profile = ref<Profile>({
    user: "",
    tutor: "",
    email: "",
    tier: "",
});

const userTextarea = ref<HTMLTextAreaElement | null>(null);
const tutorTextarea = ref<HTMLTextAreaElement | null>(null);

const cloudTokens = computed(() => {
    return authStore.cloudTokens;
});

const currentMentorName = computed(() => {
    return mentorStore.currentMentor;
});

const displayTierName = computed(() => {
    const tierCode = profile.value.tier;
    const tierNameMap: Record<string, string> = {
        free: "Aspirant (free)",
        paid: "Awakened",
        pro: "Ascendant",
    };
    return tierNameMap[tierCode] || "Unknown Tier";
});

const currentTheme = computed(() => {
    return themeStore.darkMode;
});

const fetchProfile = async () => {
    try {
        const response = await axios.get("/api/profile");
        if (response.data.status === "success") {
            profile.value = response.data.profile;
            nextTick(() => {
                if (userTextarea.value) {
                    autoGrow({ target: userTextarea.value });
                }
                if (tutorTextarea.value) {
                    autoGrow({ target: tutorTextarea.value });
                }
            });
        } else {
            console.error("Failed to fetch profile");
        }
    } catch (error) {
        console.error("Error fetching profile:", error);
    }
};

const updateProfile = async (type: 'user' | 'tutor') => {
    try {
        const response = await axios.post(`/api/profile/${type}`, {
            data: profile.value[type],
        });
        if (response.data.status === "success") {
            popupStore.showPopup(`Profile of ${type} updated successfully.`);
        } else {
            popupStore.showPopup(`Failed to update ${type} profile`);
        }
    } catch (error) {
        popupStore.showPopup(`Error updating ${type} profile:`);
    }
};

const logout = async () => {
    try {
        let response = await axios.get("/api/logout");
        if (response.data.status === "success") {
            authStore.logout();
            router.push("/");
        } else {
            popupStore.showPopup("Failed to logout.");
        }
    } catch (error) {
        popupStore.showPopup("Error logging out:");
    }
};

const changeTheme = () => {
    themeStore.toggleDarkMode();
};

// const resetConversation = async () => {
//     // Commented out functionality
// };

const autoGrow = (event: { target: HTMLTextAreaElement }) => {
    const textarea = event.target;
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
};

onMounted(() => {
    fetchProfile();
});
</script>

<style scoped>
.profile-section {
    margin-top: 16px;
    padding-bottom: 16px;
    width: 100%;
    max-width: 720px;
    border-bottom: 2px solid var(--background-color-1t);
}

.settings-buttons {
    margin-top: 16px;
    width: 100%;
    max-width: 720px;
}

.profile-info {
    padding: 8px 16px;
    margin: 4px;
    width: 100%;
    
    margin-top: 4px;
    color: var(--text-color);
    justify-content: center;
    display: flex;
    align-items: center;
    border: 1px solid var(--element-color-1);
    border-radius: 8px;
}

.section-title {
    margin-bottom: 8px;
}

.profile-textarea {
    resize: none;
    overflow-y: hidden;
    background-color: #00000000;
    outline: none;
    width: 100%;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid var(--text-color);
}

.update-btn {
    margin-top: 8px;
    padding: 8px 16px;
    background-color: var(--element-color-1);
    color: var(--text-color);
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.update-btn:hover {
    background-color: var(--element-color-2);
}

.half-n-half {
    display: flex;
    flex-direction: row;
}

.red {
    background-color: red;
}
</style>
