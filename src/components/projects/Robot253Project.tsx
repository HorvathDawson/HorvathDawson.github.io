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
      <div className="project-card-media">
        <div className="project-media-frame" style={{ width: '100%', maxHeight: '100%', aspectRatio: '16/10', margin: '0 auto', position: 'relative' }}>
          <RobotDisplay />
        </div>
      </div>
    </BaseProjectItem>
  );
};
