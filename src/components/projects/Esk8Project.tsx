import React from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';

const projectConfig: ProjectConfig = {
  id: 'esk8',
  category: 'Project', 
  title: 'DIY E-Sk8',
  description: 'Designed and built a DIY electric skateboard with dual 6374 motors, a custom 10s4p Li-ion battery, and Vedder ESCs, optimized for daily commuting with waterproofing and tailored gearing.'
};

export const Esk8Project: React.FC = () => {
  return (
    <BaseProjectItem config={projectConfig} className="esk8">
      <div className="project-portfolio__item-image esk8">
        <div className="project-portfolio__item-image-container">
          <img
            src="/assets/projects/esk8/foreground.png"
            alt=""
            className="foreground"
            loading="lazy"
            style={{ opacity: 0 }}
          />
          <img
            src="/assets/projects/esk8/background.svg"
            alt=""
            className="background"
            loading="lazy"
            style={{ opacity: 1 }}
          />
        </div>
      </div>
    </BaseProjectItem>
  );
};
