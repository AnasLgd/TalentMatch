import { uploadService, UploadErrorType, UPLOAD_CONFIG } from '../upload-service';
import apiClient from '@/lib/api/api-client';

// Mock du module api-client
jest.mock('@/lib/api/api-client');

describe('uploadService', () => {
  // Configuration des mocks
  const mockApiClient = apiClient as jest.Mocked<typeof apiClient>;
  
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  describe('validateFile', () => {
    it('devrait valider un fichier correctement formaté', () => {
      // Arrange
      const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' });
      
      // Act
      const result = uploadService.validateFile(file);
      
      // Assert
      expect(result).toBeNull();
    });
    
    it('devrait rejeter un fichier avec un format non supporté', () => {
      // Arrange
      const file = new File(['test content'], 'test.txt', { type: 'text/plain' });
      
      // Act
      const result = uploadService.validateFile(file);
      
      // Assert
      expect(result).not.toBeNull();
      expect(result?.type).toBe(UploadErrorType.FORMAT_INVALID);
      expect(result?.message).toContain('Format d\'image non pris en charge');
    });
    
    it('devrait rejeter un fichier trop volumineux', () => {
      // Arrange - Simuler un fichier de 6MB
      const largeContent = 'x'.repeat(6 * 1024 * 1024);
      const file = new File([largeContent], 'large.jpg', { type: 'image/jpeg' });
      Object.defineProperty(file, 'size', { value: 6 * 1024 * 1024 });
      
      // Act
      const result = uploadService.validateFile(file);
      
      // Assert
      expect(result).not.toBeNull();
      expect(result?.type).toBe(UploadErrorType.SIZE_EXCEEDED);
      expect(result?.message).toContain('Taille d\'image trop importante');
    });
  });
  
  describe('uploadFile', () => {
    it('devrait télécharger un fichier avec succès', async () => {
      // Arrange
      const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' });
      const expectedUrl = 'https://minio.example.com/profiles/test.jpg';
      mockApiClient.post.mockResolvedValue({ url: expectedUrl });
      
      // Act
      const result = await uploadService.uploadFile(file);
      
      // Assert
      expect(result).toBe(expectedUrl);
      expect(mockApiClient.post).toHaveBeenCalledWith(
        '/upload',
        expect.any(FormData),
        expect.objectContaining({
          headers: { 'Content-Type': 'multipart/form-data' }
        })
      );
    });
    
    it('devrait spécifier le bon dossier lors de l\'upload', async () => {
      // Arrange
      const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' });
      const folder = 'custom-folder';
      const expectedUrl = 'https://minio.example.com/custom-folder/test.jpg';
      mockApiClient.post.mockResolvedValue({ url: expectedUrl });
      
      // Mock FormData.append pour vérifier les arguments
      const originalAppend = FormData.prototype.append;
      const appendMock = jest.fn();
      FormData.prototype.append = appendMock;
      
      // Act
      const result = await uploadService.uploadFile(file, folder);
      
      // Assert
      expect(result).toBe(expectedUrl);
      expect(appendMock).toHaveBeenCalledWith('folder', folder);
      
      // Restaurer la méthode originale
      FormData.prototype.append = originalAppend;
    });
    
    it('devrait lever une erreur si la validation échoue', async () => {
      // Arrange
      const file = new File(['test content'], 'test.txt', { type: 'text/plain' });
      
      // Act & Assert
      await expect(uploadService.uploadFile(file)).rejects.toEqual(
        expect.objectContaining({
          type: UploadErrorType.FORMAT_INVALID
        })
      );
      expect(mockApiClient.post).not.toHaveBeenCalled();
    });
    
    it('devrait propager les erreurs du serveur', async () => {
      // Arrange
      const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' });
      mockApiClient.post.mockRejectedValue(new Error('Server error'));
      
      // Act & Assert
      await expect(uploadService.uploadFile(file)).rejects.toThrow('Impossible de télécharger le fichier');
    });
  });
  
  describe('deleteFile', () => {
    it('devrait supprimer un fichier avec succès', async () => {
      // Arrange
      const fileUrl = 'https://minio.example.com/profiles/test.jpg';
      mockApiClient.delete.mockResolvedValue({});
      
      // Act
      await uploadService.deleteFile(fileUrl);
      
      // Assert
      expect(mockApiClient.delete).toHaveBeenCalled();
      const deleteArg = mockApiClient.delete.mock.calls[0][0];
      expect(deleteArg).toContain('profiles/test.jpg');
    });
    
    it('devrait propager les erreurs du serveur lors de la suppression', async () => {
      // Arrange
      const fileUrl = 'https://minio.example.com/profiles/test.jpg';
      mockApiClient.delete.mockRejectedValue(new Error('Server error'));
      
      // Act & Assert
      await expect(uploadService.deleteFile(fileUrl)).rejects.toThrow('Impossible de supprimer le fichier');
    });
  });
});