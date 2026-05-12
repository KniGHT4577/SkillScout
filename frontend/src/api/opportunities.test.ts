import { describe, it, expect, vi, beforeEach } from 'vitest';
import { getOpportunities, getBookmarks, createBookmark, deleteBookmark } from './opportunities';
import { apiClient } from './client';

// Mock the apiClient
vi.mock('./client', () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('opportunities API', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('getOpportunities', () => {
    it('should call apiClient.get with the correct URL and params', async () => {
      const params = { q: 'react' };
      const mockResponse = { data: [{ id: 1, title: 'React Job' }] };
      vi.mocked(apiClient.get).mockResolvedValueOnce(mockResponse);

      const result = await getOpportunities(params);

      expect(apiClient.get).toHaveBeenCalledWith('/opportunities/', { params });
      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('getBookmarks', () => {
    it('should call apiClient.get with the correct URL', async () => {
      const mockResponse = { data: [{ id: 1, opportunity_id: 100 }] };
      vi.mocked(apiClient.get).mockResolvedValueOnce(mockResponse);

      const result = await getBookmarks();

      expect(apiClient.get).toHaveBeenCalledWith('/bookmarks/');
      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('createBookmark', () => {
    it('should call apiClient.post with the correct URL and body', async () => {
      const opportunityId = 999;
      const mockResponse = { data: { id: 1, opportunity_id: 999 } };
      vi.mocked(apiClient.post).mockResolvedValueOnce(mockResponse);

      const result = await createBookmark(opportunityId);

      expect(apiClient.post).toHaveBeenCalledWith('/bookmarks/', { opportunity_id: opportunityId });
      expect(result).toEqual(mockResponse.data);
    });
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
