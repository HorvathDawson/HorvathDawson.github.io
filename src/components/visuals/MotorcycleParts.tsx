import React, { useRef, useEffect } from 'react';
import { useVisualsForceHover } from './VisualsContext';

export interface MotorcyclePartsProps {
  className?: string;
  forceHover?: boolean;
}

export const MotorcycleParts: React.FC<MotorcyclePartsProps> = ({ 
  className = '',
  forceHover
}) => {
  const contextForce = useVisualsForceHover();
  const effectiveForceHover = forceHover ?? contextForce ?? false;
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleMouseEnter = () => {
      if (effectiveForceHover) return;
      const foreground = container.querySelector('.foreground-layer') as HTMLElement;
      const backgrounds = container.querySelectorAll('.background-layer:not([data-part])') as NodeListOf<HTMLElement>;
      
      if (foreground) foreground.style.opacity = '1';
      backgrounds.forEach(el => el.style.opacity = '0');
    };

    const handleMouseLeave = () => {
      if (effectiveForceHover) return;
      const foreground = container.querySelector('.foreground-layer') as HTMLElement;
      const backgrounds = container.querySelectorAll('.background-layer:not([data-part])') as NodeListOf<HTMLElement>;
      
      if (foreground) foreground.style.opacity = '0';
      backgrounds.forEach(el => el.style.opacity = '1');
    };

    container.addEventListener('mouseenter', handleMouseEnter);
    container.addEventListener('mouseleave', handleMouseLeave);

    // Scroll-based explosion animation is handled by parent component via App.tsx
    // The parts with data-part="1", "2", etc. will be animated by the global scroll handler

    return () => {
      container.removeEventListener('mouseenter', handleMouseEnter);
      container.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, []);



  return (
    <div 
      ref={containerRef}
      data-motorcycle-parts
      className={className}
      style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}
    >
      <div style={{ width: 900, height: 700, maxWidth: '100%', maxHeight: '100%', position: 'relative' }}>
        {/* Section view animation - shows on hover */}
        <img
          src="/assets/projects/buell/motor_images/section-view.gif"
          alt="Buell motorcycle engine section view"
          className="foreground-layer"
          loading="lazy"
          style={{ 
            opacity: effectiveForceHover ? 1 : 0,
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            objectFit: 'contain',
            zIndex: 5
          }}
        />
      
      {/* Static engine case - shows by default */}
      <img
        src="/assets/projects/buell/motor_images/case.png"
        alt="Buell motorcycle engine case"
        className="background-layer"
        loading="lazy"
        style={{ 
          opacity: effectiveForceHover ? 0 : 1,
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          zIndex: 4
        }}
      />
      
      {/* Left cylinder - shows by default */}
      <img
        src="/assets/projects/buell/motor_images/left-cylinder.png"
        alt="Buell motorcycle left cylinder"
        className="background-layer"
        loading="lazy"
        style={{ 
          opacity: effectiveForceHover ? 0 : 1,
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          zIndex: 4
        }}
      />
      
  {/* Exploding parts - animated by scroll */}
    <img
      src="/assets/projects/buell/motor_images/cylinder-barrel.png"
      alt="Buell motorcycle cylinder barrel"
      data-part="1"
      className="background-layer"
        loading="lazy"
        style={{ 
          opacity: effectiveForceHover ? 0 : 1,
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          zIndex: 4
        }}
      />
      <img
        src="/assets/projects/buell/motor_images/rocker-box.png"
        alt="Buell motorcycle rocker box"
        data-part="2"
        className="background-layer"
        loading="lazy"
        style={{ 
          opacity: effectiveForceHover ? 0 : 1,
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          zIndex: 4
        }}
      />
      <img
        src="/assets/projects/buell/motor_images/rocker-box-top.png"
        alt="Buell motorcycle rocker box top"
        data-part="3"
        className="background-layer"
        loading="lazy"
        style={{ 
          opacity: effectiveForceHover ? 0 : 1,
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          zIndex: 4
        }}
      />
      <img
        src="/assets/projects/buell/motor_images/push-rods.png"
        alt="Buell motorcycle push rods"
        data-part="4"
        className="background-layer"
        loading="lazy"
        style={{ 
          opacity: effectiveForceHover ? 0 : 1,
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          zIndex: 4
        }}
      />
      </div>
    </div>
  );
};
