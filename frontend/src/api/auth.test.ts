import { describe, it, expect, vi, beforeEach } from 'vitest';
import { login } from './auth';
import { apiClient } from './client';

// Mock the apiClient module
vi.mock('./client', () => ({
  apiClient: {
    post: vi.fn(),
  },
}));

describe('auth API', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('login', () => {
    it('should send a POST request to /auth/login with urlencoded form data', async () => {
      // Setup mock response
      const mockResponse = { data: { token: 'fake-token' } };
      (apiClient.post as any).mockResolvedValue(mockResponse);

      // Input data
      const inputData = {
        email: 'test@example.com',
        password: 'password123',
      };

      // Call the function
      const result = await login(inputData);

      // Verify the result
      expect(result).toEqual(mockResponse.data);

      // Verify the post was called correctly
      expect(apiClient.post).toHaveBeenCalledTimes(1);

      const [url, data, config] = (apiClient.post as any).mock.calls[0];

      // Check URL
      expect(url).toBe('/auth/login');

      // Check data is URLSearchParams with correct values
      expect(data).toBeInstanceOf(URLSearchParams);
      expect(data.get('username')).toBe(inputData.email);
      expect(data.get('password')).toBe(inputData.password);

      // Check config headers
      expect(config).toEqual({
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });
    });

    it('should propagate errors from the API client', async () => {
      // Setup mock error
      const mockError = new Error('Network error');
      (apiClient.post as any).mockRejectedValue(mockError);

      // Call the function and expect it to throw
      await expect(login({ email: 'test@example.com', password: 'password123' })).rejects.toThrow('Network error');
    });
  });
});
