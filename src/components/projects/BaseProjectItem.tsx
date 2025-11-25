import React, { useRef, useEffect } from 'react';

export interface ProjectConfig {
  id: string;
  category: string;
  title: string;
  description: string;
  link?: string;
  buttonText?: string;
  downloadable?: boolean;
}

export interface ProjectImageProps {
  src: string;
  className: string;
  style?: React.CSSProperties;
  alt?: string;
}

interface BaseProjectItemProps {
  config: ProjectConfig;
  className?: string;
  onMouseEnter?: () => void;
  onMouseLeave?: () => void;
  customAnimations?: (element: HTMLDivElement) => void | (() => void);
  children: React.ReactNode;
}

export const BaseProjectItem: React.FC<BaseProjectItemProps> = ({
  config,
  className = '',
  onMouseEnter,
  onMouseLeave,
  customAnimations,
  children
}) => {
  const itemRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const item = itemRef.current;
    if (!item) return;

    // Helper to determine if we are in tablet/mobile mode
    const isTablet = () => window.matchMedia('(max-width: 1024px)').matches;

    // Default hover animations
    const handleMouseEnter = () => {
      const backgrounds = item.querySelectorAll('.background-layer');
      const foregrounds = item.querySelectorAll('.foreground-layer');
      const splashes = item.querySelectorAll('.splash-layer');
      const canvases = item.querySelectorAll('canvas');

      backgrounds.forEach((el: Element) => {
        (el as HTMLElement).style.opacity = '0';
      });
      foregrounds.forEach((el: Element) => {
        (el as HTMLElement).style.opacity = '1';
      });
      splashes.forEach((el: Element) => {
        (el as HTMLElement).style.opacity = '1';
      });
      canvases.forEach((canvas: Element) => {
        (canvas as HTMLCanvasElement).dataset.hover = 'true';
      });

      // Add box shadow to project card when hovered
      try { item.style.boxShadow = '0 0 86px 6px #7038cfcc'; } catch (e) { /* ignore */ }

      // Call custom mouse enter handler if provided
      if (onMouseEnter) onMouseEnter();
    };

    const handleMouseLeave = () => {
      const backgrounds = item.querySelectorAll('.background-layer');
      const foregrounds = item.querySelectorAll('.foreground-layer');
      const splashes = item.querySelectorAll('.splash-layer');
      const canvases = item.querySelectorAll('canvas');

      backgrounds.forEach((el: Element) => {
        (el as HTMLElement).style.opacity = '1';
      });
      foregrounds.forEach((el: Element) => {
        (el as HTMLElement).style.opacity = '0';
      });
      splashes.forEach((el: Element) => {
        (el as HTMLElement).style.opacity = '0';
      });
      canvases.forEach((canvas: Element) => {
        (canvas as HTMLCanvasElement).dataset.hover = 'false';
      });

      // Remove box shadow when mouse leaves ONLY if NOT in tablet mode
      if (!isTablet()) {
        try { item.style.boxShadow = ''; } catch (e) { /* ignore */ }
      }

      // Call custom mouse leave handler if provided
      if (onMouseLeave) onMouseLeave();
    };

    // Ensure shadow is applied correctly on window resize/load based on mode
    const handleResize = () => {
      if (isTablet()) {
        try { item.style.boxShadow = '0 0 86px 6px #7038cfcc'; } catch (e) { /* ignore */ }
      } else {
        // If returning to desktop, clear the forced shadow 
        // (hover events will re-apply it if mouse is actually over)
        try { item.style.boxShadow = ''; } catch (e) { /* ignore */ }
      }
    };

    item.addEventListener('mouseenter', handleMouseEnter);
    item.addEventListener('mouseleave', handleMouseLeave);
    window.addEventListener('resize', handleResize);
    
    // Initial check on mount
    handleResize();

    // Apply custom animations if provided. If the function returns a cleanup, call it on unmount.
    let customCleanup: void | (() => void);
    if (customAnimations) {
      const maybeCleanup = customAnimations(item);
      if (typeof maybeCleanup === 'function') customCleanup = maybeCleanup;
    }

    return () => {
      item.removeEventListener('mouseenter', handleMouseEnter);
      item.removeEventListener('mouseleave', handleMouseLeave);
      window.removeEventListener('resize', handleResize);
      if (customCleanup) customCleanup();
    };
  }, [onMouseEnter, onMouseLeave, customAnimations]);

  const rootClass = ['project-card', config.id, className];

  return (
    <div ref={itemRef} className={rootClass.filter(Boolean).join(' ')}>
      <div className="project-card-overlay" />
      <div className="project-card-content content-width-constrained">
        <h6 className="project-category">{config.category}</h6>
        <h1 className="section-title">
          {config.link ? (
            <a href={config.link} target="_blank" rel="noopener noreferrer">
              <span className="text-highlighted">{config.title}</span>
            </a>
          ) : (
            <span className="text-highlighted">{config.title}</span>
          )}
        </h1>
        <p className="about-description">{config.description}</p>
        
        {/* Simplified Button Logic */}
        {config.link && config.buttonText && (
          <a
            href={config.link}
            target="_blank"
            rel="noopener noreferrer"
            className="project-cta-button button"
            {...(config.downloadable ? { download: true } : {})}
            style={{ display: 'inline-block', marginTop: '18px' }}
          >
            {config.buttonText}
          </a>
        )}
      </div>
      {children}
    </div>
  );
};