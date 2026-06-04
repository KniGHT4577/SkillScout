import { describe, it, expect, vi, afterEach } from 'vitest';
import { signup, login, getMe } from './auth';
import { apiClient } from './client';

// Mock the apiClient module
vi.mock('./client', () => ({
  apiClient: {
    post: vi.fn(),
    get: vi.fn(),
  },
}));

describe('auth API', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('signup', () => {
    it('should call apiClient.post with correct arguments and return data', async () => {
      const mockData = { email: 'test@example.com', password: 'password123', name: 'Test User' };
      const mockResponse = { data: { id: 1, ...mockData } };

      // Setup the mock implementation
      vi.mocked(apiClient.post).mockResolvedValueOnce(mockResponse);

      // Call the function
      const result = await signup(mockData);

      // Verify expectations
      expect(apiClient.post).toHaveBeenCalledTimes(1);
      expect(apiClient.post).toHaveBeenCalledWith('/auth/signup', mockData);
      expect(result).toEqual(mockResponse.data);
    });

    it('should throw an error if the request fails', async () => {
      const mockData = { email: 'test@example.com', password: 'password123' };
      const mockError = new Error('Network Error');

      // Setup the mock implementation
      vi.mocked(apiClient.post).mockRejectedValueOnce(mockError);

      // Verify the function throws
      await expect(signup(mockData)).rejects.toThrow('Network Error');
    });
  });

  describe('login', () => {
    it('should call apiClient.post with correct form data and return data', async () => {
      const mockData = { email: 'test@example.com', password: 'password123' };
      const mockResponse = { data: { access_token: 'fake-token' } };

      // Setup the mock implementation
      vi.mocked(apiClient.post).mockResolvedValueOnce(mockResponse);

      // Call the function
      const result = await login(mockData);

      // Verify expectations
      expect(apiClient.post).toHaveBeenCalledTimes(1);

      // Verify URLSearchParams
      const expectedFormData = new URLSearchParams();
      expectedFormData.append('username', mockData.email);
      expectedFormData.append('password', mockData.password);

      expect(apiClient.post).toHaveBeenCalledWith('/auth/login', expectedFormData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('getMe', () => {
    it('should call apiClient.get and return data', async () => {
      const mockResponse = { data: { id: 1, email: 'test@example.com' } };

      // Setup the mock implementation
      vi.mocked(apiClient.get).mockResolvedValueOnce(mockResponse);

      // Call the function
      const result = await getMe();

      // Verify expectations
      expect(apiClient.get).toHaveBeenCalledTimes(1);
      expect(apiClient.get).toHaveBeenCalledWith('/users/me');
      expect(result).toEqual(mockResponse.data);
    });
  });
});
