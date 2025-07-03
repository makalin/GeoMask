import React from 'react';
import styled from 'styled-components';
import { FiGithub, FiTwitter, FiMail } from 'react-icons/fi';

const FooterContainer = styled.footer`
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  padding: 40px 0 20px;
  margin-top: auto;
`;

const FooterContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
`;

const FooterSection = styled.div`
  h3 {
    color: #333;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 15px;
  }
  
  p {
    color: #666;
    line-height: 1.6;
    margin-bottom: 10px;
  }
`;

const SocialLinks = styled.div`
  display: flex;
  gap: 15px;
  margin-top: 15px;
`;

const SocialLink = styled.a`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  text-decoration: none;
  transition: transform 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
  }
`;

const FooterBottom = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 20px 0;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  margin-top: 30px;
  text-align: center;
  color: #666;
  font-size: 14px;
`;

const Link = styled.a`
  color: #667eea;
  text-decoration: none;
  
  &:hover {
    text-decoration: underline;
  }
`;

function Footer() {
  return (
    <FooterContainer>
      <FooterContent>
        <FooterSection>
          <h3>GeoMask</h3>
          <p>
            Protect your privacy from AI-powered GeoGuessr tools by automatically 
            replacing identifiable background views with AI-generated decoy scenes.
          </p>
          <SocialLinks>
            <SocialLink href="https://github.com/makalin/GeoMask" target="_blank" rel="noopener noreferrer">
              <FiGithub size={20} />
            </SocialLink>
            <SocialLink href="https://twitter.com/geomask" target="_blank" rel="noopener noreferrer">
              <FiTwitter size={20} />
            </SocialLink>
            <SocialLink href="mailto:contact@geomask.app">
              <FiMail size={20} />
            </SocialLink>
          </SocialLinks>
        </FooterSection>

        <FooterSection>
          <h3>Features</h3>
          <p>🌐 Replace window views with AI-generated decoy locations</p>
          <p>🏙️ Choose from presets: cityscapes, nature, mountains</p>
          <p>🔒 Prevent AI-based geolocation or doxxing</p>
          <p>🖼️ High-resolution output ready for social media</p>
        </FooterSection>

        <FooterSection>
          <h3>Quick Links</h3>
          <p><Link href="/upload">Upload Photo</Link></p>
          <p><Link href="/about">About GeoMask</Link></p>
          <p><Link href="https://github.com/makalin/GeoMask" target="_blank" rel="noopener noreferrer">GitHub</Link></p>
          <p><Link href="/privacy">Privacy Policy</Link></p>
        </FooterSection>

        <FooterSection>
          <h3>Support</h3>
          <p>Need help? Contact us for support and feature requests.</p>
          <p>Email: <Link href="mailto:support@geomask.app">support@geomask.app</Link></p>
          <p>GitHub Issues: <Link href="https://github.com/makalin/GeoMask/issues" target="_blank" rel="noopener noreferrer">Report Bug</Link></p>
        </FooterSection>
      </FooterContent>

      <FooterBottom>
        <p>
          © 2024 GeoMask. Made with ❤️ for privacy protection. 
          <Link href="/license"> MIT License</Link>
        </p>
      </FooterBottom>
    </FooterContainer>
  );
}

export default Footer; 