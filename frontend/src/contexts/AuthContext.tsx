'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { AuthAPI, SignInResponse } from '@/lib/auth';

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  accessToken: string | null;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // Load tokens from localStorage on mount
  useEffect(() => {
    const storedAccessToken = localStorage.getItem('access_token');
    const storedRefreshToken = localStorage.getItem('refresh_token');

    if (storedAccessToken) {
      setAccessToken(storedAccessToken);
    }
    if (storedRefreshToken) {
      setRefreshToken(storedRefreshToken);
    }

    setIsLoading(false);
  }, []);

  // Auto-refresh token before expiry
  useEffect(() => {
    if (!refreshToken) return;

    // Refresh token every 50 minutes (tokens expire in 60 minutes)
    const interval = setInterval(
      async () => {
        try {
          const response = await AuthAPI.refreshToken({ refresh_token: refreshToken });
          setAccessToken(response.access_token);
          localStorage.setItem('access_token', response.access_token);
        } catch (error) {
          console.error('Token refresh failed:', error);
          // If refresh fails, sign out
          handleSignOut();
        }
      },
      50 * 60 * 1000
    ); // 50 minutes

    return () => clearInterval(interval);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [refreshToken]);

  const handleSignIn = async (email: string, password: string) => {
    const response = await AuthAPI.signIn({ email, password });
    setAccessToken(response.access_token);
    setRefreshToken(response.refresh_token);
    localStorage.setItem('access_token', response.access_token);
    localStorage.setItem('refresh_token', response.refresh_token);
    localStorage.setItem('id_token', response.id_token);
  };

  const handleSignOut = async () => {
    try {
      if (accessToken) {
        await AuthAPI.signOut(accessToken);
      }
    } catch (error) {
      console.error('Sign out error:', error);
    } finally {
      setAccessToken(null);
      setRefreshToken(null);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('id_token');
      router.push('/auth/signin');
    }
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: !!accessToken,
        isLoading,
        accessToken,
        signIn: handleSignIn,
        signOut: handleSignOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
