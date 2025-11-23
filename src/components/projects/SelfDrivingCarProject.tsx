import React from 'react';
import { BaseProjectItem, ProjectImage, type ProjectConfig } from './BaseProjectItem';

const projectConfig: ProjectConfig = {
  id: 'self-driving-car',
  category: 'Simulation',
  title: 'Self Driving Car',
  description: 'Simulated a self-driving robot in Gazebo and ROS using computer vision and machine learning to navigate roads, avoid obstacles, and process license plate data from parked cars.'
};

export const SelfDrivingCarProject: React.FC = () => {
  // Custom animation for screen rotation (handled by global scroll handler in App.tsx)
  const customAnimations = (_element: HTMLDivElement) => {
    // This project's custom animations are handled in the main App.tsx scroll handler
    // We could move specific logic here if needed for better encapsulation
  };

  return (
    <BaseProjectItem 
      config={projectConfig} 
      className="project-self-driving-car"
      customAnimations={customAnimations}
    >
      <div className="project-card-image project-self-driving-car">
        <div className="laptop-screen">
          <ProjectImage
            src="/assets/projects/self-driving-car/computer-foreground.svg"
            className="foreground-layer"
            style={{ opacity: 0 }}
          />
          <ProjectImage
            src="/assets/projects/self-driving-car/computer-background.svg"
            className="background-layer"
            style={{ opacity: 1 }}
          />
          <div
            className="computer-screen splash-layer"
            style={{
              opacity: 0
            }}
          />
        </div>
        <div className="laptop-keyboard">
          <ProjectImage
            src="/assets/projects/self-driving-car/computer-keys-foreground.svg"
            className="foreground-layer"
            style={{ opacity: 0 }}
          />
          <ProjectImage
            src="/assets/projects/self-driving-car/computer-keys-background.svg"
            className="background-layer"
            style={{ opacity: 1 }}
          />
        </div>
      </div>
    </BaseProjectItem>
  );
};
