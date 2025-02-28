// main.js
import { createApp, defineAsyncComponent } from 'vue';
import { createPinia } from 'pinia'
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from "@/store/authStore";
// import { useGameStore } from "@/store/gameStore";
import './assets/styles.css';
import './assets/themes.css';
import axios from 'axios';

const routes = [

    // root
    { path: '/', component: defineAsyncComponent(() => import('./components/Footer/HomePage.vue')), meta: { title: 'Ascendance·☁️| Create Library' } },

    // basically main home page
    // TODO eventually add back in - maybe like talk abt the struggle of school and / or my background or something
    // { path: '/about', component: defineAsyncComponent(() => import('./components/Footer/MainPage.vue')), meta: { title: 'Ascendance·☁️| Learn Anything!' } },

    // llm chatbot = not necessary for me
    //   { path: '/lessons', component: defineAsyncComponent(() => import('./components/Chat/ChatComponent.vue')), meta: { title: 'Ascendance·☁️| Lessons' } }, 
    //   { path: '/lesson/:id', component: defineAsyncComponent(() => import('./components/Chat/ChatComponent.vue')), meta: { title: 'Ascendance·☁️| Learning' } },
    { path: '/lessons/:id/:roomName', component: defineAsyncComponent(() => import('./components/Game/NewGame/GamePage.vue')), meta: { title: 'Ascendance·☁️| Explore Library', hideHeaderFooter: true } },
    { path: '/lessons/:id', component: defineAsyncComponent(() => import('./components/Backstage/MapPage.vue')), meta: { title: 'Ascendance·☁️| Explore Library', requiresCreator: true } },

    // create library (game)
    { path: '/library', component: defineAsyncComponent(() => import('./components/Game/Creation/LibraryCreator.vue')), meta: { title: 'Ascendance·☁️| Create Library' } },

    // actual games - come back to later, try to access whole game
    //   { path: '/library/:id', component: defineAsyncComponent(() => import('./components/Game/NewGame/GamePage.vue')), meta: { title: 'Ascendance·☁️| Explore Library' } },
    //   { path: '/library/:id/:roomName', component: defineAsyncComponent(() => import('./components/Game/NewGame/GamePage.vue')), meta: { title: 'Ascendance·☁️| Explore Library', hideHeaderFooter: true } },

    // statistics basically, % lessons complete, that type thing
    { path: '/progress', component: defineAsyncComponent(() => import('./components/Backstage/ProgressPage.vue')), meta: { title: 'Ascendance·☁️| Progress' } },

    // knowledge map (probably not going to include yet)
    //   { path: '/knowledge', component: defineAsyncComponent(() => import('./components/Backstage/MapPage.vue')), meta: { title: 'Ascendance·☁️| Knowledge Map' } },

    // the maps of different courses
    //   { path: '/knowledge/:id', component: defineAsyncComponent(() => import('./components/Backstage/MapPage.vue')), meta: { title: 'Ascendance·☁️| Knowledge Map' } },


    // submit feedback
    { path: '/contact', component: defineAsyncComponent(() => import('./components/Footer/ContactPage.vue')), meta: { title: 'Ascendance·☁️| Contact Us' } },

    // user settings page
    { path: '/settings', component: defineAsyncComponent(() => import('./components/Backstage/SettingsPage.vue')), meta: { title: 'Ascendance·☁️| Settings' } },

    // actual legal acreement thing (not sure???)
    { path: '/terms', component: defineAsyncComponent(() => import('./components/Footer/TermsAndPoliciesPage.vue')), meta: { title: 'Ascendance·☁️| Terms and Policies' } },

    // choose free vs other membership
    { path: '/plan', component: defineAsyncComponent(() => import('./components/Monetization/PlanPage.vue')), meta: { title: 'Ascendance·☁️| Premium Plans' } },

    // im assuming it is login page
    { path: '/login', component: defineAsyncComponent(() => import('./components/Auth/LoginSignupPopup.vue')), meta: { title: 'Ascendance·☁️| Login/Signup' } },

    // admin stuff, basically users and what not - might be useful later
    { path: '/admin', component: defineAsyncComponent(() => import('./components/Auth/AdminPage.vue')), meta: { title: 'Ascendance·☁️| Admin' } },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});
router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore();
    // const gameStore = useGameStore();

    // if (from.path.startsWith('/library/')) {
    //     gameStore.resetGameState();
    // }

    // if (to.path.startsWith('/library/') && from.path.startsWith('/library/')) {
    //     const toLibraryId = to.path.split('/')[2];
    //     const toRoomName = to.path.split('/')[3];
    //     gameStore.fetchLibraryDetails(toLibraryId, toRoomName);
    // }

    const publicPaths = [
        '/',
        '/login',
        '/terms',
        '/contact',
        '/plan',
        '/',
    ];

    const requiresAuth =
        !publicPaths.includes(to.path) &&
        !to.path.startsWith('/lesson/') &&
        !to.path.startsWith('/library') && !to.path.startsWith('/lessons');

    if (to.meta.requiresCreator && to.params.id) {
        // Only proceed with this check if the user is logged in
        if (authStore.loggedIn) {
            try {
                
                // Check if the user is the creator of the library
                const response = await axios.get(`/api/library/${to.params.id}`);
                if (response.data && 
                    response.data.data && 
                    response.data.data.user_id == authStore.userId) {
                        // User is the creator, continues as per usual
                        return next();
                } else { // invalid data 
                    return next('/library');
                }
                    
            } catch (error) {
                console.error("Error checking library permissions:", error);
                return next('/library');
            }
        } else {
            // If not logged in and the route requires creator access, redirect to login
            return next({
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
    } else if (to.path === '/login' && !to.query.redirect) {
        // Ensure the redirect query is included when navigating to the login page from any route
        next({
            path: '/login',
            query: { redirect: from.fullPath },
        });
    } else {
        next();
    }

    document.title = to.meta.title || 'Ascendance·☁️| Learn Anything!';
});

// axios.defaults.baseURL = 'https://obscure-memory-64wr7jgrgrvhr7g4-5000.app.github.dev';
axios.defaults.baseURL = 'http://localhost:5000';
axios.defaults.withCredentials = true;

const pinia = createPinia()

const app = createApp(App);
app.use(pinia)
app.use(router);
app.mount('#app');
