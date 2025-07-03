import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiMenu, FiX, FiShield, FiMapPin } from 'react-icons/fi';

const HeaderContainer = styled.header`
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  position: sticky;
  top: 0;
  z-index: 1000;
`;

const Nav = styled.nav`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
`;

const Logo = styled(Link)`
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #333;
  font-size: 24px;
  font-weight: 700;
  
  &:hover {
    color: #667eea;
  }
`;

const LogoIcon = styled.div`
  display: flex;
  align-items: center;
  gap: 5px;
`;

const NavLinks = styled.div`
  display: flex;
  align-items: center;
  gap: 30px;
  
  @media (max-width: 768px) {
    display: none;
  }
`;

const NavLink = styled(Link)`
  text-decoration: none;
  color: #333;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.2s ease;
  position: relative;
  
  &:hover {
    color: #667eea;
    background: rgba(102, 126, 234, 0.1);
  }
  
  &.active {
    color: #667eea;
    background: rgba(102, 126, 234, 0.1);
  }
`;

const MobileMenuButton = styled.button`
  display: none;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #333;
  
  @media (max-width: 768px) {
    display: block;
  }
`;

const MobileMenu = styled(motion.div)`
  position: fixed;
  top: 70px;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  
  @media (min-width: 769px) {
    display: none;
  }
`;

const MobileNavLink = styled(Link)`
  text-decoration: none;
  color: #333;
  font-weight: 500;
  padding: 12px 16px;
  border-radius: 8px;
  transition: all 0.2s ease;
  
  &:hover {
    color: #667eea;
    background: rgba(102, 126, 234, 0.1);
  }
  
  &.active {
    color: #667eea;
    background: rgba(102, 126, 234, 0.1);
  }
`;

function Header() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  const isActive = (path) => location.pathname === path;

  return (
    <HeaderContainer>
      <Nav>
        <Logo to="/">
          <LogoIcon>
            <FiShield size={28} />
            <FiMapPin size={20} />
          </LogoIcon>
          GeoMask
        </Logo>

        <NavLinks>
          <NavLink to="/" className={isActive('/') ? 'active' : ''}>
            Home
          </NavLink>
          <NavLink to="/upload" className={isActive('/upload') ? 'active' : ''}>
            Upload Photo
          </NavLink>
          <NavLink to="/about" className={isActive('/about') ? 'active' : ''}>
            About
          </NavLink>
        </NavLinks>

        <MobileMenuButton onClick={toggleMobileMenu}>
          {isMobileMenuOpen ? <FiX /> : <FiMenu />}
        </MobileMenuButton>
      </Nav>

      {isMobileMenuOpen && (
        <MobileMenu
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.2 }}
        >
          <MobileNavLink 
            to="/" 
            className={isActive('/') ? 'active' : ''}
            onClick={closeMobileMenu}
          >
            Home
          </MobileNavLink>
          <MobileNavLink 
            to="/upload" 
            className={isActive('/upload') ? 'active' : ''}
            onClick={closeMobileMenu}
          >
            Upload Photo
          </MobileNavLink>
          <MobileNavLink 
            to="/about" 
            className={isActive('/about') ? 'active' : ''}
            onClick={closeMobileMenu}
          >
            About
          </MobileNavLink>
        </MobileMenu>
      )}
    </HeaderContainer>
  );
}

export default Header; 