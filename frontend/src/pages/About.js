import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiShield, FiEye, FiMapPin, FiLock, FiCode, FiHeart } from 'react-icons/fi';

const AboutContainer = styled.div`
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
`;

const AboutHeader = styled.div`
  text-align: center;
  margin-bottom: 60px;
`;

const AboutTitle = styled(motion.h1)`
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  
  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`;

const AboutSubtitle = styled(motion.p)`
  font-size: 1.2rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
`;

const Section = styled(motion.section)`
  margin-bottom: 60px;
`;

const SectionTitle = styled.h2`
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
`;

const ContentGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
  margin-bottom: 40px;
`;

const ContentCard = styled.div`
  background: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
`;

const CardIcon = styled.div`
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: white;
  font-size: 1.5rem;
`;

const CardTitle = styled.h3`
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
`;

const CardText = styled.p`
  color: #666;
  line-height: 1.6;
`;

const TechStack = styled.div`
  background: #f8f9fa;
  padding: 40px;
  border-radius: 16px;
  margin-bottom: 40px;
`;

const TechGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 30px;
`;

const TechItem = styled.div`
  background: white;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
`;

const TechName = styled.div`
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
`;

const TechDescription = styled.div`
  font-size: 0.9rem;
  color: #666;
`;

const PrivacySection = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px;
  border-radius: 16px;
  text-align: center;
  margin-bottom: 40px;
`;

const PrivacyTitle = styled.h2`
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 20px;
`;

const PrivacyText = styled.p`
  font-size: 1.1rem;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
`;

const TeamSection = styled.div`
  text-align: center;
  margin-bottom: 40px;
`;

const TeamMember = styled.div`
  background: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  display: inline-block;
  margin: 0 20px;
  
  @media (max-width: 768px) {
    margin: 20px 0;
  }
`;

const TeamAvatar = styled.div`
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

const TeamName = styled.h3`
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 10px;
  color: #333;
`;

const TeamRole = styled.p`
  color: #666;
  margin-bottom: 15px;
`;

const TeamBio = styled.p`
  color: #666;
  line-height: 1.6;
  font-size: 0.9rem;
`;

function About() {
  const features = [
    {
      icon: <FiShield />,
      title: "Privacy Protection",
      text: "Automatically detect and replace identifiable background views with AI-generated decoy scenes to prevent geolocation tracking."
    },
    {
      icon: <FiEye />,
      title: "AI-Powered",
      text: "Advanced AI technology ensures seamless and realistic background replacement that looks natural and professional."
    },
    {
      icon: <FiMapPin />,
      title: "Multiple Scenes",
      text: "Choose from various scene types including cityscapes, mountain villages, beaches, forests, and custom descriptions."
    },
    {
      icon: <FiLock />,
      title: "Secure Processing",
      text: "Your photos are processed securely and never stored permanently. We prioritize your privacy and data protection."
    }
  ];

  const techStack = [
    { name: "Python", description: "Backend API with FastAPI" },
    { name: "React", description: "Modern frontend interface" },
    { name: "OpenAI", description: "AI image generation" },
    { name: "OpenCV", description: "Image processing" },
    { name: "Docker", description: "Containerized deployment" },
    { name: "Styled Components", description: "Modern CSS-in-JS" }
  ];

  return (
    <AboutContainer>
      <AboutHeader>
        <AboutTitle
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          About GeoMask
        </AboutTitle>
        <AboutSubtitle
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          Protecting your privacy in the age of AI-powered geolocation tools
        </AboutSubtitle>
      </AboutHeader>

      <Section
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
      >
        <SectionTitle>Why GeoMask?</SectionTitle>
        <ContentGrid>
          {features.map((feature, index) => (
            <ContentCard key={index}>
              <CardIcon>{feature.icon}</CardIcon>
              <CardTitle>{feature.title}</CardTitle>
              <CardText>{feature.text}</CardText>
            </ContentCard>
          ))}
        </ContentGrid>
      </Section>

      <Section
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
      >
        <SectionTitle>Technology Stack</SectionTitle>
        <TechStack>
          <TechGrid>
            {techStack.map((tech, index) => (
              <TechItem key={index}>
                <TechName>{tech.name}</TechName>
                <TechDescription>{tech.description}</TechDescription>
              </TechItem>
            ))}
          </TechGrid>
        </TechStack>
      </Section>

      <Section
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
      >
        <PrivacySection>
          <PrivacyTitle>Privacy First</PrivacyTitle>
          <PrivacyText>
            At GeoMask, we believe privacy is a fundamental human right. Our technology 
            is designed to protect your location privacy without compromising on quality 
            or user experience. Your photos are processed securely and never stored permanently.
          </PrivacyText>
        </PrivacySection>
      </Section>

      <Section
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
      >
        <SectionTitle>Meet the Team</SectionTitle>
        <TeamSection>
          <TeamMember>
            <TeamAvatar>
              <FiCode />
            </TeamAvatar>
            <TeamName>makalin</TeamName>
            <TeamRole>Founder & Developer</TeamRole>
            <TeamBio>
              Passionate about privacy protection and AI technology. 
              Building tools to help people maintain their digital privacy 
              in an increasingly connected world.
            </TeamBio>
          </TeamMember>
        </TeamSection>
      </Section>

      <Section
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
      >
        <ContentCard>
          <CardIcon>
            <FiHeart />
          </CardIcon>
          <CardTitle>Open Source</CardTitle>
          <CardText>
            GeoMask is open source and available on GitHub. We believe in transparency 
            and community collaboration. Feel free to contribute, report issues, or 
            suggest new features!
          </CardText>
        </ContentCard>
      </Section>
    </AboutContainer>
  );
}

export default About; 