import React from 'react';
import { Routes, Route } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';

import Header from './components/Header';
import Home from './pages/Home';
import Upload from './pages/Upload';
import About from './pages/About';
import Footer from './components/Footer';

const AppContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
`;

const MainContent = styled(motion.main)`
  flex: 1;
  padding: 20px 0;
`;

function App() {
  return (
    <AppContainer>
      <Header />
      <MainContent
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </MainContent>
      <Footer />
    </AppContainer>
  );
}

export default App; 