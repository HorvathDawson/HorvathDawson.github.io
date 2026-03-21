import React, { useCallback } from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';
import { DesktopDisplay } from '../visuals/DesktopDisplay';

const projectConfig: ProjectConfig = {
  id: 'bc-fishing-regulations',
  category: 'Web App',
  title: 'Can I Fish This?',
  description: 'A web app that simplifies BC fishing regulations, helping anglers quickly find what they can fish, where, and when.',
  link: 'https://canifishthis.ca',
  buttonText: 'Visit Site'
};

export const BCFishingProject: React.FC = () => {
  const customAnimations = useCallback((rootElement: HTMLElement) => {
    const display = rootElement.querySelector('[data-desktop-display]') as HTMLElement | null;
    const frame = rootElement.querySelector('.project-media-frame') as HTMLElement | null;

    if (!display || !frame) return;

    let raf = 0;

    const onScroll = () => {
      if (raf) return;

      raf = requestAnimationFrame(() => {
        const rect = frame.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        const windowCenterY = windowHeight / 2;
        const itemCenterY = rect.top + rect.height / 2;
        const distanceToCenter = itemCenterY - windowCenterY;

        let factor = distanceToCenter / windowCenterY;
        factor = Math.max(0, factor);

        const translateY = 60 * factor;
        display.style.transform = `translate3d(0, ${translateY}px, 0)`;

        raf = 0;
      });
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    return () => {
      window.removeEventListener('scroll', onScroll);
      if (raf) cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <BaseProjectItem
      config={projectConfig}
      className="project-bc-fishing"
      customAnimations={customAnimations}
    >
      <DesktopDisplay />
    </BaseProjectItem>
  );
};
