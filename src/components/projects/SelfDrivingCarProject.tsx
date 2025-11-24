import React from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';
import { LaptopWithScreen } from '../visuals';

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
        <div className="project-card-media">
          <div className="project-media-frame" style={{ width: '100%', maxHeight: '100%', aspectRatio: '16/10', margin: '0 auto', position: 'relative' }}>
            <LaptopWithScreen />
          </div>
        </div>
      </BaseProjectItem>
  );
};
