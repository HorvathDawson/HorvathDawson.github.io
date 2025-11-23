import React from 'react';
import { BaseProjectItem, ProjectImageContainer, ProjectImage, type ProjectConfig } from './BaseProjectItem';

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
      <ProjectImageContainer className="project-card-media" imageClassName="project-a40austin">
        <ProjectImage
          src="/assets/projects/a40austin/foreground.png"
          className="foreground-layer"
          style={{ opacity: 0 }}
        />
        <ProjectImage
          src="/assets/projects/a40austin/background.png"
          className="background-layer"
          style={{ opacity: 1 }}
        />
      </ProjectImageContainer>
    </BaseProjectItem>
  );
};
