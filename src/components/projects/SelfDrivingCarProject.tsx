import React from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';
import { LaptopWithScreen } from '../visuals';

const projectConfig: ProjectConfig = {
  id: 'self-driving-car',
  category: 'Simulation',
  title: 'Self Driving Car',
  description: 'Simulated a self-driving robot in Gazebo and ROS.'
};

export const SelfDrivingCarProject: React.FC = () => {
  const customAnimations = (_element: HTMLDivElement) => {
    const root = document.querySelector('.project-self-driving-car');
    if (!root) return;
    const screen = root.querySelector('[data-laptop-screen]') as HTMLElement | null;
    if (!screen) return;

    let raf = 0;
    const container = document.querySelector('.parallax-container') as HTMLElement | null || window;

    const onScroll = () => {
      if (raf) return;
      raf = requestAnimationFrame(() => {
        const rect = screen.getBoundingClientRect();
        const itemCenterY = rect.top + rect.height / 2;
        const windowHeight = window.innerHeight;
        const windowCenterY = windowHeight / 2;
        const distanceToCenter = Math.min(0, 1.5 * windowCenterY - itemCenterY);
        
        // POSITIVE Rotation (Leaning Back)
        let rotation = Math.abs(Math.min(70, -85 * (distanceToCenter / (windowHeight / 2))));
        
        screen.style.transform = `rotateX(${rotation}deg)`;
        raf = 0;
      });
    };

    (container as any).addEventListener ? (container as any).addEventListener('scroll', onScroll) : window.addEventListener('scroll', onScroll);
    onScroll();

    return () => {
      (container as any).removeEventListener ? (container as any).removeEventListener('scroll', onScroll) : window.removeEventListener('scroll', onScroll);
      if (raf) cancelAnimationFrame(raf);
    };
  };

  return (
    <BaseProjectItem
      config={projectConfig}
      className="project-self-driving-car"
      customAnimations={customAnimations}
    >
      <div className="project-card-media">
        <div 
          className="project-media-frame" 
          style={{ 
            width: '100%', 
            height: '100%', 
            margin: '0 auto', 
            position: 'relative',
            overflow: 'visible',
            zIndex: 10
          }}
        >
          <LaptopWithScreen />
        </div>
      </div>
    </BaseProjectItem>
  );
};