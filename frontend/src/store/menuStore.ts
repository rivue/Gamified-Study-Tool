// stores/menuStore.js
import { defineStore } from 'pinia';

export const useMenuStore = defineStore('menu', {
    state: () => ({
        sideMenuOpen: false,
        actionsMenuOpen: false,
        sideMenuClickListener: null as ((event: MouseEvent) => void) | null,
        actionMenuClickListener: null as ((event: MouseEvent) => void) | null,
    }),
    actions: {
        toggleSideMenu() {
            this.sideMenuOpen = !this.sideMenuOpen;
            if (this.sideMenuOpen) {
                this.setupClickAwayListenerSideMenu();
            } else {
                this.removeClickAwayListenerSideMenu();
            }
        },
        hideSideMenu() {
            if (this.sideMenuClickListener) {
                document.removeEventListener('click', this.sideMenuClickListener);
                this.sideMenuClickListener = null;
            }
            this.sideMenuOpen = false;
        },
        openSideMenu() {
            this.sideMenuOpen = true;
            this.setupClickAwayListenerSideMenu();
        },
        closeSideMenu() {  // Add new method
            this.sideMenuOpen = false;
        },

        toggleActionMenu() {
            this.actionsMenuOpen = !this.actionsMenuOpen;
            if (this.actionsMenuOpen) {
                this.setupClickAwayListenerActionMenu();
            } else {
                this.removeClickAwayListenerActionMenu();
            }
        },
        hideActionMenu() {
            if (this.actionMenuClickListener) {
                document.removeEventListener('click', this.actionMenuClickListener);
                this.actionMenuClickListener = null;
            }
            this.actionsMenuOpen = false;
        },
        openActionMenu() {
            this.actionsMenuOpen = true;
            this.setupClickAwayListenerActionMenu();
        },

        setupClickAwayListenerActionMenu() {
            setTimeout(() => {
                const clickAwayListener = (event: MouseEvent) => {
                    const menuElement = document.querySelector('.action-menu');
                    if (menuElement && !menuElement.contains(event.target as Node)) {
                        this.hideActionMenu();
                    }
                };
                this.actionMenuClickListener = clickAwayListener;
                document.addEventListener('click', clickAwayListener);
            }, 0);
        },

        setupClickAwayListenerSideMenu() {
            setTimeout(() => {
                const clickAwayListener = (event: MouseEvent) => {
                    const sideMenuElement = document.querySelector('.side-menu');
                    if (sideMenuElement && !sideMenuElement.contains(event.target as Node)) {
                        this.hideSideMenu();
                    }
                };
                this.sideMenuClickListener = clickAwayListener;
                document.addEventListener('click', clickAwayListener);
            }, 0);
        },

        removeClickAwayListenerActionMenu() {
            if (this.actionMenuClickListener) {
                document.removeEventListener('click', this.actionMenuClickListener);
                this.actionMenuClickListener = null;
            }
        },

        removeClickAwayListenerSideMenu() {
            if (this.sideMenuClickListener) {
                document.removeEventListener('click', this.sideMenuClickListener);
                this.sideMenuClickListener = null;
            }
        }
    },
});
