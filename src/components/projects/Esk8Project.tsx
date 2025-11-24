import React from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';
import { SkateboardDisplay } from '../visuals';

const projectConfig: ProjectConfig = {
  id: 'esk8',
  category: 'Project', 
  title: 'DIY E-Sk8',
  description: 'Designed and built a DIY electric skateboard with dual 6374 motors, a custom 10s4p Li-ion battery, and Vedder ESCs, optimized for daily commuting with waterproofing and tailored gearing.'
};

export const Esk8Project: React.FC = () => {
  return (
    <BaseProjectItem config={projectConfig} className="project-esk8">
      <div className="project-card-image project-esk8">
        <SkateboardDisplay />
      </div>
    </BaseProjectItem>
  );
};
