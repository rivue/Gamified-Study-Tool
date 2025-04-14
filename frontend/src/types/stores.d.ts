import { useGameStore } from "@/store/gameStore";
declare module "pinia" {
    export interface PiniaCustomStores {
        gameStore: ReturnType<typeof useGameStore>;
    }
}

import { useAuthStore } from "@/store/authStore";
declare module "pinia" {
    export interface PiniaCustomStores {
        authStore: ReturnType<typeof useAuthStore>;
    }
}

import { useMessageStore } from "@/store/messageStore";
declare module "pinia" {
  export interface PiniaCustomStores {
    messageStore: ReturnType<typeof useMessageStore>;
  }
}

import { usePopupStore } from "@/store/popupStore";
declare module "pinia" {
  export interface PiniaCustomStores {
    popupStore: ReturnType<typeof usePopupStore>;
  }
}