// Import de @testing-library/jest-dom pour ajouter les matchers personnalisés
import '@testing-library/jest-dom';

// Mock global pour URL.createObjectURL
global.URL.createObjectURL = jest.fn(() => 'mock-blob-url');

// Mock des variables d'environnement
global.process.env = {
  ...process.env,
  VITE_API_BASE_URL: 'http://localhost:8000/api',
};

// Supprimer tous les mocks après chaque test
afterEach(() => {
  jest.clearAllMocks();
});

// Éviter les erreurs console pendant les tests
const originalConsoleError = console.error;
console.error = (...args) => {
  if (
    typeof args[0] === 'string' &&
    (args[0].includes('Warning: ReactDOM.render') ||
     args[0].includes('Error: Not implemented'))
  ) {
    return;
  }
  originalConsoleError(...args);
};