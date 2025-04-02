
import React, { createContext, useContext, useState, useEffect } from "react";

interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Vérifie si l'utilisateur est déjà connecté au chargement
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        // Simulons la récupération du token et des informations utilisateur
        const token = localStorage.getItem("auth_token");
        if (token) {
          // Dans une implémentation réelle, vous vérifieriez le token auprès du backend
          // Pour l'instant, simulons un utilisateur connecté
          setUser({
            id: "1",
            name: "John Doe",
            email: "john.doe@example.com",
            role: "admin"
          });
        }
      } catch (err) {
        console.error("Erreur lors de la vérification de l'authentification:", err);
        setError("Erreur d'authentification");
      } finally {
        setIsLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    try {
      // Simulons un appel d'API pour l'authentification
      // Dans une implémentation réelle, vous feriez un appel à votre backend
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Vérification simple pour la démo
      if (email === "demo@example.com" && password === "password") {
        const user = {
          id: "1",
          name: "John Doe",
          email: "john.doe@example.com",
          role: "admin"
        };
        
        // Stockage du token (simulé)
        localStorage.setItem("auth_token", "fake-jwt-token");
        
        setUser(user);
      } else {
        throw new Error("Identifiants invalides");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur d'authentification");
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem("auth_token");
    setUser(null);
  };

  const value = {
    user,
    isLoading,
    error,
    login,
    logout,
    isAuthenticated: !!user
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
