import React, { useRef, useEffect } from 'react';
import { useVisualsForceHover } from './VisualsContext';

export interface LaptopWithScreenProps {
  className?: string;
  forceHover?: boolean;
}

export const LaptopWithScreen: React.FC<LaptopWithScreenProps> = ({
  className = '',
  forceHover
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const contextForce = useVisualsForceHover();
  const effectiveForceHover = forceHover ?? contextForce ?? false;

  // ... (Keep existing useEffect resize logic exactly as is) ...
  useEffect(() => {
    const container = containerRef.current;
    const content = contentRef.current;
    if (!container || !content) return;

    const updateSize = () => {
      if (!container || !content) return;
      const parent = container.parentElement;
      if (!parent) return;

      const parentRect = parent.getBoundingClientRect();
      const parentWidth = parentRect.width;
      const parentHeight = parentRect.height;
      if (parentWidth === 0 || parentHeight === 0) return;

      const targetAspectRatio = 1000 / 700; 
      const parentAspectRatio = parentWidth / parentHeight;
      let width, height;

      if (parentAspectRatio > targetAspectRatio) {
        height = parentHeight;
        width = height * targetAspectRatio;
      } else {
        width = parentWidth;
        height = width / targetAspectRatio;
      }
      content.style.width = `${width}px`;
      content.style.height = `${height}px`;
    };

    const observer = new ResizeObserver(updateSize);
    if (container.parentElement) observer.observe(container.parentElement);
    window.addEventListener('resize', updateSize);
    requestAnimationFrame(updateSize);

    const handleMouseEnter = () => {
      if (effectiveForceHover) return;
      const foregrounds = container.querySelectorAll('.foreground-layer') as NodeListOf<HTMLElement>;
      const backgrounds = container.querySelectorAll('.background-layer') as NodeListOf<HTMLElement>;
      const screens = container.querySelectorAll('.computer-screen') as NodeListOf<HTMLElement>;
      foregrounds.forEach(el => el.style.opacity = '1');
      backgrounds.forEach(el => el.style.opacity = '0');
      screens.forEach(el => el.style.opacity = '1');
    };

    const handleMouseLeave = () => {
      if (effectiveForceHover) return;
      const foregrounds = container.querySelectorAll('.foreground-layer') as NodeListOf<HTMLElement>;
      const backgrounds = container.querySelectorAll('.background-layer') as NodeListOf<HTMLElement>;
      const screens = container.querySelectorAll('.computer-screen') as NodeListOf<HTMLElement>;
      foregrounds.forEach(el => el.style.opacity = '0');
      backgrounds.forEach(el => el.style.opacity = '1');
      screens.forEach(el => el.style.opacity = '0');
    };

    container.addEventListener('mouseenter', handleMouseEnter);
    container.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      observer.disconnect();
      window.removeEventListener('resize', updateSize);
      container.removeEventListener('mouseenter', handleMouseEnter);
      container.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, []);

  return (
    <div
      ref={containerRef}
      data-laptop-with-screen
      className={className}
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'visible'
      }}
    >
      <div
        ref={contentRef}
        style={{
          position: 'relative',
          aspectRatio: '10 / 7',
          // KEY CHANGE: Removed 'preserve-3d'. 
          // This flattens the scene. The browser will render layers based strictly on z-index.
        //   perspective: '1000px', 
          overflow: 'visible'
        }}
      >
        {/* === SCREEN CONTAINER === */}
        <div
          data-laptop-screen
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            top: '-30%',
            transformOrigin: '50% 100%', 
            transformStyle: 'preserve-3d', // Keep this internal 3D for the screen itself
            // FORCE VISIBILITY: High z-index ensures it sits on top of the keyboard 
            // and the background, regardless of rotation angle.
            zIndex: 20 
          }}
        >
          <div
            style={{
              width: '75%',
              aspectRatio: '300 / 194',
              position: 'absolute',
              left: '50%',
              top: '100%',
              transform: 'translate(-50%, -100%)',
            }}
          >
            <img src="/assets/projects/self-driving-car/computer-foreground.svg" alt="" className="foreground-layer" loading="lazy" style={{ opacity: effectiveForceHover ? 1 : 0, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain', zIndex: 3 }} />
            <img src="/assets/projects/self-driving-car/computer-background.svg" alt="" className="background-layer" loading="lazy" style={{ opacity: effectiveForceHover ? 0 : 1, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain', zIndex: 1 }} />
            <div className="splash-layer computer-screen" style={{ opacity: effectiveForceHover ? 1 : 0, position: 'absolute', top: '10%', left: '4%', width: '92%', height: '84%', backgroundSize: 'cover', backgroundPosition: 'center', backgroundImage: 'url(/assets/projects/self-driving-car/screen.gif)', zIndex: 6 }} />
          </div>
        </div>

        {/* === KEYBOARD CONTAINER === */}
        <div
          data-laptop-keyboard
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            top: '70%',
            transformOrigin: '50% 50%',
            // Lower z-index means it will always be behind the screen
            zIndex: 10 
          }}
        >
          <div
            style={{
              width: '97%',
              aspectRatio: '300 / 61',
              position: 'absolute',
              left: '50%',
              top: '0%',
              transform: 'translate(-50%, 0%)',
              zIndex: 10
            }}
          >
             <img src="/assets/projects/self-driving-car/computer-keys-foreground.svg" alt="" className="foreground-layer" loading="lazy" style={{ opacity: effectiveForceHover ? 1 : 0, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain', zIndex: 10 }} />
             <img src="/assets/projects/self-driving-car/computer-keys-background.svg" alt="" className="background-layer" loading="lazy" style={{ opacity: effectiveForceHover ? 0 : 1, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain', zIndex: 10 }} />
          </div>
        </div>
      </div>
    </div>
  );
};