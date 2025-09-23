// main.js
import { createApp, defineAsyncComponent } from 'vue';
import { createPinia } from 'pinia'
import App from './App.vue';
import { createRouter, createWebHistory, NavigationGuardNext, RouteLocationNormalized } from 'vue-router';
import { useAuthStore } from "@/store/authStore";
import { useLoadingStore } from "@/store/loadingStore";
// import { useGameStore } from "@/store/gameStore";
import './assets/styles.css';
import './assets/themes.css';
import axios from 'axios';
import { showExperimentsToast } from './utils/toasts';

// basically main home page
// { path: '/', component: defineAsyncComponent(() => import('./components/Footer/MainPage.vue')), meta: { title: Rivue.ai | Learn Anything!' } },

// { 
//     path: '/:pathMatch(.*)*', 
//     component: defineAsyncComponent(() => import('./components/Footer/HomePage.vue')),
//     meta: { title: Rivue.ai | Page Not Found' } 
// }
// llm chatbot = not necessary for me
//   { path: '/lessons', component: defineAsyncComponent(() => import('./components/Chat/ChatComponent.vue')), meta: { title: Rivue.ai | Lessons' } }, 
//   { path: '/lesson/:id', component: defineAsyncComponent(() => import('./components/Chat/ChatComponent.vue')), meta: { title: Rivue.ai | Learning' } },


// actual games - come back to later, try to access whole game
//   { path: '/library/:id', component: defineAsyncComponent(() => import('./components/Game/NewGame/GamePage.vue')), meta: { title: Rivue.ai | Explore Library' } },
//   { path: '/library/:id/:roomName', component: defineAsyncComponent(() => import('./components/Game/NewGame/GamePage.vue')), meta: { title: Rivue.ai | Explore Library', hideHeaderFooter: true } },
// knowledge map (probably not going to include yet)
//   { path: '/knowledge', component: defineAsyncComponent(() => import('./components/Backstage/MapPage.vue')), meta: { title: Rivue.ai | Knowledge Map' } },

// the maps of different courses
//   { path: '/knowledge/:id', component: defineAsyncComponent(() => import('./components/Backstage/MapPage.vue')), meta: { title: Rivue.ai | Knowledge Map' } },
// { path: '/:pathMatch(.*)*', redirect: '/' },

// Catch-all for 404 errors
// { 
//     path: '/:pathMatch(.*)*', 
//     component: defineAsyncComponent(() => import('./components/Footer/HomePage.vue')),
//     meta: { title: 'Rivue.ai | Page Not Found' } 
// }

const routes = [
    // Main routes
    { path: '/', component: defineAsyncComponent(() => import('./components/HomePage.vue')), meta: { title: 'Rivue.ai' } },
    { path: '/explore', component: defineAsyncComponent(() => import('./components/Main/Explore.vue')), meta: { title: 'Rivue.ai' } },
    // Put specific routes before the generic dynamic :roomName route
    // {
    //     name: 'MockTerminalLesson',
    //     path: '/lessons/:id/mock-terminal',
    //     component: defineAsyncComponent(() => import('./components/Game/NewGame/TerminalMockLesson.vue')),
    //     meta: { title: 'Rivue.ai | Mock Terminal', hideHeaderFooter: true }
    // },
    {
        name: 'GamePage',
        path: '/lessons/:id/:roomName',
        component: defineAsyncComponent(() => import('./components/Game/NewGame/GamePage.vue')),
        meta: { title: 'Rivue.ai | Explore Library', hideHeaderFooter: true },
        beforeEnter: async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
            try {
                const response = await axios.get(`/api/library/${to.params.id}`);
                if (response.data?.status === "success") {
                    const roomList = response.data.data.room_names || [];
                    const roomNames = roomList.map((room: any[]) => room[0]); // Extract just the room names
                    const decodedRoomName = decodeURIComponent(to.params.roomName as string);
                    roomNames.includes(decodedRoomName) ? next() : next(`/lessons/${to.params.id}`);

                } else {
                    next('/create');
                }
            } catch (error) {
                console.error("Failed to validate library/room:", error);
                next('/create');
            }
        }
    },
    {
        path: '/lessons/:id/experiments',
        component: defineAsyncComponent(() => import('./components/Graphs/Experiments/Experiments.vue')),
        meta: { title: 'Rivue.ai' }
    },
    {
        path: '/lessons/:id/braindump',
        component: defineAsyncComponent(() => import('./components/Graphs/Experiments/BrainDump.vue')),
        meta: { title: 'Rivue.ai', hideHeaderFooter: true },
        beforeEnter: async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
            try {
                const response = await axios.get(`/api/library/${to.params.id}`);
                if (response.data?.status === "success") {
                    next();
                } else {
                    showExperimentsToast();

                }
            } catch (error) {
                showExperimentsToast();

            }
        },
    },
    // {
    //     path: '/lessons/:id/process-master',
    //     component: defineAsyncComponent(() => import('./components/Graphs/Experiments/Processes.vue')),
    //     meta: { title: 'Rivue.ai', hideHeaderFooter: true },
    //     beforeEnter: async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
    //         try {
    //             const response = await axios.get(`/api/library/${to.params.id}`);
    //             if (response.data?.status === "success") {
    //                 next();
    //             } else {
    //                 showExperimentsToast();

    //             }
    //         } catch (error) {
    //             showExperimentsToast();

    //         }
    //     },
    // },
    // {
    //     path: '/lessons/:id/fact-sprint',
    //     component: defineAsyncComponent(() => import('./components/Graphs/Experiments/FactSprint.vue')),
    //     meta: { title: 'Rivue.ai', hideHeaderFooter: true },
    //     beforeEnter: async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
    //         try {
    //             const response = await axios.get(`/api/library/${to.params.id}`);
    //             if (response.data?.status === "success") {
    //                 next();
    //             } else {
    //                 showExperimentsToast();

    //             }
    //         } catch (error) {
    //             showExperimentsToast();

    //         }
    //     },
    // },
    {
        path: '/lessons/:id',
        component: defineAsyncComponent(() => import('./components/Backstage/MapPage.vue')),
        meta: { title: 'Rivue.ai | Explore Library', requiresCreator: true },
        beforeEnter: async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
            try {
                const response = await axios.get(`/api/library/${to.params.id}`);
                response.data?.status === "success" ? next() : next('/create');
            } catch (error) {
                console.error("Failed to validate library:", error);
                next('/create');
            }
        }
    },
    {
        name: 'Leaderboard',
        path: '/lessons/:libraryId/leaderboard',
        component: defineAsyncComponent(() => import('./components/Graphs/LearningPath/Leaderboard.vue')),
        meta: { title: 'Rivue.ai | Leaderboard', requiresCreator: true },
        beforeEnter: async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
            try {
                console.log(to.params.libraryId)
                const response = await axios.get(`/api/library/${to.params.libraryId}/scores`);
                response.data?.status === "success" ? next() : next('/create');
            } catch (error) {
                console.error("Failed to validate library:", error);
                next('/create');
            }
        }
    },
    {
        name: 'StudySlots',
        path: '/lessons/:libraryId/study-slots',
        component: defineAsyncComponent(() => import('./components/Graphs/LearningPath/StudySlots.vue')),
        meta: { title: 'Rivue.ai | Study Slots', requiresCreator: true },
        beforeEnter: async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
            try {
                const response = await axios.get(`/api/library/${to.params.libraryId}`);
                response.data?.status === "success" ? next() : next('/create');
            } catch (error) {
                console.error("Failed to validate library:", error);
                next('/create');
            }
        }
    },
    {
        path: '/lessons/:id/quizzes',
        name: 'QuizManager',
        component: () => import('@/views/QuizManager.vue')
    },
    {
        path: '/lessons/:id/materials',
        name: 'CourseMaterials',
        component: () => import('@/components/Graphs/Materials/CourseMaterials.vue'),
        meta: { requiresAuth: true }
    },

    // Simple routes
    {
        name: 'Home',
        path: '/home',
        alias: ['/courses'],
        component: defineAsyncComponent(() => import('./components/Game/Creation/LibraryBrowser.vue')),
        meta: { title: 'Rivue.ai | Home' }
    },
    { path: '/create', component: defineAsyncComponent(() => import('./components/Game/Creation/LibraryCreator.vue')), meta: { title: 'Rivue.ai | Create Course' } },
    // { path: '/progress', component: defineAsyncComponent(() => import('./components/Backstage/ProgressPage.vue')), meta: { title: 'Rivue.ai | Progress' } },
    { path: '/contact', component: defineAsyncComponent(() => import('./components/Footer/ContactPage.vue')), meta: { title: 'Rivue.ai | Contact Us' } },
    { path: '/settings', component: defineAsyncComponent(() => import('./components/Backstage/SettingsPage.vue')), meta: { title: 'Rivue.ai | Settings' } },
    // { path: '/terms', component: defineAsyncComponent(() => import('./components/Footer/TermsAndPoliciesPage.vue')), meta: { title: 'Rivue.ai | Terms and Policies' } },
    // { path: '/plan', component: defineAsyncComponent(() => import('./components/Monetization/PlanPage.vue')), meta: { title: 'Rivue.ai | Premium Plans' } },
    { path: '/login', component: defineAsyncComponent(() => import('./components/Auth/LoginSignupPopup.vue')), meta: { title: 'Rivue.ai | Login/Signup' } },
    // { path: '/admin', component: defineAsyncComponent(() => import('./components/Auth/AdminPage.vue')), meta: { title: 'Rivue.ai | Admin' } },
    { 
        name: "Verify", 
        path: '/verify', 
        component: defineAsyncComponent(() => import('./components/Auth/VerifyEmail.vue')), meta: { title: 'Rivue.ai | Verify Email' } },
    { path: '/verify/:token', component: defineAsyncComponent(() => import('./components/Auth/VerifyEmail.vue')), meta: { title: 'Rivue.ai | Verify Email' } },
    { path: '/reset-password/:token', component: defineAsyncComponent(() => import('./components/Auth/PasswordResetForm.vue')), props: true, meta: { title: 'Rivue.ai | Password Reset' } },
    { path: '/profile', component: defineAsyncComponent(() => import('./components/Graphs/UserStats.vue')), props: true, meta: { title: 'Rivue.ai | My Profile' } },

    // Redirects
    // { path: '/lessons', redirect: '/' },
    {
        path: '/legal',
        component: defineAsyncComponent(() => import('./components/LegalDocuments.vue')),
        meta: { title: 'Rivue.ai | Legal' }
    },
    {
        path: '/',
        redirect: () => {
            if (process.env.NODE_ENV === 'production') {
                window.location.href = 'https://try.rivue.ai';
                return 'https://try.rivue.ai'; // Fallback for router
            }
            return '/explore'; // Redirect to a local page in development
        },
    },
    // { path: '/lessons/:pathMatch(.*)*', redirect: '/' },
    { path: '/explore/:pathMatch(.*)*', redirect: '/explore' },
    { path: '/courses/:pathMatch(.*)*', redirect: '/home' },
    { path: '/home/:pathMatch(.*)*', redirect: '/home' },
    { path: '/create/:pathMatch(.*)*', redirect: '/create' },
    // { path: '/progress/:pathMatch(.*)*', redirect: '/progress' },
    { path: '/contact/:pathMatch(.*)*', redirect: '/contact' },
    { path: '/settings/:pathMatch(.*)*', redirect: '/settings' },
    { path: '/legal/:pathMatch(.*)*', redirect: '/legal' },
    // { path: '/terms/:pathMatch(.*)*', redirect: '/terms' },
    // { path: '/plan/:pathMatch(.*)*', redirect: '/plan' },
    { path: '/login/:pathMatch(.*)*', redirect: '/login' },
    { path: '/profile/:pathMatch(.*)*', redirect: '/profile' },
    { path: '/lessons/:id/quizzes/:pathMatch(.*)*', redirect: '/lessons/:id/quizzes' },
    // { path: '/admin/:pathMatch(.*)*', redirect: '/admin' },

    // Catch-all route - must be last!
    { path: '/:pathMatch(.*)*', component: defineAsyncComponent(() => import('./components/Backstage/404.vue')), meta: { title: 'Page Not Found' }},

];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    // window.location.href = 'https://try.rivue.ai/';
    // return;

    const authStore = useAuthStore();

    const loading = useLoadingStore()
    if (!from.matched.length) loading.start()

    const publicPaths = [
        '/',
        '/login',
        '/terms',
        '/contact',
        '/plan',
        '/legal/',
        '/verify', // Explicitly add /verify as a public path
        '/verify/', // Make /verify/ a public path
    ];

    // Check if the path is a reset password path
    const isResetPasswordPath = to.path.startsWith('/reset-password/');

    // Check if the path is /verify exactly (public) or starts with /verify/ (now also public)
    const isPublicVerifyPath = to.path === '/verify' || to.path.startsWith('/verify/');

    const requiresAuth = !publicPaths.includes(to.path) &&
        !isResetPasswordPath &&
        !isPublicVerifyPath;

    if (to.meta.requiresCreator && to.params.id) {
        // Only proceed with this check if the user is logged in
        if (authStore.loggedIn) {
            try {
                let user = 0;
                const curr_user = await axios.get('/api/check-auth');
                if (curr_user.data.userId) {
                    user = curr_user.data.userId;
                } else {
                    return next('/login');
                }
                // Check if the user is the creator of the library
                const response = await axios.get(`/api/library/${to.params.id}`);
                if (response.data &&
                    response.data.data &&
                    response.data.data.membership_status) { // membership_status is true / false
                    return next();
                } else {
                    console.log(response.data.data.membership_status)
                    return next('/library');
                }

            } catch (error) {
                console.error("Error checking library permissions:", error);
                return next('/library');
            }
        } else {
            // If not logged in and the route requires creator access, redirect to login
            console.debug("Requires creator access, redirecting to login");
            return next(
                {
                    path: '/login',
                    query: { redirect: to.fullPath },
                });
        }
    }

    if (authStore.loggedIn && to.path === '/login') {
        // Redirect authenticated users away from the login page
        
        next('/');
    } else if (!authStore.loggedIn && requiresAuth) {
        // Redirect unauthenticated users to the login page with redirect to the intended page
        next({
            path: '/login',
            query: { redirect: from.fullPath },
        });
    } else {
        next();
    }

    document.title = (to.meta.title as string) || 'Rivue.ai | Learn Anything!';
});

router.afterEach(() => {
    const loading = useLoadingStore()
    loading.finish()
})

// axios.defaults.baseURL = import.meta.VITE_API_BASE_URL || 'http://localhost:5000';
axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL;

axios.defaults.withCredentials = true;

const pinia = createPinia()

const app = createApp(App);
app.use(pinia)
app.use(router);
app.mount('#app');
