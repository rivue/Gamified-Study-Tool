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

    // basically main home page
    // { path: '/changelog', component: defineAsyncComponent(() => import('./components/Footer/MainPage.vue')), meta: { title: Rivue.ai | Learn Anything!' } },
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
        {
            name: 'GamePage',
            path: '/lessons/:id/:roomName',
            component: defineAsyncComponent(() => import('./components/Game/NewGame/GamePage.vue')),
            meta: { title: 'Rivue.ai | Explore Library', hideHeaderFooter: true },
            beforeEnter: async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
                try {
                    const response = await axios.get(`/api/library/${to.params.id}`);
                    if (response.data?.status === "success") {
                        const roomList = response.data.data.room_names[0] || [];
                        roomList.includes(to.params.roomName) ? next() : next(`/lessons/${to.params.id}`);

                    } else {
                        next('/library');
                    }
                } catch (error) {
                    console.error("Failed to validate library/room:", error);
                    next('/library');
                }
            }
        },
        { 
            path: '/lessons/:id',
            component: defineAsyncComponent(() => import('./components/Backstage/MapPage.vue')), 
            meta: { title: 'Rivue.ai | Explore Library', requiresCreator: true },
            beforeEnter: async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
                try {
                    const response = await axios.get(`/api/library/${to.params.id}`);
                    response.data?.status === "success" ? next() : next('/library');
                } catch (error) {
                    console.error("Failed to validate library:", error);
                    next('/library');
                }
            }
        },
        
        // Simple routes
        { path: '/changelog', component: defineAsyncComponent(() => import('./components/Backstage/ChangelogPage.vue')), meta: { title: 'Rivue.ai | Learn Anything!' } },
        { path: '/library', component: defineAsyncComponent(() => import('./components/Game/Creation/LibraryCreator.vue')), meta: { title: 'Rivue.ai | Create Library' } },
        // { path: '/progress', component: defineAsyncComponent(() => import('./components/Backstage/ProgressPage.vue')), meta: { title: 'Rivue.ai | Progress' } },
        { path: '/contact', component: defineAsyncComponent(() => import('./components/Footer/ContactPage.vue')), meta: { title: 'Rivue.ai | Contact Us' } },
        { path: '/settings', component: defineAsyncComponent(() => import('./components/Backstage/SettingsPage.vue')), meta: { title: 'Rivue.ai | Settings' } },
        // { path: '/terms', component: defineAsyncComponent(() => import('./components/Footer/TermsAndPoliciesPage.vue')), meta: { title: 'Rivue.ai | Terms and Policies' } },
        // { path: '/plan', component: defineAsyncComponent(() => import('./components/Monetization/PlanPage.vue')), meta: { title: 'Rivue.ai | Premium Plans' } },
        { path: '/login', component: defineAsyncComponent(() => import('./components/Auth/LoginSignupPopup.vue')), meta: { title: 'Rivue.ai | Login/Signup' } },
        // { path: '/admin', component: defineAsyncComponent(() => import('./components/Auth/AdminPage.vue')), meta: { title: 'Rivue.ai | Admin' } },
        { path: '/verify', component: defineAsyncComponent(() => import('./components/Auth/VerifyEmail.vue')), meta: { title: 'Rivue.ai | Verify Email' }},
        { path: '/verify/:token', component: defineAsyncComponent(() => import('./components/Auth/VerifyEmail.vue')), meta: { title: 'Rivue.ai | Verify Email' }},
        { path: '/reset-password/:token', component: defineAsyncComponent(() => import('./components/Auth/PasswordResetForm.vue')), props: true, meta: { title: 'Rivue.ai | Password Reset' }},
        
        // Redirects
        // { path: '/lessons', redirect: '/' },
        { path: '/lessons/:pathMatch(.*)*', redirect: '/' },
        { path: '/changelog/:pathMatch(.*)*', redirect: '/' },
        { path: '/library/:pathMatch(.*)*', redirect: '/library' },
        // { path: '/progress/:pathMatch(.*)*', redirect: '/progress' },
        { path: '/contact/:pathMatch(.*)*', redirect: '/contact' },
        { path: '/settings/:pathMatch(.*)*', redirect: '/settings' },
        // { path: '/terms/:pathMatch(.*)*', redirect: '/terms' },
        // { path: '/plan/:pathMatch(.*)*', redirect: '/plan' },
        { path: '/login/:pathMatch(.*)*', redirect: '/login' },
        // { path: '/admin/:pathMatch(.*)*', redirect: '/admin' },
        
        // Catch-all route - must be last!
        // { path: '/:pathMatch(.*)*', component: defineAsyncComponent(() => import('./components/Backstage/404.vue')), meta: { title: 'Rivue.ai' } },

    ];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore();

    const loading = useLoadingStore()
    if (!from.matched.length) loading.start()
    console.debug("idk")

    const publicPaths = [
        '/',
        '/changelog',
        '/login',
        '/terms',
        '/contact',
        '/plan',
        '/verify', // Explicitly add /verify as a public path
    ];
    console.debug(to.path);
    
    // Check if the path is a reset password path
    const isResetPasswordPath = to.path.startsWith('/reset-password/');
    
    // Check if the path is /verify exactly (public) or starts with /verify/ (requires auth)
    const isPublicVerifyPath = to.path === '/verify';
    const isProtectedVerifyPath = to.path.startsWith('/verify/') && to.path !== '/verify';
    
    const requiresAuth = !publicPaths.includes(to.path) && 
                         !isResetPasswordPath && 
                         !(isPublicVerifyPath) && 
                         (isProtectedVerifyPath || !to.path.startsWith('/verify'));

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
                    response.data.data.user_id == user) {
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
    } else if (to.path === '/login' && !to.query.redirect) {
        // Ensure the redirect query is included when navigating to the login page from any route
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
