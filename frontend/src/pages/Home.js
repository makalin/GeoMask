import React from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiShield, FiMapPin, FiUpload, FiDownload, FiEye, FiLock } from 'react-icons/fi';

const HeroSection = styled.section`
  text-align: center;
  padding: 80px 20px;
  color: white;
`;

const HeroTitle = styled(motion.h1)`
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  
  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`;

const HeroSubtitle = styled(motion.p)`
  font-size: 1.3rem;
  margin-bottom: 40px;
  opacity: 0.9;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  
  @media (max-width: 768px) {
    font-size: 1.1rem;
  }
`;

const CTAButton = styled(motion(Link))`
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 16px 32px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  }
`;

const FeaturesSection = styled.section`
  padding: 80px 20px;
  background: white;
`;

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const SectionTitle = styled(motion.h2)`
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 60px;
  color: #333;
  
  @media (max-width: 768px) {
    font-size: 2rem;
  }
`;

const FeaturesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
  margin-bottom: 60px;
`;

const FeatureCard = styled(motion.div)`
  background: white;
  padding: 40px 30px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease;
  
  &:hover {
    transform: translateY(-10px);
  }
`;

const FeatureIcon = styled.div`
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: white;
  font-size: 2rem;
`;

const FeatureTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
`;

const FeatureDescription = styled.p`
  color: #666;
  line-height: 1.6;
  font-size: 1rem;
`;

const HowItWorksSection = styled.section`
  padding: 80px 20px;
  background: #f8f9fa;
`;

const StepsContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
  margin-top: 60px;
`;

const StepCard = styled(motion.div)`
  background: white;
  padding: 30px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  position: relative;
`;

const StepNumber = styled.div`
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 1.2rem;
  margin: 0 auto 20px;
`;

const StepTitle = styled.h3`
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
`;

const StepDescription = styled.p`
  color: #666;
  line-height: 1.6;
`;

function Home() {
  const features = [
    {
      icon: <FiShield />,
      title: "Privacy Protection",
      description: "Automatically detect and replace identifiable background views with AI-generated decoy scenes."
    },
    {
      icon: <FiMapPin />,
      title: "Multiple Scenes",
      description: "Choose from cityscapes, mountain villages, beaches, forests, and custom scenes."
    },
    {
      icon: <FiUpload />,
      title: "Easy Upload",
      description: "Simply upload your photo and let our AI handle the background replacement."
    },
    {
      icon: <FiDownload />,
      title: "High Quality",
      description: "Get high-resolution output ready for social media sharing."
    },
    {
      icon: <FiEye />,
      title: "AI-Powered",
      description: "Advanced AI technology ensures seamless and realistic background replacement."
    },
    {
      icon: <FiLock />,
      title: "Secure",
      description: "Your photos are processed securely and never stored permanently."
    }
  ];

  const steps = [
    {
      number: "1",
      title: "Upload Photo",
      description: "Upload a photo with a window or background you want to mask."
    },
    {
      number: "2",
      title: "Choose Scene",
      description: "Select a decoy scene or let GeoMask randomize it for you."
    },
    {
      number: "3",
      title: "Download",
      description: "Download your protected photo — ready for posting!"
    }
  ];

  return (
    <>
      <HeroSection>
        <HeroTitle
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          Protect Your Privacy from AI
        </HeroTitle>
        <HeroSubtitle
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          GeoMask automatically replaces identifiable background views in your photos 
          with AI-generated decoy scenes to prevent geolocation tracking.
        </HeroSubtitle>
        <CTAButton
          to="/upload"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <FiUpload />
          Start Protecting Your Photos
        </CTAButton>
      </HeroSection>

      <FeaturesSection>
        <Container>
          <SectionTitle
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            Why Choose GeoMask?
          </SectionTitle>
          <FeaturesGrid>
            {features.map((feature, index) => (
              <FeatureCard
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <FeatureIcon>{feature.icon}</FeatureIcon>
                <FeatureTitle>{feature.title}</FeatureTitle>
                <FeatureDescription>{feature.description}</FeatureDescription>
              </FeatureCard>
            ))}
          </FeaturesGrid>
        </Container>
      </FeaturesSection>

      <HowItWorksSection>
        <Container>
          <SectionTitle
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            How It Works
          </SectionTitle>
          <StepsContainer>
            {steps.map((step, index) => (
              <StepCard
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
              >
                <StepNumber>{step.number}</StepNumber>
                <StepTitle>{step.title}</StepTitle>
                <StepDescription>{step.description}</StepDescription>
              </StepCard>
            ))}
          </StepsContainer>
        </Container>
      </HowItWorksSection>
    </>
  );
}

export default Home; 