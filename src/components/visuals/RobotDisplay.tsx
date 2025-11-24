import React, { useRef, useEffect } from 'react';

export interface RobotDisplayProps {
  className?: string;
}

export const RobotDisplay: React.FC<RobotDisplayProps> = ({ 
  className = ''
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleMouseEnter = () => {
      const foreground = container.querySelector('.foreground-layer') as HTMLElement;
      const background = container.querySelector('.background-layer') as HTMLElement;
      const splash = container.querySelector('.splash-layer') as HTMLElement;
      
      if (foreground) foreground.style.opacity = '1';
      if (background) background.style.opacity = '0';
      if (splash) splash.style.opacity = '1';
    };

    const handleMouseLeave = () => {
      const foreground = container.querySelector('.foreground-layer') as HTMLElement;
      const background = container.querySelector('.background-layer') as HTMLElement;
      const splash = container.querySelector('.splash-layer') as HTMLElement;
      
      if (foreground) foreground.style.opacity = '0';
      if (background) background.style.opacity = '1';
      if (splash) splash.style.opacity = '0';
    };

    container.addEventListener('mouseenter', handleMouseEnter);
    container.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      container.removeEventListener('mouseenter', handleMouseEnter);
      container.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, []);

  // size and position props are intentionally ignored — visuals fill the media viewport

  const containerStyles = {
    position: 'absolute' as const,
    inset: 0 as const,
    width: '100%',
    height: '100%'
  };

  // intrinsic frame size: visual authors should treat 800x600 as the design canvas
  const intrinsicFrameStyles = {
    width: 800,
    height: 600,
    maxWidth: '100%',
    maxHeight: '100%',
    position: 'relative' as const
  };

  const imageStyles = {
    position: 'absolute' as const,
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    objectFit: 'contain' as const,
    transition: 'opacity 0.3s ease',
  };

  return (
    <div 
      ref={containerRef}
      className={`robot-display ${className}`.trim()}
      style={containerStyles}
    >
      <div style={intrinsicFrameStyles}>
        <div style={{ position: 'relative', width: '100%', height: '100%' }}>
        {/* Robot foreground - shows on hover */}
        <img
          src="/assets/projects/253robot/foreground.png"
          alt="Robot 253 foreground"
          className="foreground-layer"
          loading="lazy"
          style={{ ...imageStyles, opacity: 0 }}
        />
        {/* Robot background - shows by default */}
        <img
          src="/assets/projects/253robot/background2.png"
          alt="Robot 253 background"
          className="background-layer"
          loading="lazy"
          style={{ ...imageStyles, opacity: 1 }}
        />
        {/* Robot splash overlay - shows on hover */}
        <img
          src="/assets/projects/253robot/splash.png"
          alt="Robot 253 splash"
          className="splash-layer"
          loading="lazy"
          style={{ ...imageStyles, opacity: 0 }}
        />
      </div>
    </div>
    </div>
  );
};
