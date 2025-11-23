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
    <BaseProjectItem config={projectConfig} className="project-robot253">
      <ProjectImageContainer className="project-card-media" imageClassName="project-robot253">
        <ProjectImage
          src="/assets/projects/253robot/foreground.png"
          className="foreground-layer"
          style={{ opacity: 0 }}
        />
        <ProjectImage
          src="/assets/projects/253robot/background2.png"
          className="background-layer"
          style={{ opacity: 1 }}
        />
        <ProjectImage
          src="/assets/projects/253robot/splash.png"
          className="splash-layer"
          style={{ opacity: 0 }}
        />
      </ProjectImageContainer>
    </BaseProjectItem>
  );
};
