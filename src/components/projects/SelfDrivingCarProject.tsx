import React, { useCallback } from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';
import { LaptopWithScreen } from '../visuals';

const projectConfig: ProjectConfig = {
  id: 'self-driving-car',
  category: 'Simulation',
  title: 'Self Driving Car',
  description: 'Simulated a self-driving robot in Gazebo and ROS.'
};

export const SelfDrivingCarProject: React.FC = () => {

  const customAnimations = useCallback((rootElement: HTMLElement) => {
    // 1. SELECT ELEMENTS
    // Target the specific screen inside this component
    const screen = rootElement.querySelector('[data-laptop-screen]') as HTMLElement | null;
    
    // Target the STATIC frame to measure position. 
    // IMPORTANT: We measure this because it doesn't move/rotate.
    const frame = rootElement.querySelector('.project-media-frame') as HTMLElement | null;

    if (!screen || !frame) return;

    let raf = 0;

    const onScroll = () => {
      if (raf) return;
      
      raf = requestAnimationFrame(() => {
        // 2. MEASURE STATIC FRAME
        const rect = frame.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        const windowCenterY = windowHeight / 2;
        
        // Center of the laptop frame
        const itemCenterY = rect.top + rect.height / 2;
        
        // 3. CALCULATE FACTOR
        // Distance from center of screen
        // Positive = Below center (scrolling in)
        // Negative = Above center (scrolled past)
        const distanceToCenter = itemCenterY - windowCenterY;

        // Normalize to a 0..1 factor based on half screen height
        let factor = distanceToCenter / windowCenterY;
        
        // Clamp: We only animate when it's below center (opening up)
        // Stops animating once it hits the center or goes above
        factor = Math.max(0, factor);

        // 4. ANIMATION MATH
        // At bottom of screen (factor 1) -> Rotate 90deg (Closed/Flat)
        // At center of screen (factor 0) -> Rotate 0deg (Open/Upright)
        const maxRotation = 90; 
        const rotation = maxRotation * factor;
        
        // Using rotateX to simulate lid opening
        screen.style.transform = `rotateX(-${rotation}deg)`; 
        
        raf = 0;
      });
    };

    // 5. ATTACH TO WINDOW
    window.addEventListener('scroll', onScroll, { passive: true });
    
    // Initial calculation
    onScroll();

    return () => {
      window.removeEventListener('scroll', onScroll);
      if (raf) cancelAnimationFrame(raf);
    };
  }, []);

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
            overflow: 'visible', // Must be visible for 3D elements to poke out
            zIndex: 10,
            // CRITICAL: Perspective is required for rotateX to look like 3D tilting
            // otherwise it just looks like the element is getting squashed.
            perspective: '1000px' 
          }}
        >
          {/* The LaptopWithScreen component should contain the [data-laptop-screen] 
             attribute on the specific div that represents the screen/lid 
          */}
          <LaptopWithScreen />
        </div>
      </div>
    </BaseProjectItem>
  );
};