import React, { useRef, useEffect } from 'react';

export interface SpinningLegProps {
  className?: string;
}

export const SpinningLeg: React.FC<SpinningLegProps> = ({ 
  className = ''
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleMouseEnter = () => {
      const foreground = container.querySelector('.foreground-layer') as HTMLElement;
      const background = container.querySelector('.background-layer') as HTMLElement;
      
      if (foreground && background) {
        foreground.style.opacity = '1';
        background.style.opacity = '0';
      }
    };

    const handleMouseLeave = () => {
      const foreground = container.querySelector('.foreground-layer') as HTMLElement;
      const background = container.querySelector('.background-layer') as HTMLElement;
      
      if (foreground && background) {
        foreground.style.opacity = '0';
        background.style.opacity = '1';
      }
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
      className={`spinning-leg ${className}`.trim()}
      style={{ position: 'relative', width: '100%', height: '100%' }}
    >
      {/* Body spin animation - shows on hover */}
      <img
        src="/assets/projects/opensim2real/leg-spin-body-small.gif"
        alt="OpenSim2Real spinning leg body animation"
        className="foreground-layer"
        loading="lazy"
        style={{ 
          opacity: 0,
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          objectFit: 'contain'
        }}
      />
      {/* Edge spin animation - shows by default */}
      <img
        src="/assets/projects/opensim2real/leg-spin-edge-small.gif"
        alt="OpenSim2Real spinning leg edge animation"
        className="background-layer"
        loading="lazy"
        style={{ 
          opacity: 1,
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          objectFit: 'contain'
        }}
      />
    </div>
  );
};
