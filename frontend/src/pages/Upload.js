import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { FiUpload, FiImage, FiDownload, FiSettings, FiCheck } from 'react-icons/fi';
import toast from 'react-hot-toast';
import axios from 'axios';

const UploadContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
`;

const UploadCard = styled(motion.div)`
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
`;

const UploadHeader = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px;
  text-align: center;
`;

const UploadTitle = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 10px;
  
  @media (max-width: 768px) {
    font-size: 2rem;
  }
`;

const UploadSubtitle = styled.p`
  font-size: 1.1rem;
  opacity: 0.9;
`;

const UploadContent = styled.div`
  padding: 40px;
`;

const DropzoneContainer = styled.div`
  border: 3px dashed #e1e5e9;
  border-radius: 16px;
  padding: 60px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f8f9fa;
  
  &:hover {
    border-color: #667eea;
    background: rgba(102, 126, 234, 0.05);
  }
  
  &.drag-active {
    border-color: #667eea;
    background: rgba(102, 126, 234, 0.1);
  }
`;

const DropzoneIcon = styled.div`
  font-size: 4rem;
  color: #667eea;
  margin-bottom: 20px;
`;

const DropzoneText = styled.div`
  h3 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 10px;
    color: #333;
  }
  
  p {
    color: #666;
    font-size: 1rem;
  }
`;

const ImagePreview = styled.div`
  margin: 30px 0;
  text-align: center;
`;

const PreviewImage = styled.img`
  max-width: 100%;
  max-height: 400px;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
`;

const SceneSelection = styled.div`
  margin: 30px 0;
`;

const SectionTitle = styled.h3`
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: #333;
`;

const SceneGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
`;

const SceneOption = styled.div`
  padding: 15px;
  border: 2px solid ${props => props.selected ? '#667eea' : '#e1e5e9'};
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: ${props => props.selected ? 'rgba(102, 126, 234, 0.1)' : 'white'};
  
  &:hover {
    border-color: #667eea;
    background: rgba(102, 126, 234, 0.05);
  }
`;

const SceneName = styled.div`
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
`;

const SceneDescription = styled.div`
  font-size: 0.9rem;
  color: #666;
`;

const CustomPromptInput = styled.textarea`
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 16px;
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const ProcessButton = styled(motion.button)`
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const LoadingSpinner = styled.div`
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
`;

const ResultSection = styled(motion.div)`
  margin-top: 30px;
  padding: 30px;
  background: #f8f9fa;
  border-radius: 16px;
  text-align: center;
`;

const DownloadButton = styled.a`
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);
  }
`;

const scenes = [
  { id: 'random', name: 'Random Location', description: 'AI chooses a random scene' },
  { id: 'city', name: 'Cityscape', description: 'Urban city view' },
  { id: 'mountain', name: 'Mountain Village', description: 'Swiss mountain village' },
  { id: 'beach', name: 'Beach', description: 'Tropical beach scene' },
  { id: 'forest', name: 'Forest', description: 'Dense forest view' },
  { id: 'desert', name: 'Desert', description: 'Desert landscape' },
  { id: 'custom', name: 'Custom', description: 'Describe your own scene' }
];

function Upload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedScene, setSelectedScene] = useState('random');
  const [customPrompt, setCustomPrompt] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [processedImage, setProcessedImage] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) { // 10MB limit
        toast.error('File size must be less than 10MB');
        return;
      }
      
      if (!file.type.startsWith('image/')) {
        toast.error('Please upload an image file');
        return;
      }
      
      setSelectedFile(file);
      setProcessedImage(null);
      toast.success('Image uploaded successfully!');
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp']
    },
    multiple: false
  });

  const handleProcess = async () => {
    if (!selectedFile) {
      toast.error('Please upload an image first');
      return;
    }

    setIsProcessing(true);
    
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('scene_type', selectedScene);
      formData.append('custom_prompt', customPrompt);

      const response = await axios.post('/api/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        setProcessedImage(response.data);
        toast.success('Image processed successfully!');
      } else {
        toast.error('Failed to process image');
      }
    } catch (error) {
      console.error('Error processing image:', error);
      toast.error(error.response?.data?.detail || 'Failed to process image');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownload = () => {
    if (processedImage?.download_url) {
      window.open(processedImage.download_url, '_blank');
    }
  };

  return (
    <UploadContainer>
      <UploadCard
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <UploadHeader>
          <UploadTitle>Upload & Protect</UploadTitle>
          <UploadSubtitle>
            Upload your photo and let AI replace the background with a decoy scene
          </UploadSubtitle>
        </UploadHeader>

        <UploadContent>
          <DropzoneContainer
            {...getRootProps()}
            className={isDragActive ? 'drag-active' : ''}
          >
            <input {...getInputProps()} />
            <DropzoneIcon>
              {selectedFile ? <FiImage /> : <FiUpload />}
            </DropzoneIcon>
            <DropzoneText>
              {selectedFile ? (
                <>
                  <h3>Image Selected</h3>
                  <p>{selectedFile.name}</p>
                </>
              ) : (
                <>
                  <h3>Drop your image here</h3>
                  <p>or click to browse files</p>
                </>
              )}
            </DropzoneText>
          </DropzoneContainer>

          {selectedFile && (
            <ImagePreview>
              <PreviewImage
                src={URL.createObjectURL(selectedFile)}
                alt="Preview"
              />
            </ImagePreview>
          )}

          {selectedFile && (
            <SceneSelection>
              <SectionTitle>Choose Scene Type</SectionTitle>
              <SceneGrid>
                {scenes.map((scene) => (
                  <SceneOption
                    key={scene.id}
                    selected={selectedScene === scene.id}
                    onClick={() => setSelectedScene(scene.id)}
                  >
                    <SceneName>{scene.name}</SceneName>
                    <SceneDescription>{scene.description}</SceneDescription>
                  </SceneOption>
                ))}
              </SceneGrid>

              {selectedScene === 'custom' && (
                <div>
                  <SectionTitle>Custom Scene Description</SectionTitle>
                  <CustomPromptInput
                    placeholder="Describe the scene you want (e.g., 'A cozy coffee shop in Paris with Eiffel Tower view')"
                    value={customPrompt}
                    onChange={(e) => setCustomPrompt(e.target.value)}
                  />
                </div>
              )}

              <ProcessButton
                onClick={handleProcess}
                disabled={isProcessing || (selectedScene === 'custom' && !customPrompt.trim())}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                {isProcessing ? (
                  <>
                    <LoadingSpinner />
                    Processing...
                  </>
                ) : (
                  <>
                    <FiSettings />
                    Process Image
                  </>
                )}
              </ProcessButton>
            </SceneSelection>
          )}

          <AnimatePresence>
            {processedImage && (
              <ResultSection
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <h3>✅ Processing Complete!</h3>
                <p>Your image has been processed and is ready for download.</p>
                <DownloadButton
                  href={processedImage.download_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={handleDownload}
                >
                  <FiDownload />
                  Download Protected Image
                </DownloadButton>
              </ResultSection>
            )}
          </AnimatePresence>
        </UploadContent>
      </UploadCard>
    </UploadContainer>
  );
}

export default Upload; 