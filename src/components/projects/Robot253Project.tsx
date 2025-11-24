import React from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';
import { RobotDisplay } from '../visuals';

const projectConfig: ProjectConfig = {
  id: 'robot253',
  category: 'Competition',
  title: 'Autonomous Robot',
  description: 'Designed an autonomous robot for the Engineering Physics Robot Competition, featuring a custom drivetrain, SPI communication, control loop and mechanical systems.'
};

export const Robot253Project: React.FC = () => {
  return (
    <BaseProjectItem config={projectConfig} className="project-robot253">
      <div className="project-card-image project-robot253">
        <RobotDisplay />
      </div>
    </BaseProjectItem>
  );
};
