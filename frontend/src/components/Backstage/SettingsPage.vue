<template>
    <div class="page-main-container">
        <h1 class="page-title">Settings</h1>

        <div class="profile-section">
            <h2 class="section-title">Account Information</h2>
            <div class="form-field">
                <label for="email">Email:</label>
                <input type="text" id="email" :value="profile.email" readonly class="profile-input-readonly" />
            </div>
            <div class="form-field">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="editableProfile.username" class="profile-input" />
            </div>
            <div class="settings-buttons">
                <MenuButton label="Save Username" @click="saveUsername" customClass="action-button" />
            </div>
        </div>

        <div class="profile-section">
            <h2 class="section-title">Personal Details</h2>
            <div class="form-field">
                <label for="first_name">First Name:</label>
                <input type="text" id="first_name" v-model="editableProfile.first_name" class="profile-input" />
            </div>
            <div class="form-field">
                <label for="last_name">Last Name:</label>
                <input type="text" id="last_name" v-model="editableProfile.last_name" class="profile-input" />
            </div>
        </div>

        <div class="profile-section">
            <h2 class="section-title">Localization</h2>
            <div class="form-field">
                <label for="timezone">Time Zone:</label>
                <select id="timezone" v-model="editableProfile.timezone" class="profile-input">
                    <option v-if="timezonesList.length === 0" value="" disabled>Loading timezones...</option>
                    <option v-for="tz in timezonesList" :key="tz" :value="tz">{{ tz }}</option>
                </select>
            </div>
        </div>


        <div class="profile-section">
            <h2 class="section-title">Change Password</h2>
            <div class="form-field">
                <label for="currentPassword">Current Password:</label>
                <input type="password" id="currentPassword" v-model="currentPassword" class="profile-input" />
            </div>
            <div class="form-field">
                <label for="newPassword">New Password:</label>
                <input type="password" id="newPassword" v-model="newPassword" class="profile-input" />
            </div>
            <div class="form-field">
                <label for="confirmNewPassword">Confirm New Password:</label>
                <input type="password" id="confirmNewPassword" v-model="confirmNewPassword" class="profile-input" />
            </div>
            <div class="settings-buttons">
                <MenuButton label="Change Password" @click="changePassword" customClass="action-button" />
            </div>
        </div>

        <div class="settings-buttons half-n-half">
            <MenuButton label="Save Profile" @click="saveUserProfile" customClass="action-button" />
            <MenuButton label="Logout" @click="logout" customClass="danger-button" />
        </div>
        
        <div class="profile-section">
            <p class="text-center opacity-70 pt-4">
                Member Since: {{ new Date(profile.joined_at).toLocaleDateString() }}
            </p>

            <!-- TODO: maybe add light mode later -->


            <!-- TODO: maybe add light mode later -->

        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from "axios";
import MenuButton from "@/components/Menus/MenuButton.vue";
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
    user: string; // Corresponds to 'profile' text blob
    tutor: string;
    email: string;
    // tier: string;
    username: string;
    first_name: string;
    last_name: string;
    timezone: string;
    joined_at: string;
}

// For data fetched from backend (largely read-only display)
const profile = ref<Profile>({
    user: "", 
    tutor: "",
    email: "",
    // tier: "",
    username: "",
    first_name: "",
    last_name: "",
    timezone: "UTC", // Default value
    joined_at: ""
});

// For editable fields to avoid direct mutation of profile during editing
const editableProfile = ref({
    username: "",
    first_name: "",
    last_name: "",
    timezone: "UTC",
    profile_text: "" // For the generic profile text field
});

const currentPassword = ref("");
const newPassword = ref("");
const confirmNewPassword = ref("");

const timezonesList = ref<string[]>([]);

// const cloudTokens = computed(() => authStore.cloudTokens);
// const currentMentorName = computed(() => mentorStore.currentMentor);
// const currentTheme = computed(() => themeStore.darkMode);

// const displayTierName = computed(() => {
//     const tierCode = profile.value.tier;
//     const tierNameMap: Record<string, string> = {
//         free: "Aspirant (free)",
//         paid: "Awakened",
//         pro: "Ascendant",
//     };
//     return tierNameMap[tierCode] || "Unknown Tier";
// });
// const displayTierName = computed(() => {
//     const tierCode = profile.value.tier;
//     const tierNameMap: Record<string, string> = {
//         free: "Aspirant (free)",
//         paid: "Awakened",
//         pro: "Ascendant",
//     };
//     return tierNameMap[tierCode] || "Unknown Tier";
// });

const fetchProfile = async () => {
    try {
        const response = await axios.get("/api/profile");
        if (response.data.status === "success") {
            profile.value = response.data.profile;
            // Initialize editableProfile with fetched data
            editableProfile.value.username = response.data.profile.username || authStore.user?.username || ""; // Use authStore as fallback
            editableProfile.value.first_name = response.data.profile.first_name || "";
            editableProfile.value.last_name = response.data.profile.last_name || "";
            editableProfile.value.timezone = response.data.profile.timezone || "UTC";
            editableProfile.value.profile_text = response.data.profile.user || ""; // 'user' field from backend is the 'profile' text blob
        } else {
            popupStore.showPopup("Failed to fetch profile information.");
            console.error("Failed to fetch profile");
        }
    } catch (error) {
        popupStore.showPopup("Error fetching profile information.");
        console.error("Error fetching profile:", error);
    }
};

const saveUserProfile = async () => {
    try {
        const payload = {
            data: {
                first_name: editableProfile.value.first_name,
                last_name: editableProfile.value.last_name,
                timezone: editableProfile.value.timezone,
                profile_text: editableProfile.value.profile_text // This maps to User.profile
            }
        };
        const response = await axios.post(`/api/profile/user`, payload);
        if (response.data.status === "success") {
            popupStore.showPopup("Profile updated successfully.");
            // Re-fetch profile to get any backend-side updates or confirmations
            fetchProfile();
        } else {
            popupStore.showPopup(response.data.message || "Failed to update profile.");
        }
    } catch (error: any) {
        popupStore.showPopup(error.response?.data?.message || "Error updating profile.");
    }
};

const saveUsername = async () => {
    if (!editableProfile.value.username) {
        popupStore.showPopup("Username cannot be empty.");
        return;
    }
    try {
        const response = await axios.post(`/api/profile/username`, {
            new_username: editableProfile.value.username,
        });
        if (response.data.status === "success") {
            popupStore.showPopup("Username updated successfully.");
            // Update local profile state and authStore
            profile.value.username = editableProfile.value.username;
            if (authStore.user) {
                authStore.user.username = editableProfile.value.username;
            }
        } else {
            popupStore.showPopup(response.data.message || "Failed to update username.");
        }
    } catch (error: any) {
        popupStore.showPopup(error.response?.data?.message || "Error updating username.");
    }
};

const logout = async () => {
    try {
        const response = await axios.get("/api/logout");
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

const autoGrow = (event: { target: HTMLTextAreaElement }) => {
    const textarea = event.target;
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
};

const fetchTimezones = async () => {
    try {
        const response = await axios.get<string[]>("/api/timezones");
        if (response.data && Array.isArray(response.data)) {
            timezonesList.value = response.data;
        } else {
            console.error("Failed to fetch timezones: Invalid data format", response.data);
            popupStore.showPopup("Could not load timezones.");
        }
    } catch (error) {
        console.error("Error fetching timezones:", error);
        popupStore.showPopup("Error fetching timezones.");
    }
};

onMounted(() => {
    fetchProfile();
    fetchTimezones();
});


const changePassword = async () => {
    if (!newPassword.value) {
        popupStore.showPopup("New password cannot be empty.");
        return;
    }
    if (newPassword.value !== confirmNewPassword.value) {
        popupStore.showPopup("New passwords do not match.");
        return;
    }
    // Optional: Add password strength validation (e.g., min length)
    if (newPassword.value.length < 8) {
        popupStore.showPopup("New password must be at least 8 characters long.");
        return;
    }

    const formData = new FormData();
    formData.append("current_password", currentPassword.value);
    formData.append("new_password", newPassword.value);

    try {
        const response = await axios.post("/api/change-password", formData);
        if (response.data.status === "success") {
            popupStore.showPopup("Password changed successfully.");
            currentPassword.value = "";
            newPassword.value = "";
            confirmNewPassword.value = "";
        } else {
            popupStore.showPopup(response.data.message || "Failed to change password.");
        }
    } catch (error: any) {
        if (error.response && error.response.data && error.response.data.message) {
            popupStore.showPopup(error.response.data.message);
        } else {
            popupStore.showPopup("An unexpected error occurred while changing password.");
        }
        console.error("Error changing password:", error);
    }
};
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
    display: flex;
    /* Added for button layout */
    gap: 10px;
    /* Added for spacing between buttons */
}

.profile-info,
.profile-input,
.profile-input-readonly {
    padding: 10px;
    margin: 4px 0;
    /* Adjusted margin */
    width: 100%;
    box-sizing: border-box;
    /* Ensures padding doesn't add to width */
    color: var(--text-color);
    border: 1px solid var(--element-color-1);
    border-radius: 8px;
    background-color: var(--background-color-2); /* Consistent background */
    font-size: 16px;
}

.profile-input-readonly {
    background-color: var(--background-color-1t); /* Slightly different for readonly */
    cursor: not-allowed;
}

.profile-input:focus {
    outline: none;
    border-color: var(--accent-color-1);
    box-shadow: 0 0 0 2px var(--accent-color-1-t);
}

.form-field {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

.form-field label {
  font-size: 16px;
  color: var(--text-color-secondary); /* Softer color for label */
  margin-bottom: 4px;
}

.section-title {
    margin-bottom: 12px;
    /* Increased margin */
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

.action-button {
    /* Custom styles for general action buttons if needed */
    /* Example: flex-grow: 1; to make buttons take equal space */
}

.danger-button {
    background-color: var(red) !important;
    /* Ensure high specificity */
    color: red !important;
}

.danger-button:hover {
    background-color: var(red) !important;
}
</style>