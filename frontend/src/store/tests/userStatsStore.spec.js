import { setActivePinia, createPinia } from 'pinia';
import { useUserStatsStore } from '../userStatsStore';
import axios from 'axios';

// Mock axios
jest.mock('axios');

describe('useUserStatsStore', () => {
  beforeEach(() => {
    // Creates a new Pinia instance and makes it active so it's automatically picked
    // up by any useStore() call without needing to pass it to it:
    // `useStore(pinia)`
    setActivePinia(createPinia());
    // Reset mocks before each test
    axios.get.mockClear();
  });

  it('setStreakData correctly updates the state', () => {
    const store = useUserStatsStore();
    store.setStreakData(10, 15);
    expect(store.currentStreak).toBe(10);
    expect(store.bestStreak).toBe(15);
    expect(store.streakLoaded).toBe(true);
  });

  describe('fetchStreak', () => {
    it('fetches streak data successfully and updates the state', async () => {
      const store = useUserStatsStore();
      const mockData = { current_streak: 5, max_streak: 10 };
      axios.get.mockResolvedValueOnce({ data: mockData });

      await store.fetchStreak();

      expect(axios.get).toHaveBeenCalledWith('/api/user/streak');
      expect(store.currentStreak).toBe(5);
      expect(store.bestStreak).toBe(10);
      expect(store.streakLoaded).toBe(true);
    });

    it('handles API error gracefully', async () => {
      const store = useUserStatsStore();
      axios.get.mockRejectedValueOnce(new Error('API Error'));
      console.error = jest.fn(); // Mock console.error

      await store.fetchStreak();

      expect(axios.get).toHaveBeenCalledWith('/api/user/streak');
      expect(store.currentStreak).toBeNull();
      expect(store.bestStreak).toBeNull();
      expect(store.streakLoaded).toBe(true); // streakLoaded is true even on error, as per implementation
      expect(console.error).toHaveBeenCalledWith('Error fetching stats from backend', expect.any(Error));
    });

    it('fetches data on multiple calls', async () => {
        const store = useUserStatsStore();
        const mockData1 = { current_streak: 3, max_streak: 6 };
        const mockData2 = { current_streak: 4, max_streak: 8 };

        axios.get.mockResolvedValueOnce({ data: mockData1 });
        await store.fetchStreak();
        expect(store.currentStreak).toBe(3);
        expect(store.bestStreak).toBe(6);
        expect(axios.get).toHaveBeenCalledTimes(1);

        axios.get.mockResolvedValueOnce({ data: mockData2 });
        await store.fetchStreak();
        expect(store.currentStreak).toBe(4);
        expect(store.bestStreak).toBe(8);
        expect(axios.get).toHaveBeenCalledTimes(2); // Confirms axios.get was called again
      });
  });

  it('resetStats correctly resets the state', () => {
    const store = useUserStatsStore();
    // Set some initial state
    store.currentStreak = 5;
    store.bestStreak = 10;
    store.streakLoaded = true;

    store.resetStats();

    expect(store.currentStreak).toBeNull();
    expect(store.bestStreak).toBeNull();
    expect(store.streakLoaded).toBe(false);
  });
});
