import React from 'react';
import { BaseProjectItem, ProjectImageContainer, ProjectImage, type ProjectConfig } from './BaseProjectItem';

const projectConfig: ProjectConfig = {
  id: 'robot253',
  category: 'Competition',
  title: 'Autonomous Robot',
  description: 'Designed an autonomous robot for the Engineering Physics Robot Competition, featuring a custom drivetrain, SPI communication, control loop and mechanical systems.'
};

export const Robot253Project: React.FC = () => {
  return (
    <BaseProjectItem config={projectConfig} className="robot253">
      <ProjectImageContainer className="project-portfolio__item-image-container">
        <ProjectImage
          src="/assets/projects/253robot/foreground.png"
          className="foreground"
          style={{ opacity: 0 }}
        />
        <ProjectImage
          src="/assets/projects/253robot/background2.png"
          className="background"
          style={{ opacity: 1 }}
        />
        <ProjectImage
          src="/assets/projects/253robot/splash.png"
          className="splash"
          style={{ opacity: 0 }}
        />
      </ProjectImageContainer>
    </BaseProjectItem>
  );
};
