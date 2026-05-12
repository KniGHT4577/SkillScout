import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import MockAdapter from 'axios-mock-adapter';
import { apiClient } from './client';
import { getBookmarks } from './opportunities';

describe('opportunities API', () => {
  let mock: MockAdapter;

  beforeEach(() => {
    mock = new MockAdapter(apiClient);
  });

  afterEach(() => {
    mock.restore();
  });

  describe('getBookmarks', () => {
    it('should fetch bookmarks successfully', async () => {
      const mockData = [
        { id: 1, title: 'Bookmark 1' },
        { id: 2, title: 'Bookmark 2' },
      ];

      mock.onGet('/bookmarks/').reply(200, mockData);

      const result = await getBookmarks();

      expect(mock.history.get.length).toBe(1);
      expect(mock.history.get[0].url).toBe('/bookmarks/');
      expect(result).toEqual(mockData);
    });

    it('should throw an error if the request fails', async () => {
      mock.onGet('/bookmarks/').reply(500);

      await expect(getBookmarks()).rejects.toThrow();
      expect(mock.history.get.length).toBe(1);
      expect(mock.history.get[0].url).toBe('/bookmarks/');
    });
  });
});
