import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { logout as apiLogout } from '@/api/auth';

interface User {
  id: number;
  email: string;
  full_name?: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  setAuth: (user: User) => void;
  logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      setAuth: (user) => {
        set({ user, isAuthenticated: true });
      },
      logout: async () => {
        try {
          await apiLogout();
        } catch (error) {
          console.error("Logout API failed", error);
        } finally {
          set({ user: null, isAuthenticated: false });
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user, isAuthenticated: state.isAuthenticated }),
    }
  )
);
