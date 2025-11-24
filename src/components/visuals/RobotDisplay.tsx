import React, { useRef, useEffect } from 'react';

export interface RobotDisplayProps {
  className?: string;
  size?: 'small' | 'medium' | 'large';
  position?: 'left' | 'center' | 'right';
}

export const RobotDisplay: React.FC<RobotDisplayProps> = ({ 
  className = '', 
  size = 'medium',
  position = 'right'
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

  const getSizeStyles = () => {
    switch (size) {
      case 'small':
        return { width: '50%', height: '40%' };
      case 'large':
        return { width: '90%', height: '90%' };
      default:
        return { width: '70%', height: '70%' };
    }
  };

  const getPositionStyles = () => {
    switch (position) {
      case 'left':
        return { left: '5%', right: 'auto', top: '5%', bottom: 'auto' };
      case 'center':
        return { left: '50%', transform: 'translateX(-50%)', right: 'auto', top: '5%', bottom: 'auto' };
      default:
        return { right: 'auto', left: 'auto', top: '5%', bottom: 'auto', insetInlineStart: '5%', insetInlineEnd: '0%' };
    }
  };

  const containerStyles = {
    position: 'absolute' as const,
    ...getSizeStyles(),
    ...getPositionStyles(),
  };

  const mediaStyles = {
    position: 'relative' as const,
    width: '100%',
    height: '100%',
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
      <div style={mediaStyles}>
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
  );
};
