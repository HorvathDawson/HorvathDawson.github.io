import React from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';
import { MotorcycleParts } from '../visuals';

const projectConfig: ProjectConfig = {
  id: 'buell',
  category: 'Fix',
  title: 'Buell Motor Rebuild',
  description: 'Rebuilt a 2008 Buell XB9SX motor by disassembling, inspecting, and replacing worn components, requiring precision and expertise to restore performance and reliability.'
};

export const BuellProject: React.FC = () => {
  // Custom animations for motor parts explosion (handled by global scroll handler in App.tsx)
  const customAnimations = (_element: HTMLDivElement) => {
    // Part explosion animations are handled in the main App.tsx scroll handler
    // which looks for elements with class*="part__" within this project
  };

  return (
    <BaseProjectItem 
      config={projectConfig} 
      className="project-buell"
      customAnimations={customAnimations}
    >
      <div className="project-card-image project-buell">
        <MotorcycleParts />
      </div>
    </BaseProjectItem>
  );
};
