import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useAuthStore } from './useAuthStore';

describe('useAuthStore', () => {
  beforeEach(() => {
    // Clear localStorage
    localStorage.clear();
    // Reset store state
    useAuthStore.setState({
      user: null,
      token: null,
      isAuthenticated: false,
    });
    vi.clearAllMocks();
  });

  it('should have correct initial state', () => {
    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.token).toBeNull();
    expect(state.isAuthenticated).toBe(false);
  });

  it('should set auth data correctly and save token to localStorage', () => {
    const user = { id: 1, email: 'test@example.com', full_name: 'Test User' };
    const token = 'fake-jwt-token';

    const setItemSpy = vi.spyOn(Storage.prototype, 'setItem');

    useAuthStore.getState().setAuth(user, token);

    const state = useAuthStore.getState();
    expect(state.user).toEqual(user);
    expect(state.token).toBe(token);
    expect(state.isAuthenticated).toBe(true);

    // Verify manual localStorage.setItem was called
    expect(setItemSpy).toHaveBeenCalledWith('token', token);
  });

  it('should clear auth data and remove token from localStorage on logout', () => {
    const user = { id: 1, email: 'test@example.com', full_name: 'Test User' };
    const token = 'fake-jwt-token';

    useAuthStore.setState({
      user,
      token,
      isAuthenticated: true,
    });
    localStorage.setItem('token', token);

    const removeItemSpy = vi.spyOn(Storage.prototype, 'removeItem');

    useAuthStore.getState().logout();

    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.token).toBeNull();
    expect(state.isAuthenticated).toBe(false);

    // Verify manual localStorage.removeItem was called
    expect(removeItemSpy).toHaveBeenCalledWith('token');
  });
});
