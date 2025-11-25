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
    const root = document.querySelector('.project-buell');
    if (!root) return;

    const parts = Array.from(root.querySelectorAll('[data-part]')) as HTMLElement[];
    if (!parts.length) return;

    let raf = 0;
    const container = document.querySelector('.parallax-container') as HTMLElement | null || window;

    const onScroll = () => {
      if (raf) return;
      raf = requestAnimationFrame(() => {
        const windowHeight = window.innerHeight;
        const windowCenterY = windowHeight / 2;


  const rect = root.getBoundingClientRect();
  const itemCenterY = rect.top + rect.height / 2;
  const distanceToCenter = Math.abs(itemCenterY - windowCenterY);
  // Invert behavior: parts start away (when far from center) and move toward center as the card approaches
  const factor = Math.min(1, distanceToCenter / windowCenterY);

        const baseDistance = 30;
        const angleInDegrees = 60;
        const angleInRadians = (angleInDegrees * Math.PI) / 180;

        parts.forEach((part) => {
          const partAttr = part.getAttribute('data-part');
          if (!partAttr) return;
          const partNumber = parseInt(partAttr, 10);
          const distance = baseDistance * partNumber * factor;

          const translateX = distance * Math.cos(angleInRadians);
          const translateY = -distance * Math.sin(angleInRadians);

          part.style.transform = `translate(${translateX}px, ${translateY}px)`;
        });

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
      className="project-buell"
      customAnimations={customAnimations}
    >
      <div className="project-card-media">
        <div className="project-media-frame" style={{ width: '100%', maxHeight: '100%', aspectRatio: '4/3', margin: '0 auto', position: 'relative' }}>
          <MotorcycleParts />
        </div>
      </div>
    </BaseProjectItem>
  );
};
