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
      const backgrounds = item.querySelectorAll('.background');
      const foregrounds = item.querySelectorAll('.foreground');
      const splashes = item.querySelectorAll('.splash');
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
      const backgrounds = item.querySelectorAll('.background');
      const foregrounds = item.querySelectorAll('.foreground');
      const splashes = item.querySelectorAll('.splash');
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

  return (
    <div ref={itemRef} className={`project-portfolio__item ${config.id} ${className}`}>
      <div className="project-portfolio__item-overlay"></div>
      <div className="project-portfolio__item-text item-text-width">
        <h6 className="category-heading">{config.category}</h6>
        <h1 className="heading-3">
          {config.link ? (
            <a href={config.link} target="_blank" rel="noopener noreferrer">
              <span className="text-highlight">{config.title}</span>
            </a>
          ) : (
            <span className="text-highlight">{config.title}</span>
          )}
        </h1>
        <p className="paragraph-2">{config.description}</p>
      </div>
      {children}
      {config.link && config.buttonText && (
        <a
          href={config.link}
          target="_blank"
          rel="noopener noreferrer"
          className="button-portfolio--tile-2 w-button"
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
  children: React.ReactNode;
}> = ({ className = "project-portfolio__item-image-container", children }) => (
  <div className="project-portfolio__item-image">
    <div className={className}>
      {children}
    </div>
  </div>
);
