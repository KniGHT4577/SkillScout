import { describe, it, expect, vi, beforeEach } from 'vitest';
import { deleteBookmark } from './opportunities';
import { apiClient } from './client';

// Mock the apiClient
vi.mock('./client', () => ({
  apiClient: {
    delete: vi.fn(),
  },
}));

describe('opportunities API', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('deleteBookmark', () => {
    it('should call apiClient.delete with the correct URL', async () => {
      const opportunityId = 123;
      const mockResponse = { data: { success: true } };

      // Setup the mock to return a promise that resolves to our mockResponse
      vi.mocked(apiClient.delete).mockResolvedValueOnce(mockResponse);

      const result = await deleteBookmark(opportunityId);

      // Verify the api client was called correctly
      expect(apiClient.delete).toHaveBeenCalledWith(`/bookmarks/${opportunityId}`);
      expect(apiClient.delete).toHaveBeenCalledTimes(1);

      // Verify it returns the data property from the response
      expect(result).toEqual(mockResponse.data);
    });

    it('should throw an error if the API call fails', async () => {
      const opportunityId = 456;
      const mockError = new Error('Network error');

      vi.mocked(apiClient.delete).mockRejectedValueOnce(mockError);

      await expect(deleteBookmark(opportunityId)).rejects.toThrow('Network error');
    });
  });
});
