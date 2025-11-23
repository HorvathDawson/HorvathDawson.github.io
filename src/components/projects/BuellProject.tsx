import React from 'react';
import { BaseProjectItem, ProjectImageContainer, ProjectImage, type ProjectConfig } from './BaseProjectItem';

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
      <ProjectImageContainer className="project-card-media" imageClassName="project-buell">
        <ProjectImage
          src="/assets/projects/buell/motor_images/section-view.gif"
          className="foreground-layer"
          style={{ opacity: 0 }}
        />
        <ProjectImage
          src="/assets/projects/buell/motor_images/case.png"
          className="background-layer"
          style={{ opacity: 1 }}
        />
        <ProjectImage
          src="/assets/projects/buell/motor_images/left-cylinder.png"
          className="background-layer"
          style={{ opacity: 1 }}
        />
        <ProjectImage
          src="/assets/projects/buell/motor_images/cylinder-barrel.png"
          className="background-layer part__1"
          style={{ opacity: 1 }}
        />
        <ProjectImage
          src="/assets/projects/buell/motor_images/rocker-box.png"
          className="background-layer part__2"
          style={{ opacity: 1 }}
        />
        <ProjectImage
          src="/assets/projects/buell/motor_images/rocker-box-top.png"
          className="background-layer part__3"
          style={{ opacity: 1 }}
        />
        <ProjectImage
          src="/assets/projects/buell/motor_images/push-rods.png"
          className="background-layer part__4"
          style={{ opacity: 1 }}
        />
      </ProjectImageContainer>
    </BaseProjectItem>
  );
};
