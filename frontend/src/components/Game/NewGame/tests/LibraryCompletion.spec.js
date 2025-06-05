import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia, storeToRefs } from 'pinia';
import LibraryCompletion from '../LibraryCompletion.vue';
import { useUserStatsStore } from '@/store/userStatsStore';
import { useGameStore } from '@/store/gameStore'; // Needed as the component uses it

// Mock the router
const mockRouterPush = jest.fn();
jest.mock('vue-router', () => ({
  useRouter: () => ({
    push: mockRouterPush,
  }),
}));

describe('LibraryCompletion.vue', () => {
  let pinia;

  beforeEach(() => {
    pinia = createPinia();
    setActivePinia(pinia);

    // Mock gameStore as it's used by the component
    // We need to ensure 'completed' is true for the component to be visible
    const gameStore = useGameStore();
    gameStore.completed = true; // Make the component visible
    gameStore.libraryId = 'test-lib-id'; // Provide a libraryId for the nextPage navigation

    // Reset router mock
    mockRouterPush.mockClear();
  });

  it('displays the current streak from userStatsStore', () => {
    const userStatsStore = useUserStatsStore();
    userStatsStore.currentStreak = 7; // Set a mock streak

    const wrapper = mount(LibraryCompletion, {
      global: {
        plugins: [pinia],
      },
    });

    // Check if the component is visible (controlled by gameStore.completed)
    expect(wrapper.find('.completion-overlay').exists()).toBe(true);

    // Find the element displaying the streak
    // Looking for the text "Current Streak: X"
    const streakTextElement = wrapper.find('.streak-days');
    expect(streakTextElement.exists()).toBe(true);
    // Check if the text content includes the streak number
    // The actual rendered text will be something like "Current Streak: 7" with an image inside
    expect(streakTextElement.text()).toContain('Current Streak:');
    expect(streakTextElement.text()).toContain('7');
  });

  it('calls userStatsStore.resetStats and navigates on "Continue" button click', async () => {
    const userStatsStore = useUserStatsStore();
    userStatsStore.resetStats = jest.fn(); // Mock the resetStats action

    const gameStore = useGameStore(); // gameStore already set up in beforeEach

    const wrapper = mount(LibraryCompletion, {
      global: {
        plugins: [pinia],
      },
    });

    expect(wrapper.find('.completion-overlay').exists()).toBe(true);

    const continueButton = wrapper.find('.primary-cta');
    expect(continueButton.exists()).toBe(true);

    await continueButton.trigger('click');

    expect(userStatsStore.resetStats).toHaveBeenCalled();
    expect(mockRouterPush).toHaveBeenCalledWith('/lessons/test-lib-id');
    // Check if the component attempts to hide or change state after click
    // Based on the component logic, page.value changes, which hides the firstPage content
    // So, we can check if 'pre-completion-content' is no longer visible if page.value changes
    // This requires a bit more understanding of how the component's internal state affects visibility
    // For now, just checking the store interaction and navigation is sufficient for this test's scope.
  });

  it('renders correctly when completionVisible is true', () => {
    const gameStore = useGameStore();
    gameStore.completed = true; // Explicitly set for this test

    const wrapper = mount(LibraryCompletion, {
      global: {
        plugins: [pinia],
      },
    });
    expect(wrapper.find('.completion-overlay').exists()).toBe(true);
    expect(wrapper.find('.main-title').text()).toBe('Lesson Complete!');
  });

  it('does not render when completionVisible is false', () => {
    const gameStore = useGameStore();
    gameStore.completed = false; // Explicitly set for this test

    const wrapper = mount(LibraryCompletion, {
      global: {
        plugins: [pinia],
      },
    });
    expect(wrapper.find('.completion-overlay').exists()).toBe(false);
  });
});
