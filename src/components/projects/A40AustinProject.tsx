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
    // Move the A40 car translation animation here so it's scoped to this project
    const root = document.querySelector('.project-a40austin');
    if (!root) return;

    const car = root.querySelector('[data-vintage-car]') as HTMLElement | null;
    if (!car) return;

    let raf = 0;
    const container = document.querySelector('.parallax-container') as HTMLElement | null || window;

    const onScroll = () => {
      if (raf) return;
      raf = requestAnimationFrame(() => {
        const rect = car.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        const windowCenterY = windowHeight / 2;
        const itemCenterY = rect.top + rect.height / 2;
        const distanceToCenter = Math.max(0, itemCenterY - windowCenterY);
        const factor = Math.max(0, distanceToCenter / windowCenterY);

        const baseDistance = -150;
        const angleInDegrees = 30;
        const angleInRadians = (angleInDegrees * Math.PI) / 180;

        const translateX = baseDistance * factor * Math.cos(angleInRadians);
        const translateY = baseDistance * factor * Math.sin(angleInRadians);

        car.style.transform = `translate(${translateX}px, ${translateY}px)`;

        raf = 0;
      });
    };

    // Attach to parallax container if present otherwise window
    container.addEventListener ? container.addEventListener('scroll', onScroll) : window.addEventListener('scroll', onScroll);

    // Run once to initialize
    onScroll();

    // return cleanup fn
    return () => {
      container.removeEventListener ? container.removeEventListener('scroll', onScroll) : window.removeEventListener('scroll', onScroll);
      if (raf) cancelAnimationFrame(raf);
    };
  };

  return (
    <BaseProjectItem 
      config={projectConfig} 
      className="project-a40austin"
      customAnimations={customAnimations}
    >
      <div className="project-card-media">
        <div className="project-media-frame" style={{ width: '100%', maxHeight: '100%', aspectRatio: '16/9', margin: '0 auto', position: 'relative' }}>
          <VintageCarDisplay />
        </div>
      </div>
    </BaseProjectItem>
  );
};
