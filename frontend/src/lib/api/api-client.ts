/**
 * Client API centralisé pour toutes les requêtes au backend
 * Gère l'authentification, les intercepteurs et le formatage des réponses
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';

// URL de base de l'API, définie dans le fichier .env
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Configuration par défaut
const config: AxiosRequestConfig = {
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 secondes de timeout par défaut
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
};

// Création de l'instance Axios
const axiosInstance: AxiosInstance = axios.create(config);

// Intercepteur pour ajouter le token d'authentification
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Intercepteur pour gérer les réponses
axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => response.data,
  (error: AxiosError) => {
    // Gestion des erreurs selon le statut HTTP
    if (error.response) {
      const { status } = error.response;
      
      // Erreur d'authentification
      if (status === 401) {
        // Redirection vers la page de login si l'utilisateur n'est pas authentifié
        localStorage.removeItem('auth_token');
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      }

      // Erreur d'autorisation
      if (status === 403) {
        console.error('Accès non autorisé');
      }

      // Erreur de validation
      if (status === 422) {
        console.error('Données invalides', error.response.data);
      }

      // Erreur serveur
      if (status >= 500) {
        console.error('Erreur serveur', error.response.data);
      }
    } else if (error.request) {
      // La requête a été envoyée mais aucune réponse n'a été reçue
      console.error('Aucune réponse reçue du serveur', error.request);
    } else {
      // Une erreur est survenue lors de la configuration de la requête
      console.error('Erreur de configuration de la requête', error.message);
    }

    // On rejette la promesse pour que le code appelant puisse gérer l'erreur
    return Promise.reject(error);
  }
);

// API client avec les méthodes HTTP courantes
const apiClient = {
  /**
   * Méthode GET
   */
  get: <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    return axiosInstance.get(url, config);
  },

  /**
   * Méthode POST
   */
  post: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    return axiosInstance.post(url, data, config);
  },

  /**
   * Méthode PUT
   */
  put: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    return axiosInstance.put(url, data, config);
  },

  /**
   * Méthode PATCH
   */
  patch: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    return axiosInstance.patch(url, data, config);
  },

  /**
   * Méthode DELETE
   */
  delete: <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    return axiosInstance.delete(url, config);
  }
};

export default apiClient;
