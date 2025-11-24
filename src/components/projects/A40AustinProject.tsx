import React from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';
import { VintageCarDisplay } from '../visuals';

const projectConfig: ProjectConfig = {
  id: 'a40austin',
  category: 'In Progress',
  title: '1950 A40 Austin',
  description: 'Currently modernizing a 1950 Austin A40 by upgrading its suspension, brakes, and motor, blending modern performance with a classic design.'
};

export const A40AustinProject: React.FC = () => {
  // Custom animations for car sliding (handled by global scroll handler in App.tsx)
  const customAnimations = (_element: HTMLDivElement) => {
    // Car translation animations are handled in the main App.tsx scroll handler
    // which looks for .project-a40austin .project-card-media
  };

  return (
    <BaseProjectItem 
      config={projectConfig} 
      className="project-a40austin"
      customAnimations={customAnimations}
    >
      <div className="project-card-image project-a40austin">
        <VintageCarDisplay />
      </div>
    </BaseProjectItem>
  );
};
