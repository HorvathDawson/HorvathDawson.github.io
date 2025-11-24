import React, { useRef, useEffect } from 'react';

export interface FumeExtractorArmProps {
  className?: string;
}

export const FumeExtractorArm: React.FC<FumeExtractorArmProps> = ({ 
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
      const fumeAnimation = container.querySelector('.fume-animation') as HTMLElement;
      
      if (foreground) foreground.style.opacity = '1';
      if (background) background.style.opacity = '0';
      if (splash) splash.style.opacity = '1';
      if (fumeAnimation) fumeAnimation.style.opacity = '1';
    };

    const handleMouseLeave = () => {
      const foreground = container.querySelector('.foreground-layer') as HTMLElement;
      const background = container.querySelector('.background-layer') as HTMLElement;
      const splash = container.querySelector('.splash-layer') as HTMLElement;
      const fumeAnimation = container.querySelector('.fume-animation') as HTMLElement;
      
      if (foreground) foreground.style.opacity = '0';
      if (background) background.style.opacity = '1';
      if (splash) splash.style.opacity = '0';
      if (fumeAnimation) fumeAnimation.style.opacity = '0';
    };

    container.addEventListener('mouseenter', handleMouseEnter);
    container.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      container.removeEventListener('mouseenter', handleMouseEnter);
      container.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, []);

  return (
    <div 
      ref={containerRef}
      className={`fume-extractor-arm ${className}`.trim()}
      style={{ position: 'relative', width: '100%', height: '100%' }}
    >
      {/* Arm foreground - shows on hover */}
      <img
        src="/assets/projects/fume-extractor/arm.png"
        alt="Fume extractor arm"
        className="foreground-layer"
        loading="lazy"
        style={{ 
          opacity: 0,
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          zIndex: 5
        }}
      />
      {/* Arm edge - shows by default */}
      <img
        src="/assets/projects/fume-extractor/arm-edge.png"
        alt="Fume extractor arm edge"
        className="background-layer"
        loading="lazy"
        style={{ 
          opacity: 1,
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          zIndex: 4
        }}
      />
      {/* Splash overlay - shows on hover */}
      <img
        src="/assets/projects/fume-extractor/splash.png"
        alt="Fume extractor splash"
        className="splash-layer"
        loading="lazy"
        style={{ 
          opacity: 0,
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          zIndex: 4
        }}
      />
      {/* Fume animation - shows on hover */}
      <img
        src="/assets/projects/fume-extractor/fumes.gif"
        alt="Fume animation"
        className="splash-layer fume-animation"
        loading="lazy"
        style={{ 
          opacity: 0,
          position: 'absolute',
          transform: 'rotate(80deg)',
          height: '20%',
          top: '58%',
          left: '75%',
          width: 'auto',
          objectFit: 'contain',
          zIndex: 6
        }}
      />
    </div>
  );
};
