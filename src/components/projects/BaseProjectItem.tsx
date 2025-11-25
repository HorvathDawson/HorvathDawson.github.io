import React, { useRef, useEffect, useState } from 'react';
import { VisualsForceHoverContext } from '../visuals/VisualsContext';

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
  const [isCollapsed, setIsCollapsed] = useState(false);
  const lastMousePos = useRef<{ x: number; y: number } | null>(null);

  useEffect(() => {
    const item = itemRef.current;
    if (!item) return;

    // Helper to check whether the project card is in the stacked/collapsed layout
    const checkCollapsed = () => {
      if (!item) return;
      const style = getComputedStyle(item);
      setIsCollapsed(style.flexDirection === 'column');
    };

    // Initialize collapsed state immediately
    checkCollapsed();

    // Default hover animations
    const handleMouseEnter = () => {
      if (isCollapsed) return;
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
      if (isCollapsed) return;
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

      // Remove box shadow when mouse leaves
      try { item.style.boxShadow = ''; } catch (e) { /* ignore */ }

      // Call custom mouse leave handler if provided
      if (onMouseLeave) onMouseLeave();
    };

    item.addEventListener('mouseenter', handleMouseEnter);
    item.addEventListener('mouseleave', handleMouseLeave);

    // Track last known mouse position so we can detect "virtual" mouseenter
    // events that occur when the page is scrolled and an element moves under
    // a stationary cursor.
    const updateMousePos = (ev: MouseEvent) => {
      lastMousePos.current = { x: ev.clientX, y: ev.clientY };
    };
    window.addEventListener('mousemove', updateMousePos);

    // Scroll handler: when scrolling, check if the last known mouse position
    // is currently over this project card. Use rAF to debounce rapid scroll.
    let scrollRaf = 0 as number | null;
    const scrollCheck = () => {
      if (!lastMousePos.current) return;
      const { x, y } = lastMousePos.current;
      const el = document.elementFromPoint(x, y);
      const isOver = !!el && item.contains(el);
      if (isOver) {
        handleMouseEnter();
      } else {
        handleMouseLeave();
      }
    };

    const onScroll = () => {
      if (scrollRaf) return;
      scrollRaf = requestAnimationFrame(() => {
        scrollCheck();
        scrollRaf = 0;
      }) as unknown as number;
    };

    const parallax = document.querySelector('.parallax-container') as HTMLElement | null;
    if (parallax) parallax.addEventListener('scroll', onScroll, { passive: true });
    else window.addEventListener('scroll', onScroll, { passive: true });

    // Apply custom animations if provided. If the function returns a cleanup, call it on unmount.
    let customCleanup: void | (() => void);
    if (customAnimations) {
      const maybeCleanup = customAnimations(item);
      if (typeof maybeCleanup === 'function') customCleanup = maybeCleanup;
    }

    // Observe layout changes to detect when the project-card has collapsed (stacked)
    const ro = new ResizeObserver(() => {
      // ResizeObserver may fire when sizes change; recompute collapsed state
      checkCollapsed();
    });
    ro.observe(item);

    // Also listen to window resize events as a reliable fallback when layout rules change
    const handleWindowResize = () => checkCollapsed();
    window.addEventListener('resize', handleWindowResize);

    return () => {
  item.removeEventListener('mouseenter', handleMouseEnter);
  item.removeEventListener('mouseleave', handleMouseLeave);
  if (customCleanup) customCleanup();
      ro.disconnect();
      window.removeEventListener('resize', handleWindowResize);
      window.removeEventListener('mousemove', updateMousePos);
      if (parallax) parallax.removeEventListener('scroll', onScroll as EventListener);
      else window.removeEventListener('scroll', onScroll as EventListener);
    };
  }, [onMouseEnter, onMouseLeave, customAnimations, isCollapsed]);

  // When collapsed state changes, immediately apply the forced-hover visuals state
  useEffect(() => {
    const item = itemRef.current;
    if (!item) return;

    const backgrounds = item.querySelectorAll('.background-layer');
    const foregrounds = item.querySelectorAll('.foreground-layer');
    const splashes = item.querySelectorAll('.splash-layer');
    const canvases = item.querySelectorAll('canvas');

    if (isCollapsed) {
      backgrounds.forEach((el: Element) => { (el as HTMLElement).style.opacity = '0'; });
      foregrounds.forEach((el: Element) => { (el as HTMLElement).style.opacity = '1'; });
      splashes.forEach((el: Element) => { (el as HTMLElement).style.opacity = '1'; });
      canvases.forEach((canvas: Element) => { (canvas as HTMLCanvasElement).dataset.hover = 'true'; });
      // When collapsed, also visually indicate hover with shadow
      try { item.style.boxShadow = '0 0 86px 6px #7038cfcc'; } catch (e) { /* ignore */ }
    } else {
      backgrounds.forEach((el: Element) => { (el as HTMLElement).style.opacity = '1'; });
      foregrounds.forEach((el: Element) => { (el as HTMLElement).style.opacity = '0'; });
      splashes.forEach((el: Element) => { (el as HTMLElement).style.opacity = '0'; });
      canvases.forEach((canvas: Element) => { (canvas as HTMLCanvasElement).dataset.hover = 'false'; });
      try { item.style.boxShadow = ''; } catch (e) { /* ignore */ }
    }
  }, [isCollapsed]);

  const rootClass = ['project-card', config.id, className];

  return (
    <VisualsForceHoverContext.Provider value={isCollapsed}>
      <div ref={itemRef} className={rootClass.filter(Boolean).join(' ')}>
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
          {/* For OpenSim2Real we render the CTA inside the content so it stays left-justified */}
          { (config.id === 'opensim2real' || config.id === 'resume') && config.link && config.buttonText && (
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
  {/* Other projects render CTA here (and may be cornered via CSS) */}
  {config.id !== 'opensim2real' && config.id !== 'resume' && config.link && config.buttonText && (
          <a
            href={config.link}
            target="_blank"
            rel="noopener noreferrer"
            className="project-cta-button button"
            {...(config.downloadable ? { download: true } : {})}
          >
            {config.buttonText}
          </a>
        )}
    </div>
    </VisualsForceHoverContext.Provider>
  );
};

// Helper component for creating project images with consistent structure
export const ProjectImage: React.FC<ProjectImageProps> = ({ src, className, style, alt = "" }) => (
  <img
    src={src}
    className={className}
    style={style}
    alt={alt}
    loading="lazy"
  />
);

// Container component for project image sections
export const ProjectImageContainer: React.FC<{ 
  className?: string; 
  imageClassName?: string;
  children: React.ReactNode;
}> = ({ className = "project-card-media", imageClassName = "", children }) => (
  // Render only the media viewport. The outer .project-card-image wrapper was removed
  // to ensure the media element is the direct child used for layout and hover behaviors.
  <div className={[className, imageClassName].filter(Boolean).join(' ')}>
    {children}
  </div>
);
