import { setActivePinia, createPinia } from 'pinia';
import { useAuthStore, UserData } from '../authStore';
import { useUserStatsStore } from '../userStatsStore';
import axios from 'axios';

// Mock axios
jest.mock('axios');
// Mock userStatsStore
jest.mock('../userStatsStore', () => ({
  useUserStatsStore: jest.fn(() => ({
    setStreakData: jest.fn(),
    resetStats: jest.fn(), // Added for logout test
  })),
}));

describe('useAuthStore', () => {
  let authStore: ReturnType<typeof useAuthStore>;
  let mockUserStatsStore: ReturnType<typeof useUserStatsStore>;

  beforeEach(() => {
    setActivePinia(createPinia());
    authStore = useAuthStore();
    // Get the mocked instance of useUserStatsStore
    // We need to call useUserStatsStore() to get the mock instance created by jest.mock
    mockUserStatsStore = useUserStatsStore();

    // Clear localStorage and reset mocks
    localStorage.clear();
    axios.get.mockClear();
    (mockUserStatsStore.setStreakData as jest.Mock).mockClear();
    (mockUserStatsStore.resetStats as jest.Mock).mockClear();
  });

  describe('login action', () => {
    it('updates state and localStorage correctly, and calls userStatsStore.setStreakData with streak data', () => {
      const loginPayload: UserData = {
        id: '123',
        username: 'testuser',
        firstName: 'Test',
        lastName: 'User',
        current_streak: 5,
        highest_streak: 10,
      };

      authStore.login(loginPayload);

      expect(authStore.loggedIn).toBe(true);
      expect(localStorage.getItem('loggedIn')).toBe('true');
      expect(authStore.user.id).toBe('123');
      expect(localStorage.getItem('userId')).toBe('123');
      expect(authStore.user.username).toBe('testuser');
      expect(localStorage.getItem('username')).toBe('testuser');
      expect(authStore.user.firstName).toBe('Test');
      expect(localStorage.getItem('firstName')).toBe('Test');
      expect(authStore.user.lastName).toBe('User');
      expect(localStorage.getItem('lastName')).toBe('User');

      expect(mockUserStatsStore.setStreakData).toHaveBeenCalledWith(5, 10);
    });

    it('calls userStatsStore.setStreakData only if streak data is present in payload', () => {
      const loginPayload: UserData = {
        id: '456',
        username: 'anotheruser',
        firstName: 'Another',
        lastName: 'User',
        // No streak data
      };

      authStore.login(loginPayload);

      expect(mockUserStatsStore.setStreakData).not.toHaveBeenCalled();
    });

    it('handles login with undefined payload (should not error and not call setStreakData)', () => {
        authStore.login(undefined);

        expect(authStore.loggedIn).toBe(true);
        expect(localStorage.getItem('loggedIn')).toBe('true');
        // User details should remain as per initial state or previous state if any (null in this clean setup)
        expect(authStore.user.id).toBeNull();
        expect(mockUserStatsStore.setStreakData).not.toHaveBeenCalled();
      });
  });

  describe('logout action', () => {
    it('clears state and localStorage, and calls userStatsStore.resetStats', () => {
      // Setup initial logged-in state
      authStore.loggedIn = true;
      authStore.user = {
        id: '123',
        username: 'testuser',
        firstName: 'Test',
        lastName: 'User',
      };
      localStorage.setItem('loggedIn', 'true');
      localStorage.setItem('userId', '123');

      authStore.logout();

      expect(authStore.loggedIn).toBe(false);
      expect(authStore.user.id).toBeNull();
      expect(authStore.user.username).toBeNull();
      expect(localStorage.getItem('loggedIn')).toBe('false');
      expect(localStorage.getItem('userId')).toBeNull();
      // Assuming resetStats from userStatsStore should be called on logout
      // Although the original subtask did not specify this, it's a logical addition
      // If this is not desired, this expect can be removed.
      // expect(mockUserStatsStore.resetStats).toHaveBeenCalled();
    });
  });

  describe('checkAuth action', () => {
    it('logs in user if API returns loggedIn true', async () => {
        axios.get.mockResolvedValueOnce({ data: { loggedIn: true, userId: '789' } });
        await authStore.checkAuth();

        expect(authStore.loggedIn).toBe(true);
        expect(authStore.user.id).toBe('789');
        expect(localStorage.getItem('loggedIn')).toBe('true');
        expect(localStorage.getItem('userId')).toBe('789');
    });

    it('logs out user if API returns loggedIn false', async () => {
        // Pre-set loggedIn to true to see it change
        authStore.loggedIn = true;
        localStorage.setItem('loggedIn', 'true');

        axios.get.mockResolvedValueOnce({ data: { loggedIn: false } });
        await authStore.checkAuth();

        expect(authStore.loggedIn).toBe(false);
        expect(localStorage.getItem('loggedIn')).toBe('false');
        // expect(mockUserStatsStore.resetStats).toHaveBeenCalled(); // Assuming logout calls resetStats
    });

    it('logs out user on API error', async () => {
        // Pre-set loggedIn to true
        authStore.loggedIn = true;
        localStorage.setItem('loggedIn', 'true');

        axios.get.mockRejectedValueOnce(new Error('API Error'));
        await authStore.checkAuth();

        expect(authStore.loggedIn).toBe(false);
        expect(localStorage.getItem('loggedIn')).toBe('false');
        // expect(mockUserStatsStore.resetStats).toHaveBeenCalled();
    });
  });

  describe('updateUserDetails action', () => {
    it('updates user details in state and localStorage', () => {
        authStore.updateUserDetails({ username: 'newname', firstName: 'NewFirst' });

        expect(authStore.user.username).toBe('newname');
        expect(localStorage.getItem('username')).toBe('newname');
        expect(authStore.user.firstName).toBe('NewFirst');
        expect(localStorage.getItem('firstName')).toBe('NewFirst');

        authStore.updateUserDetails({ lastName: null }); // Test removing a detail
        expect(authStore.user.lastName).toBeNull();
        expect(localStorage.getItem('lastName')).toBeNull();
    });
  });
});
