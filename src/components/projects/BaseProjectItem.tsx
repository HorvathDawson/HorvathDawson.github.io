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
  customAnimations?: (element: HTMLDivElement) => void;
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

      // Call custom mouse leave handler if provided
      if (onMouseLeave) onMouseLeave();
    };

    item.addEventListener('mouseenter', handleMouseEnter);
    item.addEventListener('mouseleave', handleMouseLeave);

    // Apply custom animations if provided
    if (customAnimations) {
      customAnimations(item);
    }

    return () => {
      item.removeEventListener('mouseenter', handleMouseEnter);
      item.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, [onMouseEnter, onMouseLeave, customAnimations]);

  const rootClass = ['project-card', config.id, className];
  // Keep the CTA in-flow for OpenSim2Real and Resume; other cards get cornered CTAs
  if (config.id !== 'opensim2real' && config.id !== 'resume') rootClass.push('cta-corner');

  return (
    <div ref={itemRef} className={rootClass.filter(Boolean).join(' ')}>
      <div className="project-card-overlay"></div>
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
