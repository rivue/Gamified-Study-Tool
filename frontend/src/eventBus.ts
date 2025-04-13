// src/eventBus.ts
import { reactive } from 'vue'

type EventCallback = (...args: any[]) => void;

type ListenerMap = {
  [event: string]: EventCallback | undefined;
};

const listeners = reactive<ListenerMap>({});

const eventBus = {
  emit(event: string, ...args: any[]) {
    listeners[event]?.(...args);
  },
  on(event: string, callback: EventCallback) {
    listeners[event] = callback;
  },
  off(event: string) {
    delete listeners[event];
  },
};

export default eventBus;
