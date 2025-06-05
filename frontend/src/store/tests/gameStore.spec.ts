import { setActivePinia, createPinia } from 'pinia';
import { useGameStore } from '../gameStore';
import { useUserStatsStore } from '../userStatsStore';
import axios from 'axios';

// Mock axios
jest.mock('axios');
// Mock userStatsStore
jest.mock('../userStatsStore', () => ({
  useUserStatsStore: jest.fn(() => ({
    setStreakData: jest.fn(),
  })),
}));

// Mock popupStore as it's used in loadRoom, though not directly in endGame
jest.mock('../popupStore', () => ({
    usePopupStore: jest.fn(() => ({
        showPopup: jest.fn(),
        showLibraryInstructions: jest.fn(),
    })),
}));

// Mock authStore as it's used in openRoom
jest.mock('../authStore', () => ({
    useAuthStore: jest.fn(() => ({
        cloudTokens: 0, // Provide a default value for cloudTokens
    })),
}));


describe('useGameStore', () => {
  let gameStore: ReturnType<typeof useGameStore>;
  let mockUserStatsStore: ReturnType<typeof useUserStatsStore>;

  const DEFAULT_SECTIONID_VALUE = -1000;

  beforeEach(() => {
    setActivePinia(createPinia());
    gameStore = useGameStore();
    mockUserStatsStore = useUserStatsStore();

    // Reset mocks and localStorage
    axios.post.mockClear();
    axios.get.mockClear(); // If fetchLibraryDetails or other GET requests are indirectly called
    (mockUserStatsStore.setStreakData as jest.Mock).mockClear();

    // Reset gameStore state to default for relevant properties
    gameStore.libraryId = null;
    gameStore.sectionId = DEFAULT_SECTIONID_VALUE;
    gameStore.completed = false;
    gameStore.incorrectQuestionAnswers = []; // Important for the guard in endGame
  });

  describe('endGame action', () => {
    it('calls userStatsStore.setStreakData with streak data from successful API response', async () => {
      gameStore.libraryId = 'lib1';
      gameStore.sectionId = 1;
      gameStore.incorrectQuestionAnswers = []; // Ensure this is empty to pass the guard

      const mockResponseData = {
        status: 'success',
        message: 'Game ended successfully.',
        current_streak: 7,
        highest_streak: 12,
      };
      axios.post.mockResolvedValueOnce({ data: mockResponseData });

      await gameStore.endGame();

      expect(axios.post).toHaveBeenCalledWith('/api/library/end', {
        libraryId: 'lib1',
        sectionId: 1,
      });
      expect(gameStore.completed).toBe(true);
      expect(gameStore.sectionId).toBe(DEFAULT_SECTIONID_VALUE); // Check if sectionId is reset
      expect(mockUserStatsStore.setStreakData).toHaveBeenCalledWith(7, 12);
    });

    it('does not call userStatsStore.setStreakData if API response is not successful', async () => {
      gameStore.libraryId = 'lib2';
      gameStore.sectionId = 2;
      gameStore.incorrectQuestionAnswers = [];

      const mockResponseData = {
        status: 'error',
        message: 'Failed to end game.',
      };
      axios.post.mockResolvedValueOnce({ data: mockResponseData });
      console.error = jest.fn(); // Mock console.error

      await gameStore.endGame();

      expect(axios.post).toHaveBeenCalledWith('/api/library/end', {
        libraryId: 'lib2',
        sectionId: 2,
      });
      expect(gameStore.completed).toBe(false); // Game should not be marked as completed
      expect(mockUserStatsStore.setStreakData).not.toHaveBeenCalled();
      expect(console.error).toHaveBeenCalledWith("Failed to end game:", "Failed to end game.");
    });

    it('does not call setStreakData if streak data is missing in successful API response', async () => {
      gameStore.libraryId = 'lib3';
      gameStore.sectionId = 3;
      gameStore.incorrectQuestionAnswers = [];

      const mockResponseData = {
        status: 'success',
        message: 'Game ended successfully.',
        // Missing current_streak and highest_streak
      };
      axios.post.mockResolvedValueOnce({ data: mockResponseData });

      await gameStore.endGame();

      expect(gameStore.completed).toBe(true);
      expect(mockUserStatsStore.setStreakData).not.toHaveBeenCalled();
    });

    it('handles API call failure gracefully', async () => {
      gameStore.libraryId = 'lib4';
      gameStore.sectionId = 4;
      gameStore.incorrectQuestionAnswers = [];

      axios.post.mockRejectedValueOnce(new Error('Network Error'));
      console.error = jest.fn(); // Mock console.error

      await gameStore.endGame();

      expect(gameStore.completed).toBe(false);
      expect(mockUserStatsStore.setStreakData).not.toHaveBeenCalled();
      expect(console.error).toHaveBeenCalledWith("Error sending game end data:", expect.any(Error));
    });

    it('does not proceed if incorrectQuestionAnswers has 4 or more items', async () => {
        gameStore.libraryId = 'lib5';
        gameStore.sectionId = 5;
        gameStore.incorrectQuestionAnswers = [1, 2, 3, 4]; // 4 items

        await gameStore.endGame();

        expect(axios.post).not.toHaveBeenCalled();
        expect(mockUserStatsStore.setStreakData).not.toHaveBeenCalled();
        expect(gameStore.completed).toBe(false);
    });
  });
});
