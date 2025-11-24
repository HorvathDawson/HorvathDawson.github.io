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
      <div className="project-card-media">
        <div className="project-media-frame" style={{ width: '100%', maxHeight: '100%', aspectRatio: '16/9', margin: '0 auto', position: 'relative' }}>
          <SkateboardDisplay />
        </div>
      </div>
    </BaseProjectItem>
  );
};
